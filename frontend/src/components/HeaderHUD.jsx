import React from 'react';
import { Terminal, Shield, Zap, DollarSign, MapPin, Cpu, Sliders } from 'lucide-react';

export default function HeaderHUD({ player, crtEnabled, setCrtEnabled, useMock, setUseMock }) {
  const hpPercent = Math.max(0, Math.min(100, (player.hp / player.max_hp) * 100));

  return (
    <header className="z-20 mb-6 border-b border-[#00f3ff]/30 pb-4 flex flex-wrap justify-between items-center gap-4 bg-[#0d0f1d]/60 backdrop-blur-md p-4 rounded-xl border border-[#00f3ff]/20">
      <div>
        <h1 className="text-2xl md:text-3xl font-black tracking-widest text-[#ff0055] drop-shadow-[0_0_10px_rgba(255,0,85,0.7)] flex items-center gap-2 uppercase">
          <Terminal className="animate-pulse text-[#00f3ff]" /> NEO-THESSALONIKI-STORIES
        </h1>
        <p className="text-xs text-[#00f3ff]/80 flex items-center gap-1 mt-1 font-mono tracking-wider">
          <MapPin size={12} className="text-[#ff0055]" /> {player.location}
        </p>
      </div>

      <div className="flex gap-3 flex-wrap items-center">
        {/* HP Bar */}
        <div className="bg-[#080811] px-3 py-2 rounded-lg border border-[#ff0055]/40 flex items-center gap-3 min-w-[160px]">
          <Shield className="text-[#ff0055] shrink-0" size={18} />
          <div className="flex-1">
            <div className="flex justify-between text-xs font-bold mb-1">
              <span className="text-gray-400">VIT</span>
              <span className="text-[#ff0055]">{player.hp}/{player.max_hp}</span>
            </div>
            <div className="w-full bg-gray-900 h-1.5 rounded-full overflow-hidden border border-[#ff0055]/30">
              <div 
                className="bg-[#ff0055] h-full transition-all duration-500 shadow-[0_0_8px_#ff0055]" 
                style={{ width: `${hpPercent}%` }}
              />
            </div>
          </div>
        </div>

        {/* Eddies */}
        <div className="bg-[#080811] px-3 py-2 rounded-lg border border-yellow-500/40 flex items-center gap-2">
          <DollarSign className="text-yellow-400 shrink-0" size={18} />
          <div>
            <div className="text-[10px] text-gray-400 uppercase leading-none">Money</div>
            <div className="font-bold text-yellow-400 text-sm">{player.eddies}</div>
          </div>
        </div>

        {/* Role */}
        <div className="bg-[#080811] px-3 py-2 rounded-lg border border-[#00f3ff]/40 flex items-center gap-2">
          <Zap className="text-[#00f3ff] shrink-0" size={18} />
          <div>
            <div className="text-[10px] text-gray-400 uppercase leading-none">CLASS</div>
            <div className="font-bold text-[#00f3ff] text-sm">{player.role}</div>
          </div>
        </div>

        
      </div>
    </header>
  );
}
