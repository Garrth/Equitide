# Hydrowheel Buoyancy Engine

## What This Is

A theoretical feasibility study of a buoyancy + hydrofoil engine consisting of 30 open-bottom cylindrical vessels (3 vertical loops × 10 vessels) orbiting a central shaft in a 24 ft diameter × 60 ft deep fresh water cylinder. Ascending vessels are air-filled (buoyant); descending vessels are water-filled and pulled down by the chain. Hydrofoils on every vessel are tacked so both ascending and descending vessels contribute torque in the same rotational direction. Co-rotation of the water body reduces horizontal drag without reducing the vertical lift that drives the hydrofoils. The study determines whether the system can produce 1.5W of shaft output per 1W of air pumping input.

## Current Milestone: v1.1 AoA Parametric Sweep

**Goal:** Determine whether adjusting the hydrofoil angle of attack — specifically reversing the foil mount to flip F_vert upward — yields COP ≥ 1.5 and constitutes a viable path to prototype.

**Target results:**

- AoA at which F_vert = 0 (neutral vertical force) and resulting COP
- Full parametric COP(AoA) sweep from current design point (AoA ≈ 10° at λ = 0.9) through reversed-mount geometry
- Go/no-go verdict on reversed foil mounting as prototype design path

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

- [x] What is the net pumping energy cost per vessel cycle? — W_iso = 20,644.6 J (isothermal lower bound), W_adia = 23,959.5 J (adiabatic upper bound); W_pump = 28,188–36,861 J at η_c = 0.85–0.65 — v1.0
- [x] What buoyancy work is produced per ascending vessel? — W_buoy = W_iso = 20,644.6 J (identity confirmed to 2×10⁻⁷%); buoyancy alone cannot exceed COP = 0.73 — v1.0
- [x] What hydrofoil torque do ascending and descending vessels contribute? — W_foil_asc = W_foil_desc = 20,767 J/vessel at λ = 1; COP_partial = 2.057 at design λ = 0.9 (upper bound, pre-F_vert correction) — v1.0
- [x] Does co-rotation reduce drag without reducing lift? — YES: 47.5 kW drag reduction at 720 W maintenance cost; lift geometrically preserved — v1.0
- [x] Is jet recovery significant? — No: W_jet = 0 as separate term; already contained in W_buoy integral — v1.0
- [x] Is the fill window sufficient? — YES (GO): 274 SCFM at 26 psig, medium industrial compressor — v1.0
- [x] Does the system balance yield COP ≥ 1.5? — **NO**: self-consistent v_loop = 2.384 m/s; corrected COP ∈ [0.811, 1.186], NO_GO — v1.0

### Active (v1.1)

- [ ] At what foil AoA does F_vert = 0 (neutral vertical force), and what COP results?
- [ ] Is there an AoA with F_vert slightly upward-assisting while maintaining meaningful tangential torque — and does COP reach ≥ 1.5?
- [ ] Full parametric AoA sweep: from current design (AoA ≈ 10° at λ = 0.9) down to minimum effective lift angle

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

### Known Results (v1.0 Complete)

- **Thermodynamics:** W_iso = 20,644.6 J, W_adia = 23,959.5 J per vessel cycle; W_pump = 28,188–36,861 J at η_c = 0.85–0.65
- **Buoyancy:** W_buoy = W_iso to 2×10⁻⁷% (identity gate PASSED); COP_ideal_max = 0.73 max — hydrofoil required
- **Terminal velocity:** v_nominal = 3.714 m/s (C_D = 1.0, F_chain = 0); conservative 3.075 m/s; self-consistent 2.384 m/s (with F_vert)
- **Fill:** GO — 274 SCFM at 26 psig; medium industrial rotary screw compressor sufficient
- **Hydrofoil (upper bound):** COP_partial = 2.057 at λ = 0.9; tacking confirmed by vector geometry; both loop halves contribute positive torque
- **F_vert coupling (critical):** F_vert = −663.9 N downward at design point; reduces v_loop from 3.714 → 2.384 m/s (36% drop)
- **Co-rotation:** f_stall = 0.294; P_net = 46.8 kW saved at nominal velocity; scales to 12.4 kW at corrected v_loop (v³ scaling)
- **System verdict (NO_GO):** Corrected COP_nominal = 0.925; full range [0.811, 1.186] across 9 scenarios — all below 1.5
- **Decisive design path:** Reversed foil mounting → upward F_vert → higher v_loop → restored co-rotation savings

### What Is New (v1.1 Question)

Whether reducing foil AoA rotates the lift vector to reduce F_vert magnitude toward zero — and whether any AoA produces COP ≥ 1.5 with F_vert neutral or assisting — is the unresolved question that determines prototype viability.

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
| Use precise P_r = 2.7669 (not rounded 2.770) for all calculations | Avoids 0.34% compounding rounding error through 4 phases | Good |
| W_pump = W_adia/η_c as COP denominator (not W_iso) | W_iso is theoretical limit; real pump uses adiabatic work | Good |
| F_b_avg = W_iso/H as energy-weighted driving force | Correct for energy accounting; avoids constant-force approximation | Good |
| Fixed mount angle 38° at λ = 1, AoA_target = 7° | Design point; AoA_eff sweeps as λ changes | Good |
| F_vert/F_b_avg > 0.20 → Phase 4 coupled solution mandatory | 1.15 >> 0.20 flag triggered correctly; uncorrected COP = upper bound only | Good |
| brentq for coupled (v_loop, ω) solution; not fixed-point | Fixed-point diverges when F_vert ∝ v² faster than hull drag | Good |
| Co-rotation P_net scaled by (v_corr/v_nom)³ in Phase 4 | Consistent with v³ drag scaling; halves the apparent co-rotation benefit | Good |
| Lossless gate COP ≠ 1 is expected; use buoy-iso gate instead | Multi-source machine with net energy production; W_buoy = W_iso is the First Law check | Good |
| Verdict: NO_GO on v1.0 foil orientation; test reversed mounting | F_vert direction is the single highest-leverage unknown | Pending prototype |

---

_Last updated: 2026-03-19 after v1.1 milestone start_
