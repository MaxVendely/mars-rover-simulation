# Mars Rover Simulation Platform

A modular Mars rover simulation platform built to explore simulation programming, software architecture, testing, telemetry, relational data, and multi-system integration.

The project currently combines a tested Python simulation core with a SQLite persistence layer. It can execute timed mission commands, model rover movement and battery consumption, track waypoint objectives, record telemetry, evaluate mission outcomes, and persist complete mission histories for later querying and analysis.

## Project Status

**Phase 1 — Python Simulation Core: Complete**

**Phase 2 — SQL and Persistent Mission Data: Complete**

**Phase 3 — Web Mission Control: Next**

The Python simulation core serves as the validated foundation for a larger multi-technology system. SQLite now provides persistent storage for rover configurations, missions, telemetry, and mission commands.

Future phases will introduce a web-based mission control interface, Docker containerization, a C++ simulation engine, and Unity 3D visualization.

## Features

### Rover Simulation

* 2D position and heading simulation
* Forward and reverse movement
* Target-speed control with acceleration and deceleration limits
* Maximum speed and turn-rate constraints
* Shortest-path heading changes across 0°/360°
* Distance-based battery consumption and depletion
* Operational-state restrictions

### Mission System

* Configurable mission duration and simulation timestep
* Timed rover commands
* Exact command execution between timestep boundaries
* Multiple commands within a single timestep
* Sequential waypoint objectives with configurable tolerance
* Mission outcome evaluation
* Deterministic simulation reruns from the original rover state

### Telemetry and Visualization

* Timestamped rover-state history
* Historical state snapshots
* CSV telemetry export
* Rover trajectory visualization
* Speed-over-time visualization
* Persistent telemetry histories in SQLite
* Telemetry queries over selected mission time ranges

### Persistent Mission Data

* SQLite relational database
* Persistent rover configurations
* Mission metadata and results
* Complete telemetry histories
* Mission command persistence
* Foreign-key enforcement between related records
* Mission history queries using relational joins
* Indexed telemetry and mission-command retrieval

### Mission Analytics

Historical telemetry can be queried to calculate:

* Distance traveled
* Battery consumed
* Average speed
* Maximum speed
* Mission duration and result
* Rover associated with each mission

Speed analytics use speed magnitude so reverse movement is represented correctly.

### Testing and Reliability

* Automated testing with pytest
* Tests for rover dynamics, mission behavior, simulation timing, telemetry, and database behavior
* Boundary and invalid-input validation
* Foreign-key constraint testing
* Relational query and analytics testing
* Mission-command persistence testing
* Unsupported-command validation
* End-to-end simulation-to-database integration testing

## Architecture

The system currently contains a Python simulation layer and a SQLite persistence layer.

### `Rover`

Models the physical state and behavior of the rover, including position, heading, speed, acceleration, turning, battery consumption, and operational status.

### `Mission`

Defines mission duration, scheduled commands, and sequential waypoint objectives.

### `Simulation`

Coordinates the mission and rover over time. It advances the simulation in discrete timesteps while ensuring commands scheduled between timestep boundaries execute at their exact requested times. It also tracks waypoint progress, determines mission results, and supports deterministic reruns.

### `TelemetryLogger`

Records timestamped snapshots of rover state throughout a simulation. Telemetry can be exported to CSV, visualized as trajectory and speed plots, or persisted to the database.

### `Database`

Provides the SQLite persistence layer for rover configurations, missions, telemetry, mission commands, and historical mission analytics.

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
                              |
                              v
                         Database
                              |
                              v
                           SQLite
                    +---------+---------+
                    |         |         |
                  Rovers   Missions  Telemetry
                                      Commands
```

`main.py` serves as the current application entry point and contains an example Crater Survey mission demonstrating the simulation and persistence systems.

## Database Design

The SQLite schema currently contains four primary tables:

### `rovers`

Stores rover identity and simulation configuration, including battery consumption, maximum speed, acceleration, and turn rate.

### `missions`

Stores mission metadata, duration, result, and the rover associated with the mission.

### `telemetry`

Stores timestamped rover state throughout each mission, including position, heading, speed, battery level, and operational status.

### `mission_commands`

Stores supported mission commands in a SQL-safe representation, including execution time, command type, and value.

Foreign keys enforce the relationships between rovers, missions, telemetry, and commands.

Composite indexes on mission and time fields support the application's primary telemetry and command query patterns.

## Getting Started

### Prerequisites

* Python 3
* pip
* SQLite 3

### Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/MaxVendely/mars-rover-simulation.git
cd mars-rover-simulation
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

* Run the rover mission simulation
* Print the mission summary
* Persist mission data and telemetry to SQLite
* Export telemetry to `output/mission.csv`
* Display the rover trajectory
* Display rover speed over time

### Running Tests

Run the complete automated test suite with:

```bash
python -m pytest
```

The test suite covers the simulation core, mission behavior, telemetry, database persistence, relational constraints, analytics, command persistence, and simulation-to-database integration.

## Key Design Decisions

### Discrete Timestep Simulation

The simulation advances using a configurable fixed timestep. Commands scheduled between timestep boundaries are executed at their exact requested times rather than being delayed until the next simulation step.

### Separation of Responsibilities

Rover behavior, mission definition, simulation orchestration, telemetry, and persistence are separated into distinct components. This keeps individual systems easier to test and allows them to evolve independently.

### Deterministic Reruns

A `Simulation` stores the rover's initial state and restores it when rerun. Under identical conditions, repeated simulations therefore produce identical results.

### SQLite Persistence

SQLite provides relational persistence without requiring a separate database service during the current stage of development. Rover configurations, missions, telemetry, and commands can be stored and queried after a simulation completes.

### Runtime and Persistence Command Representations

Mission commands remain Python callables during simulation execution. A persistence adapter translates supported commands into SQL-safe command types such as `TURN_TO` and `SET_SPEED`.

This preserves the existing simulation design while allowing commands to be stored relationally without coupling runtime behavior directly to the database representation.

### Query-Oriented Indexing

Composite indexes are defined around the application's actual access patterns. Telemetry uses an index on `(mission_id, time)`, while mission commands use `(mission_id, execute_time)`.

SQLite query-plan inspection is used to verify index behavior rather than assuming an index improves a query.

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
├── database.py
├── schema.sql
├── requirements.txt
├── tests/
│   ├── test_database.py
│   ├── test_mission.py
│   ├── test_rover.py
│   ├── test_simulation.py
│   └── test_telemetry.py
└── output/
    └── mission.csv
```

output/ contains generated simulation data and is excluded from version control.

## Roadmap

The project is being developed as one evolving simulation platform, with each phase introducing technology that serves a specific architectural purpose.

* [x] **Phase 1 — Python Simulation Core**

  * Rover dynamics and battery behavior
  * Mission commands and waypoint objectives
  * Simulation orchestration
  * Telemetry and visualization
  * Automated testing

* [x] **Phase 2 — SQL and Persistent Mission Data**

  * Relational SQLite schema
  * Rover, mission, telemetry, and command persistence
  * Foreign-key relationships
  * Historical mission queries and joins
  * Mission analytics
  * Query-oriented indexing
  * Simulation-to-database integration testing

* [ ] **Phase 3 — Web Mission Control**

  * FastAPI backend
  * Browser-based mission control dashboard
  * Rover and mission API endpoints
  * Live rover status and telemetry
  * Historical mission data and analytics

* [ ] **Phase 4 — Docker**

  * Containerize application services
  * Reproducible multi-service development environment

* [ ] **Phase 5 — C++ Simulation Engine**

  * Migrate appropriate computational simulation responsibilities to C++
  * Validate behavior against the Python prototype
  * Benchmark performance where appropriate

* [ ] **Phase 6 — Unity 3D Visualization**

  * Real-time Mars environment
  * Rover and mission visualization
  * Integration with simulation state

* [ ] **Phase 7 — Integration and Portfolio Polish**

  * End-to-end system integration
  * Documentation and architecture diagrams
  * Demo media and final portfolio presentation