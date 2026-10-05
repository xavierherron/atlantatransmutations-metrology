import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

# 1. Remove BufferGeometryUtils import
content = re.sub(r"import \* as BufferGeometryUtils from 'three/examples/jsm/utils/BufferGeometryUtils\.js';\n", "", content)

# 2. Simplify exportSTL
old_export = """  const exportSTL = () => {
    if (models.length === 0) return;
    
    try {
        const geometriesToExport = models.map(m => {
            const exportGeo = m.geometry.clone();
            exportGeo.scale(m.scale, m.scale, m.scale);
            exportGeo.rotateX(m.snapRotation.x);
            exportGeo.rotateY(m.snapRotation.y);
            exportGeo.rotateZ(m.snapRotation.z);
            exportGeo.computeBoundingBox();
            if (exportGeo.boundingBox) {
              const center = new THREE.Vector3();
              exportGeo.boundingBox.getCenter(center);
              exportGeo.translate(-center.x, -exportGeo.boundingBox.min.y, -center.z);
            }
            exportGeo.rotateY(m.fineRotationY);
            exportGeo.translate(m.panOffset.x, m.panOffset.y, m.panOffset.z);
            exportGeo.rotateX(Math.PI / 2);
            return exportGeo;
        });

        let finalExportGeo = geometriesToExport[0];
        if (geometriesToExport.length > 1) {
            // Fix: ensure all geometries have the same attributes before merging
            // Delete attributes that are not 'position' or 'normal' to avoid mismatches
            geometriesToExport.forEach(g => {
                for (const key in g.attributes) {
                    if (key !== 'position' && key !== 'normal') {
                        g.deleteAttribute(key);
                    }
                }
            });
            finalExportGeo = BufferGeometryUtils.mergeGeometries(geometriesToExport, false);
        }

        // Fix: Use a Scene or Object3D instead of a single Mesh if merging fails,
        // Actually, STLExporter supports exporting an Object3D containing multiple meshes!
        // So we don't even need to merge them if we just put them in a Group!
        const group = new THREE.Group();
        if (geometriesToExport.length > 1) {
            geometriesToExport.forEach(geo => {
                group.add(new THREE.Mesh(geo, new THREE.MeshBasicMaterial()));
            });
        } else {
            group.add(new THREE.Mesh(finalExportGeo, new THREE.MeshBasicMaterial()));
        }

        const exporter = new STLExporter();
        const stlString = exporter.parse(group);
        
        const blob = new Blob([stlString], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.style.display = 'none';
        link.href = url;
        link.download = 'aligned_part.stl';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    } catch (err) {
        console.error("Export failed:", err);
        alert("Failed to export STL: " + (err instanceof Error ? err.message : String(err)));
    }
  };"""

new_export = """  const exportSTL = () => {
    if (models.length === 0) return;
    
    try {
        const geometriesToExport = models.map(m => {
            const exportGeo = m.geometry.clone();
            exportGeo.scale(m.scale, m.scale, m.scale);
            exportGeo.rotateX(m.snapRotation.x);
            exportGeo.rotateY(m.snapRotation.y);
            exportGeo.rotateZ(m.snapRotation.z);
            exportGeo.computeBoundingBox();
            if (exportGeo.boundingBox) {
              const center = new THREE.Vector3();
              exportGeo.boundingBox.getCenter(center);
              exportGeo.translate(-center.x, -exportGeo.boundingBox.min.y, -center.z);
            }
            exportGeo.rotateY(m.fineRotationY);
            exportGeo.translate(m.panOffset.x, m.panOffset.y, m.panOffset.z);
            exportGeo.rotateX(Math.PI / 2);
            return exportGeo;
        });

        const group = new THREE.Group();
        geometriesToExport.forEach(geo => {
            group.add(new THREE.Mesh(geo, new THREE.MeshBasicMaterial()));
        });

        const exporter = new STLExporter();
        const stlString = exporter.parse(group);
        
        const blob = new Blob([stlString], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.style.display = 'none';
        link.href = url;
        link.download = 'aligned_assembly.stl';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    } catch (err) {
        console.error("Export failed:", err);
        alert("Failed to export STL: " + (err instanceof Error ? err.message : String(err)));
    }
  };"""

content = content.replace(old_export, new_export)

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
