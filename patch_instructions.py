import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

# 1. Add state
old_state = "const [showMeasurements, setShowMeasurements] = useState(true);"
new_state = "const [showMeasurements, setShowMeasurements] = useState(true);\n  const [showInstructions, setShowInstructions] = useState(true);"
content = content.replace(old_state, new_state)

# 2. Add Help button to header
old_tools = """          {/* Tools Group */}
          <div className="flex items-center gap-1 border-r border-[#4a2800] pr-4">"""
new_tools = """          {/* Tools Group */}
          <div className="flex items-center gap-1 border-r border-[#4a2800] pr-4">
            <button 
              onClick={() => setShowInstructions(true)}
              className="px-3 py-2 rounded text-sm font-bold font-mono text-amber-600 hover:bg-[#3a2000] transition-colors"
              title="Help / Instructions"
            >
              ?
            </button>"""
content = content.replace(old_tools, new_tools)

# 3. Add Instructions Modal
old_canvas_end = """        {models.length === 0 && isPreviewMode && (
          <div className="absolute z-10 text-gray-500 font-mono text-sm border-2 border-gray-300 p-8 rounded-xl border-dashed bg-white/50 backdrop-blur-sm pointer-events-none shadow-sm">
            Upload an STL to preview inside the <span className="font-bold text-gray-700">{activePrinter.name}</span>
          </div>
        )}"""

new_canvas_end = """        {models.length === 0 && isPreviewMode && (
          <div className="absolute z-10 text-gray-500 font-mono text-sm border-2 border-gray-300 p-8 rounded-xl border-dashed bg-white/50 backdrop-blur-sm pointer-events-none shadow-sm">
            Upload an STL to preview inside the <span className="font-bold text-gray-700">{activePrinter.name}</span>
          </div>
        )}

        {showInstructions && (
          <div className="absolute bottom-8 left-8 z-30 bg-[#1a0f00]/95 backdrop-blur-md border border-[#4a2800] rounded-xl p-5 shadow-2xl max-w-sm pointer-events-auto">
             <div className="flex justify-between items-center mb-3">
                <h3 className="text-amber-500 font-bold uppercase tracking-widest text-sm">How to use it</h3>
                <button onClick={() => setShowInstructions(false)} className="text-amber-700 hover:text-amber-400 font-bold transition-colors">✕</button>
             </div>
             <ul className="text-amber-600/80 text-xs space-y-2 leading-relaxed">
               <li><strong className="text-amber-500">X / Z Axes (Horizontal):</strong> Use your <kbd className="bg-[#0a0500] px-1.5 py-0.5 rounded border border-[#4a2800] font-mono shadow-sm">Arrow Keys</kbd> to slide parts across the floor.</li>
               <li><strong className="text-amber-500">Y Axis (Elevation):</strong> Use <kbd className="bg-[#0a0500] px-1.5 py-0.5 rounded border border-[#4a2800] font-mono shadow-sm">W</kbd> and <kbd className="bg-[#0a0500] px-1.5 py-0.5 rounded border border-[#4a2800] font-mono shadow-sm">S</kbd> to levitate parts up or push them down.</li>
               <li><strong className="text-amber-500">Fine Rotation:</strong> Use <kbd className="bg-[#0a0500] px-1.5 py-0.5 rounded border border-[#4a2800] font-mono shadow-sm">[</kbd> and <kbd className="bg-[#0a0500] px-1.5 py-0.5 rounded border border-[#4a2800] font-mono shadow-sm">]</kbd> to smoothly rotate the active part.</li>
               <li><strong className="text-amber-500">Speed Boost:</strong> Hold <kbd className="bg-[#0a0500] px-1.5 py-0.5 rounded border border-[#4a2800] font-mono shadow-sm">Shift</kbd> while pressing any of the above keys to move 10x faster.</li>
               <li><strong className="text-amber-500">Reset:</strong> Press <kbd className="bg-[#0a0500] px-1.5 py-0.5 rounded border border-[#4a2800] font-mono shadow-sm">C</kbd> to instantly center the active part.</li>
             </ul>
             <button onClick={() => setShowInstructions(false)} className="mt-4 w-full py-2 bg-amber-600/20 hover:bg-amber-600/30 text-amber-500 border border-amber-900/50 rounded font-bold transition-colors">
               Got it
             </button>
          </div>
        )}"""

content = content.replace(old_canvas_end, new_canvas_end)


with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
