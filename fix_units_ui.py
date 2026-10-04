import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

# 1. Update UI Toggle
old_toggle = """            <button 
              onClick={() => setUnit(unit === 'mm' ? 'in' : 'mm')}
              className="px-3 py-2 rounded text-sm font-bold font-mono text-amber-600 hover:bg-[#3a2000] transition-colors"
              title="Toggle Units (mm / in)"
            >
              {unit}
            </button>"""

new_toggle = """            <button 
              onClick={() => {
                if (unit === 'mm') setUnit('in');
                else if (unit === 'in') setUnit('ft');
                else if (unit === 'ft') setUnit('yd');
                else setUnit('mm');
              }}
              className="px-3 py-2 rounded text-sm font-bold font-mono text-amber-600 hover:bg-[#3a2000] transition-colors"
              title="Toggle Units"
            >
              {unit}
            </button>"""
content = content.replace(old_toggle, new_toggle)

# 2. Update format decimal places
old_mr_format = """  const format = (val: number) => {
    if (unit === 'in') return (val / 25.4).toFixed(2);
    if (unit === 'ft') return (val / 304.8).toFixed(2);
    if (unit === 'yd') return (val / 914.4).toFixed(2);
    return val.toFixed(2);
  };"""

new_mr_format = """  const format = (val: number) => {
    if (unit === 'in') return (val / 25.4).toFixed(4);
    if (unit === 'ft') return (val / 304.8).toFixed(4);
    if (unit === 'yd') return (val / 914.4).toFixed(4);
    return val.toFixed(4);
  };"""
content = content.replace(old_mr_format, new_mr_format)

old_vp_format = """    const format = (val: number) => {
        if (unit === 'in') return (val / 25.4).toFixed(1) + ' in';
        if (unit === 'ft') return (val / 304.8).toFixed(2) + ' ft';
        if (unit === 'yd') return (val / 914.4).toFixed(2) + ' yd';
        if (val >= 1000 && unit === 'mm') return (val / 1000).toFixed(1) + ' m';
        return val.toFixed(1) + ' mm';
    };"""

new_vp_format = """    const format = (val: number) => {
        if (unit === 'in') return (val / 25.4).toFixed(4) + ' in';
        if (unit === 'ft') return (val / 304.8).toFixed(4) + ' ft';
        if (unit === 'yd') return (val / 914.4).toFixed(4) + ' yd';
        if (val >= 1000 && unit === 'mm') return (val / 1000).toFixed(4) + ' m';
        return val.toFixed(4) + ' mm';
    };"""
content = content.replace(old_vp_format, new_vp_format)

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
