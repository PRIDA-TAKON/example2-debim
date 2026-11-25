"""
Continuous Integration & Verification Test Suite for Modern Tropical Residence
"""

import sys
from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

MANIFEST_FILE = ROOT_DIR / "project.yaml"

def test_manifest_exists():
    assert MANIFEST_FILE.exists(), "project.yaml must exist"

def test_debim_validation_and_compilation():
    from debim.schema import load_manifest
    from debim.compiler import compile_to_ifc

    manifest = load_manifest(MANIFEST_FILE)
    assert manifest.project.id == "PRJ-MODERN-TROPICAL-2STOREY"
    assert len(manifest.elements) > 50, f"Expected > 50 elements, got {len(manifest.elements)}"

    # Test IFC compilation
    out_ifc = ROOT_DIR / "test_output.ifc"
    try:
        compile_to_ifc(manifest, out_ifc)
        assert out_ifc.exists()
        assert out_ifc.stat().st_size > 50000
    finally:
        if out_ifc.exists():
            out_ifc.unlink()

def test_architectural_spatial_verification():
    from verify_design import run_verification
    model_json = ROOT_DIR / "house_spatial_model.json"
    assert model_json.exists()
    # Runs the 5 verification checks (Setbacks, OSR, Negatives, Graph, Ensuite)
    run_verification(model_json)
