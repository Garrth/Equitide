# Hydrowheel Buoyancy Engine

## What This Is

A theoretical feasibility study of a buoyancy + hydrofoil engine consisting of 30 open-bottom cylindrical vessels (3 vertical loops × 10 vessels) orbiting a central shaft in a 24 ft diameter × 60 ft deep fresh water cylinder. Ascending vessels are air-filled (buoyant); descending vessels are water-filled and pulled down by the chain. Hydrofoils on every vessel are tacked so both ascending and descending vessels contribute torque in the same rotational direction. Co-rotation of the water body reduces horizontal drag without reducing the vertical lift that drives the hydrofoils. The study determines whether the system can produce 1.5W of shaft output per 1W of air pumping input.

## Core Research Question

Can this buoyancy + hydrofoil engine produce at least 1.5W of shaft power for every 1W of air pumping input, as determined by a component-by-component energy balance?

## Scoping Contract Summary

### Contract Coverage

- **Claim (claim-net-positive):** System produces ≥ 1.5W out per 1W in — success = energy ratio ≥ 1.5 under reasonable (not optimistic) assumptions
- **Claim (claim-fill-feasible):** Vessel can be air-filled within the 1/4 loop window at 3 m/s — success = required flow rate achievable with practical equipment
- **Acceptance signal:** Complete system balance table including pumping, buoyancy, hydrofoil torque (ascending + descending), co-rotation drag reduction, jet recovery, and all losses
- **False progress to reject:** Net positive buoyancy work alone (thermodynamically can't exceed pumping energy); individual components looking favorable without a complete system balance

### User Guidance To Preserve

- **User-stated observables:** Energy balance ratio (output W / input W); net shaft power in watts; fill time window duration; required air flow rate
- **User-stated deliverables:** Component-by-component energy table; go/no-go verdict on 1.5W/W target; fill feasibility note
- **Must-have references / prior outputs:** Initial pumping calculation: ~20.6 kJ isothermal, ~24.0 kJ adiabatic per cycle for 7.069 ft³ vessel at 60 ft depth
- **Stop / rethink conditions:** If complete system balance shows output/input < 1.0 under reasonable assumptions, concept is not viable — stop and revisit design before further calculation

### Scope Boundaries

**In scope**

- Air pumping energy per vessel cycle (compression from 1 atm to 2.770 atm)
- Buoyancy work during ascent at 3 m/s (30 ascending vessels)
- Hydrofoil lift and drag analysis — parametric over L/D range, not final design
- Co-rotation drag reduction model
- Jet propulsion recovery from expanding air during ascent
- Fill time feasibility: 1/4 loop at 3 m/s
- Component-by-component energy balance and go/no-go verdict

**Out of scope**

- Detailed hydrofoil profile design (deferred to physical model)
- Tack-flip mechanism engineering (deferred to physical model)
- Full geometry optimization
- Salt water operation
- Physical prototype construction details

### Active Anchor Registry

- **initial-pumping-calc**: Pumping energy estimate from scoping conversation
  - Why it matters: Establishes the input energy baseline per cycle; all efficiency claims are relative to this
  - Carry forward: execution, verification
  - Required action: use, compare

### Carry-Forward Inputs

- Initial pumping calculation: 20.6 kJ isothermal / 24.0 kJ adiabatic for single vessel (7.069 ft³ at 2.770 atm)
- 3 m/s vessel velocity (user estimate from buoyancy analysis)
- 1/4 loop fill window constraint (user design specification)

### Skeptical Review

- **Weakest anchor:** Hydrofoil L/D ratio in low-speed water flow — no measured value yet, using literature estimates for parametric analysis
- **Unvalidated assumptions:** 3 m/s vessel velocity maintained under hydrofoil drag load; co-rotation of water body achievable and stable; tack-flip mechanism adds negligible energy loss
- **Competing explanation:** If hydrofoil L/D in this low-speed regime is < 5, system may not reach 1.5W/W target; co-rotation may require energy input to maintain, reducing net gain
- **Disconfirming observation:** If complete system balance including all losses shows output/input < 1.0, concept is not viable
- **False progress to reject:** Any result that only shows buoyancy ≈ pumping without the hydrofoil contribution — that is expected and not success

### Open Contract Questions

- Final loop geometry (needed to compute vessel spacing and fill window duration)
- Hydrofoil chord length, span, and profile for L/D estimate
- Co-rotation achievement mechanism and energy cost

## Research Questions

### Answered

(None yet — investigate to answer)

### Active

- [ ] What is the net pumping energy cost per vessel cycle at 60 ft depth (isothermal and adiabatic bounds)?
- [ ] What buoyancy work is produced per ascending vessel during the 60 ft ascent at 3 m/s?
- [ ] What hydrofoil torque do ascending and descending vessels contribute per cycle (parametric in L/D)?
- [ ] Does co-rotation reduce horizontal drag without reducing lift, and by how much?
- [ ] How much energy is recovered from the expanding air jet during ascent?
- [ ] Is the fill window (1/4 loop at 3 m/s) sufficient for a practical air injection system?
- [ ] Does the complete system energy balance yield output/input ≥ 1.5?

### Out of Scope

- Optimal hydrofoil geometry — requires physical model
- Tack-flip mechanism design — requires physical model
- Long-term structural loads and fatigue — separate engineering study

## Research Context

### Physical System

30 open-bottom cylindrical vessels (4 ft × 18 in diameter, 7.069 ft³ each) on 3 vertical loops inside a 24 ft diameter × 60 ft deep fresh water cylinder. Each vessel carries a hydrofoil. Ascending vessels are air-filled at depth and rise by buoyancy; descending vessels are water-filled and pulled down by the chain coupling to ascending vessels. Air is injected at the bottom of each loop over a fill window of 1/4 loop circumference.

### Theoretical Framework

Classical fluid mechanics, hydrostatics, thermodynamics (ideal gas), and hydrofoil aerodynamics/hydrodynamics applied to a low-speed water flow regime.

### Key Parameters and Scales

| Parameter | Symbol | Value / Regime | Notes |
| --------- | ------ | -------------- | ----- |
| Vessel diameter | d | 18 in (0.457 m) | Cylinder |
| Vessel length | L | 4 ft (1.219 m) | |
| Vessel volume | V | 7.069 ft³ (0.2002 m³) | π × 0.75² × 4 |
| Depth | h | 60 ft (18.29 m) | Bottom of vessel to surface |
| Depth pressure | P₂ | 2.770 atm (40.70 psi) | Fresh water |
| Volume at depth | V_d | 2.553 ft³ (0.0723 m³) | Air fill at depth |
| Vessel velocity | v | 3 m/s | User estimate |
| Number of vessels | N | 30 | 3 loops × 10 |
| Cylinder diameter | D | 24 ft (7.32 m) | Outer tank |
| Cylinder depth | H | 60 ft (18.29 m) | |
| Hydrofoil AoA | α | 5–10° | To be optimized |
| Target efficiency | η | 1.5 W/W | Go/no-go threshold |

### Known Results

- Pumping energy (isothermal, ideal): 20.6 kJ per vessel cycle — from initial scoping calculation
- Pumping energy (adiabatic): 24.0 kJ per vessel cycle — from initial scoping calculation
- In ideal isothermal case, buoyancy work = pumping energy (thermodynamic equivalence) — net gain must come from hydrofoil

### What Is New

This study quantifies whether the combination of dual-direction hydrofoil torque harvesting (tacking), co-rotation drag cancellation, and jet recovery can produce a net positive energy output exceeding the thermodynamic break-even of a simple buoyancy engine.

### Target Venue

Engineering feasibility study for internal use; go/no-go decision for physical prototype construction.

### Computational Environment

Analytical calculations; spreadsheet or Python for numerical integration where needed. No HPC required.

## Notation and Conventions

See `.gpd/CONVENTIONS.md` for all notation and sign conventions.

## Unit System

SI primary (m, kg, s, W, J, Pa) with Imperial cross-checks (ft, lb, BTU, psi) where relevant to the physical design.

## Requirements

See `.gpd/REQUIREMENTS.md` for the detailed requirements specification.

## Key References

- Initial pumping calculation from scoping (no external publication — user estimate + ideal gas law)
- Hydrofoil L/D data: to be sourced from standard naval architecture / low-speed hydrodynamics literature during Phase 2

## Constraints

- **Velocity:** 3 m/s vessel speed — affects fill time, hydrofoil forces, and drag
- **Fill window:** 1/4 loop circumference at 3 m/s — constrains air injection system design
- **Fresh water only:** ρ = 1000 kg/m³ (62.4 lb/ft³), 1 atm = 33.9 ft
- **Scale:** 30 vessels in a 24 ft × 60 ft cylinder — sets absolute power scale

## Key Decisions

| Decision | Rationale | Outcome |
| -------- | --------- | ------- |
| Use actual cylinder volume (7.069 ft³) not user estimate (4 ft³) | π × 0.75² × 4 = 7.069; user was ballparking | Confirmed |
| Fill target: air fills vessel exactly at surface | Constraint "air doesn't expand beyond vessel" → at surface V_air = V_vessel | Confirmed |
| Fill window = 1/4 loop circumference at 3 m/s | User design specification | Confirmed |
| Fresh water, bottom of vessel at 60 ft | User specification | Confirmed |
| Analyze components separately before system balance | User's stated methodology | Confirmed |

---

_Last updated: 2026-03-16 after initialization_
