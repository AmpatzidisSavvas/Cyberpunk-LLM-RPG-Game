import React, { useEffect } from 'react';
import { sounds } from '../utils/audio';

export default function ActionButtons({ suggestedActions, handleAction, loading }) {
  // Keybindings 1-4 for quick response selection
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (['1', '2', '3', '4'].includes(e.key)) {
        const index = parseInt(e.key, 10) - 1;
        if (suggestedActions[index] && !loading) {
          sounds.playBeep(900, 0.05);
          handleAction(suggestedActions[index]);
        }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [suggestedActions, loading, handleAction]);

  return (
    <div className="mt-4 pt-3 border-t border-[#00f3ff]/20 grid grid-cols-1 md:grid-cols-2 gap-2">
      {suggestedActions.map((choice, i) => (
        <button
          key={i}
          onClick={() => {
            sounds.playBeep(800, 0.04);
            handleAction(choice);
          }}
          disabled={loading}
          className="group relative text-left text-xs p-3 rounded-lg bg-[#00f3ff]/5 hover:bg-[#00f3ff]/20 border border-[#00f3ff]/30 text-[#00f3ff] transition-all hover:border-[#00f3ff] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-between"
        >
          <span className="font-mono truncate pr-2">&gt; {choice}</span>
          <span className="px-1.5 py-0.5 rounded text-[10px] bg-[#00f3ff]/20 border border-[#00f3ff]/40 text-[#00f3ff] group-hover:bg-[#00f3ff] group-hover:text-black font-bold transition">
            [{i + 1}]
          </span>
        </button>
      ))}
    </div>
  );
}
