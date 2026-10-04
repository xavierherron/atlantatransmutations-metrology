import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

# Fix the Hangar arch roof orientation
old_hangar_roof = """        {/* Arch Roof */}
        <mesh position={[0, height/2, 0]} rotation={[0, 0, 0]}>
          <cylinderGeometry args={[width/2, width/2, depth, 32, 1, false, 0, Math.PI]} />
          <meshStandardMaterial color="#111" side={THREE.DoubleSide} />
        </mesh>"""

new_hangar_roof = """        {/* Arch Roof */}
        <mesh position={[0, height, 0]} rotation={[Math.PI/2, Math.PI/2, 0]}>
          <cylinderGeometry args={[width/2, width/2, depth, 32, 1, true, 0, Math.PI]} />
          <meshStandardMaterial color="#111" side={THREE.DoubleSide} />
        </mesh>"""

content = content.replace(old_hangar_roof, new_hangar_roof)

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
