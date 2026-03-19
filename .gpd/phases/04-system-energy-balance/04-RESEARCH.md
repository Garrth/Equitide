# Phase 4: System Energy Balance — Research

**Researched:** 2026-03-18
**Domain:** Classical mechanics, thermodynamics — buoyancy engine system integration
**Confidence:** HIGH

<!-- ASSERT_CONVENTION: natural_units=SI, fourier_convention=N/A, metric_signature=N/A -->

---

## Summary

Phase 4 is the integration phase: all component results from Phases 1–3 are assembled into a complete, signed energy balance and a definitive go/no-go verdict is delivered against the 1.5 W/W threshold. The primary research challenge is not deriving new physics — it is correctly coupling the F_vert feedback into the self-consistent (v_loop, ω) solution, accounting for every loss term with appropriate uncertainty, and structuring the sensitivity analysis so that the verdict is robust rather than point-estimate fragile.

The key unresolved item from Phases 1–3 is the F_vert coupling: hydrofoil vertical force is 1.15 × F_b_avg, which means the ascending vessel is not in pure buoyancy-drag equilibrium — the foil is pulling the vessel upward as well. This changes the terminal velocity v_loop (upward), which in turn changes all per-vessel power terms. The magnitude of this coupling determines whether the Phase 2 COP_partial of 2.057 (labeled as an upper bound) survives to a Phase 4 verdict of COP ≥ 1.5. The self-consistency equation is the central mathematical task.

The second research question is completeness: what loss terms are commonly omitted from buoyancy-engine balances? Chain/bearing mechanical losses (5–15% of total power), which have been flagged throughout earlier phases, are the most consequential unquantified item. The sensitivity analysis must demonstrate that the go/no-go verdict is stable across the full credible range of this parameter.

**Primary recommendation:** Structure Phase 4 around three sequential tasks: (1) solve the coupled (v_loop, ω) self-consistency equation with F_vert included, producing corrected per-vessel energy terms; (2) assemble the complete signed energy balance with all 30 vessels and all loss terms; (3) compute COP with uncertainty range and deliver the verdict. Use the existing JSON outputs from Phases 1–3 as the authoritative input source — do not re-derive any quantity that is already locked.

---

## Active Anchor References

| Anchor / Artifact | Type | Why It Matters Here | Required Action | Where It Must Reappear |
|---|---|---|---|---|
| `analysis/phase1/outputs/phase1_summary_table.json` | Prior artifact | W_pump_J=34227.8, W_buoy_J=20644.62, v_loop=3.7137 m/s, F_b_avg=1128.86 N | Load directly; these are the Phase 4 energy balance denominators | Plan: energy balance table; execution: all COP calculations |
| `analysis/phase2/outputs/phase2_summary_table.json` | Prior artifact | F_tan, W_foil_asc/desc per vessel, F_vert/F_b_avg=1.15, COP_partial=2.057 (upper bound), geometry | Load directly; F_vert ratio drives the coupled solution | Plan: coupled velocity task; execution: F_vert correction |
| `analysis/phase3/outputs/phase3_summary_table.json` | Prior artifact | P_corot_W=720, P_net_at_fss_W=46826, COP_corot_at_fss=0.603, F_vert_flag_propagated=true | Load directly; P_corot enters as explicit loss term in system balance | Plan: loss term table; execution: all P_net calculations |
| F_vert/F_b_avg = 1.15 flag | Method requirement | Phase 2 and Phase 3 COP values are labeled upper bounds; Phase 4 coupled solution is MANDATORY | Solve self-consistency equation for corrected v_loop; do not use v_loop=3.7137 m/s as final value | Plan: Task 1; execution: v_loop_corrected |
| COP_partial = 2.057 (Phase 2, upper bound) | Benchmark | Starting upper bound for Phase 4; Phase 4 verdict must be lower than or equal to this | Never use 2.057 as the Phase 4 answer; use it as the upper bound to bound the correction | Plan: verdict section; execution: validation check |
| COP_buoy_only = 0.603 (Phase 3 at f_stall) | Benchmark | Lower bound for COP when foil forces go to zero; Phase 4 COP must be between 0.603 and 2.057 | Sanity check: Phase 4 COP must fall in [0.603, 2.057] | Execution: bounds check |
| W_pump at eta_c=0.70: 34,228 J | Benchmark (Phase 1 verified) | Denominator of all COP calculations at nominal eta_c | Use as nominal; sweep over eta_c=[0.65, 0.85] for sensitivity | Plan: sensitivity table |
| Phase 2 target from Phase 1: W_foil_net ≥ 30,697 J/cycle to reach COP=1.5 at eta_c=0.70 | Method requirement | Sets the minimum foil work needed; Phase 4 checks whether the corrected foil terms clear this bar | Verify in execution | Verdict: go/no-go table |

**Missing or weak anchors:** Chain/bearing mechanical loss fraction is the only major unquantified input. The PITFALLS.md and SUMMARY.md both cite 5–15% of total power; this range must be explicitly carried as uncertainty in the Phase 4 sensitivity analysis. No external literature anchor exists for this specific machine geometry — treat as a scenario parameter with three levels: optimistic 5%, nominal 10%, conservative 15%.

---

## Conventions

| Choice | Convention | Source |
|---|---|---|
| Unit system | SI throughout: J (energy), W (power), N (force), m (length), rad/s (angular velocity), dimensionless (COP, f, lambda) | Phase 1–3 artifacts; SUMMARY.md |
| Pressure | Absolute throughout; P_atm = 101,325 Pa; P(z) = P_atm + rho_w g (H-z) | CONVENTIONS.md |
| Buoyancy integral | Variable-volume V(z) = V_0 P_atm / P(z); constant-volume approximation FORBIDDEN | PITFALLS.md PITFALL-C1 |
| COP label | All COP values from Phases 1–3 labeled COP_partial; Phase 4 delivers COP_system (the final value) | Phase 2 pattern-established |
| Power sign | Energy in (pumping) is positive denominator; energy out (shaft work) is positive numerator; losses enter as subtractions from numerator | METHODS.md §8 |
| Co-rotation fraction | f = v_water_h / v_vessel_h; v_rel_h = v_h(1-f); v_rel_v = v_loop (unchanged by co-rotation) | Phase 3 convention |
| N_ascending | 24 vessels ascending at design operating point (lambda=0.9, N_total=30; 6 fill/release vessels not producing torque) | Phase 2 JSON: N_ascending=12, N_descending=12, N_total=24 active |
| Velocity triangle | beta = arctan(v_loop / v_tan) = arctan(1/lambda); F_tan = L sin(beta) - D cos(beta) | Phase 2 Plan 01 |

**CRITICAL: All COP calculations use W_pump = W_adia / eta_c (NOT W_iso as pump energy). W_iso appears only in the buoyancy work numerator. Using W_iso in the denominator is PITFALL-M1 and underestimates the input by 25–54%.**

---

## Mathematical Framework

### Key Equations and Starting Points

| Equation | Name/Description | Source | Role in This Phase |
|---|---|---|---|
| COP_system = (W_buoy + W_foil_asc + W_foil_desc + P_net_corot × t_cycle − W_losses) / W_pump | System COP — complete signed balance | METHODS.md §8; this phase | Central deliverable |
| v_loop_corrected = sqrt(2(F_b_avg + F_vert − F_chain) / (rho_w C_D A_frontal)) | Coupled terminal velocity with F_vert | METHODS.md §3 + Phase 2 F_vert result | Task 1 — self-consistency |
| F_vert = C_L_3D × (0.5 rho_w v_rel² A_foil) × sin(alpha_3D) | Vertical component of hydrofoil lift | Phase 2 geometry; F_vert/F_b_avg = 1.14994 | Task 1 — provides F_vert_N |
| W_pump = W_adia / eta_c | Actual pump work per vessel | Phase 1 locked | Denominator of COP |
| W_buoy = P_atm V_0 ln(P_r) = W_iso | Buoyancy work per vessel (thermodynamic identity) | Phase 1 verified gate | Numerator term 1 |
| W_foil_asc = F_tan × v_tan × t_asc | Foil work per ascending vessel | Phase 2 Plan 01 | Numerator term 2 |
| W_foil_desc = F_tan × v_tan × t_desc | Foil work per descending vessel (tacking confirmed) | Phase 2 Plan 02 | Numerator term 3 |
| P_net_corot = P_drag_saved(f) − P_corot(f) | Net co-rotation power benefit | Phase 3 Plan 02 | Numerator term 4 (positive) |
| W_losses = W_chain_friction + W_bearing + W_hull_drag + W_foil_profile_drag | All mechanical and fluid losses | METHODS.md §8; PITFALLS.md M4 | Numerator subtractions |
| lambda = v_tan / v_loop | Tip-speed ratio (controls foil AoA and F_tan) | Phase 2 | Coupling parameter |
| lambda_eff(f) = lambda_design / (1 − f) | Effective lambda with co-rotation | Phase 3 Plan 01 | Determines stall boundary |

### Required Techniques

| Technique | What It Does | Where Applied | Standard Reference |
|---|---|---|---|
| Fixed-point iteration for v_loop | Solves v_loop_corrected = sqrt(2(F_b_avg + F_vert(v_loop)) / (rho_w C_D A)) self-consistently | Task 1 — coupled velocity | METHODS.md §3; Phase 1 Plan 03 |
| Complete signed energy accounting | Assembles all positive and negative energy terms per cycle; computes COP | Task 2 — energy balance | METHODS.md §8 |
| Parametric sweep | COP as function of (L/D, eta_c, W_losses_fraction) | Task 3 — sensitivity analysis | Phase 1 computational approach |
| Uncertainty propagation | Carries known uncertainties from each phase into final COP range | Task 3 — confidence interval | SUMMARY.md cross-validation matrix |
| Scalar JSON loading discipline | Loads all prior-phase values from JSON; no re-derivation or hardcoding | All tasks | Phase 2/3 pattern established |

### Approximation Schemes

| Approximation | Parameter | Regime of Validity | Error Estimate | Alternatives if Invalid |
|---|---|---|---|---|
| Quasi-steady terminal velocity | Vessel acceleration / total velocity < 5% | Valid: ascent takes ~4.9 s, acceleration time ~0.5 s | ~5% error in v_loop | Full coupled ODE (unnecessary for feasibility) |
| Per-vessel COP formula scales to system | All vessels identical; symmetry of ascending = descending | Valid by design symmetry | Exact by symmetry | Per-position integration (unnecessary) |
| Taylor-Couette P_corot ±50% | Smooth cylinder approximation | Discrete-vessel geometry introduces factor-of-2 correction | ±50% at C_f level | Physical torque measurement (future prototype) |
| Chain/bearing losses as fixed fraction | Machine-specific; not modeled analytically | Feasibility level only | 5–15% range covers typical values | Mechanical engineering measurement |
| Ideal gas, Boyle's law | P < 10 atm, T ≈ constant during ascent | Valid: P_r = 2.767 < 10 atm; ascent in ~5 s (isothermal) | < 0.1% on W_iso | Van der Waals equation (unnecessary) |

---

## Standard Approaches

### Approach 1: Coupled Iteration then Direct Assembly (RECOMMENDED)

**What:** (1) Solve the coupled (v_loop, ω) equation with F_vert feedback using fixed-point iteration, producing v_loop_corrected. (2) Re-evaluate all per-vessel energy terms at the corrected velocity. (3) Sum across all 30 vessels and subtract all losses to get W_net. (4) Compute COP = W_net / W_pump_total. (5) Sensitivity sweep.

**Why standard:** Fixed-point iteration is the standard method for self-consistent terminal velocity problems in fluid mechanics. It converges in < 10 iterations (established in Phase 1). The coupling through F_vert is linear in the force balance — it simply adds to the upward force — so convergence is guaranteed.

**Key steps:**

1. Load all prior-phase JSON values. Do not re-derive or hardcode any prior quantity.
2. Solve for v_loop_corrected via fixed-point iteration: v_{n+1} = sqrt(2(F_b_avg + F_vert_N − F_chain) / (rho_w C_D A_frontal)), where F_vert_N = F_vert_fraction × F_b_avg × correction. Note: F_vert depends on v_rel, which depends on v_loop. The iteration must account for this.
3. Recompute omega_corrected = lambda_design × v_loop_corrected / r_arm.
4. Recompute W_foil_asc_corrected and W_foil_desc_corrected at the corrected (v_loop, omega) pair.
5. Assemble the 30-vessel energy balance: compute total W_pump_in, total W_buoy, total W_foil_asc, total W_foil_desc, P_net_corot × t_cycle, and all losses.
6. Compute COP_system = (W_buoy_total + W_foil_total + W_corot_benefit) / W_pump_total × (1 − mechanical_loss_fraction).
7. Sensitivity sweep over [eta_c, L/D (via NACA AoA interpolation), mechanical_loss_fraction].
8. Deliver go/no-go verdict: COP_system ≥ 1.5 for any credible (eta_c, L/D, loss) combination?

**Known difficulties at each step:**

- Step 2: F_vert is a strong function of C_L_3D, which Phase 2 computed at AoA=7 deg. The corrected v_loop changes the velocity triangle, which changes the effective AoA. For a fixed-mount foil, this must be re-evaluated. If AoA changes significantly, the F_vert fraction may change. Flag if the correction loop shifts AoA by more than 2 degrees.
- Step 5: N_ascending and N_descending must match the Phase 2 definition (12+12=24 active; 6 vessels in fill/release transition). Do not use N_total=30 for the torque sum without verifying that fill-transition vessels produce zero torque.
- Step 6: Avoid double-counting co-rotation benefit. P_net_corot is already net of P_corot (Phase 3 PITFALL-C3). Do not add P_drag_saved and subtract P_corot separately if Phase 3 provides P_net_at_fss directly.

### Approach 2: Conservative Bound without Coupled Correction (FALLBACK)

**What:** Use Phase 2 COP_partial = 2.057 as the upper bound. Estimate the F_vert correction as a downward adjustment to v_loop, compute the fractional change in COP, and argue the corrected COP is still above 1.5.

**When to switch:** If the fixed-point iteration for the coupled system fails to converge or produces physically implausible results (e.g., v_loop_corrected > 6 m/s or < 1 m/s).

**Tradeoffs:** This approach does not deliver a precise COP value; it only confirms whether the margin above 1.5 is sufficient to survive the correction. It is less informative for the sensitivity analysis but satisfies the minimum go/no-go requirement.

### Anti-Patterns to Avoid

- **Using W_iso as pump energy:** W_pump = W_adia / eta_c. W_iso appears only as buoyancy work (numerator), never as the pump energy (denominator). This is PITFALL-M1.
  - _Example:_ COP = W_iso / W_iso = 1.0 is a mathematical identity, not a physics result. It would incorrectly imply a perfect-compressor system is at break-even.

- **Treating COP_partial = 2.057 as the Phase 4 answer:** This is an upper bound. Phase 4 must deliver the corrected value after F_vert coupling.
  - _Example:_ Reporting Phase 4 COP = 2.057 without running the F_vert correction loop would violate the explicit flag in every Phase 2 and Phase 3 output file.

- **Summing ascending torque and descending torque as independent additive contributions without chain coupling check:** Tacking converts descending drag from pure loss to useful torque; it does not add a new energy source. The total output is still bounded by total buoyancy input. (PITFALL-C4)
  - _Example:_ If W_foil_asc + W_foil_desc + W_buoy > W_pump × COP_ceiling, a term has been double-counted.

- **Omitting chain/bearing mechanical losses:** These are the largest unquantified loss. Even 10% of total power at COP~2 represents a ~0.2 reduction in COP. At marginal COP values (1.5–1.7), this can flip the verdict.
  - _Example:_ If gross COP = 1.6 and mechanical loss fraction = 0.10, net COP = 1.44 < 1.5 → NO-GO.

- **Reporting a go/no-go verdict based on a single point estimate:** The sensitivity analysis is not optional (SYS-03). The verdict must show COP over the credible range of (L/D, eta_c, loss fraction).

---

## Existing Results to Leverage

**These are established by prior phases and must be CITED, not re-derived.**

### Established Results (DO NOT RE-DERIVE)

| Result | Exact Form / Value | Source | How to Use |
|---|---|---|---|
| W_iso = W_buoy (thermodynamic identity) | W_buoy = P_atm V_0 ln(P_r) = 20,644.62 J (per vessel) | Phase 1, gate BUOY-02; analytical proof | Buoyancy term in COP numerator |
| W_adia = 23,959.45 J (per vessel) | γ/(γ-1) P_atm V_0 (P_r^((γ-1)/γ) − 1) | Phase 1, thrm01 JSON | Numerator of W_pump formula |
| W_pump at eta_c=0.70: 34,227.8 J (per vessel) | W_adia / eta_c | Phase 1, phase1_summary_table.json | COP denominator at nominal eta_c |
| W_pump range: 28,188–36,861 J | eta_c = 0.65–0.85 | Phase 1 JSON | Sensitivity parameter bounds |
| F_b_avg = 1128.86 N | W_iso / H = 20644.62 / 18.288 | Phase 1 JSON | Force balance input |
| v_loop_nominal = 3.7137 m/s | Fixed-point iteration at C_D=1.0, F_chain=0 | Phase 1 buoy03 JSON | Upper bound for v_loop; corrected in Task 1 |
| v_loop_conservative = 3.0752 m/s | At C_D=1.2, F_chain=200 N | Phase 1 buoy03 JSON | Conservative scenario for sensitivity |
| W_foil_ascending per vessel at lambda=1: 20,766.59 J | F_tan × v_tan × t_asc = 1135.524 × 3.7137 × 4.9245 | Phase 2 phase2_summary_table.json | Numerator term (upper bound) |
| W_foil_descending per vessel at lambda=1: 20,766.46 J | Tacking confirmed; same formula | Phase 2 phase2_summary_table.json | Numerator term (upper bound) |
| F_vert / F_b_avg = 1.14994 | From Phase 2 foil01; NACA 0012 at AoA=7 deg | Phase 2 ascending_foils section | Coupling parameter for Task 1 |
| COP_partial at lambda=0.9: 2.057 | (W_buoy + W_foil_asc + W_foil_desc) / W_pump per vessel | Phase 2 phase2_summary_table.json | Upper bound; Phase 4 must correct |
| P_corot at f_stall: 720 W | Taylor-Couette, omega_w = f_stall × omega_design | Phase 3 phase4_inputs JSON | Co-rotation maintenance cost (loss) |
| P_net_at_fss: 46,826 W | P_drag_saved − P_corot at f=f_stall=0.294 | Phase 3 phase4_inputs JSON | Co-rotation net benefit (positive term) |
| f_stall = 0.294003 | lambda_design / lambda_max = 0.9 / 1.2748 subtracted from 1 | Phase 3 corot01 JSON | Maximum achievable co-rotation fraction |
| Phase 4 COP must lie in [0.603, 2.057] | Lower bound = COP at stall (foils gone); upper bound = Phase 2 COP | Phase 3 summary | Sanity check bounds |
| W_buoy total (30 vessels) = 20,644.62 × 30 J | Linear scale | Phase 1 | Total buoyancy input |
| W_pump total at eta_c=0.70 = 34,227.8 × 30 J | Linear scale | Phase 1 | Total pumping input (COP denominator) |

**Key insight:** Re-deriving W_buoy, W_pump, or foil forces wastes execution budget and risks introducing inconsistency with the verified, locked Phase 1–3 values. Load from JSON files. Verify the loaded values match the expected Phase 1–3 figures (±0.1%) as a consistency gate, then proceed.

### Useful Intermediate Results

| Result | What It Gives You | Source | Conditions |
|---|---|---|---|
| COP_buoy_only at eta_c=0.70: 0.6032 | Baseline COP without any foil contribution; lower bound | Phase 1 JSON | eta_c = 0.70 specifically |
| (L/D)_min = cot(beta) = lambda | Minimum L/D for positive F_tan at given lambda | Phase 2 Plan 01 algebraic proof | Fixed-mount foil at that lambda |
| omega_design = 0.9132 rad/s (8.72 RPM) | Shaft angular velocity at lambda=0.9 design point | Phase 2 JSON | lambda=0.9, v_loop=3.7137 m/s |
| v_tan_design = 3.3423 m/s | Tangential velocity at design lambda | Phase 2 JSON | lambda=0.9, r_arm=3.66 m |
| N_ascending = N_descending = 12; N_total active = 24 | Vessel count for torque summation | Phase 2 geometry JSON | lambda=0.9 operating point |
| Spin-up time ~71 s | Phase 3 corot01; relevant for startup transient | Phase 3 corot01 JSON | Not relevant to steady-state balance |
| lambda_max = 1.2748 | Stall boundary | Phase 3/Phase 2 JSON | AoA-stall limited |

### Relevant Prior Work

| Result | What to Extract |
|---|---|
| PITFALL-C4 (tacking energy budget) | Chain coupling: ascending buoyancy drives descending drag via chain tension; tacking converts descending drag loss to useful torque but does not add energy. Both ascending and descending foil work must be bounded by total buoyancy input. Phase 4 must verify: W_foil_total ≤ W_buoy_total (approximately). |
| PITFALL-C5 (no external reservoir) | Phase 4 COP > 1.0 comes from energy already input by the compressor being redistributed efficiently by foil geometry. There is no violation of the First Law; the foils are not adding energy. Verify: explicitly identify where the extra energy (above buoyancy-return) comes from if COP > 1.0. Answer: it does not exist — the COP formulation counts W_buoy as recovered energy (the compressor energy that returns through buoyancy). The "extra" COP comes from the foil redirecting mechanical energy that would otherwise be lost to drag. |
| PITFALL-M4 (chain/bearing losses) | 5–15% of total power. At COP=2.0 gross, a 10% mechanical loss gives net COP = 1.8. At COP=1.5 gross, a 10% loss gives net COP = 1.35 < 1.5 — a NO-GO flip. This is the most consequential unquantified term. |

---

## Computational Tools

### Core Tools

| Tool | Version/Module | Purpose | Why Standard |
|---|---|---|---|
| Python 3.x | json, math | Load prior-phase JSON files, scalar calculations | Used throughout Phases 1–3; establishes pattern |
| numpy | Standard | Array operations for parametric sweep | Standard for 3D COP(L/D, eta_c, loss) array |
| scipy.optimize.fixed_point | Optional | Fixed-point iteration for v_loop_corrected | Convenience; can also implement manually in < 10 lines |
| matplotlib | Standard | COP contour plots, sensitivity visualization | Standard for feasibility study deliverables |

### Supporting Tools

| Tool | Purpose | When to Use |
|---|---|---|
| json.load() | Load phase1/2/3 summary JSON files | All tasks — do not hardcode prior values |
| numpy.meshgrid | Create (eta_c, L/D, loss_fraction) parameter space | Sensitivity sweep in Task 3 |
| matplotlib.contourf | COP contour plot over (L/D, eta_c) with loss_fraction as scenario | Deliverable visualization |

### Computational Feasibility

| Computation | Estimated Cost | Bottleneck | Mitigation |
|---|---|---|---|
| Fixed-point iteration for v_loop_corrected | < 1 ms; < 10 iterations | None | Implemented in < 10 lines of Python |
| 30-vessel energy balance assembly | < 1 ms | None | All inputs are scalars from JSON |
| 3D parametric sweep (30 eta_c × 20 L/D × 5 loss levels = 3,000 points) | < 1 s | None | numpy array operations |
| Contour plots | < 5 s | None | Standard matplotlib |

No additional package installation is required beyond the existing Python/numpy/scipy/matplotlib environment established in Phases 1–3.

---

## Validation Strategies

### Internal Consistency Checks

| Check | What It Validates | How to Perform | Expected Result |
|---|---|---|---|
| Lossless COP gate (eta_c=1, no drag, no losses) | First Law closure — energy accounting completeness | Set eta_c=1 (isothermal), zero all losses and drags; compute COP | COP = 1.000 ± 0.01%; if not, a term is double-counted or missing |
| COP_system in [0.603, 2.057] | Phase 4 COP is within the established bounds | Verify at all parameter combinations | Any COP outside this range is a sign error or accounting error |
| W_foil_total ≤ W_buoy_total (approximate bound) | Tacking does not add energy beyond the buoyancy budget | Sum W_foil_asc + W_foil_desc for all 24 active vessels and compare to 24 × W_buoy | If W_foil > W_buoy, PITFALL-C4 has been violated |
| Phase 1 anchor reproduction | JSON loading correctness | Recompute W_iso = P_atm × V_0 × ln(P_r) from loaded parameters | Must match 20,644.62 J to < 0.1% |
| Phase 2 COP anchor reproduction | JSON loading correctness | Compute (W_buoy + W_foil_asc + W_foil_desc) / W_pump using loaded values at lambda=1 | Must match 1.817 (lambda=1 COP_partial) or 2.057 (lambda=0.9 COP_partial) to < 0.1% |
| P_net_corot sign | Co-rotation is a net benefit (verified in Phase 3) | P_net_at_fss must be positive in Phase 4 assembly | P_net = 46,826 W; if negative, Phase 3 result has been misapplied |

### Known Limits and Benchmarks

| Limit | Parameter Regime | Known Result | Source |
|---|---|---|---|
| No hydrofoil, no co-rotation | L/D = 0 (or F_tan = 0) | COP_system = COP_buoy_only = W_buoy / W_pump = 0.6032 at eta_c=0.70 | Phase 1 |
| Perfect compressor (eta_c=1, isothermal) | eta_c = 1 | COP_buoy_only = 1.000 without foils; with foils, higher | Phase 1 First Law argument |
| Stall operating point (f=f_stall) | lambda_eff = lambda_max | COP_corot_at_fss = 0.603 (foil contribution nearly zero) | Phase 3 phase4_inputs |
| Design operating point (lambda=0.9, f=f_stall) | Nominal parameters | COP_partial = 2.057 (upper bound before F_vert correction) | Phase 2 |

### Numerical Validation

| Test | Method | Tolerance | Reference Value |
|---|---|---|---|
| W_pump reproduction | P_atm × V_0 × ln(P_r) × gamma/(gamma-1) / eta_c from loaded parameters | < 0.1% | 34,227.8 J at eta_c=0.70 |
| v_loop_corrected convergence | Fixed-point iteration termination condition | \|v_{n+1} − v_n\| / v_n < 1e-6 | Expected range: 3.7–4.5 m/s (F_vert adds to buoyancy → increases v_loop) |
| COP_system at lambda=1, f=0, eta_c=0.70, no losses | Direct calculation | COP in [1.8, 2.0] (from Phase 2 COP_partial_nominal = 1.817) | 1.817 |
| COP_system at lambda=0.9, f=0, eta_c=0.70, no losses | Should reproduce Phase 2 result | COP in [2.05, 2.07] | 2.057 |

### Red Flags During Computation

- If COP_system > 2.5 at any parameter combination, a term has been double-counted or W_pump is using the wrong formula (check: is eta_c in denominator correctly?).
- If COP_system > W_foil_total / W_pump (i.e., COP exceeds the foil-only contribution), something is wrong — the buoyancy work should not count as "output" above its "input" from the compressor.
- If v_loop_corrected < 2.5 m/s after F_vert correction, check the force balance direction — F_vert should add to (not subtract from) the upward forces on an ascending vessel.
- If the lossless COP gate returns anything other than 1.000 ± 0.01%, stop and trace the accounting before proceeding to lossy runs. The gate is a mandatory pass criterion.
- If P_net_corot enters as negative in the balance (after correct loading from Phase 3), check sign convention — Phase 3 delivers P_net as a positive number (benefit), not a loss.

---

## Common Pitfalls

### Pitfall 1: Using W_iso as Pump Energy (PITFALL-M1, Critical)

**What goes wrong:** Setting W_pump = W_iso in the COP denominator underestimates pump energy by 25–54% and makes COP appear larger than it is.
**Why it happens:** W_iso is the theoretical minimum (isothermal); real pump work W_pump = W_adia / eta_c is always larger.
**How to avoid:** Always use W_pump = W_adia / eta_c. W_iso appears only in the numerator as W_buoy (they are equal by the thermodynamic identity).
**Warning signs:** COP_buoy_only = W_buoy / W_pump approaching 1.0 at eta_c < 1.0 — this is impossible from Phase 1 analysis.
**Recovery:** Trace every COP formula and verify W_pump in the denominator is W_adia / eta_c.

### Pitfall 2: F_vert Coupling Not Resolved (Critical New Pitfall for Phase 4)

**What goes wrong:** Using v_loop = 3.7137 m/s (the Phase 1 uncoupled nominal value) for the final COP calculation, ignoring that F_vert adds ~1.15 × F_b_avg of upward force, which changes v_loop.
**Why it happens:** F_vert coupling was a known flag from Phase 2, but it requires an explicit correction step.
**How to avoid:** The Phase 4 Task 1 must solve the self-consistency equation: v_loop_corrected = f(F_b_avg + F_vert, C_D, A). Note that F_vert increases v_loop (upward pull assists buoyancy), so the correction makes COP higher than the Phase 2 upper bound — this is counterintuitive but correct. The Phase 2 upper bound label was conservative about F_vert's sign.
**Warning signs:** If the Phase 4 execution reports v_loop_corrected = 3.7137 m/s identically to Phase 1, the coupling was not actually run.
**Recovery:** Re-run fixed-point iteration with (F_b_avg + F_vert_N) as the net upward force. F_vert_N = F_vert_fraction × F_b_avg = 1.14994 × 1128.86 = 1298 N (approximately).

**Note on sign:** F_vert is the vertical component of hydrofoil lift. For an ascending vessel with a fixed-mount foil, the lift vector has a component opposing gravity (upward) and a component in the tangential direction (drives shaft). The upward component F_vert assists the vessel in rising faster, reducing drag dominance. This is why the Phase 2 COP = 2.057 is a conservative upper bound with respect to F_vert: the actual corrected v_loop is HIGHER than 3.7137 m/s, producing a slightly HIGHER COP. However, this conclusion must be verified by the iteration — if the fixed-mount AoA changes significantly at the higher v_loop, the foil forces change and the picture may differ.

### Pitfall 3: Mechanical Losses Omitted (PITFALL-M4, Verdict-Critical)

**What goes wrong:** Not subtracting chain/bearing/mechanical losses, making COP appear 5–15% higher than achievable.
**Why it happens:** These losses are not modeled analytically; they require a mechanical engineering estimate.
**How to avoid:** Include an explicit W_losses_mechanical = loss_fraction × W_pump_total term. Run three scenarios: optimistic (5%), nominal (10%), conservative (15%).
**Warning signs:** Phase 4 COP contours with no mechanical loss reduction compared to Phase 2/3 outputs.
**Recovery:** Apply fractional loss as a multiplicative reduction: COP_net = COP_gross × (1 − loss_fraction).

### Pitfall 4: N_vessel Counting Error

**What goes wrong:** Using N_total = 30 for the torque/foil work sum instead of N_ascending + N_descending = 24 (the 6 fill/release-transition vessels produce no torque).
**Why it happens:** The project specifies 30 vessels; the Phase 2 geometry JSON specifies 24 active for torque production.
**How to avoid:** Load N_ascending and N_descending from Phase 2 JSON; use N_active = 24 for energy output terms.
**Warning signs:** W_foil_total = W_foil_per_vessel × 30 (should be × 24); COP appears ~25% too high.

### Pitfall 5: Co-rotation Benefit Double-Counted

**What goes wrong:** Adding P_drag_saved and P_net_corot as separate terms — but P_net_corot = P_drag_saved − P_corot already. Using both double-counts the drag saving.
**Why it happens:** Phase 3 provides both the breakdown (P_drag_saved, P_corot) and the net result (P_net_at_fss). Only the net result enters Phase 4.
**How to avoid:** In the Phase 4 energy balance, use P_net_corot = P_net_at_fss_W = 46,826 W from phase3_summary_table.json. Do not also add P_drag_saved separately.

---

## Level of Rigor

**Required for this phase:** Controlled approximation with explicit uncertainty ranges; physicist's proof for the coupled velocity derivation.

**Justification:** This is a feasibility study, not a detailed design. The goal is to determine whether COP ≥ 1.5 under reasonable assumptions — not to compute COP to 4 significant figures. The dominant uncertainties (chain/bearing losses, C_f for Taylor-Couette, NACA L/D at operating Re) are all ±10–50%, so a 5%-precision COP answer is the appropriate target.

**What this means concretely:**

- The go/no-go verdict must be robust across the credible parameter range, not just at the nominal point.
- Mechanical loss fraction must be explicitly varied (3 scenarios minimum).
- eta_c must be varied across [0.65, 0.85] (from Phase 1 bounds).
- The COP range must be stated as [COP_pessimistic, COP_optimistic], not a single point.
- The F_vert correction iteration must converge, but does not need to iterate beyond 1e-6 relative tolerance.
- No new physics derivations are required — this phase is integration, not derivation.

---

## Self-Consistency Equation for v_loop (Key Mathematical Task)

This is the central mathematical task for Phase 4 and requires careful formulation.

### Force Balance with F_vert

For a steady-state ascending vessel:

```
F_net = F_buoy(z) + F_vert(v_loop) - F_drag_hull(v_loop) - F_chain = 0
```

Where:
- `F_buoy(z)` = rho_w × g × V_air(z) — varies with depth; use the average F_b_avg = W_iso / H = 1128.86 N
- `F_vert(v_loop)` = the upward component of hydrofoil lift ≈ F_vert_fraction × F_buoy_avg (Phase 2: fraction = 1.14994)
- `F_drag_hull(v_loop)` = 0.5 × rho_w × C_D × A_frontal × v_loop^2
- `F_chain` = chain tension from coupling to descending vessels (set to 0 for conservative v_loop upper bound; or use the Phase 1 nominal of F_chain ≈ 200 N as a moderate estimate)

### Self-consistency Loop Structure

Since F_vert depends on the foil forces, which depend on v_rel and thus on v_loop, the iteration structure is:

```
v_loop_0 = 3.7137  # Phase 1 starting point

while not converged:
    # At current v_loop:
    beta = arctan(v_loop / v_tan_design)  # velocity triangle angle
    v_rel = sqrt(v_loop^2 + v_tan_design^2)
    # Re-evaluate F_vert using foil force formula at (beta, v_rel):
    F_L = 0.5 * rho_w * C_L_3D * A_foil * v_rel^2
    F_vert_new = F_L * sin(beta)  # vertical component of lift
    # Update v_loop:
    v_loop_new = sqrt(2 * (F_b_avg + F_vert_new - F_chain) / (rho_w * C_D * A_frontal))
    if |v_loop_new - v_loop| / v_loop < 1e-6: break
    v_loop = v_loop_new
```

**Expected behavior:** Since F_vert is large (≈ 1300 N ≈ 1.15 × F_b_avg), the corrected v_loop will be significantly higher than 3.7137 m/s — possibly in the range 5–7 m/s (rough estimate: adding ~1.15 × 1128.86 N to the 1128.86 N buoyancy gives total upward force ≈ 2 × F_b_avg, implying v_loop_corrected ≈ sqrt(2) × v_loop_nominal ≈ 5.25 m/s). This is a substantial correction.

**Implications for the energy balance:** Higher v_loop means higher kinetic energy per vessel, higher v_rel, stronger foil forces, and potentially higher COP — but also higher hull drag power (scales as v_loop³). The net effect on COP must be computed numerically.

**Caution:** The fixed-mount foil at v_loop_corrected will have a different effective AoA (since beta = arctan(v_loop / v_tan) changes). If the mount angle is fixed at 38° (designed for AoA=7° at lambda=1), a higher v_loop at the same omega (or adjusted omega at the same lambda) means AoA changes. This must be tracked in the iteration to determine whether the foil remains below stall and whether the (L/D)_effective changes.

**Recommended simplification for feasibility:** For a first-pass feasibility verdict, hold lambda = 0.9 (adjust omega proportionally to v_loop_corrected) and let the velocity triangle re-evaluate naturally. This preserves the design AoA approximately. Then check: does the corrected v_loop place the vessel above stall? (lambda_eff at f=f_stall must still be ≤ lambda_max = 1.2748.)

---

## Sensitivity Analysis Structure

SYS-03 requires sensitivity analysis on L/D and co-rotation efficiency. The recommended structure:

### Primary Sweep Parameters

| Parameter | Nominal | Range | Rationale |
|---|---|---|---|
| eta_c | 0.70 | [0.65, 0.85] | Phase 1 established bounds |
| L/D effective (via AoA/NACA table) | ~15 (Phase 2 3D at AR=4) | [10, 25] | Phase 2 Phase 1 NACA range |
| Mechanical loss fraction | 0.10 | [0.05, 0.15] | PITFALL-M4; SUMMARY.md estimate |
| Co-rotation efficiency (via C_f uncertainty ±50%) | f_stall=0.294 | f in [0.15, 0.294] | Phase 3 uncertainty; actual f_ss may be less than f_stall |

### Output Surface

- Primary: COP_system(eta_c, L/D) at nominal loss fraction = 0.10 (2D contour plot)
- Secondary: COP_system at three loss scenarios (5%, 10%, 15%) as overlaid contours or table
- Tertiary: Go/no-go decision boundary (COP = 1.5 isoline on the primary contour)

### Verdict Logic

```
if COP_pessimistic (conservative eta_c, worst-case losses, lower co-rotation) >= 1.5:
    verdict = "GO (robust)"
elif COP_nominal >= 1.5 and COP_pessimistic < 1.5:
    verdict = "GO (conditional on eta_c >= X, loss fraction <= Y)"
else:
    verdict = "NO-GO"
```

The verdict statement must include the specific parameter combination that achieves COP = 1.5 and whether that combination is commercially achievable.

---

## State of the Art

This phase uses only established classical mechanics and thermodynamics. There are no modern method advances relevant to system energy balance integration for a buoyancy engine at this scale. The computational approach (Python + numpy parametric sweep) is standard and well-validated across Phases 1–3.

---

## Open Questions

1. **What is v_loop_corrected after F_vert coupling?**
   - What we know: F_vert/F_b_avg = 1.14994 (Phase 2); adds substantially to upward force
   - What's unclear: The exact iteration convergence point and the resulting AoA shift
   - Impact: Determines whether Phase 4 COP is above or below the Phase 2 upper bound of 2.057
   - Recommendation: Solve in Task 1; expected result v_loop_corrected ∈ [4.5, 5.5] m/s (rough estimate); verify via iteration

2. **What is the achievable mechanical loss fraction for this machine?**
   - What we know: Typical value 5–15% (PITFALLS.md M4; established mechanical engineering knowledge)
   - What's unclear: The specific chain/bearing configuration for 30 vessels on a rotating loop
   - Impact: 10% loss at COP=1.6 gives net COP=1.44 < 1.5 — verdict-critical at marginal COP
   - Recommendation: Use three scenarios (5%, 10%, 15%); clearly state which is required for GO verdict

3. **What is the actual achievable co-rotation fraction f_ss in the discrete-vessel geometry?**
   - What we know: f_ss_upper_bound = 0.635 (smooth cylinder); f_stall = 0.294 is the physical limit; actual f_ss in discrete-vessel geometry likely 0.3–0.5 × f_ss_upper_bound
   - What's unclear: The correction factor for discrete vessels
   - Impact: If f_ss_actual = 0.15 (half of f_stall), P_drag_saved drops significantly
   - Recommendation: Run sensitivity for f in [0.15, 0.294]; Phase 3 shows P_net > 0 throughout achievable domain, so this does not flip the verdict sign, but does affect the magnitude

---

## Alternative Approaches if Primary Fails

| If This Fails | Because Of | Switch To | Cost of Switching |
|---|---|---|---|
| Fixed-point iteration for v_loop_corrected | Non-convergence (unlikely given the linear force balance) | scipy.optimize.brentq bracketed root-finder on F_net(v_loop) = 0 | < 1 hour; trivial code change |
| Full coupled energy balance | F_vert correction makes v_loop too high, pushing lambda_eff above stall | Use conservative scenario: hold v_loop = 3.7137 m/s, treat F_vert as making the Phase 2 COP even more conservative | This gives a lower bound on COP; if lower bound > 1.5, verdict is GO regardless |
| Parametric COP sweep | COP never reaches 1.5 across the full parameter space | Deliver NO-GO verdict with explicit statement of what parameter combination would be needed (e.g., "COP ≥ 1.5 requires L/D ≥ 25 AND eta_c ≥ 0.85 AND loss fraction ≤ 5%") | Verdict changes from GO to NO-GO; report honestly |

**Decision criteria:** If the go/no-go verdict is NO-GO under the nominal parameters but GO under achievable optimistic parameters, the recommendation should include explicit guidance on which design changes or component specifications would flip the verdict.

---

## Caveats and Alternatives

**Self-critique responses:**

1. *What assumption might be wrong?* The F_vert sign/direction assumption. The above analysis assumes F_vert is upward (assisting the ascending vessel). If the foil geometry produces a net downward vertical force component for some operating conditions (e.g., if the AoA sign convention is reversed or the foil is mounted differently), F_vert would oppose buoyancy and reduce v_loop. Phase 2 explicitly computes F_vert_fraction = 1.14994 (positive, in Phase 1's sign convention = upward). Verify this from Phase 2 foil geometry before proceeding.

2. *What alternative approach was dismissed too quickly?* A fully time-resolved simulation (coupled ODE for all 30 vessels in the chain) would remove the quasi-steady approximation. However, at feasibility level, this adds complexity without changing the verdict, since the quasi-steady approximation introduces < 5% error (Phase 1 established). Appropriate to defer.

3. *What limitation is understated?* The mechanical loss fraction of 5–15% covers chain, bearings, and seal friction, but NOT losses from imperfect tack-flip mechanics. Each of the 30 vessels must flip its foil at top and bottom of the loop. During the flip transient, the vessel produces neither ascending nor descending torque and may experience increased drag. This is a potentially significant loss that is not included in the 5–15% estimate. Phase 4 should note this as an additional uncertainty and recommend it be characterized in prototype testing.

4. *Is there a simpler method?* Yes: bound analysis. If (COP_upper_bound − maximum credible losses) > 1.5, the verdict is GO without needing the full coupled solution. COP_upper_bound = 2.057 (Phase 2). Maximum credible losses: 15% mechanical + P_corot correction. 2.057 × (1 − 0.15) = 1.748 > 1.5. This simple bound argument might be sufficient for a conservative GO verdict, avoiding the coupled iteration entirely. Phase 4 should compute this bound first; if it gives GO, the coupled iteration is confirmatory rather than decisive.

---

## Sources

### Primary (HIGH confidence)

- Phase 1 phase1_summary_table.json — All Phase 1 locked values (W_pump, W_buoy, v_loop, F_b_avg, W_pump range); independently verified to 14/15 checks
- Phase 2 phase2_summary_table.json — All Phase 2 locked values (W_foil_asc/desc, F_vert, COP_partial, lambda design, omega design, N_ascending/descending); verified 4/4 contract targets
- Phase 3 phase3_summary_table.json — All Phase 3 locked values (P_corot, P_net_at_fss, COP_corot, f_stall, F_vert_flag_propagated); verified all 8 acceptance tests
- PITFALLS.md — Pitfalls C1–C7, M1–M5, m1–m5; HIGH confidence (derivable from first principles)
- METHODS.md §8 — System energy balance structure; HIGH confidence (algebraic assembly)
- SUMMARY.md §Approximation Landscape — All approximation validity ranges; MEDIUM-HIGH confidence

### Secondary (MEDIUM confidence)

- Schlichting & Gersten, "Boundary Layer Theory," 9th ed. — Taylor-Couette turbulent wall friction C_f; basis for P_corot estimate with ±50% uncertainty
- Hoerner, "Fluid-Dynamic Drag," 1965 — Hull C_D = 0.8–1.2 for blunt cylinders at Re ~ 10⁶; basis for F_chain = 0 conservative terminal velocity

### Tertiary (LOW confidence — training knowledge, verify if verdict is marginal)

- Mechanical loss fraction 5–15% for chain/belt drive systems — general mechanical engineering knowledge; no specific reference for this machine configuration; if verdict is marginal (COP in [1.4, 1.6]), this range should be narrowed by consulting manufacturer specifications for the chain and bearing system

---

## Metadata

**Confidence breakdown:**

- Mathematical framework (self-consistency equation, energy balance): HIGH — classical mechanics, established in Phases 1–3
- Standard approaches (fixed-point iteration, parametric sweep): HIGH — used and validated in Phases 1–3
- Computational tools (Python/numpy): HIGH — same stack as Phases 1–3
- Validation strategies (lossless gate, anchor reproduction): HIGH — derived from first principles
- Mechanical loss estimate: LOW — specific to this machine; range 5–15% is engineering knowledge only
- F_vert correction magnitude: MEDIUM — derived from Phase 2 output; the iteration result is not yet known

**Research date:** 2026-03-18
**Valid until:** Results from Phases 1–3 are locked; this research document is valid as long as those locked values are not revised. If Phase 2 AoA or foil geometry changes, the F_vert fraction changes and this document must be updated.
