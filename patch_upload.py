import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

# Add import
import_str = "import { STLExporter } from 'three/examples/jsm/exporters/STLExporter.js';\nimport * as BufferGeometryUtils from 'three/examples/jsm/utils/BufferGeometryUtils.js';"
content = content.replace("import { STLExporter } from 'three/examples/jsm/exporters/STLExporter.js';", import_str)

# Replace handleFileUpload
old_upload = """  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      const contents = e.target?.result as ArrayBuffer;
      const loader = new STLLoader();
      try {
        const geo = loader.parse(contents);
        geo.rotateX(-Math.PI / 2);
        
        geo.computeBoundingBox();
        if (geo.boundingBox) {
          const center = new THREE.Vector3();
          geo.boundingBox.getCenter(center);
          geo.translate(-center.x, -geo.boundingBox.min.y, -center.z);
        }
        
        setGeometry(geo);
        setObjectScale(1); 
        setPanOffset({ x: 0, z: 0 });
        setFineRotationY(0);
      } catch (err) {
        alert("Failed to parse STL file. Please ensure it's a valid STL.");
      }
    };
    reader.readAsArrayBuffer(file);
  };"""

new_upload = """  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || []);
    if (files.length === 0) return;

    const loader = new STLLoader();
    const geometries: THREE.BufferGeometry[] = [];

    for (const file of files) {
      try {
        const buffer = await file.arrayBuffer();
        const geo = loader.parse(buffer);
        geometries.push(geo);
      } catch (err) {
        console.error("Failed to parse", file.name, err);
        alert(`Failed to parse ${file.name}. Ensure it's a valid STL.`);
      }
    }

    if (geometries.length === 0) return;

    // Merge all geometries into a single assembly to preserve relative positions
    let finalGeo = geometries[0];
    if (geometries.length > 1) {
      finalGeo = BufferGeometryUtils.mergeGeometries(geometries);
    }

    finalGeo.rotateX(-Math.PI / 2); // Convert to Y-up
    
    finalGeo.computeBoundingBox();
    if (finalGeo.boundingBox) {
      const center = new THREE.Vector3();
      finalGeo.boundingBox.getCenter(center);
      finalGeo.translate(-center.x, -finalGeo.boundingBox.min.y, -center.z);
    }
    
    setGeometry(finalGeo);
    setObjectScale(1); 
    setPanOffset({ x: 0, z: 0 });
    setFineRotationY(0);
    setSnapRotation({x: 0, y: 0, z: 0});
  };"""

content = content.replace(old_upload, new_upload)

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
