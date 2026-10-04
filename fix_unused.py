import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace("  const panOffset = activeModel?.panOffset || { x: 0, z: 0 };\n", "")
content = content.replace("  const snapRotation = activeModel?.snapRotation || { x: 0, y: 0, z: 0 };\n", "")

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
