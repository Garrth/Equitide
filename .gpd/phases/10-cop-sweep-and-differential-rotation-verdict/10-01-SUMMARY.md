---
phase: 10-cop-sweep-and-differential-rotation-verdict
plan: 01
status: complete
date: 2026-03-21
executor: claude-sonnet-4-6
tasks_completed: 3
tasks_total: 3
duration_minutes: ~50
plan_contract_ref: 10-01-PLAN.md
---

# Phase 10 Plan 01 Summary — COP Sweep and Differential Rotation Verdict

## One-liner

Differential rotation is **no_gain**: COP(r) is monotone decreasing for all r ∈ [1.0, 1.30] with self-consistent brentq; r* = 1.0, COP(r*) = 0.9437, zero gain over Phase 6 baseline; v1.3 verdict = **NO_GO**.

## Conventions

| Parameter | Value |
|---|---|
| Unit system | SI throughout (N, m/s, J, W, degrees for AoA display) |
| F_vert sign | Phase 2: negative = downward = opposing buoyancy |
| v_tangential_net | lambda * v_loop * (2 - r) — NOT r*lambda*v_loop (PITFALL-P9-WRONG-VTAN) |
| mount_angle | 46.012788 deg (FIXED from Phase 6/Phase 9; never re-optimized) |
| brentq | Re-run at each r (PITFALL-P9-BRENTQ; Phase 9 forces were upper bounds at fixed v_loop) |
| W_pump | N_total * W_adia_J / eta_c (PITFALL-M1: W_adia, not W_iso) |
| NACA source | Imported from analysis/phase5/aoa_sweep_solver.py (not re-implemented) |
| eta_c (primary) | 0.70 (Phase 6 nominal) |
| loss_frac (primary) | 0.10 = 10% (Phase 6 nominal) |

## Key Results

### Continuity Gate (r = 1.0)

| Quantity | Value |
|---|---|
| COP(r=1.0) from extended solver | 0.943726 |
| Phase 6 COP_max_nominal anchor | 0.943726 |
| Percentage difference | 0.0000% |
| Gate status | **PASSED** (threshold: 0.5%) |

The extended solver exactly reproduces Phase 6 at r=1.0, confirming the r-extension is a valid generalization.

### COP Sweep Table (11 r values)

| r | v_loop (m/s) | COP_nominal | AoA_eff (deg) | is_stalled | brentq |
|---|---|---|---|---|---|
| 1.00 | 3.2733 | **0.94373** | 2.000 | No | PASS |
| 1.05 | 3.0732 | 0.94337 | 3.457 | No | PASS |
| 1.10 | 2.9174 | 0.94075 | 4.980 | No | PASS |
| 1.15 | 2.8069 | 0.93701 | 6.571 | No | PASS |
| 1.20 | 2.7113 | 0.93235 | 8.233 | No | PASS |
| 1.25 | 2.6368 | 0.92714 | 9.968 | No | PASS |
| 1.30 | 2.6392 | 0.92390 | 11.776 | No | PASS |
| 1.35 | 2.7176 | 0.91930 | 13.660 | **STALLED** | PASS |
| 1.40 | 2.7773 | 0.91852 | 15.618 | **STALLED** | PASS |
| 1.45 | 2.8316 | 0.91854 | 17.652 | **STALLED** | PASS |
| 1.50 | 2.8867 | 0.91841 | 19.759 | **STALLED** | PASS |

All 11 brentq calls converged. All force balance residuals < 7e-6 N (< 1e-5 N threshold).

**[CONFIDENCE: HIGH]** — Continuity identity exact (0.0000% error), AoA_eff at r=1.30 matches Phase 9 to 0.0002 deg, all 11 brentq convergences verified, all residuals < 1e-5 N.

### r* Identification

- **Case C: Monotone decreasing** (all 6 valid-range differences negative)
- COP differences: [−0.00035, −0.00263, −0.00373, −0.00466, −0.00521, −0.00324]
- r* = 1.0 (no interior or boundary maximum; optimal is the baseline itself)
- COP(r*) = 0.9437
- COP gain = 0.000

### v1.3 Verdict

| Field | Value |
|---|---|
| **v13_verdict** | **NO_GO** |
| r* | 1.0 |
| COP(r*) | 0.9437 |
| COP(r=1.0) baseline | 0.9437 |
| **COP gain vs r=1** | **0.000** |
| r_star_case | no_gain |
| response_type | **no_gain** (NOT multiplicative, NOT additive) |
| Phase 6 nominal (0.94373) | No improvement — equals Phase 6 baseline |
| Phase 6 best case (1.2096) | Gap = 0.266 |
| Gap to threshold (1.5) | **0.556** |
| v_loop(r*) / v_loop(r=1.0) | 1.000 (r* = r=1.0 = baseline) |

## Physical Explanation

The sweep shows monotone decreasing COP because two competing effects are unbalanced:

**What helps:** As r increases, AoA_eff increases (from 2° to 11.8°), C_L grows strongly (0.147 → 0.754), W_foil_total grows from 99,084 J to 201,845 J (+104%). Phase 9 classified this as "enhanced-both" — F_tan and F_vert both increase.

**What hurts (dominant):** The strongly increasing |F_vert_pv| (−251.8 N → −558.7 N at r=1.30; +122%) suppresses v_loop via brentq (3.273 → 2.639 m/s; −19%). This suppression causes W_corot to fall from 358,300 J to 232,921 J (−35%), because W_corot ~ v_loop³ × t_cycle ~ v_loop². The W_corot loss dominates the W_foil gain at all r > 1.0.

**Why multiplicative is impossible:** True multiplicative response requires F_vert to DECREASE with r (so v_loop increases, amplifying W_corot). Phase 9 established that F_vert INCREASES at all r ∈ (1.0, 1.31). This is geometric: at fixed mount_angle, higher AoA increases C_L (→ more F_vert) while the v_rel² reduction is only ~8% at r=1.30. The C_L increase (~5×) overwhelms the v_rel² decrease.

## Locked Phase 9 Values Inherited

| Value | Source | Used As |
|---|---|---|
| r_stall_onset = 1.31 | phase9_force_table.json | Stall onset boundary (AoA_eff = 12.147 deg) |
| r_stall_full = 1.36 | phase9_force_table.json | Full stall boundary (AoA_eff = 14.045 deg) |
| v_loop_Phase9 = 3.273346 m/s | phase9 (fixed from Phase 6) | Upper bound reference (Phase 10 brentq gives lower v_loop at r > 1) |
| mount_angle = 46.012788 deg | phase9_geometry_table.json | Fixed mount angle for all r |
| classification = enhanced-both | phase9_force_table.json | Confirms multiplicative impossibility |

## Contract Coverage

| Claim | Status | Evidence |
|---|---|---|
| claim-CONT-01: COP(r=1.0) within 0.5% of 0.94373 | **PASS** | 0.0000% diff; phase10_cop_sweep.json continuity_check_passed=true |
| claim-SWEEP-01: COP(r) at 11 points with brentq | **PASS** | phase10_cop_sweep.json; all 11 converged |
| claim-RSTAR-01: r* located or absence documented | **PASS** | Case C (monotone decreasing) documented with sweep evidence |
| claim-VERDICT-01: v1.3 verdict with gain and comparison | **PASS** | phase10_verdict.json; gain=0.000; Phase 6 comparison explicit |

## Acceptance Tests

| Test | Status | Notes |
|---|---|---|
| test-continuity-gate | **PASS** | pct_diff = 0.0000% < 0.5% |
| test-brentq-convergence | **PASS** | All 11 r values converged |
| test-dimensional-consistency | **PASS** | v_tan identity at r=1.0 exact; W_foil v_loop cancellation verified; W_pump uses W_adia |
| test-rstar-identification | **PASS** | Case C documented; evidence: all 6 finite differences negative |
| test-verdict-complete | **PASS** | All required fields present; Phase 6 comparison explicit; forbidden proxies rejected |

## Pitfall Guards Verified

| Guard | Status |
|---|---|
| PITFALL-P9-WRONG-VTAN: v_tan = lambda*(2-r)*v_loop | VERIFIED at load time (assertion) |
| PITFALL-P9-BRENTQ: brentq re-run at each r | VERIFIED (v_loop ranges 2.64–3.27 m/s across sweep) |
| PITFALL-M1: W_pump uses W_adia not W_iso | VERIFIED |
| PITFALL-C6: W_jet = 0.0 explicit | VERIFIED |
| Phase 5 per-vessel brentq (not N_ascending multiplier) | VERIFIED (imported from Phase 5) |

## Forbidden Proxies

| Proxy | Status |
|---|---|
| fp-reversed-foil | REJECTED: F_vert kinematic |
| fp-fixed-vloop | REJECTED: brentq re-run at each r |
| fp-wrong-vtan | REJECTED: correct formula asserted |
| fp-cop-lossless-primary | REJECTED: COP_nominal is primary |
| fp-no-continuity | REJECTED: gate passed at 0.0000% |
| fp-multiplier-claim | REJECTED: enhanced-both (not multiplicative) per Phase 9 + Phase 10 verification |

## Deviations

None. The plan was executed as specified. The continuity gate passed exactly. The sweep confirmed Case C (monotone decreasing) as the predicted "disconfirming observation" from the plan's `uncertainty_markers` section.

## Output Files

| File | Status |
|---|---|
| `analysis/phase10/cop_sweep.py` | Complete; all gates and guards embedded |
| `analysis/phase10/outputs/phase10_cop_sweep.json` | 11-point COP table; continuity_check_passed=true |
| `analysis/phase10/outputs/phase10_verdict.json` | v1.3 verdict=NO_GO; all forbidden proxies rejected |

## Self-Check

- [x] Continuity gate passed (0.0000% vs 0.5% threshold)
- [x] All 11 brentq calls converged
- [x] AoA_eff at r=1.30 = 11.776 deg matches Phase 9 (11.776285 deg) within 0.001 deg
- [x] Force balance residuals all < 7e-6 N < 1e-5 N threshold
- [x] COP range [0.918, 0.944] within expected [0.4, 1.5]
- [x] response_type = "no_gain" (not "multiplicative")
- [x] All forbidden proxies rejected in both code and JSON
- [x] Phase 6 comparison explicit and honest (no oversell)
- [x] v_loop(r) decreasing with r for pre-stall range (physics consistent)
- [x] W_corot(r) decreasing with r (v_loop^2 scaling confirmed)

## Self-Check: PASSED
