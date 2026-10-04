import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

old_block = """                <group position={[panOffset.x, 0, panOffset.z]} rotation={[0, fineRotationY, 0]}>
                  
                    <ModelRenderer geometry={geometry} scale={objectScale} snapRotation={snapRotation} showMeasurements={showMeasurements} unit={unit} isPreviewMode={isPreviewMode} />
                  
                </group>"""

new_block = """                {models.map(m => (
                  <group key={m.id} position={[m.panOffset.x, 0, m.panOffset.z]} rotation={[0, m.fineRotationY, 0]}>
                    <ModelRenderer geometry={m.geometry} scale={m.scale} snapRotation={m.snapRotation} showMeasurements={showMeasurements && activeModelId === m.id} unit={unit} isPreviewMode={isPreviewMode} />
                  </group>
                ))}"""

content = content.replace(old_block, new_block)

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
