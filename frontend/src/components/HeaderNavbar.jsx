import React from 'react';
import { Cpu } from 'lucide-react';

export default function HeaderNavbar() {
  return (
    <header className="relative z-10 border-b border-[#00f3ff]/40 bg-[#080811]/90 backdrop-blur px-4 py-3">
      <div className="max-w-7xl mx-auto flex flex-wrap justify-between items-center gap-4">
        <div className="flex items-center gap-3">
          <Cpu className="text-[#00f3ff] w-7 h-7 animate-pulse" />
          <div>
            <h1 className="text-xl md:text-2xl font-bold tracking-wider text-white flex items-center gap-1">
              THESSALONIKI <span className="text-[#00f3ff]">2099</span>
            </h1>
            <p className="text-[10px] md:text-xs text-[#c0c9e2]/70 font-['Share_Tech_Mono'] tracking-widest">
              CYBERPUNK INTERACTIVE NARRATIVE ENGINE
            </p>
          </div>
        </div>
      </div>
    </header>
  );
}