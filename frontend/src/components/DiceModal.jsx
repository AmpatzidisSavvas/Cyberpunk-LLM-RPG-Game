import React from 'react';

export default function DiceModal({
  rolling,
  rollData,
  rollFinished,
  animatedRollValue,
  onClose
}) {
  if (!rolling || !rollData) return null;

  return (
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
              {rollData.success ? "✅ WIN" : "💀 LOST"}
            </div>

            <button
              onClick={onClose}
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
  );
}