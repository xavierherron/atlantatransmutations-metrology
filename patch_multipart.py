import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

# 1. State changes
state_old = """  const [geometry, setGeometry] = useState<THREE.BufferGeometry | null>(null);
  const [snapRotation, setSnapRotation] = useState({x: 0, y: 0, z: 0});
  const [isCalibrating, setIsCalibrating] = useState(false);
  const [isPreviewMode, setIsPreviewMode] = useState(true);
  const [showMeasurements, setShowMeasurements] = useState(true);
  const [unit, setUnit] = useState<'mm'|'in'>('mm');
  const [projScale, setProjScale] = useState(1);
  const [objectScale, setObjectScale] = useState(1);
  
  const [panOffset, setPanOffset] = useState({ x: 0, z: 0 });
  const [fineRotationY, setFineRotationY] = useState(0);"""

state_new = """  const [models, setModels] = useState<any[]>([]);
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
  const [unit, setUnit] = useState<'mm'|'in'>('mm');
  const [projScale, setProjScale] = useState(1);"""

content = content.replace(state_old, state_new)

# 2. handleFileUpload
upload_old = """  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || []);
    if (files.length === 0) return;

    const loader = new STLLoader();
    const geometries: THREE.BufferGeometry[] = [];

    for (const file of files) {
      try {
        const buffer = await file.arrayBuffer();
        const geo = loader.parse(buffer);
        geometries.push(geo);
      } catch (err) {
        console.error("Failed to parse", file.name, err);
        alert(`Failed to parse ${file.name}. Ensure it's a valid STL.`);
      }
    }

    if (geometries.length === 0) return;

    // Merge all geometries into a single assembly to preserve relative positions
    let finalGeo = geometries[0];
    if (geometries.length > 1) {
      finalGeo = BufferGeometryUtils.mergeGeometries(geometries);
    }

    finalGeo.rotateX(-Math.PI / 2); // Convert to Y-up
    
    finalGeo.computeBoundingBox();
    if (finalGeo.boundingBox) {
      const center = new THREE.Vector3();
      finalGeo.boundingBox.getCenter(center);
      finalGeo.translate(-center.x, -finalGeo.boundingBox.min.y, -center.z);
    }
    
    setGeometry(finalGeo);
    setObjectScale(1); 
    setPanOffset({ x: 0, z: 0 });
    setFineRotationY(0);
    setSnapRotation({x: 0, y: 0, z: 0});
  };"""

upload_new = """  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
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
  };"""

content = content.replace(upload_old, upload_new)

# 3. Canvas rendering
canvas_old = """                <group position={[panOffset.x, 0, panOffset.z]} rotation={[0, fineRotationY, 0]}>
                  <ModelRenderer geometry={geometry} scale={objectScale} snapRotation={snapRotation} showMeasurements={showMeasurements} unit={unit} isPreviewMode={isPreviewMode} />
                </group>"""

canvas_new = """                {models.map(m => (
                  <group key={m.id} position={[m.panOffset.x, 0, m.panOffset.z]} rotation={[0, m.fineRotationY, 0]}>
                    <ModelRenderer geometry={m.geometry} scale={m.scale} snapRotation={m.snapRotation} showMeasurements={showMeasurements && activeModelId === m.id} unit={unit} isPreviewMode={isPreviewMode} />
                  </group>
                ))}"""

content = content.replace(canvas_old, canvas_new)

# 4. Sidebar active part selection
sidebar_old = """        {geometry && isPreviewMode && (
          <div className="absolute top-24 left-6 w-56 z-10 bg-[#140b00]/95 backdrop-blur-md border border-[#4a2800] rounded-xl p-4 shadow-2xl flex flex-col gap-3 pointer-events-auto">
             <div className="text-xs font-bold tracking-wider uppercase text-amber-600">Snap Rotate 90°</div>"""

sidebar_new = """        {models.length > 0 && isPreviewMode && (
          <div className="absolute top-24 left-6 w-56 z-10 bg-[#140b00]/95 backdrop-blur-md border border-[#4a2800] rounded-xl p-4 shadow-2xl flex flex-col gap-3 pointer-events-auto">
             <div className="text-xs font-bold tracking-wider uppercase text-amber-600">Active Part</div>
             <select value={activeModelId || ''} onChange={e => setActiveModelId(e.target.value)} className="w-full bg-[#0a0500] text-amber-500 border border-[#4a2800] rounded p-1 mb-2 text-xs">
               {models.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
             </select>
             <div className="text-xs font-bold tracking-wider uppercase text-amber-600">Snap Rotate 90°</div>"""

content = content.replace(sidebar_old, sidebar_new)

# 5. exportSTL
export_old = """  const exportSTL = () => {
    if (!geometry) return;
    const exportGeo = geometry.clone();
    
    // Apply transformations in the exact order they are rendered
    exportGeo.scale(objectScale, objectScale, objectScale);
    
    exportGeo.rotateX(snapRotation.x);
    exportGeo.rotateY(snapRotation.y);
    exportGeo.rotateZ(snapRotation.z);
    
    exportGeo.computeBoundingBox();
    if (exportGeo.boundingBox) {
      const center = new THREE.Vector3();
      exportGeo.boundingBox.getCenter(center);
      exportGeo.translate(-center.x, -exportGeo.boundingBox.min.y, -center.z);
    }
    
    exportGeo.rotateY(fineRotationY);
    exportGeo.translate(panOffset.x, 0, panOffset.z);
    
    // Convert back from ThreeJS Y-up space to standard STL Z-up space
    exportGeo.rotateX(Math.PI / 2);

    const exporter = new STLExporter();
    const mesh = new THREE.Mesh(exportGeo, new THREE.MeshBasicMaterial());
    const result = exporter.parse(mesh, { binary: true });
    
    const blob = new Blob([result], { type: 'application/octet-stream' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'aligned_projection.stl';
    link.click();
    URL.revokeObjectURL(url);
  };"""

export_new = """  const exportSTL = () => {
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

    const exporter = new STLExporter();
    const mesh = new THREE.Mesh(finalExportGeo, new THREE.MeshBasicMaterial());
    const result = exporter.parse(mesh, { binary: true });
    
    const blob = new Blob([result], { type: 'application/octet-stream' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'aligned_projection.stl';
    link.click();
    URL.revokeObjectURL(url);
  };"""

content = content.replace(export_old, export_new)

# 6. Additional !geometry checks
content = content.replace("{!geometry && isPreviewMode", "{models.length === 0 && isPreviewMode")

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
