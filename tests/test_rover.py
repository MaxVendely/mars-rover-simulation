from rover import Rover
import pytest

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

def test_move(confidence):
    # Arrange
    time_step = 0.1
    steps = 100

    # Act
    for _ in range(steps):
        confidence.update(time_step)

    # Assert
    assert confidence.position[0] == 50

def test_accelerate(confidence):
    # Arrange
    confidence.current_speed = 0    
    confidence.set_speed(5)

    time_step = 0.1
    steps = 10

    # Act
    for _ in range(steps):
        confidence.update(time_step)

    # Assert
    assert confidence.current_speed == pytest.approx(2)

def test_battery(confidence):
    # Arrange
    time_step = 0.1
    steps = 2000

    # Act
    for _ in range(steps):
        confidence.update(time_step)

    # Assert
    assert confidence.battery_percentage == pytest.approx(0, abs=1e-9)

def test_battery_limits_movement(confidence):
    # Arrange
    time_step = 0.1
    steps = 3000

    # Act
    for _ in range(steps):
        confidence.update(time_step)

    # Assert
    assert confidence.position[0] == pytest.approx(1000)
    assert confidence.battery_percentage == pytest.approx(0, abs=1e-9)

def test_turn_to(confidence):
    # Arrange
    time_step = 0.1
    steps = 100
    confidence.heading = 350
    confidence.turn_to(10)

    # Act
    for _ in range(steps):
        confidence.update(time_step)

    # Assert
    assert confidence.heading == 10

def test_turn_to_negative(confidence):
    # Arrange
    time_step = 0.1
    steps = 100
    confidence.heading = 10
    confidence.turn_to(350)

    # Act
    for _ in range(steps):
        confidence.update(time_step)

    # Assert
    assert confidence.heading == 350

def test_turn_to_shortest_path_positive(confidence):
    # Arrange
    confidence.heading = 350
    confidence.turn_to(10)

    # Act
    confidence.update(0.1)

    # Assert
    assert confidence.heading == 353

def test_heading_wrap(confidence):
    # Arrange
    confidence.heading = 350
    confidence.target_heading = 350

    # Act
    confidence.turn_to(20)
    confidence.update_heading(1)

    # Assert
    assert confidence.heading == 20

def test_turn_to_shortest_path_negative(confidence):
    # Arrange
    confidence.heading = 10
    confidence.turn_to(350)

    # Act
    confidence.update(0.1)

    # Assert
    assert confidence.heading == 7

def test_battery_depleted_prevents_actuation(confidence):
    # Arrange
    confidence.battery_percentage = 0
    confidence.current_speed = 0
    confidence.heading = 0

    confidence.set_speed(5)
    confidence.turn_to(90)

    # Act
    confidence.update(1)

    # Assert
    assert confidence.target_speed == 5
    assert confidence.target_heading == 90

    assert confidence.current_speed == 0
    assert confidence.heading == 0
    assert confidence.position == [0, 0, 0]

def test_negative_battery():
    with pytest.raises(ValueError):
        Rover(
            rover_name="Failure",
            battery_percentage=-1,
            position=[0, 0, 0],
            heading=90,
            operational_status=True,
            current_speed=5,
            battery_consumption=0.1,
            max_speed=5,
            max_acceleration=2,
            max_turn_rate=30
        )

def test_excessive_battery():
    with pytest.raises(ValueError):
        Rover(
            rover_name="Failure",
            battery_percentage=101,
            position=[0, 0, 0],
            heading=90,
            operational_status=True,
            current_speed=5,
            battery_consumption=0.1,
            max_speed=5,
            max_acceleration=2,
            max_turn_rate=30
        )


def test_valid_battery_consumption():
    confidence = Rover(
        rover_name="Confidence",
        battery_percentage=100,
        position=[0, 0, 0],
        heading=90,
        operational_status=True,
        current_speed=5,
        battery_consumption=0,
        max_speed=5,
        max_acceleration=2,
        max_turn_rate=30
    )

    assert confidence.battery_consumption == 0

    with pytest.raises(ValueError):
        Rover(
            rover_name="Failure",
            battery_percentage=100,
            position=[0, 0, 0],
            heading=90,
            operational_status=True,
            current_speed=5,
            battery_consumption=-1,
            max_speed=5,
            max_acceleration=2,
            max_turn_rate=30
        )

def test_zero_max_speed():
    with pytest.raises(ValueError):
        Rover(
            rover_name="Failure",
            battery_percentage=100,
            position=[0, 0, 0],
            heading=90,
            operational_status=True,
            current_speed=5,
            battery_consumption=1,
            max_speed=0,
            max_acceleration=2,
            max_turn_rate=30
        )

def test_negative_max_speed():
    with pytest.raises(ValueError):
        Rover(
            rover_name="Failure",
            battery_percentage=100,
            position=[0, 0, 0],
            heading=90,
            operational_status=True,
            current_speed=5,
            battery_consumption=1,
            max_speed=-1,
            max_acceleration=2,
            max_turn_rate=30
        )

def test_zero_max_acceleration():
    with pytest.raises(ValueError):
        Rover(
            rover_name="Failure",
            battery_percentage=100,
            position=[0, 0, 0],
            heading=90,
            operational_status=True,
            current_speed=5,
            battery_consumption=1,
            max_speed=5,
            max_acceleration=0,
            max_turn_rate=30
        )

def test_negative_max_acceleration():
    with pytest.raises(ValueError):
        Rover(
            rover_name="Failure",
            battery_percentage=100,
            position=[0, 0, 0],
            heading=90,
            operational_status=True,
            current_speed=5,
            battery_consumption=1,
            max_speed=5,
            max_acceleration=-1,
            max_turn_rate=30
        )

def test_zero_turn_rate():
    with pytest.raises(ValueError):
        Rover(
            rover_name="Failure",
            battery_percentage=100,
            position=[0, 0, 0],
            heading=90,
            operational_status=True,
            current_speed=5,
            battery_consumption=1,
            max_speed=5,
            max_acceleration=2,
            max_turn_rate=0
        )

def test_negative_turn_rate():
    with pytest.raises(ValueError):
        Rover(
            rover_name="Failure",
            battery_percentage=100,
            position=[0, 0, 0],
            heading=90,
            operational_status=True,
            current_speed=5,
            battery_consumption=1,
            max_speed=5,
            max_acceleration=2,
            max_turn_rate=-30
        )

def test_excessive_initial_speed():
    with pytest.raises(ValueError):
        Rover(
            rover_name="Failure",
            battery_percentage=100,
            position=[0, 0, 0],
            heading=90,
            operational_status=True,
            current_speed=6,
            battery_consumption=1,
            max_speed=5,
            max_acceleration=2,
            max_turn_rate=30
        )

def test_excessive_negative_initial_speed():
    with pytest.raises(ValueError):
        Rover(
            rover_name="Failure",
            battery_percentage=100,
            position=[0, 0, 0],
            heading=90,
            operational_status=True,
            current_speed=-6,
            battery_consumption=1,
            max_speed=5,
            max_acceleration=2,
            max_turn_rate=30
        )
