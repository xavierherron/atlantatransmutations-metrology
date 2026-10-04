import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

# 1. Add delete logic
delete_logic = """  const deleteActiveModel = () => {
    if (!activeModelId) return;
    const remaining = models.filter(m => m.id !== activeModelId);
    setModels(remaining);
    setActiveModelId(remaining.length > 0 ? remaining[0].id : null);
  };
"""

content = content.replace("const [projScale, setProjScale] = useState(1);", "const [projScale, setProjScale] = useState(1);\n" + delete_logic)


# 2. Add delete button UI
sidebar_select_old = """             <select value={activeModelId || ''} onChange={e => setActiveModelId(e.target.value)} className="w-full bg-[#0a0500] text-amber-500 border border-[#4a2800] rounded p-1 mb-2 text-xs">
               {models.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
             </select>"""

sidebar_select_new = """             <div className="flex gap-2 mb-2">
               <select value={activeModelId || ''} onChange={e => setActiveModelId(e.target.value)} className="flex-1 bg-[#0a0500] text-amber-500 border border-[#4a2800] rounded p-1 text-xs truncate">
                 {models.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
               </select>
               <button onClick={deleteActiveModel} className="px-2 bg-red-900/50 hover:bg-red-800 text-red-400 border border-red-900 rounded font-bold transition-colors" title="Delete Part">✕</button>
             </div>"""

content = content.replace(sidebar_select_old, sidebar_select_new)

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
