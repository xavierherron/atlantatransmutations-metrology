import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

# 1. Add Center to drei imports
content = re.sub(
    r"import \{ OrthographicCamera, PerspectiveCamera, OrbitControls, Html \} from '@react-three/drei';",
    "import { OrthographicCamera, PerspectiveCamera, OrbitControls, Html, Center } from '@react-three/drei';",
    content
)

# 2. Update ModelRenderer props and size calculation
model_renderer_old = """const ModelRenderer = ({ geometry, scale = 1, showMeasurements = false, unit = 'mm', isPreviewMode = true }: { geometry: THREE.BufferGeometry | null, scale?: number, showMeasurements?: boolean, unit?: 'mm' | 'in', isPreviewMode?: boolean }) => {
  if (!geometry) return null;
  
  const baseColor = "#ffaa00";
  const edgeColor = "#ffff00";

  const size = new THREE.Vector3();
  if (geometry.boundingBox) {
    geometry.boundingBox.getSize(size);
    size.multiplyScalar(scale);
  }

  const format = (val: number) => (unit === 'in' ? val / 25.4 : val).toFixed(2);

  return (
    <mesh geometry={geometry} scale={[scale, scale, scale]}>
      <meshBasicMaterial color={baseColor} wireframe={false} transparent opacity={0.4} blending={THREE.AdditiveBlending} depthWrite={false} />
      <lineSegments>
        <edgesGeometry args={[geometry, 15]} />
        <lineBasicMaterial color={edgeColor} linewidth={2} transparent opacity={0.8} blending={THREE.AdditiveBlending} depthWrite={false} />
      </lineSegments>"""

model_renderer_new = """const ModelRenderer = ({ geometry, scale = 1, snapRotation = {x:0, y:0, z:0}, showMeasurements = false, unit = 'mm', isPreviewMode = true }: { geometry: THREE.BufferGeometry | null, scale?: number, snapRotation?: {x:number, y:number, z:number}, showMeasurements?: boolean, unit?: 'mm' | 'in', isPreviewMode?: boolean }) => {
  if (!geometry) return null;
  
  const baseColor = "#ffaa00";
  const edgeColor = "#ffff00";

  const size = new THREE.Vector3();
  if (geometry.boundingBox) {
    const dummy = new THREE.Mesh(geometry);
    dummy.rotation.set(snapRotation.x, snapRotation.y, snapRotation.z);
    dummy.scale.set(scale, scale, scale);
    dummy.updateMatrixWorld(true);
    const box = new THREE.Box3().setFromObject(dummy);
    box.getSize(size);
  }

  const format = (val: number) => (unit === 'in' ? val / 25.4 : val).toFixed(2);

  return (
    <group rotation={[snapRotation.x, snapRotation.y, snapRotation.z]}>
      <mesh geometry={geometry} scale={[scale, scale, scale]}>
        <meshBasicMaterial color={baseColor} wireframe={false} transparent opacity={0.4} blending={THREE.AdditiveBlending} depthWrite={false} />
        <lineSegments>
          <edgesGeometry args={[geometry, 15]} />
          <lineBasicMaterial color={edgeColor} linewidth={2} transparent opacity={0.8} blending={THREE.AdditiveBlending} depthWrite={false} />
        </lineSegments>
      </mesh>
    </group>"""

content = content.replace(model_renderer_old, model_renderer_new)

# 3. Update App state
content = content.replace(
    "const [, setRenderTick] = useState(0);",
    "const [snapRotation, setSnapRotation] = useState({x: 0, y: 0, z: 0});"
)

# 4. Update rotateGeometry
rotate_geom_old = """  const rotateGeometry = (axis: 'x' | 'y' | 'z') => {
    if (!geometry) return;
    
    // Mutate in-place to avoid freezing the browser on massive STLs
    if (axis === 'x') geometry.rotateX(Math.PI / 2);
    if (axis === 'y') geometry.rotateY(Math.PI / 2);
    if (axis === 'z') geometry.rotateZ(Math.PI / 2);
    
    geometry.computeBoundingBox();
    if (geometry.boundingBox) {
      const center = new THREE.Vector3();
      geometry.boundingBox.getCenter(center);
      geometry.translate(-center.x, -geometry.boundingBox.min.y, -center.z);
    }
    
    // Tell Three.js the vertices changed
    geometry.attributes.position.needsUpdate = true;
    if (geometry.attributes.normal) {
      geometry.computeVertexNormals();
      geometry.attributes.normal.needsUpdate = true;
    }
    
    // Force React to re-render the overlay annotations
    setRenderTick(t => t + 1);
  };"""

rotate_geom_new = """  const rotateGeometry = (axis: 'x' | 'y' | 'z') => {
    if (!geometry) return;
    setSnapRotation(prev => ({
      ...prev,
      [axis]: prev[axis as keyof typeof prev] + Math.PI / 2
    }));
  };"""

content = content.replace(rotate_geom_old, rotate_geom_new)

# 5. Update exportSTL to use snapRotation
export_stl_old = """    // Apply transformations in the exact order they are rendered
    exportGeo.scale(objectScale, objectScale, objectScale);
    exportGeo.rotateY(fineRotationY);
    exportGeo.translate(panOffset.x, 0, panOffset.z);
    
    // Convert back from ThreeJS Y-up space to standard STL Z-up space
    exportGeo.rotateX(Math.PI / 2);"""

export_stl_new = """    // Apply transformations in the exact order they are rendered
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
    exportGeo.rotateX(Math.PI / 2);"""

content = content.replace(export_stl_old, export_stl_new)

# 6. Wrap ModelRenderer in <Center> inside Canvas
canvas_old = """                <group position={[panOffset.x, 0, panOffset.z]} rotation={[0, fineRotationY, 0]}>
                  <ModelRenderer geometry={geometry} scale={objectScale} showMeasurements={showMeasurements} unit={unit} isPreviewMode={isPreviewMode} />
                </group>"""

canvas_new = """                <group position={[panOffset.x, 0, panOffset.z]} rotation={[0, fineRotationY, 0]}>
                  <Center bottom center>
                    <ModelRenderer geometry={geometry} scale={objectScale} snapRotation={snapRotation} showMeasurements={showMeasurements} unit={unit} isPreviewMode={isPreviewMode} />
                  </Center>
                </group>"""

content = content.replace(canvas_old, canvas_new)

# 7. Add reset logic for snapRotation when uploading new STL
upload_old = """        const newGeo = event.target.result as THREE.BufferGeometry;
        newGeo.rotateX(-Math.PI / 2); // Convert to Y-up immediately
        newGeo.computeBoundingBox();
        if (newGeo.boundingBox) {
          const center = new THREE.Vector3();
          newGeo.boundingBox.getCenter(center);
          newGeo.translate(-center.x, -newGeo.boundingBox.min.y, -center.z);
        }
        setGeometry(newGeo);
        setObjectScale(1);
        setPanOffset({ x: 0, z: 0 });
        setFineRotationY(0);"""

upload_new = """        const newGeo = event.target.result as THREE.BufferGeometry;
        newGeo.rotateX(-Math.PI / 2); // Convert to Y-up immediately
        newGeo.computeBoundingBox();
        if (newGeo.boundingBox) {
          const center = new THREE.Vector3();
          newGeo.boundingBox.getCenter(center);
          newGeo.translate(-center.x, -newGeo.boundingBox.min.y, -center.z);
        }
        setGeometry(newGeo);
        setObjectScale(1);
        setPanOffset({ x: 0, z: 0 });
        setFineRotationY(0);
        setSnapRotation({x: 0, y: 0, z: 0});"""

content = content.replace(upload_old, upload_new)

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
