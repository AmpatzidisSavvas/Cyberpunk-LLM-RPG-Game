import React from 'react';
import MatrixBackground from './MatrixBackground';

export default function ClassSelectionScreen({ classesData, loadingClasses, onSelectClass }) {
  return (
    <div className="relative min-h-screen bg-[#080811] text-[#00ff9f] p-4 md:p-8 flex flex-col items-center justify-center font-mono selection:bg-[#ff0055] selection:text-white">
      <MatrixBackground />
      <div className="z-20 max-w-4xl w-full border border-[#00f3ff]/40 bg-[#0d0f1d]/90 p-8 rounded-xl shadow-[0_0_30px_rgba(0,243,255,0.12)]">
        <h1 className="text-3xl font-extrabold text-center tracking-widest text-[#00f3ff] mb-2 drop-shadow-[0_0_10px_rgba(0,243,255,0.5)]">
          THESSALONIKI_2099
        </h1>
        <p className="text-center text-xs text-[#00ff9f]/70 mb-8 tracking-widest uppercase">
          Select an operative archetype to synchronize neural link
        </p>

        {loadingClasses ? (
          <div className="text-center text-[#ff0055] animate-pulse">
            [CONNECTING TO BACKEND CLASS DATABASE...]
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {Object.entries(classesData).map(([roleName, info]) => (
              <div
                key={roleName}
                onClick={() => onSelectClass(roleName, info)}
                className="border border-[#00f3ff]/30 bg-[#080811]/80 p-5 rounded-lg flex flex-col justify-between hover:border-[#00ff9f] hover:shadow-[0_0_20px_rgba(0,255,159,0.25)] transition-all cursor-pointer group"
              >
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <h2 className="text-xl font-bold text-[#00f3ff] group-hover:text-[#00ff9f] transition-colors">
                      {roleName}
                    </h2>
                    <span className="text-[10px] text-[#ff0055] border border-[#ff0055]/40 px-1.5 py-0.5 rounded">
                      CLASS
                    </span>
                  </div>
                  <p className="text-xs text-gray-400 mb-4 leading-relaxed">
                    {info.description}
                  </p>
                  <div className="text-xs space-y-1 text-[#00ff9f]/80 mb-4 bg-[#0d0f1d] p-3 rounded border border-[#00f3ff]/10">
                    <div>❤️ HP: {info.hp}/{info.max_hp}</div>
                    <div>💵 Money: {info.eddies}</div>
                    <div className="truncate">🎒 GEAR: {info.inventory.join(', ')}</div>
                  </div>
                </div>
                <button className="w-full mt-2 bg-[#00f3ff]/10 border border-[#00f3ff]/50 text-[#00f3ff] group-hover:bg-[#00ff9f] group-hover:text-black group-hover:border-[#00ff9f] py-2 text-xs font-bold tracking-wider transition-all rounded">
                  SELECT {roleName.toUpperCase()}
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}