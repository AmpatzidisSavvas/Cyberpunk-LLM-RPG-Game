import React from 'react';

export default function DiceModal({
  rolling,
  rollData,
  rollFinished,
  animatedRollValue,
  onClose
}) {
  if (!rolling || !rollData) return null;

  const modifier = rollData.modifier ?? 0;
  const displayedDieValue = rollFinished
    ? (rollData.roll ?? rollData.total - modifier)
    : animatedRollValue;

  const isCritSuccess = rollFinished && displayedDieValue === 20;
  const isCritFail = rollFinished && displayedDieValue === 1;
  const minSuccessDieRoll = Math.max(1, rollData.dc - modifier);

  const accentColor = !rollFinished
    ? "#00f3ff"
    : rollData.success
      ? "#00ff9f"
      : "#ff0055";

  const glowFilter = !rollFinished
    ? "drop-shadow(0 0 12px rgba(0, 243, 255, 0.75))"
    : rollData.success
      ? "drop-shadow(0 0 20px rgba(0, 255, 159, 0.9))"
      : "drop-shadow(0 0 20px rgba(255, 0, 85, 0.9))";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md">
      <div
        className={`border-2 border-[#00f3ff] bg-[#0d0f1d] p-8 rounded-2xl max-w-sm w-full text-center shadow-[0_0_50px_rgba(0,243,255,0.4)] ${
          isCritFail ? "animate-modal-shake" : ""
        }`}
      >
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
              {rollFinished ? rollData.total : animatedRollValue + modifier}
            </div>
          </div>
        </div>

        {/* Clean Cyberpunk D20 — Number Only in the Center */}
        <div className="relative my-3 flex items-center justify-center">
          <div
            className="absolute w-28 h-28 rounded-full blur-xl opacity-30 transition-colors duration-300"
            style={{ backgroundColor: accentColor }}
          />

          <div
            className={`relative w-36 h-36 flex items-center justify-center ${
              rollFinished ? "animate-d20-land" : "animate-d20-roll"
            }`}
            style={{ filter: glowFilter }}
          >
            <svg
              viewBox="0 0 120 120"
              className="w-full h-full overflow-visible"
              aria-label={`D20 showing ${displayedDieValue}`}
            >
              {/* Outer hexagonal d20 silhouette */}
              <polygon
                points="60,6 108,33 108,87 60,114 12,87 12,33"
                fill="#070913"
                stroke={accentColor}
                strokeWidth="2.5"
                strokeLinejoin="round"
              />

              {/* Subtle 3D facet shading */}
              <polygon
                points="60,6 108,33 88,45 60,26"
                fill={accentColor}
                fillOpacity="0.14"
              />
              <polygon
                points="12,87 60,114 60,94 32,75"
                fill={accentColor}
                fillOpacity="0.08"
              />

              {/* Center face */}
              <polygon
                points="60,26 88,75 32,75"
                fill="#0b0e1e"
                stroke={accentColor}
                strokeWidth="2"
                strokeLinejoin="round"
              />

              {/* Clean icosahedron edge lines */}
              <g stroke={accentColor} strokeWidth="1.35" strokeOpacity="0.8">
                <line x1="60" y1="6" x2="60" y2="26" />
                <line x1="108" y1="33" x2="60" y2="26" />
                <line x1="108" y1="33" x2="88" y2="75" />
                <line x1="108" y1="87" x2="88" y2="75" />
                <line x1="60" y1="114" x2="88" y2="75" />
                <line x1="60" y1="114" x2="32" y2="75" />
                <line x1="12" y1="87" x2="32" y2="75" />
                <line x1="12" y1="33" x2="32" y2="75" />
                <line x1="12" y1="33" x2="60" y2="26" />
              </g>

              {/* Corner vertices */}
              <g fill={accentColor}>
                <circle cx="60" cy="6" r="2.2" />
                <circle cx="108" cy="33" r="2.2" />
                <circle cx="108" cy="87" r="2.2" />
                <circle cx="60" cy="114" r="2.2" />
                <circle cx="12" cy="87" r="2.2" />
                <circle cx="12" cy="33" r="2.2" />
              </g>

              {/* Single rolled/winning number in the center face */}
              <text
                x="60"
                y="60"
                textAnchor="middle"
                dominantBaseline="central"
                fill={accentColor}
                fontSize="22"
                fontWeight="900"
                className="select-none transition-colors duration-300"
                style={{ textShadow: `0 0 12px ${accentColor}` }}
              >
                {displayedDieValue}
              </text>
            </svg>
          </div>
        </div>

        

        <div className="text-[12px] text-gray-400 mb-5 mt-1">
          Boost: <span className="text-[#00ff9f]">+{modifier}</span>
          
        </div>

        {/* Final Result Banner & Manual Close Button */}
        {rollFinished ? (
          <div className="space-y-4">
            <div
              className={`py-2 px-4 rounded text-xs font-black tracking-widest uppercase flex items-center justify-center gap-2 ${
                rollData.success
                  ? "bg-[#00ff9f]/20 border border-[#00ff9f] text-[#00ff9f] shadow-[0_0_15px_rgba(0,255,159,0.5)]"
                  : "bg-[#ff0055]/20 border border-[#ff0055] text-[#ff0055] shadow-[0_0_15px_rgba(255,0,85,0.5)]"
              }`}
            >
              {rollData.success
                ? `✅ SUCCESS`
                : `💀 FAILED`}
            </div>

            <button
              onClick={onClose}
              className="w-full bg-[#00f3ff] hover:bg-[#00ff9f] text-black font-bold py-2 px-4 rounded text-xs transition-all tracking-wider shadow-[0_0_15px_rgba(0,243,255,0.4)] uppercase cursor-pointer"
            >
              [ DISMISS TERMINAL ]
            </button>
          </div>
        ) : (
          <div className="text-xs text-[#00f3ff] animate-pulse tracking-widest">
            Rolling Dice...
          </div>
        )}
      </div>
    </div>
  );
}