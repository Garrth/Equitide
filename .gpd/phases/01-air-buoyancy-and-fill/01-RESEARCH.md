# Phase 1: Air, Buoyancy & Fill — Research

**Researched:** 2026-03-16
**Domain:** Thermodynamics of gas compression, hydrostatic fluid mechanics, terminal velocity in viscous flow, compressed air fill system design
**Confidence:** HIGH for all thermodynamic and buoyancy calculations (first principles, confirmed analytically); MEDIUM for terminal velocity (empirical C_D range and chain coupling uncertainty); MEDIUM for fill feasibility (compressor market data not independently verified)

---

## Summary

Phase 1 establishes the fundamental energy accounting that all downstream phases depend on. Three interlocking results must be confirmed before Phase 2 can proceed: (1) the isothermal and adiabatic compression work bounds for the 60 ft depth system, (2) the variable-volume buoyancy work integral confirming the thermodynamic identity W_buoy = W_iso to within 1%, and (3) the self-consistent terminal velocity of the ascending vessel.

The thermodynamic identity is the most critical single result in the project. It proves that the buoyancy cycle, operating under ideal isothermal conditions, is exactly energy-neutral — compressor energy in equals buoyancy work out, with no surplus. This means all shaft output above break-even must come from hydrofoil work (Phase 2). The identity follows analytically from Boyle's law and the hydrostatic pressure profile; numerical verification via scipy.integrate.quad is a mandatory gate before Phase 2 calculations use any energy values.

Terminal velocity must be derived from the force balance at steady state, not assumed. The 3 m/s user estimate may be close, but drag power scales as v³ and a 20% velocity error causes 44% error in drag power — large enough to affect the Phase 4 go/no-go verdict. The fill feasibility calculation is straightforward once terminal velocity is known: fill window duration = (1/4 loop circumference) / v_vessel, and required flow rate = V_depth / t_fill_window.

**Primary recommendation:** Execute Phase 1 in strict sequence — compression work bounds first, buoyancy integral identity confirmation second (gate: < 1% error), terminal velocity third (gate: within 20% of 3 m/s), fill feasibility fourth. Do not proceed to Phase 2 until all three gates pass.

---

## Active Anchor References

| Anchor / Artifact | Type | Why It Matters Here | Required Action | Where It Must Reappear |
| --- | --- | --- | --- | --- |
| W_iso = 20,640 J (project scoping baseline) | Prior baseline | All Phase 1 energy values are cross-checked against this | Confirm numerically to < 0.1%; do not re-derive from scratch | Phase 1 buoyancy integral gate; Phase 4 COP denominator |
| W_adia = 24,040 J (project scoping baseline) | Prior baseline | Upper bound on pump energy; adiabatic/isothermal ratio 1.165 must reproduce | Confirm: 3.5 × P_atm × V_surface × (P_r^0.2857 - 1) = 24,040 J ± 10 J | Phase 1 pump energy calculation; Phase 4 real pump cost |
| CONVENTIONS.md (entire file) | Contract-critical anchor | All symbols, formulas, sign conventions, and numerical values for Phase 1 are locked here | Read and use verbatim — do not introduce alternative notation | All Phase 1 computations and output tables |
| P(z) = P_atm + rho_w × g × (H - z) with z = 0 at bottom | Convention anchor | Defines the pressure profile used in the buoyancy integral and Boyle's law volume | Use exactly this formula — do not use depth-from-surface coordinates without converting | All buoyancy integral code; all fill volume calculations |
| PITFALLS.md (C1, C6, C7, M1, M5) | Anti-pattern catalog | C1: constant-volume buoyancy error (74% overestimate); C6: jet recovery double-counting; C7: unvalidated velocity | Check against these explicitly in every Phase 1 deliverable | Phase 1 code review gates |
| Çengel & Boles, "Thermodynamics," 9th ed., Ch. 9 | Textbook (method source) | Compression work derivations; isentropic efficiency definition | Cite when presenting isothermal and adiabatic work formulas | THRM-01 deliverable |
| Hoerner, "Fluid-Dynamic Drag," 1965 | Handbook (empirical data) | C_D for blunt cylinders at Re ~ 10^5–10^6; needed for terminal velocity | Use C_D range 0.8–1.2 from this source | BUOY-03 terminal velocity calculation |

**Missing or weak anchors:** No CONTEXT.md exists for this phase (no locked user decisions beyond CONVENTIONS.md). The compressor η_c range 0.70–0.85 comes from PRIOR-WORK.md which is marked [TRAINING-KNOWLEDGE]; this should be treated as a sensitivity parameter rather than a fixed value. Actual compressor flow rate data for FILL-03 feasibility assessment requires market data not yet available in the project research files.

---

## Conventions

All conventions are already locked in CONVENTIONS.md. The table below summarizes only those directly used in Phase 1 calculations.

| Choice | Convention | Alternatives | Source |
| --- | --- | --- | --- |
| Vertical coordinate origin | z = 0 at tank bottom; z = H at surface | z = 0 at surface (depth positive downward) | CONVENTIONS.md §1 |
| Pressure profile | P(z) = P_atm + rho_w × g × (H - z) | P(d) = P_atm + rho_w × g × d where d = H - z | CONVENTIONS.md §1 |
| Unit system | SI throughout (Pa, m³, J, m/s) | Imperial for cross-checks only | CONVENTIONS.md §2 |
| Air thermodynamics | Ideal gas; γ = 1.4 | Real gas (negligible at ≤ 3 atm) | CONVENTIONS.md §3 |
| Compression work | Isothermal lower bound; adiabatic upper bound | Polytropic interpolation | CONVENTIONS.md §3 |
| Water density | ρ_w = 998.2 kg/m³ (fresh, 20°C) | Saltwater (not applicable per scope) | CONVENTIONS.md §3 |
| Gravitational acceleration | g = 9.807 m/s² | 9.81 m/s² (negligible difference) | CONVENTIONS.md §3 |
| Buoyancy integral convention | Variable-volume V(z) = V_surface × P_atm / P(z); never constant-volume | Constant-volume F_b × H (FORBIDDEN — 74% error) | CONVENTIONS.md §6 |

**CRITICAL: All equations below use z measured upward from tank bottom. P(z) decreases as z increases. V(z) increases as z increases. All integrals run from z = 0 to z = H = 18.288 m.**

---

## Mathematical Framework

### Key Equations and Starting Points

| Equation | Name / Description | Source | Role in Phase 1 |
| --- | --- | --- | --- |
| W_iso = P_atm × V_surface × ln(P_r) | Isothermal compression work | Çengel & Boles Ch. 9; Eq. derived from W = ∫P dV with PV = const | THRM-01 lower bound; numerically = 20,640 J |
| W_adia = [γ/(γ−1)] × P_atm × V_surface × [(P_r)^((γ−1)/γ) − 1] | Adiabatic (isentropic) compression work | Çengel & Boles Ch. 9; isentropic work for ideal gas | THRM-01 upper bound; numerically = 24,040 J |
| W_actual = W_adia / η_c | Real compressor work | Isentropic efficiency definition; η_c ∈ [0.70, 0.85] | THRM-01 realistic range: 28–34 kJ |
| P(z) = P_atm + ρ_w × g × (H − z) | Hydrostatic pressure at height z | Hydrostatics; CONVENTIONS.md §1 | Foundation for V(z) and F_b(z) |
| V(z) = V_surface × P_atm / P(z) | Air volume at height z (Boyle's law) | Ideal gas; isothermal assumption | BUOY-01 variable-volume buoyancy force |
| F_b(z) = ρ_w × g × V(z) | Buoyancy force at height z | Archimedes; variable air volume | BUOY-01 force profile over ascent |
| W_buoy = ∫₀ᴴ F_b(z) dz = P_atm × V_surface × ln(P_r) = W_iso | Buoyancy work integral = isothermal compression work | Thermodynamic identity (derivable from first principles) | BUOY-02 mandatory identity gate |
| F_drag(v) = ½ × ρ_w × C_D × A_frontal × v² | Hydrodynamic drag on ascending vessel | Morison/drag equation; C_D from Hoerner for blunt cylinder | BUOY-03 terminal velocity force balance |
| v_terminal: F_b = F_drag + F_chain (at v_terminal) | Terminal velocity force balance | Newton's second law at steady state | BUOY-03 self-consistent velocity |
| v_terminal = sqrt(2 × F_b_avg / (ρ_w × C_D × A_frontal)) | Fixed-point iteration starting point | Rearranged drag balance; F_chain = 0 initially | BUOY-03 fixed-point iteration |
| t_fill = (C_loop / 4) / v_vessel | Fill window duration | Geometry: 1/4 loop circumference | FILL-01 fill window |
| Q_required = V_depth / t_fill | Required volumetric flow rate at depth pressure | Mass conservation | FILL-02 flow rate requirement |
| C_loop = 2π × R_tank (approximately) | Loop circumference | Circular loop approximation | FILL-01 geometry; R_tank = 3.66 m |

### Required Techniques

| Technique | What It Does | Where Applied | Standard Reference |
| --- | --- | --- | --- |
| Isothermal compression derivation | W = ∫ P dV with PV = const → W = P₁V₁ ln(P₂/P₁) | THRM-01 | Çengel & Boles Ch. 9 |
| Isentropic compression derivation | PV^γ = const → W = [γ/(γ−1)] P₁V₁ [(P₂/P₁)^((γ-1)/γ) - 1] | THRM-01 | Çengel & Boles Ch. 9 |
| Boyle's law isothermal expansion | PV = const → V(z) = V_surface × P_atm / P(z) | BUOY-01, BUOY-02 | Ideal gas law |
| Definite integral (analytical) | ∫₀ᴴ ρ_w × g × V_surface × P_atm / P(z) dz = P_atm × V_surface × ln(P_r) | BUOY-02 analytical result | Standard calculus; integral of 1/P(z) |
| Numerical quadrature (scipy.quad) | Cross-verify buoyancy integral against analytical result to < 0.1% | BUOY-02 numerical gate | scipy.integrate.quad documentation |
| Fixed-point iteration | v_{n+1} = sqrt(2 F_b_avg / (ρ_w C_D A_frontal)); iterate to convergence | BUOY-03 terminal velocity | Standard root-finding |
| Reynolds number check | Re = ρ_w × v × d / μ_w to confirm drag regime | BUOY-03 drag coefficient selection | Fluid mechanics; Re ~ 10^5–10^6 at 3 m/s |
| Unit conversion cross-check | SI ↔ Imperial for fill volume (ft³ → m³) and flow rate (CFM → m³/s) | FILL-01, FILL-02, FILL-03 | CONVENTIONS.md §2 |

### Approximation Schemes

| Approximation | Small Parameter | Regime of Validity | Error Estimate | Alternatives if Invalid |
| --- | --- | --- | --- | --- |
| Ideal gas law for air at depth | (P − P_atm) / P_atm ≲ 2 at P_r = 2.770 | Pressures ≤ ~10 atm; temperature constant | Compressibility factor Z ≈ 1.000 ± 0.001 at 3 atm (negligible) | Van der Waals equation (unnecessary here) |
| Isothermal compression (lower bound) | Compression time >> thermal equilibration time | Slow compression with intercooling; quasi-static | Gives minimum work; real work is higher by adiabatic factor 1.165 | Adiabatic formula for upper bound |
| Adiabatic compression (upper bound) | Compression time << thermal equilibration time | Fast compression, no heat exchange | Gives 16.5% more work than isothermal at P_r = 2.770 | Polytropic formula with n < γ for intercooled multi-stage |
| Isothermal air expansion during ascent | Ascent time >> thermal equilibration of air in vessel | v ≲ 5 m/s; vessel not thermally insulated | Expansion deviates slightly from isothermal if vessel rises rapidly; error < 5% at 3 m/s | Adiabatic expansion — gives slightly lower buoyancy work (conservative) |
| Quasi-static hydrostatic pressure profile | Dynamic pressure << static pressure: ρ_w v² / 2 ≪ P_atm | v << 1500 m/s (speed of sound in water); always valid | Dynamic pressure at 3 m/s: 4,491 Pa << 101,325 Pa; error < 0.04% | Full Navier-Stokes (not needed) |
| Single-vessel terminal velocity (F_chain = 0) | Chain coupling is small relative to buoyancy force | First estimate only; chain tension depends on N_vessels | Conservative overestimate of v_terminal; actual velocity may be lower with chain load | Coupled multi-vessel ODE (unnecessary for feasibility) |
| Blunt cylinder C_D ≈ 0.8–1.2 (Hoerner) | Re ~ 10^5–10^6; L/d ratio ~ 2.7 (1.219 m / 0.457 m) | Re = ρ_w v d / μ_w ≈ (998.2)(3.0)(0.457) / 1.004e-6 ≈ 1.36 × 10^6 | ± 20% on C_D; propagates to ± 10% on v_terminal | CFD for precise C_D (not warranted for feasibility) |
| Circular loop circumference C = 2π R_tank | Loop path ≈ circular with R ≈ R_tank | Loop radius close to tank radius; loop shape is circular | ± 5% depending on actual chain path geometry | Elliptical loop path correction if geometry deviates |

---

## Standard Approaches

### Approach 1: Analytical + Numerical Hybrid (RECOMMENDED)

**What:** Derive all compression work and buoyancy work formulas analytically, then independently verify each with scipy.integrate.quad. Derive terminal velocity analytically (force balance at steady state) and solve numerically with fixed-point iteration. The analytical result is the reference; the numerical result is the cross-check.

**Why standard:** All Phase 1 calculations are well-posed with known closed-form solutions. Numerical cross-checks prevent coding errors (wrong sign convention, wrong pressure formula) from propagating undetected.

**Track record:** The isothermal compression formula and buoyancy work identity are textbook results, used in CAES (compressed air energy storage) literature and underwater glider design. No novel physics is involved.

**Key steps:**

1. Compute W_iso = P_atm × V_surface × ln(P_r): verify = 20,640 J ± 10 J against CONVENTIONS.md test value.
2. Compute W_adia = 3.5 × P_atm × V_surface × (P_r^0.2857 - 1): verify = 24,040 J ± 10 J. Confirm ratio W_adia / W_iso = 1.165 ± 0.003.
3. Compute W_actual range: W_adia / 0.85 = 28.3 kJ (optimistic) to W_adia / 0.70 = 34.3 kJ (conservative). Flag as sensitivity parameter for Phase 4.
4. Define P(z), V(z), F_b(z) using CONVENTIONS.md formulas verbatim. Verify P(0) = 280,500 Pa, P(H) = 101,325 Pa.
5. Evaluate W_buoy analytically: substitute P(z) into ∫F_b(z) dz; complete the integral via substitution u = P(z). Result: P_atm × V_surface × ln(P_r) = W_iso exactly.
6. Evaluate W_buoy numerically via scipy.quad(F_b, 0, H). Cross-check against analytical: |W_buoy_numerical - W_iso| / W_iso < 0.01.
7. Compute F_b_avg = W_buoy / H as the effective average buoyancy force for the terminal velocity calculation.
8. Run fixed-point iteration for v_terminal starting at v = 3.0 m/s. Compute Re at each iteration to confirm C_D regime. Converge to |Δv/v| < 10^-6 in < 10 iterations.
9. Compute fill window: C_loop = 2π × R_tank = 23.00 m; t_fill = (C_loop / 4) / v_terminal = 5.75 / v_terminal seconds (at v = 3.0 m/s: 1.917 s).
10. Compute required flow rate at depth: Q = V_depth / t_fill. Convert to CFM for comparison with commercial compressor specs.

**Known difficulties at each step:**

- Step 5: The analytical integral requires recognizing that ∫₀ᴴ 1/P(z) dz = [-1/(ρ_w g)] × ln(P(z))|₀ᴴ = [1/(ρ_w g)] × ln(P_bottom/P_atm). Substitute back to recover W_iso. This substitution is straightforward but must be done carefully to avoid factor errors.
- Step 6: scipy.quad on the interval [0, H] is smooth and monotone; no convergence issues expected. Use atol=1e-6, rtol=1e-8 as in COMPUTATIONAL.md.
- Step 8: F_b_avg depends on depth at which buoyancy is averaged. The average over the full ascent path is W_buoy / H. This is physically reasonable but note that F_b varies from F_b_min (at bottom, small air volume) to F_b_max (at surface, full air volume). The terminal velocity estimated from F_b_avg is an intermediate estimate; actual velocity varies along the path.
- Step 9: The fill window uses v_terminal from step 8. If v_terminal differs significantly from 3.0 m/s, the fill window changes and FILL-01 through FILL-03 must be recalculated with the updated velocity.

### Approach 2: Full Variable-Velocity Terminal Velocity ODE (FALLBACK — NOT RECOMMENDED FOR PHASE 1)

**What:** Solve the full ODE m dv/dt = F_b(z(t)) - F_drag(v) to get v(z) profile throughout the ascent.

**When to switch:** Only if the fixed-point iteration (Approach 1 step 8) gives a terminal velocity that differs from 3 m/s by more than a factor of 2 (suggesting the system never reaches terminal velocity within H = 18.288 m), or if the chain coupling force is found to be comparable to buoyancy.

**Tradeoffs:** The ODE approach gives the full velocity profile and acceleration distance, but requires estimating chain tension (coupled system), adding complexity. For Phase 1 feasibility, the terminal velocity estimate is sufficient.

### Anti-Patterns to Avoid

- **Using constant-volume buoyancy F_b × H:** The vessel volume is NOT constant during ascent — air expands from V_depth = 0.07228 m³ at the bottom to V_surface = 0.2002 m³ at the top. Using the surface volume throughout gives F_b × H = 1959 N × 18.288 m = 35,820 J, which is ~74% higher than the correct 20,640 J. This violates PITFALL-C1 and produces a buoyancy work value that exceeds the compression work — thermodynamically impossible for an ideal isothermal cycle.
  - _Example:_ The number 35.8 kJ as Phase 1 buoyancy work result is a diagnostic indicator of this error.

- **Listing jet recovery (THRM-03) as additional output beyond W_buoy:** The expanding air jet during ascent IS the physical mechanism of buoyancy work delivery. W_jet and W_buoy are two descriptions of the same phenomenon. Listing both as separate energy line items double-counts. Choose the buoyancy integral framework. The nozzle shape can affect efficiency of momentum transfer (changing C_D_hull), but cannot add energy beyond W_buoy. See PITFALL-C6.
  - _Example:_ An energy balance with line items "+ 20.6 kJ buoyancy" and "+ 5 kJ jet recovery" is incorrect.

- **Using v = 3.0 m/s in FILL-01 through FILL-03 without first confirming terminal velocity:** Fill window duration is proportional to 1/v_vessel. If the actual terminal velocity is 2.0 m/s rather than 3.0 m/s, the fill window is 50% longer (2.88 s instead of 1.92 s), which makes FILL-03 feasibility easier to satisfy. Using the assumed value introduces unnecessary uncertainty. Calculate terminal velocity first (step 8), then compute fill window using that result.

---

## Existing Results to Leverage

**This section is MANDATORY.** The following results are already established by the project scoping and project-level research. Do not re-derive them; cite and use.

### Established Results (DO NOT RE-DERIVE)

| Result | Exact Form | Source | How to Use |
| --- | --- | --- | --- |
| W_iso = 20,640 J | P_atm × V_surface × ln(P_r) = 101,325 × 0.2002 × ln(2.770) = 20,640 J | CONVENTIONS.md §9; project scoping | Starting value; verify to < 0.1% in Phase 1 THRM-01 |
| W_adia = 24,040 J | 3.5 × P_atm × V_surface × (2.770^0.2857 − 1) = 24,040 J | CONVENTIONS.md §9; PRIOR-WORK.md Result 2 | Starting value; verify to < 0.1% in Phase 1 THRM-01 |
| W_adia / W_iso = 1.165 | [3.5 × (P_r^0.2857 − 1)] / ln(P_r) at P_r = 2.770, γ = 1.4 | PRIOR-WORK.md Result 2; confirmed to 0.3% analytically | Adiabatic penalty factor; use directly |
| Constant-volume buoyancy error = 74% | (P_r − 1 − ln P_r) / ln P_r × 100% at P_r = 2.770 | METHODS.md §2; CONVENTIONS.md §6 | Anti-pattern sentinel: if computed W_buoy > 25 kJ, the constant-volume error has occurred |
| P(z) = P_atm + ρ_w × g × (H − z) | P(0) = 280,500 Pa; P(H) = 101,325 Pa | CONVENTIONS.md §1 | Use verbatim in all Phase 1 code |
| V_depth = 0.07228 m³ = V_surface / P_r | = 0.2002 / 2.770 | CONVENTIONS.md §6 | Fill target volume; use directly in FILL-01 |
| A_frontal = 0.1640 m² | π/4 × (0.457)² | CONVENTIONS.md §12 | Terminal velocity drag area; use directly |
| R_tank = 3.66 m; C_loop ≈ 23.00 m | 2π × 3.66 | CONVENTIONS.md §4 | Fill window geometry |

**Key insight:** The W_iso and W_adia values are confirmed to < 0.3% by direct calculation in project scoping (SUMMARY.md §Critical Claim Verification). Re-deriving them from scratch in Phase 1 code is appropriate as a confirmation step, but should take < 5 lines and should reproduce the scoping result exactly — not produce new values.

### Useful Intermediate Results

| Result | What It Gives You | Source | Conditions |
| --- | --- | --- | --- |
| F_b at z = 0 (bottom) = ρ_w × g × V_depth | Minimum buoyancy force during ascent: 998.2 × 9.807 × 0.07228 = 707 N | Derived from V_depth and F_b formula | Applies only at z = 0 |
| F_b at z = H (surface) = ρ_w × g × V_surface | Maximum buoyancy force during ascent: 998.2 × 9.807 × 0.2002 = 1959 N | Derived from V_surface and F_b formula | Applies only at z = H |
| F_b_avg = W_buoy / H | Average buoyancy force for terminal velocity estimate: 20,640 / 18.288 = 1129 N | Energy-weighted average over ascent | Representative for fixed-point iteration |
| Re at v = 3.0 m/s, d = 0.457 m | Re = 998.2 × 3.0 × 0.457 / 1.004e-6 = 1.36 × 10^6 | Reynolds number formula | C_D ≈ 0.8–1.2 applies (turbulent separation) |
| v_terminal naive (F_chain = 0) | = sqrt(2 × F_b_avg / (ρ_w × C_D × A_frontal)) = sqrt(2 × 1129 / (998.2 × 1.0 × 0.1640)) ≈ 3.71 m/s at C_D = 1.0 | Fixed-point formula; initial estimate | Overestimates true terminal velocity since F_chain > 0; useful as upper bound |
| t_fill at v = 3.0 m/s | = (2π × 3.66 / 4) / 3.0 = 5.75 / 3.0 = 1.917 s | Fill window geometry | Preliminary; update with confirmed terminal velocity |
| Q_required at v = 3.0 m/s | = V_depth / t_fill = 0.07228 / 1.917 = 0.0377 m³/s = 2.27 m³/min = 80.1 CFM at depth pressure (2.770 atm) | Fill flow rate formula | Preliminary; update with confirmed terminal velocity |

### Relevant Prior Work

| Paper / Result | Authors | Year | Relevance | What to Extract |
| --- | --- | --- | --- | --- |
| Pimm et al., Energy 41(1) | Pimm, Garvey, de Jong | 2012 | Underwater CAES; discusses buoyancy-compression thermodynamic equivalence in the same energy storage context | Cite as independent confirmation that W_buoy = W_iso identity holds in the CAES regime; validates that the identity is not a project-specific claim |
| Çengel & Boles, "Thermodynamics," 9th ed. | Çengel, Boles | — | Primary textbook for compression work derivations; isentropic efficiency definition | Ch. 9 equations for W_iso, W_adia; definition of η_c = W_adia / W_actual |
| Hoerner, "Fluid-Dynamic Drag," 1965 | Hoerner | 1965 | C_D tables for blunt cylinders at Re ~ 10^5–10^6 | Extract C_D range 0.8–1.2 for L/d ≈ 2.7 cylinder; use as input to terminal velocity calculation |

---

## Computational Tools

### Core Tools

| Tool | Version / Module | Purpose | Why Standard |
| --- | --- | --- | --- |
| Python | 3.10+ | All calculations | Universal scientific stack; no special installation |
| numpy | Any recent | Numerical arrays; vectorized math (log, exp, sqrt) | Standard for scientific Python |
| scipy.integrate.quad | scipy ≥ 1.7 | Numerical integration of F_b(z); cross-check vs. analytical W_iso | Adaptive Gauss-Kronrod quadrature; sub-millisecond on smooth integrands |
| matplotlib | Any recent | Plots: P(z), V(z), F_b(z) vs. z; v_terminal vs. C_D sweep | Standard; enables visual sanity checks |

### Supporting Tools

| Tool | Purpose | When to Use |
| --- | --- | --- |
| Python assert statements | Enforce numerical gates (|W_buoy - W_iso| < 1%; |W_adia/W_iso - 1.165| < 0.01) | After every major calculation; halt execution if gate fails |
| Unit conversion checks (numpy assertions) | Verify ft³ to m³, CFM to m³/s conversions | Before all fill feasibility calculations |
| Python print / logging | Document intermediate values with units | Throughout calculation for audit trail |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
| --- | --- | --- |
| scipy.integrate.quad | Manual Riemann sum | Riemann sum at 1000 points gives < 0.01% error but is more code; quad is simpler and more robust |
| Fixed-point iteration for v_terminal | scipy.optimize.fsolve on F_net(v) = 0 | fsolve is more general but overkill; fixed-point converges in < 10 iterations for this well-conditioned problem |
| Python for all calculations | Spreadsheet (Excel) | Spreadsheet is acceptable for spot-checks but cannot enforce numerical gates automatically; Python preferred for reproducibility |

### Computational Feasibility

| Computation | Estimated Cost | Bottleneck | Mitigation |
| --- | --- | --- | --- |
| W_iso, W_adia (closed form) | < 1 ms | None | Trivial |
| scipy.quad buoyancy integral | < 10 ms | None; smooth integrand | Use atol=1e-6, rtol=1e-8 |
| Fixed-point terminal velocity iteration | < 1 ms; < 10 iterations | None | — |
| Fill window and flow rate calculations | < 1 ms | None | — |
| Full Phase 1 computation | < 1 s total | None | — |

**Installation / Setup:**
```bash
pip install numpy scipy matplotlib
# All tools are standard scientific Python; no specialized packages required
```

---

## Validation Strategies

### Internal Consistency Checks

| Check | What It Validates | How to Perform | Expected Result |
| --- | --- | --- | --- |
| W_iso gate | Compression formula correct and numerical values loaded correctly | Compute 101325 × 0.2002 × ln(2.770); compare to 20,640 J | |W_iso - 20640| < 10 J (< 0.05%) |
| W_adia gate | Adiabatic formula correct | Compute 3.5 × 101325 × 0.2002 × (2.770^0.2857 - 1); compare to 24,040 J | |W_adia - 24040| < 20 J (< 0.1%) |
| Adiabatic/isothermal ratio | Ratio formula correct | W_adia / W_iso; compare to 1.165 | |ratio - 1.165| < 0.003 |
| W_buoy numerical = W_iso (MANDATORY GATE) | Buoyancy integral coded correctly; thermodynamic identity holds numerically | scipy.quad on F_b(z) from 0 to H; compare to W_iso | |W_buoy - W_iso| / W_iso < 0.01 (1%) |
| P(z) endpoint test | Pressure profile formula and constants correct | Evaluate P(0) and P(H) | P(0) = 280,500 Pa ± 100 Pa; P(H) = 101,325 Pa exactly |
| V(z) endpoint test | Boyle's law applied correctly | Evaluate V(0) = V_surface × P_atm / P(0) and V(H) = V_surface | V(0) = 0.07228 m³ ± 0.0001 m³; V(H) = 0.2002 m³ exactly |
| F_b endpoint test | Buoyancy force at limits | F_b(0) = ρ_w × g × V(0); F_b(H) = ρ_w × g × V_surface | F_b(0) ≈ 707 N; F_b(H) ≈ 1959 N |
| Constant-volume buoyancy sentinel | Catches C1 error if it occurs | Compute F_b_surface × H; confirm it is ~74% greater than W_buoy | F_b(H) × H = 1959 × 18.288 = 35,827 J ≈ 1.736 × W_iso |
| Terminal velocity Re check | Confirms C_D regime assumption is self-consistent | Re = ρ_w × v_terminal × d / μ_w; confirm Re ∈ [10^5, 10^7] | Re ~ 10^6 expected; if Re < 10^4, different C_D regime |

### Known Limits and Benchmarks

| Limit | Parameter Regime | Known Result | Source |
| --- | --- | --- | --- |
| P_r → 1 (shallow depth) | H → 0 | W_iso → 0; W_adia → 0; ratio W_adia/W_iso → 1.0 | Taylor expansion: [(P_r^0.2857 - 1)×3.5] / ln(P_r) → 1 as P_r → 1 |
| P_r → ∞ (very deep) | H → ∞ | W_adia / W_iso → ∞; adiabatic penalty becomes dominant | Standard result from thermodynamics |
| C_D → ∞ (very high drag) | Very large vessel | v_terminal → 0; fill window → infinity | Physical limit: buoyancy cannot overcome drag |
| F_chain → 0 | Isolated vessel, no chain | v_terminal = sqrt(2 F_b_avg / (ρ_w C_D A_frontal)) ≈ 3.7 m/s at C_D = 1 | Upper bound on terminal velocity |
| Constant-volume check (should fail) | Using F_b × H | Should give 35.8 kJ, not 20.6 kJ | This is the C1 anti-pattern; use as detector |

### Numerical Validation

| Test | Method | Tolerance | Reference Value |
| --- | --- | --- | --- |
| W_iso numerical | scipy.quad on P_atm × P_atm × V_surface / P(z) integrated from 0 to H with a substitution check | < 0.1% of 20,640 J | 20,640 J |
| W_buoy vs W_iso identity | scipy.quad result vs. analytical ln formula | < 1% (mandatory gate) | 20,640 J |
| v_terminal fixed-point convergence | Δv/v between successive iterations | < 10^-6 after ≤ 10 iterations | ~3.5 m/s at C_D = 1.0, F_chain = 0 (upper bound estimate) |
| Fill window geometry | C_loop / 4 / v_terminal | ± 10% from any loop path deviation from circular | ~1.9 s at 3 m/s |
| Required flow rate units | Q in m³/s, CFM, and L/min all consistent | Conversion agreement < 0.1% | ~0.038 m³/s = 80 CFM at depth pressure |

### Red Flags During Computation

- If W_buoy > 25 kJ, the constant-volume error (PITFALL-C1) has occurred. W_buoy must equal W_iso ≈ 20.6 kJ, not F_b × H ≈ 35.8 kJ.
- If W_buoy > W_iso by more than 1%, the pressure profile or volume formula is wrong. The identity is exact for ideal isothermal conditions.
- If v_terminal > 10 m/s, the drag force is likely underestimated (wrong A_frontal or C_D too low). Check A_frontal = 0.1640 m² and C_D ≥ 0.8.
- If v_terminal < 1 m/s, drag is likely overestimated, or chain tension was accidentally included with a large value. Recheck the force balance terms.
- If Q_required > 500 CFM, re-examine whether the fill window geometry is correct. At standard compressor sizes (< 200 CFM), extremely high flow rates signal a geometric error.
- Any NaN or infinity in scipy.quad output signals a division by zero in P(z) — check that H - z is never negative (z must be in [0, H]).

---

## Common Pitfalls

### Pitfall 1: Constant-Volume Buoyancy Integral (PITFALL-C1)

**What goes wrong:** Using W_buoy = F_b × H with F_b computed at the surface volume V_surface. This gives W_buoy = 1959 N × 18.288 m = 35,820 J instead of the correct 20,640 J — a 74% overestimate.

**Why it happens:** Intuitive shortcut: "the vessel is full of air, so F_b = ρ_w g V_surface throughout." This ignores that the vessel is open at the bottom — at depth, it contains only V_depth = 0.07228 m³ of air, not V_surface.

**How to avoid:** Always use V(z) = V_surface × P_atm / P(z) in the buoyancy force. Enforce the numerical gate: if W_buoy > 22,000 J, halt and debug the integral.

**Warning signs:** W_buoy > 25 kJ; W_buoy ≈ 35–36 kJ is the specific constant-volume result.

**Recovery:** Replace F_b(z) = ρ_w × g × V_surface with F_b(z) = ρ_w × g × V_surface × P_atm / P(z) and rerun the integral.

---

### Pitfall 2: Double-Counting Jet Recovery (PITFALL-C6)

**What goes wrong:** Listing W_jet (expanding air jet thrust) as a separate energy term in addition to W_buoy. These are not additive — they are two frameworks for the same physical phenomenon.

**Why it happens:** THRM-03 asks to "estimate jet propulsion energy recovery." This is legitimate as a check of the mechanism, but must not result in two separate line items being summed.

**How to avoid:** THRM-03 deliverable is a confirmation that the jet work ≈ W_buoy, not a new energy source. In the energy balance, use only W_buoy from the integral. If the nozzle shape is improved, its effect is captured through a reduction in hull drag C_D, not as an additive jet energy term.

**Warning signs:** Energy balance lists both "20.6 kJ buoyancy" and "X kJ jet recovery" where X > 0 is significant. If both appear and sum to more than W_iso, an error has occurred.

**Recovery:** Remove the jet recovery line item. Note that W_jet is the mechanism; W_buoy is the thermodynamic accounting.

---

### Pitfall 3: Unconfirmed Vessel Velocity (PITFALL-C7)

**What goes wrong:** Using v = 3.0 m/s throughout Phase 1 calculations, including fill window and flow rate, without deriving v_terminal from the force balance.

**Why it happens:** 3.0 m/s is given as the project parameter. The calculation works algebraically with any v. But drag scales as v² and power as v³, so the fill window, cycle time, and all Phase 2 inputs are sensitive to this assumption.

**How to avoid:** Complete step 8 (terminal velocity fixed-point iteration) before steps 9–10 (fill window and flow rate). If v_terminal differs from 3.0 m/s by more than 20%, update the fill window and report the discrepancy explicitly.

**Warning signs:** Phase 1 report uses v = 3.0 m/s for fill window without showing a terminal velocity calculation.

**Recovery:** Run fixed-point iteration; update v_vessel in CONVENTIONS.md if a significantly different value is found; propagate to fill window and FILL-01–FILL-03.

---

### Pitfall 4: Real Pump Efficiency Omitted from THRM-01 (PITFALL-M1)

**What goes wrong:** Reporting only W_iso = 20.6 kJ as the pump energy, ignoring that the real compressor does W_actual = W_adia / η_c ∈ [28.3, 34.3] kJ. This underestimates the energy input to the system by 37–66% compared to realistic conditions.

**Why it happens:** The isothermal formula is the "correct" thermodynamic work integral and is often cited without noting that no real compressor achieves it.

**How to avoid:** THRM-01 must report three values: W_iso (theoretical minimum), W_adia (adiabatic bound), and W_actual range (W_adia / η_c for η_c = 0.70 to 0.85). Flag that Phase 4 must use W_actual as the pump energy denominator in COP.

**Warning signs:** THRM-01 output gives a single pump energy value of 20.6 kJ and treats it as the actual pumping cost.

**Recovery:** Add the η_c correction column to the output. Use W_actual = 28–34 kJ as the Phase 4 input, not W_iso = 20.6 kJ.

---

### Pitfall 5: Neglecting Compressor Inlet Losses (PITFALL-M5)

**What goes wrong:** Using W_actual = W_adia / η_c as the total pump energy without adding pipe friction and inlet losses for drawing air from surface and delivering it to 60 ft depth. These add 10–20% to pump energy.

**Why it happens:** The isentropic efficiency formula accounts for imperfect compression of the air within the compressor, but not for pressure drop in the delivery line.

**How to avoid:** In THRM-01, note the 10–20% additional loss estimate. In the Phase 4 balance, apply a pipe friction factor of 1.10–1.20 × W_actual. For Phase 1 feasibility, document this as an uncertainty band.

**Warning signs:** Pump energy calculation uses only the thermodynamic work formula with no mention of delivery line losses.

**Recovery:** Multiply W_actual by a delivery factor of 1.10–1.20 and carry as an uncertainty range.

---

## Level of Rigor

**Required for this phase:** Controlled analytical derivation with numerical cross-checks. Physicist's proof level — rigorous derivations from well-established first principles (ideal gas law, hydrostatics, Archimedes), verified by independent numerical integration. No formal proof of convergence rates required.

**Justification:** Phase 1 involves only first-principles results (thermodynamic identities, hydrostatic pressure, terminal velocity from drag balance). The physics is not novel or disputed. The computational complexity is low (scipy.quad, fixed-point iteration). The rigor requirement is accuracy and self-consistency, not formal proof.

**What this means concretely:**

- The W_buoy = W_iso identity must be confirmed numerically to < 1%; algebraic demonstration alone is not sufficient because coding errors are possible.
- The terminal velocity calculation must use a specific numerical value of C_D from a reputable empirical source (Hoerner), not an assumed round number.
- All intermediate values must be reported with units. Unit confusion between ft³ and m³, or between absolute and gauge pressure, is a real risk in this mixed-units project.
- The fill feasibility assessment (FILL-03) requires a comparison against actual compressor specifications; "feasible" cannot be declared based on flow rate alone without naming specific equipment.

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
| --- | --- | --- | --- |
| Buoyancy work as F_b × H (constant volume) | Variable-volume integral W_buoy = P_atm V ln(P_r) | Established in classical thermodynamics; common error persists | 74% overestimate if old approach used |
| Multi-stage compression with intercooling (for high P_r) | Single-stage acceptable at P_r = 2.770 | Single-stage efficiency adequate at low P_r | Single-stage η_c = 0.70–0.85 is acceptable here; intercooling beneficial but not required |
| Empirical drag coefficients from wind tunnel (air) | C_D tables scaled to Re; applicable in water with Reynolds number matching | Established practice | C_D for water flow at Re ~ 10^6 is same as air at same Re for blunt bodies |

**Superseded approaches to avoid:**

- Constant-volume buoyancy work (F_b × H): superseded by variable-volume integral; still sometimes used incorrectly because it is simpler. Detection: result ~74% too high.
- Gauge pressure in Boyle's law: using gauge pressure P_gauge = P(z) - P_atm instead of absolute pressure in V(z) = V_surface × P_atm / P(z). At depth, P_gauge = 179,175 Pa; using it gives wrong V(z) and wrong F_b(z). Always use absolute pressure.

---

## Open Questions

1. **What is the self-consistent terminal velocity?**
   - What we know: The naive fixed-point estimate gives ~3.7 m/s at C_D = 1.0, F_chain = 0 (upper bound). Chain coupling and higher C_D values would reduce this.
   - What's unclear: Chain tension depends on N_vessels and the weight distribution of descending vessels — a coupled system not fully specified in Phase 1.
   - Impact on this phase: Terminal velocity directly sets the fill window duration and required flow rate (FILL-01, FILL-02). It gates Phase 2 hydrofoil calculations.
   - Recommendation: Compute terminal velocity with F_chain = 0 first (upper bound). Report a sensitivity range: v_terminal for C_D ∈ {0.8, 1.0, 1.2} and F_chain ∈ {0, 500, 1000} N. Flag for Phase 2 if the range is wider than ± 20% around 3 m/s.

2. **Is the fill window geometry accurately characterized by 1/4 loop circumference?**
   - What we know: The requirement states 1/4 loop circumference. With R_tank = 3.66 m, C_loop = 23.00 m, so the fill arc = 5.75 m.
   - What's unclear: The actual loop path may not be circular or may not use R_tank as its radius. The vessel chain follows a path inside the 24 ft diameter tank; the exact radius depends on structural design.
   - Impact on this phase: A 10% uncertainty in loop radius propagates directly to a 10% uncertainty in fill window.
   - Recommendation: Use R_tank = 3.66 m as the conservative (maximum) loop radius for the shortest fill window. Flag that actual loop radius could be smaller, giving a longer fill window (easier to satisfy).

3. **What compressor specifications are feasible for FILL-03?**
   - What we know: Required flow rate is approximately 80 CFM at 2.770 atm (40.7 psi absolute = 26.0 psi gauge). This is within the range of industrial rotary screw or reciprocating compressors.
   - What's unclear: Whether 80 CFM at 26 psi gauge is available in a single unit at reasonable cost and size for a prototype.
   - Impact on this phase: FILL-03 is a feasibility gate — if the required flow rate is not available, the 3 m/s vessel velocity is not compatible with the fill constraint.
   - Recommendation: Report Q_required in CFM at depth pressure. Note that standard industrial compressors (e.g., Ingersoll Rand, Atlas Copco) in the 50–100 CFM range at 100–200 psi gauge are commercially available and well within the 40.7 psi absolute requirement. The fill constraint is likely not a show-stopper.

---

## Alternative Approaches if Primary Fails

| If This Fails | Because Of | Switch To | Cost of Switching |
| --- | --- | --- | --- |
| Fixed-point terminal velocity converges outside ± 20% of 3 m/s | Chain tension is much larger than buoyancy force | Coupled multi-vessel ODE for velocity profile | 1–2 additional tasks in Phase 1; requires chain tension model |
| W_buoy numerical gate fails (> 1% error) | Coding error in P(z) or integration limits | Debug: check P(0), P(H); swap integral limits; check V(z) formula | Debug only; no method change needed |
| Fill feasibility fails (Q_required >> available) | Vessel too fast or fill window too short | Reduce v_vessel assumption or increase fill arc to 1/2 loop | Must revisit loop geometry design; affects Phase 2 cycle time |
| Ideal gas assumption breaks down | Unexpected pressure dependence in air behavior at 2.770 atm | Van der Waals correction: (P + a/V²)(V - b) = nRT | Negligible at 3 atm; essentially no chance of this being needed |

**Decision criteria:** The primary approach (Approach 1) is robustly applicable to all Phase 1 calculations. The only realistic failure mode that requires a method switch is if the terminal velocity force balance reveals that chain tension is comparable to buoyancy force — in that case, the coupled ODE is needed. This would be flagged by v_terminal < 1.5 m/s or non-convergence of the fixed-point iteration.

---

## Caveats and Alternatives

**What assumption might be wrong?**

The isothermal expansion assumption during ascent deserves scrutiny. The buoyancy integral uses V(z) = V_surface × P_atm / P(z), which assumes the air expands isothermally as the vessel rises. If the ascent is fast (< a few seconds) and the vessel walls are thermally insulating, the expansion could be closer to adiabatic. Adiabatic expansion gives slightly less buoyancy work than isothermal (by the same factor as adiabatic compression exceeds isothermal compression). This would mean W_buoy < W_iso slightly. The thermal time constant for the air inside the open-bottom vessel at 3 m/s ascent is approximately the ascent time (~6 s) divided by the thermal equilibration time (estimated seconds for a 0.457 m diameter cylinder in water). These are comparable, suggesting the process is neither fully isothermal nor fully adiabatic — it is somewhere in between. For Phase 1 feasibility, the isothermal formula gives the correct order of magnitude and remains exact in the limit of slow ascent. The deviation from isothermal at 3 m/s is estimated at < 5% and does not change the go/no-go conclusion.

**What alternative approach was dismissed too quickly?**

The polytropic compression formula W = [n/(n-1)] × P₁V₁ × [(P₂/P₁)^((n-1)/n) - 1] with n between 1 (isothermal) and γ = 1.4 (adiabatic) was not explicitly included. For a practical single-stage compressor with some cooling, n ≈ 1.2–1.35 is realistic. The isothermal and adiabatic bounds bracket the true value, so the range is captured, but reporting a specific n = 1.25 estimate might be useful for Phase 4. This is not critical for Phase 1 feasibility.

**What limitation is understated?**

The terminal velocity calculation treats the vessel as an isolated body in an infinite fluid. In reality, the vessel chain moves in a confined 24 ft cylinder, and wake effects from adjacent vessels (PITFALL-M3) may increase the effective drag. With 15 ascending vessels spaced ~H/7.5 ≈ 2.4 m apart in a 7.32 m diameter cylinder, blockage effects could be significant. The isolated-vessel terminal velocity is an overestimate of the actual velocity under blockage conditions. This does not invalidate Phase 1, but means the terminal velocity should be treated as an upper bound.

**Is there a simpler method?**

The fixed-point iteration for terminal velocity is already simple (3–5 lines of code). There is no simpler method that gives a numerical result. A back-of-envelope estimate using F_b_avg = 1129 N and F_drag = ½ × 998.2 × 1.0 × 0.164 × v² confirms v ≈ sqrt(2 × 1129 / (998.2 × 0.164)) ≈ 3.7 m/s without any iteration — but this does not account for how F_b varies with z, which is the point of the iterative calculation.

---

## Sources

### Primary (HIGH confidence)

- Çengel, Y.A. & Boles, M.A., "Thermodynamics: An Engineering Approach," 9th ed., McGraw-Hill — Ch. 9: compression work formulas (isothermal, adiabatic), isentropic efficiency definition. Standard engineering thermodynamics reference.
- Project CONVENTIONS.md (2026-03-16) — Locked numerical values for all system parameters: H, P_atm, P_bottom, P_r, V_surface, V_depth, ρ_w, g, A_frontal. These are authoritative for Phase 1.
- Project METHODS.md (2026-03-16) — Compression work derivation path (§1), variable-volume buoyancy integral derivation and identity (§2), terminal velocity method (§3).
- Project PRIOR-WORK.md (2026-03-16) — Established Results 1–3: thermodynamic equivalence, adiabatic penalty, compressor efficiency range.
- Project PITFALLS.md (2026-03-16) — C1, C6, C7, M1, M5: the five pitfalls that apply to Phase 1.

### Secondary (MEDIUM confidence)

- Hoerner, S.F., "Fluid-Dynamic Drag," 1965 — C_D tables for blunt cylinders at Re ~ 10^5–10^6. C_D range 0.8–1.2 for L/d ≈ 2.7 used in terminal velocity calculation. [TRAINING-KNOWLEDGE — verify by accessing Hoerner tables directly]
- Pimm, A.J. et al., Energy, 41(1), 2012 — Underwater CAES; confirms buoyancy-compression thermodynamic equivalence independently. [TRAINING-KNOWLEDGE]
- Project COMPUTATIONAL.md (2026-03-16) — Python pseudocode for buoyancy integral (§3) and terminal velocity (§4); directly usable for Phase 1 implementation.
- scipy.integrate.quad documentation — Adaptive quadrature; atol and rtol parameters for convergence control. Available at docs.scipy.org.

### Tertiary (LOW confidence — training knowledge only)

- Commercial compressor specifications for FILL-03 feasibility — Market data for industrial rotary screw compressors at 100–200 CFM, 25–50 psi gauge; approximate only. Verify against specific vendor specifications before reporting FILL-03 as feasible.

---

## Metadata

**Confidence breakdown:**

- Mathematical framework (compression work, buoyancy integral): HIGH — exact first-principles derivations; confirmed in project scoping to < 0.3%
- Standard approaches (analytical + scipy.quad): HIGH — all methods are standard; no novel methods required
- Terminal velocity calculation: MEDIUM — force balance approach is exact at steady state, but C_D range (0.8–1.2) from Hoerner introduces ± 20% uncertainty; chain coupling adds additional uncertainty
- Fill feasibility (FILL-01, FILL-02): HIGH — direct geometric and flow rate calculation; uncertainty is dominated by terminal velocity uncertainty
- Fill feasibility (FILL-03, practical assessment): MEDIUM — requires comparison against compressor market data not independently verified in project research files

**Research date:** 2026-03-16

**Valid until:** The thermodynamic results are permanent (first principles). The C_D empirical values are stable (Hoerner 1965 is a standard reference). The fill feasibility compressor data may change with market availability; re-check for prototype procurement.

---

## Requirements Coverage

| Requirement | Phase 1 Method | Key Equation | Validation Gate |
| --- | --- | --- | --- |
| THRM-01 | Isothermal + adiabatic formulas; η_c correction | W_iso = P_atm V_surface ln(P_r); W_adia = 3.5 × P_atm V_surface (P_r^0.2857 - 1); W_actual = W_adia / η_c | W_iso = 20,640 J ± 10 J; W_adia = 24,040 J ± 20 J; ratio = 1.165 ± 0.003 |
| THRM-02 | Boyle's law at depth and surface; fill target condition | V_depth = V_surface / P_r = 0.07228 m³; fill target: vessel exactly full at z = H | V_depth = 0.07228 m³ ± 0.0001 m³; V_depth × P_r = V_surface (Boyle's law check) |
| THRM-03 | Confirm jet work = W_buoy; do not add as separate term | W_jet = W_buoy (same phenomenon); shaped nozzle affects C_D_hull only | No additional energy from jet beyond W_buoy; documented as single line item |
| BUOY-01 | Variable-volume F_b(z) profile | F_b(z) = ρ_w × g × V_surface × P_atm / P(z); evaluate at multiple z values | F_b(0) ≈ 707 N; F_b(H) ≈ 1959 N; monotonically increasing |
| BUOY-02 | scipy.quad integration; W_buoy vs W_iso identity | W_buoy = ∫₀ᴴ F_b(z) dz; analytical = P_atm V_surface ln(P_r) | |W_buoy - W_iso| / W_iso < 0.01 (MANDATORY GATE) |
| BUOY-03 | Fixed-point iteration on force balance | v_{n+1} = sqrt(2 F_b_avg / (ρ_w C_D A_frontal)); iterate | v_terminal within ± 20% of 3 m/s; convergence |Δv/v| < 10^-6 in ≤ 10 steps |
| FILL-01 | Loop geometry; fill arc = 1/4 circumference | t_fill = (2π R_tank / 4) / v_terminal = (π R_tank / 2) / v_terminal | t_fill ≈ 1.9 s at 3 m/s; update with v_terminal |
| FILL-02 | Flow rate from fill volume and window | Q = V_depth / t_fill; report in m³/s and CFM at depth pressure | Q ≈ 0.038 m³/s ≈ 80 CFM at 2.770 atm; update with v_terminal |
| FILL-03 | Comparison with commercial compressor specs | Industrial rotary screw at 50–200 CFM, 25–50 psi gauge; assess single-unit feasibility | Q_required < maximum available from standard commercial unit |
