---
phase: 09-differential-rotation-geometry-and-force-analysis
mode: rapid
checker: gpd-consistency-checker
date: 2026-03-21
consistency_status: CONSISTENT
checks_performed: 10
issues_found: 0
---

# Phase 9 Consistency Check (Rapid Mode)

## Summary

**Status: CONSISTENT** — Phase 9 artifacts are fully consistent with the accumulated conventions ledger through Phase 6. All four primary checks (F_vert sign, v_loop source, NACA provenance, lambda_design) pass. Six additional spot-checks confirm convention compliance.

---

## Convention Compliance Matrix

| Convention | Introduced | Relevant to Phase 9? | Compliant? | Evidence |
|---|---|---|---|---|
| F_vert sign: negative = downward = opposing buoyancy | Phase 2 | Yes | YES | All 16 F_vert_pv values in phase9_force_table.json negative; min = -251.84 N (r=1.0), max magnitude = -862.66 N (r=1.25 pre-stall) |
| v_loop source: Phase 6 AoA=2 deg optimal | Phase 6 | Yes | YES | v_loop_baseline_ms = 3.273346 in both JSON outputs; matches phase6_sweep_table.json exactly |
| NACA interpolator: imported from Phase 5 (not reimplemented) | Phase 5 | Yes | YES | pitfall_guards_verified.NACA_imported_not_reimplemented = true; ASSERT_CONVENTION block in JSON |
| lambda_design = 0.9 | Phase 2 | Yes | YES | lambda_design = 0.9 in phase9_geometry_table.json; transitively from Phase 5 aoa_sweep_solver.py |
| Unit system: SI (N, m/s, deg) | Phase 1 | Yes | YES | _units field in both JSONs: "SI; angles in degrees; velocities in m/s" |
| Force decomposition: F_tan = L*sin(beta) - D*cos(beta); F_vert = -L*cos(beta) - D*sin(beta) | Phase 2 | Yes | YES | Eq. (09.4) matches Phase 2 convention exactly; test-value verified below |
| e_oswald = 0.85 | Phase 4 | Yes | YES | Loaded transitively via Phase 5 aoa_sweep_solver.py (confirmed in ref-phase5-solver summary) |
| Quasi-steady foil forces (k << 0.1) | Phase 2 | Yes | YES | Stated in approximations table; k ~ 0.01-0.05 unchanged |
| brentq NOT called at fixed-v_loop geometry phases | Phase 5 | Yes | YES | PITFALL-P9-BRENTQ guard: true; no brentq in differential_rotation.py |
| v_tangential_net = lambda*v_loop*(2-r), NOT r*lambda*v_loop | Phase 9 (new) | Yes | YES | PITFALL-P9-WRONG-VTAN guard documented; formula produces decreasing v_tan with r as expected |
| COROT-03: v_vertical = v_loop at all r | Phase 3 | Yes | YES (assumed) | Stated as unvalidated assumption in SUMMARY; acceptable for Phase 9 geometric sweep |
| Natural units / unit system change | N/A | No | N/A | All phases use SI throughout |

---

## Provides/Consumes Verification

### Phase 5 -> Phase 9

| Quantity | Producer Value | Consumer Value | Match |
|---|---|---|---|
| NACA 0012 interpolator | analysis/phase5/aoa_sweep_solver.py, overall_anchor_pass=True | Imported directly; gate checked before computation | PASS |
| foil AR | 4.0 | 4.0 (verified in ref-phase5-solver) | PASS |
| e_oswald | 0.85 | 0.85 (verified in ref-phase5-solver) | PASS |
| A_foil | 0.25 m^2 | 0.25 m^2 (verified in ref-phase5-solver) | PASS |
| lambda_design | 0.9 | 0.9 (geometry table) | PASS |

### Phase 6 -> Phase 9

| Quantity | Producer Value | Consumer Value | Match |
|---|---|---|---|
| v_loop at AoA=2 deg | 3.273346 m/s | 3.273346 m/s | PASS (exact) |
| F_vert_pv at AoA=2 deg | -251.8383 N | -251.838307 N (0.000% error) | PASS |
| F_tan_pv at AoA=2 deg | 250.8316 N | 250.831576 N (0.000% error) | PASS |
| beta at AoA=2 deg | 48.013 deg | 48.012788 deg | PASS |
| AoA_optimal | 2.0 deg | 2.0 deg (baseline AoA_eff at r=1.0) | PASS |
| mount_angle | 46.013 deg | 46.012788 deg (arctan(1/0.9) - 2.0) | PASS |

---

## Spot-Check Test Values (Rapid Mode)

### Check 1: F_vert sign — Phase 2 convention

**Convention:** F_vert = -L*cos(beta) - D*sin(beta), must be negative (downward, opposing buoyancy).

At r=1.0: L=354.91 N, D=19.39 N, beta=48.013 deg.
- F_vert = -(354.91 * cos(48.013°)) - (19.39 * sin(48.013°))
- cos(48.013°) = 0.6692, sin(48.013°) = 0.7431
- F_vert = -(354.91 * 0.6692) - (19.39 * 0.7431) = -237.54 - 14.41 = -251.95 N
- JSON: -251.838307 N (0.05% agreement, rounding in manual trig)
- All 16 r values: F_vert_pv_N < 0 confirmed.

**Result: PASS**

### Check 2: v_loop provenance

Phase 6 locked value (STATE.md): v_loop at AoA=2 deg = 3.273346 m/s.
Phase 9 JSON v_loop_baseline_ms = 3.273346 m/s.
Difference: 0.000%.

**Result: PASS**

### Check 3: v_tan_net formula at r=1.5

Formula: v_tan_net = lambda * v_loop * (2 - r) = 0.9 * 3.273346 * (2 - 1.5) = 0.9 * 3.273346 * 0.5 = 1.47301 m/s.
JSON: 1.473006 m/s.
Difference: <0.001%.

**Result: PASS**

### Check 4: AoA_eff at r=1.0 — baseline continuity

AoA_eff(r=1.0) = arctan(1/(lambda*(2-1.0))) - arctan(1/lambda) + AoA_optimal
= arctan(1/(0.9*1.0)) - arctan(1/0.9) + 2.0
= arctan(1/0.9) - arctan(1/0.9) + 2.0 = 2.0 deg exactly.
JSON: AoA_eff_deg = 2.0.

**Result: PASS**

### Check 5: ROADMAP scope boundary (v_loop fixed, no brentq)

STATE.md decision (Phase 9 planning): "Phase 9 uses fixed v_loop from Phase 6; Phase 10 runs coupled solver".
Phase 9 SUMMARY key-decisions: "v_loop fixed at Phase 6 AoA=2 deg value (3.273346 m/s); brentq NOT called at each r".
JSON: PITFALL-P9-BRENTQ guard = "No brentq called; v_loop fixed from Phase 6".

**Result: PASS**

### Check 6: F_tan formula

At r=1.0: F_tan = L*sin(beta) - D*cos(beta) = 354.91*0.7431 - 19.39*0.6692 = 263.64 - 12.98 = 250.66 N.
JSON: 250.831576 N (0.07% agreement — rounding in manual trig values).

**Result: PASS**

---

## Approximation Validity Check

| Approximation | Validity Bound | Phase 9 Parameter | Status |
|---|---|---|---|
| Quasi-steady (k << 0.1) | k ~ 0.01-0.05 | Unchanged from Phase 5/6 | PASS |
| NACA 0012 validity at Re~10^6 | < 5% error | Re_foil ~ 1.1e6 at r=1.0 (stated in SUMMARY) | PASS |
| COROT-03 v_vertical = v_loop | Proved for arm co-rotation | Applied to wave co-rotation — acknowledged as unvalidated | WARNING (noted, not a violation) |
| v_loop fixed (no brentq) | Phase 9 only (Phase 10 corrects) | Acknowledged explicitly: forces at r!=1.0 are upper bounds | PASS (properly scoped) |

---

## Cross-Phase Error Pattern Check

| Pattern | Check | Result |
|---|---|---|
| Sign absorbed into definition | F_vert = -L*cos(beta) - D*sin(beta) — same sign structure as Phase 2 Eq.; no sign flip at boundary | CLEAR |
| Normalization factor change | State normalization unchanged (per-vessel throughout; no N_ascending multiplier) | CLEAR |
| Coupling convention mismatch | No coupling constants; N/A | N/A |
| Factor of 2pi error | No Fourier transforms; N/A | N/A |
| Implicit assumption violated | lambda_design=0.9 within [0.3, 1.27] valid range (Phase 2); r sweep identifies stall; v_loop fixed with documented scope | CLEAR |
| Reversed foil proxy | Explicitly rejected: forbidden_proxy_reversed_foil_checked=false with note; F_vert kinematic | CLEAR |

---

## Detailed Findings

No violations detected.

**Single advisory note (not a violation):**

The COROT-03 assumption (v_vertical = v_loop at all r) was proved in Phase 3 only for arm co-rotation. Phase 9 extends it to wave co-rotation without re-derivation. The SUMMARY correctly flags this as an "unvalidated assumption." This is a known and documented limitation of the Phase 9 geometric sweep; it does not affect Phase 9 consistency with prior conventions because the assumption is transparently stated and scoped to Phase 9 only. Phase 10 will operate within the same assumption and should document it in its scope.

---

## Verdict

**Phase 9 is CONSISTENT with all accumulated project conventions.**

- F_vert sign convention (Phase 2): CONFIRMED negative at all 16 r values.
- v_loop source (Phase 6, AoA=2 deg): CONFIRMED 3.273346 m/s, 0.000% error.
- NACA interpolator (Phase 5 import): CONFIRMED not reimplemented, gate-checked.
- lambda_design = 0.9 (Phase 2): CONFIRMED throughout.
- Force decomposition formula: test-value verified to <0.1%.
- Baseline continuity: 0.000% error on F_vert and F_tan vs Phase 6.
- No convention drift detected across all relevant conventions.
- All 7 pitfall guards documented and confirmed in JSON artifacts.
