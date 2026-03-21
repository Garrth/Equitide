# Phase 6: Full AoA Parametric Sweep and Go/No-Go Verdict - Research

**Researched:** 2026-03-19
**Domain:** Classical fluid mechanics / engineering energy analysis — parametric sweep and verdict
**Confidence:** HIGH

<!-- ASSERT_CONVENTION: unit_system=SI, F_vert_sign=Phase2 (negative=downward=opposing_buoyancy) -->

## Summary

Phase 6 is a purely computational phase. The validated solver from Phase 5 (`analysis/phase5/aoa_sweep_solver.py`) is the sole numerical instrument. The work is: call `compute_COP_aoa(AoA_target_deg, eta_c, loss_frac)` over a grid of AoA values and nine (eta_c, loss_frac) scenarios, collect results, find the COP maximum, and deliver a go/no-go verdict against COP ≥ 1.5.

The central physics question is where COP(AoA) is maximized over [1°, 15°]. Two effects compete: (1) decreasing AoA reduces |F_vert|, raises v_loop, and multiplies co-rotation savings by (v_loop/v_nom)³; (2) decreasing AoA also reduces the horizontal torque F_tan (proportional to C_L) and thus W_foil. The v^3 scaling of co-rotation means the co-rotation channel dominates at lower AoA, while W_foil falls. Phase 5 already computed COP(AoA=10°) = 0.925 and confirmed the solver; the sweep will map the full COP(AoA) landscape. Based on the competing-effects analysis below, COP is expected to peak somewhere in the range AoA ∈ [2°, 6°], likely near 3°–5° where the co-rotation gain is substantial but the foil work is not yet negligible.

However, because even the best-case Phase 4 nine-scenario value is COP_max = 1.186 (at η_c = 0.85, loss = 0.05), and the co-rotation term drops by (2.384/3.714)³ = 0.264 at AoA = 10°, the AoA sweep must find whether lower AoA recovers enough co-rotation benefit to push any scenario above 1.5. Based on pre-computation analysis (see Mathematical Framework), the nine-scenario table will most likely remain below 1.5 for all scenarios with the co-rotation correction, but the sweep quantifies this definitively.

**Primary recommendation:** Import `compute_COP_aoa` from `analysis/phase5/aoa_sweep_solver.py`, sweep AoA over ≥ 15 points in [1°, 15°] using uniform 1° spacing (plus the Phase 4 anchor at 10.0128° for cross-check), evaluate all nine scenarios at each AoA, then report COP_max and the go/no-go verdict table in the same nine-scenario format as Phase 4.

## User Constraints

No CONTEXT.md exists for this phase. There are no locked user decisions. All discretionary choices (sweep spacing, output format, sensitivity breakdown) are at the agent's discretion subject to the project contract.

**Key contract constraints that function as locked requirements:**
- Forbidden proxies: (1) COP at a single AoA without the full sweep; (2) co-rotation computed at v_nom instead of v_loop_corrected(AoA); (3) any reference to reversed foil mounting
- Required deliverables: SWEEP-01 (COP(AoA) table ≥ 10 points), SWEEP-02 (AoA_optimal + COP_max), VERD-01 (go/no-go verdict, all 9 scenarios)
- Required priors: foil01_force_sweep.json (Phase 2), phase4_summary_table.json — both already loaded by Phase 5 solver

## Active Anchor References

| Anchor / Artifact | Type | Why It Matters Here | Required Action | Where It Must Reappear |
| ----------------- | ---- | ------------------- | --------------- | ---------------------- |
| `analysis/phase5/aoa_sweep_solver.py` | Prior artifact (validated solver) | The only numerical instrument for Phase 6; already validated against Phase 4 anchor to 0.001% | Import and call `solve_v_loop_aoa`, `compute_COP_aoa` — do not re-implement | All tasks in Phase 6 |
| `analysis/phase5/outputs/phase5_anchor_check.json` | Gate artifact | Phase 6 must confirm `overall_anchor_pass = true` before running any new sweep points | Read `overall_anchor_pass`; halt if false | Task 1 gate check |
| `analysis/phase4/outputs/phase4_summary_table.json` | Baseline / comparison artifact | Nine-scenario table at AoA=10.0128°; Phase 6 sweep must produce a matching-format table and show improvement (or lack thereof) vs. AoA=10° | Load and compare; use as reference column for "AoA_optimal vs. AoA=10° baseline" | Plan, execution, final comparison table |
| `analysis/phase4/outputs/sys01_coupled_velocity.json` | Anchor values | Phase 4 anchor v_loop=2.383479, COP=0.92501; cross-check point for sweep at AoA=10.0128° | Verify sweep point at AoA=10.0128° matches within 0.5% | Sweep cross-check task |
| `analysis/phase2/outputs/foil01_force_sweep.json` | Input data | NACA table + foil geometry (AR=4, e_oswald=0.85) used by solver | Already loaded by Phase 5 solver (no separate action needed) | Solver input chain |
| Phase 5 data points (already computed) | Prior intermediate results | F_vert sign checks and COP bound points at AoA=1,5,10,15° | Use as 4 of the required ≥10 sweep points (no re-computation needed; read from phase5_anchor_check.json for consistency) | Sweep table |

**Missing or weak anchors:** None. Phase 5 delivered a fully validated solver and all required inputs are in JSON files already loaded by the solver. The Phase 6 task is entirely sweep execution and reporting.

## Conventions

| Choice | Convention | Alternatives | Source |
| ------ | ---------- | ------------ | ------ |
| Unit system | SI: N, m/s, J, W, dimensionless | Imperial cross-checks in output where noted | Phase 1–5 convention lock |
| F_vert sign | Negative = downward = opposing buoyancy | Positive-upward convention (not used here) | Phase 2 sign convention; Phase 5 ASSERT_CONVENTION |
| AoA parameterization | AoA_target is free parameter; mount_angle = beta − AoA_target computed dynamically | Fixed mount_angle (Phase 4 approach, not used in Phase 5/6) | Phase 5 parameterization |
| Co-rotation scaling | P_net_corot corrected by (v_loop(AoA)/v_nom)³ | Uncorrected at v_nom (forbidden proxy) | Phase 4 PITFALL-COROT |
| Stall clamp | AoA clamped to [0°, 14°] in NACA table; sweep upper limit 15° runs clamped at 14° for foil physics | No clamp | Phase 2/5 convention |
| Nine-scenario grid | η_c ∈ {0.65, 0.70, 0.85} × loss_frac ∈ {0.05, 0.10, 0.15} | Other ranges | Phase 4 contract |
| COP threshold | 1.5 W/W for "GO" verdict | — | Project contract |

**CRITICAL: All COP values reported use the co-rotation correction (v_loop(AoA)/v_nom)³. Reporting uncorrected co-rotation values is a forbidden proxy.**

## Mathematical Framework

### Key Equations and Starting Points

| Equation | Name/Description | Source | Role in This Phase |
| -------- | ---------------- | ------ | ------------------ |
| F_net(v_loop) = F_b_avg + F_vert(v_loop, AoA) − ½ρ_w C_D_hull A_frontal v_loop² = 0 | Per-vessel force balance (brentq residual) | Phase 5 Eq. 05.2 | Solved by brentq at each AoA to find v_loop(AoA) |
| F_vert = −½ρ_w A_foil v_loop²(1+λ²)(C_L,3D cos β + C_D,tot sin β) | Vertical foil force (per vessel) | Phase 5 Eq. 05.1 | Input to brentq; always negative for AoA ∈ [1°,14°] |
| F_tan = q(C_L,3D sin β − C_D,tot cos β) | Tangential foil force (per vessel) | Phase 2 / Phase 5 solver | Determines shaft power P_shaft = F_tan × v_tan |
| W_foil = N_asc × F_tan × λ × v_loop × t_asc + N_desc × same | Total foil work (ascending + descending) | Phase 5 compute_COP_aoa | Note: W_foil ∝ F_tan × 2H × λ (v_loop cancels in F_tan × v_tan × t_asc = F_tan × λ × v_loop × H/v_loop = F_tan × λ × H) |
| P_net,corot,corrected = P_net,corot,uncorrected × (v_loop(AoA)/v_nom)³ | Co-rotation correction (PITFALL-COROT) | Phase 5 Eq. 05.3 | Co-rotation benefit scales as v³; critical at low AoA where v_loop ≈ v_nom |
| W_corot = P_net,corot,corrected × t_cycle = P_net,corot,corrected × 2H/v_loop | Total co-rotation work | Phase 5 compute_COP_aoa | Scales as v_loop² for fixed P: corot_scale × (2H/v_loop) ∝ v_loop³/v_nom³ × 1/v_loop = v_loop²/v_nom³ × 2H |
| COP = (W_buoy + W_foil + W_corot) × (1 − loss_frac) / (N_total × W_adia / η_c) | System COP | Phase 4/5 formula | Primary output at each (AoA, η_c, loss_frac) point |

### AoA Sweep Landscape: Competing Effects Analysis

This is the central planning insight for sweep design. Let the fixed quantities be: H = 18.288 m, λ = 0.9, β = 48.01° (constant), v_nom = 3.7137 m/s, W_adia = 23959.45 J, W_iso = 20644.62 J, N_total = 30, N_asc = N_desc = 12.

**W_foil as a function of AoA:**

Substituting t_asc = H/v_loop into P_shaft × t_asc:
```
W_foil_pv = F_tan × (λ × v_loop) × (H / v_loop) = F_tan × λ × H
```
So W_foil is independent of v_loop! It depends only on F_tan(AoA) ∝ (C_L,3D sin β − C_D,tot cos β). This simplifies the sweep: W_foil is monotonically increasing with AoA (up to stall) because C_L,3D increases.

At β = 48.01°: sin β = 0.743, cos β = 0.669.

- AoA=1°: C_L,3D ≈ 0.22×(4/6) = 0.147, C_D,tot ≈ 0.006 + 0.147²/(π×0.85×4) ≈ 0.008; F_tan ∝ 0.147×0.743 − 0.008×0.669 = 0.109−0.005 = 0.104
- AoA=5°: C_L,3D ≈ 0.55×(4/6) = 0.367, C_D,tot ≈ 0.021; F_tan ∝ 0.367×0.743 − 0.021×0.669 = 0.273−0.014 = 0.259
- AoA=10°: C_L,3D ≈ 1.06×(4/6) = 0.707, C_D,tot ≈ 0.060; F_tan ∝ 0.707×0.743 − 0.060×0.669 = 0.525−0.040 = 0.485

W_foil at AoA=1° is approximately 0.104/0.485 ≈ 21% of W_foil at AoA=10°.

**W_corot as a function of AoA:**

```
W_corot(AoA) = P_net_corot,uncorrected × (v_loop(AoA)/v_nom)³ × (2H/v_loop(AoA))
             = P_net_corot,uncorrected × v_loop(AoA)² / v_nom³ × 2H
```

W_corot ∝ v_loop(AoA)². At AoA=1°: v_loop ≈ 3.465 m/s → scale = 3.465²/3.7137² = 0.872. At AoA=10°: v_loop ≈ 2.384 m/s → scale = 2.384²/3.7137² = 0.412.

Wait — let me restate precisely. From compute_COP_aoa:
```
W_corot = P_net_corot_corrected × t_cycle
        = P_net,uncorr × (v/v_nom)³ × (2H/v)
        = P_net,uncorr × 2H × v² / v_nom³
```

At AoA=1°: W_corot ≈ P_net,uncorr × 2H × (3.465²/3.7137³) = P_net,uncorr × 2H × 0.232
At AoA=10°: W_corot ≈ P_net,uncorr × 2H × (2.384²/3.7137³) = P_net,uncorr × 2H × 0.110

(Checking against Phase 5 anchor: P_net_corot_uncorr=46826 W, 2H=36.576 m, v=2.384 m/s → 46826 × 36.576 × (2.384²/3.7137³) = 46826 × 36.576 × 0.1102 = 189,990 J ≈ 189,971 J. Matches Phase 5 JSON to 0.01%.)

At AoA=1°: W_corot ≈ 46826 × 36.576 × (3.465²/3.7137³) = 46826 × 36.576 × 0.2320 ≈ 399,800 J (approximately 2.1× the AoA=10° value).

**W_buoy is constant** at N_total × W_iso = 30 × 20,644.62 = 619,339 J regardless of AoA.

**W_pump is constant** (numerator varies, denominator is fixed): N_total × W_adia / η_c = 30 × 23,959.45 / η_c.

At η_c=0.70: W_pump = 30 × 23,959.45 / 0.70 = 1,026,834 J.

**COP trade-off summary for Phase 6:**

| AoA (°) | v_loop (m/s) | W_foil rel. to AoA=10° | W_corot rel. to AoA=10° | Expected COP direction |
| -------- | ------------ | ----------------------- | ------------------------ | ---------------------- |
| 1        | 3.465        | ~21%                   | ~210%                    | W_corot gain likely exceeds W_foil loss |
| 5        | 2.832        | ~53%                   | ~146%                    | Both channels competitive |
| 10       | 2.384        | 100% (baseline)        | 100%                     | Phase 4 baseline |
| 15       | 2.373        | ~115% (clamped foil)   | ~99%                     | Small gain from W_foil |

**Predicted COP maximum location:** At AoA=1°, the large co-rotation gain (×2.1) combined with the W_buoy + W_foil total determines where the sum peaks. The expected landscape has a maximum somewhere in [1°, 6°] with the co-rotation gain dominating at the low end. Whether any scenario in the nine-scenario grid crosses 1.5 depends primarily on whether the co-rotation benefit at low AoA can offset the lower W_foil. At η_c=0.85, loss_frac=0.05, the Phase 4 nine-scenario maximum was 1.186 at AoA=10°. At AoA=1°, W_corot increases by ×2.1 (from ~190k to ~400k J), which adds ~210k J to W_gross ≈ 1,055k J, giving W_gross ≈ 1,265k J. After 5% loss: W_net ≈ 1,202k J. W_pump at η_c=0.85 = 845,628 J. COP ≈ 1,202/846 ≈ 1.42. This is below 1.5 but substantially better than 1.186. The exact value requires the solver.

**Conclusion: The sweep will likely show COP_max ≈ 1.3–1.5 in the best scenario (η_c=0.85, loss_frac=0.05) at low AoA, but will not cross 1.5 under the co-rotation-corrected physics.** This is the expected go/no-go outcome; the sweep is necessary to confirm it precisely.

### λ_eff Check

λ_eff = ω_loop × r / v_loop_vertical. At fixed λ = 0.9 design, v_tan = 0.9 × v_loop. As v_loop rises at low AoA, λ_eff stays fixed at 0.9 (it is a design parameter). The Phase 2 stall boundary was λ_max = 1.2748 (λ where AoA_eff = 14°). Since λ is held constant at 0.9 < 1.2748, there is no stall concern from the velocity ratio at any sweep point. Stall risk comes only from the AoA clamp at 14° (applied internally by interpolate_naca).

### Required Techniques

| Technique | What It Does | Where Applied | Standard Reference |
| --------- | ------------ | ------------- | ------------------ |
| scipy.optimize.brentq (via Phase 5 solver) | Finds v_loop root of per-vessel force balance | Every sweep point | Phase 5 solver (already validated) |
| numpy array operations | Store sweep results, compute column stats | Sweep table construction | Phase 5 pattern |
| Linear interpolation of NACA table | C_L, C_D at non-integer AoA | Internal to Phase 5 solver | NACA TR-824 (already validated) |
| numpy.argmax | Find AoA_optimal in sweep array | SWEEP-02 deliverable | Standard numpy |

### Approximation Schemes

| Approximation | Small Parameter | Regime of Validity | Error Estimate | Alternatives if Invalid |
| ------------- | --------------- | ------------------ | -------------- | ----------------------- |
| Quasi-steady foil forces | Reduced freq k = f_flip×c/v_rel << 0.1 | k < 0.05 at this system's speeds | ~5% in forces | Full unsteady panel method (not warranted) |
| Fixed λ = 0.9 across AoA sweep | Δv_loop/v_nom < 0.2 | All AoA in [1°, 15°]; v_loop in [2.37, 3.47] m/s | Forces exact for given λ | Variable-λ sweep (different phase scope) |
| Prandtl lifting-line for AR = 4 | AR − 2 > 0 (i.e., AR > 2) | AR = 4 ≥ 3 (valid) | ~10% in C_L,3D | XFLR5 VLM (not warranted for feasibility) |
| Tacking symmetry: W_foil_desc = W_foil_asc | Perfect tacking | Same AoA, same geometry on both sides | ~5% (Phase 2 confirmation) | Separate ascending/descending AoA optimization |

## Standard Approaches

### Approach 1: Uniform 1° AoA Grid with Anchor Cross-Check (RECOMMENDED)

**What:** Sweep AoA ∈ {1°, 2°, 3°, ..., 15°} plus the Phase 4 anchor point 10.0128°. This gives 16 points (≥ 10 required for SWEEP-01). Evaluate all nine (η_c, loss_frac) scenarios at each point.

**Why standard:** Uniform spacing provides regular resolution across the sweep range. 1° resolution is sufficient given the smoothly varying COP landscape (no sharp features expected). The anchor cross-check at 10.0128° provides a built-in validation of the sweep loop.

**Key steps:**
1. Gate check: confirm `phase5_anchor_check.json overall_anchor_pass == true`
2. Build sweep loop: `AoA_grid = [1, 2, 3, ..., 15] + [10.0128]`; sort for clean output
3. For each AoA: call `solve_v_loop_aoa(AoA)` to get v_loop; call `compute_COP_aoa(AoA, eta_c, loss_frac)` for each of 9 scenarios
4. Store results in a structured dict indexed by (AoA, eta_c, loss_frac)
5. For each scenario, find AoA_optimal = argmax COP over AoA grid
6. Cross-check: COP at AoA=10.0128° must match Phase 4 anchor within 0.5%
7. Extract nine-scenario verdict table at AoA_optimal
8. Write phase6_sweep.json and phase6_verdict.json

**Known difficulties:**
- Step 3: Import path for `aoa_sweep_solver.py` requires sys.path manipulation (use the pattern from Phase 5)
- Step 3: The solver prints diagnostic output on import; redirect or suppress for clean sweep output
- Step 6: AoA=10.0128° must be a separate call to `solve_v_loop_aoa(10.0128)` — do not use the nearest integer grid point 10°

**Deliverables from this approach:**
- `phase6_sweep.json`: full (AoA, v_loop, COP_nominal, W_foil, W_corot, ...) for all 16 grid points × 9 scenarios
- `phase6_verdict.json`: nine-scenario verdict table at AoA_optimal; go/no-go verdicts
- Human-readable summary: COP(AoA) table, AoA_optimal per scenario, competing-effects breakdown

### Approach 2: Denser Grid Near Expected Optimum (FALLBACK)

**What:** After the 1° uniform sweep in Task 1, if the COP maximum is near a grid boundary (e.g., COP is still rising at AoA=1°) or shows a plateau over 2+ degrees, add a dense sub-sweep at 0.25° spacing in the region [AoA_opt − 1°, AoA_opt + 1°].

**When to switch:** Only if the maximum found in Approach 1 occurs at the boundary of the grid (AoA=1° or AoA=15°), indicating the true maximum may lie outside the surveyed range. If COP is monotonically increasing all the way to AoA=1°, the mathematical boundary is at AoA=0° (which the solver handles via C_L=0); in that case, report AoA_optimal = 1° with a note that COP continues to rise toward AoA=0 but foil work is minimal there.

**Tradeoffs:** Additional computation (trivial) vs. cleaner characterization of the optimum.

### Anti-Patterns to Avoid

- **Using v_nom instead of v_loop(AoA) for co-rotation:** The co-rotation correction is forbidden to omit. Using the uncorrected P_net_corot at each AoA inflates COP by a factor of ~4× at AoA=10° and ~1.2× at AoA=1°. The solver already handles this correctly — do not override or bypass the PITFALL-COROT guard.
  - _Example:_ The Phase 4 uncorrected COP at η_c=0.70, loss=0.10 was 1.388; the corrected value is 0.925. Do not report the uncorrected value as the Phase 6 result.

- **Reporting COP at a single AoA without the sweep:** The contract requires SWEEP-01 (≥10 points). Even if the nominal operating point (AoA=10°) is known, the sweep is required.

- **Using AoA=10° as "optimal" without checking the sweep:** The Phase 5 design AoA was chosen for anchor validation, not optimization. AoA_optimal is determined by the sweep, not assumed.

- **Re-implementing the solver instead of importing it:** The Phase 5 solver is validated. Any re-implementation risks introducing the N_ascending multiplier error (which gave 63% wrong v_loop in Phase 5 Task 1) or missing pitfall guards.

- **Claiming GO if COP > 1.0 but < 1.5:** The threshold is 1.5, not 1.0. COP > 1.0 means net positive energy output (break-even exceeded) but does not meet the project target.

- **Proposing reversed foil mounting to improve COP:** F_vert is kinematic; see feedback_fvert_kinematic.md. This is an invalid optimization lever. AoA is the only lever.

## Existing Results to Leverage

### Established Results (DO NOT RE-DERIVE)

| Result | Exact Form | Source | How to Use |
| ------ | ---------- | ------ | ---------- |
| W_iso = W_buoy identity | W_iso = P_atm × V_0 × ln(P_r) = 20,644.6 J | Phase 1; METHODS.md | W_buoy_total = 30 × 20,644.6 J = 619,338 J (constant across all AoA) |
| W_pump formula | W_pump = N_total × W_adia / η_c; W_adia = 23,959.45 J | Phase 1 JSON | Denominator of COP; constant per scenario |
| Phase 4 nine-scenario COP table (corrected) | η_c=0.85, loss=0.05: COP=1.186; η_c=0.65, loss=0.15: COP=0.811 | phase4_summary_table.json sensitivity_summary.COP_table_corrected | Baseline reference column for sweep comparison |
| Phase 5 data points at AoA = 1°, 5°, 10°, 15° | v_loop = 3.465, 2.832, 2.384, 2.373 m/s; F_vert = -146.1, -472.2, -663.7, -668.0 N | phase5_anchor_check.json sign_checks | Read these directly; do not re-solve unless verifying solver consistency |
| F_vert always negative in [1°, 14°] | Algebraic: F_vert = -q(C_L,3D cos β + C_D,tot sin β) < 0 | Phase 5 claim-ANAL-01 (algebraically proved) | Do not check F_vert sign as a blocker; confirmed true |
| Per-vessel force balance (not N_asc multiplier) | F_net = F_b_avg + F_vert_pv - F_drag_hull | Phase 5 Rule 5 deviation | The solver uses this correctly; no action needed |
| NACA 0012 table (Re~10⁶) | AoA: 0–14°; C_L: 0.00–1.05; C_D0: 0.006–0.031 | NACA TR-824 (Abbott et al., 1945) | Already in solver; do not re-look up |

**Key insight:** Phase 6 does not need to re-derive any physics. Every quantity is computed by the validated Phase 5 solver. The planner's task is sweep orchestration and output formatting, not new physics derivation.

### Useful Intermediate Results

| Result | What It Gives You | Source | Conditions |
| ------ | ----------------- | ------ | ---------- |
| W_foil ∝ F_tan × λ × H (v_loop-independent) | W_foil is set by F_tan alone; co-rotation is the AoA-sensitive output channel | Phase 6 research derivation above | Fixed λ=0.9, symmetric tacking |
| W_corot ∝ v_loop(AoA)² × (2H/v_nom³) × P_net,uncorr | Co-rotation benefit is quadratic in v_loop (not cubic) after accounting for cycle time | Phase 6 research derivation above | Fixed H, v_nom |
| COP maximum expected at AoA ≈ 2°–5° | Co-rotation gain exceeds W_foil reduction in this range; sweep will confirm | Phase 6 research competing-effects analysis | Approximate; depends on detailed numbers |
| Best-scenario COP at low AoA ≈ 1.3–1.5 (η_c=0.85, loss=0.05) | Likely NO_GO but close to threshold | Phase 6 research estimate | Approximate; exact from solver |

### Relevant Prior Work

| Result | Source | What to Extract |
| ------ | ------ | --------------- |
| Phase 4 nine-scenario verdict: all NO_GO at AoA=10° | phase4_summary_table.json SYS-03_verdict | Baseline; Phase 6 confirms or improves |
| Phase 4 bound argument: Phase 2 upper-bound × (1-0.15) = 1.749 > 1.5 | phase4_summary_table.json SYS-03_verdict.bound_argument | Upper-bound context: system can in principle reach 1.5 if η_c and losses are favorable |
| Phase 4 COP_lossless = 2.204 | phase4_summary_table.json SYS-02 | Gross energy budget; confirms no First Law violation |

## Computational Tools

### Core Tools

| Tool | Version/Module | Purpose | Why Standard |
| ---- | -------------- | ------- | ------------ |
| `analysis/phase5/aoa_sweep_solver.py` | Phase 5 validated | The solver: solve_v_loop_aoa + compute_COP_aoa | Validated to Phase 4 anchor at 0.001%; all inputs loaded from JSON |
| Python 3.10+ | stdlib + json | Sweep loop orchestration, output JSON | Already used in all prior phases |
| numpy | any recent | Array operations for sweep results and statistics | Standard; used throughout project |
| matplotlib | any recent | COP(AoA) plot and competing-effects figure | Standard |

### Supporting Tools

| Tool | Purpose | When to Use |
| ---- | ------- | ----------- |
| json (stdlib) | Read phase5_anchor_check.json for gate; write sweep output | Gate check (Task 1), output (all tasks) |
| scipy.optimize.brentq | Called internally by aoa_sweep_solver.py | No direct call needed from Phase 6 script |

### Computational Feasibility

| Computation | Estimated Cost | Bottleneck | Mitigation |
| ----------- | -------------- | ---------- | ---------- |
| brentq solve at one AoA | < 1 ms | None | — |
| Full sweep: 16 AoA × 9 scenarios | < 1 second | None | — |
| Output JSON write | < 10 ms | None | — |
| Plot generation | < 2 seconds | None | — |

**Total Phase 6 runtime: < 5 seconds.** No computational feasibility concern.

**Installation / Setup:**
```bash
# All packages already used in Phases 1–5; no new installations required.
# If matplotlib is not already installed:
pip install matplotlib
```

## Validation Strategies

### Internal Consistency Checks

| Check | What It Validates | How to Perform | Expected Result |
| ----- | ----------------- | -------------- | --------------- |
| Anchor cross-check at AoA=10.0128° | Sweep loop produces same result as Phase 5 anchor | Compare sweep COP at 10.0128° to phase5_anchor_check.json COP_nominal_phase5=0.92501 | Difference < 0.5% |
| Phase 5 sign checks at AoA=1°,5°,10°,15° | v_loop values match Phase 5 JSON | Compare sweep v_loop to phase5_anchor_check.json sign_checks values | Difference < 0.1% |
| COP monotonicity: as loss_frac increases, COP decreases at fixed AoA and η_c | No accounting error | Check ∂COP/∂loss_frac < 0 for all (AoA, η_c) | Strictly decreasing |
| COP monotonicity: as η_c increases, COP increases at fixed AoA and loss_frac | No accounting error | Check ∂COP/∂η_c > 0 for all (AoA, loss_frac) | Strictly increasing |
| W_buoy constant across AoA | W_buoy = 619,338 J at all AoA points | Read W_buoy_total_J from compute_COP_aoa output at each AoA | Constant to < 0.1% |
| AoA_optimal consistent: same AoA maximizes COP for all 9 scenarios | COP(AoA) shape is scenario-independent (only scale changes with η_c, loss_frac) | Check that AoA_optimal(η_c, loss_frac) is the same for all 9 scenarios | Same AoA_optimal ± 1° |

**The last check is important:** Because W_buoy and W_pump are constant, and W_foil and W_corot both depend only on AoA (not on η_c or loss_frac), the ratio W_foil + W_corot / W_pump does not change with η_c or loss_frac. Therefore the AoA that maximizes the numerator also maximizes COP for all scenarios — the optimal AoA is scenario-independent. If the sweep finds different AoA_optimal values for different scenarios, there is a bug.

### Known Limits and Benchmarks

| Limit | Parameter Regime | Known Result | Source |
| ----- | ---------------- | ------------ | ------ |
| AoA → 0° | C_L = 0, pure drag | v_loop ≈ v_nom ≈ 3.691 m/s (Phase 5 JSON); COP = 0.938 (Phase 5 JSON limiting_case_AoA0) | phase5_anchor_check.json |
| AoA = 10.0128° | Phase 4 design point | v_loop = 2.383484 m/s; COP = 0.92501 (η_c=0.70, loss=0.10) | phase5_anchor_check.json |
| AoA = 15° (clamped at 14° for NACA) | Maximum tested in Phase 5 | v_loop = 2.373 m/s; F_vert = -668.0 N | phase5_anchor_check.json |

### Numerical Validation

| Test | Method | Tolerance | Reference Value |
| ---- | ------ | --------- | --------------- |
| Sweep at AoA=10.0128° matches Phase 4 anchor | Direct comparison | < 0.5% | COP = 0.92501, v_loop = 2.383479 |
| W_foil(AoA=10°) from sweep matches Phase 4 JSON | Direct comparison | < 0.5% | W_foil_total = 246,058 J |
| W_corot(AoA=10°) from sweep matches Phase 4 JSON | Direct comparison | < 1% | W_corot_total = 189,971 J |

### Red Flags During Computation

- If v_loop at AoA=10° differs by > 1% from 2.384 m/s: import error or solver modification — halt and diagnose
- If COP increases with increasing loss_frac at any (AoA, η_c): sign error in loss formula
- If W_corot(AoA=1°) < W_corot(AoA=10°): co-rotation scaling is inverted — check (v_loop/v_nom)³ formula direction
- If COP_max > 3.0 at any scenario: likely co-rotation is uncorrected (using v_nom instead of v_loop) — check PITFALL-COROT guard
- If brentq raises ValueError at any AoA in [1°, 15°]: check fallback scan logic; verify F_b_avg + F_vert(v_lo) > 0 (vessel can ascend)
- If the nine-scenario table shows all scenarios have exactly the same COP: η_c or loss_frac is not being passed correctly

## Common Pitfalls

### Pitfall 1: Co-Rotation Uncorrected at v_nom (PITFALL-COROT)

**What goes wrong:** Using P_net_corot_W_uncorrected = 46,826 W × t_cycle at v_nom without the (v_loop/v_nom)³ correction overestimates W_corot by 1/0.264 = 3.79× at AoA=10°.

**Why it happens:** The Phase 5 solver computes the correction correctly, but if Phase 6 code bypasses the solver or re-implements the energy balance, it may omit this scaling.

**How to avoid:** Import and call `compute_COP_aoa` directly; never compute W_corot manually in Phase 6 code.

**Warning signs:** COP_nominal at AoA=10°, η_c=0.70, loss=0.10 should be ≈ 0.925. If it is ≈ 1.388 (Phase 4 uncorrected value), the correction is missing.

**Recovery:** Add the (v_loop/v_nom)³ factor and divide the cycle-average power by the scaling.

### Pitfall 2: N_ascending Multiplier in Force Balance (Phase 5 Rule 5 Deviation)

**What goes wrong:** Including N_ascending = 12 as a multiplier on F_vert in the per-vessel force balance gives v_loop = 0.872 m/s (63% error).

**Why it happens:** The Plan pseudocode in Phase 5 had this error; the solver was corrected before validation.

**How to avoid:** Use `solve_v_loop_aoa` as provided; do not re-implement the force balance in Phase 6.

**Warning signs:** v_loop at AoA=10° ≈ 0.87 m/s instead of ≈ 2.38 m/s.

### Pitfall 3: Reporting COP at AoA=10° as the Sweep Result

**What goes wrong:** Since Phase 4/5 already computed COP at AoA=10.0128°, it is tempting to skip the sweep and report that value. This violates the contract deliverable SWEEP-01.

**How to avoid:** Run the full sweep loop; report the COP(AoA) table explicitly.

### Pitfall 4: Wrong Comparison Baseline for "Improvement"

**What goes wrong:** Reporting that AoA=optimal "improves" COP vs. a wrong reference (e.g., uncorrected Phase 4 COP of 1.388 instead of corrected 0.925).

**How to avoid:** Use Phase 4 corrected nine-scenario table from `phase4_summary_table.json sensitivity_summary.COP_table_corrected` as the comparison baseline. The corrected values are the ones labeled `"label": "corrected (v_loop=2.384 m/s co-rotation)"`.

### Pitfall 5: AoA_optimal Differs Across Scenarios Due to Bug

**What goes wrong:** If the COP calculation has a bug that depends on η_c or loss_frac in the AoA-dependent terms (W_foil or W_corot), different scenarios will appear to have different optimal AoA values.

**Why it happens:** W_foil and W_corot depend only on AoA (not on η_c or loss_frac); if a scenario-dependent term incorrectly modifies them, AoA sensitivity differs across scenarios.

**How to avoid:** Verify that the AoA that maximizes COP is the same for all nine scenarios before reporting AoA_optimal.

### Pitfall 6: Stall Clamp at AoA=15° Misinterpreted

**What goes wrong:** The NACA table is clamped at 14°; AoA=15° runs at C_L(14°)=1.05. This means v_loop at 14° and 15° are nearly identical (as confirmed by Phase 5: 2.383 vs 2.373 m/s). Reporting the 15° result without noting the clamp may mislead.

**How to avoid:** Note in the output table that AoA > 14° is clamped to 14° in the NACA table. Report "AoA=15° (NACA clamped at 14°)" in the table footnote.

## Level of Rigor

**Required for this phase:** Numerical evidence — the solver is the calculation; outputs are exact (within brentq tolerance of 1e-8).

**What this means concretely:**
- brentq tolerance is already 1e-8 (Phase 5 standard); no looser tolerance allowed
- All nine scenarios must be computed; no interpolation between scenarios
- AoA grid must have ≥ 15 uniformly-spaced points (1°, 2°, ..., 15°) plus the anchor at 10.0128°
- Verdicts are binary: COP ≥ 1.5 = GO, COP < 1.5 = NO_GO; no partial verdicts
- The go/no-go table must exactly mirror the Phase 4 nine-scenario format (η_c rows, loss_frac columns) for direct comparison

## State of the Art

This phase is project-internal; there is no relevant literature state-of-the-art for "AoA parametric sweep of a buoyancy hydrofoil engine." The methodology (parameter sweep over a validated model) is standard engineering practice.

| Old Approach | Current Approach | When Changed | Impact |
| ------------ | ---------------- | ------------ | ------ |
| Fixed AoA=38° mount (Phase 4) | AoA_target as free parameter (Phase 5/6) | Phase 5 parameterization | Enables sweep optimization; Phase 5 verified no regression |

## Open Questions

1. **Does COP_max cross 1.5 at any scenario?**
   - What we know: best Phase 4 scenario (η_c=0.85, loss=0.05) gives COP=1.186 at AoA=10°. Reducing AoA to 1° approximately doubles W_corot, potentially pushing COP to ~1.4.
   - What's unclear: whether co-rotation gain at AoA=1°–5° is large enough to reach 1.5 given the W_foil reduction.
   - Impact: determines whether verdict is GO or NO_GO.
   - Recommendation: The sweep resolves this definitively. Pre-computation estimate suggests NO_GO but close. Be prepared to report "closest approach to 1.5" with the gap quantified.

2. **Is the COP landscape unimodal over [1°, 15°]?**
   - What we know: W_foil is monotone increasing with AoA; W_corot is monotone decreasing. Their sum is expected to have a single maximum.
   - What's unclear: The exact shape near the minimum (does W_foil dominate at all AoA > 5°?).
   - Impact: If the landscape is not unimodal, report all local maxima.
   - Recommendation: Proceed with uniform sweep; numpy.argmax finds the global maximum directly.

3. **Does any scenario show v_loop > v_nom at low AoA?**
   - What we know: At AoA=0°, v_loop ≈ 3.691 m/s ≈ v_nom. At AoA=1°, v_loop = 3.465 m/s < v_nom.
   - What's unclear: Whether the brentq solver is well-conditioned in the regime v_loop → v_nom.
   - Impact: Minor; the fallback log-space scan in the solver handles this.
   - Recommendation: Monitor for unusual v_loop values; the solver's fallback bracket handles the edge case.

## Alternative Approaches if Primary Fails

| If This Fails | Because Of | Switch To | Cost of Switching |
| ------------- | ---------- | --------- | ----------------- |
| Import `aoa_sweep_solver.py` | Path resolution on Windows | Explicit sys.path.insert with REPO_ROOT | 5 minutes |
| brentq convergence at AoA=1° | v_loop near v_nom, shallow residual | Tighten initial bracket: v_lo=3.0, v_hi=3.8 m/s | 5 minutes |
| Nine-scenario loop completes but COP is NaN | Loss_frac or eta_c passed as wrong type | Cast to float explicitly | 5 minutes |

**Decision criteria:** The solver has already demonstrated convergence at AoA=1°, 5°, 10°, 15° in Phase 5. There is no expected failure mode. Alternatives above are protective planning only.

## Sweep Design Recommendations (Planner Guidance)

### Grid Spacing

Use uniform 1° spacing: AoA ∈ {1.0, 2.0, 3.0, ..., 15.0} = 15 integer points, plus 10.0128° for the anchor cross-check. This gives 16 total evaluation points, satisfying the SWEEP-01 requirement of ≥ 10 points.

**Rationale for 1° spacing:** The COP landscape is smooth (no sharp features; interpolated NACA table). 1° resolution pinpoints AoA_optimal to ± 0.5°, sufficient for a feasibility verdict.

**No need for denser spacing unless** COP at AoA=1° > COP at AoA=2° and COP is still rising monotonically toward AoA=0° at the grid boundary. In that case, add a sub-sweep at 0.25° spacing near AoA=1°. The Phase 5 AoA=0° limiting case (COP=0.938) already shows COP at AoA=0° is lower than at AoA=10° (0.925 nominal, but AoA=0° at η_c=0.70 loss=0.10 was 0.938 — actually higher). This suggests the maximum is likely in the AoA=1°–5° range.

### AoA Boundary Handling

- Lower bound AoA=1°: Physical minimum for meaningful foil work. AoA=0° is a degenerate case (no lift, pure drag).
- Upper bound AoA=15°: Includes stall regime (clamped at 14°); documents diminishing returns.
- The solver handles AoA outside [0°, 14°] via interpolate_naca clamp — safe to include up to 15°.

### Competing-Effects Breakdown Format

Present an additional table showing, for each AoA in the sweep at the reference scenario (η_c=0.70, loss=0.10):

| AoA (°) | v_loop (m/s) | W_foil (J) | W_corot (J) | W_gross (J) | COP_nominal |
| -------- | ------------ | ---------- | ----------- | ----------- | ----------- |

This separates the two competing channels and shows directly where the cross-over point is.

### Nine-Scenario Verdict Table Format

Mirror Phase 4 format exactly, at AoA_optimal:

| Scenario | η_c | loss_frac | COP_nominal | W_pump (J) | GO / NO_GO |
| -------- | --- | --------- | ----------- | ---------- | ---------- |

Include a "Delta vs. AoA=10°" column showing the improvement from Phase 4 baseline.

### Gap Analysis for NO_GO Verdict

If COP_max < 1.5 in all scenarios, quantify the gap:
- Gap = 1.5 − COP_max (absolute)
- Gap as % of W_pump: what additional energy source (J) would close the gap
- Which scenario is closest to 1.5 and what parameter change would reach it (increase η_c to X, or reduce loss_frac to Y)

This provides actionable information for the prototype design team.

## Caveats and Alternatives

**Caveat 1: Pre-computation COP_max estimate.** The analysis above estimates COP_max ≈ 1.3–1.5 at η_c=0.85, loss=0.05, low AoA. This is based on the analytical competing-effects framework (W_corot ∝ v_loop²). The exact value depends on the precise v_loop at each AoA from the brentq solver. The estimate is reliable to ~10%; the sweep provides the exact answer.

**Caveat 2: Co-rotation is the dominant term.** At AoA=10°, W_corot = 189,971 J is 36% of W_gross. At AoA=1°, W_corot ≈ 400,000 J is ~51% of W_gross. The go/no-go verdict is strongly dependent on the Phase 3 co-rotation estimate (P_net_corot = 46,826 W at v_nom), which carries MEDIUM confidence (Taylor-Couette approximation for a discrete-vessel geometry). If co-rotation is 50% lower than modeled, COP_max drops to ~0.9–1.1 even at low AoA. The Phase 6 verdict should note this sensitivity.

**Caveat 3: Tack-flip losses are unquantified.** Phase 4 noted tack-flip transient losses as unquantified and potentially 5 percentage points of additional loss. Phase 6 uses the same loss_frac parameter (5–15% mechanical) which does not include tack-flip. Any GO verdict should be flagged as conditional on tack-flip losses being within the modeled range.

**Caveat 4: What if a different alternative approach was too quickly dismissed?** The only alternative approach not explored is computing COP at both the mechanical-loss lower bound (5%) and at arbitrary loss values to find the threshold at which COP=1.5. This is a 1D root-find (trivial given the solver) and could be added as an additional deliverable without changing the sweep structure. The planner should include this as an optional task: "find loss_frac_threshold such that COP(AoA_optimal, η_c=0.85, loss_frac_threshold) = 1.5."

## Sources

### Primary (HIGH confidence)

- Phase 5 validated solver: `analysis/phase5/aoa_sweep_solver.py` — the numerical instrument for Phase 6; validated against Phase 4 anchor to 0.001%
- NACA TR-824 (Abbott, von Doenhoff & Stivers, 1945) — C_L, C_D tables; already embedded in solver
- Phase 4 summary table: `analysis/phase4/outputs/phase4_summary_table.json` — nine-scenario baseline reference
- Phase 5 anchor check: `analysis/phase5/outputs/phase5_anchor_check.json` — gate artifact and spot-check reference

### Secondary (MEDIUM confidence)

- Phase 3 co-rotation model: P_net_corot = 46,826 W at v_nom — Taylor-Couette approximation; MEDIUM confidence (confirmed internally consistent to Phase 4/5; physical model uncertainty ± factor of 2)
- Phase 6 research pre-computation: W_foil independence of v_loop; W_corot ∝ v_loop² — derived analytically in this document; confirmed against Phase 5 numerical results

### Tertiary (LOW confidence)

- None.

## Metadata

**Confidence breakdown:**
- Mathematical framework: HIGH — all equations are Phase 5 validated; W_foil/W_corot AoA scaling derived analytically and confirmed numerically
- Standard approaches: HIGH — uniform sweep is standard; solver is validated; no novel methods needed
- Computational tools: HIGH — same Python/scipy stack as prior phases; < 5 second runtime
- Validation strategies: HIGH — cross-checks against Phase 4/5 anchors are exact; COP monotonicity checks are algebraically provable

**Research date:** 2026-03-19
**Valid until:** Indefinite for the physics (equations do not change). Valid while Phase 5 solver is not modified. If `analysis/phase5/aoa_sweep_solver.py` is updated, re-check anchor cross-check tolerance.
