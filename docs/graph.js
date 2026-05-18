async function loadGraph() {
  const response = await fetch("data/truth-map-v1.json");
  const graph = await response.json();

  const svg = d3.select("#truth-map");
  const details = d3.select("#details");

  const container = svg.node();
  const width = container.clientWidth;
  const height = container.clientHeight || 680;

  svg.attr("viewBox", [0, 0, width, height]);

  const links = graph.edges.map(d => ({ ...d }));
  const nodes = graph.nodes.map(d => ({ ...d }));

  const centralityExtent = d3.extent(nodes, d => d.dependency_centrality);
  const radius = d3.scaleSqrt()
    .domain([centralityExtent[0] || 0, centralityExtent[1] || 1])
    .range([9, 34]);

  const color = d3.scaleOrdinal()
    .domain([5, 4, 3, 2, 1])
    .range(["#83b6ff", "#8df0a4", "#ffe27c", "#ff9d6f", "#ff6b8a"]);

  const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id).distance(d => 95 / Math.max(0.35, d.weight)))
    .force("charge", d3.forceManyBody().strength(d => -260 - d.dependency_centrality * 45))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collision", d3.forceCollide().radius(d => radius(d.dependency_centrality) + 18));

  const link = svg.append("g")
    .attr("stroke-linecap", "round")
    .selectAll("line")
    .data(links)
    .join("line")
    .attr("class", "link")
    .attr("stroke-width", d => 1 + d.weight * 2);

  const nodeGroup = svg.append("g")
    .selectAll("g")
    .data(nodes)
    .join("g")
    .call(drag(simulation));

  const node = nodeGroup.append("circle")
    .attr("class", "node")
    .attr("r", d => radius(d.dependency_centrality))
    .attr("fill", d => color(d.confidence_level))
    .on("click", (_, d) => showDetails(d));

  node.append("title")
    .text(d => `${d.id} — ${d.title}`);

  const label = nodeGroup.append("text")
    .attr("class", "node-label")
    .attr("text-anchor", "middle")
    .attr("dy", d => radius(d.dependency_centrality) + 14)
    .text(d => d.id.replace("UTE-FV-", ""));

  simulation.on("tick", () => {
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

    nodeGroup
      .attr("transform", d => `translate(${d.x},${d.y})`);
  });

  function showDetails(d) {
    details.html(`
      <h2>${d.id}</h2>
      <h3>${d.title}</h3>
      <p>${d.claim}</p>
      <div class="meta">
        <p><strong>Category:</strong> ${d.category}</p>
        <p><strong>Confidence level:</strong> ${d.confidence_level}</p>
        <p><strong>Dependency centrality:</strong> ${d.dependency_centrality}</p>
        <p><strong>Dependencies:</strong> ${d.dependencies.length ? d.dependencies.join(", ") : "None listed"}</p>
      </div>
    `);
  }

  function drag(simulation) {
    function dragstarted(event) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }

    function dragged(event) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }

    function dragended(event) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }

    return d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended);
  }
}

loadGraph();
