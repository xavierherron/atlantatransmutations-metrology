import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

# 1. Update State
content = content.replace("const [unit, setUnit] = useState<'mm'|'in'>('mm');", "const [unit, setUnit] = useState<'mm'|'in'|'ft'|'yd'>('mm');")

# 2. Update ModelRenderer Signature and Format
old_mr_sig = "unit?: 'mm' | 'in'"
new_mr_sig = "unit?: 'mm' | 'in' | 'ft' | 'yd'"
content = content.replace(old_mr_sig, new_mr_sig)

old_mr_format = "const format = (val: number) => (unit === 'in' ? val / 25.4 : val).toFixed(2);"
new_mr_format = """const format = (val: number) => {
    if (unit === 'in') return (val / 25.4).toFixed(2);
    if (unit === 'ft') return (val / 304.8).toFixed(2);
    if (unit === 'yd') return (val / 914.4).toFixed(2);
    return val.toFixed(2);
  };"""
content = content.replace(old_mr_format, new_mr_format)

# 3. Update VirtualPrinter Signature and Format
old_vp_sig = "unit?: 'mm'|'in'"
new_vp_sig = "unit?: 'mm'|'in'|'ft'|'yd'"
content = content.replace(old_vp_sig, new_vp_sig)

old_vp_format = """    const format = (val: number) => {
        if (val >= 1000 && unit === 'mm') return (val / 1000).toFixed(1) + ' m';
        return (unit === 'in' ? val / 25.4 : val).toFixed(1) + ' ' + unit;
    };"""
new_vp_format = """    const format = (val: number) => {
        if (unit === 'in') return (val / 25.4).toFixed(1) + ' in';
        if (unit === 'ft') return (val / 304.8).toFixed(2) + ' ft';
        if (unit === 'yd') return (val / 914.4).toFixed(2) + ' yd';
        if (val >= 1000 && unit === 'mm') return (val / 1000).toFixed(1) + ' m';
        return val.toFixed(1) + ' mm';
    };"""
content = content.replace(old_vp_format, new_vp_format)

# 4. Update UI Header Toggle
old_ui_toggle = """             <div className="flex gap-1 bg-[#1a0f00] p-1 rounded-lg border border-[#3a2000]">
               <button onClick={() => setUnit('mm')} className={`px-2 py-1 text-[10px] font-bold rounded ${unit === 'mm' ? 'bg-[#ffaa00] text-black' : 'text-amber-500'}`}>mm</button>
               <button onClick={() => setUnit('in')} className={`px-2 py-1 text-[10px] font-bold rounded ${unit === 'in' ? 'bg-[#ffaa00] text-black' : 'text-amber-500'}`}>in</button>
             </div>"""
new_ui_toggle = """             <div className="flex gap-1 bg-[#1a0f00] p-1 rounded-lg border border-[#3a2000]">
               <button onClick={() => setUnit('mm')} className={`px-2 py-1 text-[10px] font-bold rounded ${unit === 'mm' ? 'bg-[#ffaa00] text-black' : 'text-amber-500 hover:text-amber-300'}`}>mm</button>
               <button onClick={() => setUnit('in')} className={`px-2 py-1 text-[10px] font-bold rounded ${unit === 'in' ? 'bg-[#ffaa00] text-black' : 'text-amber-500 hover:text-amber-300'}`}>in</button>
               <button onClick={() => setUnit('ft')} className={`px-2 py-1 text-[10px] font-bold rounded ${unit === 'ft' ? 'bg-[#ffaa00] text-black' : 'text-amber-500 hover:text-amber-300'}`}>ft</button>
               <button onClick={() => setUnit('yd')} className={`px-2 py-1 text-[10px] font-bold rounded ${unit === 'yd' ? 'bg-[#ffaa00] text-black' : 'text-amber-500 hover:text-amber-300'}`}>yd</button>
             </div>"""
content = content.replace(old_ui_toggle, new_ui_toggle)

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
