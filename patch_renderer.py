import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

# Fix the ModelRenderer JSX
broken_renderer = """  return (
    <group rotation={[snapRotation.x, snapRotation.y, snapRotation.z]}>
      <mesh geometry={geometry} scale={[scale, scale, scale]}>
        <meshBasicMaterial color={baseColor} wireframe={false} transparent opacity={0.4} blending={THREE.AdditiveBlending} depthWrite={false} />
        <lineSegments>
          <edgesGeometry args={[geometry, 15]} />
          <lineBasicMaterial color={edgeColor} linewidth={2} transparent opacity={0.8} blending={THREE.AdditiveBlending} depthWrite={false} />
        </lineSegments>
      </mesh>
    </group>

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
  );"""

fixed_renderer = """  return (
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
  );"""

content = content.replace(broken_renderer, fixed_renderer)

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
