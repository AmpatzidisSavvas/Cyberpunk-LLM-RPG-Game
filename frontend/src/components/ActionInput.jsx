import React, { useState } from 'react';
import { Send, CornerDownLeft } from 'lucide-react';
import { sounds } from '../utils/audio';

export default function ActionInput({ input, setInput, handleAction, loading }) {
  const [history, setHistory] = useState([]);
  const [historyIdx, setHistoryIdx] = useState(-1);

  const onSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;
    sounds.playBeep(1000, 0.05);
    setHistory(prev => [input, ...prev]);
    setHistoryIdx(-1);
    handleAction(input);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'ArrowUp') {
      if (history.length > 0 && historyIdx < history.length - 1) {
        const nextIdx = historyIdx + 1;
        setHistoryIdx(nextIdx);
        setInput(history[nextIdx]);
      }
    } else if (e.key === 'ArrowDown') {
      if (historyIdx > 0) {
        const prevIdx = historyIdx - 1;
        setHistoryIdx(prevIdx);
        setInput(history[prevIdx]);
      } else if (historyIdx === 0) {
        setHistoryIdx(-1);
        setInput('');
      }
    }
  };

  return (
    <form onSubmit={onSubmit} className="mt-3 flex gap-2">
      <div className="relative flex-1">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Enter terminal prompt (or press 1-4 above)..."
          className="w-full bg-[#080811] border border-[#00f3ff]/40 rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-[#ff0055] focus:ring-1 focus:ring-[#ff0055] transition-all font-mono"
          disabled={loading}
        />
        <div className="absolute right-3 top-2.5 text-gray-500 text-xs hidden md:flex items-center gap-1">
          <CornerDownLeft size={12} /> ENTER
        </div>
      </div>
      <button
        type="submit"
        disabled={loading || !input.trim()}
        className="px-5 py-2.5 bg-[#ff0055] hover:bg-[#ff0055]/80 disabled:bg-gray-800 text-white rounded-lg flex items-center gap-2 font-bold transition-all shadow-[0_0_15px_rgba(255,0,85,0.4)] disabled:shadow-none shrink-0"
      >
        <Send size={16} />
      </button>
    </form>
  );
}
