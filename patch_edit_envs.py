import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

# 1. Update State & activePrinter
old_state = """  const [selectedPrinterPreset, setSelectedPrinterPreset] = useState(PRINTERS[0]);
  const [customDims, setCustomDims] = useState({ width: 300, depth: 300, height: 300 });

  const activePrinter = selectedPrinterPreset.name === 'Custom Printer...' 
    ? { ...selectedPrinterPreset, width: customDims.width, depth: customDims.depth, height: customDims.height } 
    : selectedPrinterPreset;"""

new_state = """  const [selectedPrinterPreset, setSelectedPrinterPreset] = useState(PRINTERS[0]);
  const [customDims, setCustomDims] = useState({ width: PRINTERS[0].width, depth: PRINTERS[0].depth, height: PRINTERS[0].height });

  const activePrinter = { ...selectedPrinterPreset, width: customDims.width, depth: customDims.depth, height: customDims.height };"""

content = content.replace(old_state, new_state)

# 2. Update the onChange for the select
old_select = """              onChange={(e) => setSelectedPrinterPreset(PRINTERS.find(p => p.name === e.target.value) || PRINTERS[0])}"""
new_select = """              onChange={(e) => {
                const p = PRINTERS.find(p => p.name === e.target.value) || PRINTERS[0];
                setSelectedPrinterPreset(p);
                setCustomDims({ width: p.width, depth: p.depth, height: p.height });
              }}"""
content = content.replace(old_select, new_select)

# 3. Always show the XYZ inputs
old_inputs = """          {selectedPrinterPreset.name === 'Custom Printer...' && (
            <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded border bg-[#1a0f00] border-[#4a2800]">
               <span className="text-xs text-amber-700 font-medium">XYZ (mm):</span>
               <input type="number" value={customDims.width} onChange={e => setCustomDims({...customDims, width: parseInt(e.target.value) || 10})} className="w-12 bg-transparent text-xs text-center border-b border-[#4a2800] focus:border-amber-500 focus:outline-none" />
               <input type="number" value={customDims.depth} onChange={e => setCustomDims({...customDims, depth: parseInt(e.target.value) || 10})} className="w-12 bg-transparent text-xs text-center border-b border-[#4a2800] focus:border-amber-500 focus:outline-none" />
               <input type="number" value={customDims.height} onChange={e => setCustomDims({...customDims, height: parseInt(e.target.value) || 10})} className="w-12 bg-transparent text-xs text-center border-b border-[#4a2800] focus:border-amber-500 focus:outline-none" />
            </div>
          )}"""

new_inputs = """          <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded border bg-[#1a0f00] border-[#4a2800]">
             <span className="text-xs text-amber-700 font-medium">XYZ (mm):</span>
             <input type="number" value={customDims.width} onChange={e => setCustomDims({...customDims, width: parseInt(e.target.value) || 10})} className="w-16 bg-transparent text-xs text-center border-b border-[#4a2800] focus:border-amber-500 focus:outline-none" />
             <input type="number" value={customDims.depth} onChange={e => setCustomDims({...customDims, depth: parseInt(e.target.value) || 10})} className="w-16 bg-transparent text-xs text-center border-b border-[#4a2800] focus:border-amber-500 focus:outline-none" />
             <input type="number" value={customDims.height} onChange={e => setCustomDims({...customDims, height: parseInt(e.target.value) || 10})} className="w-16 bg-transparent text-xs text-center border-b border-[#4a2800] focus:border-amber-500 focus:outline-none" />
          </div>"""

# Note: Changed w-12 to w-16 in inputs so that large numbers like 30000 can fit without truncating!

content = content.replace(old_inputs, new_inputs)

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
