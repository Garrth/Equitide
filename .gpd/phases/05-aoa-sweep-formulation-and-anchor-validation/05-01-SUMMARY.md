---
phase: 05-aoa-sweep-formulation-and-anchor-validation
plan: "01"
depth: complex
one-liner: "AoA-parameterized brentq solver reproduces Phase 4 anchor (v_loop=2.383484 m/s, COP=0.92501, F_vert=-663.86 N) to within 0.001% — all three VALD-01 tolerances pass; solver validated for Phase 6 sweep"
subsystem:
  - derivation
  - numerics
  - validation
tags:
  - hydrofoil
  - brentq
  - force-balance
  - AoA-parameterization
  - anchor-check

requires:
  - phase: 01-air-buoyancy-and-fill
    provides: F_b_avg_N=1128.86 N, v_terminal_nominal=3.7137 m/s, W_adia_J=23959.45 J
  - phase: 02-hydrofoil-torque
    provides: NACA 0012 table polars, foil geometry (AR=4, e_oswald=0.85), N_ascending=12
  - phase: 03-co-rotation
    provides: P_net_corot_W_uncorrected=46826.0 W at v_nominal
  - phase: 04-system-energy-balance
    provides: anchor v_loop=2.383479 m/s, F_vert=-663.8588 N, AoA=10.0128 deg, COP=0.92501

provides:
  - "AoA-parameterized brentq solver: solve_v_loop_aoa(AoA_target_deg)"
  - "Full COP computation: compute_COP_aoa(AoA_target_deg, eta_c, loss_frac)"
  - "Phase 4 anchor validation: VALD-01 all three tolerances pass"
  - "F_vert sign confirmed negative for all AoA in [1,15] deg (claim-ANAL-01)"
  - "Phase 5 module path: analysis/phase5/aoa_sweep_solver.py (importable for Phase 6)"

affects:
  - 06-aoa-sweep-and-verdict

methods:
  added:
    - "AoA parameterization: AoA_target is the free parameter; mount_angle = beta - AoA_target (dynamic)"
    - "scipy.optimize.brentq with xtol=1e-8, rtol=1e-8 for coupled v_loop solution"
    - "Prandtl lifting-line: C_L_3D = C_L_2D/(1+2/AR); C_D_i = C_L_3D^2/(pi*e_oswald*AR)"
  patterns:
    - "Per-vessel force balance: F_b_avg + F_vert_pv - F_drag_hull_pv = 0 (not N_ascending multiplier)"
    - "Co-rotation v^3 scaling: P_net_corot_corrected = P_net_corot_uncorrected * (v_loop_c/v_nom)^3"

key-files:
  created:
    - analysis/phase5/aoa_sweep_solver.py
    - analysis/phase5/outputs/phase5_anchor_check.json
  modified: []

key-decisions:
  - "Per-vessel force balance (not N_ascending multiplier): consistent with Phase 4 working code"
  - "F_vert_N in Phase 4 JSON stores per-vessel value; anchor comparison uses per-vessel"
  - "e_oswald=0.85 loaded from foil01_force_sweep.json foil_geometry section"
  - "N_total_vessels=30 hardcoded as physical constant (pump fill cycle, not from JSON)"

patterns-established:
  - "Pattern: force balance is always per-vessel for terminal velocity; energy balance uses N_ascending/N_total"
  - "Pattern: brentq bracket [0.05*v_nom, 2.0*v_nom] with fallback log-space scan"
  - "Pattern: ASSERT_CONVENTION block at top of every Phase 5+ script"

conventions:
  - "unit_system=SI: N, m/s, J, W, rad/s, dimensionless"
  - "F_vert_sign=Phase2: negative = downward = opposing buoyancy"
  - "AoA_parameterization: mount_angle computed dynamically as beta(v_loop) - AoA_target"
  - "NACA: table interpolation from TR-824; NOT thin-airfoil 2pi formula"
  - "lambda_held_constant=0.9 (Phase 4 design value)"
  - "brentq: xtol=1e-8, rtol=1e-8"

plan_contract_ref: ".gpd/phases/05-aoa-sweep-formulation-and-anchor-validation/05-01-PLAN.md#/contract"

contract_results:
  claims:
    claim-ANAL-01:
      status: passed
      summary: "F_vert = -(L*cos(beta) + D*sin(beta)) < 0 verified at AoA=1,5,10,15 deg; sign is always negative (downward, opposing buoyancy) for all lambda=0.9, AoA in [1,15] deg"
      linked_ids: [deliv-aoa-solver, test-fvert-sign, ref-phase2-json]
      evidence:
        - verifier: phase5-anchor-check
          method: direct assertion + sign_checks_AoA_1_5_10_15_deg
          confidence: high
          claim_id: claim-ANAL-01
          deliverable_id: deliv-aoa-solver
          acceptance_test_id: test-fvert-sign
          evidence_path: "analysis/phase5/outputs/phase5_anchor_check.json"

    claim-ANAL-02:
      status: passed
      summary: "brentq solver parameterized by AoA_target finds per-vessel equilibrium v_loop; mount_angle = beta(v_loop) - AoA_target computed at each brentq evaluation (confirmed by anchor match)"
      linked_ids: [deliv-aoa-solver, test-brentq-anchor, ref-phase4-sys01, ref-phase4-summary]
      evidence:
        - verifier: phase5-anchor-check
          method: anchor benchmark reproduction
          confidence: high
          claim_id: claim-ANAL-02
          deliverable_id: deliv-aoa-solver
          acceptance_test_id: test-brentq-anchor
          evidence_path: "analysis/phase5/outputs/phase5_anchor_check.json"

    claim-VALD-01:
      status: passed
      summary: "At AoA=10.0128 deg: v_loop=2.383484 m/s (0.0002% < 0.5% tol), F_vert=-663.862 N (0.0005% < 1.0% tol), COP=0.92501 (0.00007% < 0.5% tol) — all three tolerances pass"
      linked_ids: [deliv-anchor-json, test-brentq-anchor, test-cop-anchor, test-fvert-anchor]
      evidence:
        - verifier: phase5-anchor-check
          method: benchmark reproduction against Phase 4 JSON values
          confidence: high
          claim_id: claim-VALD-01
          deliverable_id: deliv-anchor-json
          acceptance_test_id: test-brentq-anchor
          evidence_path: "analysis/phase5/outputs/phase5_anchor_check.json"

  deliverables:
    deliv-aoa-solver:
      status: passed
      path: analysis/phase5/aoa_sweep_solver.py
      summary: "Python module with ASSERT_CONVENTION block, 5 functions (interpolate_naca, get_foil_forces_aoa, F_net_residual, solve_v_loop_aoa, compute_COP_aoa), sign guards, and anchor check main block. Importable by Phase 6."
      linked_ids: [claim-ANAL-01, claim-ANAL-02, test-fvert-sign, test-brentq-anchor]

    deliv-anchor-json:
      status: passed
      path: analysis/phase5/outputs/phase5_anchor_check.json
      summary: "JSON with overall_anchor_pass=true, all three tolerance checks passed, sign_checks for AoA=1,5,10,15 all pass, 7 pitfall guards all true"
      linked_ids: [claim-VALD-01, test-cop-anchor, test-fvert-anchor]

  acceptance_tests:
    test-fvert-sign:
      status: passed
      summary: "F_vert_pv < 0 (negative) at AoA=1,5,10,15 deg: -146.1, -472.2, -663.7, -668.0 N respectively. All pass."
      linked_ids: [claim-ANAL-01, deliv-aoa-solver]

    test-brentq-anchor:
      status: passed
      summary: "solve_v_loop_aoa(10.0128) = 2.383484 m/s; Phase 4 anchor = 2.383479 m/s; diff = 0.0002% < 0.5%"
      linked_ids: [claim-ANAL-02, claim-VALD-01, deliv-anchor-json, ref-phase4-sys01]

    test-cop-anchor:
      status: passed
      summary: "compute_COP_aoa(10.0128, eta_c=0.70, loss_frac=0.10) = 0.92501; Phase 4 = 0.92501; diff = 0.00007% < 0.5%; in [0.920, 0.930]"
      linked_ids: [claim-VALD-01, deliv-anchor-json, ref-phase4-summary]

    test-fvert-anchor:
      status: passed
      summary: "F_vert_pv at anchor = -663.862 N; Phase 4 = -663.8588 N; diff = 0.0005% < 1.0%"
      linked_ids: [claim-VALD-01, deliv-anchor-json, ref-phase4-sys01]

  references:
    ref-phase2-json:
      status: completed
      completed_actions: [read, compare]
      missing_actions: []
      summary: "foil01_force_sweep.json read: foil geometry (AR=4, e_oswald=0.85, A_foil=0.25 m^2) and NACA table used identically to Phase 4. e_oswald loaded from this file."

    ref-phase4-sys01:
      status: completed
      completed_actions: [read, compare]
      missing_actions: []
      summary: "sys01_coupled_velocity.json read: anchor values v_loop=2.383479, F_vert=-663.8588, AoA=10.0128 loaded dynamically. All three within tolerance."

    ref-phase4-summary:
      status: completed
      completed_actions: [read, compare]
      missing_actions: []
      summary: "phase4_summary_table.json read: COP_system_nominal_corrected=0.92501, P_net_corot_W_uncorrected=46826.0, W_adia_J (from p4 component table). COP anchor within 0.5% tolerance."

    ref-phase1-json:
      status: completed
      completed_actions: [read]
      missing_actions: []
      summary: "phase1_summary_table.json read: F_b_avg_N, v_terminal_nominal_ms, W_buoy_J, W_adia_J, W_iso_J loaded correctly."

    ref-phase2-summary:
      status: completed
      completed_actions: [read]
      missing_actions: []
      summary: "phase2_summary_table.json read: N_ascending=12, N_descending=12, lambda_design=0.9, r_arm_m=3.66, H_m=18.288, foil geometry."

    ref-phase3-json:
      status: completed
      completed_actions: [read]
      missing_actions: []
      summary: "phase3_summary_table.json read: P_net_at_fss_W=46826.0 W loaded; cross-checked against Phase 4 summary (match within 0.1%)."

  forbidden_proxies:
    proxy-fvert-zero:
      status: rejected
      notes: "F_vert computed from full foil forces at every v_loop; never set to zero"

    proxy-fixed-vloop:
      status: rejected
      notes: "brentq called at each AoA_target; v_loop computed fresh each time"

    proxy-reversed-foil:
      status: rejected
      notes: "Not referenced; F_vert is kinematic (lift perpendicular to v_rel)"

    proxy-cop-lossless-primary:
      status: rejected
      notes: "COP_nominal (eta_c=0.70, loss_frac=0.10) is the primary metric; lossless not reported as primary"

    proxy-hardcoded-anchor:
      status: rejected
      notes: "All anchor values loaded from JSON: s1['v_loop_corrected_ms'], s1['F_vert_N'], p4['SYS-02_energy_balance']['COP_system_nominal_corrected']"

    proxy-mount-angle-prefixed:
      status: rejected
      notes: "mount_angle = beta_deg - AoA_target_deg computed at each get_foil_forces_aoa call (diagnostic only); never prefixed at 38 deg"

  uncertainty_markers:
    weakest_anchors:
      - "NACA 0012 table: coarse discretization (0,2,4,5,6,7,8,9,10,12,14 deg); linear interp error O(0.5%) in C_L at intermediate AoA"
      - "A_frontal=0.163998 m^2 derived from terminal velocity balance; 5% uncertainty propagates ~2% to v_loop"
    unvalidated_assumptions:
      - "Quasi-steady foil forces (validated for k<<0.1 in Phase 2, not re-checked here)"
      - "Tacking symmetry: descending foil work = ascending foil work (Phase 2 confirmation)"
    competing_explanations: []
    disconfirming_observations:
      - "If anchor check had failed at >0.5%: would indicate brentq parameterization error or NACA mismatch — did not occur"
      - "Per-vessel vs total force balance ambiguity in plan pseudocode: resolved by comparison with Phase 4 working code"

comparison_verdicts:
  - subject_id: claim-VALD-01
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-phase4-sys01
    comparison_kind: benchmark
    metric: relative_error
    threshold: "<= 0.005 for v_loop and COP; <= 0.01 for F_vert"
    verdict: pass
    recommended_action: "Proceed to Phase 6 AoA sweep"
    notes: "v_loop error 0.0002%, F_vert error 0.0005%, COP error 0.00007% — all far below tolerance"

duration: 45min
completed: 2026-03-19
---

# Phase 5 Plan 01: AoA Sweep Formulation and Anchor Validation Summary

**AoA-parameterized brentq solver reproduces Phase 4 anchor (v_loop=2.383484 m/s, COP=0.92501, F_vert=-663.86 N) to within 0.001% — all three VALD-01 tolerances pass; solver validated for Phase 6 sweep**

## Performance

- **Duration:** ~45 min
- **Started:** 2026-03-19
- **Completed:** 2026-03-19
- **Tasks:** 2
- **Files modified:** 2

## Key Results

- anchor check PASS: v_loop=2.383484 m/s (0.0002% < 0.5% tolerance); COP=0.92501 (0.00007% < 0.5%); F_vert=-663.862 N (0.0005% < 1.0%)
- F_vert sign confirmed negative at AoA=1,5,10,15 deg: -146.1, -472.2, -663.7, -668.0 N per vessel
- Limiting case AoA=0: v_loop=3.691 m/s (near v_nom=3.714, as expected from pure drag), F_vert=-164.7 N (C_L=0)
- All 7 pitfall guards confirmed true in JSON

## Task Commits

1. **Task 1: AoA-parameterized solver** - `28a0631` (calc)
2. **Task 2: Anchor validation JSON** - `eb79fd7` (verify)

## Files Created/Modified

- `analysis/phase5/aoa_sweep_solver.py` — Complete solver module with ASSERT_CONVENTION, 5 functions, sign guards, anchor check main block. Importable by Phase 6.
- `analysis/phase5/outputs/phase5_anchor_check.json` — Anchor validation record with overall_anchor_pass=true

## Next Phase Readiness

- `solve_v_loop_aoa(AoA_target_deg)` and `compute_COP_aoa(AoA_target_deg, eta_c, loss_frac)` are ready for Phase 6 sweep
- phase6_ready: true (overall_anchor_pass = true)
- Phase 6 should sweep AoA from 1 to 15 deg and find the COP maximum

## Contract Coverage

- Claim IDs advanced: claim-ANAL-01 → passed; claim-ANAL-02 → passed; claim-VALD-01 → passed
- Deliverable IDs produced: deliv-aoa-solver → analysis/phase5/aoa_sweep_solver.py; deliv-anchor-json → analysis/phase5/outputs/phase5_anchor_check.json
- Acceptance test IDs run: test-fvert-sign → passed; test-brentq-anchor → passed; test-cop-anchor → passed; test-fvert-anchor → passed
- Reference IDs surfaced: ref-phase2-json → read,compare; ref-phase4-sys01 → read,compare; ref-phase4-summary → read,compare; ref-phase1-json → read; ref-phase2-summary → read; ref-phase3-json → read
- Forbidden proxies rejected: all 6 proxies rejected
- Decisive comparison verdicts: claim-VALD-01 → pass (0.001% error vs 0.5% tolerance)

## Equations Derived

**Eq. (05.1) — F_vert per vessel (Phase 2 convention):**

$$
F_{\text{vert}} = -\frac{1}{2}\rho_w A_\text{foil} v_\text{rel}^2 \left(C_{L,3D} \cos\beta + C_{D,\text{total}} \sin\beta\right)
$$

where $v_\text{rel}^2 = v_\text{loop}^2(1+\lambda^2)$, $\beta = \arctan(1/\lambda)$, $C_{L,3D} = C_{L,2D}/(1+2/AR)$, $C_{D,\text{total}} = C_{D,0} + C_{L,3D}^2/(\pi e A R)$. Sign is always negative (downward) for $\lambda > 0$, $\text{AoA} \in (0, 14]$ deg.

**Eq. (05.2) — Per-vessel force balance (brentq residual):**

$$
F_\text{net}(v_\text{loop}) = F_{b,\text{avg}} + F_\text{vert}(v_\text{loop}, \text{AoA}_\text{target}) - \frac{1}{2}\rho_w C_{D,\text{hull}} A_\text{frontal} v_\text{loop}^2 = 0
$$

Note: this is a per-vessel balance. Phase 4 and Phase 5 use per-vessel F_vert (not $N_\text{asc} \times F_\text{vert}$).

**Eq. (05.3) — Co-rotation correction (PITFALL-COROT):**

$$
P_\text{net,corot,corrected} = P_\text{net,corot,uncorrected} \times \left(\frac{v_\text{loop,c}}{v_\text{nom}}\right)^3
$$

## Validations Completed

- **Anchor v_loop:** 2.383484 vs 2.383479 m/s (0.0002% error, < 0.5% tolerance) PASS
- **Anchor F_vert:** -663.862 vs -663.859 N (0.0005% error, < 1.0% tolerance) PASS
- **Anchor COP_nominal:** 0.92501 vs 0.92501 (0.00007% error, < 0.5% tolerance) PASS
- **Sign check:** F_vert < 0 at AoA = 1, 5, 10, 15 deg (all four pass)
- **Limiting case AoA=0:** v_loop=3.691 m/s ≈ v_nom, F_vert=-164.7 N (C_L=0, pure drag — small as expected)
- **NACA table:** interpolate_naca(10.0) = (1.06, 0.013) exactly PASS
- **A_frontal:** computed 0.163998 m^2, expected 0.163998 m^2 (0.0001% diff) PASS
- **Co-rotation scale:** 0.264373 vs Phase 4 0.264371 (0.0007% diff < 1%) PASS
- **Dimensional analysis:** F_vert = [kg/m^3]*[m^2]*[m^2/s^2]*[-]*[-] = [N] PASS

## Decisions Made

1. **Per-vessel force balance** (not N_ascending multiplier in F_net_residual): The Plan pseudocode for F_net_residual included `N_ascending * F_vert_pv`, but Phase 4's working solver uses per-vessel balance. This was identified as DEVIATION Rule 5 (Physics Redirect). Using N_ascending multiplier gives v_loop=0.87 m/s (63% error). Per-vessel gives v_loop=2.384 m/s (matches anchor to 0.0002%). Per-vessel is correct physics.

2. **F_vert comparison is per-vessel**: Phase 4 JSON stores `F_vert_N = -663.8588 N` as the per-vessel result from `get_foil_forces()`. The anchor check compares per-vessel F_vert values for consistency.

3. **e_oswald=0.85 loaded from foil01_force_sweep.json**: Phase 2 summary table does not store e_oswald in the geometry section; it is in the foil_geometry dict of foil01_force_sweep.json.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 5 - Physics Redirect] Plan pseudocode for F_net_residual used N_ascending multiplier**

- **Found during:** Task 1 first run (anchor check gave v_loop=0.872 m/s, 63% error)
- **Issue:** Plan pseudocode: `F_vert_total = N_ascending * F_vert_pv; F_net = F_b_avg + F_vert_total - F_drag_hull`. But Phase 4's actual working code uses per-vessel balance: `F_net = F_b_avg + F_vert_pv - F_drag_hull`. The correct physics is confirmed by Phase 4 anchor: F_b_avg(1128.86 N) + F_vert_pv(-663.86 N) = 465 N = F_drag_hull at v_loop=2.384 m/s.
- **Fix:** Removed N_ascending multiplier from F_net_residual; reverted to per-vessel balance matching Phase 4
- **Files modified:** analysis/phase5/aoa_sweep_solver.py
- **Verification:** Anchor check v_loop error dropped from 63.4% to 0.0002% after fix
- **Committed in:** 28a0631

---

**Total deviations:** 1 auto-fixed (Rule 5 Physics Redirect)
**Impact on plan:** Essential correctness fix. No scope creep. Plan's analytical derivation of F_vert and all other equations were correct; only the pseudocode for F_net_residual had the N_ascending error.

## Issues Encountered

None beyond the Rule 5 deviation documented above.

## Open Questions

- At what AoA in [1, 15] deg is COP maximized? (Phase 6 primary question)
- AoA=1 deg gives v_loop=3.465 m/s (close to v_nom) but F_tan may be low; AoA=10 deg gives v_loop=2.384 m/s. The COP landscape across the full sweep is TBD.
- Co-rotation scale drops as (v_loop/v_nom)^3: at AoA=1 deg, scale=(3.465/3.714)^3=0.812 (much larger than 0.264 at AoA=10 deg). Co-rotation benefit may be significant at low AoA.

## Key Quantities and Uncertainties

| Quantity                 | Symbol           | Value      | Uncertainty  | Source                     | Valid Range      |
|--------------------------|------------------|------------|--------------|----------------------------|------------------|
| Loop velocity at anchor  | v_loop           | 2.383484 m/s | ±0.005 m/s (est.) | brentq, A_frontal ±5%      | AoA=10.0128 deg  |
| F_vert per vessel        | F_vert_pv        | -663.862 N  | ±5–10%       | NACA table, PL ±5%         | AoA=10.0128 deg  |
| COP_nominal              | COP              | 0.92501     | ±~0.05       | propagated from all sources| eta_c=0.70, loss=10% |
| v_loop at AoA=1 deg      | v_loop(1°)       | 3.465 m/s  | ±0.1 m/s     | brentq                     | AoA=1 deg        |
| v_loop at AoA=5 deg      | v_loop(5°)       | 2.832 m/s  | ±0.05 m/s    | brentq                     | AoA=5 deg        |
| v_loop at AoA=15 deg     | v_loop(15°)      | 2.373 m/s  | ±0.05 m/s    | brentq, stall clamp        | AoA=15 deg       |

## Approximations Used

| Approximation                      | Valid When                        | Error Estimate       | Breaks Down At         |
|------------------------------------|-----------------------------------|----------------------|------------------------|
| Fixed tip-speed ratio lambda=0.9   | Design operating point            | ~0% (exact at lambda) | If lambda_eff > 1.2748  |
| Quasi-steady foil forces           | Reduced freq k < 0.1              | ~5%                  | k > 0.1 (high-speed)   |
| NACA 0012 table at Re~1e6          | Re_foil in [5e5, 1e6]             | ~5-10% in C_L        | Re > 2e6 or < 2e5      |
| Prandtl lifting-line, AR=4         | AR >= 3, no stall                 | ~5-15% in C_L_3D     | AoA > 14 deg (stall)   |
| Per-vessel hull drag (A_frontal)   | C_D_hull=1.0, blunt cylinder      | ~5%                  | Near-stall, 3D effects |

## Derivation Summary

### Starting Point

Phase 2 rotating-arm vector geometry establishes:
- $v_\text{rel} = \sqrt{v_\text{loop}^2 + v_\text{tan}^2}$, $\beta = \arctan(v_\text{loop}/v_\text{tan})$
- $F_\text{vert} = -L\cos\beta - D\sin\beta$ (Phase 2 sign convention: negative = downward)

Phase 4 establishes: at fixed $\lambda$, $\beta$ is constant, so $F_\text{vert} \propto v_\text{loop}^2$ for fixed AoA.

### Phase 5 Change: AoA Parameterization

Phase 4 fixed mount_angle=38°, computed AoA_eff = beta - mount_angle. Phase 5 inverts this: AoA_target is given, mount_angle = beta - AoA_target is the implied physical foil orientation. At any v_loop, the foil is oriented so AoA_eff = AoA_target exactly.

### Final Result

At $\lambda = 0.9$, $\beta = \arctan(1/0.9) = 48.01°$ (constant). The per-vessel force balance:

$$F_{b,\text{avg}} - \frac{1}{2}\rho_w A_\text{foil} v_\text{loop}^2(1+\lambda^2)(C_{L,3D}\cos\beta + C_{D,\text{tot}}\sin\beta) = \frac{1}{2}\rho_w C_{D,\text{hull}} A_\text{frontal} v_\text{loop}^2$$

has a unique positive root $v_\text{loop}^* > 0$ for any AoA in [0, 14] deg (confirmed numerically).

## Cross-Phase Dependencies

### Results This Phase Provides To Later Phases

| Result                                    | Used By Phase     | How                                           |
|-------------------------------------------|-------------------|-----------------------------------------------|
| solve_v_loop_aoa(AoA_target_deg)          | Phase 6 sweep     | Called at each AoA in [1, 15] deg             |
| compute_COP_aoa(AoA_target_deg, ...)      | Phase 6 sweep     | Returns COP and all intermediate quantities   |
| phase5_anchor_check.json: overall=true    | Phase 6 gate      | Required before Phase 6 runs any sweep points |

### Results This Phase Consumed From Earlier Phases

| Result                              | From Phase | Verified Consistent                                      |
|-------------------------------------|------------|----------------------------------------------------------|
| F_b_avg_N=1128.86 N                 | Phase 1    | Used in force balance; anchor check confirms 0.0002%     |
| W_adia_J=23959.45 J                 | Phase 1    | W_pump=N_total*W_adia/eta_c (PITFALL-M1 guard)           |
| NACA table + e_oswald=0.85          | Phase 2    | Identical to Phase 4; anchor check confirms match        |
| P_net_corot=46826.0 W               | Phase 3    | Cross-checked vs Phase 4 summary table; exact match      |
| Anchor: v_loop=2.383479, COP=0.925  | Phase 4    | Reproduced to 0.001% — VALD-01 all tolerances passed     |

### Convention Changes

| Convention                                      | Previous         | This Phase               | Reason                                     |
|-------------------------------------------------|------------------|--------------------------|--------------------------------------------|
| AoA parameterization                            | AoA_eff=beta-38° | AoA_target is free param  | v1.1 objective: optimize over AoA          |
| None — F_vert sign, units, NACA table unchanged |                  |                          |                                            |

---

_Phase: 05-aoa-sweep-formulation-and-anchor-validation_
_Completed: 2026-03-19_
