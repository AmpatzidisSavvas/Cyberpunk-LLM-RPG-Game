import React from 'react';
import InventoryPanel from './InventoryPanel';

export default function OperativeSidebar({ player, onSwitchClass }) {
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

  return (
    <div className="lg:col-span-1 flex flex-col gap-4">
      {/* Character Illustration Card */}
      <div className="border border-[#00f3ff]/30 bg-[#0d0f1d]/80 rounded-xl p-3 shadow-[0_0_25px_rgba(0,243,255,0.08)] flex flex-col items-center">
        <div className="w-full text-center pb-2 mb-2 border-b border-[#00f3ff]/20">
          <span className="text-xs font-bold tracking-widest text-[#00f3ff] uppercase">
            [ OPERATIVE: {player.role.toUpperCase()} ]
          </span>
        </div>
        <div className="relative">
          <img 
            src={getImageSrc(player.role)} 
            alt={player.role}
            className="w-[200px] h-[200px] object-cover pixelated opacity-90 group-hover:opacity-100 transition-opacity"
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

      {/* Inventory Panel */}
      <InventoryPanel inventory={player.inventory} />

      {/* Switch Class Button */}
      <button
        onClick={onSwitchClass}
        className="w-full border border-[#ff0055]/50 bg-[#ff0055]/10 hover:bg-[#ff0055] hover:text-black text-[#ff0055] text-xs font-bold py-2 rounded transition-all tracking-wider"
      >
        ← SWITCH OPERATIVE CLASS
      </button>
    </div>
  );
}