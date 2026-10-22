import React, { useState, useEffect } from 'react';
import axios from 'axios';
import HeaderHUD from './components/HeaderHUD';
import TerminalLog from './components/TerminalLog';
import ActionButtons from './components/ActionButtons';
import ActionInput from './components/ActionInput';
import InventoryPanel from './components/InventoryPanel';
import { sounds } from './utils/audio';

export default function App() {
  const [step, setStep] = useState('SELECT_CLASS'); // 'SELECT_CLASS' or 'GAME'
  const [classesData, setClassesData] = useState({});
  const [loadingClasses, setLoadingClasses] = useState(true);

  const [player, setPlayer] = useState(null);
  const [logs, setLogs] = useState([]);
  const [input, setInput] = useState("");
  const [suggestedActions, setSuggestedActions] = useState([]);
  const [isGameOver, setIsGameOver] = useState(false);
  const [loading, setLoading] = useState(false);
  const [crtEnabled, setCrtEnabled] = useState(true);

  // --- DICE ROLL MODAL STATE ---
  const [rolling, setRolling] = useState(false);
  const [animatedRollValue, setAnimatedRollValue] = useState(1);
  const [rollData, setRollData] = useState(null);
  const [rollFinished, setRollFinished] = useState(false);
  const [pendingResponse, setPendingResponse] = useState(null);

  // 1. Fetch available classes from backend on initial load
  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/classes')
      .then((res) => {
        setClassesData(res.data);
        setLoadingClasses(false);
      })
      .catch((err) => {
        console.error("Could not fetch classes from backend:", err);
        setLoadingClasses(false);
      });
  }, []);

  // 2. Start game session via backend API
  const handleSelectClass = async (roleName, info) => {
    if (sounds?.playCyberHack) sounds.playCyberHack();

    const selectedPlayer = {
      name: "V-2077",
      role: roleName,
      hp: info.hp,
      max_hp: info.max_hp,
      eddies: info.eddies,
      inventory: [...info.inventory],
      location: info.location,
      stats: info.stats || { HACKING: 1, COMBAT: 1, TECH: 1 }
    };

    setPlayer(selectedPlayer);
    setLoading(true);
    setIsGameOver(false);
    setStep('GAME');

    try {
      const res = await axios.post('http://127.0.0.1:8000/api/start', selectedPlayer);
      const { system_log, story } = res.data;

      setLogs([
        { sender: "SYSTEM", text: system_log },
        { sender: "STORY", text: story.narrative }
      ]);
      setSuggestedActions(story.suggested_actions || []);
      
      if (story.new_location) {
        setPlayer(prev => ({ ...prev, location: story.new_location }));
      }
    } catch (err) {
      setLogs([{ sender: "SYSTEM", text: "ERROR: UNABLE TO FETCH INITIAL STARTING DATA FROM BACKEND." }]);
    } finally {
      setLoading(false);
    }
  };

  // 3. Dice Roll Animation Helper
  const triggerDiceRollAnimation = (rollInfo, responseData) => {
    setRollData(rollInfo);
    setPendingResponse(responseData);
    setRolling(true);
    setRollFinished(false);

    let counter = 0;
    const interval = setInterval(() => {
      setAnimatedRollValue(Math.floor(Math.random() * 20) + 1);
      counter++;
      if (counter > 15) {
        clearInterval(interval);
        setAnimatedRollValue(rollInfo.d20_roll); // Lock on actual backend roll
        setRollFinished(true);
        if (sounds?.playCyberHack) sounds.playCyberHack();
      }
    }, 70);
  };

  // 4. Manual Close Handler for the Dice Modal
  const handleCloseDiceModal = () => {
    if (!pendingResponse || !rollData) return;

    const { stat_used, d20_roll, modifier, total, dc, success } = rollData;
    
    // Log explanation with skull on failure or green tick on success
    const icon = success ? "✅" : "💀";
    const outcomeText = success ? "SUCCESS" : "CRITICAL FAILURE";
    const rollLog = `[CHECK: ${stat_used}] 🎲 d20(${d20_roll}) + Mod(${modifier}) = ${total} vs DC ${dc} ➔ ${outcomeText} ${icon}`;

    setLogs(prev => [
      ...prev,
      { sender: "SYSTEM", text: rollLog },
      { sender: "STORY", text: pendingResponse.narrative }
    ]);

    setPlayer(prev => {
      let updatedInv = [...prev.inventory];
      if (pendingResponse.new_items) updatedInv.push(...pendingResponse.new_items);
      if (pendingResponse.lost_items) updatedInv = updatedInv.filter(i => !pendingResponse.lost_items.includes(i));

      return {
        ...prev,
        hp: Math.min(prev.max_hp, Math.max(0, prev.hp + (pendingResponse.hp_change || 0))),
        eddies: Math.max(0, prev.eddies + (pendingResponse.eddies_change || 0)),
        inventory: updatedInv,
        location: pendingResponse.new_location || prev.location
      };
    });

    if (pendingResponse.is_game_over) {
      setIsGameOver(true);
      setSuggestedActions([]);
    } else if (pendingResponse.suggested_actions) {
      setSuggestedActions(pendingResponse.suggested_actions);
    }

    // Reset dice modal state
    setRolling(false);
    setRollData(null);
    setPendingResponse(null);
    setRollFinished(false);
  };

  // 5. Send player action to backend API
  const handleAction = async (actionText) => {
    const userAction = actionText || input;
    if (!userAction.trim() || loading || isGameOver) return;

    if (sounds?.playCyberHack) sounds.playCyberHack();

    const updatedLogs = [...logs, { sender: "PLAYER", text: userAction }];
    setLogs(updatedLogs);
    setInput("");
    setLoading(true);

    try {
      const historyStrings = updatedLogs.map(l => `${l.sender}: ${l.text}`);
      const res = await axios.post('http://127.0.0.1:8000/api/action', {
        action: userAction,
        player_state: player,
        history: historyStrings
      });

      const data = res.data;

      // If backend executed a dice check, trigger animation overlay
      if (data.roll) {
        triggerDiceRollAnimation(data.roll, data);
      } else {
        // Standard action without roll
        setLogs(prev => [...prev, { sender: "STORY", text: data.narrative }]);

        setPlayer(prev => {
          let updatedInv = [...prev.inventory];
          if (data.new_items) updatedInv.push(...data.new_items);
          if (data.lost_items) updatedInv = updatedInv.filter(i => !data.lost_items.includes(i));

          return {
            ...prev,
            hp: Math.min(prev.max_hp, Math.max(0, prev.hp + (data.hp_change || 0))),
            eddies: Math.max(0, prev.eddies + (data.eddies_change || 0)),
            inventory: updatedInv,
            location: data.new_location || prev.location
          };
        });

        if (data.is_game_over) {
          setIsGameOver(true);
          setSuggestedActions([]);
        } else if (data.suggested_actions) {
          setSuggestedActions(data.suggested_actions);
        }
      }
    } catch (err) {
      setLogs(prev => [...prev, { sender: "SYSTEM", text: "ERROR: NEURAL LINK DISRUPTED. BACKEND UNREACHABLE." }]);
    } finally {
      setLoading(false);
    }
  };

  // 6. Handle using inventory items via backend API
  const handleUseItem = async (itemName) => {
    if (loading || isGameOver) return;
    setLoading(true);

    try {
      const res = await axios.post('http://127.0.0.1:8000/api/use-item', {
        ...player,
        item_name: itemName
      });

      const data = res.data;

      setLogs(prev => [...prev, { sender: "SYSTEM", text: data.narrative }]);

      setPlayer(prev => {
        let updatedInv = [...prev.inventory];
        if (data.lost_items) updatedInv = updatedInv.filter(i => !data.lost_items.includes(i));
        if (data.new_items) updatedInv.push(...data.new_items);

        return {
          ...prev,
          hp: Math.min(prev.max_hp, Math.max(0, prev.hp + (data.hp_change || 0))),
          eddies: Math.max(0, prev.eddies + (data.eddies_change || 0)),
          inventory: updatedInv
        };
      });
    } catch (err) {
      setLogs(prev => [...prev, { sender: "SYSTEM", text: "ERROR: UNABLE TO USE ITEM." }]);
    } finally {
      setLoading(false);
    }
  };

  // --- SCREEN 1: CLASS SELECTION ---
  if (step === 'SELECT_CLASS') {
    return (
      <div className="relative min-h-screen bg-[#080811] text-[#00ff9f] p-4 md:p-8 flex flex-col items-center justify-center font-mono selection:bg-[#ff0055] selection:text-white">
        <div className="z-20 max-w-4xl w-full border border-[#00f3ff]/40 bg-[#0d0f1d]/90 p-8 rounded-xl shadow-[0_0_30px_rgba(0,243,255,0.12)]">
          <h1 className="text-3xl font-extrabold text-center tracking-widest text-[#00f3ff] mb-2 drop-shadow-[0_0_10px_rgba(0,243,255,0.5)]">
            NEO_THESSALONIK_GRID // OPERATIVE CREATION
          </h1>
          <p className="text-center text-xs text-[#00ff9f]/70 mb-8 tracking-widest uppercase">
            Select an operative archetype to synchronize neural link
          </p>

          {loadingClasses ? (
            <div className="text-center text-[#ff0055] animate-pulse">
              [CONNECTING TO BACKEND CLASS DATABASE...]
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {Object.entries(classesData).map(([roleName, info]) => (
                <div
                  key={roleName}
                  onClick={() => handleSelectClass(roleName, info)}
                  className="border border-[#00f3ff]/30 bg-[#080811]/80 p-5 rounded-lg flex flex-col justify-between hover:border-[#00ff9f] hover:shadow-[0_0_20px_rgba(0,255,159,0.25)] transition-all cursor-pointer group"
                >
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <h2 className="text-xl font-bold text-[#00f3ff] group-hover:text-[#00ff9f] transition-colors">
                        {roleName}
                      </h2>
                      <span className="text-[10px] text-[#ff0055] border border-[#ff0055]/40 px-1.5 py-0.5 rounded">
                        CLASS
                      </span>
                    </div>
                    <p className="text-xs text-gray-400 mb-4 leading-relaxed">
                      {info.description}
                    </p>
                    <div className="text-xs space-y-1 text-[#00ff9f]/80 mb-4 bg-[#0d0f1d] p-3 rounded border border-[#00f3ff]/10">
                      <div>❤️ HP: {info.hp}/{info.max_hp}</div>
                      <div>§ EDDIES: {info.eddies}</div>
                      <div className="truncate">🎒 GEAR: {info.inventory.join(', ')}</div>
                    </div>
                  </div>
                  <button className="w-full mt-2 bg-[#00f3ff]/10 border border-[#00f3ff]/50 text-[#00f3ff] group-hover:bg-[#00ff9f] group-hover:text-black group-hover:border-[#00ff9f] py-2 text-xs font-bold tracking-wider transition-all rounded">
                    SELECT {roleName.toUpperCase()}
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    );
  }

  // --- SCREEN 2: MAIN GAMEPLAY HUD ---
  return (
    <div className="relative min-h-screen bg-[#080811] text-[#00ff9f] p-4 md:p-8 flex flex-col font-mono selection:bg-[#ff0055] selection:text-white">
      
      {/* OVERLAY: CYBERPUNK DICE ROLL MODAL */}
      {rolling && rollData && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md">
          <div className="border-2 border-[#00f3ff] bg-[#0d0f1d] p-8 rounded-2xl max-w-sm w-full text-center shadow-[0_0_50px_rgba(0,243,255,0.4)]">
            <p className="text-xs text-[#00f3ff] tracking-widest uppercase mb-1">
              SKILL CHECK // {rollData.stat_used}
            </p>

            {/* VISUAL TARGET vs YOUR ROLL BOXES */}
            <div className="grid grid-cols-2 gap-4 my-4">
              {/* Target DC */}
              <div className="border border-[#ff0055]/50 bg-[#ff0055]/10 p-3 rounded-xl shadow-[0_0_15px_rgba(255,0,85,0.15)]">
                <div className="text-[10px] text-[#ff0055] font-bold tracking-widest uppercase mb-1">
                  ENEMY
                </div>
                <div className="text-3xl font-black text-[#ff0055] drop-shadow-[0_0_10px_#ff0055]">
                  {rollData.dc}
                </div>
              </div>

              {/* Your Total Roll */}
              <div className="border border-[#00f3ff]/50 bg-[#00f3ff]/10 p-3 rounded-xl shadow-[0_0_15px_rgba(0,243,255,0.15)]">
                <div className="text-[10px] text-[#00f3ff] font-bold tracking-widest uppercase mb-1">
                  YOUR TOTAL
                </div>
                <div className="text-3xl font-black text-[#00f3ff] drop-shadow-[0_0_10px_#00f3ff]">
                  {rollFinished ? rollData.total : animatedRollValue + rollData.modifier}
                </div>
              </div>
            </div>

            {/* Glowing d20 Die Frame */}
            <div className="w-16 h-16 mx-auto my-2 flex items-center justify-center border-2 border-[#00f3ff] bg-[#080811] rounded-lg shadow-[0_0_15px_rgba(0,243,255,0.4)] transform rotate-45">
              <span className="transform -rotate-45 text-xl font-black text-[#00f3ff]">
                {animatedRollValue}
              </span>
            </div>
            <div className="text-[10px] text-gray-400 mb-4">
              (Boost: <span className="text-[#00ff9f]">+{rollData.modifier}</span>)
            </div>

            {/* Final Result Banner & Manual Close Button */}
            {rollFinished ? (
              <div className="space-y-4">
                <div className={`py-2 px-4 rounded text-xs font-black tracking-widest uppercase flex items-center justify-center gap-2 ${
                  rollData.success 
                    ? "bg-[#00ff9f]/20 border border-[#00ff9f] text-[#00ff9f] shadow-[0_0_15px_rgba(0,255,159,0.5)]" 
                    : "bg-[#ff0055]/20 border border-[#ff0055] text-[#ff0055] shadow-[0_0_15px_rgba(255,0,85,0.5)]"
                }`}>
                  {rollData.success ? "✅ CHECK PASSED" : "💀 CHECK FAILED"}
                </div>

                <button
                  onClick={handleCloseDiceModal}
                  className="w-full bg-[#00f3ff] hover:bg-[#00ff9f] text-black font-bold py-2 px-4 rounded text-xs transition-all tracking-wider shadow-[0_0_15px_rgba(0,243,255,0.4)] uppercase"
                >
                  [ DISMISS TERMINAL ]
                </button>
              </div>
            ) : (
              <div className="text-xs text-[#00f3ff] animate-pulse">
                CALCULATING PROBABILITIES...
              </div>
            )}
          </div>
        </div>
      )}

      {player && (
        <HeaderHUD 
          player={player} 
          crtEnabled={crtEnabled} 
          setCrtEnabled={setCrtEnabled} 
        />
      )}

      <div className="z-20 flex-1 grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Console / Terminal Section */}
        <div className="lg:col-span-3 flex flex-col border border-[#00f3ff]/30 bg-[#0d0f1d]/80 rounded-xl p-4 h-[640px] shadow-[0_0_25px_rgba(0,243,255,0.08)]">
          <TerminalLog logs={logs} loading={loading} crtEnabled={crtEnabled} />
          
          {!isGameOver ? (
            <>
              <ActionButtons 
                suggestedActions={suggestedActions} 
                handleAction={handleAction} 
                loading={loading} 
              />
              <ActionInput 
                input={input} 
                setInput={setInput} 
                handleAction={handleAction} 
                loading={loading} 
              />
            </>
          ) : (
            <div className="p-4 border border-[#00ff9f]/40 bg-[#00ff9f]/10 rounded-lg text-center mt-auto my-2">
              <p className="text-sm font-bold text-[#00ff9f] mb-3 tracking-widest">
                ❖ STORY CONCLUSION REACHED ❖
              </p>
              <button
                onClick={() => setStep('SELECT_CLASS')}
                className="bg-[#00f3ff] hover:bg-[#00ff9f] text-black font-bold px-6 py-2 rounded text-xs transition-all tracking-wider shadow-[0_0_15px_rgba(0,243,255,0.4)]"
              >
                START NEW OPERATIVE MISSION
              </button>
            </div>
          )}
        </div>

        {/* Sidebar Inventory Section & Switch Class Button */}
        <div className="lg:col-span-1 flex flex-col gap-4">
          {player && (
            <InventoryPanel 
              inventory={player.inventory} 
              onUseItem={handleUseItem} 
            />
          )}
          
          <button
            onClick={() => setStep('SELECT_CLASS')}
            className="w-full border border-[#ff0055]/50 bg-[#ff0055]/10 hover:bg-[#ff0055] hover:text-black text-[#ff0055] text-xs font-bold py-2 rounded transition-all tracking-wider"
          >
            ← SWITCH OPERATIVE CLASS
          </button>
        </div>
      </div>
    </div>
  );
}