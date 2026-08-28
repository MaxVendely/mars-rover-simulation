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
        
    def update_mission_result(self, mission_id, result):
        with self.connect() as connection:
            cursor = connection.execute(
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