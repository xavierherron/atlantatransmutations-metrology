with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

# Fix PerspectiveCamera
old_cam = "<PerspectiveCamera makeDefault position={[0, activePrinter.height * 0.8, activePrinter.depth * 1.5]} fov={50} />"
new_cam = "<PerspectiveCamera makeDefault position={[0, activePrinter.height * 0.8, activePrinter.depth * 1.5]} fov={50} far={200000} near={1} />"

content = content.replace(old_cam, new_cam)

# Also fix the point light and ambient light to reach further, or add a hemisphere light.
# If activePrinter is massive, a point light at [0, activePrinter.height, 0] with default distance/decay will be too dim!
# We can just use an intense DirectionalLight for the massive environments
# Actually, the ambientLight handles the baseline.
old_light = "<ambientLight intensity={1.5} />"
new_light = "<ambientLight intensity={2.5} />"
content = content.replace(old_light, new_light)

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
