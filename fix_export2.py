import re

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'r') as f:
    content = f.read()

# Replace exportSTL function completely using regex
content = re.sub(
    r"const exportSTL = \(\) => \{.*?(?=  const containerRef)",
    """const exportSTL = () => {
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

    const exportMesh = new THREE.Mesh(finalExportGeo, new THREE.MeshBasicMaterial());
    const exporter = new STLExporter();
    const stlString = exporter.parse(exportMesh);
    
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
  };
""",
    content,
    flags=re.DOTALL
)

with open('/Users/xavierherron/atlantatransmutations-metrology/src/App.tsx', 'w') as f:
    f.write(content)
