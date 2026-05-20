import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

let scene,camera,renderer,controls,graph;
const nodeObjects=new Map(),edgeObjects=[];
const proofCache=new Map();

const colors={
Logic:0xa78bfa,
Arithmetic:0x82b7ff,
Geometry:0x8df0a4,
Measurement:0xffe27c,
"Logic / Arithmetic":0xa0a8ff,
"Measurement / Arithmetic":0xffdc85,
"Arithmetic / Geometry":0x8cdcb8,
"Arithmetic / Measurement":0x9ad5ff
};

async function init(){
setupScene();
await loadGraph();
setupUI();
buildGraph();
animate();
}

async function loadGraph(){
try{
graph=await (await fetch("./data/truth-map-generated-preview.json",{cache:"no-store"})).json();
}catch(e){
console.error(e);
document.getElementById("details").innerHTML="<h2>Could not load graph.</h2>";
}
}

function setupScene(){
const el=document.getElementById("map3d");
const w=el.clientWidth;
const h=el.clientHeight||820;

scene=new THREE.Scene();
scene.background=new THREE.Color(0x050812);

camera=new THREE.PerspectiveCamera(60,w/h,.1,4000);
camera.position.set(0,0,560);

renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setSize(w,h);
renderer.setPixelRatio(window.devicePixelRatio);
el.appendChild(renderer.domElement);

controls=new OrbitControls(camera,renderer.domElement);
controls.enableDamping=true;

scene.add(new THREE.AmbientLight(0xffffff,.85));

const light=new THREE.PointLight(0x9cbcff,1.4,1600);
light.position.set(240,180,320);
scene.add(light);

addStars();

renderer.domElement.addEventListener("click",onClick);

window.addEventListener("resize",resize);
}

function addStars(){
const g=new THREE.BufferGeometry();
const v=[];

for(let i=0;i<1600;i++){
v.push(
(Math.random()-.5)*2000,
(Math.random()-.5)*2000,
(Math.random()-.5)*2000
);
}

g.setAttribute("position",new THREE.Float32BufferAttribute(v,3));

scene.add(new THREE.Points(
g,
new THREE.PointsMaterial({
color:0x73839f,
size:1.2,
transparent:true,
opacity:.4
})
));
}

function buildGraph(){
const fly=document.getElementById("fly-to");

graph.nodes.forEach((n,i)=>{

const coords=n.stable_coordinates || {
x:Math.cos(i*.8)*220,
y:Math.sin(i*.8)*180,
z:(i%5)*50
};

const r=10+Math.sqrt((n.dependency_centrality||0)+1)*5;

const c=colors[n.domain]||0x83b6ff;

const mesh=new THREE.Mesh(
new THREE.SphereGeometry(r,32,32),
new THREE.MeshStandardMaterial({
color:c,
emissive:c,
emissiveIntensity:.28,
roughness:.4
})
);

mesh.position.set(coords.x,coords.y,coords.z);
mesh.userData=n;

scene.add(mesh);

nodeObjects.set(n.id,mesh);

const opt=document.createElement("option");
opt.value=n.id;
opt.textContent=n.id+" — "+n.title;
fly.appendChild(opt);

});

graph.edges.forEach(e=>{
const a=nodeObjects.get(e.source);
const b=nodeObjects.get(e.target);
if(!a||!b)return;

const line=new THREE.Line(
new THREE.BufferGeometry().setFromPoints([a.position,b.position]),
new THREE.LineBasicMaterial({
color:0x8492aa,
transparent:true,
opacity:.36
})
);

scene.add(line);
edgeObjects.push(line);
});
}

function setupUI(){

document.getElementById("fly-to").addEventListener("change",e=>{
if(e.target.value){
flyToNode(e.target.value);
}
});

document.getElementById("reset-view").addEventListener("click",()=>{
camera.position.set(0,0,560);
controls.target.set(0,0,0);
controls.update();
});

document.getElementById("search").addEventListener("input",applySearch);
}

function applySearch(e){
const q=e.target.value.toLowerCase().trim();

nodeObjects.forEach((obj,id)=>{
const n=obj.userData;
const vis=!q ||
id.toLowerCase().includes(q) ||
n.title.toLowerCase().includes(q);

obj.visible=vis;
});

edgeObjects.forEach(line=>{
line.visible=line.geometry;
});
}

function onClick(ev){

const rect=renderer.domElement.getBoundingClientRect();

const mouse=new THREE.Vector2(
((ev.clientX-rect.left)/rect.width)*2-1,
-((ev.clientY-rect.top)/rect.height)*2+1
);

const ray=new THREE.Raycaster();

ray.setFromCamera(mouse,camera);

const hits=ray.intersectObjects([...nodeObjects.values()]);

if(hits.length){
showNode(hits[0].object.userData);
}
}

async function loadProof(path){

if(proofCache.has(path)){
return proofCache.get(path);
}

try{
const text=await (await fetch("./"+path,{cache:"no-store"})).text();
proofCache.set(path,text);
return text;
}catch(e){
return "Could not load proof file.";
}
}

function parseSections(text){

const sections=[];
const lines=text.split("\n");

let current={title:"Document",content:[]};

for(const line of lines){

if(line.startsWith("## ")){
sections.push(current);
current={
title:line.replace(/^## /,"").trim(),
content:[]
};
}else{
current.content.push(line);
}
}

sections.push(current);

return sections.filter(s=>s.content.join("").trim().length>0);
}

async function showNode(n){

const deps=(n.dependencies||[]);

let proofText="No proof file.";

if(n.proof_file){
proofText=await loadProof(n.proof_file);
}

const sections=parseSections(proofText);

let html=`
<h2>${n.id}</h2>
<h3>${n.title}</h3>

<div class="proof-section">
<p><strong>Domain:</strong> ${n.domain||"Unknown"}</p>
<p><strong>Confidence:</strong> ${n.confidence_level||"Unknown"}</p>
</div>

<div class="proof-section">
<h3>Dependencies</h3>
`;

if(deps.length){
deps.forEach(dep=>{
html+=`<span class="dep-link" data-dep="${dep}">${dep}</span>`;
});
}else{
html+="<p>None</p>";
}

html+="</div>";

sections.forEach(sec=>{
html+=`
<div class="proof-section">
<h3>${sec.title}</h3>
<pre style="white-space:pre-wrap;font-family:inherit">${escapeHtml(sec.content.join("\n"))}</pre>
</div>
`;
});

document.getElementById("details").innerHTML=html;

document.querySelectorAll(".dep-link").forEach(el=>{
el.addEventListener("click",()=>{
const dep=el.dataset.dep;
flyToNode(dep);
});
});
}

function flyToNode(id){

const obj=nodeObjects.get(id);

if(!obj)return;

showNode(obj.userData);

const p=obj.position.clone();

const start=camera.position.clone();
const targetStart=controls.target.clone();

const dir=new THREE.Vector3()
.subVectors(camera.position,controls.target)
.normalize();

const end=p.clone().add(dir.multiplyScalar(150));

let t=0;

function step(){

t+=.025;

const k=1-Math.pow(1-t,3);

camera.position.lerpVectors(start,end,k);
controls.target.lerpVectors(targetStart,p,k);

controls.update();

if(t<1){
requestAnimationFrame(step);
}
}

step();
}

function escapeHtml(str){
return str
.replace(/&/g,"&amp;")
.replace(/</g,"&lt;")
.replace(/>/g,"&gt;");
}

function resize(){
const el=document.getElementById("map3d");
const w=el.clientWidth;
const h=el.clientHeight||820;

camera.aspect=w/h;
camera.updateProjectionMatrix();

renderer.setSize(w,h);
}

function animate(){
requestAnimationFrame(animate);
controls.update();
renderer.render(scene,camera);
}

init();
