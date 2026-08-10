from src.map_visualization import (
    RESULTS_FILE,
    OUTPUT_DIR,
    load_results,
    load_world_map,
    create_risk_map,
)


def test_results_file_exists():
    assert RESULTS_FILE.exists()


def test_load_results_returns_data():
    df = load_results()

    assert df is not None
    assert len(df) > 0


def test_world_map_loads():
    world = load_world_map()

    assert world is not None
    assert len(world) > 0


def test_world_map_has_country_codes():
    world = load_world_map()

    assert "ISO_A3" in world.columns


def test_risk_map_is_created():
    output_file = create_risk_map()

    assert output_file.exists()
    assert output_file.suffix == ".png"


def test_risk_map_is_not_empty():
    output_file = create_risk_map()

    assert output_file.exists()
    assert output_file.stat().st_size > 0


def test_risk_map_is_saved_in_visualization_directory():
    output_file = create_risk_map()

    assert output_file.parent == OUTPUT_DIR