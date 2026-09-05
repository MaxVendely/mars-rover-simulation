import pytest
import sqlite3
from database import Database
from mission import Mission
from rover import Rover
from simulation import Simulation


@pytest.fixture
def database(tmp_path):
    database_path = tmp_path / "test.db"

    database = Database(database_path)
    database.initialize()

    return database

def test_add_rover(database):
    rover_id = database.add_rover(
        "Confidence",
        0.1,
        5,
        2,
        30,
    )

    rovers = database.get_rovers()

    assert rover_id == 1
    assert len(rovers) == 1
    assert rovers[0] == (
        1,
        "Confidence",
        0.1,
        5.0,
        2.0,
        30.0,
    )

def test_add_multiple_rovers(database):
    rover_id = database.add_rover(
        "Confidence",
        0.1,
        5,
        2,
        30,
    )

    rover_id_2 = database.add_rover(
            "Confidence2",
            0.1,
            5,
            2,
            30,
        )
    

    rovers = database.get_rovers()

    assert rover_id == 1
    assert rover_id_2 == 2
    assert len(rovers) == 2
    assert rovers[0] == (
        1,
        "Confidence",
        0.1,
        5.0,
        2.0,
        30.0,
    )
    assert rovers[1] == (
        2,
        "Confidence2",
        0.1,
        5.0,
        2.0,
        30.0,
    )

def test_add_duplicate_rovers(database):
    rover_id = database.add_rover(
        "Confidence",
        0.1,
        5,
        2,
        30,
    )

    rover_id_2 = database.add_rover(
            "Confidence",
            0.1,
            5,
            2,
            30,
        )
    

    rovers = database.get_rovers()

    assert rover_id == rover_id_2 == 1
    assert len(rovers) == 1
    assert rovers[0] == (
        1,
        "Confidence",
        0.1,
        5.0,
        2.0,
        30.0,
    )


def test_add_mission(database):
    rover_id = database.add_rover(
        "Confidence",
        0.1,
        5,
        2,
        30,
    )

    mission_id = database.add_mission(
        rover_id,
        "Test Mission",
        35,
    )

    missions = database.get_missions()

    assert mission_id == 1
    assert len(missions) == 1
    assert missions[0] == (
        1,
        1,
        "Test Mission",
        35.0,
        None,
    )

def test_update_mission_result(database):
    rover_id = database.add_rover(
        "Confidence",
        0.1,
        5,
        2,
        30,
    )

    mission_id = database.add_mission(
        rover_id,
        "Test Mission",
        35,
    )

    database.update_mission_result(mission_id, "SUCCESS")

    missions = database.get_missions()

    assert mission_id == 1
    assert len(missions) == 1
    assert missions[0] == (
        1,
        1,
        "Test Mission",
        35.0,
        "SUCCESS",
    )

def test_add_telemetry(database):
    rover_id = database.add_rover(
        "Confidence",
        0.1,
        5,
        2,
        30,
    )

    mission_id = database.add_mission(
        rover_id,
        "Test Mission",
        35,
    )

    sample = {
        "time": 2.5,
        "position": [10, 20, 0],
        "heading": 90,
        "speed": 4,
        "battery": 95.5,
        "operational": True,
    }

    telemetry_id = database.add_telemetry(
        mission_id,
        sample
    )

    telemetry = database.get_telemetry()

    assert telemetry_id == 1
    assert len(telemetry) == 1
    assert telemetry[0] == (
        1,
        1,
        2.5,
        10.0,
        20.0,
        0.0,
        90.0,
        4.0,
        95.5,
        1,
    )

def test_add_telemetry_history(database):
    rover_id = database.add_rover(
        "Confidence",
        0.1,
        5,
        2,
        30,
    )

    mission_id = database.add_mission(
        rover_id,
        "Test Mission",
        35,
    )

    sample1 = {
        "time": 2.5,
        "position": [10, 20, 0],
        "heading": 90,
        "speed": 4,
        "battery": 95.5,
        "operational": True,
    }

    sample2 = {
        "time": 3.0,
        "position": [10, 30, 15],
        "heading": 90,
        "speed": 4,
        "battery": 95,
        "operational": True,
    }

    sample3 = {
        "time": 3.5,
        "position": [10, 40, 30],
        "heading": 90,
        "speed": 4,
        "battery": 94.5,
        "operational": True,
    }

    history = (sample1, sample2, sample3)

    database.add_telemetry_history(
        mission_id,
        history
    )

    telemetry = database.get_telemetry()

    assert len(telemetry) == 3
    assert telemetry[0] == (
        1,
        1,
        2.5,
        10.0,
        20.0,
        0.0,
        90.0,
        4.0,
        95.5,
        1,
    )
    assert telemetry[2] == (
        3,
        1,
        3.5,
        10.0,
        40.0,
        30.0,
        90.0,
        4.0,
        94.5,
        1,
    )

def test_mission_requires_valid_rover(database):
    with pytest.raises(sqlite3.IntegrityError):
        database.add_mission(
            999,
            "Test Mission without Rover",
            35,
        )

def test_telemetry_requires_valid_mission(database):
    with pytest.raises(sqlite3.IntegrityError):
        database.add_telemetry(
            999,
            {
                "time": 2.5,
                "position": [10, 20, 0],
                "heading": 90,
                "speed": 4,
                "battery": 95.5,
                "operational": True,
            }
        )

def test_get_mission_speed_metrics(database):
    rover_id = database.add_rover(
        "Confidence",
        0.1,
        5,
        2,
        30,
    )

    mission_id = database.add_mission(
        rover_id,
        "Test Mission",
        35,
    )

    sample1 = {
        "time": 0.0,
        "position": [10, 20, 0],
        "heading": 90,
        "speed": 2,
        "battery": 95.5,
        "operational": True,
    }

    sample2 = {
        "time": 1.0,
        "position": [10, 20, 0],
        "heading": 90,
        "speed": 4,
        "battery": 95.5,
        "operational": True,
    }

    sample3 = {
        "time": 2.0,
        "position": [10, 20, 0],
        "heading": 90,
        "speed": 6,
        "battery": 95.5,
        "operational": True,
    }

    history = (sample1, sample2, sample3)

    database.add_telemetry_history(
        mission_id,
        history
    )

    average_speed, max_speed = database.get_mission_speed_metrics(mission_id)

    assert average_speed == 4.0
    assert max_speed == 6.0

def test_get_mission_battery_consumption(database):
    rover_id = database.add_rover(
        "Confidence",
        0.1,
        5,
        2,
        30,
    )

    mission_id = database.add_mission(
        rover_id,
        "Test Mission",
        35,
    )

    sample1 = {
        "time": 0.0,
        "position": [10, 20, 0],
        "heading": 90,
        "speed": 4,
        "battery": 95,
        "operational": True,
    }

    sample2 = {
        "time": 1.0,
        "position": [10, 20, 0],
        "heading": 90,
        "speed": 4,
        "battery": 90,
        "operational": True,
    }

    sample3 = {
        "time": 2.0,
        "position": [10, 20, 0],
        "heading": 90,
        "speed": 4,
        "battery": 85,
        "operational": True,
    }

    history = (sample1, sample2, sample3)

    database.add_telemetry_history(
        mission_id,
        history
    )

    assert database.get_mission_battery_consumption(mission_id) == 10.0

def test_get_mission_distance_traveled(database):
    rover_id = database.add_rover(
        "Confidence",
        0.1,
        5,
        2,
        30,
    )

    mission_id = database.add_mission(
        rover_id,
        "Test Mission",
        35,
    )

    sample1 = {
        "time": 0.0,
        "position": [0, 0, 0],
        "heading": 90,
        "speed": 4,
        "battery": 95,
        "operational": True,
    }

    sample2 = {
        "time": 1.0,
        "position": [30, 40, 0],
        "heading": 90,
        "speed": 4,
        "battery": 90,
        "operational": True,
    }

    sample3 = {
        "time": 2.0,
        "position": [60, 80, 0],
        "heading": 90,
        "speed": 4,
        "battery": 85,
        "operational": True,
    }

    history = (sample1, sample2, sample3)

    database.add_telemetry_history(
        mission_id,
        history
    )

    assert database.get_mission_distance_traveled(mission_id) == 100.0

def test_simulation_persists_to_database(database):
    rover = Rover("Confidence", 100, [0, 0, 0], 0, True, 0, 0.1, 5, 2, 30)
    mission = Mission("Test Mission", 10)
    simulation = Simulation(rover, mission, 0.1)

    mission.add_command(1, rover.set_speed, 4)

    simulation.run()

    rover_id = database.add_rover(
        rover.rover_name,
        rover.battery_consumption,
        rover.max_speed,
        rover.max_acceleration,
        rover.max_turn_rate
    )
    mission_id = database.add_mission(rover_id, mission.name, mission.duration)

    database.update_mission_result(mission_id, simulation.mission_result)

    database.add_telemetry_history(mission_id, simulation.logger.history)

    rovers = database.get_rovers()
    missions = database.get_missions()
    telemetry = database.get_telemetry()

    assert len(rovers) == 1
    assert len(missions) == 1
    assert len(telemetry) == len(simulation.logger.history)
    assert len(telemetry) == 101

    assert missions[0][4] == simulation.mission_result

    assert telemetry[0][2] == 0.0
    assert telemetry[-1][2] == mission.duration

def test_get_mission_history(database):
    rover_id_1 = database.add_rover(
        "Confidence 1",
        0.1,
        5,
        2,
        30,
    )

    rover_id_2 = database.add_rover(
        "Confidence 2",
        0.1,
        5,
        2,
        30,
    )

    mission_id_1 = database.add_mission(
        rover_id_1,
        "Test Mission 1",
        35,
    )

    mission_id_2 = database.add_mission(
        rover_id_2,
        "Test Mission 2",
        30,
    )

    database.update_mission_result(mission_id_1, "SUCCESS")
    database.update_mission_result(mission_id_2, "FAILED_OBJECTIVE")

    mission_history = database.get_mission_history()

    assert len(mission_history) == 2
    assert len(mission_history[0]) == 5

    assert mission_history[0][0] == mission_id_1
    assert mission_history[0][1] == "Test Mission 1"
    assert mission_history[0][2] == 35
    assert mission_history[0][3] == "SUCCESS"
    assert mission_history[0][4] == "Confidence 1"


    assert mission_history[1][0] == mission_id_2
    assert mission_history[1][1] == "Test Mission 2"
    assert mission_history[1][2] == 30
    assert mission_history[1][3] == "FAILED_OBJECTIVE"
    assert mission_history[1][4] == "Confidence 2"

def test_get_telemetry_by_time_range(database):
    rover_id = database.add_rover(
        "Confidence",
        0.1,
        5,
        2,
        30,
    )

    mission_id = database.add_mission(
        rover_id,
        "Test Mission",
        35,
    )

    sample1 = {
        "time": 0.0,
        "position": [0, 0, 0],
        "heading": 90,
        "speed": 4,
        "battery": 95,
        "operational": True,
    }

    sample2 = {
        "time": 5.0,
        "position": [30, 40, 0],
        "heading": 90,
        "speed": 4,
        "battery": 90,
        "operational": True,
    }

    sample3 = {
        "time": 10.0,
        "position": [60, 80, 0],
        "heading": 90,
        "speed": 4,
        "battery": 85,
        "operational": True,
    }

    sample4 = {
        "time": 15.0,
        "position": [0, 0, 0],
        "heading": 90,
        "speed": 4,
        "battery": 95,
        "operational": True,
    }
    
    sample5 = {
        "time": 20.0,
        "position": [30, 40, 0],
        "heading": 90,
        "speed": 4,
        "battery": 90,
        "operational": True,
    }

    history = [sample1, sample2, sample3, sample4, sample5]

    database.add_telemetry_history(
        mission_id,
        history
    )

    telemetry_range = database.get_telemetry_by_time_range(mission_id, 5, 15)

    assert len(telemetry_range) == 3

    assert telemetry_range[0][2] == 5.0
    assert telemetry_range[1][2] == 10.0
    assert telemetry_range[2][2] == 15.0

def test_add_mission_command(database):
    rover_id = database.add_rover(
        "Confidence",
        0.1,
        5,
        2,
        30,
    )

    mission_id = database.add_mission(
        rover_id,
        "Test Mission",
        35,
    )

    command_id_1 = database.add_mission_command(mission_id, 5.0, "TURN_TO", 90)
    command_id_2 = database.add_mission_command(mission_id, 10.0, "SET_SPEED", 3)

    commands = database.get_mission_commands(mission_id)

    assert len(commands) == 2

    assert commands[0][0] == command_id_1
    assert commands[0][1] == mission_id
    assert commands[0][2] == 5.0
    assert commands[0][3] == "TURN_TO"
    assert commands[0][4] == 90.0

    assert commands[1][0] == command_id_2
    assert commands[1][1] == mission_id
    assert commands[1][2] == 10.0
    assert commands[1][3] == "SET_SPEED"
    assert commands[1][4] == 3.0
