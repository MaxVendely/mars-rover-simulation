import pytest

from database import Database

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