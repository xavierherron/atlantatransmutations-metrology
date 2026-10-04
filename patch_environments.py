import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

# 1. Update PRINTERS array
old_printers = """const PRINTERS = [
  { name: 'Flashforge Creator 5 Pro', width: 256, depth: 256, height: 300, style: 'enclosed' },
  { name: 'Bambu Lab X1 / P1S', width: 256, depth: 256, height: 256, style: 'enclosed' },
  { name: 'Creality Ender 3', width: 220, depth: 220, height: 250, style: 'i3' },
  { name: 'Prusa MK3S+ / MK4', width: 250, depth: 210, height: 220, style: 'i3' },
  { name: 'Voron 2.4 (350mm)', width: 350, depth: 350, height: 350, style: 'corexy' },
  { name: 'Elegoo Neptune 3 Max', width: 420, depth: 420, height: 500, style: 'i3' },
  { name: 'Custom Printer...', width: 300, depth: 300, height: 300, style: 'enclosed' }
];"""

new_printers = """const PRINTERS = [
  { name: 'Flashforge Creator 5 Pro', width: 256, depth: 256, height: 300, style: 'enclosed' },
  { name: 'Bambu Lab X1 / P1S', width: 256, depth: 256, height: 256, style: 'enclosed' },
  { name: 'Creality Ender 3', width: 220, depth: 220, height: 250, style: 'i3' },
  { name: 'Prusa MK3S+ / MK4', width: 250, depth: 210, height: 220, style: 'i3' },
  { name: 'Voron 2.4 (350mm)', width: 350, depth: 350, height: 350, style: 'corexy' },
  { name: 'Elegoo Neptune 3 Max', width: 420, depth: 420, height: 500, style: 'i3' },
  { name: 'Auto Garage (1-Car)', width: 3500, depth: 6000, height: 2500, style: 'garage' },
  { name: 'Airport Hangar', width: 30000, depth: 30000, height: 15000, style: 'hangar' },
  { name: 'Custom Printer...', width: 300, depth: 300, height: 300, style: 'enclosed' }
];"""

content = content.replace(old_printers, new_printers)

# 2. Update VirtualPrinter BuildPlate grid
old_build_plate = """  const BuildPlate = () => (
    <group position={[0, 0, 0]}>
      <mesh position={[0, -3.5, 0]}>
        <boxGeometry args={[width + 4, 5, depth + 4]} />
        <meshStandardMaterial color="#3a2000" metalness={0.5} roughness={0.8} />
      </mesh>
      <mesh position={[0, -0.5, 0]}>
        <boxGeometry args={[width, 1, depth]} />
        <meshStandardMaterial color="#1a0f00" metalness={0.2} roughness={0.8} />
      </mesh>
      <gridHelper args={[Math.max(width, depth), Math.max(width, depth) / 10, '#4a2800', '#2a1700']} position={[0, 0.05, 0]} />
      <mesh rotation={[-Math.PI/2, 0, 0]} position={[0, 0.1, 0]}>
        <planeGeometry args={[width, depth]} />
        <meshBasicMaterial color="#ffaa00" transparent opacity={0.05} />
      </mesh>
    </group>
  );"""

new_build_plate = """  const BuildPlate = () => {
    let gridDivisions = Math.max(width, depth) / 10;
    if (style === 'garage') gridDivisions = Math.max(width, depth) / 100; // 100mm grid for garage
    if (style === 'hangar') gridDivisions = Math.max(width, depth) / 1000; // 1000mm grid for hangar
    
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
        <mesh rotation={[-Math.PI/2, 0, 0]} position={[0, 0.1, 0]}>
          <planeGeometry args={[width, depth]} />
          <meshBasicMaterial color="#ffaa00" transparent opacity={0.05} />
        </mesh>
      </group>
    );
  };"""

content = content.replace(old_build_plate, new_build_plate)

# 3. Add styles to VirtualPrinter
old_if_i3 = "  if (style === 'i3') {"
new_styles = """  if (style === 'garage') {
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
        <mesh position={[0, height/2, 0]} rotation={[0, 0, 0]}>
          <cylinderGeometry args={[width/2, width/2, depth, 32, 1, false, 0, Math.PI]} />
          <meshStandardMaterial color="#111" side={THREE.DoubleSide} />
        </mesh>
        <LightCone headY={height} />
      </group>
    );
  }

  if (style === 'i3') {"""

content = content.replace(old_if_i3, new_styles)

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
