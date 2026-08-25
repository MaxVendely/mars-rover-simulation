import math

class Mission:
    def __init__(self, name, duration):
        if duration <= 0:
            raise ValueError("Mission duration must be greater than 0.")
        self.name = name
        self.duration = duration
        self.commands = []
        self.waypoints = []
        self.current_waypoint_index = 0

    def add_command(self, execute_time, function, *args):
        if execute_time < 0 or execute_time > self.duration:
            raise ValueError("Command execution time must be within mission duration.")
    
        self.commands.append((execute_time, function, args))

    def add_waypoint(self, x, y):
        self.waypoints.append([x, y])

    def get_current_waypoint(self):
        if self.current_waypoint_index >= len(self.waypoints):
            return None
        
        return self.waypoints[self.current_waypoint_index]
    
    def complete_current_waypoint(self):
        if self.current_waypoint_index < len(self.waypoints):
            self.current_waypoint_index += 1

    def is_current_waypoint_reached(self, rover_position, tolerance=0.5):
        waypoint = self.get_current_waypoint()
        if waypoint is None:
            return False
        
        distance = math.hypot(rover_position[0] - waypoint[0], rover_position[1] - waypoint[1])

        return distance <= tolerance
    
    def are_waypoints_complete(self):
        return self.current_waypoint_index >= len(self.waypoints)