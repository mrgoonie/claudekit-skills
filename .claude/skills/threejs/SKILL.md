---
name: threejs
description: Build 3D web apps with Three.js (WebGL/WebGPU). Use for 3D scenes, animations, custom shaders, PBR materials, VR/XR experiences, games, data visualizations, product configurators.
license: MIT
version: 2.0.0
---

# Three.js Development

Build high-performance 3D web applications using Three.js - a cross-browser WebGL/WebGPU library.

## When to Use This Skill

Use when working with:
- 3D scenes, models, animations, or visualizations
- WebGL/WebGPU rendering and graphics programming
- Interactive 3D experiences (games, configurators, data viz)
- Camera controls, lighting, materials, or shaders
- Loading 3D assets (GLTF, FBX, OBJ) or textures
- Post-processing effects (bloom, depth of field, SSAO)
- Physics simulations, VR/XR experiences, or spatial audio
- Performance optimization (instancing, LOD, frustum culling)

## Progressive Learning Path

### Level 1: Getting Started
- Load `references/00-fundamentals.md` - Fundamentals
- Load `references/01-getting-started.md` - Scene setup, basic geometries, materials, lights, rendering loop

### Level 2: Common Tasks
- **Asset Loading**: `references/02-loaders.md` - GLTF, FBX, OBJ, texture loaders
- **Textures**: `references/03-textures.md` - Types, mapping, wrapping, filtering
- **Cameras**: `references/04-cameras.md` - Perspective, orthographic, controls
- **Lights**: `references/05-lights.md` - Types, shadows, helpers
- **Animations**: `references/06-animations.md` - Clips, mixer, keyframes
- **Math**: `references/07-math.md` - Vectors, matrices, quaternions, curves
- **Geometry**: `references/18-geometry.md` - Built-in shapes, BufferGeometry, custom geometry, instancing
- **Materials**: `references/11-materials.md` - PBR, basic, phong, lambert, physical, toon, normal, depth, raw, shader materials, material properties

### Level 3: Interactive & Effects
- **Interaction**: `references/08-interaction.md` - Raycasting, picking, transforms
- **Post-Processing**: `references/09-postprocessing.md` - Passes, bloom, SSAO, SSR
- **Controls (Addons)**: `references/10-controls.md` - Orbit, transform, first-person

### Level 4: Advanced Rendering
- **Materials Advanced**: `references/11-materials-advanced.md` - PBR, custom shaders
- **Performance**: `references/12-performance.md` - Instancing, LOD, batching, culling
- **Node Materials (TSL)**: `references/13-node-materials.md` - Shader graphs, compute

### Level 5: Specialized
- **Physics**: `references/14-physics-vr.md` - Ammo, Rapier, Jolt, VR/XR
- **Advanced Loaders**: `references/15-specialized-loaders.md` - SVG, VRML, domain-specific
- **WebGPU**: `references/16-webgpu.md` - Modern backend, compute shaders
- **Shaders**: `references/17-shader.md` - GLSL, ShaderMaterial, uniforms, custom effects

## Quick Start Pattern

```javascript
// 1. Scene, Camera, Renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// 2. Add Objects
const geometry = new THREE.BoxGeometry();
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

// 3. Add Lights
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 5, 5);
scene.add(light);
scene.add(new THREE.AmbientLight(0x404040));

// 4. Animation Loop
function animate() {
  requestAnimationFrame(animate);
  cube.rotation.x += 0.01;
  cube.rotation.y += 0.01;
  renderer.render(scene, camera);
}
animate();
```

## External Resources

- Official Docs: https://threejs.org/docs/
- Examples: https://threejs.org/examples/
- Editor: https://threejs.org/editor/
- Discord: https://discord.gg/56GBJwAnUS
