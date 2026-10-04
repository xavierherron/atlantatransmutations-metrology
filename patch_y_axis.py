import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

# 1. Update initial panOffset
content = content.replace("panOffset: { x: 0, z: 0 }", "panOffset: { x: 0, y: 0, z: 0 }")

# 2. Update handleKeyDown
old_keydown = """      switch(e.key) {
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
      }"""

new_keydown = """      switch(e.key) {
        case 'ArrowUp': setPanOffset((p: {x:number, y:number, z:number}) => ({ ...p, z: p.z - step })); break;
        case 'ArrowDown': setPanOffset((p: {x:number, y:number, z:number}) => ({ ...p, z: p.z + step })); break;
        case 'ArrowLeft': setPanOffset((p: {x:number, y:number, z:number}) => ({ ...p, x: p.x - step })); break;
        case 'ArrowRight': setPanOffset((p: {x:number, y:number, z:number}) => ({ ...p, x: p.x + step })); break;
        case 'w':
        case 'W': setPanOffset((p: {x:number, y:number, z:number}) => ({ ...p, y: p.y + step })); break;
        case 's':
        case 'S': setPanOffset((p: {x:number, y:number, z:number}) => ({ ...p, y: p.y - step })); break;
        case '[': setFineRotationY((r: number) => r + THREE.MathUtils.degToRad(rotStep)); break;
        case ']': setFineRotationY((r: number) => r - THREE.MathUtils.degToRad(rotStep)); break;
        case 'c': 
        case 'C': 
           setPanOffset({ x: 0, y: 0, z: 0 }); 
           setFineRotationY(0);
           break;
      }"""

content = content.replace(old_keydown, new_keydown)

# 3. Update export translation
content = content.replace("exportGeo.translate(m.panOffset.x, 0, m.panOffset.z);", "exportGeo.translate(m.panOffset.x, m.panOffset.y, m.panOffset.z);")

# 4. Update canvas mapping
old_canvas = "position={[m.panOffset.x, 0, m.panOffset.z]}"
new_canvas = "position={[m.panOffset.x, m.panOffset.y, m.panOffset.z]}"
content = content.replace(old_canvas, new_canvas)

# 5. Update UI text
old_ui_text = """<div className="text-[10px] text-amber-700 leading-tight mb-3">Use <kbd className="bg-[#0a0500] px-1 py-0.5 rounded border border-[#4a2800] font-mono text-amber-500 shadow-sm">Arrow Keys</kbd> to nudge projection position.</div>"""
new_ui_text = """<div className="text-[10px] text-amber-700 leading-tight mb-3">Use <kbd className="bg-[#0a0500] px-1 py-0.5 rounded border border-[#4a2800] font-mono text-amber-500 shadow-sm">Arrows (X/Z)</kbd> and <kbd className="bg-[#0a0500] px-1 py-0.5 rounded border border-[#4a2800] font-mono text-amber-500 shadow-sm">W/S (Y)</kbd> to nudge projection position.</div>"""
content = content.replace(old_ui_text, new_ui_text)

# 6. Update Reset button UI
old_reset = "setPanOffset({x:0,z:0});"
new_reset = "setPanOffset({x:0,y:0,z:0});"
content = content.replace(old_reset, new_reset)


with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
