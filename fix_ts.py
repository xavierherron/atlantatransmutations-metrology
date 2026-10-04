import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

# 1. Type the params in keyboard shortcuts
content = content.replace("setPanOffset(p =>", "setPanOffset((p: {x:number, z:number}) =>")
content = content.replace("setFineRotationY(r =>", "setFineRotationY((r: number) =>")
content = content.replace("setSnapRotation(prev =>", "setSnapRotation((prev: {x:number, y:number, z:number}) =>")

# 2. Check if BufferGeometryUtils is really in exportSTL
if "BufferGeometryUtils.mergeGeometries" not in content:
    # It failed to replace exportSTL earlier!
    export_old = """  const exportSTL = () => {
    if (!geometry) return;
    const exportGeo = geometry.clone();
    
    // Apply transformations in the exact order they are rendered
    exportGeo.scale(objectScale, objectScale, objectScale);
    
    exportGeo.rotateX(snapRotation.x);
    exportGeo.rotateY(snapRotation.y);
    exportGeo.rotateZ(snapRotation.z);
    
    exportGeo.computeBoundingBox();
    if (exportGeo.boundingBox) {
      const center = new THREE.Vector3();
      exportGeo.boundingBox.getCenter(center);
      exportGeo.translate(-center.x, -exportGeo.boundingBox.min.y, -center.z);
    }
    
    exportGeo.rotateY(fineRotationY);
    exportGeo.translate(panOffset.x, 0, panOffset.z);
    
    // Convert back from ThreeJS Y-up space to standard STL Z-up space
    exportGeo.rotateX(Math.PI / 2);

    const exporter = new STLExporter();
    const mesh = new THREE.Mesh(exportGeo, new THREE.MeshBasicMaterial());
    const result = exporter.parse(mesh, { binary: true });
    
    const blob = new Blob([result], { type: 'application/octet-stream' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'aligned_projection.stl';
    link.click();
    URL.revokeObjectURL(url);
  };"""

    export_new = """  const exportSTL = () => {
    if (models.length === 0) return;
    
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
        exportGeo.translate(m.panOffset.x, 0, m.panOffset.z);
        exportGeo.rotateX(Math.PI / 2);
        return exportGeo;
    });

    let finalExportGeo = geometriesToExport[0];
    if (geometriesToExport.length > 1) {
        finalExportGeo = BufferGeometryUtils.mergeGeometries(geometriesToExport);
    }

    const exporter = new STLExporter();
    const mesh = new THREE.Mesh(finalExportGeo, new THREE.MeshBasicMaterial());
    const result = exporter.parse(mesh, { binary: true });
    
    const blob = new Blob([result], { type: 'application/octet-stream' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'aligned_projection.stl';
    link.click();
    URL.revokeObjectURL(url);
  };"""
    content = content.replace(export_old, export_new)

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
