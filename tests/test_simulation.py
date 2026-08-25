import pytest

from rover import Rover
from simulation import Simulation
from mission import Mission


@pytest.fixture
def rover():
    return Rover(
        rover_name="Confidence",
        battery_percentage=100,
        position=[0, 0, 0],
        heading=0,
        operational_status=True,
        current_speed=0,
        battery_consumption=0.1,
        max_speed=5,
        max_acceleration=2,
        max_turn_rate=30
    )

def test_simulation_time(rover):
    mission = Mission("Test Mission", 10)

    simulation = Simulation(
        rover=rover,
        mission=mission,
        time_step=1
    )

    simulation.run()

    assert simulation.current_time == pytest.approx(10)

def test_simulation_remainder(rover):
    mission = Mission("Test Mission", 10)

    simulation = Simulation(
        rover=rover,
        mission=mission,
        time_step=3
    )

    simulation.run()

    assert simulation.current_time == pytest.approx(10)

def test_simulation_logging(rover):
    mission = Mission("Test Mission", 10)

    simulation = Simulation(
        rover=rover,
        mission=mission,
        time_step=1
    )

    simulation.run()

    assert len(simulation.logger.history) == 11

    assert simulation.logger.history[0]["time"] == pytest.approx(0)

    assert simulation.logger.history[-1]["time"] == pytest.approx(10)

def test_scheduled_command(rover):
    mission = Mission("Test Mission", 10)

    simulation = Simulation(
        rover=rover,
        mission=mission,
        time_step=2
    )

    mission.add_command(3, rover.set_speed, 5)

    simulation.run()

    assert 0 in simulation.executed_commands

    assert rover.target_speed == pytest.approx(5)

def test_command_at_zero(rover):
    mission = Mission("Test Mission", 10)

    simulation = Simulation(
        rover=rover,
        mission=mission,
        time_step=1
    )

    mission.add_command(0, rover.set_speed, 5)

    simulation.run()

    assert 0 in simulation.executed_commands

    assert rover.target_speed == pytest.approx(5)

def test_successful_mission(rover):
    mission = Mission("Test Mission", 10)

    simulation = Simulation(
        rover=rover,
        mission=mission,
        time_step=1
    )

    simulation.run()

    assert simulation.mission_successful is True

    assert simulation.mission_result == "SUCCESS"

def test_failed_system(rover):
    rover.operational_status = False

    mission = Mission("Test Mission", 10)

    simulation = Simulation(
        rover=rover,
        mission=mission,
        time_step=1
    )

    simulation.run()

    assert simulation.mission_successful is False

    assert simulation.mission_result == "FAILED_SYSTEM"

def test_failed_battery(rover):
    rover.battery_percentage = 0

    mission = Mission("Test Mission", 10)

    simulation = Simulation(
        rover=rover,
        mission=mission,
        time_step=1
    )

    simulation.run()

    assert simulation.mission_successful is False

    assert simulation.mission_result == "FAILED_BATTERY"

def test_mission_summary(rover):
    mission = Mission("Test Mission", 10)

    simulation = Simulation(
        rover=rover,
        mission=mission,
        time_step=1
    )

    simulation.run()

    summary = simulation.get_summary()

    assert summary["mission"] == "Test Mission"
    assert summary["result"] == "SUCCESS"
    assert summary["duration"] == pytest.approx(10)

    assert "final_position" in summary
    assert "final_heading" in summary
    assert "final_battery" in summary


def test_summary_position_is_copy(rover):
    mission = Mission("Test Mission", 10)

    simulation = Simulation(
        rover=rover,
        mission=mission,
        time_step=1
    )

    simulation.run()

    summary = simulation.get_summary()
    original_x = rover.position[0]

    summary["final_position"][0] = 999

    assert rover.position[0] == pytest.approx(original_x)

def test_command_between_steps(rover):
    mission = Mission("Test Mission", 0.2)

    simulation = Simulation(
        rover=rover,
        mission=mission,
        time_step=0.1
    )

    mission.add_command(0.15, rover.set_speed, 5)

    simulation.run()

    assert rover.position[1] > 0

def test_multiple_commands_between_steps(rover):
    mission = Mission("Test Mission", 0.2)

    simulation = Simulation(
        rover=rover,
        mission=mission,
        time_step=0.1
    )

    mission.add_command(0.12, rover.set_speed, 5)
    mission.add_command(0.18, rover.set_speed, 2)

    simulation.run()

    assert rover.target_speed == 2
    assert 0 in simulation.executed_commands
    assert 1 in simulation.executed_commands

def test_waypoint_reached(rover):
    mission = Mission("Test Mission", 5)

    simulation = Simulation(
        rover=rover,
        mission=mission,
        time_step=0.1
    )

    mission.add_waypoint(0, 2)

    mission.add_command(0, rover.set_speed, 5)

    simulation.run()

    assert mission.are_waypoints_complete() is True
    assert simulation.get_summary()["result"] == "SUCCESS"

def test_waypoint_not_reached(rover):
    mission = Mission("Test Mission", 5)

    simulation = Simulation(
        rover=rover,
        mission=mission,
        time_step=0.1
    )

    mission.add_waypoint(0, 2)
    mission.add_waypoint(2, 0)

    mission.add_command(0, rover.set_speed, 5)

    simulation.run()

    assert mission.are_waypoints_complete() is False
    assert simulation.get_summary()["result"] == "FAILED_OBJECTIVE"

def test_multiple_waypoints_reached(rover):
    mission = Mission("Test Mission", 5)

    simulation = Simulation(
        rover=rover,
        mission=mission,
        time_step=0.1
    )

    mission.add_waypoint(0, 2)
    mission.add_waypoint(0, 4)
    mission.add_waypoint(0, 6)
    mission.add_waypoint(0, 8)

    mission.add_command(0, rover.set_speed, 5)

    simulation.run()

    assert mission.are_waypoints_complete() is True
    assert simulation.get_summary()["result"] == "SUCCESS"

def test_waypoint_at_start(rover):
    mission = Mission("Test Mission", 5)

    simulation = Simulation(
        rover=rover,
        mission=mission,
        time_step=1
    )

    mission.add_command(0, rover.set_speed, 5)

    mission.add_waypoint(0, 0)

    simulation.run()

    assert mission.are_waypoints_complete() is True
    assert simulation.get_summary()["result"] == "SUCCESS"

def test_zero_timestep(rover):
    mission = Mission("Test Mission", 5)

    with pytest.raises(ValueError):
        Simulation(rover, mission, 0)

def test_negative_timestep(rover):
    mission = Mission("Test Mission", 5)

    with pytest.raises(ValueError):
        Simulation(rover, mission, -1)

def test_rerun_simulation(rover):
    mission = Mission("Test Mission", 5)
    mission.add_command(0, rover.set_speed, 5)
    mission.add_command(1, rover.turn_to, 90)
    mission.add_command(4, rover.turn_to, 180)

    simulation = Simulation(
        rover=rover,
        mission=mission,
        time_step=0.1
    )

    simulation.run()

    run_1_summary = simulation.get_summary()

    simulation.run()

    run_2_summary = simulation.get_summary()

    assert run_1_summary["final_position"] == run_2_summary["final_position"] 
    assert run_1_summary["final_battery"] == run_2_summary["final_battery"]
    assert run_1_summary["result"] == run_2_summary["result"]

def test_reset_restores_waypoint_progress(rover):
    mission = Mission("Test Mission", 5)

    simulation = Simulation(
        rover=rover,
        mission=mission,
        time_step=0.1
    )

    mission.add_waypoint(0, 2)

    mission.add_command(0, rover.set_speed, 5)

    simulation.run()

    assert mission.are_waypoints_complete() is True
    assert simulation.get_summary()["result"] == "SUCCESS"

    simulation.reset()

    assert mission.are_waypoints_complete() is False

    simulation.run()

    assert mission.are_waypoints_complete() is True
    assert simulation.get_summary()["result"] == "SUCCESS"