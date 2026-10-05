import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

old_export_logic = """        const exporter = new STLExporter();
        const stlString = exporter.parse(group);
        
        const blob = new Blob([stlString], { type: 'text/plain' });"""

new_export_logic = """        const exporter = new STLExporter();
        const result = exporter.parse(group, { binary: true });
        
        const blob = new Blob([result], { type: 'application/octet-stream' });"""

content = content.replace(old_export_logic, new_export_logic)

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
