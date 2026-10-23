import React, { useState, useEffect } from "react";
import axios from "axios";

import ClassSelectionScreen from "./components/ClassSelection";
import GameplayScreen from "./components/GameplayScreen";
import { sounds } from "./utils/audio";

export default function App() {
    const [step, setStep] = useState("SELECT_CLASS");
    const [classesData, setClassesData] = useState({});
    const [loadingClasses, setLoadingClasses] = useState(true);

    const [player, setPlayer] = useState(null);
    const [logs, setLogs] = useState([]);
    const [input, setInput] = useState("");
    const [suggestedActions, setSuggestedActions] = useState([]);
    const [isGameOver, setIsGameOver] = useState(false);
    const [loading, setLoading] = useState(false);
    const [crtEnabled, setCrtEnabled] = useState(true);
    const [audioEnabled, setAudioEnabled] = useState(true);

    // --- DICE ROLL MODAL STATE ---
    const [rolling, setRolling] = useState(false);
    const [animatedRollValue, setAnimatedRollValue] = useState(1);
    const [rollData, setRollData] = useState(null);
    const [rollFinished, setRollFinished] = useState(false);
    const [pendingResponse, setPendingResponse] = useState(null);

    // 1. Fetch available classes on mount
    useEffect(() => {
        axios
            .get("http://127.0.0.1:8000/api/classes")
            .then((res) => {
                setClassesData(res.data);
                setLoadingClasses(false);
            })
            .catch((err) => {
                console.error("Could not fetch classes from backend:", err);
                setLoadingClasses(false);
            });
    }, []);

    // 2. Start game session
    const handleSelectClass = async (roleName, info) => {
        if (audioEnabled && sounds?.playCyberHack) sounds.playCyberHack();

        const selectedPlayer = {
            name: "V-2077",
            role: roleName,
            hp: info.hp,
            max_hp: info.max_hp,
            eddies: info.eddies,
            inventory: [...info.inventory],
            location: info.location,
            stats: info.stats || { HACKING: 1, COMBAT: 1, TECH: 1 },
            // ---> INITIALIZE DEFAULT FACTION REPUTATION <---
            reputation: {
                corporates: 0,
                underground: 0,
                law_enforcement: 0
            }
        };

        setPlayer(selectedPlayer);
        setLoading(true);
        setIsGameOver(false);
        setStep("GAME");

        try {
            const res = await axios.post("http://127.0.0.1:8000/api/start", selectedPlayer);
            const { system_log, story } = res.data;

            setLogs([
                { sender: "SYSTEM", text: system_log },
                { sender: "STORY", text: story.narrative }
            ]);
            setSuggestedActions(story.suggested_actions || []);

            if (story.new_location) {
                setPlayer((prev) => ({ ...prev, location: story.new_location }));
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
                setAnimatedRollValue(rollInfo.d20_roll);
                setRollFinished(true);
                if (audioEnabled && sounds?.playCyberHack) sounds.playCyberHack();
            }
        }, 70);
    };

    // 4. Dice Modal Close Handler
    const handleCloseDiceModal = () => {
        if (!pendingResponse || !rollData) return;

        const { stat_used, d20_roll, modifier, total, dc, effective_dc, rep_modifier, success } = rollData;
        const icon = success ? "✅" : "💀";
        const outcomeText = success ? "SUCCESS" : "CRITICAL FAILURE";
        
        // Show effective DC and reputation modifier in log if present
        const dcText = rep_modifier ? `Effective DC ${effective_dc} (Base ${dc}, Rep Mod ${rep_modifier > 0 ? `+${rep_modifier}` : rep_modifier})` : `DC ${dc}`;
        const rollLog = `[CHECK: ${stat_used}] 🎲 d20(${d20_roll}) + Mod(${modifier}) = ${total} vs ${dcText} ➔ ${outcomeText} ${icon}`;

        setLogs((prev) => [...prev, { sender: "SYSTEM", text: rollLog }, { sender: "STORY", text: pendingResponse.narrative }]);

        setPlayer((prev) => {
            let updatedInv = [...prev.inventory];
            if (pendingResponse.new_items) updatedInv.push(...pendingResponse.new_items);
            if (pendingResponse.lost_items) updatedInv = updatedInv.filter((i) => !pendingResponse.lost_items.includes(i));

            return {
                ...prev,
                hp: Math.min(prev.max_hp, Math.max(0, prev.hp + (pendingResponse.hp_change || 0))),
                eddies: Math.max(0, prev.eddies + (pendingResponse.eddies_change || 0)),
                inventory: updatedInv,
                location: pendingResponse.new_location || prev.location,
                // ---> SYNC REPUTATION FROM BACKEND RESPONSE <---
                reputation: pendingResponse.updated_reputation || prev.reputation
            };
        });

        if (pendingResponse.is_game_over) {
            setIsGameOver(true);
            setSuggestedActions([]);
        } else if (pendingResponse.suggested_actions) {
            setSuggestedActions(pendingResponse.suggested_actions);
        }

        setRolling(false);
        setRollData(null);
        setPendingResponse(null);
        setRollFinished(false);
    };

    // 5. Send action to backend
    const handleAction = async (actionText) => {
        const userAction = actionText || input;
        if (!userAction.trim() || loading || isGameOver) return;

        if (audioEnabled && sounds?.playCyberHack) sounds.playCyberHack();

        const updatedLogs = [...logs, { sender: "PLAYER", text: userAction }];
        setLogs(updatedLogs);
        setInput("");
        setLoading(true);

        try {
            const historyStrings = updatedLogs.map((l) => `${l.sender}: ${l.text}`);
            const res = await axios.post("http://127.0.0.1:8000/api/action", {
                action: userAction,
                player_state: player,
                history: historyStrings
            });

            const data = res.data;

            if (data.roll) {
                triggerDiceRollAnimation(data.roll, data);
            } else {
                setLogs((prev) => [...prev, { sender: "STORY", text: data.narrative }]);

                setPlayer((prev) => {
                    let updatedInv = [...prev.inventory];
                    if (data.new_items) updatedInv.push(...data.new_items);
                    if (data.lost_items) updatedInv = updatedInv.filter((i) => !data.lost_items.includes(i));

                    return {
                        ...prev,
                        hp: Math.min(prev.max_hp, Math.max(0, prev.hp + (data.hp_change || 0))),
                        eddies: Math.max(0, prev.eddies + (data.eddies_change || 0)),
                        inventory: updatedInv,
                        location: data.new_location || prev.location,
                        // ---> SYNC REPUTATION FROM BACKEND RESPONSE <---
                        reputation: data.updated_reputation || prev.reputation
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
            setLogs((prev) => [...prev, { sender: "SYSTEM", text: "ERROR: NEURAL LINK DISRUPTED. BACKEND UNREACHABLE." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-[#080811] text-white relative overflow-x-hidden">
            <main className="relative z-10">
                {step === "SELECT_CLASS" ? (
                    <ClassSelectionScreen classesData={classesData} loadingClasses={loadingClasses} onSelectClass={handleSelectClass} />
                ) : (
                    <GameplayScreen
                        player={player}
                        logs={logs}
                        loading={loading}
                        crtEnabled={crtEnabled}
                        setCrtEnabled={setCrtEnabled}
                        isGameOver={isGameOver}
                        suggestedActions={suggestedActions}
                        input={input}
                        setInput={setInput}
                        handleAction={handleAction}
                        onSwitchClass={() => setStep("SELECT_CLASS")}
                        rolling={rolling}
                        rollData={rollData}
                        rollFinished={rollFinished}
                        animatedRollValue={animatedRollValue}
                        handleCloseDiceModal={handleCloseDiceModal}
                    />
                )}
            </main>
        </div>
    );
}