import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

# Replace <input type="file" ... /> to include multiple
# We'll use regex to find it

content = re.sub(
    r'<input\s+type="file"\s+accept="\.stl"\s+className="hidden"\s+onChange=\{handleFileUpload\}\s*/>',
    '<input type="file" multiple accept=".stl" className="hidden" onChange={handleFileUpload} />',
    content
)

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
