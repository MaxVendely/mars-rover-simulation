import pytest
from rover import Rover
from telemetry import TelemetryLogger

@pytest.fixture
def rover():
    return Rover(
        rover_name="Confidence",
        battery_percentage=100,
        position=[0, 0, 0],
        heading=90,
        operational_status=True,
        current_speed=0,
        battery_consumption=0.1,
        max_speed=5,
        max_acceleration=2,
        max_turn_rate=30
    )

def test_plot_trajectory_without_data():
    logger = TelemetryLogger()
    with pytest.raises(ValueError):
        logger.plot_trajectory()

def test_plot_speed_without_data():
    logger = TelemetryLogger()
    with pytest.raises(ValueError):
        logger.plot_speed()

def test_record(rover):
    logger = TelemetryLogger()
    logger.record(2.5, rover)

    assert len(logger.history) == 1

    rover.set_speed(5)
    rover.update(10)

    assert logger.history[0]["time"] == 2.5
    assert logger.history[0]["position"][0] == 0
    assert logger.history[0]["position"][1] == 0
    assert logger.history[0]["position"][2] == 0
    assert logger.history[0]["heading"] == 90
    assert logger.history[0]["speed"] == 0
    assert logger.history[0]["battery"] == 100
    assert logger.history[0]["operational"] is True

def test_export_csv(rover, tmp_path):
    logger = TelemetryLogger()
    logger.record(2.5, rover)

    filename = tmp_path / "telemetry.csv"
    logger.export_csv(filename)

    with open(filename, "r") as file:
        contents = file.read()

    assert "Timestamp" in contents
    assert "Position X" in contents
    assert "Battery Level" in contents
    assert "Operational" in contents

    assert "2.5" in contents
    assert "90" in contents
    assert "100" in contents
    assert "True" in contents