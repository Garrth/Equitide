# Research Digest: v1.1 AoA Parametric Sweep

Generated: 2026-03-21
Milestone: v1.1
Phases: 5–6

## Narrative Arc

The v1.0 study left one analytical lever untested: angle of attack (AoA). The Phase 4 system verdict (NO_GO, COP_nominal=0.925) was delivered at the design AoA of ~10°, where the self-consistent v_loop = 2.384 m/s (36% below the uncoupled estimate) due to the downward F_vert load. Phase 5 rederived the force balance as an explicit function of AoA_target, inverting the Phase 4 parameterization: instead of fixing the mount angle and computing the effective AoA, v1.1 fixes the desired AoA and computes the implied mount angle dynamically at each brentq evaluation. The Phase 4 anchor was reproduced to 0.001% before any new AoA was computed. Phase 6 then swept 16 points from 1° to 15°, revealing a shallow COP maximum at AoA=2°: reducing AoA raises v_loop (and thus co-rotation savings, which scale as v³) but reduces horizontal torque (lower C_L). The competing effects peak at 2° where net ΔJ = +21 kJ over the 10° baseline — a 2% COP improvement that is far too small to bridge the gap to 1.5. The nine-scenario verdict table confirms NO_GO across all η_c × loss_frac combinations; the required compressor efficiency η_c* = 1.054 exceeds the isothermal thermodynamic limit, making COP=1.5 physically unreachable at the current geometry and depth.

## Key Results

| Phase | Result | Equation / Value | Validity Range | Confidence |
| ----- | ------ | ---------------- | -------------- | ---------- |
| 5 | F_vert(AoA) always negative (downward) | F_vert = −½ρ_w A_foil v_rel²(C_L,3D cos β + C_D,tot sin β) | AoA ∈ [1°,15°], λ=0.9 | High (confirmed at 4 AoA checkpoints) |
| 5 | Anchor validation PASS | v_loop=2.383484 m/s (0.0002% err), COP=0.92501 (0.00007% err), F_vert=−663.86 N (0.0005% err) | AoA=10.0128°, Phase 4 reference | High |
| 6 | AoA_optimal = 2.0° (scenario-independent) | argmax_AoA COP(AoA) = 2° for all 9 (η_c, loss_frac) combinations | λ=0.9, AoA ∈ [1°,15°] | High (algebraic proof: only W_gross depends on AoA) |
| 6 | COP_max_nominal = 0.94373 | COP at (η_c=0.70, loss=10%, AoA=2°); +2.0% over Phase 4 anchor | Nominal scenario | High |
| 6 | COP_max_all_scenarios = 1.210 | (η_c=0.85, loss=5%, AoA=2°); gap = 0.290 to threshold | Best-case scenario | High |
| 6 | VERDICT: NO_GO | η_c* = 1.054 > 1.0 (isothermal limit); at η_c=1.0, loss=5%: COP_max=1.423 < 1.5 | All AoA ∈ [1°,15°], all 9 scenarios | High |

## Methods Employed

- **Phase 5:** AoA parameterization inversion — AoA_target is free parameter; mount_angle = β(v_loop) − AoA_target computed dynamically at each brentq evaluation (departure from Phase 4 fixed mount_angle=38°)
- **Phase 5:** scipy.optimize.brentq with xtol=rtol=1e-8 for coupled (v_loop, ω) solution; bracket [0.05·v_nom, 2.0·v_nom] with log-space fallback scan
- **Phase 5:** Prandtl lifting-line: C_L,3D = C_L,2D/(1+2/AR); C_D,i = C_L,3D²/(π·e·AR); NACA TR-824 table interpolation
- **Phase 6:** Phase 5 solver import pattern (sys.path manipulation, compute_COP_aoa public interface); gate check on overall_anchor_pass before sweep
- **Phase 6:** Competing-effects breakdown: ΔW_foil and ΔW_corot relative to anchor baseline at each AoA; nine-scenario grid scan; scenario-independence verification
- **Phase 6:** η_c* back-calculation: η_c* = N_total × W_adia / (W_gross_optimal × (1−loss_min)) needed for COP=1.5

## Convention Evolution

| Phase | Convention | Description | Status |
| ----- | ---------- | ----------- | ------ |
| Phase 0 | Unit system: SI | N, m/s, J, W, Pa; Imperial in parentheses only | Active |
| Phase 0 | z=0 at tank bottom, z increases upward | P(z) = P_atm + ρ_w·g·(H−z) | Active |
| Phase 0 | F_vert sign: Phase 2 convention | Negative = downward = opposing buoyancy | Active |
| Phase 2 | N_active_foil = 24 (not 30) | 12 ascending + 12 descending; 6 vessels in transition arcs | Active |
| Phase 4 | brentq coupled solver | Per-vessel force balance: F_b,avg + F_vert,pv − F_drag,hull,pv = 0 | Active |
| Phase 4 | Co-rotation v³ scaling | P_net,corot,corrected = P_net,corot,uncorrected × (v_loop,c/v_nom)³ | Active |
| Phase 5 | AoA parameterization (NEW) | AoA_target is free parameter; mount_angle = β − AoA_target (dynamic, not fixed at 38°) | Active |
| Phase 5 | λ held constant at 0.9 | ω adjusts so v_tan/v_loop = 0.9 at each AoA; v_loop varies | Active |

No convention changes from Phase 0 values; Phase 5 added AoA parameterization inversion.

## Figures and Data Registry

| File | Phase | Description | Paper-ready? |
| ---- | ----- | ----------- | :----------: |
| analysis/phase5/aoa_sweep_solver.py | 5 | AoA-parameterized brentq solver module; importable by Phase 6 | No (script) |
| analysis/phase5/outputs/phase5_anchor_check.json | 5 | Anchor validation record: overall_anchor_pass=true, all tolerances passed | Yes |
| analysis/phase6/aoa_full_sweep.py | 6 | Full sweep execution script with gate check and nine-scenario grid | No (script) |
| analysis/phase6/outputs/phase6_sweep_table.json | 6 | 16-point AoA sweep table: F_vert, v_loop, W_foil, W_corot, COP, competing-effects at each point | Yes |
| analysis/phase6/outputs/phase6_verdict.json | 6 | Nine-scenario COP table, VERDICT=NO_GO, gap=0.290, η_c*=1.054, scenario-independence | Yes |

## Open Questions

1. What design changes (depth, vessel count, geometry) are required to reach COP ≥ 1.5 — to be addressed in v1.2?
2. Tack-flip loss fraction (estimated +5% COP reduction from +5% effective loss): this is the highest-priority prototype measurement; reduces COP_max from 0.944 to 0.891 in the nominal scenario
3. Can a deeper loop (e.g., 100 ft / 30.5 m, P_r ≈ 3.92) or larger vessel count reach COP=1.5 at realistic compressor efficiency? Requires a new depth/count sensitivity analysis.

## Dependency Graph

```
Phase 5 "AoA Sweep Formulation and Anchor Validation"
  requires:
    - Phase 1: F_b_avg_N=1128.86 N, v_terminal_nominal=3.7137 m/s, W_adia_J=23959.45 J
    - Phase 2: NACA 0012 table polars, foil geometry (AR=4, e_oswald=0.85), N_ascending=12
    - Phase 3: P_net_corot_W_uncorrected=46826.0 W at v_nominal
    - Phase 4: anchor v_loop=2.383479 m/s, F_vert=-663.8588 N, AoA=10.0128 deg, COP=0.92501
  provides:
    - AoA-parameterized brentq solver: solve_v_loop_aoa(AoA_target_deg)
    - Full COP computation: compute_COP_aoa(AoA_target_deg, eta_c, loss_frac)
    - Phase 4 anchor validation: VALD-01 all three tolerances pass
    - F_vert sign confirmed negative for all AoA in [1,15] deg
    - Phase 5 module path: analysis/phase5/aoa_sweep_solver.py (importable for Phase 6)

  -> Phase 6 "Full AoA Parametric Sweep and Go/No-Go Verdict"
       requires:
         - Phase 5: validated aoa_sweep_solver.py, overall_anchor_pass=true
         - Phase 4: anchor values and nine-scenario grid structure; W_foil_reference=246058.1 J
       provides:
         - AoA_optimal = 2.0° (scenario-independent)
         - COP_max_nominal = 0.94373 at (eta_c=0.70, loss=10%, AoA=2°)
         - Nine-scenario verdict table: COP_max range 0.828–1.210
         - VERDICT: NO_GO; gap=0.290; eta_c*=1.054 > 1.0 (isothermal limit)
         - Scenario independence confirmed: argmax_AoA identical for all nine scenarios
```

## Mapping to Original Objectives

| Requirement | Status | Fulfilled by | Key Result |
| ----------- | :----: | ------------ | ---------- |
| ANAL-01: Derive F_vert(AoA) analytically | Complete | Phase 5 Plan 01 | F_vert = −½ρ_w A_foil v_rel²(C_L,3D cos β + C_D,tot sin β); always negative in [1°,15°] |
| ANAL-02: Coupled (v_loop, ω) as function of AoA via brentq | Complete | Phase 5 Plan 01 | solve_v_loop_aoa(AoA_target_deg); v_loop ∈ [2.373, 3.465] m/s across sweep |
| VALD-01: Anchor check — reproduce Phase 4 at AoA≈10° | Complete | Phase 5 Plan 01 | v_loop error 0.0002%, COP error 0.00007%, F_vert error 0.0005% — all pass |
| SWEEP-01: Full AoA sweep 1°–15°, ≥10 points, 5 quantities | Complete | Phase 6 Plan 01 | 16-point sweep; F_vert, v_loop, W_foil, W_corot, COP at each point |
| SWEEP-02: Identify AoA_optimal | Complete | Phase 6 Plan 01 | AoA_optimal = 2.0°; competing effects quantified; scenario-independence proved |
| VERD-01: Go/no-go verdict under nine-scenario grid | Complete | Phase 6 Plan 01 | NO_GO; COP_max=1.210; η_c*=1.054 > 1.0; COP=1.5 physically unreachable |
| EXTD-01: Map required design changes (if NO_GO) | Partial | Phase 6 Plan 01 | η_c* identified; qualitative path analysis provided; quantitative v1.2 sweep deferred |
| EXTD-02: λ sensitivity at λ=0.8 or 1.0 | Deferred | — | Not executed; AoA_optimal is scenario-independent (algebraic argument); λ sweep is next-tier |
