# Mars Rover Simulation Platform --- Project Plan

## Project Goal

Build a portfolio-quality Mars rover simulation platform that
demonstrates practical software engineering across multiple technologies
while filling skill gaps relevant to software, simulation, defense,
medical, and emerging-technology roles.

The guiding principle is **one evolving project, not a collection of
disconnected tutorials**. Every major technology should be introduced
because it solves a real architectural problem.

## Portfolio Story

By the end of the project, the system should demonstrate:

-   Python application and simulation development
-   Automated testing and debugging
-   Telemetry collection and data analysis
-   SQL database design and querying
-   Web API and frontend development
-   Docker/containerized development
-   C++ systems and simulation programming
-   Unity 3D real-time visualization
-   Multi-component system integration
-   Technical documentation and architecture decisions

Target final architecture:

``` text
Unity 3D Visualization
        |
        v
Web / API Layer
        |
        +------ SQL Database
        |
        v
Python Mission / Application Layer
        |
        v
C++ Simulation Engine
        |
        v
Rover / Environment / Sensors
```

Docker will be used to package and orchestrate appropriate services.

------------------------------------------------------------------------

## Phase 1 --- Python Simulation Core

**Estimated total:** 7–10 focused development days  
**Actual:** 7 focused business-day sessions  
**Status:** Complete

### Purpose

Build a reliable simulation foundation while strengthening core Python
and software-engineering skills.

### Current implementation

-   `Rover` class
-   Position and heading
-   Forward and reverse movement
-   Target speed
-   Acceleration and deceleration
-   Maximum speed
-   Maximum acceleration
-   Turn-rate limits
-   Shortest-path heading updates
-   Battery consumption and depletion behavior
-   Simulation timestep loop
-   Telemetry logging
-   CSV telemetry export
-   Matplotlib telemetry visualization
-   pytest test suite

### Current design decisions

-   Position represented as `[x, y, z]`
-   Heading represented in degrees and normalized to `[0, 360)`
-   Movement:
    -   `x += sin(heading) * distance`
    -   `y += cos(heading) * distance`
-   Reverse movement is supported
-   Rover decelerates to zero before reversing direction
-   Speed commands are clamped to rover limits
-   Battery use is based on absolute distance traveled
-   Rover movement is limited by remaining battery
-   Turning currently does not consume battery

### Completed Phase 1 Scope

- Rover movement with forward and reverse operation
- Target-speed control with acceleration/deceleration limits
- Maximum speed, acceleration, and turn-rate constraints
- Shortest-path heading control
- Battery consumption, depletion, and zero-consumption behavior
- Operational-state restrictions
- Configurable timestep simulation
- Exact command execution between timestep boundaries
- Multiple commands within a single timestep
- Mission command scheduling
- Sequential waypoint objectives
- Mission result evaluation
- Deterministic simulation reruns
- Telemetry state snapshots
- CSV telemetry export
- Trajectory and speed visualization
- Constructor and input validation
- Automated pytest coverage across Rover, Mission, Simulation, and TelemetryLogger
- Clean repository and test organization
- Git version control and public GitHub repository
- Dependency and generated-output management
- Portfolio-quality README and setup documentation

### Skills demonstrated

Python, OOP, simulation loops, numerical logic, pytest, debugging, file
I/O, CSV, Matplotlib, code organization, documentation.

------------------------------------------------------------------------

## Phase 2 --- SQL and Persistent Mission Data

**Estimated:** 3--5 days

### Purpose

Move beyond CSV-only telemetry and introduce persistent structured data.

### Planned work

-   Design relational schema
-   Store missions
-   Store rover information/state
-   Store telemetry samples
-   Store mission commands
-   Store mission events/faults
-   Begin with SQLite for simplicity
-   Keep schema portable enough for later PostgreSQL use
-   Connect database operations to the Python application

### Example queries

-   Distance traveled per mission
-   Battery consumed per mission
-   Average and maximum rover speed
-   Mission duration
-   Mission/fault history
-   Telemetry over a selected time range

### Skills demonstrated

SQL, relational modeling, schemas, CRUD, joins, aggregation,
persistence, Python/database integration.

------------------------------------------------------------------------

## Phase 3 --- Web Backend and Mission Control Dashboard

**Estimated:** 7--10 days

### Purpose

Turn the simulator into an application that can be controlled and
observed externally.

### Backend

Likely use Python with FastAPI.

Potential API capabilities:

-   Start/load a mission
-   Retrieve current rover state
-   Retrieve telemetry history
-   Retrieve mission history
-   Issue rover commands
-   Surface faults/events
-   Query analytics

### Frontend

Begin with core HTML/CSS/JavaScript concepts, then introduce a framework
such as React if it provides a meaningful benefit.

Potential dashboard features:

-   Rover status
-   Position and heading
-   Speed
-   Battery level
-   Mission elapsed time
-   Telemetry charts
-   Mission history
-   Command controls
-   Warning/fault display

### Skills demonstrated

HTTP, REST APIs, JSON, frontend fundamentals, backend development,
client/server architecture, asynchronous application behavior, UI
development.

------------------------------------------------------------------------

## Phase 4 --- Docker

**Estimated:** 2--4 days

### Purpose

Make the growing multi-service application reproducible and easy to run.

### Planned work

-   Create Dockerfiles for appropriate services
-   Containerize the backend
-   Containerize the web application where appropriate
-   Run the database as a service where appropriate
-   Configure Docker Compose
-   Use environment variables
-   Configure ports and networking
-   Add persistent database volumes
-   Document one-command project startup

### Skills demonstrated

Docker, containers, images, networking, environment configuration,
volumes, Docker Compose, reproducible development environments.

------------------------------------------------------------------------

## Phase 5 --- C++ Simulation Engine

**Estimated:** 7--10 days

### Purpose

Introduce C++ for a legitimate systems/simulation reason rather than
adding a second language only for résumé coverage.

Python begins as the rapid-prototyping environment. Once simulation
behavior is stable and tested, computational simulation responsibilities
can be migrated into a C++ engine.

### Likely C++ responsibilities

-   Rover dynamics
-   Simulation timestep
-   Velocity/acceleration calculations
-   Heading calculations
-   Environment calculations
-   Sensor simulation
-   Potentially higher-volume or multi-rover simulation

### Responsibilities that should likely remain in Python

-   Mission orchestration
-   Backend/API
-   Database access
-   Telemetry analysis
-   Plotting
-   Automation and scripting

### Integration progression

Start with the simplest reasonable interface, potentially:

1.  Build the simulation component as a C++ executable/library.
2.  Exchange structured state/commands with Python.
3.  Verify C++ behavior against existing Python tests/results.
4.  Consider direct Python/C++ bindings such as `pybind11` only if
    useful.
5.  Benchmark computational workloads where C++ should provide an
    advantage.

### Portfolio justification

The intended story is:

> The simulation was initially prototyped and validated in Python. Once
> its behavior stabilized, computationally intensive simulation
> responsibilities were extracted into C++, while Python remained
> responsible for orchestration, persistence, analytics, and application
> services.

Performance claims should be supported by actual benchmarks rather than
assumed.

### Skills demonstrated

C++, static typing, compilation, headers/source files, classes,
references/pointers, memory concepts, STL, CMake/build systems, testing,
cross-language interfaces, benchmarking.

------------------------------------------------------------------------

## Phase 6 --- Unity 3D Visualization

**Estimated:** 7--12 days

### Purpose

Create a polished real-time Mars visualization while demonstrating
integration between traditional software/simulation systems and a
real-time 3D engine.

Unity should primarily act as a **client/visualization layer**, rather
than becoming the authoritative source of simulation state.

### Planned features

-   Mars terrain/environment
-   3D rover
-   Rover movement driven by simulation state
-   Position/heading synchronization
-   Mission targets
-   Hazards
-   Telemetry UI
-   Camera modes
-   Mission visualization
-   Potential sensor visualization
-   Potential robotic-arm extension

### Skills demonstrated

Unity, C#, real-time 3D, client integration, visualization, simulation
presentation, interactive UI.

------------------------------------------------------------------------

## Phase 7 --- Integration and Portfolio Polish

**Estimated:** 5--7 days

### Purpose

Turn the collection of working components into one coherent,
demonstrable engineering project.

### Final system goals

A user should be able to:

1.  Launch the system with minimal setup.
2.  Start or configure a rover mission.
3.  Run the rover simulation.
4.  Issue commands through mission control.
5.  Observe current telemetry.
6.  Persist mission data to SQL.
7.  Query historical mission data.
8.  Visualize rover behavior in Unity.
9.  See meaningful errors/faults when something goes wrong.

### Engineering polish

-   Expand automated tests
-   Add integration tests where useful
-   Improve logging
-   Handle failure cases
-   Review code comments
-   Clean repository structure
-   Remove dead/experimental code
-   Create architecture diagram
-   Document setup
-   Document architectural decisions and tradeoffs
-   Record screenshots/GIFs/video
-   Create final portfolio presentation/write-up

### README should eventually cover

-   Project overview
-   Demo media
-   Architecture
-   Technology stack
-   Setup/run instructions
-   Testing instructions
-   Key engineering challenges
-   Design decisions
-   Performance measurements
-   Future improvements

------------------------------------------------------------------------

## Estimated Overall Schedule

  Phase                    Estimated Focused Days
  ---------------------- ------------------------
  Python                              7--10 total
  SQL                                        3--5
  Web                                       7--10
  Docker                                     2--4
  C++                                       7--10
  Unity 3D                                  7--12
  Integration / Polish                       5--7

**Approximate total:** 35--50 focused development days, including Python
work already completed.

At roughly one focused session per day, expect approximately **7--10
weeks** of consistent development.

------------------------------------------------------------------------

## Project Rules

### 1. One project, continuous growth

New skills should extend the Mars Rover platform whenever reasonably
possible instead of becoming unrelated tutorial projects.

### 2. Technology must earn its place

Do not add a framework, language, database, or tool solely to list it on
a résumé. Each technology should solve an identifiable problem.

### 3. Learn before abstracting

Prefer understandable implementations while learning. Introduce
frameworks and abstractions once their purpose is clear.

### 4. Test important behavior

Important simulation and application behavior should have automated
tests. Testing is part of implementation, not an optional final step.

### 5. Document decisions

Record meaningful architectural decisions and tradeoffs so they can
later be discussed in interviews and portfolio material.

### 6. Measure performance claims

Do not claim C++, Docker, database changes, or other architectural
decisions improved performance/reliability without evidence.

### 7. Keep the project runnable

Each major phase should end with a functioning project rather than
leaving the repository broken until the final phase.

------------------------------------------------------------------------

## Current Checkpoint — Updated 8/25

**Current phase:** Phase 1 complete — Phase 2 begins next development session

### Phase 1 Final Status

The Python Simulation Core is feature-complete, tested, documented, and version-controlled.

Core components:
- `Rover`
- `Mission`
- `Simulation`
- `TelemetryLogger`

Major completed behaviors:
- 2D forward/reverse rover movement
- Acceleration and deceleration
- Speed and turn-rate limits
- Shortest-path heading control
- Battery consumption and depletion
- Operational-state restrictions
- Exact timed mission commands
- Sequential waypoint objectives
- Mission success/failure evaluation
- Deterministic simulation reruns
- Telemetry history and historical snapshots
- CSV export
- Matplotlib trajectory and speed plots
- Input and constructor validation
- Automated pytest coverage

### Phase 1 Final Design Decisions

- `turn()` was removed; `turn_to()` and `update_heading()` are the authoritative turning system.
- Position is copied where historical or initial state must remain independent of mutable rover state.
- Initial headings are normalized.
- Zero battery consumption is intentionally supported.
- Commands may update target speed/heading without battery, while physical actuation remains disabled.
- A repeated `Simulation.run()` performs a fresh deterministic run from the original rover state.
- Missions with no waypoint objectives are considered objectively complete.
- Fixed-rate telemetry remains the current model; richer event/fault logging is deferred.
- Sensors are deferred as a strong candidate for the C++ simulation phase.
- Terrain and hazards are deferred until they provide value during later visualization/integration work.
- Randomized/Monte Carlo simulation is deferred until persistence and analytics make it more useful.
- Mission command representation remains Python-callable-based for now and will be reconsidered during SQL persistence because callables cannot be stored directly in a relational database.

### Packaging Status

- Repository structure cleaned
- Tests organized under `tests/`
- Generated output isolated under `output/`
- `.gitignore` configured
- `requirements.txt` created
- Git repository initialized
- Public GitHub repository created
- README documents architecture, setup, execution, testing, design decisions, and roadmap
- Crater Survey Run serves as the Phase 1 demonstration mission
- Final demo completes successfully
- Full automated test suite passes

### Next Session — Phase 2: SQL and Persistent Mission Data

Begin with SQLite and relational schema design.

Initial persistence targets:
- Missions
- Rover information/state
- Telemetry samples
- Mission results/events
- Mission commands, after determining a persistable command representation

The immediate goal is to move beyond CSV-only telemetry while keeping the existing Python simulation runnable and tested.

------------------------------------------------------------------------

## Definition of Done

The project is complete when it can credibly be presented as an
**end-to-end rover simulation platform**, rather than simply a
collection of technologies.

The finished portfolio story should demonstrate the ability to:

-   Design simulation logic
-   Write and test production-style code
-   Model and persist data
-   Build APIs
-   Build a usable frontend
-   Work across Python and C++
-   Package services with Docker
-   Integrate a real-time Unity visualization
-   Debug interactions between multiple systems
-   Explain architectural decisions and tradeoffs

The final goal is not merely to say **"I used Python, C++, SQL, Docker,
web technologies, and Unity."**

The goal is to be able to explain **why each one exists in the system
and how they work together.**
