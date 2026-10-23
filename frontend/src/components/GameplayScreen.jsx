import React from 'react';
import HeaderHUD from './HeaderHUD';
import TerminalLog from './TerminalLog';
import ActionButtons from './ActionButtons';
import OperativeSidebar from './OperativeSidebar';
import DiceModal from './DiceModal';
import MatrixBackground from './MatrixBackground';

export default function GameplayScreen({
  player,
  logs,
  loading,
  crtEnabled,
  setCrtEnabled,
  isGameOver,
  suggestedActions,
  handleAction,
  onSwitchClass,
  rolling,
  rollData,
  rollFinished,
  animatedRollValue,
  handleCloseDiceModal
}) {
  // Helper to format faction scores with color coding (-100 to +100)
  const getRepColor = (score) => {
    if (score > 20) return "text-[#00ff9f] drop-shadow-[0_0_5px_rgba(0,255,159,0.5)]";
    if (score < -20) return "text-[#ff0055] drop-shadow-[0_0_5px_rgba(255,0,85,0.5)]";
    return "text-[#00f3ff]/70";
  };

  return (
    <div className="relative min-h-screen bg-[#080811] text-[#00ff9f] p-4 md:p-8 flex flex-col font-mono selection:bg-[#ff0055] selection:text-white">
      
      <MatrixBackground />
      
      {/* Dice Roll Modal (Displays d20 roll, modifiers, and effective DC) */}
      <DiceModal 
        rolling={rolling}
        rollData={rollData}
        rollFinished={rollFinished}
        animatedRollValue={animatedRollValue}
        onClose={handleCloseDiceModal}
      />

      {/* Header HUD */}
      {player && (
        <HeaderHUD 
          player={player} 
          crtEnabled={crtEnabled} 
          setCrtEnabled={setCrtEnabled} 
        />
      )}

      {/* Main Gameplay Layout */}
      <div className="z-20 flex-1 grid grid-cols-1 lg:grid-cols-4 gap-6 mt-4">
        
        {/* Left / Center: Console & Terminal Section */}
        <div className="lg:col-span-3 flex flex-col border border-[#00f3ff]/30 bg-[#0d0f1d]/80 rounded-xl p-4 h-[640px] shadow-[0_0_25px_rgba(0,243,255,0.08)]">
          <TerminalLog logs={logs} loading={loading} crtEnabled={crtEnabled} />
          
          {!isGameOver ? (
            <ActionButtons 
              suggestedActions={suggestedActions} 
              handleAction={handleAction} 
              loading={loading} 
            />
          ) : (
            <div className="p-4 border border-[#00ff9f]/40 bg-[#00ff9f]/10 rounded-lg text-center mt-auto my-2">
              <p className="text-sm font-bold text-[#00ff9f] mb-3 tracking-widest">
                ❖ STORY CONCLUSION REACHED ❖
              </p>
              <button
                onClick={onSwitchClass}
                className="bg-[#00f3ff] hover:bg-[#00ff9f] text-black font-bold px-6 py-2 rounded text-xs transition-all tracking-wider shadow-[0_0_15px_rgba(0,243,255,0.4)]"
              >
                START NEW OPERATIVE MISSION
              </button>
            </div>
          )}
        </div>

        {/* Right Sidebar: Character Data & Faction Standings */}
        <div className="flex flex-col gap-6">
          
          {/* Character Inventory & Profile Sidebar */}
          <OperativeSidebar 
            player={player} 
            onSwitchClass={onSwitchClass} 
          />

          {/* Faction Reputation Widget */}
          {player && player.reputation && (
            <div className="border border-[#00f3ff]/20 bg-[#0d0f1d]/90 rounded-xl p-4 shadow-[0_0_15px_rgba(0,243,255,0.05)]">
              <h3 className="text-xs uppercase tracking-widest text-[#00f3ff] mb-3 border-b border-[#00f3ff]/20 pb-1 flex justify-between items-center">
                <span>[FACTION STANDINGS]</span>
                <span className="text-[10px] text-gray-400">[-100 / +100]</span>
              </h3>
              
              <div className="space-y-3 text-xs">
                {Object.entries(player.reputation).map(([faction, score]) => (
                  <div key={faction} className="flex flex-col">
                    <div className="flex justify-between uppercase tracking-wider mb-1">
                      <span className="text-gray-300">{faction}</span>
                      <span className={`font-bold ${getRepColor(score)}`}>
                        {score > 0 ? `+${score}` : score}
                      </span>
                    </div>
                    {/* Progress Bar representation */}
                    <div className="w-full bg-black/60 h-1.5 rounded-full overflow-hidden border border-[#00f3ff]/10">
                      <div 
                        className={`h-full transition-all duration-500 ${score >= 0 ? 'bg-[#00ff9f]' : 'bg-[#ff0055]'}`}
                        style={{ 
                          width: `${Math.min(100, Math.abs(score))}%`, 
                          marginLeft: score < 0 ? `${50 - Math.abs(score)/2}%` : '50%'
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}