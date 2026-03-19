# Phase 3: Co-rotation — Research

**Researched:** 2026-03-18
**Domain:** Rotating enclosed fluid mechanics / Taylor-Couette flow / turbulent wall drag / spin-up dynamics
**Confidence:** MEDIUM (mathematical framework HIGH for analytical model; equilibrium co-rotation fraction MEDIUM; discrete-vessel geometry correction LOW)

---

## Summary

Phase 3 must quantify whether water co-rotation inside the 24 ft cylinder helps or hurts the net system energy balance, and by how much. The physical picture is: the 24 orbiting vessels (12 ascending + 12 descending in steady state) continuously drag water in the tangential direction, imparting angular momentum to the enclosed water body. In steady state, this angular momentum input is exactly balanced by viscous dissipation at the outer tank wall. The resulting co-rotation fraction f (v_water = f × v_vessel tangentially) reduces horizontal drag on the vessels by a factor (1-f)², but requires continuous energy input to maintain against wall friction. If the drag savings exceed the maintenance cost, co-rotation provides a net benefit to COP.

The fluid mechanics of enclosed water spin-up by orbiting bodies is well-characterized in the literature (Maynes & Klewicki, J. Fluid Mech. 388, 1999; Greenspan & Howard, J. Fluid Mech. 17, 1963). The key results are: (1) spin-up to some fraction of the driver velocity occurs on a turbulent diffusion time scale τ ~ R²/(ν_T) where ν_T is the turbulent eddy viscosity; (2) the steady-state co-rotation fraction is determined by the balance of angular momentum input (vessel form drag × radius) against wall torque (turbulent skin friction × wall area × radius); (3) at the Hydrowheel's parameters (Re_vessel ~ 10⁵–10⁶), the process is fully turbulent and standard Prandtl-type correlations apply. The critical concern is whether f can be large enough to give meaningful drag reduction without driving λ_eff = λ/(1-f) above the stall limit (λ_max ≈ 1.27 from Phase 2).

The recommended approach is a two-part analytical model: (A) a steady-state angular momentum balance to compute f as a function of C_D_vessel, C_f_wall, and geometry; and (B) a swept net-benefit calculation P_drag_saved(f) − P_corot(f) as a function of f ∈ [0,1]. The model requires Python/numpy only — no CFD. The key result to report is the sign and magnitude of the net benefit, and whether the optimal f pushes λ_eff to stall.

**Primary recommendation:** Use the turbulent angular momentum balance model (steady-state torque equilibrium) to compute f_ss, then evaluate drag savings (1-f)² × F_D_baseline versus wall friction power P_corot = τ_w × 2πRL × ωR. Treat f as a parameter in [0, 1] and report the full net-benefit curve P_net(f).

---

## Active Anchor References

| Anchor / Artifact | Type | Why It Matters Here | Required Action | Where It Must Reappear |
| --- | --- | --- | --- | --- |
| `analysis/phase2/outputs/phase2_summary_table.json` | Prior artifact — Phase 2 outputs | Provides omega_design=0.913 rad/s, v_loop=3.7137 m/s, v_tan_design=3.342 m/s, F_D_baseline, COP_partial=2.057 at λ=0.9 (upper bound) | Load at start of Phase 3; do NOT hardcode Phase 2 values | COROT-01, COROT-02, COROT-03, all computations |
| `analysis/phase1/outputs/phase1_summary_table.json` | Prior artifact — Phase 1 outputs | Provides W_pump=34,228 J, W_buoy=20,645 J, v_vessel range | Load for system energy context | COROT-02 net benefit calculation |
| F_D_baseline (no co-rotation) | Derived quantity | Phase 2 baseline horizontal drag: F_D = ½ρ_w × C_D × A_frontal × v_vessel² ≈ 1300 N at v=3.71 m/s, C_D=1.0 | Compute from first principles; use as Phase 3 input | COROT-02 |
| Phase 2 COP_partial = 2.057 at λ=0.9 | Prior result (upper bound) | Phase 3 co-rotation reduces effective λ; Phase 3 must show how COP changes with f | Carry forward explicitly as the upper bound that co-rotation modifies | COROT-02, Phase 4 inputs |
| Greenspan & Howard (1963), J. Fluid Mech. 17, pp. 385–404 | Method reference — spin-up theory | Establishes the Ekman-layer spin-up time scale E^(-1/2) × Ω^(-1); defines framework for co-rotation analysis | Cite for spin-up time estimate | COROT-01 |
| Schlichting & Gersten, "Boundary Layer Theory," 9th ed. | Method reference — turbulent skin friction | C_f = 0.074 × Re^(-0.2) for turbulent flat plate (Prandtl 1/5-power law); applies to cylindrical tank wall | Cite for wall friction estimate | COROT-01, COROT-02 |

**Missing or weak anchors:** No published measurement directly gives f_ss for the specific geometry of discrete orbiting vessels (as opposed to a continuous rotating inner cylinder). The Taylor-Couette approximation treats the vessel chain as a smooth inner cylinder — this is the dominant source of uncertainty in Phase 3. The Maynes & Klewicki (1999) paper on spin-up by a single rotating bluff body is the closest literature analogue but covers a single body, not a chain of 24 bodies; its time-scale scaling is useful but its steady-state f values are geometry-specific and cannot be transferred directly.

---

## Conventions

| Choice | Convention | Alternatives | Source |
| --- | --- | --- | --- |
| Unit system | SI (m, kg, s, N, J, W, Pa, rad/s) | Imperial (design reference only) | Phase 1/2 lock |
| Fluid density | ρ_w = 998.2 kg/m³ (fresh water, 20°C) | Salt water 1025 kg/m³ | Phase 1 lock |
| Kinematic viscosity | ν_w = 1.004 × 10⁻⁶ m²/s (20°C) | Temperature-dependent table | Phase 2 lock |
| Co-rotation fraction | f ∈ [0, 1]: f = v_water_tangential / v_vessel_tangential | — | Project SUMMARY.md convention |
| Horizontal relative velocity | v_rel_h = v_vessel_h × (1 − f) = v_tan × (1 − f) | — | Project SUMMARY.md convention |
| Drag force formula | F_D = ½ × ρ_w × C_D × A_frontal × v_rel² | — | Phase 1/2 convention |
| Drag reduction factor | F_D_reduced / F_D_full = (1 − f)² [form drag scales as v_rel²] | — | Standard drag scaling |
| Effective tip-speed ratio | λ_eff = v_tan / v_rel_h = λ / (1 − f) | — | Phase 2 contract |
| Wall friction model | τ_w = ½ × ρ_w × C_f × (ω × R_tank)² | — | Schlichting §21 |
| Reynolds number for wall friction | Re_wall = ω × R_tank × H / ν_w (or Re_wall = v_wall × L / ν_w) | — | Schlichting convention |
| Maintenance power | P_corot = T_wall × ω = τ_w × A_wall × R_tank × ω | — | Torque × angular velocity |

**CRITICAL: All equations and results below use these conventions. The (1-f)² drag reduction assumes the dominant drag is form drag scaling as v_rel². If skin friction is significant, the reduction is also (1-f)² to leading order but the coefficient differs. The Hydrowheel vessels are bluff bodies (C_D ≈ 0.8–1.2) so form drag dominates and the (1-f)² formula is appropriate.**

---

## Mathematical Framework

### Key Equations and Starting Points

| Equation | Name/Description | Source | Role in This Phase |
| --- | --- | --- | --- |
| v_rel_h = v_tan × (1 − f) | Horizontal relative velocity under co-rotation | Project convention | Starting point for drag reduction |
| F_D_h = ½ ρ_w C_D A_frontal [v_tan(1-f)]² | Horizontal drag force with co-rotation | Standard drag law | COROT-02 drag reduction |
| F_D_reduction = F_D_full × [1 − (1-f)²] | Drag reduction from co-rotation | Standard drag scaling | COROT-02 net force saving |
| P_drag_saved = P_drag_full × [1 − (1-f)³] | Drag POWER saved by co-rotation (CUBIC — NOT force × v_tan) | Power = ½ρC_D A v_rel³; saving = P_full×[1-(1-f)³] (Pitfall C2 discipline) | COROT-02 power saving |
| τ_w = ½ ρ_w C_f (ω R_tank)² | Wall shear stress (turbulent flat plate) | Schlichting §21 (Prandtl 1/5-power law) | Wall friction model |
| C_f = 0.074 × Re_wall^(−0.2) | Turbulent skin friction (smooth wall) | Schlichting eq. 21.16; Prandtl 1/5-power law | Wall friction coefficient |
| T_wall = τ_w × (2π R_tank L_tank) × R_tank | Wall torque (shear force × moment arm) | Torque = Force × radius | Co-rotation maintenance torque |
| P_corot = T_wall × ω | Co-rotation maintenance power | Power = Torque × angular velocity | COROT-01 energy cost |
| P_net(f) = N_total × P_drag_saved(f) − P_corot(ω(f)) | Net benefit of co-rotation | Energy balance | COROT-02 key output |
| τ_spin_up ~ R_tank² / ν_T | Turbulent spin-up time scale | Maynes & Klewicki (1999) / Greenspan & Howard (1963) | COROT-01 achievability |
| λ_eff = λ_design / (1 − f) | Effective tip-speed ratio with co-rotation | Phase 2 COP formula | Stall limit check |
| COP_partial_corot = COP_partial_Phase2 × (1 − f)² | Approximate COP degradation with co-rotation (first-order, valid for f << 1) | Scaling from drag force → power ratio | COROT-02 COP adjustment |

**Note on the COP degradation formula:** The exact COP(f) requires re-running the Phase 2 force calculation at λ_eff(f) with the modified v_rel. The approximate formula COP_partial_corot ≈ COP_partial_Phase2 × (1-f)² holds only if the hydrofoil operates in the same F_tan regime. For f approaching the stall threshold (λ_eff → λ_max), the formula breaks down and the full Phase 2 sweep at λ_eff must be used.

### Required Techniques

| Technique | What It Does | Where Applied | Standard Reference |
| --- | --- | --- | --- |
| Steady-state torque balance | Equates vessel drag torque input to wall friction torque at equilibrium to solve for f_ss | COROT-01: steady-state f calculation | Fluid mechanics fundamentals |
| Turbulent skin friction correlation | Gives C_f as function of Re_wall; converts wall speed to wall shear stress | COROT-01, COROT-02 wall torque model | Schlichting & Gersten §21.2 |
| Drag scaling by relative velocity | Scales F_D ∝ v_rel² to quantify drag reduction as f increases | COROT-02 drag reduction curve | Standard bluff body drag |
| Parametric sweep over f ∈ [0,1] | Computes P_net(f) = P_drag_saved(f) − P_corot(f) and finds optimal f | COROT-02 net benefit sweep | numpy parameter sweep |
| Stall limit check | Verifies λ_eff = λ/(1-f) stays below λ_max ≈ 1.27 for all f in operating range | COROT-03 | Phase 2 stall analysis |
| Power balance (F × v) | Converts force savings to power savings correctly (avoids Pitfall C2) | All power calculations | Phase 2 power balance discipline |

### Approximation Schemes

| Approximation | Small Parameter | Regime of Validity | Error Estimate | Alternatives if Invalid |
| --- | --- | --- | --- | --- |
| Taylor-Couette smooth-cylinder model | Vessel diameter << tank circumference | Vessel d_vessel = 0.457 m << 2π × 3.66 m = 23 m ✓ | Factor of 2 on P_corot; treat as order-of-magnitude | Full CFD (not needed for feasibility) |
| Turbulent Prandtl 1/5-power law for C_f | Re_wall >> 5×10⁵ | Re_wall = ωR²/ν = (0.91 × 3.66²) / 1.004e-6 ~ 1.2×10⁷ >> 5×10⁵ ✓ | ±20% vs. fully rough wall | Blasius or Karman-Prandtl log law |
| Form drag dominates (C_D ≈ 1.0) | C_D_skin << C_D_form | True for blunt cylinders at Re ~ 10⁵; C_D_skin ~ 0.002 << C_D_form ~ 1.0 ✓ | < 1% error from ignoring skin friction on vessels | Full drag decomposition |
| Quasi-steady co-rotation (f = const during operations) | Spin-up time << operating time | τ_spinup ~ R²/ν_T ~ 10⁴/(10⁻²) ~ 10⁶ s for laminar; turbulent: τ ~ R/v ~ 4 s (very fast) | Likely valid for turbulent case; must verify | Transient model |
| (1-f)² drag reduction formula (form drag only) | Form drag dominates | Valid when C_D_form >> C_D_skin (true here) | Exact for pure form drag; < 1% error | Full drag decomposition |

---

## Standard Approaches

### Approach 1: Steady-State Angular Momentum Balance (RECOMMENDED)

**What:** Derive the steady-state co-rotation fraction f_ss by setting the angular momentum input rate (vessel drag torque) equal to the angular momentum dissipation rate (wall friction torque). This gives f_ss analytically as a function of C_D, C_f, geometry, and vessel number.

**Why standard:** This is the textbook approach for problems of this class — equivalent to finding the equilibrium rotation rate of a fluid driven by an internal body against viscous wall drag. It requires no CFD and gives an order-of-magnitude estimate with known accuracy (factor of 2 for turbulent wall friction).

**Track record:** The Greenspan-Howard (1963) framework and its turbulent extensions (Schlichting §21) have been validated against experiments for smooth cylindrical walls and are standard in oceanography, geophysical fluid dynamics, and stirred reactor design. The Maynes & Klewicki (1999) experiments confirm the turbulent time-scale scaling.

**Key steps:**

1. **Compute vessel drag torque per vessel:** T_vessel = F_D_h(f) × R_tank = ½ ρ_w C_D A_frontal [v_tan(1-f)]² × R_tank. This is the torque imparted to the water per vessel as it drags water tangentially.

2. **Compute total angular momentum input rate:** dL/dt_in = N_total × T_vessel × ω_loop (where ω_loop = v_tan/R_tank). Note: the vessels orbit, so the torque is applied at radius R_tank continuously.

3. **Compute wall friction torque:** T_wall = τ_w × 2π R_tank × L_tank × R_tank, where τ_w = ½ ρ_w C_f (ω × R_tank)², C_f = 0.074 Re_wall^(-0.2), Re_wall = ω R_tank² / ν_w.

4. **Set equilibrium (dL/dt_in = T_wall × ω) and solve for ω (or equivalently f = ω/ω_vessel):** This gives an implicit equation for f_ss that can be solved numerically with a fixed-point iteration or solved in a sweep.

5. **Compute P_corot(f) = T_wall(f) × ω(f):** This is the ongoing power cost of co-rotation maintenance.

6. **Compute P_drag_saved(f) = N_total × [F_D_full − F_D_reduced(f)] × v_tan:** This is the power saved by reduced form drag. NOTE: the saved power enters the system as reduced drag on ascending vessels, effectively reducing the drag loss term in the Phase 4 energy balance.

7. **Compute P_net(f) = P_drag_saved(f) − P_corot(f):** If P_net > 0 at the equilibrium f_ss, co-rotation provides a net benefit.

**Known difficulties at each step:**

- Step 1-2: The "torque imparted by vessels to water" depends on whether the vessel drag is the FULL drag (at v_vessel relative to the still-water reference) or the REDUCED drag (at v_rel = v_vessel − v_water). In steady state these must be self-consistent: the vessel drag that drives co-rotation IS the drag at v_rel = v_tan(1-f). This requires iterative solution.
- Step 3: The wall area is the inner surface of the 24 ft cylinder. With an open bottom, the effective wall area for friction may be approximately 2πR × H (side wall only, since bottom is open). This is a source of uncertainty.
- Step 4: The implicit equation may have multiple solutions or no positive solution (if the vessels cannot drive the water fast enough against wall friction). Check for solution existence before reporting.
- Step 6: The POWER saving is not just F × (reduction in force) — it requires careful tracking of which velocity the force acts through. Use P = F_D_reduced × v_rel_reduced (power lost to drag at reduced relative speed) vs. P = F_D_full × v_tan (power lost at full speed). The net power saved = P_drag_full − P_drag_reduced = ½ ρ_w C_D A_frontal v_tan³ × [1 − (1-f)³].

**Correction note — third-power formula:** When computing POWER (not force) saved by co-rotation, the correct formula is P_drag ∝ F_D × v_rel = ½ ρ_w C_D A v_rel² × v_rel ∝ v_rel³. Therefore:

- P_drag_full = ½ ρ_w C_D A v_tan³
- P_drag_reduced = ½ ρ_w C_D A [v_tan(1-f)]³ = P_drag_full × (1-f)³
- P_drag_saved = P_drag_full × [1 − (1-f)³]

The force saving is proportional to (1-f)² but the POWER saving is proportional to [1 − (1-f)³]. For f=0.3: force saving = 51%, power saving = 65.7%. Report both; use the power saving for energy balance purposes.

### Approach 2: Pure Parametric Sweep without Equilibrium Calculation (FALLBACK)

**What:** Skip the angular momentum balance derivation. Instead, treat f as a free parameter in [0,1] and compute P_net(f) = P_drag_saved(f) − P_corot(f) analytically for each f. Report the curve and identify: (a) the break-even f where P_net = 0, and (b) the regime where the stall limit is approached.

**When to switch:** If the angular momentum balance produces results with very high uncertainty (e.g., the predicted f_ss differs by more than a factor of 3 from the geometric mean of plausible values), it is more informative to report the full curve P_net(f) and bound the system behavior, rather than pin down f_ss with false precision.

**Tradeoffs:** Loses the predictive estimate of f_ss (what co-rotation actually achieves) but gains robustness. The project contract only requires quantifying COROT-01, COROT-02, and COROT-03 — the curve approach satisfies all three if f_ss is given as a range.

### Anti-Patterns to Avoid

- **Claiming co-rotation is "free":** P_corot must always appear as an explicit energy cost (PITFALL-C3). Even if f_ss is small, P_corot is nonzero.
  - _Example:_ Reporting "drag reduced by 30% at f=0.3" without subtracting the wall friction power that achieves f=0.3 inflates the net benefit.

- **Using force saving instead of power saving for energy balance:** The energy balance requires power terms (W/s), not force terms (N). Use P_drag_saved = F_D_full × v_tan × [1 − (1-f)³], not F_D_full × [1 − (1-f)²].
  - _Example:_ At f=0.5, force saving = 75% but power saving = 87.5%. Using 75% in a power balance gives wrong COP.

- **Ignoring λ_eff stall check:** Co-rotation reduces v_rel_h, which increases λ_eff = v_tan / v_rel_h. At f=0.3, λ_eff = 0.9/0.7 = 1.29 — just above the Phase 2 stall limit λ_max ≈ 1.27. This means the hydrofoil stalls before meaningful co-rotation can be achieved. This constraint may bound f to < 0.25.
  - _Example:_ Reporting "maximum net benefit at f=0.5" when f>0.28 drives the hydrofoil to stall is physically invalid.

- **Double-counting drag savings:** The horizontal drag that co-rotation reduces is the SAME drag that drives co-rotation in the first place. The energy balance must be self-consistent: the reduced drag is the post-co-rotation drag, not the sum of full drag (as vessel input) plus reduced drag (as co-rotation benefit).

---

## Existing Results to Leverage

### Established Results (DO NOT RE-DERIVE)

| Result | Exact Form | Source | How to Use |
| --- | --- | --- | --- |
| Turbulent flat plate C_f | C_f = 0.074 × Re^(−1/5) (valid 5×10⁵ < Re < 10⁷) | Schlichting & Gersten §21.2, eq. 21.16 | Direct use for wall friction; cite and plug in Re_wall |
| Drag force formula | F_D = ½ ρ C_D A v_rel² | Textbook (Schlichting, Hoerner) | Phase 3 baseline drag; already used in Phase 1/2 |
| Spin-up time Ekman-layer mechanism | τ_spinup ~ E^(-1/2) Ω^(-1) where E = ν/(ΩL²) | Greenspan & Howard (1963), §3 | Estimate whether co-rotation reaches steady state quickly; cite |
| Turbulent spin-up time scale | τ_turb ~ R²/ν_T (turbulent diffusion time); ν_T ~ κ u* L | Maynes & Klewicki (1999), J. Fluid Mech. 388 | For turbulent case: τ_turb << laminar τ; use to argue spin-up is fast |
| Isothermal compression identity | W_buoy = W_iso (Phase 1) | Phase 1 numerical result; SUMMARY.md | Carry forward as energy accounting anchor |
| Phase 2 COP_partial = 2.057 at λ=0.9 | Upper bound on system COP without F_vert coupling | Phase 2 Summary JSON | Starting value that co-rotation degrades |
| Phase 2 F_D_baseline | F_D = ½ × 998.2 × 1.0 × 0.164 × 3.7137² ≈ 1130 N per vessel (from Phase 1 terminal velocity calculation; C_D=1.0, A_frontal = π/4 × 0.457² = 0.164 m²) | Phase 1 terminal velocity derivation | Use as drag baseline for drag reduction calculation |

**Key insight:** The drag baseline, wall friction formula, and spin-up time scale are all textbook results requiring only plugging in Hydrowheel geometry. Do not re-derive them; cite the sources and apply.

### Useful Intermediate Results

| Result | What It Gives You | Source | Conditions |
| --- | --- | --- | --- |
| Re_wall at design ω = 0.913 rad/s | Re_wall = ω R² / ν = 0.913 × 3.66² / 1.004e-6 = 1.22×10⁷ | Derived (Phase 2 JSON + ν_w from Phase 2) | At design lambda=0.9, R_tank=3.66 m |
| C_f at Re_wall = 1.22×10⁷ | C_f = 0.074 × (1.22e7)^(-0.2) = 0.074 / 40.8 ≈ 0.00181 | Schlichting formula | Turbulent smooth wall; ~±30% uncertainty |
| τ_w at design | τ_w = ½ × 998.2 × 0.00181 × (0.913 × 3.66)² = ½ × 998.2 × 0.00181 × 11.17 ≈ 10.1 Pa | Derived | Smooth wall estimate |
| T_wall at design | T_wall = τ_w × 2π × 3.66 × 18.288 × 3.66 ≈ 10.1 × 421.1 × 3.66 ≈ 15,570 N·m | Derived | Side wall only (open bottom) |
| P_corot at design | P_corot = T_wall × ω = 15,570 × 0.913 ≈ 14,200 W | Derived | Smooth wall; upper estimate |
| F_D per vessel (full, no co-rotation) | ≈ 1130 N at v_tan = 3.71 m/s | Phase 1 terminal velocity calc | C_D=1.0, A=0.164 m² |
| P_drag per vessel (full) | P_drag = F_D × v_tan = 1130 × 3.71 ≈ 4,193 W | Derived | No co-rotation |
| P_drag total (24 vessels) | P_drag_total = 24 × 4,193 ≈ 100,600 W | Derived | All ascending + descending vessels |

**Important calibration check:** P_corot ≈ 14 kW (wall friction) vs P_drag_total ≈ 101 kW (vessel drag). The ratio is P_corot / P_drag_total ≈ 14%. This means: at full co-rotation (f → 1), the wall friction power approaches the total vessel drag power — the system spends nearly as much energy fighting the wall as it saves from reduced drag. This suggests that high co-rotation fractions are NOT self-evidently beneficial; the optimal f is well below 1.

**Second calibration check:** At the Phase 2 design λ=0.9, the stall limit is at λ_eff = λ_max ≈ 1.27. This means f is bounded by f_max = 1 − λ/λ_max = 1 − 0.9/1.27 = 0.29. Thus the maximum useful co-rotation fraction (before hydrofoil stall) is approximately f ≈ 0.29 — a key constraint that limits how much drag reduction is achievable.

### Relevant Prior Work

| Paper/Result | Authors | Year | Relevance | What to Extract |
| --- | --- | --- | --- | --- |
| Spin-up in a tank induced by a rotating bluff body | Maynes, Klewicki, McMurtry | 1999, J. Fluid Mech. 388, 49–68 | Direct analogue: bluff bodies spinning up water in an enclosed tank | Three temporal regimes; turbulent diffusion time scale; confirms turbulent spin-up is fast |
| On a time-dependent motion of a rotating fluid | Greenspan & Howard | 1963, J. Fluid Mech. 17, 385–404 | Classical spin-up theory; Ekman-layer driven mechanism | τ_spinup ~ E^(-1/2) Ω^(-1); linear regime basis |
| The Theory of Rotating Fluids | Greenspan | 1968, Cambridge University Press | Textbook treatment of rotating enclosed flows | Taylor-Couette and spin-up chapters |
| Boundary Layer Theory, 9th ed. | Schlichting & Gersten | 2017 | Wall friction C_f correlations; turbulent rotating cylinder drag | §21: turbulent skin friction; C_f = 0.074 Re^(-0.2) |
| Fluid-Dynamic Drag | Hoerner | 1965 | Form drag on blunt bodies including cylinders | C_D for open-bottomed cylinders at Re ~ 10⁵–10⁶ |

---

## Computational Tools

### Core Tools

| Tool | Version/Module | Purpose | Why Standard |
| --- | --- | --- | --- |
| Python 3.10+ | numpy, scipy | Parametric sweep of f, angular momentum balance, P_net(f) calculation | Already used in Phases 1 and 2; zero additional setup |
| numpy | linspace, vectorized ops | f sweep [0, 1] in 100+ steps; all power calculations | Consistent with Phase 2 scripts |
| matplotlib | pyplot | P_net(f) curve, stall limit overlay, COP(f) curve | Already used; output format matches prior phases |
| json | standard library | Load phase2_summary_table.json, phase1_summary_table.json | Phase 2 pattern established; mandatory |

### Supporting Tools

| Tool | Purpose | When to Use |
| --- | --- | --- |
| scipy.optimize.fsolve | Solve implicit angular momentum balance equation for f_ss | If fixed-point iteration diverges |
| scipy.integrate.quad | Integrate steady-state torque equations if closed-form is unavailable | Unlikely to be needed; analytical form expected |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
| --- | --- | --- |
| Analytical Taylor-Couette model | OpenFOAM CFD | CFD gives factor of 2–3 improvement in accuracy on P_corot; NOT justified for feasibility scope |
| Prandtl 1/5-power C_f | Karman-Prandtl logarithmic law | Log law is more accurate at high Re but requires iterative solve; 1/5-power is adequate here |
| Steady-state equilibrium | Transient spin-up model | Transient model reveals spin-up time but Phase 3 only needs steady state for energy balance |

### Computational Feasibility

| Computation | Estimated Cost | Bottleneck | Mitigation |
| --- | --- | --- | --- |
| f sweep (100 points) | < 1 ms | None | Vectorized numpy |
| Angular momentum balance iteration | < 10 iterations | None | Fixed-point iteration converges rapidly |
| COP(f) curve (Phase 2 sweep at each f) | < 1 s for 50 f × 48 λ points | None | Inner loop re-uses Phase 2 force formula |
| Plot generation | < 1 s | None | matplotlib standard |

**Installation / Setup:**

```bash
# All tools already present from Phase 1/2. No new packages required.
# Verify: python3 -c "import numpy, scipy, matplotlib, json; print('OK')"
```

---

## Validation Strategies

### Internal Consistency Checks

| Check | What It Validates | How to Perform | Expected Result |
| --- | --- | --- | --- |
| P_net(f=0) = 0 | At zero co-rotation, no drag saved and no wall power spent | Substitute f=0 into P_net formula | P_net = 0 exactly |
| P_net(f→1) sign check | At full co-rotation, wall friction dominates | Substitute f=1 into P_net | P_net < 0 (wall friction exceeds drag savings) |
| P_corot / P_drag_total ~ 14% order check | Wall friction power vs. vessel drag power | Compute P_corot / P_drag_total at design ω | Should be in range 5%–30%; alert if outside |
| λ_eff = λ/(1-f) stall limit | Co-rotation must not push foil to stall | Verify f_optimal < f_stall = 1 − λ/λ_max | f_stall ≈ 0.29 at λ=0.9 |
| Energy conservation: P_drag_saved + P_corot ≤ P_buoyancy | Co-rotation doesn't create energy | Check P_net against total buoyancy power | Must be true; if violated, model has error |
| Drag power formula: P_drag ∝ v_rel³ (not v_rel²) | Power scaling is cubic, not quadratic | Verify P_drag_saved = ½ ρ C_D A v³ [1-(1-f)³] | Check at f=0.5: factor = 1 - 0.5³ = 0.875 |

### Known Limits and Benchmarks

| Limit | Parameter Regime | Known Result | Source |
| --- | --- | --- | --- |
| f → 0 (no co-rotation) | v_water = 0 | Full drag F_D = ½ ρ C_D A v_tan²; P_corot = 0 | Trivial; validates formula at baseline |
| f → 1 (full co-rotation) | v_rel_h → 0 | F_D_h → 0; but P_corot → T_wall × ω_vessel | Net benefit is strongly negative: wall power ≈ 14 kW without any drag reduction benefit |
| Taylor-Couette laminar limit | Re_gap → 0 (viscous regime) | τ_wall = μ × ω × R / δ_gap → linear profile; NOT applicable here (turbulent) | Schlichting §6 | Use only to verify turbulent model gives LARGER P_corot than laminar |
| P_corot order of magnitude | At ω = 0.913 rad/s, R = 3.66 m | P_corot ~ 1–15 kW depending on C_f model | Project SUMMARY.md estimate: ~1.3 kW (lower bound); This research: ~14 kW (smooth wall). Discrepancy FLAG — see Pitfall 1. |

### Numerical Validation

| Test | Method | Tolerance | Reference Value |
| --- | --- | --- | --- |
| P_corot at ω = 0.913 rad/s | Compute T_wall × ω using C_f formula | Within factor of 2 of SUMMARY.md estimate (1.3 kW) | SUMMARY.md quotes ~1.3 kW; re-derived estimate ~14 kW — see Pitfall 1 for reconciliation |
| Phase 2 anchor | Load W_buoy and W_pump from JSON; check COP_buoy = 0.6032 ± 0.001 | < 0.1% | 0.6032 (Phase 2 anchor) |
| P_drag_total at baseline | 24 × ½ × 998.2 × 1.0 × 0.164 × v_tan² × v_tan | Within 5% of Phase 1 drag estimate | ~100 kW |

### Red Flags During Computation

- **If P_corot > P_drag_total:** The wall absorbs more power than all vessel drag combined — the model is unphysical. Check wall area formula; confirm area = 2π R H (not 2π R H + π R²).
- **If f_ss > 0.5:** For this geometry (bluff bodies driving a large tank), achieving f > 0.5 would require the vessels to be more efficient at driving the water than the wall is at resisting it. This is geometrically implausible given C_D_vessel ~ 1.0 and C_f_wall ~ 0.002. A value f_ss > 0.5 indicates a model error.
- **If P_net(f) is monotonically increasing:** This would imply more co-rotation is always better, contradicting the physical expectation that wall friction eventually dominates. Check the P_corot formula — it should scale as ω³ (∝ f³) while P_drag_saved scales as [1-(1-f)³] × P_drag_full.
- **If λ_eff < λ_design after co-rotation correction:** Co-rotation increases λ_eff above λ_design, not decreases it. A decrease would imply negative co-rotation (counter-rotation), which is unphysical here.

---

## Common Pitfalls

### Pitfall 1: P_corot Estimate Discrepancy Between SUMMARY.md and Derived Value

**What goes wrong:** The project SUMMARY.md quotes P_corot ~ 1.3 kW, but the Taylor-Couette smooth-wall formula gives ~14 kW at the design ω. This is a factor-of-10 discrepancy.

**Why it happens:** The SUMMARY.md estimate appears to use C_f ≈ 0.006 (from a rough estimate), while the Prandtl 1/5-power law gives C_f ≈ 0.00181 at Re_wall = 1.22×10⁷. However, 0.00181 vs 0.006 is only a factor of 3. The remaining factor ~3 discrepancy likely comes from the SUMMARY.md estimate using a smaller reference area or different velocity assumption. The Phase 3 calculation should re-derive P_corot from first principles and document the reconciliation. Do NOT silently carry forward the 1.3 kW figure.

**How to avoid:** Derive P_corot explicitly in Phase 3 using the full Taylor-Couette formula with the geometry values from Phase 2 JSON. Report the derived value and reconcile with the SUMMARY.md estimate. Flag if they differ by more than a factor of 2.

**Warning signs:** Any P_corot that is not derived explicitly from τ_w × A_wall × R_tank × ω.

**Recovery:** Re-derive P_corot step by step: τ_w → T_wall → P_corot = T_wall × ω. Check each factor's numerical value.

### Pitfall 2: Using (1-f)² for Power Saving Instead of [1-(1-f)³]

**What goes wrong:** The force saving from co-rotation is F_D_saved = F_D_full × [1-(1-f)²]. But the power saving is P_D_saved = P_D_full × [1-(1-f)³] because power = force × velocity, and the velocity also decreases with co-rotation. The phase researcher notes (Phase 2 PITFALL-C2) that L/D is a force ratio not a power ratio; the same discipline applies here.

**How to avoid:** Always use P = F × v for both terms. P_drag_full = ½ ρ C_D A v_tan³ and P_drag_reduced = ½ ρ C_D A [v_tan(1-f)]³. Power saving = P_drag_full × [1-(1-f)³].

**Warning signs:** The power saving percentage (for f=0.3) exceeds the force saving percentage — if you see force saving > power saving, you have an error.

### Pitfall 3: Ignoring the Stall Constraint (λ_eff Limit)

**What goes wrong:** Co-rotation reduces v_rel_h, which increases λ_eff = v_tan / v_rel_h. At λ=0.9 design, f > 0.29 pushes λ_eff > 1.27 (stall). The drag reduction formula (1-f)³ and the COP formula both break down past stall because the hydrofoil stops generating useful lift.

**How to avoid:** Add a stall check: compute f_stall = 1 − λ_design/λ_max for the current design lambda. Only report P_net(f) for f ∈ [0, f_stall]. For λ=0.9 and λ_max=1.27: f_stall = 1 − 0.9/1.27 = 0.291. This is the hard upper limit on co-rotation fraction.

**Warning signs:** Claiming COP benefit from co-rotation at f > 0.3 — this requires the hydrofoil to operate past its stall limit.

### Pitfall 4: PITFALL-C3 Recurrence — Co-rotation Maintenance Cost Omitted

**What goes wrong:** Reporting "co-rotation reduces drag by X%" without reporting the power cost of achieving that co-rotation fraction. This is documented as PITFALL-C3 in the project PITFALLS.md and is a contract-level forbidden proxy.

**How to avoid:** Every co-rotation result must be accompanied by: (a) the co-rotation fraction f, (b) the drag saving P_drag_saved(f), (c) the wall friction cost P_corot(f), and (d) the net benefit P_net(f) = P_drag_saved − P_corot. Never report (b) alone.

### Pitfall 5: Self-Consistency Failure in Angular Momentum Balance

**What goes wrong:** The vessel drag that drives co-rotation is the drag at v_rel = v_tan(1-f), NOT at v_rel = v_tan. But co-rotation is caused by vessel drag. The equilibrium equation must be solved self-consistently: the f that satisfies the angular momentum balance IS the f at which vessel drag equals wall friction torque.

**How to avoid:** Use fixed-point iteration: start with f=0 (full drag), compute the angular momentum input to the water, compute the resulting f from the wall friction torque, iterate until convergence. Do not use f=0 drag to compute the driving torque and then report a non-zero f without checking consistency.

---

## Level of Rigor

**Required for this phase:** Controlled approximation (order-of-magnitude / factor-of-2 accuracy for P_corot; factor-of-2 for f_ss).

**Justification:** The Taylor-Couette smooth-wall model is known to overestimate wall torque for rough or corrugated walls and to differ from discrete-vessel geometries by up to a factor of 2–3. Precision beyond factor-of-2 is not achievable without CFD or physical experiment. The Phase 3 output is a "net benefit flag" (P_net > 0, = 0, or < 0), not a precision measurement. Order-of-magnitude accuracy is sufficient for the Phase 4 go/no-go decision.

**What this means concretely:**

- P_corot reported as a range, not a single value: [P_corot_lower, P_corot_upper] based on C_f uncertainty ±50%.
- f_ss reported as a range, not a single value; flag if the range spans zero net benefit (P_net crosses zero within the uncertainty).
- Stall limit is a hard constraint (not uncertain): λ_eff < λ_max = 1.27 is computed from Phase 2 results.
- COP degradation with co-rotation reported as a curve COP(f), not a single number.

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
| --- | --- | --- | --- |
| Laminar Taylor-Couette theory (Stokes 1845) | Turbulent Taylor-Couette with Prandtl skin friction correlation | Taylor (1936), Schlichting (1960s) | At Re > 10⁵, turbulent model gives factor of 3-10 higher torque than laminar — use turbulent model always |
| Viscous spin-up (E^(-1/2) timescale) | Turbulent spin-up (much faster, τ ~ R/u*) | Greenspan & Howard (1963) + turbulent extensions | Turbulent spin-up is fast (seconds to minutes vs hours); co-rotation achieves steady state quickly |

**Superseded approaches to avoid:**

- **Laminar Couette velocity profile (linear):** Gives P_corot several orders of magnitude lower than turbulent value at this Re. Always use turbulent skin friction at Re_wall ~ 10⁷.

---

## Open Questions

1. **What is the actual steady-state co-rotation fraction f_ss for the discrete-vessel geometry?**
   - What we know: For a smooth inner cylinder, the Taylor-Couette formula gives f_ss analytically. For discrete orbiting bodies, the momentum coupling is different.
   - What's unclear: Whether the discrete-vessel geometry gives f_ss significantly different from the smooth-cylinder approximation.
   - Impact on this phase: Factor-of-2 uncertainty on f_ss, which translates to uncertainty in the net benefit magnitude.
   - Recommendation: Use the smooth-cylinder approximation as the best available estimate; label it as upper bound on f_ss (discrete vessels are less efficient at driving co-rotation than a smooth surface). Report as a range.

2. **Is the stall constraint at f ≈ 0.29 (λ=0.9) actually binding?**
   - What we know: Phase 2 establishes λ_max ≈ 1.27 (AoA ≈ 15° for NACA 0012). At f_stall = 0.291, λ_eff = 1.27.
   - What's unclear: Whether the mount angle (38°) can be adjusted in operation to extend the usable f range; whether the design can be switched to a lower nominal λ to give more co-rotation headroom.
   - Impact: If stall prevents f > 0.29, co-rotation benefit is capped at ~[1-(0.71)³] × P_drag_full ≈ 64% drag power reduction.
   - Recommendation: Report P_net at f = 0.29 (the stall-bounded maximum) as the key result; suggest that operating at lower λ (e.g., λ=0.7) would allow f up to 0.45.

3. **What is the open-bottom correction for wall area?**
   - What we know: The tank is open-bottomed; there is no floor boundary layer.
   - What's unclear: Whether the open bottom significantly reduces wall dissipation, or whether secondary flows (Ekman pumping) add additional dissipation.
   - Impact: Affects P_corot estimate by possibly ±30%.
   - Recommendation: Use side-wall area only (2π R H) as the lower bound; add an uncertainty factor of 1.5× for the upper bound.

---

## Alternative Approaches if Primary Fails

| If This Fails | Because Of | Switch To | Cost of Switching |
| --- | --- | --- | --- |
| Taylor-Couette smooth-wall model | Wall friction strongly geometry-dependent; result implausible | Pure parametric sweep with no f_ss prediction; just show P_net(f) curve and state "f_ss unknown" | Low — the parametric sweep is already part of Approach 1 Step 7 |
| Fixed-point iteration for f_ss | Multiple equilibria or no convergence | Bisection search on the angular momentum balance | Low — one extra function call |
| Closed-form solution | Implicit equations | Numerical root finding via scipy.optimize.brentq | Low |

**Decision criteria:** If f_ss > 0.5 from the angular momentum balance, the model has almost certainly overestimated the momentum coupling efficiency. Switch to the parametric sweep approach and report f_ss as "unknown, likely < 0.3 based on geometry."

---

## Caveats and Alternatives

**What assumption am I making that might be wrong?** The principal assumption is that the discrete vessel chain can be approximated as a smooth inner cylinder for the Taylor-Couette torque calculation. Actual vessel spacing = 2π × 3.66 / 10 ≈ 2.3 m between vessels on each arm, with vessel diameter 0.457 m. The "fill fraction" of the inner perimeter is 10 × 0.457 / (2π × 3.66) ≈ 20% per arm, or 60% total across 3 arms. This is not negligible. The smooth-cylinder approximation may overestimate the drag-coupling efficiency by a factor of 1.5–3.

**What alternative did I dismiss too quickly?** Direct CFD for this geometry would eliminate the factor-of-2 uncertainty in P_corot and f_ss. However, the project contract is a feasibility study, and the go/no-go decision does not require precision better than a factor of 2. CFD is deferred appropriately.

**What limitation am I understating?** The stall constraint (f < 0.29 at λ=0.9) is more binding than it might appear. With only 29% co-rotation headroom, the maximum power saving from co-rotation is [1-(0.71)³] ≈ 64% of the baseline drag power — but this is reduced by the wall friction cost and the fact that the drag power itself is only a fraction of the total energy balance. The net benefit to COP may be modest.

**Is there a simpler method?** The simplest useful result is: "co-rotation provides net benefit if and only if P_drag_saved(f_ss) > P_corot(f_ss)." This requires only two numbers (each with ±50% uncertainty) to answer the Phase 3 question. The full parametric sweep is informative but the sign of P_net at the estimated f_ss is the key result.

**Would a fluid mechanics specialist disagree?** A specialist might argue that the Hydrowheel geometry is closer to a stirred tank (impeller in a tank) than a Taylor-Couette system, and that stirred-tank power correlations (dimensionless power number N_p ~ 5 for turbulent mixing) are more appropriate. This is a valid alternative: N_p = P/(ρ N³ D⁵) where N is impeller rotation rate and D is impeller diameter. For Phase 3, the stirred-tank approach could be used as a cross-check on P_corot.

---

## Sources

### Primary (HIGH confidence)

- Schlichting, H. & Gersten, K., "Boundary Layer Theory," 9th ed., Springer, 2017 — §21.2: turbulent flat plate C_f = 0.074 Re^(-0.2); wall friction formula directly applicable
- Greenspan, H.P., "The Theory of Rotating Fluids," Cambridge University Press, 1968 — rotating enclosed flows; spin-up chapter; Taylor-Couette framework
- Abbott, I.H. & von Doenhoff, A.E., "Theory of Wing Sections," Dover, 1959 — Phase 2 anchor; C_L, C_D for NACA 0012; already validated in Phase 2

### Secondary (MEDIUM confidence)

- Greenspan, H.P. & Howard, L.N., "On a time-dependent motion of a rotating fluid," J. Fluid Mech. 17(3), 1963, pp. 385–404 — spin-up theory; Ekman layer timescale; classical result
- Maynes, R.D., Klewicki, J. & McMurtry, P., "Spin-up in a tank induced by a rotating bluff body," J. Fluid Mech. 388, 1999, pp. 49–68 — single bluff body in a tank; turbulent diffusion timescale; three-regime spin-up — closest published analogue to Hydrowheel geometry
- Hoerner, S.F., "Fluid-Dynamic Drag," 1965 — C_D for blunt cylinders (vessel hull drag baseline); already used in Phase 1

### Tertiary (LOW confidence — training knowledge only, verify before use)

- Mixing tank / stirred reactor power correlations (N_p ~ 5 for turbulent impeller in unbaffled tank) — potential cross-check method for P_corot; [TRAINING-KNOWLEDGE], verify against Perry's Chemical Engineers' Handbook before use

---

## Metadata

**Confidence breakdown:**

- Mathematical framework (drag reduction formula, wall friction formula): HIGH — standard fluid mechanics, well-established
- Steady-state co-rotation fraction f_ss: MEDIUM — smooth-cylinder Taylor-Couette applies; discrete-vessel correction introduces factor-of-2 uncertainty
- Computational tools: HIGH — identical to Phase 2 stack; already validated
- Validation strategies: HIGH — multiple internal consistency checks; known limiting cases well-defined
- P_corot absolute value: MEDIUM-LOW — factor of 10 discrepancy between SUMMARY.md prior estimate and derived value; must be reconciled in Phase 3

**Research date:** 2026-03-18
**Valid until:** Physics stable indefinitely; Schlichting C_f correlations standard for decades. Phase 3 input values (v_tan, ω) depend on Phase 2 JSON — valid as long as Phase 2 outputs are not revised.
