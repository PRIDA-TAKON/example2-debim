import os
import glob
import subprocess
import pytest
from debim.loader import load_debim_file
from debim.schema import load_manifest
from debim.resolver import resolve_manifest
from debim.compliance import check_topological_continuity, detect_mep_structural_clashes

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_FILE = os.path.join(ROOT_DIR, "project.yaml")

def test_manifest_loads_and_includes():
    """Verify that root manifest loads and merges all modular includes."""
    manifest = load_debim_file(PROJECT_FILE)
    assert manifest is not None
    assert "elements" in manifest
    assert len(manifest["elements"]) >= 380, f"Expected >= 380 elements, got {len(manifest['elements'])}"
    assert "includes" in manifest
    
    # Check that modular includes exist in models/ directory
    yaml_files = glob.glob(os.path.join(ROOT_DIR, "models", "**", "*.yaml"), recursive=True)
    assert len(yaml_files) >= 15, f"Expected >= 15 modular yaml files, got {len(yaml_files)}"

def test_debim_cli_validate():
    """Verify that debim validate CLI command exits with code 0."""
    res = subprocess.run(["debim", "validate", "-m", PROJECT_FILE], capture_output=True, text=True)
    assert res.returncode == 0, f"Validation failed: {res.stderr or res.stdout}"
    assert "Pydantic Schema Validation passed" in res.stdout
    assert "Validation completed successfully with 0 warnings or errors" in res.stdout

def test_compliance_rules():
    """Verify programmatic compliance rules: schema, topology, clash detection."""
    manifest = load_manifest(PROJECT_FILE)
    assert manifest is not None
    
    # 1. Topology continuity check (empty list means 0 topology continuity issues)
    topo_issues = check_topological_continuity(manifest)
    assert len(topo_issues) == 0, f"Topology continuity issues found: {topo_issues}"
    
    # 2. MEP Structural clashes (empty list means 0 clashes)
    clashes = detect_mep_structural_clashes(manifest)
    assert len(clashes) == 0, f"Clashes found: {clashes}"

def test_resolved_spatial_hierarchy():
    """Verify storeys and spatial grid resolution."""
    manifest = load_manifest(PROJECT_FILE)
    assert len(manifest.spatial_structure.storeys) == 4
    storey_ids = [s.id for s in manifest.spatial_structure.storeys]
    assert "Foundation" in storey_ids
    assert "L1" in storey_ids
    assert "L2" in storey_ids
    assert "Roof" in storey_ids
    
    resolved = resolve_manifest(manifest)
    assert resolved is not None
    assert len(resolved.columns) > 0
    assert len(resolved.beams) > 0
    assert len(resolved.walls) > 0
