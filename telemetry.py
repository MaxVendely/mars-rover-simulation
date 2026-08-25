import csv
import matplotlib.pyplot as plt

class TelemetryLogger:
    def __init__(self):
        self.history = []

    def record(self, simulation_time, rover):
        self.history.append({
            "time": simulation_time,
            "position": rover.position.copy(),
            "heading": rover.heading,
            "speed": rover.current_speed,
            "battery": rover.battery_percentage,
            "operational": rover.operational_status
        })

    def export_csv(self, filename):
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Timestamp", 
                "Position X", 
                "Position Y", 
                "Position Z", 
                "Heading", 
                "Speed", 
                "Battery Level",
                "Operational"
            ])
            for log in self.history:
                writer.writerow([
                    log["time"], 
                    log["position"][0], 
                    log["position"][1], 
                    log["position"][2], 
                    log["heading"], 
                    log["speed"], 
                    log["battery"],
                    log["operational"]
                ])

    def plot_trajectory(self):
        if not self.history:
            raise ValueError("No telemetry data available to plot.")

        x_positions = []
        y_positions = []

        for log in self.history:
            x_positions.append(log["position"][0])
            y_positions.append(log["position"][1])

        plt.plot(x_positions, y_positions)
        plt.xlabel("Position X (m)")
        plt.ylabel("Position Y (m)")
        plt.title("Rover Trajectory")
        plt.axis("equal")
        plt.grid(True)
        plt.scatter(x_positions[0], y_positions[0], label="Start")
        plt.scatter(x_positions[-1], y_positions[-1], label="End")
        plt.legend()
        plt.show()

    def plot_speed(self):
        if not self.history:
            raise ValueError("No telemetry data available to plot.")

        speed = []
        time = []

        for log in self.history:
            speed.append(log["speed"])
            time.append(log["time"])

        plt.plot(time, speed)
        plt.xlabel("Time (s)")
        plt.ylabel("Speed (m/s)")
        plt.title("Rover Speed")
        plt.grid(True)
        plt.show()