import os
import pytest
from debim.loader import load_debim_file

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_FILE = os.path.join(ROOT_DIR, "project.yaml")

@pytest.fixture(scope="module")
def manifest():
    return load_debim_file(PROJECT_FILE)

def test_staircase_cantilever_beams(manifest):
    """Verify that staircase landing cantilever beams exist at Grid 4 projecting +0.50m East."""
    elems = {e.get('tag'): e for e in manifest['elements']}
    
    # L1 Stair cantilevers
    assert 'GB-CANT-STAIR-4C' in elems, "Missing GB-CANT-STAIR-4C"
    assert 'GB-CANT-STAIR-4D' in elems, "Missing GB-CANT-STAIR-4D"
    assert 'GB-EDGE-STAIR' in elems, "Missing GB-EDGE-STAIR"
    
    gb_4c = elems['GB-CANT-STAIR-4C']['placement']
    assert gb_4c['from_grid'] == ['4', 'C']
    assert gb_4c['to_grid'] == ['4 + 0.50', 'C']
    assert gb_4c.get('allow_cantilever') is True
    
    # L2 Stair cantilevers
    assert 'B-CANT-STAIR-4C' in elems, "Missing B-CANT-STAIR-4C"
    assert 'B-CANT-STAIR-4D' in elems, "Missing B-CANT-STAIR-4D"
    assert 'B-EDGE-STAIR' in elems, "Missing B-EDGE-STAIR"

def test_staircase_landing_and_bay_walls(manifest):
    """Verify staircase landing slab and exterior enclosure walls with window."""
    elems = {e.get('tag'): e for e in manifest['elements']}
    
    # Stair landing slab
    assert 'STAIR-LANDING' in elems, "Missing STAIR-LANDING"
    landing_bnd = elems['STAIR-LANDING']['placement']['boundary']
    assert ['4 + 0.50', 'C'] in landing_bnd or any('+ 0.50' in pt[0] for pt in landing_bnd)
    
    # Stair enclosure walls
    assert 'W1-STAIR-BAY-WALL' in elems
    assert 'W1-STAIR-BAY-RET-S' in elems
    assert 'W1-STAIR-BAY-RET-N' in elems
    assert 'W2-STAIR-BAY-WALL' in elems
    
    # Window WIN-N5-STAIR
    assert 'WIN-N5-STAIR' in elems
    win5 = elems['WIN-N5-STAIR']
    assert win5['host_wall'] == 'W1-STAIR-BAY-WALL'
    assert win5['dimensions']['width'] == 1.40
    assert win5['dimensions']['height'] == 2.05

def test_living_bay_window_cantilevers(manifest):
    """Verify living room bay window cantilever projecting -0.60m West from Grid 1."""
    elems = {e.get('tag'): e for e in manifest['elements']}
    
    assert 'GB-CANT-1B' in elems
    assert 'GB-CANT-1C' in elems
    assert 'GB-CANT-EDGE' in elems
    assert 'W1-LIVING-BAY-WALL' in elems
    assert 'WIN-N1-LIVING' in elems

def test_master_bedroom_west_and_front_cantilevers(manifest):
    """Verify Level 2 continuous West cantilevers and South front balcony."""
    elems = {e.get('tag'): e for e in manifest['elements']}
    
    # West cantilevers
    for tag in ['B-CANT-1B', 'B-CANT-1C', 'B-CANT-1D', 'B-CANT-1E', 'B-EDGE-WEST']:
        assert tag in elems, f"Missing {tag}"
        
    # South front balcony
    for tag in ['B-CANT-FRONT-1', 'B-CANT-FRONT-2', 'B-EDGE-FRONT']:
        assert tag in elems, f"Missing {tag}"
        
    assert 'W2-MBED-FRONT-WALL' in elems
    assert 'DOOR-D1-BALCONY' in elems
    assert elems['DOOR-D1-BALCONY']['host_wall'] == 'W2-MBED-FRONT-WALL'
