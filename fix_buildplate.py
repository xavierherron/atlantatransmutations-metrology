import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

# Replace BuildPlate completely
content = re.sub(
    r'  const BuildPlate = \(\) => \(.*?\);\n',
    """  const BuildPlate = () => {
    let gridDivisions = Math.max(width, depth) / 10;
    if (style === 'garage') gridDivisions = Math.max(width, depth) / 100; // 100mm grid for garage
    if (style === 'hangar') gridDivisions = Math.max(width, depth) / 1000; // 1000mm grid for hangar
    
    const format = (val: number) => {
        if (val >= 1000 && unit === 'mm') return (val / 1000).toFixed(1) + ' m';
        return (unit === 'in' ? val / 25.4 : val).toFixed(1) + ' ' + unit;
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
""",
    content,
    flags=re.DOTALL
)

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
