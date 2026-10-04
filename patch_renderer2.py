import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

renderer_regex = r"const ModelRenderer = \(\{ geometry.*?(?=};\n\nconst VirtualPrinter)قات"
# wait, let me just replace by string

old_renderer = """const ModelRenderer = ({ geometry, scale = 1, snapRotation = {x:0, y:0, z:0}, showMeasurements = false, unit = 'mm', isPreviewMode = true }: { geometry: THREE.BufferGeometry | null, scale?: number, snapRotation?: {x:number, y:number, z:number}, showMeasurements?: boolean, unit?: 'mm' | 'in', isPreviewMode?: boolean }) => {
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

        {/* Measurement Overlays */}
        {showMeasurements && size.length() > 0 && (
          <group scale={[1/scale, 1/scale, 1/scale]}>
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
      </mesh>
    </group>
  );
};"""

new_renderer = """const ModelRenderer = ({ geometry, scale = 1, snapRotation = {x:0, y:0, z:0}, showMeasurements = false, unit = 'mm', isPreviewMode = true }: { geometry: THREE.BufferGeometry | null, scale?: number, snapRotation?: {x:number, y:number, z:number}, showMeasurements?: boolean, unit?: 'mm' | 'in', isPreviewMode?: boolean }) => {
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

  const format = (val: number) => (unit === 'in' ? val / 25.4 : val).toFixed(2);

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
};"""

content = content.replace(old_renderer, new_renderer)

# Also remove `<Center bottom>` wrapping from App.tsx Canvas
content = content.replace("<Center bottom>", "")
content = content.replace("</Center>", "")

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
