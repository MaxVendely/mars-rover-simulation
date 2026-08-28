from rover import Rover
from simulation import Simulation
from mission import Mission
from pathlib import Path
from database import Database


def main():
    optimism = Rover(
        rover_name="Optimism",
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

    mission = Mission(
        name="Crater Survey Run",
        duration=35
    )

    # Mission objectives
    mission.add_waypoint(0, 16)
    mission.add_waypoint(12, 28)
    mission.add_waypoint(28, 22)
    mission.add_waypoint(28, 3)
    mission.add_waypoint(-2, -6)

    # Launch north
    mission.add_command(0, optimism.set_speed, 4)
    # Sweep east across the survey area
    mission.add_command(6, optimism.turn_to, 90)
    # Slow down for a tighter maneuver
    mission.add_command(12, optimism.set_speed, 2)
    # Turn south toward the crater
    mission.add_command(14, optimism.turn_to, 180)
    # Accelerate through the crater corridor
    mission.add_command(21, optimism.set_speed, 5)
    # Turn west for the return sweep
    mission.add_command(24, optimism.turn_to, 270)
    # Brake near the final survey area
    mission.add_command(30, optimism.set_speed, 0)
    # Face north at mission end
    mission.add_command(32, optimism.turn_to, 0)

    simulation = Simulation(optimism, mission, 0.1)
    simulation.run()


    database = Database()
    database.initialize()

    rover_id = database.add_rover(
        optimism.rover_name,
        optimism.battery_consumption,
        optimism.max_speed,
        optimism.max_acceleration,
        optimism.max_turn_rate
    )

    mission_id = database.add_mission(
        rover_id,
        mission.name,
        mission.duration
    )

    database.update_mission_result(
        mission_id,
        simulation.mission_result
    )

    database.add_telemetry_history(
        mission_id,
        simulation.logger.history
    )


    Path("output").mkdir(exist_ok=True)
    simulation.logger.export_csv("output/mission.csv")

    print(simulation.get_summary())
    simulation.logger.plot_trajectory()
    simulation.logger.plot_speed()

if __name__ == "__main__":
    main()