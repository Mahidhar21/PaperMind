import ForceGraph2D from "react-force-graph-2d";

export default function KnowledgeGraph({ graph }) {
  if (!Array.isArray(graph) || graph.length === 0) {
    return null;
  }

  const nodeMap = new Map();
  const links = [];

  graph.forEach((edge) => {
    if (!edge.source || !edge.target) return;

    if (!nodeMap.has(edge.source)) {
      nodeMap.set(edge.source, {
        id: edge.source,
        connections: 0,
      });
    }

    if (!nodeMap.has(edge.target)) {
      nodeMap.set(edge.target, {
        id: edge.target,
        connections: 0,
      });
    }

    nodeMap.get(edge.source).connections++;
    nodeMap.get(edge.target).connections++;

    links.push({
      source: edge.source,
      target: edge.target,
      label: edge.relation,
    });
  });

  const nodes = Array.from(nodeMap.values());

  return (
    <div className="w-full h-[900px] rounded-3xl overflow-hidden border border-zinc-800 bg-black mt-6">
      <ForceGraph2D
        graphData={{
          nodes,
          links,
        }}
        backgroundColor="#000000"
        cooldownTicks={300}
        d3VelocityDecay={0.15}
        enableNodeDrag={true}
        nodeRelSize={6}
        nodeLabel="id"
        linkCurvature={0.15}
        linkDirectionalArrowLength={4}
        linkDirectionalArrowRelPos={1}
        linkColor={() => "#444"}
        nodeCanvasObject={(node, ctx, globalScale) => {
          const label =
            node.id.length > 25
              ? node.id.slice(0, 25) + "..."
              : node.id;

          const fontSize = Math.max(
            11 / globalScale,
            4
          );

          const radius = Math.max(
            5,
            Math.min(
              node.connections * 1.2,
              18
            )
          );

          ctx.beginPath();

          ctx.arc(
            node.x,
            node.y,
            radius,
            0,
            2 * Math.PI
          );

          ctx.fillStyle = "#ffffff";
          ctx.fill();

          ctx.font = `${fontSize}px Sans-Serif`;
          ctx.fillStyle = "#ffffff";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";

          ctx.fillText(
            label,
            node.x,
            node.y - radius - 12
          );
        }}
      />
    </div>
  );
}