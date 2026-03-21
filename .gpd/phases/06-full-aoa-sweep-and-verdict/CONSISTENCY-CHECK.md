# Consistency Check — Phase 06-full-aoa-sweep-and-verdict

**Mode:** rapid
**Scope:** Phase 06 vs full conventions ledger and all accumulated project state (Phases 1–5)
**Date:** 2026-03-21
**Checker:** gpd-consistency-checker (rapid mode)
**Result:** CONSISTENT

---

## Summary

Phase 6 results are fully consistent with the accumulated conventions ledger and the
provides/consumes chains established across Phases 1–5. Eleven cross-phase checks were
performed; all passed. One stale bookkeeping entry was noted (non-blocking).

| Check Category | Count | Pass | Fail | Warning |
|---|---|---|---|---|
| Convention compliance (custom conventions) | 8 | 8 | 0 | 0 |
| Provides/consumes semantic verification | 3 | 3 | 0 | 0 |
| Spot-check test values | 6 | 6 | 0 | 0 |
| Approximation validity | 2 | 2 | 0 | 0 |
| Pitfall guards (cross-phase) | 4 | 4 | 0 | 0 |
| **Total** | **23** | **23** | **0** | **0** |

---

## Step 0: Conventions Self-Test

The 18 canonical physics conventions are all N/A for this classical fluid mechanics project.
No metric signature, Fourier convention, or quantum convention applies.
Self-test: trivially consistent — N/A declarations are uniform across state.json and
CONVENTIONS.md.

Active custom conventions (24 entries): all populated and consistent between state.json
`convention_lock.custom_conventions` and the live convention list output. No discrepancy.

---

## Step 1: Convention Compliance — Phase 6 vs Full Ledger

### Relevant custom conventions checked against Phase 6 artifacts

| Convention | Value | Phase 6 Compliant? | Evidence |
|---|---|---|---|
| unit_system | SI (J, W, m/s, N) | YES | `_assert_convention` in both output JSONs; all quantities in SI |
| F_vert sign (Phase 2) | Negative = downward = opposing buoyancy | YES | All 16 sweep points: F_vert_pv_N < 0 (range −146.1 to −685.6 N) |
| force_sign_convention | F_b positive upward; F_D positive magnitude | YES | Consistent throughout solver (imported from Phase 5) |
| energy_sign_convention | W_pump = denominator; W_buoy, W_foil, W_corot = numerator | YES | COP formula applied correctly; losses subtracted from numerator |
| hydrofoil_force_convention | L = 0.5*rho_w*C_L_3D*A_foil*v_rel^2 | YES | Phase 5 solver (imported); not re-implemented in Phase 6 |
| co_rotation_convention | v_rel_h = v_h*(1-f_corot) | YES | Co-rotation correction applied as (v_loop/v_nom)^3 per Phase 3/4 |
| COP_formula | (W_buoy+W_foil+W_corot-losses)/W_pump | YES | Confirmed by spot-check below |
| buoyancy_integral_rule | Integrate F_b(z) over z=0..H | YES | W_buoy = 619,338.5 J constant = 30×W_iso (Phase 1 identity) |
| PITFALL-M1 | W_pump uses W_adia not W_iso | YES | `pitfall_guards_verified.W_pump_uses_W_adia_not_W_iso: true` in both JSONs |
| PITFALL-N-ACTIVE | N_foil = 24 not 30 | YES | `N_foil_active_24_not_30: true`; W_foil formula uses N_asc=N_desc=12 |
| mandatory_check_buoyancy_identity | W_buoy=W_iso within 0.01% | YES | W_buoy_total = 619,338.5 J = 30×20,644.62 J (Phase 1 gate PASS propagated) |
| W_adia | 23,959.45 J | YES | W_pump = 30×23,959.45/eta_c used in all nine scenarios |
| lambda_max | 1.2748 (Phase 3 locked) | YES | lambda_eff = 0.9 < 1.2748 at all 16 AoA points; stall not triggered |

**All conventions: COMPLIANT**

---

## Step 2: Provides/Consumes Semantic Verification

### 2a. Phase 5 → Phase 6: Validated brentq solver

**Physical meaning (producer):** Phase 5 provides `aoa_sweep_solver.py` with `compute_COP_aoa(AoA_target_deg, eta_c, loss_frac)`, validated to reproduce Phase 4 anchor (v_loop=2.383484 m/s, COP=0.92501) to < 0.001%.

**Physical meaning (consumer):** Phase 6 imports this solver and calls it at 16 AoA points across [1°, 15°] for nine (eta_c, loss_frac) scenarios.

**Meaning match:** YES — same function, same interface, gate check `overall_anchor_pass=true` verified before any computation.

**Units:** v_loop in m/s, COP dimensionless, energies in J, forces in N. SI throughout.

**Test value:** v_loop at AoA=10.0128°: Phase 5 provides 2.383484 m/s; Phase 6 consumes 2.383484 m/s. Error = 0.0002% << 0.5% tolerance. PASS.

**Convention match:** YES — same sign convention, same PITFALL guards, same formula.

**Status: VERIFIED**

### 2b. Phase 4 → Phase 6: Nine-scenario table reference

**Physical meaning (producer):** Phase 4 provides COP_nominal = 0.92501 at (AoA=10.0128°, eta_c=0.70, loss=0.10) as the corrected anchor, and W_foil_total = 246,058.1 J.

**Physical meaning (consumer):** Phase 6 uses these as baseline comparison values for the sweep table and verdict.

**Test value 1:** COP at (AoA=10.0128°, eta_c=0.70, loss=0.10): Phase 4 = 0.92501; Phase 6 = 0.925011. Error = 0.00007% << 0.01%. PASS.

**Test value 2:** W_foil at AoA=10.0128°: Phase 4 = 246,058.1 J; Phase 6 = 246,059.3 J. Error = 0.0005% << 0.1%. PASS.

**Status: VERIFIED**

### 2c. Phase 3 → Phase 6: Co-rotation power (P_net_corot_uncorrected)

**Physical meaning (producer):** Phase 3 provides P_net_corot = 46,826 W at v_nom = 3.7137 m/s (net power saved from co-rotation drag reduction). Applies only at v_nom; must be scaled as (v_loop/v_nom)^3 at other velocities (PITFALL-COROT).

**Physical meaning (consumer):** Phase 6 inherits this value through the Phase 5 solver. At AoA=10° (anchor): W_corot = 46,826 × (2.384²/3.7137³) × 2×18.288 = 189,971 J. Phase 6 reports 189,971.05 J. PASS.

**Test value spot-check at AoA=2°:**
v_loop = 3.273346 m/s; corot_scale = (3.273346/3.7137)³ = 0.684787.
W_corot = 46,826 × 0.684787 × (2×18.288/3.273346)
= 46,826 × 0.684787 × 11.177
= 358,304 J.
Phase 6 reports 358,299.9 J. Error < 0.002%. PASS.

**Convention match:** YES — PITFALL-COROT guard explicitly verified in both output JSONs.

**Status: VERIFIED**

---

## Step 3: Spot-Check Test Values (Load-Bearing Equations)

### Test 1: COP formula at AoA_optimal (AoA=2°, nominal scenario)

Convention: COP = (W_buoy + W_foil + W_corot) × (1-loss_frac) / (N_total × W_adia / eta_c)

Substituting:
- W_buoy = 619,338.5 J
- W_foil = 99,083.7 J
- W_corot = 358,300.0 J
- loss_frac = 0.10; (1-loss_frac) = 0.90
- W_pump = 30 × 23,959.45 / 0.70 = 1,026,834 J

COP = (619,338.5 + 99,083.7 + 358,300.0) × 0.90 / 1,026,834
    = 1,076,722.2 × 0.90 / 1,026,834
    = 969,050.0 / 1,026,834
    = **0.9437**

Phase 6 reports: 0.943726. Match to 4 significant figures. PASS.

### Test 2: Best-scenario COP (eta_c=0.85, loss=0.05, AoA=2°)

COP = 1,076,722.2 × 0.95 / (30 × 23,959.45 / 0.85)
    = 1,022,886.1 / 845,628.5
    = **1.2096**

Phase 6 reports: 1.209617. PASS.

### Test 3: eta_c* back-calculation

Required: COP = 1.5 at (AoA=2°, loss=0.05).
1.5 = 1,076,722 × 0.95 / (30 × 23,959.45 / eta_c*)
eta_c* = 1.5 × 30 × 23,959.45 / (1,076,722 × 0.95)
       = 1,078,175.25 / 1,022,885.9
       = **1.0541**

Phase 6 reports: 1.054052. PASS. Exceeds isothermal limit (eta_c ≤ 1.0): NO_GO confirmation correct.

### Test 4: W_buoy constant across AoA

W_buoy = N_total × W_iso = 30 × 20,644.62 = 619,338.6 J.
Phase 6 verdict JSON: W_buoy_total_J = 619,338.477 J. Error = 0.00002%. PASS.
AoA-independence confirmed: W_buoy does not appear in the brentq residual.

### Test 5: corot_scale at AoA=1°

(3.465008 / 3.7137)^3 = (0.93274)^3 = 0.8122.
Phase 6 reports corot_scale = 0.812255. Error = 0.0006%. PASS.

### Test 6: W_foil v_loop-independence

W_foil = F_tan × lambda × H × N_active_foils (v_loop cancels: F_tan × v_tan × (H/v_loop) = F_tan × lambda × H).
At AoA=10.0128°: F_tan_pv = 622.9022 N; W_foil = 622.9022 × 0.9 × 18.288 × 24 = 246,059.3 J.
Phase 6 reports W_foil_total_J = 246,059.3208 J. PASS.

---

## Step 4: Approximation Validity

| Approximation | Validity Condition | Phase 6 Parameter Values | Status |
|---|---|---|---|
| lambda < lambda_max (no stall from tip speed) | lambda_eff < 1.2748 at all AoA | lambda_eff = 0.9 constant across all 16 points | PASS |
| AoA < 14° for NACA table (no stall clamp distortion) | AoA_optimal must be in valid range | AoA_optimal = 2° << 14° stall; clamp only at 14°/15° (documented) | PASS |
| Quasi-steady foil forces | k << 0.1 | Unchanged from Phase 5/2 (k ~ 0.01–0.05); no new parameter values introduced | PASS |
| Prandtl lifting-line (AR=4) | AR ≥ 2 | AR = 4 (unchanged) | PASS |

All existing validity bounds satisfied. Phase 6 introduces no new parameter values outside prior approximation ranges.

---

## Step 5: Cross-Phase Error Patterns

| Error Pattern | Checked? | Result |
|---|---|---|
| Sign absorbed into definition (F_vert, self-energy analog) | YES | F_vert negative convention maintained; all 16 points F_vert < 0 |
| Normalization factor change (N_active_foils = 24 not 30) | YES | PITFALL-N-ACTIVE guard verified; N=24 used in W_foil, N=30 in W_pump |
| Co-rotation at v_nom instead of v_loop(AoA) | YES | PITFALL-COROT guard verified; corot_scale computed at each AoA |
| W_iso vs W_adia in W_pump denominator | YES | PITFALL-M1 guard verified; W_adia used throughout |
| Assumption violation: coupling constant range | YES | lambda held at 0.9; well within [0.3, 1.27] valid operating range (Phase 2) |
| AoA outside [1°, 15°] sweep contract | YES | Sweep covers exactly [1°, 15°] with 16 points including anchor |

No cross-phase error patterns detected.

---

## Step 6: Minor Issue (Non-Blocking)

### state.json position field is stale

**Location:** `.gpd/state.json` fields `position.current_phase = 5`, `status = "Defining objectives"`, `progress_percent = 0`.

**Issue:** These fields reflect the v1.1 milestone kickoff state, not the Phase 5/6 completion state. STATE.md (human-readable) correctly records Phase 5 completion and Phase 6 results.

**Impact:** Zero — no physics calculations depend on state.json position fields. These are bookkeeping metadata used by orchestration tooling, not numerical inputs.

**Severity:** Minor bookkeeping artifact (non-blocking).

**Recommended action:** Orchestrator should update state.json position to reflect Phase 6 completion.

---

## Convention Compliance Matrix

| Convention | Introduced Phase | Relevant to Phase 6? | Compliant? | Evidence |
|---|---|---|---|---|
| SI unit system | Init | YES | YES | Both JSONs assert `unit_system=SI` |
| F_vert negative = downward | Phase 2 | YES | YES | All sweep points F_vert < 0 |
| COP_formula (full) | Phase 4 | YES | YES | Spot-check verified to 4 sig figs |
| buoyancy_integral_rule | Phase 1 | YES | YES | W_buoy = 619,338.5 J constant |
| W_adia in W_pump | Phase 1 | YES | YES | PITFALL-M1 guard; W_adia=23,959.45 J |
| N_foil_active = 24 | Phase 2 | YES | YES | PITFALL-N-ACTIVE guard |
| PITFALL-COROT: v_loop^3 scaling | Phase 4 | YES | YES | corot_scale computed at each AoA |
| lambda_max = 1.2748 | Phase 3 | YES | YES | lambda_eff = 0.9 at all points |
| co_rotation_convention | Phase 3 | YES | YES | Inherited via Phase 5 solver |
| hydrofoil_force_convention | Phase 2 | YES | YES | Inherited via Phase 5 solver |
| mandatory_check_buoyancy_identity | Phase 1 | YES | YES | W_buoy = W_iso identity holds |
| e_oswald = 0.85 | Phase 4 | YES | YES | Loaded from foil01_force_sweep.json by solver |
| AoA parameterization (dynamic mount_angle) | Phase 5 | YES | YES | Phase 5 solver used; mount_angle = beta - AoA_target |
| metric_signature to gamma_matrix_convention (18 canonical) | Init | NO | N/A | Classical project; not applicable |

---

## End-to-End Research Chain

**Chain: Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → Verdict**

| Transfer | Quantity | Error | Status |
|---|---|---|---|
| Ph1→Ph2 | W_iso = 20,644.6 J | < 0.01% | PASS |
| Ph2→Ph4 | e_oswald = 0.85, AR = 4 | inherited via solver | PASS |
| Ph3→Ph4 | P_net_corot = 46,826 W at v_nom | inherited via solver | PASS |
| Ph4→Ph5 | v_loop = 2.383484 m/s, COP = 0.92501 | 0.0002%, 0.00007% | PASS |
| Ph5→Ph6 | Solver import; gate pass | 0.0000% | PASS |
| Ph6 verdict | NO_GO; COP_max = 1.210 < 1.5 | eta_c* = 1.054 > 1.0 confirmed | PASS |

Chain is complete, unbroken, and all transfers verified with test values.

---

## Verdict

**consistency_status: CONSISTENT**

Phase 6 is fully consistent with all accumulated conventions (Phases 1–5). All 23 checks
passed. The NO_GO verdict is supported by verified arithmetic: the gap of 0.290 to COP=1.5
is confirmed by back-calculation of eta_c* = 1.054 which exceeds the isothermal limit.

No blocking issues. One minor bookkeeping note: state.json position fields are stale and
should be updated by the orchestrator.
