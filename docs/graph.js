const categoryColors = {
  Logic: 0xa78bfa,
  Arithmetic: 0x83b6ff,
  Geometry: 0x8df0a4,
  Measurement: 0xffe27c
};

const state = {
  graph: null,
  scene: null,
  camera: null,
  renderer: null,
  controls: null,
  nodeObjects: new Map(),
  labelObjects: new Map(),
  edgeObjects: [],
  selected: null
};

async function init() {
  const response = await fetch("data/truth-map-v1.json");
  state.graph = await response.json();

  setupControls();
  setupScene();
  buildGraph();
  animate();
}

function setupControls() {
  const categories = [...new Set(state.graph.nodes.map(n => n.category))].sort();
  const select = document.getElementById("category-filter");
  categories.forEach(category => {
    const option = document.createElement("option");
    option.value = category;
    option.textContent = category;
    select.appendChild(option);
  });

  document.getElementById("search").addEventListener("input", applyFilters);
  select.addEventListener("change", applyFilters);
  document.getElementById("reset-view").addEventListener("click", () => {
    state.camera.position.set(0, 0, 420);
    state.controls.target.set(0, 0, 0);
    state.controls.update();
  });
}

function setupScene() {
  const container = document.getElementById("map3d");
  const width = container.clientWidth;
  const height = container.clientHeight;

  state.scene = new THREE.Scene();
  state.scene.background = new THREE.Color(0x050812);

  state.camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 3000);
  state.camera.position.set(0, 0, 420);

  state.renderer = new THREE.WebGLRenderer({ antialias: true });
  state.renderer.setPixelRatio(window.devicePixelRatio);
  state.renderer.setSize(width, height);
  container.appendChild(state.renderer.domElement);

  state.controls = new THREE.OrbitControls(state.camera, state.renderer.domElement);
  state.controls.enableDamping = true;
  state.controls.dampingFactor = 0.06;
  state.controls.rotateSpeed = 0.55;
  state.controls.zoomSpeed = 0.75;

  const ambient = new THREE.AmbientLight(0xffffff, 0.75);
  state.scene.add(ambient);

  const point = new THREE.PointLight(0x9dbdff, 1.4, 900);
  point.position.set(180, 120, 260);
  state.scene.add(point);

  addStarfield();

  window.addEventListener("resize", onResize);
  state.renderer.domElement.addEventListener("click", onCanvasClick);
}

function addStarfield() {
  const geometry = new THREE.BufferGeometry();
  const vertices = [];
  for (let i = 0; i < 900; i++) {
    vertices.push(
      (Math.random() - 0.5) * 1400,
      (Math.random() - 0.5) * 1400,
      (Math.random() - 0.5) * 1400
    );
  }
  geometry.setAttribute("position", new THREE.Float32BufferAttribute(vertices, 3));
  const material = new THREE.PointsMaterial({ color: 0x6f7f9f, size: 1.2, transparent: true, opacity: 0.45 });
  state.scene.add(new THREE.Points(geometry, material));
}

function buildGraph() {
  const nodes = state.graph.nodes;
  const edges = state.graph.edges;

  const maxCentrality = Math.max(...nodes.map(n => n.dependency_centrality), 1);
  const positions = computeInitialPositions(nodes);

  nodes.forEach(node => {
    const mass = node.dependency_centrality;
    const radius = 8 + Math.sqrt(mass + 1) * 5;
    const color = categoryColors[node.category] || 0xffffff;

    const geometry = new THREE.SphereGeometry(radius, 32, 32);
    const material = new THREE.MeshStandardMaterial({
      color,
      emissive: color,
      emissiveIntensity: 0.18 + (mass / maxCentrality) * 0.35,
      roughness: 0.45,
      metalness: 0.05
    });

    const sphere = new THREE.Mesh(geometry, material);
    const p = positions.get(node.id);
    sphere.position.set(p.x, p.y, p.z);
    sphere.userData = node;

    state.scene.add(sphere);
    state.nodeObjects.set(node.id, sphere);

    const label = makeLabel(node.id.replace("UTE-FV-", ""));
    label.position.set(p.x, p.y - radius - 10, p.z);
    state.scene.add(label);
    state.labelObjects.set(node.id, label);
  });

  edges.forEach(edge => {
    const source = state.nodeObjects.get(edge.source);
    const target = state.nodeObjects.get(edge.target);
    if (!source || !target) return;

    const material = new THREE.LineBasicMaterial({
      color: 0x8391aa,
      transparent: true,
      opacity: 0.55,
      linewidth: 1
    });

    const points = [source.position, target.position];
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const line = new THREE.Line(geometry, material);
    line.userData = edge;
    state.scene.add(line);
    state.edgeObjects.push(line);
  });
}

function computeInitialPositions(nodes) {
  const positions = new Map();
  const categoryAngle = {
    Logic: 0,
    Arithmetic: Math.PI * 0.75,
    Geometry: Math.PI * 1.35,
    Measurement: Math.PI * 1.8
  };

  nodes.forEach((node, i) => {
    const centrality = node.dependency_centrality;
    const baseRadius = Math.max(35, 160 - centrality * 18);
    const angle = (categoryAngle[node.category] ?? 0) + i * 0.42;
    const z = (Math.sin(i * 1.31) * 70) + (node.category === "Logic" ? 0 : 20);
    positions.set(node.id, {
      x: Math.cos(angle) * baseRadius,
      y: Math.sin(angle) * baseRadius,
      z
    });
  });

  const equality = positions.get("UTE-FV-0002");
  if (equality) {
    equality.x = 0; equality.y = 0; equality.z = 0;
  }
  return positions;
}

function makeLabel(text) {
  const canvas = document.createElement("canvas");
  canvas.width = 256;
  canvas.height = 80;
  const ctx = canvas.getContext("2d");
  ctx.font = "bold 34px system-ui, sans-serif";
  ctx.fillStyle = "rgba(238,243,255,0.95)";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.shadowColor = "rgba(0,0,0,0.95)";
  ctx.shadowBlur = 10;
  ctx.fillText(text, 128, 40);

  const texture = new THREE.CanvasTexture(canvas);
  const material = new THREE.SpriteMaterial({ map: texture, transparent: true, depthWrite: false });
  const sprite = new THREE.Sprite(material);
  sprite.scale.set(46, 15, 1);
  return sprite;
}

function onCanvasClick(event) {
  const rect = state.renderer.domElement.getBoundingClientRect();
  const mouse = new THREE.Vector2(
    ((event.clientX - rect.left) / rect.width) * 2 - 1,
    -((event.clientY - rect.top) / rect.height) * 2 + 1
  );

  const raycaster = new THREE.Raycaster();
  raycaster.setFromCamera(mouse, state.camera);

  const intersects = raycaster.intersectObjects([...state.nodeObjects.values()]);
  if (intersects.length > 0) {
    const node = intersects[0].object.userData;
    showDetails(node);
    state.selected = node.id;
  }
}

function showDetails(node) {
  const dependents = state.graph.nodes
    .filter(n => n.dependencies.includes(node.id))
    .map(n => n.id)
    .join(", ") || "None listed";

  document.getElementById("details").innerHTML = `
    <h2>${node.id}</h2>
    <h3>${node.title}</h3>
    <p>${node.summary}</p>
    <div class="meta">
      <p><strong>Claim:</strong> ${node.claim}</p>
      <p><strong>Domain:</strong> ${node.category}</p>
      <p><strong>Confidence level:</strong> ${node.confidence_level}</p>
      <p><strong>Dependency centrality:</strong> ${node.dependency_centrality}</p>
      <p><strong>Depends on:</strong> ${node.dependencies.length ? node.dependencies.join(", ") : "None listed"}</p>
      <p><strong>Depended on by:</strong> ${dependents}</p>
    </div>
  `;
}

function applyFilters() {
  const q = document.getElementById("search").value.toLowerCase().trim();
  const category = document.getElementById("category-filter").value;

  const visible = new Set(state.graph.nodes
    .filter(n => {
      const matchesText = !q || n.id.toLowerCase().includes(q) || n.title.toLowerCase().includes(q);
      const matchesCategory = category === "all" || n.category === category;
      return matchesText && matchesCategory;
    })
    .map(n => n.id));

  state.nodeObjects.forEach((obj, id) => {
    obj.visible = visible.has(id);
  });
  state.labelObjects.forEach((obj, id) => {
    obj.visible = visible.has(id);
  });
  state.edgeObjects.forEach(line => {
    line.visible = visible.has(line.userData.source) && visible.has(line.userData.target);
  });
}

function onResize() {
  const container = document.getElementById("map3d");
  const width = container.clientWidth;
  const height = container.clientHeight;
  state.camera.aspect = width / height;
  state.camera.updateProjectionMatrix();
  state.renderer.setSize(width, height);
}

function animate() {
  requestAnimationFrame(animate);
  state.controls.update();
  state.renderer.render(state.scene, state.camera);
}

init();
