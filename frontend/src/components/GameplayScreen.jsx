import React, { useState, useEffect } from 'react';
import TerminalLog from './TerminalLog';
import ActionButtons from './ActionButtons';
import OperativeSidebar from './OperativeSidebar';
import DiceModal from './DiceModal';
import MatrixBackground from './MatrixBackground';
import FactionReputationWidget from './FactionReputationWidget';
import { resolveNodeId } from './StorylineMapPanel';

export default function GameplayScreen({
  player,
  logs,
  loading,
  crtEnabled,
  setCrtEnabled,
  isGameOver,
  suggestedActions,
  handleAction,
  onSwitchClass,
  rolling,
  rollData,
  rollFinished,
  animatedRollValue,
  handleCloseDiceModal,
}) {
  const [visitedTrail, setVisitedTrail] = useState([]);

  useEffect(() => {
    if (!player?.role || !player?.location) return;
    const nodeId = resolveNodeId(player.current_node_id, player.location);

    setVisitedTrail((prev) => {
      if (prev.length === 0 || prev[0]?.role !== player.role) {
        return [{ role: player.role, nodeId, location: player.location }];
      }
      const last = prev[prev.length - 1];
      if (last.location === player.location && last.nodeId === nodeId) {
        return prev;
      }
      return [...prev, { role: player.role, nodeId, location: player.location }];
    });
  }, [player?.role, player?.location, player?.current_node_id]);

  return (
    <div className="relative min-h-screen lg:h-screen lg:overflow-hidden bg-[#080811] text-[#00ff9f] p-3 sm:p-5 flex flex-col font-mono selection:bg-[#ff0055] selection:text-white">
      <MatrixBackground />

      <DiceModal
        rolling={rolling}
        rollData={rollData}
        rollFinished={rollFinished}
        animatedRollValue={animatedRollValue}
        onClose={handleCloseDiceModal}
      />

      {/* Main 12-Column Grid locked to viewport height on desktop */}
      <div className="z-20 flex-1 grid grid-cols-1 lg:grid-cols-12 gap-4 min-h-0">
        
        {/* LEFT COLUMN (9 Cols): Terminal Window on Top + Faction Standing Below */}
        <div className="lg:col-span-9 flex flex-col gap-4 min-h-0">
          
          {/* Terminal Box (Automatically fills remaining vertical space) */}
          <div className="flex-1 flex flex-col relative border border-[#00f3ff]/30 bg-[#0d0f1d]/85 backdrop-blur-md rounded-xl p-4 shadow-[0_0_30px_rgba(0,243,255,0.08)] overflow-hidden min-h-[360px] lg:min-h-0">
            {/* Top Neon Edge & Corner Accents */}
            <div className="absolute top-0 inset-x-0 h-[1px] bg-gradient-to-r from-transparent via-[#00f3ff]/70 to-transparent" />
            <div className="absolute top-0 left-0 w-3 h-3 border-t-2 border-l-2 border-[#00f3ff]/70 rounded-tl-xl pointer-events-none" />
            <div className="absolute top-0 right-0 w-3 h-3 border-t-2 border-r-2 border-[#00f3ff]/70 rounded-tr-xl pointer-events-none" />

            {/* Scrollable Terminal Log */}
            <div className="flex-1 flex flex-col min-h-0 overflow-hidden mb-3">
              <TerminalLog logs={logs} loading={loading} crtEnabled={crtEnabled} />
            </div>

            {/* Action Buttons or Game Over Banner */}
            <div className="shrink-0 pt-3 border-t border-[#00f3ff]/15">
              {!isGameOver ? (
                <ActionButtons
                  suggestedActions={suggestedActions}
                  handleAction={handleAction}
                  loading={loading}
                />
              ) : (
                <div className="p-3.5 border border-[#00ff9f]/40 bg-gradient-to-b from-[#00ff9f]/15 to-[#00ff9f]/5 rounded-lg text-center shadow-[inset_0_0_20px_rgba(0,255,159,0.05)]">
                  <p className="text-xs sm:text-sm font-bold text-[#00ff9f] mb-2.5 tracking-[0.2em] uppercase">
                    ❖ Story Conclusion Reached ❖
                  </p>
                  <button
                    onClick={onSwitchClass}
                    className="bg-[#00f3ff] hover:bg-[#00ff9f] active:scale-[0.98] text-[#05070e] font-extrabold px-6 py-2 rounded-md text-xs transition-all duration-200 tracking-widest uppercase shadow-[0_0_20px_rgba(0,243,255,0.4)] hover:shadow-[0_0_25px_rgba(0,255,159,0.6)] cursor-pointer"
                  >
                    Start New Operative Mission
                  </button>
                </div>
              )}
            </div>
          </div>

          
          <div className="shrink-0">
            <FactionReputationWidget reputation={player?.reputation} />
          </div>

        </div>

        
        <div className="lg:col-span-3 flex flex-col min-h-0 overflow-y-auto">
          <OperativeSidebar
            player={player}
            onSwitchClass={onSwitchClass}
            visitedTrail={visitedTrail}
          />
        </div>

      </div>
    </div>
  );
}