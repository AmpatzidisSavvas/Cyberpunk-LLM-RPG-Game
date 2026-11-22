import React from 'react';
import StorylineMapPanel from './StorylineMapPanel';
import {  Shield, Zap, DollarSign, MapPin,  } from 'lucide-react';

export default function OperativeSidebar({
  player,
  onSwitchClass,
  visitedTrail = [],
}) {
  if (!player) return null;

  const getImageSrc = (role) => {
    switch (role) {
      case 'Netrunner':
        return '/img/class-3.png';
      case 'Gunner':
        return '/img/class-2.png';
      default:
        return '/img/class-1.png';
    }
  };

  const hpPercent = Math.max(0, Math.min(100, (player.hp / player.max_hp) * 100));

  return (
    <div className="lg:col-span-1 flex flex-col gap-4">
      {/* Switch Class Button */}
      <button
        onClick={onSwitchClass}
        className="w-full border border-[#ff0055]/50 bg-[#ff0055]/10 hover:bg-[#ff0055] hover:text-black text-[#ff0055] text-xs font-bold py-2 rounded transition-all tracking-wider"
      >
        ← SWITCH OPERATIVE CLASS
      </button>

      <div className="flex gap-3 flex-wrap items-center justify-center">
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

      {/* Character Illustration Card */}
      <div className="group border border-[#00f3ff]/30 bg-[#0d0f1d]/80 rounded-xl p-3 animate-cyan-pulse transition-colors duration-300 hover:border-[#00f3ff]/60 flex flex-col items-center">
        <div className="w-full text-center pb-2 mb-2 border-b border-[#00f3ff]/20">
          <span className="text-xs font-bold tracking-widest text-[#00f3ff] uppercase">
            [ OPERATIVE: {player.role.toUpperCase()} ]
          </span>
        </div>
        <div className="relative overflow-hidden rounded-lg">
          <img
            src={getImageSrc(player.role)}
            alt={player.role}
            className="w-[200px] h-[200px] object-cover pixelated opacity-90 animate-operative-idle transition-all duration-300 group-hover:opacity-100 group-hover:scale-105"
            onError={(e) => {
              e.target.style.display = 'none';
              if (e.target.nextSibling) {
                e.target.nextSibling.style.display = 'flex';
              }
            }}
          />
          <div className="absolute inset-0 hidden items-center justify-center text-[10px] text-gray-500 italic">
            [NO IMAGE ASSET FOUND]
          </div>
        </div>
      </div>

      {/* Storyline Places Tracker */}
      <StorylineMapPanel
        player={player}
        visitedTrail={visitedTrail}
      />
      
    </div>
  );
}