import React, { useState, useRef, Suspense, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrthographicCamera, PerspectiveCamera, OrbitControls, Html } from '@react-three/drei';
import * as THREE from 'three';
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader.js';
import { Upload, Maximize2, Crosshair, Grid, Settings2, Box, Scaling, Ruler, Download } from 'lucide-react';
import { STLExporter } from 'three/examples/jsm/exporters/STLExporter.js';
import * as BufferGeometryUtils from 'three/examples/jsm/utils/BufferGeometryUtils.js';

const PRINTERS = [
  { name: 'Flashforge Creator 5 Pro', width: 256, depth: 256, height: 300, style: 'enclosed' },
  { name: 'Bambu Lab X1 / P1S', width: 256, depth: 256, height: 256, style: 'enclosed' },
  { name: 'Creality Ender 3', width: 220, depth: 220, height: 250, style: 'i3' },
  { name: 'Prusa MK3S+ / MK4', width: 250, depth: 210, height: 220, style: 'i3' },
  { name: 'Voron 2.4 (350mm)', width: 350, depth: 350, height: 350, style: 'corexy' },
  { name: 'Elegoo Neptune 3 Max', width: 420, depth: 420, height: 500, style: 'i3' },
  { name: 'Auto Garage (1-Car)', width: 3500, depth: 6000, height: 2500, style: 'garage' },
  { name: 'Airport Hangar', width: 30000, depth: 30000, height: 15000, style: 'hangar' },
  { name: 'Custom Printer...', width: 300, depth: 300, height: 300, style: 'enclosed' }
];

const ModelRenderer = ({ geometry, scale = 1, snapRotation = {x:0, y:0, z:0}, showMeasurements = false, unit = 'mm', isPreviewMode = true }: { geometry: THREE.BufferGeometry | null, scale?: number, snapRotation?: {x:number, y:number, z:number}, showMeasurements?: boolean, unit?: 'mm' | 'in' | 'ft' | 'yd', isPreviewMode?: boolean }) => {
  if (!geometry) return null;
  
  const baseColor = "#ffaa00";
  const edgeColor = "#ffff00";

  let yOffset = 0;
  let xOffset = 0;
  let zOffset = 0;
  const size = new THREE.Vector3();
  
  if (geometry.boundingBox) {
    const dummy = new THREE.Mesh(geometry);
    dummy.rotation.set(snapRotation.x, snapRotation.y, snapRotation.z);
    dummy.scale.set(scale, scale, scale);
    dummy.updateMatrixWorld(true);
    const box = new THREE.Box3().setFromObject(dummy);
    box.getSize(size);
    yOffset = -box.min.y;
    const center = new THREE.Vector3();
    box.getCenter(center);
    xOffset = -center.x;
    zOffset = -center.z;
  }

  const format = (val: number) => {
    if (unit === 'in') return (val / 25.4).toFixed(2);
    if (unit === 'ft') return (val / 304.8).toFixed(2);
    if (unit === 'yd') return (val / 914.4).toFixed(2);
    return val.toFixed(2);
  };

  return (
    <group position={[xOffset, yOffset, zOffset]}>
      <group rotation={[snapRotation.x, snapRotation.y, snapRotation.z]}>
        <mesh geometry={geometry} scale={[scale, scale, scale]}>
          <meshBasicMaterial color={baseColor} wireframe={false} transparent opacity={0.4} blending={THREE.AdditiveBlending} depthWrite={false} />
          <lineSegments>
            <edgesGeometry args={[geometry, 15]} />
            <lineBasicMaterial color={edgeColor} linewidth={2} transparent opacity={0.8} blending={THREE.AdditiveBlending} depthWrite={false} />
          </lineSegments>
        </mesh>
      </group>

      {/* Measurement Overlays placed in the unrotated parent group! */}
      {showMeasurements && size.length() > 0 && (
        <group>
          <Html position={[0, 0, size.z/2 + 15]} center style={{ pointerEvents: 'none' }}>
            <div className={`px-2 py-1 rounded text-xs font-mono whitespace-nowrap shadow-xl border ${isPreviewMode ? 'bg-[#2a1700]/90 text-amber-500 border-[#4a2800]' : 'bg-black text-[#ffaa00] border-[#ffaa00]/50'}`}>
              X: {format(size.x)} {unit}
            </div>
          </Html>
          <Html position={[size.x/2 + 15, 0, 0]} center style={{ pointerEvents: 'none' }}>
            <div className={`px-2 py-1 rounded text-xs font-mono whitespace-nowrap shadow-xl border ${isPreviewMode ? 'bg-[#2a1700]/90 text-amber-500 border-[#4a2800]' : 'bg-black text-[#ffaa00] border-[#ffaa00]/50'}`}>
              Y: {format(size.z)} {unit}
            </div>
          </Html>
          <Html position={[-size.x/2 - 15, size.y/2, 0]} center style={{ pointerEvents: 'none' }}>
            <div className={`px-2 py-1 rounded text-xs font-mono whitespace-nowrap shadow-xl border ${isPreviewMode ? 'bg-[#2a1700]/90 text-amber-500 border-[#4a2800]' : 'bg-black text-[#ffaa00] border-[#ffaa00]/50'}`}>
              Z: {format(size.y)} {unit}
            </div>
          </Html>
        </group>
      )}
    </group>
  );
};

const VirtualPrinter = ({ width, depth, height, style, isPreviewMode, isCalibrating, showMeasurements = false, unit = 'mm' }: { width: number, depth: number, height: number, style: string, isPreviewMode: boolean, isCalibrating: boolean, showMeasurements?: boolean, unit?: 'mm'|'in'|'ft'|'yd' }) => {
  const lightColor = "#ffaa00";

  // In projection mode, we MUST project a pitch-black background.
  // We will ALWAYS render the glowing boundary outline so there is contrast on the physical build plate!
  if (!isPreviewMode) {
    return (
      <group position={[0, -1, 0]}>
        {/* Only show the full grid if actively calibrating */}
        {isCalibrating && (
          <gridHelper args={[Math.max(width, depth), Math.max(width, depth) / 10, '#4a2800', '#2a1700']} />
        )}
        <lineSegments rotation={[-Math.PI/2, 0, 0]}>
          <edgesGeometry args={[new THREE.PlaneGeometry(width, depth)]} />
          <lineBasicMaterial color={lightColor} linewidth={2} transparent opacity={1} />
        </lineSegments>
      </group>
    );
  }

  const BuildPlate = () => {
    let gridDivisions = Math.max(width, depth) / 10;
    if (style === 'garage') gridDivisions = Math.max(width, depth) / 100; // 100mm grid for garage
    if (style === 'hangar') gridDivisions = Math.max(width, depth) / 1000; // 1000mm grid for hangar
    
    const format = (val: number) => {
        if (unit === 'in') return (val / 25.4).toFixed(1) + ' in';
        if (unit === 'ft') return (val / 304.8).toFixed(2) + ' ft';
        if (unit === 'yd') return (val / 914.4).toFixed(2) + ' yd';
        if (val >= 1000 && unit === 'mm') return (val / 1000).toFixed(1) + ' m';
        return val.toFixed(1) + ' mm';
    };
    
    return (
      <group position={[0, 0, 0]}>
        <mesh position={[0, -3.5, 0]}>
          <boxGeometry args={[width + 4, 5, depth + 4]} />
          <meshStandardMaterial color={style === 'garage' || style === 'hangar' ? "#1a1a1a" : "#3a2000"} metalness={0.5} roughness={0.8} />
        </mesh>
        <mesh position={[0, -0.5, 0]}>
          <boxGeometry args={[width, 1, depth]} />
          <meshStandardMaterial color={style === 'garage' || style === 'hangar' ? "#0f0f0f" : "#1a0f00"} metalness={0.2} roughness={0.8} />
        </mesh>
        <gridHelper args={[Math.max(width, depth), gridDivisions, '#4a2800', '#2a1700']} position={[0, 0.05, 0]} />
        <group position={[0, 0.1, 0]} rotation={[-Math.PI / 2, 0, 0]}>
          <lineSegments>
            <edgesGeometry args={[new THREE.PlaneGeometry(width, depth)]} />
            <lineBasicMaterial color={lightColor} linewidth={2} transparent opacity={0.6} />
          </lineSegments>
        </group>

        {showMeasurements && isPreviewMode && (
          <group>
            <Html position={[0, 0, depth/2 + (style==='hangar'?500:20)]} center style={{ pointerEvents: 'none' }}>
              <div className="px-2 py-1 rounded text-[10px] font-mono whitespace-nowrap opacity-60 bg-black text-[#8a5d00] border border-[#4a2800]">
                Width: {format(width)}
              </div>
            </Html>
            <Html position={[width/2 + (style==='hangar'?500:20), 0, 0]} center style={{ pointerEvents: 'none' }}>
              <div className="px-2 py-1 rounded text-[10px] font-mono whitespace-nowrap opacity-60 bg-black text-[#8a5d00] border border-[#4a2800]">
                Depth: {format(depth)}
              </div>
            </Html>
            <Html position={[-width/2 - (style==='hangar'?500:20), height/2, 0]} center style={{ pointerEvents: 'none' }}>
              <div className="px-2 py-1 rounded text-[10px] font-mono whitespace-nowrap opacity-60 bg-black text-[#8a5d00] border border-[#4a2800]">
                Height: {format(height)}
              </div>
            </Html>
          </group>
        )}
      </group>
    );
  };

  const LightCone = ({ headY }: { headY: number }) => (
    <group position={[0, headY, 0]}>
      <mesh position={[0, -10, 0]}>
        <boxGeometry args={[40, 20, 40]} />
        <meshStandardMaterial color="#2a1700" />
      </mesh>
      <mesh position={[0, -headY/2 - 20, 0]}>
        <cylinderGeometry args={[width/1.5, 1, headY, 32, 1, true]} />
        <meshBasicMaterial color={lightColor} transparent opacity={0.03} side={THREE.DoubleSide} blending={THREE.AdditiveBlending} depthWrite={false} />
      </mesh>
    </group>
  );

  if (style === 'garage') {
    return (
      <group>
        <BuildPlate />
        {/* Back Wall */}
        <mesh position={[0, height/2, -depth/2 - 50]}><boxGeometry args={[width, height, 100]} /><meshStandardMaterial color="#222" /></mesh>
        {/* Side Walls */}
        <mesh position={[width/2 + 50, height/2, 0]}><boxGeometry args={[100, height, depth]} /><meshStandardMaterial color="#222" /></mesh>
        <mesh position={[-width/2 - 50, height/2, 0]}><boxGeometry args={[100, height, depth]} /><meshStandardMaterial color="#222" /></mesh>
        {/* Roof */}
        <mesh position={[0, height + 50, 0]}><boxGeometry args={[width + 200, 100, depth + 200]} /><meshStandardMaterial color="#111" /></mesh>
        <LightCone headY={height} />
      </group>
    );
  }

  if (style === 'hangar') {
    return (
      <group>
        <BuildPlate />
        {/* Back Wall */}
        <mesh position={[0, height/2, -depth/2 - 500]}><boxGeometry args={[width, height, 1000]} /><meshStandardMaterial color="#1a1a1a" /></mesh>
        {/* Arch Roof */}
        <mesh position={[0, height, 0]} rotation={[Math.PI/2, Math.PI/2, 0]}>
          <cylinderGeometry args={[width/2, width/2, depth, 32, 1, true, 0, Math.PI]} />
          <meshStandardMaterial color="#111" side={THREE.DoubleSide} />
        </mesh>
        <LightCone headY={height} />
      </group>
    );
  }

  if (style === 'i3') {
    return (
      <group>
        <BuildPlate />
        <mesh position={[0, -12, 0]}><boxGeometry args={[40, 16, depth + 60]} /><meshStandardMaterial color="#140b00" /></mesh>
        <mesh position={[0, -12, 0]}><boxGeometry args={[width + 100, 16, 40]} /><meshStandardMaterial color="#140b00" /></mesh>
        <mesh position={[width/2 + 25, height/2, 0]}><boxGeometry args={[20, height + 40, 40]} /><meshStandardMaterial color="#1a0f00" /></mesh>
        <mesh position={[-width/2 - 25, height/2, 0]}><boxGeometry args={[20, height + 40, 40]} /><meshStandardMaterial color="#1a0f00" /></mesh>
        <mesh position={[0, height + 20, 0]}><boxGeometry args={[width + 100, 20, 40]} /><meshStandardMaterial color="#1a0f00" /></mesh>
        <mesh position={[0, height - 10, 0]}><boxGeometry args={[width + 60, 20, 20]} /><meshStandardMaterial color="#2a1700" /></mesh>
        <LightCone headY={height} />
      </group>
    );
  }

  if (style === 'corexy') {
    const ext = 20;
    return (
      <group>
        <BuildPlate />
        <mesh position={[0, -12, -depth/2 + 20]}><boxGeometry args={[width - 40, 16, 40]} /><meshStandardMaterial color="#1a0f00" /></mesh>
        <mesh position={[0, -20, 0]}><boxGeometry args={[width + 60, ext, depth + 60]} /><meshStandardMaterial color="#0a0500" /></mesh>
        <mesh position={[0, height + 20, 0]}><boxGeometry args={[width + 60, ext, depth + 60]} /><meshStandardMaterial color="#0a0500" /></mesh>
        <mesh position={[width/2 + 20, height/2, depth/2 + 20]}><boxGeometry args={[ext, height + 40, ext]} /><meshStandardMaterial color="#140b00" /></mesh>
        <mesh position={[-width/2 - 20, height/2, depth/2 + 20]}><boxGeometry args={[ext, height + 40, ext]} /><meshStandardMaterial color="#140b00" /></mesh>
        <mesh position={[width/2 + 20, height/2, -depth/2 - 20]}><boxGeometry args={[ext, height + 40, ext]} /><meshStandardMaterial color="#140b00" /></mesh>
        <mesh position={[-width/2 - 20, height/2, -depth/2 - 20]}><boxGeometry args={[ext, height + 40, ext]} /><meshStandardMaterial color="#140b00" /></mesh>
        <LightCone headY={height} />
      </group>
    );
  }

  const frameColor = "#2a1700";
  const frameThickness = 20;
  return (
    <group>
      <group position={[0, 0, 0]}>
        <BuildPlate />
        <mesh position={[0, -12, -depth/2 + 20]}><boxGeometry args={[width - 40, 16, 40]} /><meshStandardMaterial color="#1a0f00" /></mesh>
        <mesh position={[-width/2 + 30, -height/2, -depth/2 + 20]}><cylinderGeometry args={[4, 4, height]} /><meshStandardMaterial color="#3a2000" metalness={0.9} /></mesh>
        <mesh position={[width/2 - 30, -height/2, -depth/2 + 20]}><cylinderGeometry args={[4, 4, height]} /><meshStandardMaterial color="#3a2000" metalness={0.9} /></mesh>
      </group>
      <mesh position={[0, -height/2 - 10, 0]}><boxGeometry args={[width + frameThickness*2, 20, depth + frameThickness*2]} /><meshStandardMaterial color="#140b00" /></mesh>
      <mesh position={[width/2 + frameThickness/2, height/2, -depth/2 - frameThickness/2]}><boxGeometry args={[frameThickness, height, frameThickness]} /><meshStandardMaterial color={frameColor} /></mesh>
      <mesh position={[-width/2 - frameThickness/2, height/2, -depth/2 - frameThickness/2]}><boxGeometry args={[frameThickness, height, frameThickness]} /><meshStandardMaterial color={frameColor} /></mesh>
      <mesh position={[width/2 + frameThickness/2, height/2, depth/2 + frameThickness/2]}><boxGeometry args={[frameThickness, height, frameThickness]} /><meshStandardMaterial color={frameColor} /></mesh>
      <mesh position={[-width/2 - frameThickness/2, height/2, depth/2 + frameThickness/2]}><boxGeometry args={[frameThickness, height, frameThickness]} /><meshStandardMaterial color={frameColor} /></mesh>
      <mesh position={[width/2 + frameThickness/2, height/2, 0]}><boxGeometry args={[2, height, depth]} /><meshPhysicalMaterial color="#ffaa00" transmission={0.9} opacity={0.2} transparent roughness={0.1} /></mesh>
      <mesh position={[-width/2 - frameThickness/2, height/2, 0]}><boxGeometry args={[2, height, depth]} /><meshPhysicalMaterial color="#ffaa00" transmission={0.9} opacity={0.2} transparent roughness={0.1} /></mesh>
      <mesh position={[0, height + frameThickness/2, 0]}><boxGeometry args={[width + frameThickness*2, frameThickness, depth + frameThickness*2]} /><meshStandardMaterial color={frameColor} /></mesh>
      <LightCone headY={height} />
    </group>
  );
};

function App() {
  const [models, setModels] = useState<any[]>([]);
  const [activeModelId, setActiveModelId] = useState<string | null>(null);

  const activeModel = models.find(m => m.id === activeModelId);
  const geometry = activeModel?.geometry || null;
  const objectScale = activeModel?.scale || 1;
  const panOffset = activeModel?.panOffset || { x: 0, z: 0 };
  const fineRotationY = activeModel?.fineRotationY || 0;
  const snapRotation = activeModel?.snapRotation || { x: 0, y: 0, z: 0 };

  const updateActiveModel = (updater: (prev: any) => any) => {
    setModels(prev => prev.map(m => m.id === activeModelId ? updater(m) : m));
  };

  const setPanOffset = (updater: any) => updateActiveModel(m => ({ ...m, panOffset: typeof updater === 'function' ? updater(m.panOffset) : updater }));
  const setFineRotationY = (updater: any) => updateActiveModel(m => ({ ...m, fineRotationY: typeof updater === 'function' ? updater(m.fineRotationY) : updater }));
  const setSnapRotation = (updater: any) => updateActiveModel(m => ({ ...m, snapRotation: typeof updater === 'function' ? updater(m.snapRotation) : updater }));
  const setObjectScale = (val: number) => updateActiveModel(m => ({ ...m, scale: val }));

  const [isCalibrating, setIsCalibrating] = useState(false);
  const [isPreviewMode, setIsPreviewMode] = useState(true);
  const [showMeasurements, setShowMeasurements] = useState(true);
  const [unit, setUnit] = useState<'mm'|'in'|'ft'|'yd'>('mm');
  const [projScale, setProjScale] = useState(1);
  const deleteActiveModel = () => {
    if (!activeModelId) return;
    const remaining = models.filter(m => m.id !== activeModelId);
    setModels(remaining);
    setActiveModelId(remaining.length > 0 ? remaining[0].id : null);
  };


  const [selectedPrinterPreset, setSelectedPrinterPreset] = useState(PRINTERS[0]);
  const [customDims, setCustomDims] = useState({ width: 300, depth: 300, height: 300 });

  const activePrinter = selectedPrinterPreset.name === 'Custom Printer...' 
    ? { ...selectedPrinterPreset, width: customDims.width, depth: customDims.depth, height: customDims.height } 
    : selectedPrinterPreset;

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const step = e.shiftKey ? 10 : 1;
      const rotStep = e.shiftKey ? 5 : 0.5;

      if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
        e.preventDefault();
      }

      switch(e.key) {
        case 'ArrowUp': setPanOffset((p: {x:number, z:number}) => ({ ...p, z: p.z - step })); break;
        case 'ArrowDown': setPanOffset((p: {x:number, z:number}) => ({ ...p, z: p.z + step })); break;
        case 'ArrowLeft': setPanOffset((p: {x:number, z:number}) => ({ ...p, x: p.x - step })); break;
        case 'ArrowRight': setPanOffset((p: {x:number, z:number}) => ({ ...p, x: p.x + step })); break;
        case '[': setFineRotationY((r: number) => r + THREE.MathUtils.degToRad(rotStep)); break;
        case ']': setFineRotationY((r: number) => r - THREE.MathUtils.degToRad(rotStep)); break;
        case 'c': 
        case 'C': 
           setPanOffset({ x: 0, z: 0 }); 
           setFineRotationY(0);
           break;
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || []);
    if (files.length === 0) return;

    const loader = new STLLoader();
    const newModels: any[] = [];

    for (const file of files) {
      try {
        const buffer = await file.arrayBuffer();
        const geo = loader.parse(buffer);
        
        geo.rotateX(-Math.PI / 2); // Convert to Y-up
        geo.computeBoundingBox();
        if (geo.boundingBox) {
          const center = new THREE.Vector3();
          geo.boundingBox.getCenter(center);
          // Only drop to floor, do not center X and Z automatically to preserve assembly spacing
          geo.translate(-center.x, -geo.boundingBox.min.y, -center.z);
        }

        newModels.push({
          id: Math.random().toString(36).substring(7),
          name: file.name,
          geometry: geo,
          scale: 1,
          panOffset: { x: 0, z: 0 },
          fineRotationY: 0,
          snapRotation: { x: 0, y: 0, z: 0 }
        });
      } catch (err) {
        console.error("Failed to parse", file.name, err);
      }
    }

    if (newModels.length === 0) return;

    setModels(prev => {
        const next = [...prev, ...newModels];
        if (!activeModelId) setActiveModelId(next[next.length - 1].id);
        return next;
    });
  };

  const rotateGeometry = (axis: 'x' | 'y' | 'z') => {
    if (!geometry) return;
    setSnapRotation((prev: {x:number, y:number, z:number}) => ({
      ...prev,
      [axis]: prev[axis as keyof typeof prev] + Math.PI / 2
    }));
  };

  const exportSTL = () => {
    if (models.length === 0) return;
    
    const geometriesToExport = models.map(m => {
        const exportGeo = m.geometry.clone();
        exportGeo.scale(m.scale, m.scale, m.scale);
        exportGeo.rotateX(m.snapRotation.x);
        exportGeo.rotateY(m.snapRotation.y);
        exportGeo.rotateZ(m.snapRotation.z);
        exportGeo.computeBoundingBox();
        if (exportGeo.boundingBox) {
          const center = new THREE.Vector3();
          exportGeo.boundingBox.getCenter(center);
          exportGeo.translate(-center.x, -exportGeo.boundingBox.min.y, -center.z);
        }
        exportGeo.rotateY(m.fineRotationY);
        exportGeo.translate(m.panOffset.x, 0, m.panOffset.z);
        exportGeo.rotateX(Math.PI / 2);
        return exportGeo;
    });

    let finalExportGeo = geometriesToExport[0];
    if (geometriesToExport.length > 1) {
        finalExportGeo = BufferGeometryUtils.mergeGeometries(geometriesToExport);
    }

    const exportMesh = new THREE.Mesh(finalExportGeo, new THREE.MeshBasicMaterial());
    const exporter = new STLExporter();
    const stlString = exporter.parse(exportMesh);
    
    const blob = new Blob([stlString], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.style.display = 'none';
    link.href = url;
    link.download = 'aligned_part.stl';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };
  const containerRef = useRef<HTMLDivElement>(null);

  const toggleFullscreen = () => {
    setIsPreviewMode(false); 
    setIsCalibrating(false);
    if (!document.fullscreenElement) {
      containerRef.current?.requestFullscreen().catch(err => {
        console.error(`Error attempting to enable fullscreen: ${err.message}`);
      });
    } else {
      document.exitFullscreen();
    }
  };

  return (
    <div className="min-h-screen bg-[#140b00] text-amber-500 font-sans flex flex-col h-screen overflow-hidden">
      {/* Header / Controls */}
      <div className="p-4 bg-[#2a1700] border-b border-[#4a2800] flex justify-between items-center z-10 shrink-0 shadow-sm">
        <div className="flex items-center gap-4">
          <h1 className="text-xl font-bold text-amber-400">Atlanta Transmutations</h1>
          <span className="text-sm hidden md:inline text-amber-700 font-medium">Metrology Hologram</span>
        </div>
        
        <div className="flex items-center gap-2 md:gap-4 overflow-x-auto">
          {geometry && (
            <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded border bg-[#1a0f00] border-[#4a2800]">
              <Scaling size={16} className="text-amber-600" />
              <span className="text-sm text-amber-600 font-medium">Part Scale:</span>
              <input 
                type="number" 
                step="0.1" 
                min="0.1"
                value={objectScale} 
                onChange={(e) => setObjectScale(Math.max(0.01, parseFloat(e.target.value) || 1))}
                className="bg-transparent text-sm w-16 focus:outline-none font-mono text-amber-400 font-bold" 
              />
            </div>
          )}

          <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded border bg-[#1a0f00] border-[#4a2800]">
            <Settings2 size={16} className="text-amber-600" />
            <select 
              className="bg-transparent text-sm focus:outline-none cursor-pointer text-amber-500 font-medium"
              value={selectedPrinterPreset.name}
              onChange={(e) => setSelectedPrinterPreset(PRINTERS.find(p => p.name === e.target.value) || PRINTERS[0])}
            >
              {PRINTERS.map(p => (
                <option key={p.name} value={p.name} className="bg-[#1a0f00]">{p.name}</option>
              ))}
            </select>
          </div>
          
          {selectedPrinterPreset.name === 'Custom Printer...' && (
            <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded border bg-[#1a0f00] border-[#4a2800]">
               <span className="text-xs text-amber-700 font-medium">XYZ (mm):</span>
               <input type="number" value={customDims.width} onChange={e => setCustomDims({...customDims, width: parseInt(e.target.value) || 10})} className="w-12 bg-transparent text-xs text-center border-b border-[#4a2800] focus:border-amber-500 focus:outline-none" />
               <input type="number" value={customDims.depth} onChange={e => setCustomDims({...customDims, depth: parseInt(e.target.value) || 10})} className="w-12 bg-transparent text-xs text-center border-b border-[#4a2800] focus:border-amber-500 focus:outline-none" />
               <input type="number" value={customDims.height} onChange={e => setCustomDims({...customDims, height: parseInt(e.target.value) || 10})} className="w-12 bg-transparent text-xs text-center border-b border-[#4a2800] focus:border-amber-500 focus:outline-none" />
            </div>
          )}

          {/* Tools Group */}
          <div className="flex items-center gap-1 border-r border-[#4a2800] pr-4">
            <button 
              onClick={() => setUnit(unit === 'mm' ? 'in' : 'mm')}
              className="px-3 py-2 rounded text-sm font-bold font-mono text-amber-600 hover:bg-[#3a2000] transition-colors"
              title="Toggle Units (mm / in)"
            >
              {unit}
            </button>
            <button 
              onClick={() => setShowMeasurements(!showMeasurements)}
              className={`p-2 rounded transition-colors ${showMeasurements ? 'bg-[#4a2800] text-amber-400' : 'text-amber-700 hover:bg-[#3a2000]'}`}
              title="Toggle Dimensions"
            >
              <Ruler size={16} />
            </button>
          </div>

          <label className="flex items-center gap-2 px-3 py-2 md:px-4 rounded cursor-pointer transition-colors text-sm font-medium whitespace-nowrap bg-amber-600 hover:bg-amber-500 text-black shadow-[0_0_15px_rgba(217,119,6,0.4)]">
            <Upload size={16} />
            <span className="hidden xl:inline">Upload STL</span>
            <input type="file" multiple accept=".stl" className="hidden" onChange={handleFileUpload} />
          </label>

          <button 
            onClick={exportSTL}
            disabled={!geometry}
            className={`flex items-center gap-2 px-3 py-2 md:px-4 rounded transition-colors text-sm font-medium whitespace-nowrap shadow-sm border ${!geometry ? 'bg-[#2a1700] text-[#4a2800] border-[#3a2000] cursor-not-allowed' : 'bg-[#1a0f00] text-amber-500 border-[#4a2800] hover:bg-[#2a1700]'}`}
            title="Download Aligned STL"
          >
            <Download size={16} />
            <span className="hidden xl:inline">Export STL</span>
          </button>
          
          <button 
            onClick={() => setIsPreviewMode(!isPreviewMode)}
            className={`flex items-center gap-2 px-3 py-2 md:px-4 rounded transition-colors text-sm font-medium whitespace-nowrap shadow-sm border ${isPreviewMode ? 'bg-[#4a2800] text-amber-400 border-amber-700' : 'bg-[#1a0f00] text-amber-600 border-[#4a2800] hover:bg-[#2a1700]'}`}
          >
            <Box size={16} />
            <span className="hidden xl:inline">3D Preview</span>
          </button>

          <button 
            onClick={() => { setIsCalibrating(!isCalibrating); setIsPreviewMode(false); }}
            className={`flex items-center gap-2 px-3 py-2 md:px-4 rounded transition-colors text-sm font-medium whitespace-nowrap shadow-sm border ${isCalibrating ? 'bg-amber-400 text-black border-amber-200' : 'bg-[#1a0f00] text-amber-600 border-[#4a2800] hover:bg-[#2a1700]'}`}
          >
            {isCalibrating ? <Grid size={16} /> : <Crosshair size={16} />}
            <span className="hidden xl:inline">{isCalibrating ? 'Exit Calibrate' : 'Calibrate Scale'}</span>
          </button>

          <button 
            onClick={toggleFullscreen}
            className="flex items-center gap-2 px-3 py-2 md:px-4 rounded transition-colors text-sm font-medium whitespace-nowrap bg-amber-500 hover:bg-amber-400 text-black shadow-sm"
          >
            <Maximize2 size={16} />
            <span className="hidden md:inline">Project Fullscreen</span>
          </button>
        </div>
      </div>

      {/* Main Projection Area */}
      <div 
        ref={containerRef} 
        className={`flex-1 relative flex items-center justify-center cursor-crosshair overflow-hidden ${isPreviewMode ? 'bg-[#0a0500]' : 'bg-black'}`}
      >
        {/* Floating Controls Toolbar */}
        {models.length > 0 && isPreviewMode && (
          <div className="absolute top-4 left-4 z-20 flex flex-col gap-2 p-4 w-56 rounded-xl border bg-[#1a0f00]/90 border-[#4a2800] backdrop-blur-md shadow-xl pointer-events-auto">
             <div className="text-xs font-bold tracking-wider uppercase text-amber-600">Active Part</div>
             <div className="flex gap-2 mb-2">
               <select value={activeModelId || ''} onChange={e => setActiveModelId(e.target.value)} className="flex-1 bg-[#0a0500] text-amber-500 border border-[#4a2800] rounded p-1 text-xs truncate">
                 {models.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
               </select>
               <button onClick={deleteActiveModel} className="px-2 bg-red-900/50 hover:bg-red-800 text-red-400 border border-red-900 rounded font-bold transition-colors" title="Delete Part">✕</button>
             </div>
             <div className="text-xs font-bold tracking-wider uppercase text-amber-600">Snap Rotate 90°</div>
             <div className="flex gap-2 mb-2">
               <button onClick={() => rotateGeometry('x')} className="flex-1 px-2 py-1.5 rounded-lg text-xs font-bold bg-[#2a1700] hover:bg-[#3a2000] text-amber-500 transition-colors border border-[#4a2800] shadow-sm">X</button>
               <button onClick={() => rotateGeometry('y')} className="flex-1 px-2 py-1.5 rounded-lg text-xs font-bold bg-[#2a1700] hover:bg-[#3a2000] text-amber-500 transition-colors border border-[#4a2800] shadow-sm">Y</button>
               <button onClick={() => rotateGeometry('z')} className="flex-1 px-2 py-1.5 rounded-lg text-xs font-bold bg-[#2a1700] hover:bg-[#3a2000] text-amber-500 transition-colors border border-[#4a2800] shadow-sm">Z</button>
             </div>
             
             <div className="flex justify-between items-end mt-2">
                <div className="text-xs font-bold tracking-wider uppercase text-amber-600">Fine Align Y</div>
                <div className="text-[10px] font-mono text-amber-400 font-bold bg-[#3a2000] px-1.5 py-0.5 rounded">{Math.round(THREE.MathUtils.radToDeg(fineRotationY))}°</div>
             </div>
             <input type="range" min="-180" max="180" value={THREE.MathUtils.radToDeg(fineRotationY)} onChange={e => setFineRotationY(THREE.MathUtils.degToRad(parseFloat(e.target.value)))} className="w-full accent-amber-500" />
             
             <div className="text-xs font-bold mt-4 tracking-wider uppercase text-amber-600">Calibration Pan</div>
             <div className="text-[10px] text-amber-700 leading-tight mb-3">Use <kbd className="bg-[#0a0500] px-1 py-0.5 rounded border border-[#4a2800] font-mono text-amber-500 shadow-sm">Arrow Keys</kbd> to nudge projection position.</div>
             
             <button onClick={() => { setPanOffset({x:0,z:0}); setFineRotationY(0); }} className="px-3 py-2 w-full rounded-lg text-sm font-bold bg-[#3a2000] text-amber-400 hover:bg-[#4a2800] transition-colors border border-[#5a3000] shadow-sm">
               Reset to Center
             </button>
          </div>
        )}
        
        {/* Fullscreen Hotkey Legend */}
        {!isPreviewMode && (
          <div className="absolute bottom-6 left-6 z-20 pointer-events-none opacity-50">
             <div className="font-mono text-xs px-3 py-2 rounded bg-[#0a0500]/80 text-amber-700 border border-[#4a2800]">
               <span className="font-bold text-amber-500">[Arrows]</span> Pan &nbsp;|&nbsp; <span className="font-bold text-amber-500">[ and ]</span> Rotate &nbsp;|&nbsp; <span className="font-bold text-amber-500">[C]</span> Center
             </div>
          </div>
        )}

        {isCalibrating && !isPreviewMode && (
          <div className="absolute inset-0 pointer-events-none z-20 flex flex-col items-center justify-center">
             <div className="relative mt-4 px-6 py-4 rounded-xl font-mono text-sm text-center bg-[#140b00]/90 text-amber-500 border border-amber-600/50 backdrop-blur-md shadow-2xl pointer-events-auto">
               <button 
                 onClick={() => setIsCalibrating(false)} 
                 className="absolute top-2 right-2 text-amber-600 hover:text-amber-400 font-sans font-bold px-2 py-1"
                 title="Close Calibration"
               >✕</button>
               <div className="font-bold text-amber-400 mb-1 pr-6">Scale Calibration Mode</div>
               Measure the physical projection on the build plate.<br/>
               Adjust scale until the digital grid matches the real printer edges.
               <div className="mt-4 flex items-center gap-3 bg-[#0a0500] p-3 rounded-lg border border-[#4a2800]">
                 <input 
                   type="range" min="0.1" max="10" step="0.001" 
                   value={projScale} 
                   onChange={e => setProjScale(parseFloat(e.target.value))} 
                   className="flex-1 accent-amber-500"
                 />
                 <span className="font-bold text-amber-300 bg-[#2a1700] px-2 py-1 rounded border border-[#4a2800]">{projScale.toFixed(3)}x</span>
               </div>
             </div>
          </div>
        )}

        {/* 3D Canvas */}
        <div className="absolute inset-0 z-0">
          <Canvas>
            {isPreviewMode ? (
              <>
                <PerspectiveCamera makeDefault position={[0, activePrinter.height * 0.8, activePrinter.depth * 1.5]} fov={50} far={200000} near={1} />
                <OrbitControls target={[0, activePrinter.height / 3, 0]} maxPolarAngle={Math.PI / 2} />
                <ambientLight intensity={2.5} />
                <pointLight position={[0, activePrinter.height, 0]} intensity={2} color="#ffffff" />
                <directionalLight position={[100, 200, 100]} intensity={1} color="#ffffff" />
              </>
            ) : (
              <>
                <OrthographicCamera makeDefault position={[0, 200, 0]} rotation={[-Math.PI/2, 0, 0]} zoom={3 * projScale} near={0.1} far={1000} />
                <ambientLight intensity={1} />
              </>
            )}
            
            <Suspense fallback={null}>
              <group>
                <VirtualPrinter width={activePrinter.width} depth={activePrinter.depth} height={activePrinter.height} style={activePrinter.style} isPreviewMode={isPreviewMode} isCalibrating={isCalibrating} showMeasurements={showMeasurements} unit={unit} />
                <group position={[panOffset.x, 0, panOffset.z]} rotation={[0, fineRotationY, 0]}>
                  
                    <ModelRenderer geometry={geometry} scale={objectScale} snapRotation={snapRotation} showMeasurements={showMeasurements} unit={unit} isPreviewMode={isPreviewMode} />
                  
                </group>
              </group>
            </Suspense>
          </Canvas>
        </div>

        {models.length === 0 && isPreviewMode && (
          <div className="absolute z-10 text-gray-500 font-mono text-sm border-2 border-gray-300 p-8 rounded-xl border-dashed bg-white/50 backdrop-blur-sm pointer-events-none shadow-sm">
            Upload an STL to preview inside the <span className="font-bold text-gray-700">{activePrinter.name}</span>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
