# Roadmap: Hydrowheel Buoyancy Engine

## Overview

Component-by-component energy feasibility study of a 30-vessel buoyancy + hydrofoil engine in a 24 ft × 60 ft fresh water cylinder. Each phase isolates one subsystem, calculates its energy contribution or cost, then Phase 4 integrates everything into a complete system balance. The decisive output is whether the system can produce ≥ 1.5W per 1W of pumping input — if yes, build a physical prototype; if no, identify which component is limiting.

## Phases

- [x] **Phase 1: Air, Buoyancy & Fill** — Pumping energy, buoyancy work, jet recovery, and fill window feasibility
- [x] **Phase 2: Hydrofoil & Torque** — Lift/drag analysis, torque from ascending and descending vessels with tacking
- [ ] **Phase 3: Co-rotation** — Drag reduction model, lift preservation, energy cost of maintaining co-rotation
- [ ] **Phase 4: System Energy Balance** — Integrate all components, compute energy ratio, deliver go/no-go verdict

## Phase Details

### Phase 1: Air, Buoyancy & Fill

**Goal:** Establish all energy values associated with the air/water/buoyancy subsystem and confirm fill feasibility
**Depends on:** Nothing (first phase)
**Requirements:** THRM-01, THRM-02, THRM-03, BUOY-01, BUOY-02, BUOY-03, FILL-01, FILL-02, FILL-03

**Contract coverage:**
- Establishes pumping energy baseline (input W per cycle) — critical anchor for 1.5W/W claim
- Confirms buoyancy ≈ pumping energy in ideal case (sets expectation that gain must come from hydrofoil)
- Fill feasibility assessment for claim-fill-feasible
- Forbidden proxy guard: buoyancy work ≈ pumping energy is expected, NOT success

**Success Criteria** (what must be TRUE):

1. Pumping energy per cycle computed for both isothermal and adiabatic bounds, confirmed against initial scoping estimate (~20.6–24.0 kJ)
2. Buoyancy integral over 60 ft ascent computed; thermodynamic equivalence to pumping energy confirmed within 1%
3. Fill window duration calculated from loop geometry; required flow rate computed; practical feasibility assessed
4. Terminal velocity of vessel under buoyancy alone computed; 3 m/s confirmed as physically achievable

**Plans:** 3 plans in 3 waves

Plans:

- [ ] 01-01-PLAN.md -- Thermodynamic compression work bounds + buoyancy force profile (THRM-01, THRM-02, THRM-03, BUOY-01)
- [ ] 01-02-PLAN.md -- Buoyancy integral identity gate + terminal velocity sweep (BUOY-02, BUOY-03)
- [ ] 01-03-PLAN.md -- Fill window, flow rate, feasibility assessment, Phase 1 summary (FILL-01, FILL-02, FILL-03)

---

### Phase 2: Hydrofoil & Torque

**Goal:** Parametric analysis of hydrofoil lift/drag and torque contribution from both ascending and descending vessels
**Depends on:** Phase 1 (vessel velocity confirmed, buoyancy work established)
**Requirements:** FOIL-01, FOIL-02, FOIL-03, FOIL-04

**Contract coverage:**
- Quantifies the primary gain mechanism (obs-hydrofoil-torque) for claim-net-positive
- Tacking analysis: descending vessel foil torque in same direction as ascending
- Identifies minimum L/D required to reach 1.5W/W — key parameter for go/no-go

**Success Criteria** (what must be TRUE):

1. Lift and drag forces calculated for L/D range 5–30 at 3 m/s, AoA 5–10°
2. Torque from ascending vessels computed per cycle
3. Torque from descending vessels (tacked foil) computed per cycle; confirmed same rotational direction
4. Minimum L/D for 1.5W/W identified; assessed against realistic hydrofoil performance data

**Plans:** 2 plans in 2 waves

Plans:

- [ ] 02-01-PLAN.md -- Loop geometry + foil forces + ascending torque (FOIL-01, FOIL-02)
- [ ] 02-02-PLAN.md -- Descending tacking sign verification + minimum L/D + Phase 2 summary (FOIL-03, FOIL-04)

---

### Phase 3: Co-rotation

**Goal:** Model water co-rotation in the 24 ft cylinder and quantify drag reduction and lift preservation
**Depends on:** Phase 2 (hydrofoil drag values needed as baseline)
**Requirements:** COROT-01, COROT-02, COROT-03

**Contract coverage:**
- Quantifies co-rotation's contribution to drag reduction without reducing lift
- Addresses weakest assumption: co-rotation achievable and stable
- Flags energy cost of maintaining co-rotation (could reduce net gain)

**Success Criteria** (what must be TRUE):

1. Co-rotation angular velocity achievable in 24 ft cylinder modeled under realistic conditions
2. Horizontal drag reduction factor quantified (fraction of baseline drag eliminated)
3. Vertical relative velocity (and thus hydrofoil lift) shown to be preserved under co-rotation
4. Any energy input required to maintain co-rotation estimated and included in system balance

**Plans:** 2 plans in 2 waves

Plans:

- [ ] 03-01-PLAN.md -- Angular momentum balance (f_ss, P_corot, reconciliation) + lift preservation (COROT-01, COROT-03)
- [ ] 03-02-PLAN.md -- P_net(f) sweep, COP_corot(f) curve, phase3_verdict, Phase 4 handoff (COROT-02)

---

### Phase 4: System Energy Balance

**Goal:** Integrate all component results into a complete energy balance; deliver go/no-go verdict on 1.5W/W
**Depends on:** Phases 1, 2, 3
**Requirements:** SYS-01, SYS-02, SYS-03

**Contract coverage:**
- Delivers deliv-energy-balance and deliv-component-table (decisive deliverables for claim-net-positive)
- Enforces test-no-missing-losses: all losses explicitly accounted for
- Delivers go/no-go verdict against 1.5W/W threshold
- Forbidden proxy enforced: no partial analysis accepted as success

**Success Criteria** (what must be TRUE):

1. All 30-vessel contributions summed: pumping input, buoyancy work, hydrofoil torque (ascending + descending), jet recovery, co-rotation drag reduction, bearing/friction losses
2. Energy ratio (output W / input W) computed with uncertainty range from L/D and co-rotation efficiency sensitivity
3. Explicit go/no-go verdict delivered: ratio ≥ 1.5 → proceed to prototype; ratio < 1.0 → concept not viable; 1.0–1.5 → marginal, identify limiting component
4. Sensitivity table shows which parameter (L/D, velocity, co-rotation) most controls the result

Plans:

- [ ] 04-01: [TBD — created during /gpd:plan-phase 4]

---

## Progress

| Phase | Plans Complete | Status | Completed |
| ----- | -------------- | ------ | --------- |
| 1. Air, Buoyancy & Fill | 3/3 | ✓ Complete | 2026-03-17 |
| 2. Hydrofoil & Torque | 2/2 | ✓ Complete | 2026-03-17 |
| 3. Co-rotation | 0/2 | Planned | - |
| 4. System Energy Balance | 0/TBD | Not started | - |
