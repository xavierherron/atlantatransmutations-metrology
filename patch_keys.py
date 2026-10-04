with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

old_keys = """      switch(e.key) {
        case 'ArrowUp': setPanOffset(p => ({ ...p, z: p.z - step })); break;
        case 'ArrowDown': setPanOffset(p => ({ ...p, z: p.z + step })); break;
        case 'ArrowLeft': setPanOffset(p => ({ ...p, x: p.x - step })); break;
        case 'ArrowRight': setPanOffset(p => ({ ...p, x: p.x + step })); break;
        case '[': setFineRotationY(r => r + THREE.MathUtils.degToRad(rotStep)); break;
        case ']': setFineRotationY(r => r - THREE.MathUtils.degToRad(rotStep)); break;
        case 'c': 
        case 'C': 
           setPanOffset({ x: 0, z: 0 }); 
           setFineRotationY(0);
           break;
      }"""

new_keys = """      if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
        e.preventDefault();
      }

      switch(e.key) {
        case 'ArrowUp': setPanOffset(p => ({ ...p, z: p.z - step })); break;
        case 'ArrowDown': setPanOffset(p => ({ ...p, z: p.z + step })); break;
        case 'ArrowLeft': setPanOffset(p => ({ ...p, x: p.x - step })); break;
        case 'ArrowRight': setPanOffset(p => ({ ...p, x: p.x + step })); break;
        case '[': setFineRotationY(r => r + THREE.MathUtils.degToRad(rotStep)); break;
        case ']': setFineRotationY(r => r - THREE.MathUtils.degToRad(rotStep)); break;
        case 'c': 
        case 'C': 
           setPanOffset({ x: 0, z: 0 }); 
           setFineRotationY(0);
           break;
      }"""

content = content.replace(old_keys, new_keys)

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
