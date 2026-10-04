import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

# Replace the Canvas rendering
content = re.sub(
    r'<group position=\{\[panOffset\.x, 0, panOffset\.z\]\} rotation=\{\[0, fineRotationY, 0\]\}>.*?</group>',
    """{models.map(m => (
                  <group key={m.id} position={[m.panOffset.x, 0, m.panOffset.z]} rotation={[0, m.fineRotationY, 0]}>
                    <ModelRenderer geometry={m.geometry} scale={m.scale} snapRotation={m.snapRotation} showMeasurements={showMeasurements && activeModelId === m.id} unit={unit} isPreviewMode={isPreviewMode} />
                  </group>
                ))}""",
    content,
    flags=re.DOTALL
)

# Replace the Sidebar
content = re.sub(
    r'\{models\.length === 0 && isPreviewMode && \(\s*<div className="absolute top-24 left-6.*?<div className="text-xs font-bold tracking-wider uppercase text-amber-600">Snap Rotate 90°</div>',
    """{models.length > 0 && isPreviewMode && (
          <div className="absolute top-24 left-6 w-56 z-10 bg-[#140b00]/95 backdrop-blur-md border border-[#4a2800] rounded-xl p-4 shadow-2xl flex flex-col gap-3 pointer-events-auto">
             <div className="text-xs font-bold tracking-wider uppercase text-amber-600">Active Part</div>
             <div className="flex gap-2 mb-2">
               <select value={activeModelId || ''} onChange={e => setActiveModelId(e.target.value)} className="flex-1 bg-[#0a0500] text-amber-500 border border-[#4a2800] rounded p-1 text-xs truncate">
                 {models.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
               </select>
               <button onClick={deleteActiveModel} className="px-2 bg-red-900/50 hover:bg-red-800 text-red-400 border border-red-900 rounded font-bold transition-colors" title="Delete Part">✕</button>
             </div>
             <div className="text-xs font-bold tracking-wider uppercase text-amber-600">Snap Rotate 90°</div>""",
    content,
    flags=re.DOTALL
)

# Let me check what the actual string is for the sidebar start!
