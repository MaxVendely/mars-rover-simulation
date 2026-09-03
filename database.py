import math
import sqlite3


class Database:
    def __init__(self, database_path="mars_rover.db"):
        self.database_path = database_path

    def connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.execute("PRAGMA foreign_keys = ON;")
        return connection
    
    def initialize(self, schema_path="schema.sql"):
        with self.connect() as connection:
            with open(schema_path, "r") as schema_file:
                connection.executescript(schema_file.read())

    def add_rover(
            self,
            name,
            battery_consumption,
            max_speed,
            max_acceleration,
            max_turn_rate,
    ):
        existing_rover = self.get_rover_by_name(name)

        if existing_rover is not None:
            return existing_rover[0]

        with self.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO rovers (
                    name,
                    battery_consumption,
                    max_speed,
                    max_acceleration,
                    max_turn_rate
                )
                VALUES (?, ?, ?, ?, ?);""",
                (
                    name,
                    battery_consumption,
                    max_speed,
                    max_acceleration,
                    max_turn_rate,
                ),
            )

            return cursor.lastrowid
        
    def get_rovers(self):
        with self.connect() as connection:
            cursor = connection.execute(
                """
                SELECT
                    id,
                    name,
                    battery_consumption,
                    max_speed,
                    max_acceleration,
                    max_turn_rate
                FROM rovers;
                """
            )

            return cursor.fetchall()
        
    def get_rover_by_name(self, name):
        with self.connect() as connection:
            cursor = connection.execute(
                """
                SELECT id
                FROM rovers
                WHERE name = ?;
                """,
                (name,),
            )

            return cursor.fetchone()
        
    def add_mission(self, rover_id, name, duration):
        with self.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO missions(
                    rover_id,
                    name,
                    duration
                )
                VALUES (?, ?, ?)
                """,
                (
                    rover_id,
                    name,
                    duration,
                )
            )

            return cursor.lastrowid

    def get_missions(self):
        with self.connect() as connection:
            cursor = connection.execute(
                """
                SELECT
                    id,
                    rover_id,
                    name,
                    duration,
                    result
                FROM missions;
                """
            )

            return cursor.fetchall()
        
    def update_mission_result(self, mission_id, result):
        with self.connect() as connection:
            connection.execute(
                """
                UPDATE missions
                SET result = ?
                WHERE id = ?
                """,
                (
                    result,
                    mission_id,
                )
            )

    def add_telemetry(self, mission_id, sample):
        with self.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO telemetry(
                    mission_id,
                    time,
                    position_x,
                    position_y,
                    position_z,
                    heading,
                    speed,
                    battery,
                    operational
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    mission_id,
                    sample["time"],
                    sample["position"][0],
                    sample["position"][1],
                    sample["position"][2],
                    sample["heading"],
                    sample["speed"],
                    sample["battery"],
                    int(sample["operational"]),
                )
            )

            return cursor.lastrowid

    def get_telemetry(self):
        with self.connect() as connection:
            cursor = connection.execute(
                """
                SELECT
                    id,
                    mission_id,
                    time,
                    position_x,
                    position_y,
                    position_z,
                    heading,
                    speed,
                    battery,
                    operational
                FROM telemetry;
                """
            )

            return cursor.fetchall()
        
    def add_telemetry_history(self, mission_id, history):
        with self.connect() as connection:
            for sample in history:
                connection.execute(
                    """
                    INSERT INTO telemetry(
                        mission_id,
                        time,
                        position_x,
                        position_y,
                        position_z,
                        heading,
                        speed,
                        battery,
                        operational
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        mission_id,
                        sample["time"],
                        sample["position"][0],
                        sample["position"][1],
                        sample["position"][2],
                        sample["heading"],
                        sample["speed"],
                        sample["battery"],
                        int(sample["operational"]),
                    )
                )

    def get_mission_speed_metrics(self, mission_id):
        with self.connect() as connection:
            cursor = connection.execute(
                """
                SELECT
                    AVG(speed),
                    MAX(speed)
                FROM telemetry
                WHERE mission_id = ?;
                """,
                (mission_id,),
            )

            return cursor.fetchone()

    def get_mission_battery_consumption(self, mission_id):
            with self.connect() as connection:
                cursor = connection.execute(
                    """
                    SELECT
                        (
                            SELECT battery
                            FROM telemetry
                            WHERE mission_id = ?
                            ORDER BY time ASC
                            LIMIT 1
                        )
                        -
                        (
                            SELECT battery
                            FROM telemetry
                            WHERE mission_id = ?
                            ORDER BY time DESC
                            LIMIT 1
                        )
                    """,
                    (mission_id, mission_id,),
                )
    
                return cursor.fetchone()[0]

    def get_mission_positions(self, mission_id):
        with self.connect() as connection:
            cursor = connection.execute(
                """
                SELECT
                    position_x,
                    position_y
                FROM telemetry
                WHERE mission_id = ?
                ORDER BY time ASC;
                """,
                (mission_id,),
            )

            return cursor.fetchall()

    def get_mission_distance_traveled(self, mission_id):
        positions = self.get_mission_positions(mission_id)

        total_distance = 0.0

        for index in range(1, len(positions)):
            previous_x, previous_y = positions[index - 1]
            current_x, current_y = positions[index]

            total_distance += math.hypot(
                current_x - previous_x,
                current_y - previous_y
            )

        return total_distance