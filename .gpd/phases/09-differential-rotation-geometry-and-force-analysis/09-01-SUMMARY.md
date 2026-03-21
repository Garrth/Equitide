---
phase: 09-differential-rotation-geometry-and-force-analysis
plan: "01"
depth: full
one-liner: "Differential rotation geometry sweep confirms r_stall=1.31 at AoA_onset=12 deg; for r in (1.0, 1.31), wave co-rotation produces enhanced-both response (Gamma_h_ratio up to 4.48x AND |F_vert| up to 3.41x), not multiplicative; Phase 6 baseline reproduced to 0.000% error at r=1.0"

subsystem:
  - computation
  - analysis
  - validation

tags:
  - hydrofoil
  - differential-rotation
  - wave-coupling
  - aoa-sweep
  - force-decomposition
  - NACA-0012

requires:
  - phase: 05-aoa-sweep-formulation
    provides: "Phase 5 NACA 0012 interpolator, foil geometry (AR=4, e_oswald=0.85, A_foil=0.25 m^2), lambda_design=0.9; overall_anchor_pass=true gate"
  - phase: 06-full-aoa-sweep-and-verdict
    provides: "Phase 6 AoA=2 deg baseline: v_loop=3.273346 m/s, F_vert_pv=-251.8383 N, F_tan_pv=250.8316 N, beta=48.013 deg; AoA_optimal=2 deg; mount_angle=46.013 deg"

provides:
  - "v_tangential_net(r) = lambda*v_loop*(2-r) — geometric proof that wave co-rotation reduces relative tangential flow"
  - "AoA_eff(r) = arctan(1/(lambda*(2-r))) - arctan(1/lambda) + AoA_optimal — closed-form formula"
  - "r_stall_onset = 1.31 (AoA=12 deg), r_stall_full = 1.36 (AoA=14 deg)"
  - "Phase 9 geometry table: 16 r values in [1.0, 1.5], v_tan_net, v_rel, beta_eff, AoA_eff"
  - "Phase 9 force table: F_tan, F_vert, Gamma_h_ratio, F_vert_ratio, response_type at each r"
  - "Classification: enhanced-both (Gamma_h up, |F_vert| up) for r in (1.0, 1.31); negative at r >= 1.31"
  - "Max Gamma_h_ratio = 4.477 at r=1.30 (just before stall onset)"
  - "Phase 10 ready: r_stall identified, baseline reproduced, geometry and forces tabulated"

affects:
  - 10-cop-sweep-and-verdict

methods:
  added:
    - "Differential rotation geometry: v_tangential_net(r) = lambda*v_loop*(2-r) formula derived from first principles"
    - "Speed ratio r sweep with stall detection at two thresholds (onset 12 deg, full 14 deg)"
    - "Force classification taxonomy: baseline / enhanced-both / multiplicative / additive / negative"
  patterns:
    - "Phase 5 NACA interpolator imported directly (not reimplemented) — same table, same 3D correction"
    - "Gate check on Phase 5 overall_anchor_pass=true before any computation"
    - "Baseline continuity verified at r=1.0 before r != 1 computation proceeds"

key-files:
  created:
    - analysis/phase9/differential_rotation.py
    - analysis/phase9/outputs/phase9_geometry_table.json
    - analysis/phase9/outputs/phase9_force_table.json

key-decisions:
  - "v_tangential_net(r) = lambda*v_loop*(2-r): wave co-rotation adds velocity in arm direction, REDUCING relative tangential flow; NOT r*lambda*v_loop (which would decrease AoA with r)"
  - "mount_angle = 46.013 deg fixed from Phase 6 optimal; NOT re-optimized at each r (Phase 10 task)"
  - "v_loop fixed at Phase 6 AoA=2 deg value (3.273346 m/s); brentq NOT called at each r (Phase 10 task)"
  - "Classification: F_vert_ratio > 1 throughout valid sweep — response is enhanced-both, not multiplicative"
  - "r_stall_onset = 1.31 (AoA=12 deg, C_L peak); r_stall_full = 1.36 (AoA=14 deg, table end)"
  - "High-density sweep grid around r_stall (1.31–1.36 at 0.01 resolution) to locate stall precisely"

patterns-established:
  - "PITFALL-P9-WRONG-VTAN: Never use r*lambda*v_loop for v_tan_net; use lambda*(2-r)*v_loop"
  - "PITFALL-P9-BRENTQ: Phase 9 uses fixed v_loop from Phase 6; Phase 10 runs coupled solver"
  - "Phase 2 sign convention propagated: F_vert = -L*cos(beta) - D*sin(beta) < 0 always"
  - "Geometry baseline check at r=1.0 must pass to < 0.01 deg AoA tolerance before any r != 1 work"

conventions:
  - "unit_system=SI (N, m/s, deg, dimensionless ratios)"
  - "F_vert_sign=Phase2 (negative=downward=opposing_buoyancy)"
  - "v_tangential_net=lambda*v_loop*(2-r)"
  - "v_vertical=v_loop (COROT-03 preserved)"
  - "mount_angle=46.013 deg FIXED (from Phase 6)"
  - "NACA=imported from Phase 5 (NACA TR-824 table, linear interpolation)"

# Contract outcome ledger
plan_contract_ref: ".gpd/phases/09-differential-rotation-geometry-and-force-analysis/09-01-PLAN.md#/contract"

contract_results:
  claims:
    claim-GEOM-01:
      status: passed
      summary: "Apparent flow vector at speed ratio r has v_tan_net(r) = lambda*v_loop*(2-r) (geometric proof in script docstring); v_vertical = v_loop (COROT-03). AoA_eff(r) = arctan(1/(lambda*(2-r))) - arctan(1/lambda) + AoA_optimal. At r=1.0: AoA_eff = 2.0000 deg (within 0.01 deg of Phase 6 optimal). mount_angle = 46.013 deg fixed."
      linked_ids: [deliv-geometry-table, test-baseline-continuity, test-stall-boundary, ref-phase6-sweep, ref-phase6-verdict]
      evidence:
        - verifier: executor
          method: baseline_benchmark_reproduction
          confidence: high
          claim_id: claim-GEOM-01
          deliverable_id: deliv-geometry-table
          acceptance_test_id: test-baseline-continuity
          reference_id: ref-phase6-sweep
          evidence_path: "analysis/phase9/outputs/phase9_geometry_table.json"

    claim-FORCE-01:
      status: passed
      summary: "At r=1.0, Phase 5/6 NACA interpolation with identical table and 3D corrections reproduces F_vert_pv=-251.8383 N to 0.000% error and F_tan_pv=250.8316 N to 0.000% error (both well within 0.5% tolerance). F_vert_pv < 0 at all r in [1.0, 1.5] — kinematic constraint confirmed."
      linked_ids: [deliv-force-table, test-baseline-continuity, test-force-sign, ref-phase6-sweep, ref-phase5-solver]
      evidence:
        - verifier: executor
          method: benchmark_reproduction
          confidence: high
          claim_id: claim-FORCE-01
          deliverable_id: deliv-force-table
          acceptance_test_id: test-baseline-continuity
          reference_id: ref-phase6-sweep
          evidence_path: "analysis/phase9/outputs/phase9_force_table.json"

    claim-CLASS-01:
      status: passed
      summary: "Gamma_h_ratio and F_vert_ratio computed at all 16 r values. For r in (1.0, 1.31): both increase — Gamma_h_ratio rises to 4.477 (at r=1.30), F_vert_ratio rises to 3.41 (at r=1.30). Classification: enhanced-both (not multiplicative). r_stall_onset = 1.31 (within [1.0, 1.5]). Rows at r >= 1.31 classified 'negative'."
      linked_ids: [deliv-force-table, test-classification, test-stall-boundary, ref-phase6-sweep]
      evidence:
        - verifier: executor
          method: physics_consistency
          confidence: high
          claim_id: claim-CLASS-01
          deliverable_id: deliv-force-table
          acceptance_test_id: test-classification
          reference_id: ref-phase6-sweep
          evidence_path: "analysis/phase9/outputs/phase9_force_table.json"

  deliverables:
    deliv-geometry-table:
      status: passed
      path: analysis/phase9/outputs/phase9_geometry_table.json
      summary: "16-point geometry table at r in [1.0, 1.5]; baseline_check_passed=true; AoA_eff(r=1.0)=2.0 deg; r_stall_onset=1.31; r_stall_full=1.36; _assert_convention block present; pitfall_guard_WRONG_VTAN documented"
      linked_ids: [claim-GEOM-01, test-baseline-continuity, test-stall-boundary]

    deliv-force-table:
      status: passed
      path: analysis/phase9/outputs/phase9_force_table.json
      summary: "Force classification table at all 16 r values; baseline_force_check_passed=true; force_classification_table complete; classification_summary with enhanced_both_r_range and negative_r_range; forbidden_proxy_reversed_foil_checked=false; pitfall guards verified"
      linked_ids: [claim-FORCE-01, claim-CLASS-01, test-baseline-continuity, test-force-sign, test-classification, test-stall-boundary]

    deliv-script:
      status: passed
      path: analysis/phase9/differential_rotation.py
      summary: "Standalone script: imports Phase 5 NACA interpolator, derives geometry (Task 1) and computes forces (Task 2), writes both output JSONs. Gate check on Phase 5 overall_anchor_pass. Baseline continuity checks for both geometry and forces before r != 1 computation. Full ASSERT_CONVENTION block at top."
      linked_ids: [claim-GEOM-01, claim-FORCE-01, claim-CLASS-01]

  acceptance_tests:
    test-baseline-continuity:
      status: passed
      summary: "At r=1.0: AoA_eff=2.0000 deg (|error|=0.0000 deg < 0.01 deg threshold). F_vert_pv=-251.8383 N (0.0000% diff < 0.5% tolerance). F_tan_pv=250.8316 N (0.0000% diff < 0.5% tolerance). beta=48.0128 deg matches Phase 6 exactly."
      linked_ids: [claim-GEOM-01, claim-FORCE-01, deliv-geometry-table, deliv-force-table, ref-phase6-sweep]

    test-stall-boundary:
      status: passed
      summary: "r_stall_onset = 1.31 (AoA_eff = 12.147 deg >= 12 deg threshold). r_stall_full = 1.36 (AoA_eff = 14.045 deg >= 14 deg threshold). Both within [1.0, 1.5]. Expected r_stall_onset ~1.31 confirmed. All r < 1.31 marked is_stalled=false."
      linked_ids: [claim-CLASS-01, deliv-geometry-table]

    test-force-sign:
      status: passed
      summary: "F_vert_pv < 0 at all 16 r values in sweep. At r=1.0: F_vert=-251.84 N; at r=1.5: F_vert=-574.96 N. F_tan_pv > 0 at r=1.0 (F_tan=250.83 N). Kinematic constraint holds throughout sweep."
      linked_ids: [claim-FORCE-01, deliv-force-table]

    test-classification:
      status: passed
      summary: "Gamma_h_ratio > 1.0 at all r in (1.0, 1.31) — monotonically increases from 1.701 (r=1.05) to 4.477 (r=1.30). F_vert_ratio > 1.0 at all r > 1.0 (observed: 1.603 at r=1.05 up to 3.413 at r=1.30). Classification: enhanced-both for r in (1.0, 1.31); negative for r >= 1.31. Pre-execution prediction (F_vert_ratio > 1) confirmed."
      linked_ids: [claim-CLASS-01, deliv-force-table]

  references:
    ref-phase6-sweep:
      status: completed
      completed_actions: [read, compare, use-as-baseline]
      missing_actions: []
      summary: "Loaded phase6_sweep_table.json: v_loop=3.273346 m/s, F_vert_pv=-251.8383 N, F_tan_pv=250.8316 N, beta=48.013 deg at AoA=2 deg. Used as r=1.0 baseline. Reproduced to 0.000% error."

    ref-phase6-verdict:
      status: completed
      completed_actions: [read]
      missing_actions: []
      summary: "Loaded phase6_verdict.json: AoA_optimal=2.0 deg confirmed. mount_angle = 48.013 - 2.0 = 46.013 deg used as fixed mount angle."

    ref-phase5-solver:
      status: completed
      completed_actions: [import, verify-same-table]
      missing_actions: []
      summary: "Imported interpolate_naca, foil_AR=4.0, e_oswald=0.85, A_foil=0.25, lambda_design=0.9 from aoa_sweep_solver.py. Verified foil_AR=4.0, e_oswald=0.85 exactly. Same NACA TR-824 table as Phase 5/6."

    ref-phase5-anchor:
      status: completed
      completed_actions: [read, gate-check]
      missing_actions: []
      summary: "Loaded phase5_anchor_check.json: overall_anchor_pass=True confirmed. Gate check passed before any Phase 9 computation proceeded."

    ref-phase2-summary:
      status: completed
      completed_actions: [verify-loaded-by-solver]
      missing_actions: []
      summary: "lambda_design=0.9, foil geometry loaded transitively via Phase 5 solver imports. Phase 5 aoa_sweep_solver.py loads phase2_summary_table.json directly."

  forbidden_proxies:
    fp-reversed-foil:
      status: rejected
      notes: "F_vert_pv < 0 at ALL 16 r values. Confirmed kinematic: reversed foil cannot change F_vert sign. Noted explicitly in force_table JSON (forbidden_proxy_reversed_foil_checked=false, with explanatory note)."

    fp-brentq-at-each-r:
      status: rejected
      notes: "No brentq call anywhere in differential_rotation.py. v_loop fixed at 3.273346 m/s from Phase 6 throughout. PITFALL-P9-BRENTQ guard documented in ASSERT_CONVENTION and JSON."

    fp-aoa-anchor-not-optimal:
      status: rejected
      notes: "Used AoA_optimal=2.0 deg (Phase 6) as baseline, NOT Phase 5 anchor AoA=10.0128 deg. Loaded v_loop=3.273346 m/s from phase6_sweep_table.json at AoA=2.0 entry."

    fp-positive-tangential:
      status: rejected
      notes: "Used v_tangential_net=lambda*(2-r)*v_loop throughout. PITFALL-P9-WRONG-VTAN guard documented. Formula gives v_tan_net decreasing from 2.946 m/s (r=1) to 1.473 m/s (r=1.5), matching expected stall at r~1.31."

  uncertainty_markers:
    weakest_anchors:
      - "Phase 9 forces computed at fixed v_loop from Phase 6 (3.273346 m/s). At r != 1.0, the self-consistent v_loop (Phase 10) will differ — Phase 9 forces are approximate for r != 1.0."
      - "r_stall determination depends on AoA_stall threshold (12 deg onset vs 14 deg full). Both identified: 1.31 and 1.36."
    unvalidated_assumptions:
      - "COROT-03 vertical flow preservation applies at all r in [1.0, 1.5]: v_vertical = v_loop regardless of wave co-rotation fraction. (Proved in Phase 3 for arm co-rotation; assumed to hold for wave co-rotation.)"
    disconfirming_observations:
      - "None triggered: AoA_eff(r=1.0) = 2.0000 deg (error < 0.0001 deg); force baseline 0.000% error. All disconfirming thresholds safely passed."

comparison_verdicts:
  - subject_id: test-baseline-continuity
    subject_kind: acceptance_test
    subject_role: decisive
    reference_id: ref-phase6-sweep
    comparison_kind: benchmark
    metric: relative_error_force
    threshold: "<= 0.005"
    verdict: pass
    recommended_action: "Proceed to Phase 10 COP sweep"
    notes: "F_vert error = 3e-6 (0.0003%), F_tan error = 1e-5 (0.001%). Both far below 0.5% threshold. Phase 9 is consistent with Phase 6 at r=1.0."

  - subject_id: test-stall-boundary
    subject_kind: acceptance_test
    subject_role: decisive
    reference_id: ref-phase6-sweep
    comparison_kind: physics-consistency
    metric: r_stall_within_sweep
    threshold: "r_stall in [1.0, 1.5]"
    verdict: pass
    recommended_action: "Use r_stall_onset=1.31 as valid regime boundary for Phase 10"
    notes: "r_stall_onset=1.31 (predicted ~1.31), r_stall_full=1.36 (predicted ~1.36). Both within sweep range."

  - subject_id: test-classification
    subject_kind: acceptance_test
    subject_role: decisive
    reference_id: ref-phase6-sweep
    comparison_kind: physics-consistency
    metric: Gamma_h_ratio_monotonicity
    threshold: "Gamma_h_ratio > 1.0 for all r in (1.0, r_stall)"
    verdict: pass
    recommended_action: "Report enhanced-both as the observed response type; update ROADMAP classification"
    notes: "Gamma_h monotone increasing from 1.701 (r=1.05) to 4.477 (r=1.30). F_vert_ratio also > 1 (predicted by pre-execution analysis: C_L triples while v_rel^2 drops only ~8%). Classification = enhanced-both, not multiplicative."

duration: "~35min"
completed: "2026-03-21"
---

# Phase 9 Plan 01: Differential Rotation Geometry and Force Analysis Summary

**Differential rotation geometry sweep confirms r_stall=1.31 (AoA_onset=12 deg) and r_stall_full=1.36 (AoA=14 deg); wave co-rotation produces enhanced-both response (Gamma_h up to 4.48x AND |F_vert| up to 3.41x) for r in (1.0, 1.31); Phase 6 baseline reproduced to 0.000% at r=1.0**

## Performance

- **Duration:** ~35 min
- **Started:** 2026-03-21
- **Completed:** 2026-03-21
- **Tasks:** 2
- **Files created:** 3

## Key Results

- **r_stall_onset = 1.31** (AoA_eff = 12.147 deg >= 12 deg onset); **r_stall_full = 1.36** (AoA_eff = 14.045 deg). Both within expected [1.31, 1.36] range.
- **Classification: enhanced-both** for r in (1.0, 1.31). Gamma_h_ratio increases monotonically from 1.70 (r=1.05) to **4.48 at r=1.30**. F_vert_ratio also increases from 1.60 to **3.41** — both useful (torque) and harmful (opposing buoyancy) forces grow. NOT multiplicative (F_vert does not decrease).
- **Baseline continuity PASSED**: AoA_eff(r=1.0) = 2.0000 deg, F_vert = -251.8383 N (0.000% error), F_tan = 250.8316 N (0.000% error) — perfect match to Phase 6.
- **Key geometry formula**: v_tangential_net(r) = lambda * v_loop * (2 - r). Wave co-rotation reduces relative tangential flow, increasing AoA_eff from 2 deg at r=1.0 toward stall at r=1.31.

## Task Commits

1. **Task 1: Vector geometry derivation and geometry table (WAVE-01)** - `aed1edb`
2. **Task 2: Force computation and classification table (WAVE-02)** - `eee1d6f`

## Files Created/Modified

- `analysis/phase9/differential_rotation.py` — Main script: geometry derivation, NACA force computation, classification; imports Phase 5 solver
- `analysis/phase9/outputs/phase9_geometry_table.json` — 16-point geometry sweep (r in [1.0, 1.5])
- `analysis/phase9/outputs/phase9_force_table.json` — Force classification table with Gamma_h_ratio, F_vert_ratio, response_type at each r

## Next Phase Readiness

- **phase10_ready: true** — r_stall_onset=1.31 and r_stall_full=1.36 identified; geometry and forces tabulated at 16 r values; baseline continuity confirmed
- Phase 10 will run the coupled brentq solver at each r to find self-consistent v_loop(r), then compute COP(r); Phase 9 results serve as the geometric input
- Phase 10 should use r_stall_onset=1.31 as the valid regime upper bound for COP optimization

## Contract Coverage

- Claims advanced: claim-GEOM-01 → passed; claim-FORCE-01 → passed; claim-CLASS-01 → passed
- Deliverables produced: deliv-geometry-table → analysis/phase9/outputs/phase9_geometry_table.json; deliv-force-table → analysis/phase9/outputs/phase9_force_table.json; deliv-script → analysis/phase9/differential_rotation.py
- Acceptance tests: test-baseline-continuity → passed; test-stall-boundary → passed; test-force-sign → passed; test-classification → passed
- References surfaced: ref-phase6-sweep → read/compare/use-as-baseline; ref-phase6-verdict → read; ref-phase5-solver → import/verify; ref-phase5-anchor → gate-check; ref-phase2-summary → verify-loaded-by-solver
- Forbidden proxies rejected: fp-reversed-foil, fp-brentq-at-each-r, fp-aoa-anchor-not-optimal, fp-positive-tangential — all rejected
- Decisive comparisons: baseline continuity (pass, 0.000% error); stall boundary (pass, r=1.31 in [1.0,1.5]); classification (pass, Gamma_h monotone, enhanced-both confirmed)

## Equations Derived

**Eq. (09.1): Tangential relative flow at speed ratio r**

$$
v_{\text{tan,net}}(r) = \lambda \cdot v_{\text{loop}} \cdot (2 - r)
$$

Wave co-rotation adds water velocity in the arm direction, reducing the foil's relative tangential flow. At r=1.0: recovers Phase 6 baseline. At r=1.5: v_tan = 0.5*lambda*v_loop.

**Eq. (09.2): Apparent inflow angle at speed ratio r**

$$
\beta_{\text{eff}}(r) = \arctan\!\left(\frac{v_{\text{loop}}}{\lambda \cdot v_{\text{loop}} \cdot (2-r)}\right) = \arctan\!\left(\frac{1}{\lambda(2-r)}\right)
$$

**Eq. (09.3): Effective angle of attack at speed ratio r**

$$
\text{AoA}_{\text{eff}}(r) = \beta_{\text{eff}}(r) - \underbrace{\left[\arctan\!\left(\frac{1}{\lambda}\right) - \text{AoA}_{\text{optimal}}\right]}_{\text{mount\_angle} = 46.013°}
$$

At r=1.0: AoA_eff = 2.000 deg (Phase 6 optimal). At r=r_stall_onset=1.31: AoA_eff = 12.147 deg (onset stall).

**Eq. (09.4): Force decomposition (Phase 2 convention)**

$$
F_{\text{tan}} = L\sin\beta - D\cos\beta \quad [\text{positive: drives shaft}]
$$
$$
F_{\text{vert}} = -L\cos\beta - D\sin\beta \quad [\text{negative: opposes buoyancy, always}]
$$

## Validations Completed

1. **Baseline continuity (DECISIVE GATE)**: At r=1.0, AoA_eff=2.0000 deg (Phase 6 value), F_vert=-251.8383 N (0.000% error), F_tan=250.8316 N (0.000% error). Phase 6 baseline reproduced exactly.
2. **r=1.5 check**: AoA_eff = 19.76 deg >> stall, v_tan_net = 1.473 m/s = 0.5*lambda*v_loop (consistent with (2-1.5)*0.9*3.273 = 1.473 ✓).
3. **r=1.3 stall proximity**: AoA_eff = 11.776 deg (< 12 deg onset), computed value at r=1.31 = 12.147 deg (> 12 deg). Stall transition well-resolved.
4. **Dimensional check**: q = 0.5 * 998.2 * 4.4038^2 * 0.25 = 2419.86 N. F_vert = -2419.86 * (0.1467 * cos(48.01°) + 0.0080 * sin(48.01°)) = -251.84 N ✓
5. **F_vert sign**: All 16 r values: F_vert_pv < 0 (kinematic constraint confirmed, no violations).
6. **Gamma_h monotonicity**: Increases from 1.0 (r=1.0) to 4.477 (r=1.30) — monotone in valid regime.
7. **Phase 5 gate check**: overall_anchor_pass=true verified before any computation.
8. **PITFALL-P9-WRONG-VTAN**: v_tangential_net uses (2-r) factor confirmed; increasing r reduces v_tan_net (tested: 2.946, 2.799, 2.651, ..., 1.473 m/s ✓).

## Decisions Made

- **v_tangential_net formula**: Used lambda*v_loop*(2-r) per ROADMAP specification and geometric proof. Wave co-rotation in same direction as arm reduces relative flow.
- **Fixed v_loop**: Used Phase 6 AoA=2 deg value (3.273346 m/s) throughout. Phase 10 will run brentq at each r for self-consistent v_loop(r).
- **mount_angle**: Fixed at 46.013 deg from Phase 6 optimal. Not re-optimized per r.
- **Classification taxonomy**: F_vert_ratio > 1.0 throughout valid regime — classified as "enhanced-both" (both Gamma_h and |F_vert| increase). Pre-execution contract predicted this correctly.
- **Stall thresholds**: Two thresholds reported (onset 12 deg, full 14 deg). Both identified within sweep: 1.31 and 1.36.

## Deviations from Plan

None — plan executed exactly as written. All backtracking triggers remained silent (baseline check passed, Gamma_h monotone, F_vert negative throughout).

**Key observation confirmed vs. pre-execution analysis:** The plan's verification section (lines 675–721) correctly predicted F_vert_ratio > 1.0 (C_L triples from 2° to ~12° while v_rel^2 decreases only ~8%, net |F_vert| increases ~3.4x). The "enhanced-both" classification was anticipated and confirmed.

## Issues Encountered

None.

## Key Quantities and Uncertainties

| Quantity | Symbol | Value | Uncertainty | Source | Valid Range |
|---|---|---|---|---|---|
| Stall onset speed ratio | r_stall_onset | 1.31 | ±0.005 (grid resolution 0.01) | AoA_eff >= 12 deg criterion | r sweep [1.0, 1.5] |
| Stall full speed ratio | r_stall_full | 1.36 | ±0.005 (grid resolution 0.01) | AoA_eff >= 14 deg criterion | r sweep [1.0, 1.5] |
| Max Gamma_h_ratio | Gamma_h_ratio | 4.477 | Systematic (fixed v_loop) | At r=1.30, just before stall | r in [1.0, 1.31) |
| Max F_vert_ratio | F_vert_ratio | 3.413 | Systematic (fixed v_loop) | At r=1.30 | r in [1.0, 1.31) |
| Baseline F_vert error | — | 0.000% | — | vs Phase 6 -251.8383 N | r=1.0 only |
| AoA_eff at r=1.30 | AoA_eff | 11.776 deg | <0.01 deg | Geometric formula | Pre-stall |
| AoA_eff at r=1.31 | AoA_eff | 12.147 deg | <0.01 deg | Geometric formula | Stall onset |

Note: All force values at r != 1.0 have systematic uncertainty from using fixed v_loop (Phase 6 value). Phase 10 will correct this with the self-consistent brentq solution at each r.

## Approximations Used

| Approximation | Valid When | Error Estimate | Breaks Down At |
|---|---|---|---|
| Fixed v_loop = 3.273346 m/s | Phase 9 geometric sweep only | O(v_loop variation) ~unknown | Phase 10 will quantify; changes at each r |
| Quasi-steady foil forces | k ~ 0.01-0.05 << 0.1 | < 5% | High reduced frequency (not relevant here) |
| NACA 0012 at Re ~ 10^6 | Re_foil = v_rel*chord/nu = 4.4*0.25/(1.004e-6) ~ 1.1e6 | < 5% table accuracy | Stall regime (clamped at 14 deg) |
| Fixed mount_angle = 46.013 deg | Phase 6 optimal AoA=2 deg operating point | Exact for r=1.0 | Phase 10 may re-optimize per r |
| COROT-03: v_vertical = v_loop at all r | Wave co-rotation in same plane as arm rotation | Assumed; not re-derived here | If wave adds vertical component (not the case per ROADMAP) |

## Open Questions

- **Phase 10 self-consistent v_loop(r)**: At r != 1.0, the terminal velocity changes because F_vert changes. Phase 10's brentq solver will find v_loop(r) at each r, giving corrected forces and COP(r).
- **Enhanced-both implications for COP**: Gamma_h increases (good for shaft power) but |F_vert| also increases (bad, reduces v_loop). The net COP(r) effect requires Phase 10's coupled solution.
- **Optimal r for COP**: The maximum COP(r) may be below r_stall where the Gamma_h benefit outweighs the |F_vert| penalty. Phase 10 will find r_COP_max.
- **Wave pump energy accounting**: Phase 9 is kinematic (geometry and force only). The energy cost of driving water at r > 1 is not accounted. v1.3 states no energy accounting for the rotation source; this remains a known caveat.

## Uncertainty Budget

**r_stall_onset = 1.31:**
- Central value: 1.31 (first r in grid where AoA_eff >= 12.0 deg)
- Grid resolution: 0.01 (sweep step near stall is 0.01 from 1.30 to 1.36)
- Uncertainty: ±0.005 (half grid step)
- AoA_eff at r=1.30 is 11.776 deg (< 12 deg, valid), at r=1.31 is 12.147 deg (> 12 deg, onset stall)
- The continuous r_stall_onset (exact) is between 1.30 and 1.31.

**Gamma_h_ratio and F_vert_ratio at r != 1.0:**
- These values are computed at fixed v_loop = 3.273346 m/s (Phase 6 value)
- The self-consistent v_loop(r) (Phase 10) will be lower than this at r > 1 because |F_vert| increases with r, further reducing the vessel ascent speed
- Consequence: Phase 9 OVERESTIMATES Gamma_h_ratio (forces larger due to higher v_loop) and OVERESTIMATES |F_vert_ratio| similarly
- Both ratios are upper bounds relative to the Phase 10 self-consistent result
- Propagation method: qualitative (direction known, magnitude unknown until Phase 10)

---

_Phase: 09-differential-rotation-geometry-and-force-analysis_
_Completed: 2026-03-21_

## Self-Check: PASSED

- [x] phase9_geometry_table.json exists and baseline_check_passed=true
- [x] phase9_force_table.json exists and baseline_force_check_passed=true
- [x] differential_rotation.py committed at aed1edb
- [x] phase9_geometry_table.json committed at aed1edb
- [x] phase9_force_table.json committed at eee1d6f
- [x] AoA_eff(r=1.0) = 2.0000 deg (within 0.01 deg ✓)
- [x] F_vert(r=1.0) = -251.8383 N (0.000% error, within 0.5% ✓)
- [x] F_tan(r=1.0) = 250.8316 N (0.000% error, within 0.5% ✓)
- [x] r_stall_onset = 1.31 (within [1.0, 1.5] ✓)
- [x] r_stall_full = 1.36 (within [1.0, 1.5] ✓)
- [x] Gamma_h_ratio > 1.0 at all r in (1.0, 1.31) ✓
- [x] F_vert < 0 at all 16 r values ✓
- [x] No brentq called; no reversed foil proxy; no r*lambda*v_loop formula ✓
- [x] NACA table imported from Phase 5 (not reimplemented) ✓
- [x] Phase 5 gate check passed (overall_anchor_pass=true) ✓

## Validation: PASSED

Physics validation gates:
1. Geometry closure at r=1.0: v_tan=2.946 m/s → v_rel=4.404 m/s → beta=48.013° → AoA=2.000° ✓
2. AoA at r=1.0: beta - mount_angle = 48.013 - 46.013 = 2.000° ✓
3. Stall estimate: arctan(1/(0.9*(2-1.31))) - 46.013 + 48.013 ≈ 12.15° ≈ 12° ✓
4. Force sign: F_vert < 0 at all r (kinematic constraint, Phase 2 convention) ✓
5. Gamma_h monotone: increases from 1.00 → 4.477 as AoA_eff goes from 2° to 11.8° ✓
6. Dimensional: q = 2419.86 N, F_vert = -251.84 N at r=1.0 ✓
7. Forbidden proxies: all 4 rejected and documented ✓
