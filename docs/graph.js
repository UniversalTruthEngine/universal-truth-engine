import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

let scene, camera, renderer, controls, graph;
const nodeObjects = new Map();
const labelObjects = new Map();
const edgeObjects = [];
const proofCache = new Map();

const domainColors = {
  "Logic": 0xa78bfa,
  "Arithmetic": 0x82b7ff,
  "Geometry": 0x8df0a4,
  "Measurement": 0xffe27c,
  "Logic / Arithmetic": 0xa0a8ff,
  "Logic / Measurement": 0xb9a0ff,
  "Measurement / Arithmetic": 0xffdc85,
  "Measurement / Logic": 0xd7b2ff,
  "Measurement / Geometry": 0xb4efc2,
  "Arithmetic / Geometry": 0x8cdcb8,
  "Arithmetic / Measurement": 0x9ad5ff,
  "Geometry / Measurement": 0x9fe8bd
};

async function init() {
  setupScene();
  await loadGraph();
  setupUI();
  buildGraph();
  await loadHealth();
  animate();
}

async function loadGraph() {
  const response = await fetch("./data/truth-map-v1.json", { cache: "no-store" });
  graph = await response.json();
  document.getElementById("status").textContent =
    "Loaded " + graph.nodes.length + " truths and " + graph.edges.length + " dependency links.";
}

function setupScene() {
  const el = document.getElementById("map3d");
  const w = el.clientWidth;
  const h = el.clientHeight || 820;
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x050812);
  camera = new THREE.PerspectiveCamera(60, w / h, 0.1, 4000);
  camera.position.set(0, 0, 620);
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(w, h);
  el.appendChild(renderer.domElement);
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  scene.add(new THREE.AmbientLight(0xffffff, 0.82));
  const light = new THREE.PointLight(0x9cbcff, 1.4, 1600);
  light.position.set(240, 180, 320);
  scene.add(light);
  addStars();
  renderer.domElement.addEventListener("click", onCanvasClick);
  window.addEventListener("resize", resize);
}

function addStars() {
  const g = new THREE.BufferGeometry();
  const v = [];
  for (let i = 0; i < 1600; i++) v.push((Math.random() - 0.5) * 2200, (Math.random() - 0.5) * 2200, (Math.random() - 0.5) * 2200);
  g.setAttribute("position", new THREE.Float32BufferAttribute(v, 3));
  scene.add(new THREE.Points(g, new THREE.PointsMaterial({ color: 0x73839f, size: 1.15, transparent: true, opacity: 0.38 })));
}

function setupUI() {
  const filter = document.getElementById("domain-filter");
  const fly = document.getElementById("fly-to");
  [...new Set(graph.nodes.map(n => n.domain))].sort().forEach(domain => {
    const opt = document.createElement("option");
    opt.value = domain;
    opt.textContent = domain;
    filter.appendChild(opt);
  });
  graph.nodes.slice().sort((a, b) => a.id.localeCompare(b.id)).forEach(n => {
    const opt = document.createElement("option");
    opt.value = n.id;
    opt.textContent = n.id.replace("UTE-FV-", "") + " — " + n.title;
    fly.appendChild(opt);
  });
  document.getElementById("search").addEventListener("input", applyFilters);
  filter.addEventListener("change", applyFilters);
  fly.addEventListener("change", e => { if (e.target.value) flyToNode(e.target.value); });
  document.getElementById("reset-view").addEventListener("click", () => {
    camera.position.set(0, 0, 620);
    controls.target.set(0, 0, 0);
    controls.update();
    clearHighlight();
  });
}

function buildGraph() {
  const max = Math.max(...graph.nodes.map(n => n.dependency_centrality || 0), 1);
  graph.nodes.forEach(n => {
    const p = n.stable_coordinates || { x: 0, y: 0, z: 0 };
    const r = 9 + Math.sqrt((n.dependency_centrality || 0) + 1) * 5.5;
    const color = domainColors[n.domain] || 0x83b6ff;
    const sphere = new THREE.Mesh(new THREE.SphereGeometry(r, 32, 32), new THREE.MeshStandardMaterial({
      color, emissive: color, emissiveIntensity: 0.22 + ((n.dependency_centrality || 0) / max) * 0.45, roughness: 0.4, transparent: true, opacity: 1
    }));
    sphere.position.set(p.x, p.y, p.z);
    sphere.userData = n;
    scene.add(sphere);
    nodeObjects.set(n.id, sphere);
    const label = makeLabel(n.id.replace("UTE-FV-", "") + " " + n.title);
    label.position.set(p.x, p.y - r - 16, p.z);
    scene.add(label);
    labelObjects.set(n.id, label);
  });
  graph.edges.forEach(e => {
    const a = nodeObjects.get(e.source), b = nodeObjects.get(e.target);
    if (!a || !b) return;
    const line = new THREE.Line(new THREE.BufferGeometry().setFromPoints([a.position, b.position]), new THREE.LineBasicMaterial({ color: 0x8492aa, transparent: true, opacity: 0.34 }));
    line.userData = e;
    scene.add(line);
    edgeObjects.push(line);
  });
}

function makeLabel(text) {
  const c = document.createElement("canvas");
  c.width = 512; c.height = 96;
  const ctx = c.getContext("2d");
  ctx.font = "bold 27px system-ui";
  ctx.fillStyle = "rgba(238,243,255,.96)";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.shadowColor = "#000";
  ctx.shadowBlur = 12;
  ctx.fillText(text.slice(0, 38), 256, 48);
  const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(c), transparent: true, depthWrite: false, opacity: 0.9 }));
  sprite.scale.set(94, 18, 1);
  return sprite;
}

async function loadHealth() {
  try {
    const h = await (await fetch("./data/topology-health-preview.json", { cache: "no-store" })).json();
    document.getElementById("health").innerHTML = '<div class="meta"><p><strong>Map health:</strong> ' + h.truth_count + " truths, " + h.edge_count + " links.</p><p>Missing dependencies: " + h.missing_dependencies.length + "</p></div>";
  } catch (e) {}
}

function applyFilters() {
  const q = document.getElementById("search").value.toLowerCase().trim();
  const domain = document.getElementById("domain-filter").value;
  const visible = new Set(graph.nodes.filter(n => (!q || n.id.toLowerCase().includes(q) || n.title.toLowerCase().includes(q)) && (domain === "all" || n.domain === domain)).map(n => n.id));
  nodeObjects.forEach((obj, id) => obj.visible = visible.has(id));
  labelObjects.forEach((obj, id) => obj.visible = visible.has(id));
  edgeObjects.forEach(line => line.visible = visible.has(line.userData.source) && visible.has(line.userData.target));
}

function onCanvasClick(ev) {
  const rect = renderer.domElement.getBoundingClientRect();
  const mouse = new THREE.Vector2(((ev.clientX - rect.left) / rect.width) * 2 - 1, -((ev.clientY - rect.top) / rect.height) * 2 + 1);
  const ray = new THREE.Raycaster();
  ray.setFromCamera(mouse, camera);
  const hits = ray.intersectObjects([...nodeObjects.values()]);
  if (hits.length) {
    selectNode(hits[0].object.userData.id);
    document.getElementById("fly-to").value = hits[0].object.userData.id;
  }
}

async function selectNode(id) {
  const obj = nodeObjects.get(id);
  if (!obj) return;
  highlightChain(id);
  await showNode(obj.userData);
}

function getNode(id) { return graph.nodes.find(n => n.id === id); }

function getRecursiveDependencies(id, seen = new Set()) {
  const n = getNode(id);
  if (!n) return seen;
  (n.dependencies || []).forEach(dep => {
    if (!seen.has(dep)) {
      seen.add(dep);
      getRecursiveDependencies(dep, seen);
    }
  });
  return seen;
}

function highlightChain(id) {
  const chain = getRecursiveDependencies(id);
  chain.add(id);
  nodeObjects.forEach((o, k) => { o.material.opacity = chain.has(k) ? 1 : 0.16; o.material.emissiveIntensity = chain.has(k) ? 0.65 : 0.04; });
  labelObjects.forEach((o, k) => { o.material.opacity = chain.has(k) ? 1 : 0.13; });
  edgeObjects.forEach(l => {
    const active = chain.has(l.userData.source) && chain.has(l.userData.target);
    l.material.opacity = active ? 0.92 : 0.07;
    l.material.color.set(active ? 0xeef3ff : 0x8492aa);
  });
}

function clearHighlight() {
  nodeObjects.forEach(o => { o.material.opacity = 1; o.material.emissiveIntensity = 0.25; });
  labelObjects.forEach(o => o.material.opacity = 0.9);
  edgeObjects.forEach(l => { l.material.opacity = 0.34; l.material.color.set(0x8492aa); });
}

async function showNode(n) {
  const proofText = n.proof_file ? await loadText(n.proof_file) : "";
  const sections = parseMarkdownSections(proofText);
  const proofCards = sections.length ? sections.map(s => '<div class="proof-card"><h4>' + escapeHtml(s.title) + '</h4><pre>' + escapeHtml(s.content) + '</pre></div>').join("") : "<p>Proof file unavailable.</p>";
  const deps = (n.dependencies || []).length ? (n.dependencies || []).map(dep => '<span class="dep-link" data-dep="' + dep + '">' + dep + '</span>').join("") : "<p>None</p>";
  document.getElementById("details").innerHTML =
    "<h2>" + escapeHtml(n.id) + "</h2><h3>" + escapeHtml(n.title) + "</h3><p>" + escapeHtml(n.summary || "") + "</p>" +
    '<div class="meta"><p><strong>Domain:</strong> ' + escapeHtml(n.domain) + "</p><p><strong>Confidence:</strong> " + escapeHtml(String(n.confidence_level)) + "</p><p><strong>Dependency centrality:</strong> " + escapeHtml(String(n.dependency_centrality)) + "</p></div>" +
    '<div class="tabs"><button data-tab="summary">Summary</button><button data-tab="proof">Proof</button><button data-tab="dependencies">Dependencies</button><button data-tab="raw">Raw Proof</button></div>' +
    '<section id="tab-summary" class="tab active"><p>' + escapeHtml(n.summary || "") + "</p></section>" +
    '<section id="tab-proof" class="tab">' + proofCards + "</section>" +
    '<section id="tab-dependencies" class="tab"><h4>Dependencies</h4>' + deps + "</section>" +
    '<section id="tab-raw" class="tab"><pre>' + escapeHtml(proofText || "Proof file unavailable.") + "</pre></section>";
  document.querySelectorAll(".tabs button").forEach(btn => btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    document.getElementById("tab-" + btn.dataset.tab).classList.add("active");
  }));
  document.querySelectorAll(".dep-link").forEach(el => el.addEventListener("click", () => flyToNode(el.dataset.dep)));
}

function parseMarkdownSections(text) {
  if (!text) return [];
  const lines = text.split("\n");
  const sections = [];
  let title = "Overview", content = [];
  lines.forEach(line => {
    if (line.startsWith("## ")) {
      if (content.join("").trim()) sections.push({ title, content: content.join("\n").trim() });
      title = line.replace(/^## /, "").trim();
      content = [];
    } else if (!line.startsWith("# ")) {
      content.push(line);
    }
  });
  if (content.join("").trim()) sections.push({ title, content: content.join("\n").trim() });
  return sections;
}

async function loadText(path) {
  if (proofCache.has(path)) return proofCache.get(path);
  try {
    const res = await fetch(path, { cache: "no-store" });
    if (res.ok) {
      const text = await res.text();
      proofCache.set(path, text);
      return text;
    }
  } catch (e) {}
  return "";
}

function flyToNode(id) {
  const obj = nodeObjects.get(id);
  if (!obj) return;
  selectNode(id);
  const p = obj.position.clone(), start = camera.position.clone(), targetStart = controls.target.clone();
  const dir = new THREE.Vector3().subVectors(camera.position, controls.target).normalize();
  const end = p.clone().add(dir.multiplyScalar(155));
  let t = 0;
  function step() {
    t += 0.025;
    const k = 1 - Math.pow(1 - t, 3);
    camera.position.lerpVectors(start, end, k);
    controls.target.lerpVectors(targetStart, p, k);
    controls.update();
    if (t < 1) requestAnimationFrame(step);
  }
  step();
}

function escapeHtml(str) {
  return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function resize() {
  const el = document.getElementById("map3d");
  const w = el.clientWidth, h = el.clientHeight || 820;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h);
}

function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}

init().catch(e => {
  document.getElementById("status").textContent = "Map failed to load: " + e.message;
  console.error(e);
});
