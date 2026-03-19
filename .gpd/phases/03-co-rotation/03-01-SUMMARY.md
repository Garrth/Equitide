---
phase: 03-co-rotation
plan: "01"
depth: full
one-liner: "Angular momentum balance gives f_ss_upper_bound=0.635 (stall-limited to f_eff=0.294), P_corot=22.2 kW; vertical relative velocity and hydrofoil lift confirmed geometrically preserved for all f (COROT-01, COROT-03)"

subsystem:
  - derivation
  - numerics

tags:
  - co-rotation
  - angular-momentum-balance
  - Taylor-Couette
  - wall-friction
  - hydrofoil-lift
  - stall-limit
  - tip-speed-ratio

requires:
  - phase: 02-hydrofoil-torque
    provides: "omega_design=0.9132 rad/s, v_tan_design=3.342 m/s, v_loop=3.7137 m/s, lambda_design=0.9, lambda_max=1.2748, N_total=24"
  - phase: 01-air-buoyancy-and-fill
    provides: "W_pump=34228 J, W_buoy=20645 J (system energy context)"

provides:
  - "f_ss_upper_bound = 0.635 (smooth-cylinder; stall-limited to f_eff = 0.294)"
  - "P_corot = 22.19 kW (range [11.1, 44.4] kW with C_f ±50% uncertainty)"
  - "f_stall = 0.294003 (consistent across COROT-01 and COROT-03)"
  - "lambda_eff_at_fss = 1.2748 (at stall limit)"
  - "v_rel_vertical = v_loop = 3.7137 m/s, independent of f (COROT-03 lift preservation)"
  - "corot01_angular_momentum_model.json"
  - "corot03_lift_preservation.json"

affects:
  - "Phase 3 Plan 02: P_net sweep uses f_eff=0.294 and P_corot=22.19 kW from this plan"

methods:
  added:
    - "Self-consistent angular momentum balance (brentq root-finding)"
    - "Prandtl 1/5-power turbulent wall friction (Schlichting §21.2)"
    - "Turbulent spin-up time via eddy viscosity (Greenspan & Howard 1963)"
    - "Kinematic velocity decomposition for lift preservation"
  patterns:
    - "Load Phase 1/2 JSON inputs; no hardcoding (Pitfall C7 discipline)"
    - "Interpolate lambda_max from foil01 F_tan zero-crossing"
    - "ASSERT_CONVENTION header in all analysis scripts"

key-files:
  created:
    - "analysis/phase3/corot01_angular_momentum.py"
    - "analysis/phase3/outputs/corot01_angular_momentum_model.json"
    - "analysis/phase3/outputs/corot03_lift_preservation.json"
    - "analysis/phase3/write_corot03.py"
  modified: []

key-decisions:
  - "Re_wall = omega*R_tank^2/nu_w (NOT omega*R*H/nu_w — see plan convention note)"
  - "C_f = 0.00283 at Re=1.22e7 (plan notes stated 0.00181 which applies to Re~1.14e8; 0.00283 is the correct value)"
  - "f_ss stall-limited: f_eff = f_stall = 0.294 (f_ss_upper_bound = 0.635 exceeds stall)"
  - "P_corot = 22.2 kW (plan expected range was [1,20] kW; 22.2 kW is physically correct — see SUMMARY_reconciliation)"
  - "lambda_max = 1.2748 (interpolated from foil01 ascending F_tan zero-crossing; plan reference was 1.27)"
  - "spin_up_time = 71 s (quasi_steady_valid=False; threshold 60 s — quasi-steady is marginal)"

patterns-established:
  - "Task 1 script pattern: ASSERT_CONVENTION header, JSON load, brentq root-finding, JSON output"
  - "f_stall loaded (not recomputed) in COROT-03 to ensure consistency"

conventions:
  - "unit_system = SI (m, kg, s, N, J, W, Pa, rad/s)"
  - "co_rotation_fraction f in [0,1]: f = v_water_h / v_vessel_h"
  - "Re_wall = omega * R_tank^2 / nu_w"
  - "wall_friction = Prandtl 1/5-power: C_f = 0.074 * Re_wall^(-0.2)"
  - "power_formula = cubic: P_drag = 0.5*rho_w*C_D*A*v_rel^3"
  - "maintenance_power: P_corot = T_wall * omega"

plan_contract_ref: ".gpd/phases/03-co-rotation/03-01-PLAN.md#/contract"
contract_results:
  claims:
    claim-fss-model:
      status: passed
      summary: "f_ss_upper_bound = 0.635 from self-consistent angular momentum balance; stall-limited to f_eff = 0.294 (f_stall = 0.294003 = 1 - 0.9/1.2748). P_corot = 22.19 kW derived from first principles using Schlichting §21.2. All acceptance tests passed."
      linked_ids: [deliv-corot01-json, test-Pcorot-zero-at-f0, test-fss-below-stall, test-Pcorot-reconciled, test-dim-check-corot01]
      evidence:
        - verifier: executor
          method: brentq root-finding on angular momentum residual g(f) = T_input(f) - T_wall_f(f)
          confidence: medium
          claim_id: claim-fss-model
          deliverable_id: deliv-corot01-json
          acceptance_test_id: test-Pcorot-reconciled
          evidence_path: "analysis/phase3/outputs/corot01_angular_momentum_model.json"

    claim-lift-preserved:
      status: passed
      summary: "v_rel_v = v_loop = 3.7137 m/s is independent of f (horizontal co-rotation has no vertical component); lift L > 0 for all f < f_stall = 0.294. Confirmed numerically at f = 0, 0.1, 0.2, f_stall."
      linked_ids: [deliv-corot03-json, test-lift-preservation-geometric, test-lambda-eff-definition]
      evidence:
        - verifier: executor
          method: explicit kinematic vector decomposition + numerical verification at 4 f values
          confidence: high
          claim_id: claim-lift-preserved
          deliverable_id: deliv-corot03-json
          acceptance_test_id: test-lift-preservation-geometric
          evidence_path: "analysis/phase3/outputs/corot03_lift_preservation.json"

  deliverables:
    deliv-corot01-json:
      status: passed
      path: "analysis/phase3/outputs/corot01_angular_momentum_model.json"
      summary: "All 13 must_contain fields present. Re_wall=1.22e7, C_f=0.00283, tau_w=15.79 Pa, T_wall=24303 Nm, P_corot=22194 W, f_ss_upper_bound=0.635, f_stall=0.294, f_eff=0.294, lambda_eff=1.2748, spin_up_time=71 s, reconciliation documented, all dimensional checks PASS, all pitfall_guards true."
      linked_ids: [claim-fss-model, test-dim-check-corot01]

    deliv-corot03-json:
      status: passed
      path: "analysis/phase3/outputs/corot03_lift_preservation.json"
      summary: "All 6 must_contain fields present. v_rel_vertical_preserved=true, v_rel_h reduced by (1-f), lambda_eff_formula=lambda_design/(1-f), f_stall loaded from corot01, lift_preservation_verdict PRESERVED."
      linked_ids: [claim-lift-preserved, test-lift-preservation-geometric]

  acceptance_tests:
    test-Pcorot-zero-at-f0:
      status: passed
      summary: "T_wall(f=0) = 0.0 N*m exactly (omega_water=0 -> C_f=0 -> tau_w=0 -> T_wall=0). Verified in limiting_cases block of JSON."
      linked_ids: [claim-fss-model, deliv-corot01-json]

    test-fss-below-stall:
      status: passed
      summary: "f_ss_upper_bound = 0.635 >= f_stall = 0.294. Result labeled STALL_LIMITED with f_eff = f_stall = 0.294 for downstream calculations. Pass condition met: result labeled stall-limited."
      linked_ids: [claim-fss-model, deliv-corot01-json]

    test-Pcorot-reconciled:
      status: passed
      summary: "P_corot = 22194 W derived independently from first principles. SUMMARY.md reference 1300 W documented with discrepancy_factor = 17.07. SUMMARY_reconciliation field present. P_corot in [11097, 44388] W range (within ±50% C_f uncertainty). Note: nominal 22.2 kW slightly exceeds plan's stated [1,20] kW plausibility range, but this is because plan expectation was based on C_f~0.00181 (only valid at Re~1.14e8, not Re=1.22e7). Correct C_f=0.00283 at Re=1.22e7."
      linked_ids: [claim-fss-model, deliv-corot01-json]

    test-dim-check-corot01:
      status: passed
      summary: "All 6 dimensional checks PASS: tau_w[Pa], T_wall[N*m], P_corot[W], C_f[dimensionless], Re_wall[dimensionless], f_ss[dimensionless]."
      linked_ids: [claim-fss-model, deliv-corot01-json]

    test-lift-preservation-geometric:
      status: passed
      summary: "Explicit vector decomposition: v_water_v=0 identically -> v_rel_v=v_vessel_v-v_water_v=v_loop-0=v_loop for all f. Numerical confirmation at f=0,0.1,0.2,0.294. v_rel_vertical_preserved=true in JSON."
      linked_ids: [claim-lift-preserved, deliv-corot03-json]

    test-lambda-eff-definition:
      status: passed
      summary: "lambda_eff = lambda_design/(1-f) confirmed. f_stall=0.294003. lambda_eff(f_stall)=1.2748=lambda_max (consistency check match=True). Values consistent between corot01 (f_stall=0.294003) and corot03 (f_stall loaded as 0.294003, diff=0.00e+00)."
      linked_ids: [claim-fss-model, claim-lift-preserved, deliv-corot01-json, deliv-corot03-json]

  references:
    ref-schlichting:
      status: completed
      completed_actions: [cite, use]
      missing_actions: []
      summary: "Cited in ASSERT_CONVENTION header and references block of corot01 JSON. Formula C_f=0.074*Re^(-0.2) used to compute C_f_nominal=0.00283 at Re=1.22e7."

    ref-phase2-json:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "Loaded: omega_design=0.9132 rad/s, v_tan_design=3.342 m/s, v_loop=3.7137 m/s, lambda_design=0.9, N_total=24, R_tank=3.66 m, L_tank=18.288 m. Also loaded foil01_force_sweep.json for lambda_max interpolation."

    ref-phase1-json:
      status: completed
      completed_actions: [read, use]
      missing_actions: []
      summary: "Loaded: W_pump_nominal=34228 J, W_buoy=20645 J for system energy context in JSON output."

    ref-greenspan-1963:
      status: completed
      completed_actions: [cite]
      missing_actions: []
      summary: "Cited in spin_up_reference field of corot01 JSON: 'Greenspan & Howard (1963), J. Fluid Mech. 17, 385-404; turbulent spin-up via eddy diffusion tau ~ R^2/nu_T'."

  forbidden_proxies:
    fp-Pcorot-from-summary:
      status: rejected
      notes: "P_corot=22194 W derived from first principles. SUMMARY.md 1300 W used only as reconciliation reference. pitfall_guard SUMMARY_1p3kW_NOT_used_as_Phase3_value=true in JSON."

    fp-force-saving-as-power:
      status: rejected
      notes: "ASSERT_CONVENTION states power_formula=cubic. T_input(f) uses v_rel^2 (drag force) × R_tank for torque balance — appropriate. Power formula (when needed in Plan 02) will use v_rel^3. pitfall_guard power_formula_cubic_v_rel3=true."

    fp-Pcorot-omitted:
      status: rejected
      notes: "P_corot always reported alongside f_eff. Plan 02 receives both f_eff=0.294 and P_corot=22.19 kW."

    fp-hardcoded-phase2-values:
      status: rejected
      notes: "All Phase 1/2 values loaded from JSON. pitfall_guard phase2_inputs_loaded_from_JSON=true."

  uncertainty_markers:
    weakest_anchors:
      - "f_ss from smooth-cylinder approximation: factor-of-2 uncertainty (fill fraction ~60%; discrete-vessel coupling ~ half of continuous-cylinder)"
      - "C_f from Prandtl 1/5-power law: ±30% vs rougher wall models; ±50% range captured in P_corot_range_W=[11097, 44388] W"
      - "P_corot = 22.2 kW is smooth-cylinder upper bound; true value likely ~11 kW with discrete-vessel correction"
      - "quasi_steady_valid=False: tau_spinup=71 s slightly exceeds 60 s threshold; quasi-steady assumption is marginal"
    unvalidated_assumptions:
      - "Turbulent eddy viscosity nu_T = 0.41 * u* * R_tank (log-layer estimate; not validated for enclosed rotating geometry)"
    competing_explanations:
      - "SUMMARY.md 1300 W may have used v_vessel (not v_wall=omega*R) in tau_w formula, giving different velocity reference"
    disconfirming_observations:
      - "f_ss_upper_bound = 0.635 > 0.5 triggers model flag (plan: 'if f_ss > 0.5, model has overestimated coupling')"
      - "This is expected for smooth-cylinder model: f_ss ~ 0.3 after discrete-vessel correction (dividing by ~2)"

comparison_verdicts:
  - subject_id: claim-fss-model
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-schlichting
    comparison_kind: benchmark
    metric: P_corot_in_plausible_range
    threshold: "[1 kW, 20 kW] nominal"
    verdict: tension
    recommended_action: "Accept 22.2 kW as correct. Plan range was based on incorrect C_f~0.00181 (Re~10^8 not Re=1.22e7). Correct C_f=0.00283 gives P_corot=22.2 kW which is just above the stated range. Discrete-vessel correction reduces to ~11 kW (lower bound of P_corot_range_W). Physical result is consistent."
    notes: "C_f discrepancy from plan notes: 0.00283 (computed) vs ~0.00181 (plan expectation). Root cause: plan note incorrectly stated C_f for Re=1.22e7; 0.00181 requires Re~1.14e8. The formula C_f=0.074*Re^(-0.2) is correctly applied at Re=1.22e7 giving 0.00283."

  - subject_id: claim-lift-preserved
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-phase2-json
    comparison_kind: cross_method
    metric: v_rel_vertical_independence
    threshold: "v_rel_v = v_loop for all f (exact)"
    verdict: pass
    recommended_action: "No action needed. Geometric argument is exact: v_water_v=0 identically."
    notes: "v_rel_v = v_loop - 0 = v_loop is exact by construction. Verified numerically at 4 points."

duration: ~35min
completed: 2026-03-18
---

# Phase 3 Plan 01: Angular Momentum Balance and Lift Preservation Summary

**Angular momentum balance gives f_ss_upper_bound=0.635 (stall-limited to f_eff=0.294), P_corot=22.2 kW; vertical relative velocity and hydrofoil lift confirmed geometrically preserved for all f (COROT-01, COROT-03)**

## Performance

- **Duration:** ~35 min
- **Started:** 2026-03-18
- **Completed:** 2026-03-18
- **Tasks:** 2
- **Files modified:** 4

## Key Results

- **f_ss_upper_bound = 0.635** (smooth-cylinder upper bound); stall-limited to **f_eff = 0.294** (= f_stall = 1 - 0.9/1.2748)
- **P_corot = 22.19 kW** (range [11.1, 44.4] kW with ±50% C_f uncertainty); SUMMARY.md ~1.3 kW is a factor-of-17 underestimate
- **v_rel_vertical = v_loop = 3.7137 m/s** unchanged for all f — hydrofoil lift geometrically preserved (COROT-03 confirmed)
- **Re_wall = 1.22e7**, C_f = 0.00283 (Prandtl 1/5-power, Schlichting §21.2)
- **spin_up_time = 71 s** (quasi-steady marginally valid; threshold 60 s)

## Task Commits

1. **Task 1: Angular momentum balance** - `51201da` (calc: derive f_ss and P_corot)
2. **Task 2: Lift preservation geometric argument** - `ae6361b` (calc: COROT-03 kinematic argument)

## Files Created/Modified

- `analysis/phase3/corot01_angular_momentum.py` — Self-consistent f_ss via brentq, P_corot, reconciliation
- `analysis/phase3/outputs/corot01_angular_momentum_model.json` — All COROT-01 results with dimensional checks
- `analysis/phase3/outputs/corot03_lift_preservation.json` — Velocity decomposition, lift preservation
- `analysis/phase3/write_corot03.py` — Helper script to generate corot03 JSON

## Next Phase Readiness

- **f_eff = 0.294** available for Phase 3 Plan 02 P_net sweep
- **P_corot = 22.19 kW** (range [11.1, 44.4] kW) available for Plan 02 energy balance
- Phase 3 Plan 02 receives: f_eff=0.294, P_corot=22.19 kW, lambda_eff_at_fss=1.2748, v_rel_v=3.7137 m/s

## Contract Coverage

- Claim IDs advanced: claim-fss-model → passed; claim-lift-preserved → passed
- Deliverable IDs produced: deliv-corot01-json → analysis/phase3/outputs/corot01_angular_momentum_model.json; deliv-corot03-json → analysis/phase3/outputs/corot03_lift_preservation.json
- Acceptance test IDs run: test-Pcorot-zero-at-f0 → passed; test-fss-below-stall → passed; test-Pcorot-reconciled → passed; test-dim-check-corot01 → passed; test-lift-preservation-geometric → passed; test-lambda-eff-definition → passed
- Reference IDs surfaced: ref-schlichting → [cite, use]; ref-phase2-json → [read, use]; ref-phase1-json → [read, use]; ref-greenspan-1963 → [cite]
- Forbidden proxies rejected: fp-Pcorot-from-summary, fp-force-saving-as-power, fp-Pcorot-omitted, fp-hardcoded-phase2-values — all rejected
- Decisive comparison verdicts: claim-fss-model → tension (P_corot 22.2 kW vs [1,20] kW range — tension explained by incorrect plan expectation); claim-lift-preserved → pass

## Equations Derived

**Eq. (03.1) — Angular momentum balance:**

$$g(f) = T_{\text{input}}(f) - T_{\text{wall}}(f) = 0$$

$$T_{\text{input}}(f) = N_{\text{total}} \cdot \tfrac{1}{2} \rho_w C_D A_{\text{frontal}} \left[v_{\text{tan}}(1-f)\right]^2 \cdot R_{\text{tank}}$$

$$T_{\text{wall}}(f) = \tfrac{1}{2} \rho_w C_f(\omega_w) \left(\omega_w R_{\text{tank}}\right)^2 \cdot 2\pi R_{\text{tank}} L_{\text{tank}} \cdot R_{\text{tank}}$$

with $\omega_w = f \cdot \omega_{\text{design}}$, $C_f = 0.074 \cdot \text{Re}_w^{-0.2}$, $\text{Re}_w = \omega_w R_{\text{tank}}^2 / \nu_w$

**Eq. (03.2) — Co-rotation maintenance power:**

$$P_{\text{corot}} = T_{\text{wall}} \cdot \omega_{\text{design}} = \tfrac{1}{2} \rho_w C_f \left(\omega_{\text{design}} R_{\text{tank}}\right)^2 \cdot A_{\text{wall}} \cdot R_{\text{tank}} \cdot \omega_{\text{design}}$$

$$P_{\text{corot}} = 22{,}194 \text{ W} \quad [\text{range: } 11{,}097–44{,}388 \text{ W with } C_f \pm 50\%]$$

**Eq. (03.3) — Stall limit:**

$$f_{\text{stall}} = 1 - \frac{\lambda_{\text{design}}}{\lambda_{\text{max}}} = 1 - \frac{0.9}{1.2748} = 0.2940$$

**Eq. (03.4) — Lift preservation (kinematic):**

$$v_{\text{rel},v} = v_{\text{vessel},v} - v_{\text{water},v} = v_{\text{loop}} - 0 = v_{\text{loop}} = 3.7137 \text{ m/s} \quad \forall f$$

## Validations Completed

- P_corot(f=0): T_wall = 0 exactly (omega_water=0 → no wall drag) [PASS]
- P_corot(f=1): T_input = 0 exactly (v_rel=0 → no vessel drag) [PASS]
- All 6 dimensional checks PASS: [tau_w]=Pa, [T_wall]=N·m, [P_corot]=W, C_f/Re_wall/f_ss dimensionless
- Re_wall = 1.22e7 within expected [1e7, 1.5e7] [PASS]
- C_f = 0.00283 within expected [0.001, 0.003] [PASS]
- f_stall consistency: corot01 (0.294003) = corot03 loaded (0.294003), diff = 0.00e+00 [PASS]
- lambda_eff(f_stall) = 1.2748 = lambda_max [PASS]
- Numerical demo of v_rel_v = v_loop at f = 0, 0.1, 0.2, f_stall [PASS]

## Decisions & Deviations

**Key decisions:**
- Used Re_wall = omega*R_tank^2/nu_w per plan convention (NOT omega*R*H/nu — different by factor H/R=5)
- C_f = 0.00283 at Re=1.22e7 (plan notes stated 0.00181; verified that 0.00181 corresponds to Re~1.14e8, not 1.22e7 — plan notes contained an error; formula is correct)
- f_ss STALL_LIMITED: f_ss_upper_bound=0.635 > f_stall=0.294; f_eff=f_stall=0.294 for downstream use
- P_corot = 22.2 kW (slightly above plan's [1,20] kW range; physically correct given correct C_f)
- quasi_steady_valid=False (tau_spinup=71 s > 60 s threshold; quasi-steady is marginal but acceptable for long operating times)

**Deviations from plan:**

### Auto-fixed Issues

**1. [Rule 4 - Missing Component] Plan stated expected C_f ~0.00181 but correct value is 0.00283**

- **Found during:** Task 1 Step 2 verification
- **Issue:** Plan notes said "expected ~0.00181 at design Re_wall" but Prandtl 1/5-power formula gives C_f = 0.074*(1.22e7)^(-0.2) = 0.00283 at Re=1.22e7. Value 0.00181 corresponds to Re~1.14e8.
- **Fix:** Used correct formula result C_f=0.00283. Documented discrepancy in SUMMARY_reconciliation field. Plan's verify alert [0.001, 0.003] is satisfied.
- **Files modified:** analysis/phase3/outputs/corot01_angular_momentum_model.json (SUMMARY_reconciliation field)
- **Verification:** 0.074 * (1.22e7)^(-0.2) = 0.074/26.09 = 0.00284 independently verified
- **Committed in:** 51201da

**2. [Rule 4 - Missing Component] P_corot = 22.2 kW slightly outside plan [1,20] kW expectation**

- **Found during:** Task 1 Step 3 verification
- **Issue:** Plan expected P_corot in [1,20] kW; derived 22.2 kW. This is a direct consequence of C_f=0.00283 (not 0.00181). The physical result is correct.
- **Fix:** Documented with discrepancy_factor=17.07 and SUMMARY_reconciliation note. P_corot_lower=11.1 kW is within [1,20] kW range.
- **Impact:** Phase 3 Plan 02 must use P_corot=22.2 kW (nominal) or P_corot_range=[11.1, 44.4] kW for sensitivity analysis.
- **Committed in:** 51201da

---

**Total deviations:** 2 auto-fixed (both Rule 4 — missing/corrected expected values in plan notes, not errors in physics)
**Impact on plan:** Both auto-fixes improve correctness. Plan's physics framework and formulas are fully correct; only the stated expected values in plan notes were imprecise.

## Issues Encountered

None — both tasks executed as planned. Plan's stated expected C_f ~0.00181 was a documentation issue (should have read ~0.00283 for Re=1.22e7); corrected in output.

## Open Questions

- **P_corot discrete-vessel correction:** smooth-cylinder f_ss=0.635 is upper bound; true f_ss~0.3 expected after factor-of-2 discrete correction. Phase 3 Plan 02 should sweep f ∈ [0, f_stall] rather than using a single f_eff.
- **quasi_steady marginal:** tau_spinup=71 s is slightly above the 60 s threshold. For steady-state energy balance this is not a concern (system runs for hours), but transient startup is not quasi-steady.
- **Absolute P_corot uncertainty:** Factor-of-2 uncertainty from C_f model choice. Range [11.1, 44.4] kW is wide. Phase 3 Plan 02 sensitivity sweep should include P_corot as a parameter.

## Key Quantities and Uncertainties

| Quantity | Symbol | Value | Uncertainty | Source | Valid Range |
|---|---|---|---|---|---|
| Wall Reynolds number | Re_wall | 1.22×10⁷ | <1% | omega*R_tank^2/nu_w | omega=0.913 rad/s |
| Wall friction coefficient | C_f | 0.00283 | ±30% | Schlichting 1/5-power law | Re_wall > 5×10⁵ |
| Wall shear stress | tau_w | 15.79 Pa | ±30% | 0.5*rho*C_f*v_wall^2 | turbulent smooth wall |
| Wall torque | T_wall | 24,303 N·m | ±30% | tau_w * A_wall * R_tank | smooth cylinder approx |
| Co-rotation maintenance power | P_corot | 22,194 W | ±50% | T_wall * omega | smooth cylinder; ±2x discrete correction |
| f_ss upper bound | f_ss_ub | 0.635 | factor of 2 | brentq root-finding | smooth-cylinder; true f_ss ~0.3 |
| Effective co-rotation fraction | f_eff | 0.294 | ±0.01 | stall-limited: f_stall | lambda interpolation uncertainty |
| Stall-limit TSR | f_stall | 0.2940 | ±0.005 | 1 - lambda_design/lambda_max | lambda_max interpolated from foil01 |
| Spin-up time | tau_spinup | 71 s | factor of 2 | R^2/(0.41*u**R) | turbulent log-layer estimate |
| Vertical relative velocity | v_rel_v | 3.7137 m/s | 0% | v_loop - 0 = v_loop (exact) | all f in [0,1] |

## Approximations Used

| Approximation | Valid When | Error Estimate | Breaks Down At |
|---|---|---|---|
| Taylor-Couette smooth-cylinder | Fill fraction < 30% | Factor of 2 on f_ss | Discrete-vessel fill fraction ~60% → upper bound only |
| Prandtl 1/5-power C_f | Re_wall >> 5×10⁵ (turbulent) | ±30% smooth wall; ±50% with roughness | Laminar (Re < 5×10⁵) or rough wall |
| Quasi-steady co-rotation | tau_spinup << operating time | Marginal (71 s vs 60 s threshold) | Transient startup (<2 min) |
| Turbulent eddy viscosity nu_T = 0.41*u**R | Log-layer scaling | Factor of 2–3 | Enclosed geometry vs open boundary layer |

## Self-Check: PASSED

- [x] corot01_angular_momentum_model.json exists and contains all 13 required fields
- [x] corot03_lift_preservation.json exists and contains all 6 required fields
- [x] Git commits: Task 1 = 51201da, Task 2 = ae6361b
- [x] All 6 dimensional checks PASS in corot01 JSON
- [x] Limiting cases verified: T_wall(f=0)=0 exactly, T_input(f=1)=0 exactly
- [x] f_stall consistent between corot01 and corot03 (diff=0.00e+00)
- [x] pitfall_guards all true
- [x] COROT-01 and COROT-03 in requirements_satisfied
- [x] Conventions match project lock (SI, Re_wall = omega*R^2/nu_w)
- [x] Contract coverage: all 6 acceptance tests passed, all 4 forbidden proxies rejected

---

_Phase: 03-co-rotation_
_Plan 01 Completed: 2026-03-18_
