import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

const colors={Logic:0xa78bfa,Arithmetic:0x83b6ff,Geometry:0x8df0a4,Measurement:0xffe27c};
let graph,scene,camera,renderer,controls;const nodeObjects=new Map(),labelObjects=new Map(),edgeObjects=[];

async function init(){
 try{
  graph=await (await fetch("./data/truth-map-v1.json",{cache:"no-store"})).json();
  setupControls(); setupScene(); buildGraph(); animate();
  document.getElementById("status").textContent="3D map loaded. Truth Inspector v1 active.";
 }catch(e){document.getElementById("status").textContent="Map failed to load: "+e.message; console.error(e)}
}

function setupControls(){
 const catSelect=document.getElementById("category-filter"), fly=document.getElementById("fly-to");
 [...new Set(graph.nodes.map(n=>n.category))].sort().forEach(c=>{const o=document.createElement("option");o.value=c;o.textContent=c;catSelect.appendChild(o)});
 graph.nodes.sort((a,b)=>a.id.localeCompare(b.id)).forEach(n=>{const o=document.createElement("option");o.value=n.id;o.textContent=n.id.replace("UTE-FV-","")+" — "+n.title;fly.appendChild(o)});
 document.getElementById("search").addEventListener("input",applyFilters);
 catSelect.addEventListener("change",applyFilters);
 fly.addEventListener("change",()=>{if(fly.value)flyToNode(fly.value)});
 document.getElementById("reset-view").addEventListener("click",()=>{camera.position.set(0,0,520);controls.target.set(0,0,0);controls.update()});
}

function setupScene(){
 const el=document.getElementById("map3d"),w=el.clientWidth,h=el.clientHeight||780;
 scene=new THREE.Scene(); scene.background=new THREE.Color(0x050812);
 camera=new THREE.PerspectiveCamera(60,w/h,.1,4000); camera.position.set(0,0,520);
 renderer=new THREE.WebGLRenderer({antialias:true}); renderer.setPixelRatio(window.devicePixelRatio); renderer.setSize(w,h); el.appendChild(renderer.domElement);
 controls=new OrbitControls(camera,renderer.domElement); controls.enableDamping=true; controls.dampingFactor=.06;
 scene.add(new THREE.AmbientLight(0xffffff,.8)); const light=new THREE.PointLight(0x9dbdff,1.5,1200); light.position.set(220,160,320); scene.add(light);
 addStars(); renderer.domElement.addEventListener("click",clickNode); window.addEventListener("resize",resize);
}

function addStars(){const g=new THREE.BufferGeometry(),v=[];for(let i=0;i<1400;i++)v.push((Math.random()-.5)*1800,(Math.random()-.5)*1800,(Math.random()-.5)*1800);g.setAttribute("position",new THREE.Float32BufferAttribute(v,3));scene.add(new THREE.Points(g,new THREE.PointsMaterial({color:0x6f7f9f,size:1.15,transparent:true,opacity:.42})))}

function buildGraph(){
 const max=Math.max(...graph.nodes.map(n=>n.dependency_centrality),1);
 graph.nodes.forEach(n=>{
  const p=n.stable_coordinates; const r=10+Math.sqrt(n.dependency_centrality+1)*6; const c=colors[n.category]||0xffffff;
  const s=new THREE.Mesh(new THREE.SphereGeometry(r,32,32),new THREE.MeshStandardMaterial({color:c,emissive:c,emissiveIntensity:.2+(n.dependency_centrality/max)*.45,roughness:.4}));
  s.position.set(p.x,p.y,p.z); s.userData=n; scene.add(s); nodeObjects.set(n.id,s);
  const lab=makeLabel(n.id.replace("UTE-FV-","")); lab.position.set(p.x,p.y-r-13,p.z); scene.add(lab); labelObjects.set(n.id,lab);
 });
 graph.edges.forEach(e=>{const a=nodeObjects.get(e.source),b=nodeObjects.get(e.target);if(!a||!b)return;const line=new THREE.Line(new THREE.BufferGeometry().setFromPoints([a.position,b.position]),new THREE.LineBasicMaterial({color:0x8391aa,transparent:true,opacity:.56}));line.userData=e;scene.add(line);edgeObjects.push(line)});
}

function makeLabel(t){const c=document.createElement("canvas");c.width=256;c.height=80;const x=c.getContext("2d");x.font="bold 34px system-ui";x.fillStyle="rgba(238,243,255,.95)";x.textAlign="center";x.textBaseline="middle";x.shadowColor="#000";x.shadowBlur=10;x.fillText(t,128,40);const spr=new THREE.Sprite(new THREE.SpriteMaterial({map:new THREE.CanvasTexture(c),transparent:true,depthWrite:false}));spr.scale.set(48,15,1);return spr}

function clickNode(e){const r=renderer.domElement.getBoundingClientRect();const mouse=new THREE.Vector2(((e.clientX-r.left)/r.width)*2-1,-((e.clientY-r.top)/r.height)*2+1);const ray=new THREE.Raycaster();ray.setFromCamera(mouse,camera);const hit=ray.intersectObjects([...nodeObjects.values()]);if(hit.length){showInspector(hit[0].object.userData);document.getElementById("fly-to").value=hit[0].object.userData.id}}

async function showInspector(n){
 const detail=await (await fetch("./"+n.truth_data_file,{cache:"no-store"})).json();
 const depended=detail.related_truths?.depended_on_by?.join(", ")||"None listed";
 document.getElementById("details").innerHTML=`<h2>${detail.id}</h2><h3>${detail.title}</h3><div class="inspector-tabs"><button data-tab="summary">Summary</button><button data-tab="proof">Proof</button><button data-tab="validation">Validation</button><button data-tab="links">Links</button></div><section id="tab-summary" class="truth-section active"><p>${detail.summary}</p><div class="meta"><p><strong>Claim:</strong> ${detail.claim}</p><p><strong>Domain:</strong> ${detail.category}</p><p><strong>Region:</strong> ${detail.region}</p></div></section><section id="tab-proof" class="truth-section"><p><strong>Intuitive / structural proof:</strong></p><p>${detail.proof_layers.formal_or_structural_proof}</p><p><strong>Reconstruction basis:</strong></p><p>${detail.proof_layers.empirical_or_reconstruction_basis}</p></section><section id="tab-validation" class="truth-section"><p>${detail.proof_layers.validation_assessment}</p><p><strong>Confidence level:</strong> ${detail.confidence_level}</p><p><strong>Dependency centrality:</strong> ${detail.dependency_centrality}</p></section><section id="tab-links" class="truth-section"><p><strong>Depends on:</strong> ${detail.dependencies.length?detail.dependencies.join(", "):"None listed"}</p><p><strong>Depended on by:</strong> ${depended}</p><p><strong>Stable coordinates:</strong> (${detail.stable_coordinates.x}, ${detail.stable_coordinates.y}, ${detail.stable_coordinates.z})</p><a class="small-link" href="./${n.truth_data_file}" target="_blank">Open machine-readable truth object</a></section>`;
 document.querySelectorAll(".inspector-tabs button").forEach(btn=>btn.addEventListener("click",()=>{document.querySelectorAll(".truth-section").forEach(s=>s.classList.remove("active"));document.getElementById("tab-"+btn.dataset.tab).classList.add("active")}));
}

function flyToNode(id){const obj=nodeObjects.get(id); if(!obj)return; showInspector(obj.userData); const p=obj.position; const start=camera.position.clone(), targetStart=controls.target.clone(); const direction=new THREE.Vector3().subVectors(camera.position,controls.target).normalize(); const end=new THREE.Vector3(p.x,p.y,p.z).add(direction.multiplyScalar(150)); const endTarget=new THREE.Vector3(p.x,p.y,p.z); let t=0; function step(){t+=0.025; const k=1-Math.pow(1-t,3); camera.position.lerpVectors(start,end,k); controls.target.lerpVectors(targetStart,endTarget,k); controls.update(); if(t<1)requestAnimationFrame(step)} step()}

function applyFilters(){const q=document.getElementById("search").value.toLowerCase().trim(),cat=document.getElementById("category-filter").value;const vis=new Set(graph.nodes.filter(n=>(!q||n.id.toLowerCase().includes(q)||n.title.toLowerCase().includes(q))&&(cat==="all"||n.category===cat)).map(n=>n.id));nodeObjects.forEach((o,id)=>o.visible=vis.has(id));labelObjects.forEach((o,id)=>o.visible=vis.has(id));edgeObjects.forEach(l=>l.visible=vis.has(l.userData.source)&&vis.has(l.userData.target))}

function resize(){const el=document.getElementById("map3d"),w=el.clientWidth,h=el.clientHeight||780;camera.aspect=w/h;camera.updateProjectionMatrix();renderer.setSize(w,h)}
function animate(){requestAnimationFrame(animate);controls.update();renderer.render(scene,camera)}
init();
