import math

class Rover:
    def __init__(self, rover_name, battery_percentage, position, heading, operational_status, current_speed, battery_consumption, max_speed, max_acceleration, max_turn_rate):
        if not 0 <= battery_percentage <= 100:
            raise ValueError("Battery level must be in the range 0-100.")
        if battery_consumption < 0:
            raise ValueError("Battery consumption cannot be negative.")
        if max_speed <= 0:
            raise ValueError("Max speed must be greater than 0.")
        if max_acceleration <= 0:
            raise ValueError("Max acceleration must be greater than 0.")
        if max_turn_rate <= 0:
            raise ValueError("Max turn rate must be greater than 0.")
        if abs(current_speed) > max_speed:
            raise ValueError("Current speed cannot exceed max speed.")
        self.rover_name = rover_name
        self.battery_percentage = battery_percentage
        self.position = position.copy()
        self.heading = heading % 360
        self.operational_status = operational_status
        self.current_speed = current_speed
        self.battery_consumption = battery_consumption
        self.max_speed = max_speed
        self.target_speed = current_speed
        self.max_acceleration = max_acceleration
        self.target_heading = heading
        self.max_turn_rate = max_turn_rate

    def update(self, elapsed_time):
        self.accelerate(elapsed_time)
        self.update_heading(elapsed_time)
        self.move(elapsed_time)
    
    def move(self, elapsed_time):
        if self.battery_percentage <= 0 or not self.operational_status:
            return

        distance_to_travel = self.current_speed * elapsed_time

        if self.battery_consumption == 0:
            maximum_distance = math.inf
        else:
            maximum_distance = self.battery_percentage / self.battery_consumption

        if maximum_distance < abs(distance_to_travel):
            distance_to_travel = math.copysign(maximum_distance, distance_to_travel)

        self.battery_percentage -= self.battery_consumption * abs(distance_to_travel)
        x_distance = math.sin(math.radians(self.heading)) * distance_to_travel
        y_distance = math.cos(math.radians(self.heading)) * distance_to_travel
        self.position[0] += x_distance
        self.position[1] += y_distance

    def set_speed(self, speed):
        if abs(speed) <= self.max_speed:
            self.target_speed = round(speed, 2)
        else:
            self.target_speed = math.copysign(self.max_speed, speed)

    def accelerate(self, elapsed_time):
        if self.battery_percentage <= 0 or not self.operational_status:
            return
        speed_change = self.max_acceleration * elapsed_time
        if abs(self.target_speed - self.current_speed) < speed_change:
            speed_change = abs(self.target_speed - self.current_speed)
        
        speed_change = math.copysign(speed_change, self.target_speed - self.current_speed)

        self.current_speed += speed_change

    def turn_to(self, heading):
        self.target_heading = heading % 360

    def update_heading(self, elapsed_time):
        if self.battery_percentage <= 0 or not self.operational_status:
            return
        heading_change = self.max_turn_rate * elapsed_time
        desired_change = (self.target_heading - self.heading) % 360

        if desired_change > 180:
            desired_change -= 360

        if abs(desired_change) < heading_change:
            heading_change = abs(desired_change)
            
        heading_change = math.copysign(heading_change, desired_change)

        self.heading += heading_change
        self.heading %= 360