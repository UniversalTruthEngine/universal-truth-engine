async function loadGraph() {
  const response = await fetch("data/truth-map-v1.json");
  const graph = await response.json();

  const svg = d3.select("#truth-map");
  const details = d3.select("#details");
  const tooltip = d3.select("#tooltip");
  const search = d3.select("#search");
  const categoryFilter = d3.select("#category-filter");
  const resetButton = d3.select("#reset-view");

  const container = svg.node();
  const width = container.clientWidth;
  const height = container.clientHeight || 700;
  svg.attr("viewBox", [0, 0, width, height]);

  const links = graph.edges.map(d => ({ ...d }));
  const nodes = graph.nodes.map(d => ({ ...d }));

  const categories = Array.from(new Set(nodes.map(d => d.category))).sort();
  categories.forEach(category => {
    categoryFilter.append("option").attr("value", category).text(category);
  });

  const centralityExtent = d3.extent(nodes, d => d.dependency_centrality);
  const radius = d3.scaleSqrt()
    .domain([centralityExtent[0] || 0, centralityExtent[1] || 1])
    .range([9, 36]);

  const categoryColor = d3.scaleOrdinal()
    .domain(["Logic", "Arithmetic", "Geometry", "Measurement"])
    .range(["#a78bfa", "#83b6ff", "#8df0a4", "#ffe27c"]);

  const zoomLayer = svg.append("g");

  svg.append("defs").append("marker")
    .attr("id", "arrow")
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", 19)
    .attr("refY", 0)
    .attr("markerWidth", 7)
    .attr("markerHeight", 7)
    .attr("orient", "auto")
    .append("path")
    .attr("fill", "rgba(165,183,215,0.62)")
    .attr("d", "M0,-5L10,0L0,5");

  const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id).distance(d => 105 / Math.max(0.35, d.weight)))
    .force("charge", d3.forceManyBody().strength(d => -280 - d.dependency_centrality * 50))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collision", d3.forceCollide().radius(d => radius(d.dependency_centrality) + 20));

  const link = zoomLayer.append("g")
    .attr("stroke-linecap", "round")
    .selectAll("line")
    .data(links)
    .join("line")
    .attr("class", "link")
    .attr("marker-end", "url(#arrow)")
    .attr("stroke-width", d => 1 + d.weight * 2);

  const nodeGroup = zoomLayer.append("g")
    .selectAll("g")
    .data(nodes)
    .join("g")
    .call(drag(simulation));

  const node = nodeGroup.append("circle")
    .attr("class", "node")
    .attr("r", d => radius(d.dependency_centrality))
    .attr("fill", d => categoryColor(d.category) || "#ffffff")
    .on("click", (_, d) => showDetails(d))
    .on("mousemove", (event, d) => showTooltip(event, d))
    .on("mouseleave", hideTooltip);

  const label = nodeGroup.append("text")
    .attr("class", "node-label")
    .attr("text-anchor", "middle")
    .attr("dy", d => radius(d.dependency_centrality) + 14)
    .text(d => d.id.replace("UTE-FV-", ""));

  const zoom = d3.zoom()
    .scaleExtent([0.35, 3.5])
    .on("zoom", event => zoomLayer.attr("transform", event.transform));

  svg.call(zoom);

  resetButton.on("click", () => {
    svg.transition().duration(500).call(zoom.transform, d3.zoomIdentity);
    search.property("value", "");
    categoryFilter.property("value", "all");
    applyFilters();
  });

  search.on("input", applyFilters);
  categoryFilter.on("change", applyFilters);

  simulation.on("tick", () => {
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => {
        const dx = d.target.x - d.source.x;
        const dy = d.target.y - d.source.y;
        const len = Math.sqrt(dx * dx + dy * dy) || 1;
        return d.target.x - (dx / len) * (radius(d.target.dependency_centrality) + 7);
      })
      .attr("y2", d => {
        const dx = d.target.x - d.source.x;
        const dy = d.target.y - d.source.y;
        const len = Math.sqrt(dx * dx + dy * dy) || 1;
        return d.target.y - (dy / len) * (radius(d.target.dependency_centrality) + 7);
      });

    nodeGroup.attr("transform", d => `translate(${d.x},${d.y})`);
  });

  function showDetails(d) {
    const dependents = nodes
      .filter(n => n.dependencies.includes(d.id))
      .map(n => n.id)
      .join(", ") || "None listed";

    details.html(`
      <h2>${d.id}</h2>
      <h3>${d.title}</h3>
      <p>${d.claim}</p>
      <div class="meta">
        <p><strong>Domain:</strong> ${d.category}</p>
        <p><strong>Confidence level:</strong> ${d.confidence_level}</p>
        <p><strong>Dependency centrality:</strong> ${d.dependency_centrality}</p>
        <p><strong>Depends on:</strong> ${d.dependencies.length ? d.dependencies.join(", ") : "None listed"}</p>
        <p><strong>Depended on by:</strong> ${dependents}</p>
      </div>
    `);
  }

  function showTooltip(event, d) {
    tooltip
      .style("display", "block")
      .style("left", `${event.clientX + 14}px`)
      .style("top", `${event.clientY + 14}px`)
      .html(`<strong>${d.id}</strong><br>${d.title}<br><span>${d.category}</span>`);
  }

  function hideTooltip() {
    tooltip.style("display", "none");
  }

  function applyFilters() {
    const q = search.property("value").toLowerCase().trim();
    const selectedCategory = categoryFilter.property("value");

    const visible = new Set(nodes
      .filter(d => {
        const matchesText = !q || d.id.toLowerCase().includes(q) || d.title.toLowerCase().includes(q);
        const matchesCategory = selectedCategory === "all" || d.category === selectedCategory;
        return matchesText && matchesCategory;
      })
      .map(d => d.id));

    node.classed("dimmed", d => !visible.has(d.id));
    label.classed("dimmed", d => !visible.has(d.id));
    link.classed("dimmed", d => !visible.has(d.source.id) || !visible.has(d.target.id));
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
