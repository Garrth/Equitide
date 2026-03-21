# Requirements: Hydrowheel Buoyancy Engine — v1.2 Purge Thrust and Tail Foil

**Defined:** 2026-03-21
**Core Research Question:** Does the Hydrowheel produce net positive energy (COP > 1.0), and what is the corrected COP when purge jet thrust and tail foil lift — two previously excluded contributions — are properly accounted for?

## Primary Requirements

Requirements for v1.2. Phases continue from v1.1 (last phase = 6); v1.2 starts at Phase 7.

### Purge Thrust (PROP)

- [ ] **PROP-01**: Derive the force balance for an open-bottom ascending vessel; establish analytically whether F_jet(z) (reaction force from downward water ejection during isothermal air expansion) is additive to F_buoy(z) or a restatement of it — resolve against the W_buoy = W_iso identity from v1.0
- [ ] **PROP-02**: Derive F_jet(z) from first principles: isothermal expansion → water ejection mass flux ṁ_w(z) → exit velocity v_exit(z) → reaction force F_jet(z) = ṁ_w(z) × v_exit(z); integrate to W_jet_thrust = ∫₀ᴴ F_jet(z) dz; compare to 20% upward force estimate
- [ ] **PROP-03**: Incorporate F_jet(z) into the coupled brentq solver (extending Phase 5 solver); compute corrected v_loop and COP contribution from purge thrust alone

### Tail Foil (TAIL)

- [ ] **TAIL-01**: Derive purge jet exit velocity profile v_exit(z) from the water ejection mass flux computed in PROP-02; establish the effective flow velocity seen by the tail foil at each height z
- [ ] **TAIL-02**: Compute tail foil lift and drag using NACA foil data at v_exit(z); foil span = 0.457 m (vessel diameter), chord parametric up to 0.457 m; determine W_tail_foil per vessel per cycle as a function of chord
- [ ] **TAIL-03**: Incorporate tail foil forces into the coupled force balance; confirm AoA_optimal remains near 2° (sensitivity check at AoA = 1°, 2°, 3°)

### System Verdict (VALD)

- [ ] **VALD-01**: Energy accounting verification — confirm (W_buoy + W_jet_thrust) satisfies energy conservation against W_iso; no double-counting permitted; document resolution if jet is genuinely additive to Archimedes force
- [ ] **VALD-02**: Produce full revised 9-scenario COP table (η_c ∈ {0.65, 0.70, 0.85} × loss_frac ∈ {0.05, 0.10, 0.15}) with W_jet_thrust + W_tail_foil included at AoA = 2°
- [ ] **VALD-03**: Compute COP margin above 1.0 for each scenario; identify minimum-margin (worst case) and maximum-margin (best case); confirm GO/NO_GO verdict vs COP = 1.0 threshold

## Follow-up Requirements

### Wave Coupling (v1.3)

- **WAVE-01**: Model tangential velocity injection from external wave pumps into the water cylinder; compute apparent velocity and angle seen by foils
- **WAVE-02**: Re-run rotating-arm force analysis with combined (v_loop, v_tangential) apparent velocity; compute W_foil_wave vs W_foil_baseline
- **WAVE-03**: Assess COP multiplier effect (wave energy treated as free — zero cost in denominator); parametric over achievable v_tangential

## Out of Scope

| Topic | Reason |
| ----- | ------ |
| Wave energy coupling | Deferred to v1.3 — qualitatively different input mechanism |
| Geometry optimization (depth, vessel count) | Not needed until corrected baseline COP is established |
| Tack-flip mechanism energy loss | Deferred — marked as highest prototype measurement priority in v1.1 |
| Structural or fatigue analysis | Separate engineering study |
| Salt water operation | Fresh water only per design specification |

## Accuracy and Validation Criteria

| Requirement | Accuracy Target | Validation Method |
| ----------- | --------------- | ----------------- |
| PROP-01 | Analytic result | Compare open-bottom and closed-vessel Archimedes forces; check energy balance against W_iso |
| PROP-02 | 3 significant figures on W_jet_thrust | Verify 20% force estimate; dimensional check on F_jet(z) |
| PROP-03 | v_loop to 0.5% (matching Phase 5 tolerance) | brentq solver convergence; anchor check against Phase 5/6 at AoA=10° baseline |
| TAIL-02 | W_tail_foil to 3 significant figures | NACA C_L, C_D data at Re appropriate for v_exit; verify v_exit Reynolds number regime |
| VALD-01 | Exact energy balance | W_buoy + W_jet_thrust ≤ W_iso or rigorous justification for additive case |
| VALD-02 | COP to 4 significant figures (matching Phase 6 precision) | Cross-check against Phase 6 table at zero jet/tail contribution |
| VALD-03 | Margin to 3 significant figures | Identify worst-case scenario explicitly |

## Contract Coverage

| Requirement | Decisive Output / Deliverable | Anchor / Benchmark | Prior Inputs / Baselines | False Progress To Reject |
| ----------- | ----------------------------- | ------------------ | ------------------------ | ------------------------ |
| PROP-01 | Analytic proof: additive or restatement | W_buoy = W_iso identity (v1.0, confirmed 2×10⁻⁷%) | phase1 JSON, W_iso = 20,644.6 J | Claiming jet is additive without resolving the energy accounting |
| PROP-02 | F_jet(z) profile and W_jet_thrust (J) | 20% upward force estimate (user) | V_air(z), P(z) from phase1 JSON | Accepting 20% estimate without first-principles derivation |
| VALD-01 | Energy balance table: W_buoy + W_jet vs W_iso | W_iso = 20,644.6 J (phase1) | phase1 locked values | Any result that exceeds W_iso without physical justification |
| VALD-02 | 9-scenario COP table with new contributions | Phase 6 COP table (COP_max = 1.210) | phase6_verdict.json | COP increase without verifying non-double-counting |
| VALD-03 | Margin above COP = 1.0 per scenario | COP = 1.0 (net positive threshold) | phase6_verdict.json | Reporting best-case only without worst-case minimum margin |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
| ----------- | ----- | ------ |
| PROP-01 | Phase 7: Purge Thrust and Tail Foil Derivation | Pending |
| PROP-02 | Phase 7: Purge Thrust and Tail Foil Derivation | Pending |
| PROP-03 | Phase 8: Revised System Verdict | Pending |
| TAIL-01 | Phase 7: Purge Thrust and Tail Foil Derivation | Pending |
| TAIL-02 | Phase 7: Purge Thrust and Tail Foil Derivation | Pending |
| TAIL-03 | Phase 8: Revised System Verdict | Pending |
| VALD-01 | Phase 7: Purge Thrust and Tail Foil Derivation | Pending |
| VALD-02 | Phase 8: Revised System Verdict | Pending |
| VALD-03 | Phase 8: Revised System Verdict | Pending |

**Coverage:**

- Primary requirements: 9 total
- Mapped to phases: 9
- Unmapped: 0

---

_Requirements defined: 2026-03-21_
_Last updated: 2026-03-21 after v1.2 milestone initialization_

---

# Requirements: Hydrowheel Buoyancy Engine — v1.3 Differential Rotation Analysis (Pre-planned)

**Defined:** 2026-03-21
**Core Research Question:** If v_water_tangential > v_arm_tangential, does the shifted apparent flow vector act as a COP multiplier, additive boost, or stall trigger?

**Scope:** Purely fluid mechanical — no energy accounting for how differential rotation is maintained. Speed ratio r = v_water_tangential / v_arm_tangential swept from 1.0 (co-rotation baseline) to 1.5 (50% faster than arms).

## Primary Requirements

Requirements for v1.3. Phases continue from v1.2 (last phase = 8); v1.3 starts at Phase 9.

### Differential Rotation Analysis (WAVE)

- [ ] **WAVE-01**: Derive the apparent flow vector seen by the foil at speed ratio r = v_water_tangential / v_arm_tangential; compute effective AoA_eff(r) = mount_angle − arctan(v_tangential_net / v_vertical) and |v_rel|(r) for r ∈ [1.0, 1.5] at all loop positions; identify AoA_stall boundary r_stall where AoA_eff ≥ AoA_stall
- [ ] **WAVE-02**: Compute lift L(r), drag D(r), horizontal torque Γ_h(r), and F_vert(r) at each r using NACA 0012 C_L/C_D data from Phase 5/6 (identical interpolation scheme); compare to baseline r = 1.0 to classify COP response: multiplicative (Γ_h ↑ and F_vert ↓ simultaneously), additive (|v_rel| ↑ only), or negative (AoA > AoA_stall)
- [ ] **WAVE-03**: Compute COP(r) via coupled brentq solver extending the Phase 5/6 framework; sweep r ∈ [1.0, 1.5] at 0.05 increments (11 points); find optimal r* if a COP maximum exists; report COP gain vs baseline (r = 1.0) and characterize the response type

## Out of Scope

| Topic | Reason |
| ----- | ------ |
| Energy cost of differential rotation | Out of scope by user specification — wave energy treated as free |
| r > 1.5 | Beyond physically realistic range for this geometry |
| AoA re-optimization at each r | AoA held at Phase 6 optimal (2°) for first pass; sensitivity deferred |
| Geometry changes (depth, vessel count) | Separate investigation; not part of v1.3 |

## Accuracy and Validation Criteria

| Requirement | Accuracy Target | Validation Method |
| ----------- | --------------- | ----------------- |
| WAVE-01 | AoA_eff to 0.1° | Reproduce baseline (r=1.0) → AoA_eff = Phase 6 AoA_optimal = 2.0° |
| WAVE-02 | Force components to 3 significant figures | At r=1.0, reproduce Phase 6 forces to within 0.5% |
| WAVE-03 | COP to 4 significant figures | At r=1.0, reproduce Phase 6 COP_nominal to within 0.5% (continuity check) |

## Contract Coverage

| Requirement | Decisive Output | Anchor / Benchmark | Prior Inputs | False Progress To Reject |
| ----------- | --------------- | ------------------ | ------------ | ------------------------ |
| WAVE-01 | AoA_eff(r) and \|v_rel\|(r) table | Phase 6 AoA_optimal = 2.0° at r=1.0 | phase5 solver geometry; phase6_verdict.json | AoA_eff at r≠1 without first reproducing r=1.0 baseline |
| WAVE-02 | Force classification table (multiplicative/additive/negative) | Phase 6 force components at AoA=2° | Phase 5/6 NACA 0012 interpolator | Claiming multiplier without computing F_vert(r) simultaneously |
| WAVE-03 | COP(r) sweep; optimal r*; gain vs baseline | Phase 6 COP_nominal (continuity check) | phase5 brentq solver | Reporting COP gain without continuity check at r=1.0 |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
| ----------- | ----- | ------ |
| WAVE-01 | Phase 9: Differential Rotation Geometry and Force Analysis | Pending |
| WAVE-02 | Phase 9: Differential Rotation Geometry and Force Analysis | Pending |
| WAVE-03 | Phase 10: COP Sweep and Differential Rotation Verdict | Pending |

**Coverage:**

- Primary requirements: 3 total
- Mapped to phases: 3
- Unmapped: 0

---

_v1.3 requirements pre-planned: 2026-03-21_
