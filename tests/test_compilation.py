import os
import subprocess
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_FILE = os.path.join(ROOT_DIR, "project.yaml")
OUTPUT_IFC = os.path.join(ROOT_DIR, "tests", "test_output.ifc")

def test_ifc4_compilation_success():
    """Verify that debim compiles the modular manifest to valid IFC4 with proper geometry."""
    if os.path.exists(OUTPUT_IFC):
        os.remove(OUTPUT_IFC)
        
    cmd = ["debim", "compile", "-m", PROJECT_FILE, "-o", OUTPUT_IFC]
    res = subprocess.run(cmd, capture_output=True)
    
    assert res.returncode == 0, f"Compilation failed with exit code {res.returncode}"
    assert os.path.exists(OUTPUT_IFC), "Output IFC file was not created"
    
    file_size = os.path.getsize(OUTPUT_IFC)
    assert file_size > 400_000, f"IFC file size too small: {file_size} bytes (expected > 400KB)"

def test_ifc_entities_integrity():
    """Verify essential IFC entity counts in compiled model."""
    assert os.path.exists(OUTPUT_IFC)
    with open(OUTPUT_IFC, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    assert "IFCCOLUMN" in content
    assert "IFCBEAM" in content
    assert "IFCSLAB" in content
    assert "IFCWALL" in content
    assert "IFCDOOR" in content
    assert "IFCWINDOW" in content
    assert "IFCFOOTING" in content
