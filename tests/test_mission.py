from mission import Mission
from rover import Rover
import pytest

@pytest.fixture
def mission():
    return Mission("Test Mission", 10)

@pytest.fixture
def confidence():
    return Rover(
        rover_name="Confidence",
        battery_percentage=100,
        position=[0, 0, 0],
        heading=90,
        operational_status=True,
        current_speed=5,
        battery_consumption=0.1,
        max_speed=5,
        max_acceleration=2,
        max_turn_rate=30
    )

def test_negative_time(mission, confidence):
    with pytest.raises(ValueError):
        mission.add_command(-10, confidence.turn_to, 90)

def test_excessive_time(mission, confidence):
    with pytest.raises(ValueError):
        mission.add_command(11, confidence.turn_to, 90)

def test_appropriate_time(mission, confidence):
    mission.add_command(6, confidence.turn_to, 90)

    assert len(mission.commands) == 1

def test_add_waypoint(mission):
    mission.add_waypoint(0, 1)

    assert len(mission.waypoints) == 1

    mission.add_waypoint(1, 1)

    assert len(mission.waypoints) == 2

def test_get_current_waypoint(mission):
    assert mission.get_current_waypoint() is None

    mission.add_waypoint(0, 1)

    assert mission.get_current_waypoint() == [0, 1]

    mission.add_waypoint(1, 1)

    assert mission.get_current_waypoint() == [0, 1]

def test_complete_current_waypoint(mission):
    mission.add_waypoint(0, 1)
    mission.add_waypoint(1, 1)

    assert mission.get_current_waypoint() == [0, 1]

    mission.complete_current_waypoint()

    assert mission.get_current_waypoint() == [1, 1]

def test_is_current_waypoint_reached(mission, confidence):
    mission.add_waypoint(1, 0)

    assert confidence.position == pytest.approx([0, 0, 0])
    assert mission.is_current_waypoint_reached(confidence.position) is False

    confidence.update(0.09)

    assert confidence.position == pytest.approx([0.45, 0, 0])
    assert mission.is_current_waypoint_reached(confidence.position) is False

    confidence.update(0.01)

    assert confidence.position == pytest.approx([0.5, 0, 0])
    assert mission.is_current_waypoint_reached(confidence.position) is True

def test_are_waypoints_complete(mission):
    mission.add_waypoint(1, 0)

    assert mission.are_waypoints_complete() is False

    mission.complete_current_waypoint()

    assert mission.are_waypoints_complete() is True

def test_no_waypoints_are_complete(mission):
    assert mission.are_waypoints_complete() is True

def test_negative_duration():
    with pytest.raises(ValueError):
        Mission("Test Mission", -1)

def test_zero_duration():
    with pytest.raises(ValueError):
        Mission("Test Mission", 0)