# Requirements: Hydrowheel Buoyancy Engine

**Defined:** 2026-03-16
**Core Research Question:** Can this buoyancy + hydrofoil engine produce at least 1.5W of shaft power for every 1W of air pumping input?

## Primary Requirements

### Thermodynamics

- [ ] **THRM-01**: Calculate air pumping energy per vessel cycle — isothermal and adiabatic bounds — for the 7.069 ft³ vessel at 60 ft depth (fresh water, P = 2.770 atm)
- [ ] **THRM-02**: Calculate fill volume required at depth (2.553 ft³) and equivalent surface volume (7.069 ft³), and confirm fill target condition (air expands exactly to fill vessel at surface)
- [ ] **THRM-03**: Estimate jet propulsion energy recovery from expanding air during ascent (shaped open-bottom nozzle effect)

### Fluid Mechanics — Buoyancy

- [ ] **BUOY-01**: Calculate buoyancy force on an ascending vessel as a function of depth during 60 ft ascent
- [ ] **BUOY-02**: Integrate buoyancy work over full ascent at 3 m/s and compare against pumping energy (confirm thermodynamic equivalence in ideal case)
- [ ] **BUOY-03**: Estimate terminal velocity of ascending vessel under buoyancy alone (without hydrofoil) and confirm 3 m/s is physically achievable

### Fluid Mechanics — Hydrofoil

- [ ] **FOIL-01**: Calculate lift and drag forces on a single vessel hydrofoil as a function of L/D ratio, vessel velocity (3 m/s), and angle of attack (5–10°)
- [ ] **FOIL-02**: Calculate torque contribution from ascending vessels (hydrofoil pulling in rotational direction)
- [ ] **FOIL-03**: Calculate torque contribution from descending vessels with tacked foil (same rotational direction as ascending)
- [ ] **FOIL-04**: Determine minimum L/D ratio required for system to reach 1.5W/W target

### Fluid Mechanics — Co-rotation

- [ ] **COROT-01**: Model co-rotation of water body in 24 ft cylinder — estimate achievable co-rotation speed relative to vessel speed
- [ ] **COROT-02**: Quantify horizontal drag reduction on vessels from co-rotation
- [ ] **COROT-03**: Confirm that vertical relative velocity (and thus hydrofoil lift) is preserved under co-rotation

### Fill System

- [ ] **FILL-01**: Calculate fill window duration from loop geometry and 3 m/s vessel velocity (1/4 loop circumference)
- [ ] **FILL-02**: Calculate required air flow rate (CFM at depth pressure) to fill 2.553 ft³ within the fill window
- [ ] **FILL-03**: Assess practical feasibility of the required flow rate against available compressed air equipment

### System Integration

- [ ] **SYS-01**: Compile complete component energy balance for all 30 vessels: pumping input, buoyancy work, hydrofoil torque (ascending + descending), co-rotation drag cost, jet recovery, bearing/friction losses
- [ ] **SYS-02**: Compute system energy ratio (output W / input W) and compare against 1.5W/W target
- [ ] **SYS-03**: Deliver go/no-go verdict with sensitivity analysis on L/D ratio and co-rotation efficiency

## Follow-up Requirements

### Physical Model Preparation

- **PROTO-01**: Identify minimum-scale prototype dimensions for meaningful measurement
- **PROTO-02**: Specify instrumentation needed to measure shaft power and pumping energy in a physical test

### Extended Analysis

- **EXT-01**: Optimize hydrofoil AoA and geometry for maximum net output
- **EXT-02**: Analyze tack-flip mechanism energy cost (spring, cam, or passive flip)
- **EXT-03**: Scale analysis — how does system performance change with size?

## Out of Scope

| Topic | Reason |
| ----- | ------ |
| Detailed hydrofoil profile design | Requires physical model testing to verify L/D in this regime |
| Tack-flip mechanism engineering | Mechanism design deferred to prototype phase |
| Full geometry optimization | This study establishes feasibility; optimization is follow-on |
| Salt water operation | User specified fresh water |
| Structural / fatigue analysis | Beyond scope of feasibility study |

## Accuracy and Validation Criteria

| Requirement | Accuracy Target | Validation Method |
| ----------- | --------------- | ----------------- |
| THRM-01 | ±5% on pumping energy | Compare isothermal vs adiabatic bounds; confirm with ideal gas law |
| BUOY-02 | Confirm thermodynamic equivalence ±1% | Numerical integration of P(h)×dV vs isothermal work formula |
| FOIL-01 | L/D parametric range 5–30 | Standard hydrofoil lift/drag correlations from literature |
| FILL-01 | ±10% on fill window time | Depends on loop geometry; flag if geometry changes |
| SYS-02 | ±15% on energy ratio | Sensitivity analysis over L/D and co-rotation efficiency range |

## Contract Coverage

| Requirement | Decisive Output / Deliverable | Anchor / Benchmark | Prior Inputs / Baselines | False Progress To Reject |
| ----------- | ----------------------------- | ------------------ | ------------------------ | ------------------------ |
| SYS-01, SYS-02 | deliv-energy-balance, deliv-component-table | claim-net-positive (1.5W/W) | Initial pumping calc 20.6 kJ | Buoyancy work alone equaling pumping energy |
| FILL-01, FILL-02, FILL-03 | deliv-fill-analysis | claim-fill-feasible | 3 m/s velocity, 1/4 loop constraint | Fill appearing feasible without checking actual flow rate |

## Traceability

| Requirement | Phase | Status |
| ----------- | ----- | ------ |
| THRM-01 | Phase 1: Air & Buoyancy | Pending |
| THRM-02 | Phase 1: Air & Buoyancy | Pending |
| THRM-03 | Phase 1: Air & Buoyancy | Pending |
| BUOY-01 | Phase 1: Air & Buoyancy | Pending |
| BUOY-02 | Phase 1: Air & Buoyancy | Pending |
| BUOY-03 | Phase 1: Air & Buoyancy | Pending |
| FILL-01 | Phase 1: Air & Buoyancy | Pending |
| FILL-02 | Phase 1: Air & Buoyancy | Pending |
| FILL-03 | Phase 1: Air & Buoyancy | Pending |
| FOIL-01 | Phase 2: Hydrofoil & Torque | Pending |
| FOIL-02 | Phase 2: Hydrofoil & Torque | Pending |
| FOIL-03 | Phase 2: Hydrofoil & Torque | Pending |
| FOIL-04 | Phase 2: Hydrofoil & Torque | Pending |
| COROT-01 | Phase 3: Co-rotation | Pending |
| COROT-02 | Phase 3: Co-rotation | Pending |
| COROT-03 | Phase 3: Co-rotation | Pending |
| SYS-01 | Phase 4: System Balance | Pending |
| SYS-02 | Phase 4: System Balance | Pending |
| SYS-03 | Phase 4: System Balance | Pending |

**Coverage:**

- Primary requirements: 19 total
- Mapped to phases: 19
- Unmapped: 0

---

_Requirements defined: 2026-03-16_
_Last updated: 2026-03-16 after initial definition_
