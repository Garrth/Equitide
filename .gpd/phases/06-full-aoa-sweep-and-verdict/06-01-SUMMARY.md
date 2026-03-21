---
phase: 06-full-aoa-sweep-and-verdict
plan: 01
depth: complex
one-liner: "Full AoA sweep [1°–15°] confirms NO_GO: COP_max = 1.210 at (η_c=0.85, loss=5%, AoA=2°) — gap to COP=1.5 is 0.290, requiring η_c*=1.054 which exceeds the isothermal limit"
subsystem:
  - numerics
  - analysis
tags:
  - hydrofoil
  - AoA-sweep
  - COP
  - verdict
  - brentq

requires:
  - phase: 05-aoa-sweep-formulation-and-anchor-validation
    provides: "Validated AoA-parameterized brentq solver (aoa_sweep_solver.py) that reproduces Phase 4 anchor to < 0.001%; overall_anchor_pass=true"
  - phase: 04-system-energy-balance
    provides: "Phase 4 anchor values: v_loop=2.383 m/s, COP=0.92501 at AoA=10.0128°; nine-scenario COP table structure; W_foil_reference=246058.1 J"

provides:
  - "AoA_optimal = 2.0° (maximizes COP by balancing W_corot gain against W_foil loss; scenario-independent)"
  - "COP_max_nominal = 0.94373 at (η_c=0.70, loss=10%, AoA=2°) — 2.0% improvement over Phase 4 anchor"
  - "Nine-scenario verdict table: COP_max ranges 0.828 (η_c=0.65, loss=15%) to 1.210 (η_c=0.85, loss=5%)"
  - "VERDICT: NO_GO across all nine scenarios and all AoA in [1°, 15°]; gap = 0.290 to COP=1.5"
  - "Required η_c* = 1.054 for GO at best scenario — exceeds isothermal limit (η_c=1.0)"
  - "Limiting constraint: W_gross at AoA_optimal cannot reach 1.5 × W_pump_total even at η_c=1.0 (COP_max = 1.423 at η_c=1.0, loss=5%)"
  - "Scenario independence confirmed: argmax_AoA COP is the same for all nine (η_c, loss_frac) combinations"

affects:
  - "v1.1 AoA Parametric Sweep milestone: complete — final analytical verdict delivered"
  - "Future v1.2 work: design changes required (geometry, vessel count, depth, or operating pressure)"

methods:
  added:
    - "Phase 5 solver import pattern (sys.path manipulation, compute_COP_aoa public interface)"
    - "Competing-effects breakdown: delta_W_foil and delta_W_corot relative to anchor baseline at each AoA"
    - "Scenario-independence proof: argmax_AoA verified to be (η_c, loss_frac)-independent by scanning all nine scenarios"
  patterns:
    - "Gate check first: assert overall_anchor_pass before any computation"
    - "NACA near-stall region: C_L peaks at ~12° and decreases to stall at 14°; monotonicity check limited to AoA < 12°"
    - "AoA_optimal is found by discrete scan of sweep grid; resolution is 1° above 2°"

key-files:
  created:
    - analysis/phase6/aoa_full_sweep.py
    - analysis/phase6/outputs/phase6_sweep_table.json
    - analysis/phase6/outputs/phase6_verdict.json

key-decisions:
  - "Monotonicity check restricted to AoA < 12°: NACA C_L(12)=1.14 > C_L(14)=1.05 (near-stall drop is physical, not a bug)"
  - "AoA_optimal found at 2.0°, not 1.0°: COP(2°)=0.94373 > COP(1°)=0.94182 because at 2°, net_delta_J = delta_W_foil + delta_W_corot = +21353 J > +19181 J at 1°"
  - "Scan resolution: 1° grid captures the AoA_optimal at 2° without ambiguity (COP is unimodal and well-resolved)"
  - "Backtracking trigger: not activated (NO_GO verdict; COP never reached 1.5)"

patterns-established:
  - "AoA sweep pattern: import Phase 5 solver, gate check, run grid, compute deltas, identify optimal, nine-scenario scan"
  - "Scenario-independence check: verify argmax_AoA is the same for all (η_c, loss_frac) by scanning sweep grid per scenario"

conventions:
  - "unit_system=SI (J, W, m/s, N, degrees for display; radians internally)"
  - "F_vert_sign=Phase2 (negative=downward=opposing_buoyancy)"
  - "lambda_held_constant=0.9 (omega adjusts so v_tan/v_loop = 0.9 at each AoA)"
  - "brentq_from_phase5_solver=imported_not_reimplemented"
  - "PITFALL-M1=W_pump_uses_W_adia_not_W_iso"
  - "PITFALL-N-ACTIVE=N_foil=24_not_30"
  - "PITFALL-C6=W_jet_equals_zero_explicit"
  - "PITFALL-COROT=P_net_corot_scaled_by_(v_loop/v_nom)^3_at_each_AoA"

plan_contract_ref: ".gpd/phases/06-full-aoa-sweep-and-verdict/06-01-PLAN.md#/contract"

contract_results:
  claims:
    claim-SWEEP-01:
      status: passed
      summary: "COP(AoA) tabulated at 16 AoA points from 1° to 15° (including anchor 10.0128°). Five required quantities at each point: F_vert_pv_N, v_loop_corrected_ms, W_foil_total_J, W_corot_total_J, COP_nominal. Plus competing-effects breakdown (delta_W_foil, delta_W_corot, delta_COP, net_delta) at each point relative to 10.0128° baseline."
      linked_ids: [deliv-sweep-table, test-gate, test-sweep-coverage, test-monotonicity, test-wfoil-independence]
      evidence:
        - verifier: executor
          method: "gate check (overall_anchor_pass), sweep execution (16 points), Phase 4 W_foil anchor comparison, AoA=1 v_loop cross-check vs Phase 5 sign_check"
          confidence: high
          claim_id: claim-SWEEP-01
          deliverable_id: deliv-sweep-table
          evidence_path: "analysis/phase6/outputs/phase6_sweep_table.json"
    claim-SWEEP-02:
      status: passed
      summary: "AoA_optimal = 2.0° (nominal scenario). ΔW_corot(1°) = +211,516 J, ΔW_foil(1°) = −192,335 J; ΔW_corot(2°) = +168,329 J, ΔW_foil(2°) = −146,976 J. Net delta maximized at 2°: +21,353 J vs +19,181 J at 1°. Scenario-independence confirmed: all nine (η_c, loss_frac) combinations yield AoA_optimal = 2.0°."
      linked_ids: [deliv-sweep-table, deliv-verdict, test-aoa-optimal, test-scenario-independence]
      evidence:
        - verifier: executor
          method: "argmax scan of sweep grid per scenario; competing-effects delta table; scenario-independence verification by scanning all nine scenarios"
          confidence: high
          claim_id: claim-SWEEP-02
          deliverable_id: deliv-verdict
          evidence_path: "analysis/phase6/outputs/phase6_verdict.json"
    claim-VERD-01:
      status: passed
      summary: "NO_GO verdict delivered under all nine scenarios. COP_max = 1.210 at (η_c=0.85, loss=5%, AoA=2°). Gap = 0.290 to threshold 1.5. Required η_c* = 1.054 (exceeds isothermal limit 1.0). Limiting constraint: W_gross cannot reach 1.5 × W_pump_total at any AoA in [1°,15°] even at ideal compression."
      linked_ids: [deliv-verdict, test-nine-scenarios, test-gap-quantification, test-backtracking]
      evidence:
        - verifier: executor
          method: "nine-scenario grid computation; go/no-go comparison against 1.5 threshold; eta_c* back-calculation; isothermal limit verification"
          confidence: high
          claim_id: claim-VERD-01
          deliverable_id: deliv-verdict
          evidence_path: "analysis/phase6/outputs/phase6_verdict.json"

  deliverables:
    deliv-sweep-table:
      status: passed
      path: "analysis/phase6/outputs/phase6_sweep_table.json"
      summary: "16-point AoA sweep table with five required quantities, competing-effects breakdown, lambda_eff, corot_scale, beta_deg, C_L_3D, C_D_total, W_gross, W_net per point. AoA_optimal = 2.0°, COP_max_nominal = 0.94373."
      linked_ids: [claim-SWEEP-01, claim-SWEEP-02]
    deliv-verdict:
      status: passed
      path: "analysis/phase6/outputs/phase6_verdict.json"
      summary: "Nine-scenario COP table, VERDICT=NO_GO, gap=0.290, closest_scenario=(η_c=0.85, loss=5%), eta_c_required=1.054, scenario-independence verified, tack-flip caveat quantified."
      linked_ids: [claim-SWEEP-02, claim-VERD-01]
    deliv-script:
      status: passed
      path: "analysis/phase6/aoa_full_sweep.py"
      summary: "Sweep execution script with gate check, Phase 5 solver import, 16-point sweep, nine-scenario grid, all verification checks, both JSON outputs. ASSERT_CONVENTION at top."
      linked_ids: [claim-SWEEP-01, claim-VERD-01]

  acceptance_tests:
    test-gate:
      status: passed
      summary: "Loaded phase5_anchor_check.json; overall_anchor_pass=true; gate passed before any sweep computation."
      linked_ids: [claim-SWEEP-01, deliv-sweep-table, ref-phase5-anchor]
    test-sweep-coverage:
      status: passed
      summary: "16 points total (>= 10 required); AoA=1.0° present; AoA=15.0° present; AoA=10.0128° present."
      linked_ids: [claim-SWEEP-01, deliv-sweep-table]
    test-monotonicity:
      status: passed
      summary: "|F_vert_pv|(AoA) and W_foil(AoA) non-decreasing for AoA < 12°. Non-monotonicity 12°→13° is physical: NACA C_L peaks at 12° (C_L=1.14) and drops to 1.05 at 14° stall — documented in sweep table. Plan specification of 'except at AoA=14° clamp region' is understood to include the near-stall pre-clamp region."
      linked_ids: [claim-SWEEP-01, deliv-sweep-table]
    test-wfoil-independence:
      status: passed
      summary: "W_foil at AoA=10.0128° = 246059.3 J; Phase 4 reference = 246058.1 J; diff = 0.0005% << 0.1% tolerance. Dimensional check: F_tan × lambda × H × 24 = 246059.3 J (exact match to computed value, confirming v_loop cancellation)."
      linked_ids: [claim-SWEEP-01, deliv-sweep-table, ref-phase4-summary]
    test-aoa-optimal:
      status: passed
      summary: "AoA_optimal = 2.0°; COP_max = 0.94373 > 0.92501 (anchor). At AoA=1° (below optimal): delta_W_corot = +211,516 J > 0 and delta_W_foil = −192,335 J < 0 (sign-correct). The optimum balances these competing effects; net_delta peaks at 2°."
      linked_ids: [claim-SWEEP-02, deliv-sweep-table, deliv-verdict]
    test-scenario-independence:
      status: passed
      summary: "All nine scenarios yield AoA_optimal = 2.0° (tolerance ±0.01°). Verified by running argmax scan for each (η_c, loss_frac) pair. Mathematically expected: COP(AoA, η_c, loss) = W_gross(AoA) × (1-loss) / (N_total × W_adia / η_c); the scalar multipliers do not change argmax."
      linked_ids: [claim-SWEEP-02, deliv-verdict]
    test-nine-scenarios:
      status: passed
      summary: "Nine COP values in verdict table covering all (η_c, loss_frac) combinations. Nominal COP at anchor AoA = 0.92501 (0.00007% from Phase 4 reference). η_c=0.85, loss=5% COP = 1.210 >= 1.186 (Phase 4 anchor-AoA value)."
      linked_ids: [claim-VERD-01, deliv-verdict, ref-phase4-summary]
    test-gap-quantification:
      status: passed
      summary: "gap_to_threshold = 0.2904; closest_scenario = (η_c=0.85, loss=5%, AoA=2°, COP=1.210). Limiting constraint statement: W_gross insufficient at any AoA even at η_c=1.0 (COP_max = 1.423 < 1.5). η_c* = 1.054 exceeds isothermal limit."
      linked_ids: [claim-VERD-01, deliv-verdict]
    test-backtracking:
      status: passed
      summary: "NO_GO — backtracking trigger not activated (COP never reached 1.5). All three sub-checks documented: stall_check=true (AoA_optimal=2° < 14°), lambda_eff_check=true (0.9 < 1.2748), brentq_convergence_check=true."
      linked_ids: [claim-VERD-01, deliv-verdict, deliv-sweep-table]

  references:
    ref-phase5-anchor:
      status: completed
      completed_actions: [read, gate-check, compare]
      missing_actions: []
      summary: "Loaded phase5_anchor_check.json; asserted overall_anchor_pass=true; used corot_scale_at_anchor=0.264373 and W_foil_total_J_at_anchor=246059.3 J as cross-check values; used sign_check v_loop at AoA=1° (3.465008 m/s) as cross-check target."
    ref-phase4-summary:
      status: completed
      completed_actions: [read, compare, use-as-baseline]
      missing_actions: []
      summary: "Used W_foil_total_J=246058.1 J as anchor reference for test-wfoil-independence (0.0005% agreement). Used COP_nominal=0.92501 for nominal cross-check (0.00007% agreement). Nine-scenario structure reproduced and extended with AoA_optimal."
    ref-phase2-foil:
      status: completed
      completed_actions: [verify-loaded-by-solver]
      missing_actions: []
      summary: "NACA table and foil geometry loaded by Phase 5 solver at import time (e_oswald=0.85, AR=4, chord=0.25 m, span=1.0 m). Phase 6 inherits via import — no direct read required."

  forbidden_proxies:
    fp-single-aoa:
      status: rejected
      notes: "Sweep covers 16 AoA points from 1° to 15°; explicitly rejected in script and output JSON."
    fp-cop-lossless:
      status: rejected
      notes: "COP_nominal (η_c=0.70, loss=10%) is the primary verdict metric. COP_lossless=2.204 not reported as verdict. Explicitly rejected in both output JSONs."
    fp-corot-at-vnom:
      status: rejected
      notes: "corot_scale = (v_loop_corrected / v_nom)^3 computed at each AoA. v_loop varies from 3.465 m/s (AoA=1°) to 2.373 m/s (AoA=15°). Fixed v_nom never used. Explicitly documented."
    fp-reversed-foil:
      status: rejected
      notes: "F_vert is kinematic (lift ⊥ v_rel; always negative/downward). Reversed foil is not mentioned as an improvement path anywhere in Phase 6 outputs."
    fp-fixed-vloop:
      status: rejected
      notes: "brentq called at every AoA; v_loop is solver output. Sweep table records v_loop range 2.373–3.465 m/s across AoA values. Explicitly rejected."

  uncertainty_markers:
    weakest_anchors:
      - "NACA TR-824 C_L interpolation at AoA=1° uses only the 0°–2° table interval; error < 2% of C_L_2D = 0.22. At AoA=2° (optimal), C_L=0.22 exactly from the table — no interpolation error."
      - "Co-rotation C_f Re-dependence neglected (~5%/decade variation); v_loop ranges 2.37–3.47 m/s across sweep, Re varies ≈30%; C_f error < 3% in W_corot at all AoA."
      - "AoA_optimal is 2.0° with 1° grid resolution. A denser grid (0.5° steps) might find the true optimum is between 1° and 3°. The COP function is smooth and the maximum is shallow (ΔCOPmax vs 1° and 3°: < 0.002). Does not change the NO_GO verdict."
    unvalidated_assumptions:
      - "lambda = 0.9 can be maintained as v_loop changes with AoA (motor controller holds it). If lambda cannot be maintained mechanically, v_tan and hence W_foil change."
    competing_explanations:
      - "AoA_optimal at 2° not 1°: the net_delta function has a true maximum at 2° because at 1°, the large W_foil deficit (-192 kJ) is nearly but not quite offset by the W_corot gain (+212 kJ). Net = +19 kJ. At 2°: net = +21 kJ. At 3°: net = +21 kJ (essentially tied). COP function is shallow near the optimum."
    disconfirming_observations:
      - "COP at 1° (0.9418) < COP at 2° (0.9437): confirms grid resolution is adequate; the optimum is not artificially pinned to the endpoint."
      - "COP(AoA=0) = 0.93787 from Phase 5 (without foil contribution, pure co-rotation): lower than COP_max = 0.9437. This confirms foil contribution is net positive at AoA=2°, i.e., adding a small amount of lift is beneficial even though it reduces v_loop."

comparison_verdicts:
  - subject_id: test-wfoil-independence
    subject_kind: acceptance_test
    subject_role: decisive
    reference_id: ref-phase4-summary
    comparison_kind: benchmark
    metric: relative_error
    threshold: "<= 0.001 (0.1%)"
    verdict: pass
    recommended_action: "none — anchor reproduced"
    notes: "W_foil at anchor AoA = 246059.3 J vs Phase 4 reference 246058.1 J; diff = 0.0005%"
  - subject_id: test-nine-scenarios
    subject_kind: acceptance_test
    subject_role: decisive
    reference_id: ref-phase4-summary
    comparison_kind: prior_work
    metric: relative_error
    threshold: "<= 0.0001 (0.01%)"
    verdict: pass
    recommended_action: "none — Phase 4 nominal COP reproduced"
    notes: "COP at anchor AoA (10.0128°, η_c=0.70, loss=10%) = 0.92501; diff = 0.00007%"
  - subject_id: claim-SWEEP-01
    subject_kind: claim
    subject_role: decisive
    reference_id: ref-phase5-anchor
    comparison_kind: prior_work
    metric: relative_error
    threshold: "<= 0.001 (0.1%)"
    verdict: pass
    recommended_action: "none — Phase 5 v_loop cross-check passed"
    notes: "v_loop at AoA=1° = 3.465008 m/s; Phase 5 sign_check value = 3.465008 m/s; diff = 0.0000%"

duration: ~45min
completed: 2026-03-21
---

# Phase 6 Plan 01 Summary

**Full AoA sweep [1°–15°] confirms NO_GO: COP_max = 1.210 at (η_c=0.85, loss=5%, AoA=2°) — gap to COP=1.5 is 0.290, requiring η_c*=1.054 which exceeds the isothermal compression limit.**

## Performance

- **Duration:** ~45 min
- **Completed:** 2026-03-21
- **Tasks:** 2/2 complete
- **Files created:** 3 (script + 2 JSON outputs)

## Key Results

- **AoA_optimal = 2.0°** (maximizes COP by balancing competing effects: lower AoA raises v_loop and W_corot but reduces W_foil; optimum where net_delta = ΔW_foil + ΔW_corot is maximized)
- **COP_max_nominal = 0.94373** at (η_c=0.70, loss=10%, AoA=2°) — 2.0% improvement over Phase 4 anchor (0.92501)
- **COP_max_all_scenarios = 1.210** at (η_c=0.85, loss=5%, AoA=2°) — NO_GO; gap = 0.290
- **Required η_c* = 1.054** to achieve COP=1.5 at best scenario — exceeds isothermal limit
- **At η_c=1.0, loss=5%: COP_max = 1.423 < 1.5** — COP=1.5 is physically unreachable at current geometry/depth

### Nine-Scenario COP Table at AoA_optimal = 2.0°

| | loss=5% | loss=10% | loss=15% |
|---|---|---|---|
| **η_c=0.65** | 0.9250 | 0.8763 | 0.8276 |
| **η_c=0.70** | 0.9962 | **0.9437** (nominal) | 0.8913 |
| **η_c=0.85** | **1.2096** (best) | 1.1460 | 1.0823 |

### Competing Effects at AoA_optimal vs AoA=10.0128° Baseline

| AoA | ΔW_foil (J) | ΔW_corot (J) | Net ΔJ | ΔCOP |
|---|---|---|---|---|
| 1° | −192,335 | +211,516 | +19,181 | +0.0168 |
| **2° (optimal)** | **−146,976** | **+168,329** | **+21,353** | **+0.0187** |
| 3° | −111,589 | +132,831 | +21,242 | +0.0186 |
| 10° | −29.5 | +59.7 | +30.2 | +0.0000 |

## Task Commits

1. **Task 1: Full AoA sweep + sweep table** — `a9d0d4d` (compute: 16-point sweep, competing-effects breakdown, sweep JSON)
2. **Task 2: Nine-scenario verdict + NO_GO** — `fedeb7d` (compute: nine-scenario grid, gap analysis, verdict JSON)
3. **SUMMARY.md** — (this commit)

## Files Created

- `analysis/phase6/aoa_full_sweep.py` — Sweep execution script (imports Phase 5 solver; gate check; 16-point sweep; nine-scenario grid; all verification prints; both JSON outputs)
- `analysis/phase6/outputs/phase6_sweep_table.json` — 16-point AoA sweep table with competing-effects breakdown, lambda_eff, corot_scale, beta_deg, etc.
- `analysis/phase6/outputs/phase6_verdict.json` — Nine-scenario COP table, VERDICT=NO_GO, gap=0.290, η_c*=1.054, scenario-independence proof, tack-flip caveat

## Deviations

- **[Rule 4 — Missing Component] NACA monotonicity region correction:** The plan specified monotonicity check for AoA < 14°, but NACA C_L peaks at ~12° (C_L(12)=1.14 > C_L(14)=1.05). This is a physical near-stall feature, not a bug. The monotonicity check was restricted to AoA < 12° and documented in the sweep table. This is an inline correction (adds accurate documentation to the plan's approximation note about "AoA=14° clamp region").

## Physics Consistency Checks

1. **Energy conservation:** W_buoy_total = 619,338.48 J constant across all 16 AoA points (AoA-independent, as required)
2. **W_foil v_loop-independence:** W_foil = F_tan × lambda × H (v_loop cancels); F_tan × 0.9 × 18.288 × 24 = 246,059.3 J = computed value (exact)
3. **Co-rotation scaling:** corot_scale(anchor) = (2.383484/3.7137)³ = 0.264373 = Phase 5 reference (0.0001% diff)
4. **COP formula:** (619,338 + 246,059 + 189,971) × 0.90 / (30 × 23959.45 / 0.70) = 0.92501 ✓
5. **Stall check:** AoA_optimal=2° << 14° stall limit; lambda_eff=0.9 << lambda_max=1.2748 at all points
6. **Phase 4 anchor reproduction:** COP=0.92501, diff=0.00007% (< 0.01% required) ✓
7. **Phase 5 v_loop cross-check:** v_loop(1°)=3.465008 m/s, diff=0.0000% ✓

## Physical Interpretation

The AoA sweep reveals a shallow COP maximum near 2°. The optimum arises from competing effects:
- **Reducing AoA** → higher v_loop → larger co-rotation benefit (W_corot scales as v³) but smaller W_foil (lower C_L)
- **The crossover:** At AoA=2°, the co-rotation gain (+168 kJ) slightly outweighs the foil loss (−147 kJ), giving net +21 kJ vs the anchor. But this ~2% improvement is far too small to bridge the gap to COP=1.5.

Even at the theoretical maximum (AoA=0, no foil, maximum co-rotation), COP = 0.938 — confirming that co-rotation savings alone are insufficient. The fundamental limitation is that W_gross cannot exceed ~1.08 MJ at any AoA in [0°,15°] while W_pump = 1.027 MJ at η_c=0.70, leaving no room to reach COP=1.5.

## Next Phase Readiness

**Milestone v1.1 (AoA Parametric Sweep) is complete.** The verdict is final: **NO_GO under all realistic assumptions.**

The path to COP ≥ 1.5 requires one or more of:
1. Increased operating depth H (deeper loop → larger W_buoy per cycle)
2. Increased vessel count or size (larger W_buoy total)
3. Novel W_gross augmentation not captured in the current model
4. Reducing W_pump by operating at lower pressure ratio (less depth per compression cycle)

**Tack-flip caveat (unquantified prototype measurement priority):** An additional 5% effective loss from tack-flip reduces COP_max from 0.944 to 0.891. This is the highest-priority prototype measurement.

## Self-Check: PASSED

- [x] All acceptance tests pass (test-gate, test-sweep-coverage, test-monotonicity, test-wfoil-independence, test-aoa-optimal, test-scenario-independence, test-nine-scenarios, test-gap-quantification, test-backtracking)
- [x] All 7 pitfall guards confirmed True in both output JSONs
- [x] No forbidden proxies used
- [x] Phase 4 COP reproduction: 0.00007% < 0.01% tolerance
- [x] Phase 5 v_loop cross-check: 0.0000% < 0.1% tolerance
- [x] All contract claims: passed
- [x] All deliverables: produced and verified
- [x] Required η_c* computed and physically interpreted
- [x] Tack-flip caveat quantified
