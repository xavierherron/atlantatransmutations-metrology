import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

# Replace the Sidebar
sidebar_old = """        {geometry && isPreviewMode && (
          <div className="absolute top-4 left-4 z-20 flex flex-col gap-2 p-4 w-56 rounded-xl border bg-[#1a0f00]/90 border-[#4a2800] backdrop-blur-md shadow-xl">
             <div className="text-xs font-bold tracking-wider uppercase text-amber-600">Snap Rotate 90°</div>"""

sidebar_new = """        {models.length > 0 && isPreviewMode && (
          <div className="absolute top-4 left-4 z-20 flex flex-col gap-2 p-4 w-56 rounded-xl border bg-[#1a0f00]/90 border-[#4a2800] backdrop-blur-md shadow-xl pointer-events-auto">
             <div className="text-xs font-bold tracking-wider uppercase text-amber-600">Active Part</div>
             <div className="flex gap-2 mb-2">
               <select value={activeModelId || ''} onChange={e => setActiveModelId(e.target.value)} className="flex-1 bg-[#0a0500] text-amber-500 border border-[#4a2800] rounded p-1 text-xs truncate">
                 {models.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
               </select>
               <button onClick={deleteActiveModel} className="px-2 bg-red-900/50 hover:bg-red-800 text-red-400 border border-red-900 rounded font-bold transition-colors" title="Delete Part">✕</button>
             </div>
             <div className="text-xs font-bold tracking-wider uppercase text-amber-600">Snap Rotate 90°</div>"""

content = content.replace(sidebar_old, sidebar_new)

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
