import React from 'react';

const FactionReputationWidget = ({ reputation }) => {
  if (!reputation || Object.keys(reputation).length === 0) return null;

  const getStandingTier = (score) => {
    if (score >= 80) return { label: 'EXALTED', color: 'text-[#00ff9f]', glow: 'shadow-[0_0_8px_#00ff9f]' };
    if (score >= 40) return { label: 'TRUSTED', color: 'text-[#00f3ff]', glow: 'shadow-[0_0_8px_#00f3ff]' };
    if (score > -40) return { label: 'NEUTRAL', color: 'text-gray-400', glow: '' };
    if (score > -80) return { label: 'HOSTILE', color: 'text-[#ffaa00]', glow: 'shadow-[0_0_8px_#ffaa00]' };
    return { label: 'HUNTED', color: 'text-[#ff0055]', glow: 'shadow-[0_0_8px_#ff0055]' };
  };

  return (
    <div className="border border-[#00f3ff]/30 bg-[#0d0f1d]/95 rounded-xl p-4 shadow-[0_0_20px_rgba(0,243,255,0.08)] font-mono">
      {/* Header */}
      <h3 className="text-xs uppercase tracking-widest text-[#00f3ff] mb-4 border-b border-[#00f3ff]/20 pb-1.5 flex justify-between items-center">
        <span className="flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 bg-[#00f3ff] animate-pulse rounded-full" />
          FACTION STANDINGS
        </span>
      </h3>

      {/* Faction List */}
      <div className="space-y-4 text-xs">
        {Object.entries(reputation).map(([faction, rawScore]) => {
          const score = Math.max(-100, Math.min(100, rawScore));
          const tier = getStandingTier(score);
          // Each segment represents 20 points (5 negative, 5 positive)
          const activeSegments = Math.round(Math.abs(score) / 20);

          return (
            <div key={faction} className="group">
              {/* Top Row: Name + Standing Label + Numeric Value */}
              <div className="flex justify-between items-baseline uppercase tracking-wider mb-1.5">
                <span className="text-gray-200 font-semibold group-hover:text-white transition-colors">
                  {faction}
                </span>
                <div className="flex items-center gap-2">
                  <span className={`text-[10px] px-1.5 py-0.2 rounded bg-black/50 border border-white/10 ${tier.color}`}>
                    {tier.label}
                  </span>
                  <span className={`font-bold w-9 text-right ${tier.color}`}>
                    {score > 0 ? `+${score}` : score}
                  </span>
                </div>
              </div>

              {/* Segmented Gauge */}
              <div className="flex items-center gap-1.5">
                {/* Negative Half (-100 to -20) */}
                <div className="flex-1 grid grid-cols-5 gap-1">
                  {[5, 4, 3, 2, 1].map((step) => {
                    const isActive = score < 0 && activeSegments >= step;
                    return (
                      <div
                        key={`neg-${step}`}
                        className={`h-2 rounded-[1px] transition-all duration-300 ${
                          isActive
                            ? 'bg-[#ff0055] shadow-[0_0_6px_rgba(255,0,85,0.6)]'
                            : 'bg-white/5 border border-white/5'
                        }`}
                      />
                    );
                  })}
                </div>

                {/* Center Zero Pivot */}
                <div className="w-1 h-3 bg-[#00f3ff]/50 rounded-full" title="Neutral (0)" />

                {/* Positive Half (+20 to +100) */}
                <div className="flex-1 grid grid-cols-5 gap-1">
                  {[1, 2, 3, 4, 5].map((step) => {
                    const isActive = score > 0 && activeSegments >= step;
                    return (
                      <div
                        key={`pos-${step}`}
                        className={`h-2 rounded-[1px] transition-all duration-300 ${
                          isActive
                            ? 'bg-[#00ff9f] shadow-[0_0_6px_rgba(0,255,159,0.6)]'
                            : 'bg-white/5 border border-white/5'
                        }`}
                      />
                    );
                  })}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default FactionReputationWidget;