from telemetry import TelemetryLogger

class Simulation:
    def __init__(self, rover, mission, time_step):
        if time_step <= 0:
            raise ValueError("Time step must be greater than 0.")
        self.rover = rover
        self.mission = mission
        self.time_step = time_step
        self.current_time = 0
        self.logger = TelemetryLogger()
        self.executed_commands = set()
        self.mission_successful = False
        self.mission_result = None

        # Preserve the initial rover state so repeated runs can reset.
        self.initial_position = rover.position.copy()
        self.initial_heading = rover.heading
        self.initial_battery = rover.battery_percentage
        self.initial_speed = rover.current_speed
        self.initial_operational_status = rover.operational_status
        self.initial_target_speed = rover.target_speed
        self.initial_target_heading = rover.target_heading
        self.has_run = False

    def run(self):
        if self.has_run:
            self.reset()

        self.logger.record(self.current_time, self.rover)
        self.update_mission_progress()

        self.execute_commands(self.current_time, self.current_time)
        steps = int(self.mission.duration / self.time_step)

        for step in range(steps):
            step_end = (step + 1) * self.time_step
            self.simulate_timestep(step_end)

        if self.mission.duration - self.current_time > 1e-10:
            self.simulate_timestep(self.mission.duration)

        self.mission_result = self.determine_mission_result()
        self.mission_successful = self.mission_result == "SUCCESS"

        self.has_run = True

    def simulate_timestep(self, end_time):
        upcoming_commands = self.get_commands_between(
            self.current_time,
            end_time
        )

        for index, command in upcoming_commands:
            execute_time, function, args = command

            self.rover.update(execute_time - self.current_time)
            self.current_time = execute_time
            self.update_mission_progress()
            function(*args)
            self.executed_commands.add(index)

        self.rover.update(end_time - self.current_time)
        self.current_time = end_time
        self.update_mission_progress()
        self.logger.record(self.current_time, self.rover)

    def get_commands_between(self, start_time, end_time):
        upcoming_commands = []

        for index, command in enumerate(self.mission.commands):
            execute_time, function, args = command

            if (
                index not in self.executed_commands
                and start_time < execute_time <= end_time
            ):
                upcoming_commands.append((index, command))

        upcoming_commands.sort(key=lambda item: item[1][0])

        return upcoming_commands

    def execute_commands(self, start_time, end_time):
        for index, command in enumerate(self.mission.commands):
            execute_time, function, args = command

            if (
                index not in self.executed_commands
                and execute_time <= end_time
                and (execute_time > start_time or execute_time == 0)
            ):
                function(*args)
                self.executed_commands.add(index)

    def update_mission_progress(self):
        if self.mission.is_current_waypoint_reached(self.rover.position):
            self.mission.complete_current_waypoint()

    def determine_mission_result(self):
        if abs(self.current_time - self.mission.duration) >= 1e-10:
            return "INCOMPLETE"

        if not self.rover.operational_status:
            return "FAILED_SYSTEM"

        if self.rover.battery_percentage <= 0:
            return "FAILED_BATTERY"

        if not self.mission.are_waypoints_complete():
            return "FAILED_OBJECTIVE"

        return "SUCCESS"

    def get_summary(self):
        return {
            "mission": self.mission.name,
            "result": self.mission_result,
            "duration": self.current_time,
            "final_position": self.rover.position.copy(),
            "final_heading": self.rover.heading,
            "final_battery": self.rover.battery_percentage
        }

    def reset(self):
        self.rover.position = self.initial_position.copy()
        self.rover.heading = self.initial_heading
        self.rover.battery_percentage = self.initial_battery
        self.rover.current_speed = self.initial_speed
        self.rover.operational_status = self.initial_operational_status
        self.rover.target_speed = self.initial_target_speed
        self.rover.target_heading = self.initial_target_heading

        self.mission.current_waypoint_index = 0

        self.current_time = 0
        self.logger = TelemetryLogger()
        self.executed_commands.clear()
        self.mission_successful = False
        self.mission_result = None