import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

# 1. Update VirtualPrinter signature
old_sig = "const VirtualPrinter = ({ width, depth, height, style, isPreviewMode, isCalibrating }: { width: number, depth: number, height: number, style: string, isPreviewMode: boolean, isCalibrating: boolean }) => {"
new_sig = "const VirtualPrinter = ({ width, depth, height, style, isPreviewMode, isCalibrating, showMeasurements = false, unit = 'mm' }: { width: number, depth: number, height: number, style: string, isPreviewMode: boolean, isCalibrating: boolean, showMeasurements?: boolean, unit?: 'mm'|'in' }) => {"
content = content.replace(old_sig, new_sig)

# 2. Add Environment Labels to VirtualPrinter
old_build_plate = """  const BuildPlate = () => {
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

new_build_plate = """  const BuildPlate = () => {
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
        <mesh rotation={[-Math.PI/2, 0, 0]} position={[0, 0.1, 0]}>
          <planeGeometry args={[width, depth]} />
          <meshBasicMaterial color="#ffaa00" transparent opacity={0.05} />
        </mesh>

        {showMeasurements && (
          <group>
            {/* Width Marker (X-axis, front edge) */}
            <Html position={[0, 0, depth/2 + (style==='hangar'?500:20)]} center style={{ pointerEvents: 'none' }}>
              <div className="px-2 py-1 rounded text-[10px] font-mono whitespace-nowrap opacity-60 bg-black text-[#8a5d00] border border-[#4a2800]">
                Width: {format(width)}
              </div>
            </Html>
            {/* Depth Marker (Z-axis, side edge) */}
            <Html position={[width/2 + (style==='hangar'?500:20), 0, 0]} center style={{ pointerEvents: 'none' }}>
              <div className="px-2 py-1 rounded text-[10px] font-mono whitespace-nowrap opacity-60 bg-black text-[#8a5d00] border border-[#4a2800]">
                Depth: {format(depth)}
              </div>
            </Html>
            {/* Height Marker (Y-axis, standing off to the side) */}
            <Html position={[-width/2 - (style==='hangar'?500:20), height/2, 0]} center style={{ pointerEvents: 'none' }}>
              <div className="px-2 py-1 rounded text-[10px] font-mono whitespace-nowrap opacity-60 bg-black text-[#8a5d00] border border-[#4a2800]">
                Height: {format(height)}
              </div>
            </Html>
          </group>
        )}
      </group>
    );
  };"""
content = content.replace(old_build_plate, new_build_plate)

# 3. Pass showMeasurements and unit to VirtualPrinter from App
old_virtual_printer_usage = """<VirtualPrinter 
                  width={activePrinter.width} 
                  depth={activePrinter.depth} 
                  height={activePrinter.height} 
                  style={activePrinter.style} 
                  isPreviewMode={isPreviewMode}
                  isCalibrating={isCalibrating}
                />"""

new_virtual_printer_usage = """<VirtualPrinter 
                  width={activePrinter.width} 
                  depth={activePrinter.depth} 
                  height={activePrinter.height} 
                  style={activePrinter.style} 
                  isPreviewMode={isPreviewMode}
                  isCalibrating={isCalibrating}
                  showMeasurements={showMeasurements}
                  unit={unit}
                />"""
content = content.replace(old_virtual_printer_usage, new_virtual_printer_usage)

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
