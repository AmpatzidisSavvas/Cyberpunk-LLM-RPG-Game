import React, { useState, useEffect } from 'react';

const THESSALONIKI_NODES = [
  {
    id: 'westside',
    label: 'WESTSIDE',
    keywords: ['westside', 'ghetto', 'west'],
    x: 34,
    y: 52,
  },
  {
    id: 'ano_poli',
    label: 'ANO POLI',
    keywords: ['ano poli', 'heptapyrgion', 'rampart', 'siege', 'slum'],
    x: 142,
    y: 28,
  },
  {
    id: 'rotunda',
    label: 'ROTONDA',
    keywords: ['rotunda', 'catacomb'],
    x: 162,
    y: 74,
  },
  {
    id: 'venizelou',
    label: 'VENIZELOU',
    keywords: ['venizelou', 'egnatia', 'metro', 'roman', 'subterranean'],
    x: 108,
    y: 72,
  },
  {
    id: 'ladadika',
    label: 'LADADIKA',
    keywords: ['ladadika', 'backstreet'],
    x: 74,
    y: 112,
  },
  {
    id: 'aristotelous',
    label: 'ARISTOTELOUS',
    keywords: ['aristotelous', 'plaza', 'checkpoint'],
    x: 122,
    y: 116,
  },
  {
    id: 'pier6',
    label: 'PIER 6',
    keywords: ['pier 6', 'aegean', 'harbor', 'port', 'sub-cable'],
    x: 30,
    y: 138,
  },
  {
    id: 'white_tower',
    label: 'WHITE TOWER',
    keywords: ['white tower', 'waterfront', 'tower'],
    x: 164,
    y: 136,
  },
  {
    id: 'eastside',
    label: 'EASTSIDE',
    keywords: ['eastside', 'redneck', 'industrial', 'east'],
    x: 210,
    y: 126,
  },
];

const EDGES = [
  ['westside', 'ano_poli'],
  ['westside', 'venizelou'],
  ['westside', 'pier6'],
  ['ano_poli', 'rotunda'],
  ['ano_poli', 'venizelou'],
  ['rotunda', 'venizelou'],
  ['rotunda', 'white_tower'],
  ['venizelou', 'ladadika'],
  ['venizelou', 'aristotelous'],
  ['ladadika', 'pier6'],
  ['ladadika', 'aristotelous'],
  ['aristotelous', 'white_tower'],
  ['white_tower', 'eastside'],
  ['rotunda', 'eastside'],
];

export function resolveNodeId(nodeId, locationStr = '') {
  if (nodeId && THESSALONIKI_NODES.some((n) => n.id === nodeId)) {
    return nodeId;
  }
  const lower = (locationStr || '').toLowerCase();
  const matched = THESSALONIKI_NODES.find((node) =>
    node.keywords.some((kw) => lower.includes(kw))
  );
  return matched ? matched.id : 'venizelou';
}

export default function StorylineMapPanel({ player, visitedTrail = [] }) {
  const [inspectedNodeId, setInspectedNodeId] = useState(null);

  const currentNodeId = resolveNodeId(
    player?.current_node_id,
    player?.location
  );

  useEffect(() => {
    setInspectedNodeId(currentNodeId);
  }, [currentNodeId, player?.role]);

  if (!player) return null;

  const trail =
    Array.isArray(visitedTrail) && visitedTrail.length > 0
      ? visitedTrail
      : [{ nodeId: currentNodeId, location: player.location }];

  const visitedNodeIds = trail.map((t) => t.nodeId);

  const pinsByNode = {};
  if (Array.isArray(player.story_pins)) {
    player.story_pins.forEach((pin) => {
      if (pin.status !== 'resolved') {
        pinsByNode[pin.node_id] = pin;
      }
    });
  }

  const activeNodeId = inspectedNodeId || currentNodeId;
  const activeNode =
    THESSALONIKI_NODES.find((n) => n.id === activeNodeId) ||
    THESSALONIKI_NODES[0];
  const activePin = pinsByNode[activeNodeId];
  const isCurrentNode = activeNodeId === currentNodeId;

  return (
    <div className="border border-[#00f3ff]/30 bg-[#0d0f1d]/80 rounded-xl p-3 flex flex-col gap-2.5">
      {/* Header */}
      <div className="flex items-center justify-between pb-2 border-b border-[#00f3ff]/20">
        <span className="text-xs font-bold tracking-widest text-[#00f3ff] uppercase">
          [ STORYLINE PLACES ]
        </span>
        <span className="text-[10px] text-[#00ff9f] uppercase truncate max-w-[115px]">
          {activeNode.label}
        </span>
      </div>

      {/* Interactive Inspection SVG Map */}
      <div className="relative rounded-lg border border-[#00f3ff]/20 bg-[#070913] overflow-hidden">
        <svg viewBox="0 0 245 190" className="w-full h-[185px] block">
          {/* Grid Overlay */}
          <g stroke="#00f3ff" strokeOpacity="0.08" strokeWidth="1">
            <line x1="0" y1="48" x2="245" y2="48" />
            <line x1="0" y1="95" x2="245" y2="95" />
            <line x1="0" y1="142" x2="245" y2="142" />
            <line x1="61" y1="0" x2="61" y2="190" />
            <line x1="122" y1="0" x2="122" y2="190" />
            <line x1="183" y1="0" x2="183" y2="190" />
          </g>

          {/* Thermaikos Gulf Coastline */}
          <path
            d="M 0,146 Q 75,148 158,150 T 245,168 L 245,190 L 0,190 Z"
            fill="#00f3ff"
            fillOpacity="0.08"
          />
          <path
            d="M 0,146 Q 75,148 158,150 T 245,168"
            fill="none"
            stroke="#00f3ff"
            strokeOpacity="0.35"
            strokeWidth="1.2"
            strokeDasharray="3 3"
          />
          <text
            x="12"
            y="181"
            fill="#00f3ff"
            fillOpacity="0.42"
            fontSize="7"
            letterSpacing="1.5"
          >
            THERMAIKOS GULF
          </text>

          {/* Sector Network Edges */}
          <g stroke="#ffffff" strokeOpacity="0.12" strokeWidth="1">
            {EDGES.map(([aId, bId]) => {
              const a = THESSALONIKI_NODES.find((n) => n.id === aId);
              const b = THESSALONIKI_NODES.find((n) => n.id === bId);
              if (!a || !b) return null;
              return (
                <line
                  key={`${aId}-${bId}`}
                  x1={a.x}
                  y1={a.y}
                  x2={b.x}
                  y2={b.y}
                />
              );
            })}
          </g>

          {/* Visited Storyline Route */}
          {visitedNodeIds.length > 1 &&
            visitedNodeIds.slice(0, -1).map((fromId, idx) => {
              const toId = visitedNodeIds[idx + 1];
              const fromNode = THESSALONIKI_NODES.find((n) => n.id === fromId);
              const toNode = THESSALONIKI_NODES.find((n) => n.id === toId);
              if (!fromNode || !toNode) return null;
              return (
                <line
                  key={`trail-${fromId}-${toId}-${idx}`}
                  x1={fromNode.x}
                  y1={fromNode.y}
                  x2={toNode.x}
                  y2={toNode.y}
                  stroke="#00ff9f"
                  strokeWidth="2"
                  strokeOpacity="0.85"
                />
              );
            })}

          {/* District Nodes */}
          {THESSALONIKI_NODES.map((node) => {
            const isHere = node.id === currentNodeId;
            const hasPin = Boolean(pinsByNode[node.id]);
            const isInspected = node.id === activeNodeId;
            const wasVisited = visitedNodeIds.includes(node.id);

            const fillColor = isHere
              ? '#00ff9f'
              : hasPin
              ? '#ff0055'
              : wasVisited
              ? '#00f3ff'
              : '#1f2937';

            return (
              <g
                key={node.id}
                onClick={() => setInspectedNodeId(node.id)}
                className="cursor-pointer"
              >
                {(isHere || hasPin || isInspected) && (
                  <circle
                    cx={node.x}
                    cy={node.y}
                    r={isInspected ? 10 : 7.5}
                    fill="none"
                    stroke={isHere ? '#00ff9f' : hasPin ? '#ff0055' : '#00f3ff'}
                    strokeWidth="1.2"
                    strokeOpacity={isInspected ? '0.95' : '0.5'}
                  />
                )}

                <circle
                  cx={node.x}
                  cy={node.y}
                  r={isHere ? 4.5 : 3.5}
                  fill={fillColor}
                  stroke="#080811"
                  strokeWidth="1.1"
                />

                <text
                  x={node.x}
                  y={node.y - 8}
                  textAnchor="middle"
                  fill={isInspected ? '#ffffff' : '#9ca3af'}
                  fontSize="6.2"
                  fontWeight={isHere || isInspected ? 'bold' : 'normal'}
                >
                  {node.label}
                </text>
              </g>
            );
          })}
        </svg>

        {/* Legend */}
        <div className="flex items-center justify-between px-2.5 py-1 bg-black/60 border-t border-white/10 text-[9px] text-gray-400">
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-[#00ff9f] inline-block" /> YOU
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-[#ff0055] inline-block" /> ARC BEAT
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-[#00f3ff] inline-block" /> VISITED
          </span>
        </div>
      </div>

      {/* Logged Storyline Places List */}
      <div className="rounded-lg border border-white/10 bg-black/40 p-2.5 flex flex-col gap-1.5">
        <div className="flex items-center justify-between text-[10px] text-[#00f3ff] font-bold uppercase">
          <span>ROUTE LOG</span>
          <span>{trail.length} {trail.length === 1 ? 'PLACE' : 'PLACES'}</span>
        </div>

        <div className="flex flex-col gap-1 max-h-[84px] overflow-y-auto pr-0.5">
          {trail.map((entry, idx) => {
            const isLatest = idx === trail.length - 1;
            return (
              <div
                key={`${entry.nodeId}-${idx}`}
                className={`text-[10px] flex items-center gap-1.5 truncate ${
                  isLatest ? 'text-[#00ff9f] font-bold' : 'text-gray-300'
                }`}
              >
                <span className="text-[#00f3ff] shrink-0">
                  {isLatest ? '▶' : `${idx + 1}.`}
                </span>
                <span className="truncate">{entry.location || entry.nodeId}</span>
              </div>
            );
          })}
        </div>

        <div className="pt-1.5 mt-0.5 border-t border-white/10 text-[11px] text-gray-300 leading-snug">
          {activePin
            ? activePin.objective
            : isCurrentNode
            ? `Currently at ${player.location}.`
            : `No active storyline beat recorded in ${activeNode.label}.`}
        </div>
      </div>
    </div>
  );
}