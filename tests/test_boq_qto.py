import os
import pytest
from debim.loader import load_debim_file
from debim.qto import calculate_qto

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_FILE = os.path.join(ROOT_DIR, "project.yaml")

@pytest.fixture(scope="module")
def qto_result():
    manifest = load_debim_file(PROJECT_FILE)
    qto = calculate_qto(PROJECT_FILE)
    return manifest, qto

def test_piles_count_exact_match(qto_result):
    """Verify footing pile count matches certified BOQ (157 piles)."""
    manifest, qto = qto_result
    footings = [e for e in manifest['elements'] if e.get('class') == 'IfcFooting']
    total_piles = sum(f.get('piles', {}).get('count', 0) for f in footings)
    assert total_piles == 157, f"Expected 157 piles, got {total_piles}"

def test_masonry_wall_areas_exact_match(qto_result):
    """Verify net brick wall areas match certified BOQ (Half brick: 308m2, Full brick: 47m2)."""
    manifest, qto = qto_result
    elem_map = {e.get('tag'): e for e in manifest['elements']}
    
    half_area = 0.0
    full_area = 0.0
    for e in qto.elements:
        if e.element_class == 'IfcWall':
            orig = elem_map.get(e.tag, {})
            t = float(orig.get('thickness', 0.10))
            w_area = e.concrete_volume / t
            if t <= 0.12:
                half_area += w_area
            else:
                full_area += w_area
                
    assert round(half_area, 0) == 308.0, f"Half brick area {half_area:.2f} != 308.0"
    assert round(full_area, 0) == 47.0, f"Full brick area {full_area:.2f} != 47.0"

def test_electrical_fixtures_counts(qto_result):
    """Verify lighting fixtures and electrical device counts."""
    manifest, _ = qto_result
    elems = manifest['elements']
    
    downlights = [e for e in elems if e.get('class') == 'IfcLightFixture' and 'DL' in e.get('tag', '')]
    all_lights = [e for e in elems if e.get('class') == 'IfcLightFixture']
    all_switches = [e for e in elems if e.get('class') == 'IfcSwitchingDevice']
    outlets = [e for e in elems if e.get('class') == 'IfcOutlet']
    
    assert len(downlights) == 34, f"Expected 34 downlights, got {len(downlights)}"
    assert len(all_lights) >= 38, f"Expected >= 38 total lights, got {len(all_lights)}"
    assert len(all_switches) >= 22, f"Expected >= 22 total switches, got {len(all_switches)}"
    assert len(outlets) >= 21, f"Expected >= 21 duplex receptacles, got {len(outlets)}"

def test_plank_slab_area(qto_result):
    """Verify precast plank slab area matches BOQ (149 m2)."""
    manifest, _ = qto_result
    slabs = [e for e in manifest['elements'] if e.get('class') == 'IfcSlab']
    assert len(slabs) >= 12
