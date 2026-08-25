# Mars Rover Simulation Platform

A modular Mars rover simulation platform built to explore simulation programming, software architecture, testing, telemetry, and multi-system integration.

The project currently features a Python simulation core capable of executing timed mission commands, modeling rover movement and battery consumption, tracking waypoint objectives, recording telemetry, and evaluating mission outcomes.

## Project Status

**Phase 1 — Python Simulation Core: Complete**

The Python simulation core serves as the validated prototype for a larger multi-technology system. Future phases will introduce persistent mission data with SQL, a web-based mission control interface, Docker containerization, a C++ simulation engine, and Unity 3D visualization.

## Features

### Rover Simulation
- 2D position and heading simulation
- Forward and reverse movement
- Target-speed control with acceleration and deceleration limits
- Maximum speed and turn-rate constraints
- Shortest-path heading changes across 0°/360°
- Distance-based battery consumption and depletion
- Operational-state restrictions

### Mission System
- Configurable mission duration and simulation timestep
- Timed rover commands
- Exact command execution between timestep boundaries
- Multiple commands within a single timestep
- Sequential waypoint objectives with configurable tolerance
- Mission outcome evaluation
- Deterministic simulation reruns from the original rover state

### Telemetry and Visualization
- Timestamped rover-state history
- Historical state snapshots
- CSV telemetry export
- Rover trajectory visualization
- Speed-over-time visualization

### Testing and Reliability
- Automated testing with pytest
- Tests for rover dynamics, mission behavior, simulation timing, and telemetry
- Boundary and invalid-input validation
- Tests for battery depletion, heading wrapping, waypoint behavior, command timing, and deterministic reruns

## Architecture

The Phase 1 simulation is organized around four primary components:

### `Rover`
Models the physical state and behavior of the rover, including position, heading, speed, acceleration, turning, battery consumption, and operational status.

### `Mission`
Defines mission duration, scheduled commands, and sequential waypoint objectives.

### `Simulation`
Coordinates the mission and rover over time. It advances the simulation in discrete timesteps while ensuring commands scheduled between timestep boundaries execute at their exact requested times. It also tracks waypoint progress, determines mission results, and supports deterministic reruns.

### `TelemetryLogger`
Records timestamped snapshots of rover state throughout a simulation. Telemetry can be exported to CSV or visualized as trajectory and speed plots.

The current data flow is:

```text
main.py
  |
  +--> Rover
  |
  +--> Mission
  |
  +--> Simulation
         |
         +--> reads Mission commands/objectives
         |
         +--> updates Rover state
         |
         +--> records state through TelemetryLogger
                              |
                              +--> CSV
                              +--> Matplotlib plots
```

`main.py` serves as the current application entry point and contains an example mission demonstrating the simulation system.

## Getting Started

### Prerequisites

- Python 3
- pip

### Installation

Clone the repository and navigate to the project directory:

```bash
git clone <repository-url>
cd <repository-directory>
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Running the Demo

Run the example Crater Survey mission:

```bash
python main.py
```

The demo will:

- Run the rover mission simulation
- Print the mission summary
- Export telemetry to `output/mission.csv`
- Display the rover trajectory
- Display rover speed over time

### Running Tests

Run the complete automated test suite with:

```bash
pytest
```

## Key Design Decisions

### Discrete Timestep Simulation
The simulation advances using a configurable fixed timestep. Commands scheduled between timestep boundaries are executed at their exact requested times rather than being delayed until the next simulation step.

### Separation of Responsibilities
Rover behavior, mission definition, simulation orchestration, and telemetry are separated into distinct components. This keeps simulation logic easier to test and allows individual parts of the system to evolve independently.

### Deterministic Reruns
A `Simulation` stores the rover's initial state and restores it when rerun. Under identical conditions, repeated simulations therefore produce identical results.

### Sequential Waypoint Objectives
Missions can define ordered waypoint objectives. The simulation tracks waypoint completion throughout the mission and includes objective completion when determining mission success.

### Telemetry Snapshots
Telemetry records copies of mutable rover state rather than references to the rover's live state. Historical telemetry therefore remains unchanged as the simulation continues.

### Python as the Prototype Layer
The simulation core was initially implemented and tested in Python to establish correct behavior quickly. Later phases will use the validated Python implementation as a reference as appropriate simulation responsibilities are migrated to C++.

## Project Structure

```text
Mars Rover/
├── main.py
├── mission.py
├── rover.py
├── simulation.py
├── telemetry.py
├── requirements.txt
├── PROJECT_PLAN.md
├── tests/
│   ├── test_mission.py
│   ├── test_rover.py
│   ├── test_simulation.py
│   └── test_telemetry.py
└── output/
    └── mission.csv
```

`output/` contains generated simulation data and is excluded from version control.

## Roadmap

The Python simulation core is the first phase of a larger Mars Rover Simulation Platform.

- [x] **Phase 1 — Python Simulation Core**
  - Rover dynamics and battery behavior
  - Mission commands and waypoint objectives
  - Simulation orchestration
  - Telemetry and visualization
  - Automated testing

- [ ] **Phase 2 — SQL and Persistent Mission Data**
  - Persist missions, rover data, telemetry, and mission events
  - Design a relational data model
  - Query and analyze historical mission data

- [ ] **Phase 3 — Web Mission Control**
  - Backend API
  - Browser-based mission control dashboard
  - Live rover status and telemetry

- [ ] **Phase 4 — Docker**
  - Containerize application services
  - Reproducible multi-service development environment

- [ ] **Phase 5 — C++ Simulation Engine**
  - Migrate appropriate computational simulation responsibilities to C++
  - Validate behavior against the Python prototype
  - Benchmark performance where appropriate

- [ ] **Phase 6 — Unity 3D Visualization**
  - Real-time Mars environment
  - Rover and mission visualization
  - Integration with simulation state

- [ ] **Phase 7 — Integration and Portfolio Polish**
  - End-to-end system integration
  - Documentation and architecture diagrams
  - Demo media and final portfolio presentation