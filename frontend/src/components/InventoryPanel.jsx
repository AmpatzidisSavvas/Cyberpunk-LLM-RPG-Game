import React from 'react';
import { Package, Trash2, Heart, Crosshair } from 'lucide-react';
import { sounds } from '../utils/audio';

export default function InventoryPanel({ inventory, setPlayer }) {
  const handleUseItem = (itemIndex, itemName) => {
    sounds.playCyberHack();
    if (itemName.toLowerCase().includes('hypo') || itemName.toLowerCase().includes('health')) {
      setPlayer(prev => ({
        ...prev,
        hp: Math.min(prev.max_hp, prev.hp + 35),
        inventory: prev.inventory.filter((_, idx) => idx !== itemIndex)
      }));
    } else {
      alert(`Equipped / Activated: ${itemName}`);
    }
  };

  const handleDropItem = (e, itemIndex) => {
    e.stopPropagation();
    sounds.playBeep(400, 0.08, 'sawtooth');
    setPlayer(prev => ({
      ...prev,
      inventory: prev.inventory.filter((_, idx) => idx !== itemIndex)
    }));
  };

  return (
    <div className="border border-[#ff0055]/30 bg-[#0d0f1d]/80 rounded-xl p-4 flex flex-col gap-4 h-fit shadow-[0_0_20px_rgba(255,0,85,0.1)]">
      <h2 className="text-md font-bold text-[#ff0055] flex items-center justify-between border-b border-[#ff0055]/30 pb-3">
        <span className="flex items-center gap-2 uppercase tracking-wider">
          <Package size={18} /> NEURAL GEAR LOG
        </span>
        <span className="text-xs text-gray-400">({inventory.length} items)</span>
      </h2>

      {inventory.length === 0 ? (
        <p className="text-xs text-gray-500 italic py-4 text-center">Inventory empty</p>
      ) : (
        <ul className="space-y-2">
          {inventory.map((item, index) => {
            const isConsumable = item.toLowerCase().includes('hypo') || item.toLowerCase().includes('health');
            return (
              <li 
                key={index} 
                onClick={() => handleUseItem(index, item)}
                className="group cursor-pointer text-xs bg-[#080811] hover:bg-[#00f3ff]/10 border border-[#00ff9f]/20 hover:border-[#00f3ff] p-2.5 rounded-lg flex justify-between items-center transition"
              >
                <div className="flex items-center gap-2 font-mono text-[#00ff9f]">
                  {isConsumable ? <Heart size={14} className="text-[#ff0055]" /> : <Crosshair size={14} className="text-[#00f3ff]" />}
                  <span>{item}</span>
                </div>
                <button
                  onClick={(e) => handleDropItem(e, index)}
                  className="opacity-0 group-hover:opacity-100 text-gray-500 hover:text-red-400 p-1 rounded transition"
                  title="Discard item"
                >
                  <Trash2 size={13} />
                </button>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
