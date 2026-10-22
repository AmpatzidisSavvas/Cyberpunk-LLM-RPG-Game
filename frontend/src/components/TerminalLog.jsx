import React, { useRef, useEffect } from 'react';

export default function TerminalLog({ logs, loading, crtEnabled }) {
  const logEndRef = useRef(null);

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs, loading]);

  return (
    <div className="relative flex-1 overflow-y-auto space-y-3 pr-2 scrollbar-thin scrollbar-thumb-[#00f3ff]/30 scrollbar-track-transparent">
      {crtEnabled && <div className="pointer-events-none fixed inset-0 scanlines z-30 opacity-40" />}

      {logs.map((log, idx) => (
        <div 
          key={idx} 
          className={`p-3 rounded-lg text-sm border transition-all ${
            log.sender === 'PLAYER' 
              ? 'border-[#00f3ff]/40 bg-[#00f3ff]/5 text-white ml-6' 
              : log.sender === 'SYSTEM' 
              ? 'border-yellow-500/30 bg-yellow-500/5 text-yellow-400 font-bold' 
              : 'border-[#00ff9f]/20 bg-[#080811]/60 text-[#00ff9f] leading-relaxed shadow-[inset_0_0_10px_rgba(0,255,159,0.05)]'
          }`}
        >
          <div className="flex items-center justify-between mb-1 opacity-60 text-[10px] tracking-wider uppercase">
            <span>[{log.sender}]</span>
            <span>{new Date().toLocaleTimeString()}</span>
          </div>
          <div className="whitespace-pre-wrap font-mono">{log.text}</div>
        </div>
      ))}

      {loading && (
        <div className="flex items-center gap-2 text-[#ff0055] animate-pulse p-3 border border-[#ff0055]/30 bg-[#ff0055]/5 rounded-lg text-sm font-mono">
          <div className="w-2 h-2 bg-[#ff0055] rounded-full animate-ping" />
          <span>NEURAL LINK COMPUTING PARALLEL TIMELINES...</span>
        </div>
      )}
      <div ref={logEndRef} />
    </div>
  );
}
