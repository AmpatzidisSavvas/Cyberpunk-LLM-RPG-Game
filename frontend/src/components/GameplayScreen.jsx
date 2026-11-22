import React, { useState, useEffect } from 'react';
import HeaderHUD from './HeaderHUD';
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
    <div className="relative min-h-screen bg-[#080811] text-[#00ff9f] p-4 md:p-8 flex flex-col font-mono selection:bg-[#ff0055] selection:text-white">
      <MatrixBackground />

      <DiceModal
        rolling={rolling}
        rollData={rollData}
        rollFinished={rollFinished}
        animatedRollValue={animatedRollValue}
        onClose={handleCloseDiceModal}
      />

      {/* {player && (
        <HeaderHUD
          player={player}
          crtEnabled={crtEnabled}
          setCrtEnabled={setCrtEnabled}
        />
      )} */}

      <div className="z-20 flex-1 grid grid-cols-1 lg:grid-cols-4 gap-6 mt-4">
        <div className="lg:col-span-3 flex flex-col border border-[#00f3ff]/30 bg-[#0d0f1d]/80 rounded-xl p-4 h-[640px] shadow-[0_0_25px_rgba(0,243,255,0.08)]">
          <TerminalLog logs={logs} loading={loading} crtEnabled={crtEnabled} />

          {!isGameOver ? (
            <ActionButtons
              suggestedActions={suggestedActions}
              handleAction={handleAction}
              loading={loading}
            />
          ) : (
            <div className="p-4 border border-[#00ff9f]/40 bg-[#00ff9f]/10 rounded-lg text-center mt-auto my-2">
              <p className="text-sm font-bold text-[#00ff9f] mb-3 tracking-widest">
                ❖ STORY CONCLUSION REACHED ❖
              </p>
              <button
                onClick={onSwitchClass}
                className="bg-[#00f3ff] hover:bg-[#00ff9f] text-black font-bold px-6 py-2 rounded text-xs transition-all tracking-wider shadow-[0_0_15px_rgba(0,243,255,0.4)]"
              >
                START NEW OPERATIVE MISSION
              </button>
            </div>
          )}
        </div>

        <div className="flex flex-col gap-6">
          <OperativeSidebar
            player={player}
            onSwitchClass={onSwitchClass}
            visitedTrail={visitedTrail}
          />

          <FactionReputationWidget reputation={player?.reputation} />
        </div>
      </div>
    </div>
  );
}