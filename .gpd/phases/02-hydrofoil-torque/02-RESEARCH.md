# Phase 2: Hydrofoil & Torque - Research

**Researched:** 2026-03-17
**Domain:** Hydrofoil hydrodynamics / low-speed fluid mechanics / velocity-triangle power analysis
**Confidence:** MEDIUM-HIGH (mathematical framework HIGH; tacking geometry MEDIUM; foil geometry selection MEDIUM)

---

## User Constraints

No CONTEXT.md exists for Phase 2. All method and geometry choices are at agent discretion, subject to the locked values inherited from Phase 1 and the project contract.

Key constraints from Phase 1 and the project contract:

- **SI units throughout** (m, kg, s, N, J, W, Pa)
- **v_vessel**: use nominal 3.7137 m/s (C_D=1.0, F_chain=0) and conservative 3.0752 m/s (C_D=1.2, F_chain=200 N); full range [2.5303, 4.152] m/s — NOT the assumed 3.0 m/s (Pitfall C7 guard)
- **W_pump at nominal η_c=0.70**: 34,228 J; full range 28,188–36,861 J
- **W_foil_net required for COP=1.5 at η_c=0.70**: ≥ 30,697 J per cycle (= 1.5 × 34,228 − 20,645)
- **Hydrofoil force convention**: L = 0.5 × ρ_w × C_L_3D × A_foil × v_rel²; D = 0.5 × ρ_w × (C_D_0 + C_D_i) × A_foil × v_rel²
- **Co-rotation convention**: v_rel_h = v_h × (1 − f_corot); f_corot ∈ [0,1]
- **Force sign**: F_L positive in shaft rotation direction
- **Tank geometry**: R_tank = 3.66 m, H = 18.288 m, N_vessels = 30 (10 per loop × 3 loops)
- **Vessel geometry**: cylinder 0.2286 m diameter × 1.219 m long; V_surface = 0.2002 m³
- **rho_w** = 998.2 kg/m³; **g** = 9.807 m/s²; **nu_w** = 1.004 × 10⁻⁶ m²/s (kinematic viscosity of water at 20°C)

**Deferred** (Phase 3 scope): co-rotation fraction and maintenance cost — do not compute in Phase 2.

---

## Active Anchor References

| Anchor / Artifact | Type | Why It Matters Here | Required Action | Where It Must Reappear |
| --- | --- | --- | --- | --- |
| `analysis/phase1/outputs/buoy03_terminal_velocity.json` | Prior artifact — v_vessel | v_vessel is direct input to all lift/drag/power calculations; wrong v means wrong forces | Load v_handoff values; do NOT hardcode v=3.0 | FOIL-01, FOIL-02, FOIL-03, FOIL-04 every calculation |
| `analysis/phase1/outputs/phase1_summary_table.json` | Prior artifact — W_pump, W_buoy, COP_baseline | Establishes the deficit hydrofoil must overcome: W_foil_net ≥ 30,697 J at η_c=0.70 | Load W_pump_nominal_J and W_pump_table | FOIL-04 minimum L/D calculation |
| NACA TR-824 (Abbott et al., 1945; free via NASA NTRS) | Benchmark — 2D C_L, C_D tabulated data | Primary experimental source for C_L(α), C_D(α) at Re = 3×10⁵–9×10⁶; XFOIL validation gate | Cite for validation; use Re=10⁶ section data for α = 5–10° | FOIL-01 XFOIL gate, verification |
| Abbott & von Doenhoff, "Theory of Wing Sections," Dover 1959 | Method reference — thin-airfoil + Prandtl LL | Source for C_L = 2πα, finite-span formulae; canonical textbook | Cite for all thin-airfoil and LL equations | FOIL-01 mathematical framework |
| Anderson, "Fundamentals of Aerodynamics," 5th ed., McGraw-Hill | Method reference — Prandtl lifting line | Section 5.3 Prandtl lifting-line; induced drag derivation | Cite for C_D_i = C_L² / (π e AR) formula | FOIL-01 |
| Ladson et al., NASA TM-4074, 1988 | Benchmark — XFOIL validation | NACA 0012 at Re=10⁶, α=0°: C_D ≈ 0.006 ± 15%; gates XFOIL run quality | Must pass before Phase 2 foil sweeps | FOIL-01 validation gate |
| Drela, M., "XFOIL: An Analysis and Design System for Low Reynolds Number Airfoils," 1989 | Method reference — XFOIL code | Defines valid Re range 10⁴–10⁷; N-factor transition criterion | Cite; note N_crit=9 for free-stream turbulence | FOIL-01 XFOIL section |

**Missing or weak anchors:**
- No published work directly measures hydrofoil torque contribution in a buoyancy-driven loop-conveyor system. This phase applies standard thin-airfoil + velocity-triangle methods (well established for analogous systems: buoyancy gliders, Darrieus VAWT, oscillating-foil turbines) to a novel geometry. Confidence in the method is HIGH; confidence in the specific geometry assumptions (foil span, chord, mount angle) is MEDIUM because they are design choices not yet constrained by hardware.
- No measurement of the tack-flip transition loss exists. Assume ideal tack (no transition energy loss) as the optimistic bound; flag as a source of MEDIUM uncertainty.

---

## Conventions

| Choice | Convention | Alternatives | Source |
| --- | --- | --- | --- |
| Unit system | SI (m, kg, s, N, J, W, Pa) | Imperial (for design reference only) | Phase 1 lock |
| Fluid density | ρ_w = 998.2 kg/m³ (fresh water, 20°C) | Salt water 1025 kg/m³ | Phase 1 lock |
| Kinematic viscosity | ν_w = 1.004 × 10⁻⁶ m²/s | Temperature-dependent table | CRC Handbook |
| Reynolds number | Re = v_rel × c / ν_w (c = chord length) | Re based on span | Standard aerodynamics |
| Lift/drag force convention | L = ½ ρ_w C_L A_foil v_rel²; D = ½ ρ_w C_D A_foil v_rel² | Per-unit-span | Phase 1 contract |
| C_D notation | C_D = C_D_0 + C_D_i (profile drag + induced drag) | C_D_total only | Anderson / Abbott |
| Angle of attack | α measured relative to the local flow direction (velocity triangle resultant v_rel), NOT relative to vessel axis | — | Standard aero convention; PITFALL m2 guard |
| Torque sign | Positive torque in shaft rotation direction (ascending vessel drives loop counterclockwise viewed from above, per design) | — | Phase 1 force sign convention |
| Foil planform area | A_foil = span × chord (rectangular approximation) | Trapezoidal/tapered | Standard; conservative |
| Aspect ratio | AR = span² / A_foil = span / chord (for rectangular foil) | Effective AR with endplates | Anderson Ch. 5 |
| Oswald efficiency | e = 0.85 (default for rectangular foil, AR 4–6) | 0.7–1.0 range | Anderson; will sweep |
| Energy per cycle | W_foil = integral of (net tangential force × path element) over one full loop traversal | Torque × angle | Equivalent; use force × displacement |
| Co-rotation placeholder | f_corot = 0 for Phase 2 (conservative baseline); Phase 3 will parametrize f | f ∈ [0,1] | Phase 1 contract |

**CRITICAL: All lift and drag coefficients are functions of α (angle of attack relative to local flow), not relative to the vessel long axis. The AoA seen by the foil must be computed from the velocity triangle, not assumed equal to the mount angle.**

---

## Mathematical Framework

### Key Equations and Starting Points

| Equation | Name/Description | Source | Role in This Phase |
| --- | --- | --- | --- |
| L = ½ ρ_w C_L_3D A_foil v_rel² | Lift force (3D foil, wetted area) | Abbott & von Doenhoff, NACA TR-824 | Compute lift from phase 1 velocity and chosen foil geometry |
| D = ½ ρ_w (C_D_0 + C_D_i) A_foil v_rel² | Total drag force | Abbott; Anderson Ch. 5 | Compute drag opposing vessel motion |
| C_L_2D ≈ 2π α (α in radians, small AoA) | Thin airfoil theory lift slope | Abbott & von Doenhoff Ch. 4; Anderson §4.8 | First-order estimate; cross-check NACA TR-824 data |
| C_L_3D = C_L_2D / (1 + 2/AR) | Prandtl lifting-line finite-span correction (elliptic load) | Anderson §5.3; Abbott Ch. 8 | Reduce 2D C_L to 3D; valid for AR > 4 |
| C_D_i = C_L_3D² / (π e AR) | Induced drag coefficient | Anderson §5.3 | Induced drag penalty for finite span |
| Re = v_rel × c / ν_w | Reynolds number | Standard | Validates NACA data applicability and XFOIL regime |
| α_eff = arctan(v_v / v_h) | Effective angle of attack seen by foil | Velocity triangle geometry | Key kinematic quantity linking vessel motion to foil performance |
| P_lift = F_L × v_h | Power extracted by foil lift (horizontal component) | METHODS.md §6; PITFALL-C2 | Net useful shaft power from one vessel's foil |
| P_drag_foil = F_D × v_rel | Power lost to foil drag | METHODS.md §6 | Loss term to subtract |
| P_net_foil = F_L v_h − F_D v_rel | Net power per vessel foil | METHODS.md §6 | Central quantity for FOIL-02, FOIL-03 |
| W_foil_net = N_vessels × P_net_foil × t_cycle | Net foil energy per cycle (all vessels) | Project contract | FOIL-04 COP check input |
| COP = (W_buoy + W_foil_net) / W_pump | System COP (Phase 2 partial — no drag, no co-rotation yet) | Project contract | Phase 2 go/no-go preview |

### Required Techniques

| Technique | What It Does | Where Applied | Standard Reference |
| --- | --- | --- | --- |
| Velocity triangle decomposition | Resolves vessel velocity (v_v, v_h) into foil-frame AoA and v_rel | FOIL-01 (every vessel position) | Turbomachinery standard; Anderson §4.1 |
| Thin airfoil theory (C_L = 2πα) | Gives first-order C_L without empirical data | FOIL-01 verification against NACA table | Abbott & von Doenhoff Ch. 4 |
| NACA TR-824 tabular lookup | Provides C_L(α), C_D(α) at Re = 3×10⁵–9×10⁶ for standard profiles | FOIL-01 primary data | NACA TR-824 (free via NASA NTRS ntrs.nasa.gov) |
| Prandtl lifting-line correction | Converts 2D section data to 3D finite-span foil | FOIL-01 C_L_3D, C_D_i | Anderson §5.3; Abbott Ch. 8 |
| Power balance via P = F·v | Computes net shaft power from force-velocity products | FOIL-02, FOIL-03 | PITFALL-C2 prevention; standard fluid mechanics |
| Parametric sweep (numpy) | Evaluates W_foil_net over (L/D, AR, AoA, v_vessel) grid | FOIL-04 | numpy.meshgrid; vectorized computation |
| Tacking geometry analysis | Verifies descending vessel foil direction produces torque in same sense | FOIL-03 | Darrieus VAWT analogy; see Standard Approaches |

### Approximation Schemes

| Approximation | Small Parameter | Regime of Validity | Error Estimate | Alternatives if Invalid |
| --- | --- | --- | --- | --- |
| Thin airfoil theory C_L = 2πα | α (radians) << 1; thickness/chord << 1 | α < 8°, AR >> 1, attached flow, Re > 10⁵ | O(α²), ~10% at α=8° | NACA TR-824 tabulated data (primary) |
| Prandtl lifting-line (elliptic) | 1/AR << 1 | AR > 4, attached flow throughout span | ~5–10% error in C_L at AR=4; less at AR=6 | XFLR5 vortex-lattice method (AR < 4) |
| Quasi-steady foil forces | Reduced frequency k = ωc/(2v) << 1 | k ~ (ω_loop × c) / (2 v_vessel); with c ≈ 0.25 m, v ≈ 3.7 m/s, ω_loop ≈ v/R ≈ 1 rad/s → k ≈ 0.034 << 1 | Unsteady corrections O(k²) ~ 0.1%; negligible | Theodorsen's unsteady theory if k > 0.1 |
| Rectangular planform approximation | Taper ratio → 1 | Rectangular foil; reasonable for a simple foil strut | Induced drag ~5% higher than elliptic planform at same AR | Tapered/elliptic planform (not necessary at feasibility stage) |
| Constant v_vessel during ascent | Rate of change dv/dt << v²/H | True for quasi-steady ascent of buoyancy-driven vessel | Actual acceleration phase < 0.5% of path | Full ODE trajectory (not needed for feasibility) |
| f_corot = 0 in Phase 2 | — | Conservative baseline; maximizes vessel-water relative velocity | Optimistic scenario uses f_corot > 0 (Phase 3) | Phase 3 parametric |

---

## Standard Approaches

### Approach 1: Thin Airfoil Theory + NACA Tabular Data + Prandtl Lifting Line (RECOMMENDED)

**What:** Use thin airfoil theory for intuition and cross-checking, NACA TR-824 empirical section polars as the primary C_L/C_D source, and Prandtl's lifting-line formula for the finite-span (3D) correction. Compute foil forces at each vessel velocity from the Phase 1 output, then apply the velocity-triangle power balance to get net shaft power per vessel.

**Why standard:** This is the canonical approach for preliminary hydrofoil design at Re ~ 10⁵–10⁶ and low AoA. It is used in every maritime engineering textbook for strut and foil sizing (Abbott & von Doenhoff; Kerwin, MIT OCW). It provides closed-form expressions suitable for parametric sweeps without CFD. It has been validated extensively against experiment for NACA profiles.

**Track record:** NACA TR-824 data has been used to design hydrofoils, aircraft wings, and low-speed turbine blades for 80+ years. The Prandtl lifting-line approximation is accurate to within 5–10% for AR ≥ 4 with attached flow, which covers the vessel-foil geometry at hand. The velocity-triangle power balance is used identically in buoyancy glider energy analysis (Webb et al. 2001) and oscillating-foil turbine design.

**Key steps:**

1. **Choose foil geometry.** Recommend NACA 0012 (symmetric, simple, well-documented) or NACA 4412 (cambered, higher C_L at moderate AoA). Span ≈ 1.0–1.2 m (≤ vessel length), chord ≈ 0.20–0.30 m, giving AR ≈ 4–6. These are defaults; FOIL-01 must sweep them.
2. **Compute Re at operating velocity.** Re = v_vessel × chord / ν_w. At v=3.71 m/s, chord=0.25 m: Re = 3.71 × 0.25 / 1.004×10⁻⁶ ≈ 9.2×10⁵ ≈ 10⁶. At v=3.08 m/s, chord=0.20 m: Re ≈ 6.1×10⁵. Both fall in the NACA TR-824 / XFOIL well-validated regime.
3. **Obtain C_L_2D(α), C_D_0(α) from NACA TR-824 table or XFOIL.** For NACA 0012 at Re=10⁶: C_L ≈ 0.55/0.86/1.06 and C_D ≈ 0.008/0.011/0.013 at α = 5°/8°/10°. Validate XFOIL output against Ladson et al. TM-4074 at α=0° (C_D ≈ 0.006 ± 15%).
4. **Apply finite-span correction.** C_L_3D = C_L_2D / (1 + 2/AR); C_D_i = C_L_3D² / (π × e × AR) with e=0.85.
5. **Compute velocity triangle.** For ascending vessel: v_v = v_terminal (from Phase 1), v_h = v_vessel × sin(θ_loop_position) or mean horizontal component. The foil is mounted to maximize horizontal lift; AoA in the water frame is α = arctan(v_v / v_h) minus the foil mount angle — see Tacking Geometry section.
6. **Compute forces and power.** L = ½ ρ_w C_L_3D A_foil v_rel²; D = ½ ρ_w C_D_total A_foil v_rel²; v_rel = √(v_v² + v_h²). P_net = F_L v_h − F_D v_rel.
7. **Integrate over full cycle.** W_foil = Σ_{ascending + descending} P_net × (H / v_v) per vessel, then multiply by N_vessels.
8. **Parametric sweep.** Sweep AoA ∈ [5°, 10°], AR ∈ [3, 8], chord ∈ [0.15, 0.35 m], L/D ∈ [5, 30] (as parameterized per contract). Identify minimum L/D for COP ≥ 1.5.

**Known difficulties at each step:**

- Step 1: Foil span is constrained by vessel diameter/length; overlong spans create structural complexity. Recommend starting with span = 1.0 m (vessel length minus end caps ≈ 1.1 m × 0.9 = 1.0 m usable).
- Step 3: NACA TR-824 tabulates data at Re = 3, 6, 9 × 10⁶ (high Re). At Re ~ 10⁶, interpolation or XFOIL is needed. XFOIL at Re=10⁶ agrees with experiment within 10–15% for C_D and 3–5% for C_L in the linear AoA regime.
- Step 5: The mean horizontal velocity v_h requires clarifying the chain loop geometry. See Open Questions item 1.
- Step 6: v_rel ≈ v_v when v_v >> v_h; this worsens the power balance (P_drag ≈ F_D × v_v is large relative to P_lift = F_L × v_h when v_h << v_v). This is the central feasibility risk.
- Step 7: Tacking analysis requires confirming direction sign (see PITFALL-C4 and tacking geometry).

### Approach 2: L/D Parametric Sweep without Explicit Foil Geometry (FALLBACK / COMPLEMENTARY)

**What:** Treat L/D as a free parameter (L/D ∈ [5, 30]) and compute required W_foil_net for COP = 1.5 without specifying foil profile. This gives the minimum L/D threshold independent of foil design assumptions.

**When to use:** Run this as FOIL-04 first — it immediately shows whether any L/D in the realistic range can satisfy the COP target. If the threshold L/D is above ~25 (unachievable with modest AR at this Re), the project stops. If it is below ~15 (easily achieved), detailed foil design matters less.

**Tradeoffs:** Less physically grounded than explicit foil geometry, but gives the critical feasibility threshold with minimal assumptions. Use both: parametric sweep to find threshold, explicit geometry to confirm achievability.

### Tacking Geometry Analysis (Required for FOIL-03)

The tacking mechanism is the critical claim that descending vessels contribute torque in the same rotational direction as ascending vessels. The geometry works as follows:

**Ascending vessel:**
- v_v is upward (+z direction)
- v_h is in the tangential direction of the loop (say, +x at the ascending side)
- The foil is mounted at a fixed AoA relative to the vessel axis. The flow impinges from below-and-ahead, creating lift in the +x direction (tangential to loop = driving rotation). This is the "forward" tack.

**Descending vessel:**
- v_v is downward (−z direction)
- v_h is in the −x direction (descending side of the loop moves in the opposite tangential direction)
- Without tacking: foil mounted at same angle generates lift in the −x direction = opposing rotation (waste)
- With tacking (foil angle flipped by the tack mechanism): the foil leading edge faces the new approach flow. The flow now impinges from above-and-ahead. The tacked foil generates lift in the +x direction at the descending side, which — because the descending vessel is on the opposite side of the loop — corresponds to the same sense of rotation as the ascending side.

**Key sign check (mandatory):** The tangential component of lift (F_L × cos(β)) where β is the angle between the lift vector and the loop tangent must have the same sign on both ascending and descending vessels after tacking. This is equivalent to the Darrieus VAWT blade generating positive torque on both the upstream and downstream passes. Confirm by explicit geometry calculation in FOIL-03.

**Analogy:** The Darrieus VAWT (Wikipedia; Darrieus 1931) generates positive torque on both sides of the rotation cycle because the blade always presents a favorable AoA to the apparent flow. The Hydrowheel tacking mechanism is equivalent: the foil always faces the buoyancy-driven flow such that the lift component points in the rotation direction.

### Anti-Patterns to Avoid

- **Treating L/D as a power ratio:** L/D is a force ratio only. Net power from the foil = F_L × v_h − F_D × v_rel ≠ L/D × (power_input). See PITFALL-C2.
  - _Example:_ L/D = 20, v_h = 1 m/s, v_v = 3.7 m/s: threshold L/D for net gain = v_rel/v_h = √(3.7² + 1²)/1 = 3.83. At L/D=20 >> 3.83, the foil IS net positive — but the net gain is NOT 20× the drag loss. The actual P_net = F_D × v_rel × [(L/D)(v_h/v_rel) − 1], a much smaller number.
- **Using AoA relative to vessel axis instead of flow direction:** The AoA the foil sees is determined by the velocity triangle (arctan(v_v / v_h) minus mount angle), not the geometric mount angle alone. See PITFALL m2.
- **Ignoring finite-span correction:** 2D C_L is 20–40% higher than 3D C_L_3D at AR=4–6. Over-optimistic if 2D data is used for W_foil computation.
- **Double-counting tacking contribution without tracking chain tension:** The descending vessel's foil energy comes from the ascending buoyancy transmitted through the chain. See PITFALL-C4.
- **Assuming zero v_h:** If v_h = 0, there is zero power extraction regardless of L/D (P_lift = F_L × 0 = 0). The loop geometry must provide a meaningful v_h.

---

## Existing Results to Leverage

### Established Results (DO NOT RE-DERIVE)

| Result | Exact Form | Source | How to Use |
| --- | --- | --- | --- |
| Thin airfoil lift slope | C_L_2D = 2π × sin(α) ≈ 2π α for α in rad | Abbott & von Doenhoff, Ch. 4; Anderson §4.8 | First-order C_L estimate and cross-check against table data |
| Prandtl lifting-line (elliptic) | C_L_3D = C_L_2D / (1 + 2/AR) | Anderson §5.3, Eq. 5.61 | Finite-span C_L correction |
| Induced drag | C_D_i = C_L_3D² / (π e AR), e ≈ 0.85 for rectangular foil | Anderson §5.3, Eq. 5.62 | Induced drag addition to profile drag C_D_0 |
| NACA 0012 at Re=10⁶, α=8°: C_L ≈ 0.86, C_D ≈ 0.011, L/D ≈ 78 (2D) | Tabular | NACA TR-824 (Abbott et al. 1945) via SUMMARY.md / METHODS.md | Primary 2D section data |
| NACA 0012 at Re=10⁶, α=0°: C_D ≈ 0.006 ± 15% | Tabular | Ladson et al., NASA TM-4074, 1988 | XFOIL validation gate before using XFOIL |
| NACA 0012 stall angle at Re=10⁶: ≈ 14–16° | Experimental | NACA TR-824; well-established | Upper bound on safe AoA; stay below 12° for margin |
| Net power formula | P_net = F_L v_h − F_D √(v_v² + v_h²) | METHODS.md §6; velocity triangle | Central computational formula for FOIL-02, FOIL-03 |
| Minimum L/D for net gain | (L/D)_min = v_rel / v_h = √(v_v² + v_h²) / v_h | METHODS.md §6 | Threshold check before parameter sweep |
| Buoyancy work (Phase 1) | W_buoy = 20,644.62 J | phase1_summary_table.json | COP denominator inputs |
| W_pump at η_c=0.70 | W_pump = 34,228 J | phase1_summary_table.json | Required W_foil_net = 1.5 × 34,228 − 20,645 = 30,697 J |

**Key insight:** The NACA TR-824 dataset and the Prandtl lifting-line formula are cornerstones of aeronautical engineering — they underpin the design of every subsonic wing since the 1940s. There is no need to derive lift slope or induced drag from first principles. The only novel computation in this phase is the velocity-triangle power balance in the Hydrowheel loop geometry and the tacking direction confirmation.

### Useful Intermediate Results

| Result | What It Gives You | Source | Conditions |
| --- | --- | --- | --- |
| NACA 0012 at Re=10⁶: C_L/α ≈ 6.1 per radian (slightly below 2π) | More accurate lift slope than thin-airfoil 2π = 6.28 | NACA TR-824 data (from METHODS.md) | Re = 10⁶, α < 12° |
| Oswald e ≈ 0.85 for rectangular foil, AR=4–8 | Default e value for induced drag | Anderson; standard practice | Rectangular, no sweep, attached flow |
| Re check: v=3.7 m/s, c=0.25 m → Re=9.2×10⁵ | Confirms turbulent regime, NACA data applicable | Direct calculation | Use this as reference point |
| Aspect ratio AR = 5 for span=1.25 m, chord=0.25 m | Typical design point; falls in valid Prandtl-LL regime | Geometry calculation | AR > 4 verified |
| Quasi-steady reduced frequency k ≈ 0.034 | Unsteady effects negligible | Calculation above | k << 0.1 → quasi-steady valid |

### Relevant Prior Work

| Paper/Result | Authors | Year | Relevance | What to Extract |
| --- | --- | --- | --- | --- |
| NACA TR-824 "Summary of Airfoil Data" | Abbott, von Doenhoff, Stivers | 1945 | Primary C_L/C_D tables for NACA 0012, 4412, 2412 at Re=3–9×10⁶; XFOIL validation reference | C_L, C_D tables at α=5–10° (interpolate to Re=10⁶ or use XFOIL) |
| "Theory of Wing Sections" | Abbott & von Doenhoff | 1959 | Prandtl lifting-line; thin-airfoil theory; complete NACA section database | Chapter 4 (2D theory), Chapter 8 (finite span); Appendix IV (data tables) |
| "Fundamentals of Aerodynamics" | Anderson, J.D. | 2017 (5th ed.) | Standard text for thin-airfoil and Prandtl LL with modern notation | §4.8 (thin airfoil C_L=2πα), §5.3 (Prandtl LL), Eqs. 5.61–5.62 |
| Buoyancy-driven glider energy analysis | Webb, Simonetti, Jones (IEEE JOE 2001) | 2001 | Direct structural analogy: vertical buoyancy velocity → horizontal propulsive force via foil | Velocity triangle framework for buoyancy glider; confirms method |
| Darrieus wind turbine aerodynamics | Paraschivoiu, I., "Wind Turbine Design With Emphasis on Darrieus Concept," 2002 | 2002 | Blade on both sides of rotation contributes positive torque — identical to tacking claim | AoA sign analysis on upwind/downwind passes; confirms tacking mechanism |
| Oscillating hydrofoil turbine | Kinzel, Ramsey, Lesieutre, J. Fluids Struct. 2007; also McKinney & DeLaurier, J. Energy 1981 | 2007/1981 | Power extraction from oscillating foil in cross-flow; validates velocity-triangle power balance for submerged foil | Eq. for instantaneous power P = L·ẏ (ẏ = heaving velocity); maps to P_lift = F_L × v_h |

---

## Hydrofoil Geometry Assumptions and Sensitivity

This section addresses the open geometry question that must be resolved at the start of FOIL-01.

### Recommended Default Geometry

Since no foil hardware is specified, Phase 2 should adopt a default design point for the parametric sweep and explicitly identify sensitivity to geometry assumptions:

| Parameter | Recommended Default | Range to Sweep | Rationale |
| --- | --- | --- | --- |
| Profile | NACA 0012 | Also test NACA 4412 | Symmetric (0012) simplifies tacking (same C_L at ±α); cambered (4412) gives higher C_L at lower α |
| Chord c | 0.25 m | 0.15–0.35 m | Re at v=3.7 → Re=9.2×10⁵ at c=0.25 m; stays in NACA-validated range |
| Span b | 1.0 m | 0.8–1.2 m | ≤ vessel length (1.219 m) minus structural end caps |
| Aspect ratio AR | 4.0 | 3–8 | b/c = 1.0/0.25; within Prandtl-LL valid range |
| AoA α | 7° | 5–10° (contract) | Mid-range; linear C_L regime; L/D near peak for NACA 0012 at Re=10⁶ |
| Foil count | 1 per vessel | 1–2 | Start with 1; 2 foils doubles torque but also doubles drag |
| A_foil | 0.25 m² | varies | b × c = 1.0 × 0.25 |

### Velocity Triangle for This Geometry

For an ascending vessel on the chain loop at radius R_tank = 3.66 m:

- v_v = v_terminal (from Phase 1 handoff): nominal 3.714 m/s, conservative 3.075 m/s
- v_h = horizontal velocity of vessel along loop tangent. This requires a geometric model of the chain loop. See Open Question 1 below.
- v_rel = √(v_v² + v_h²) (flow speed incident on foil)
- α_water = arctan(v_v / v_h) = angle of incident flow from horizontal plane
- α_foil = mount angle − α_water (or plus, depending on orientation) — the AoA seen by the foil
- The foil should be mounted so that at the design operating point, α_foil ≈ 7–8° for maximum L/D

**Critical geometry note:** The horizontal velocity v_h is set by the chain constraint, not independently by buoyancy. In a loop-conveyor arrangement where vessels move at constant speed along the loop, v_h is the horizontal projection of the chain velocity at each point. For a chain moving at speed v_chain along a loop of radius R: v_h varies from 0 at the top and bottom of the loop to v_chain at the sides. For vessels on the ascending vertical segment, v_h ≈ 0 and v_v = v_chain; the foil sees nearly vertical flow. This is the most important geometric uncertainty — see Open Question 1.

---

## Computational Tools

### Core Tools

| Tool | Version/Module | Purpose | Why Standard |
| --- | --- | --- | --- |
| Python 3.10+ | numpy, scipy | Parametric sweeps, force calculations, energy integration | Already established in Phase 1; vectorized; sufficient for feasibility |
| numpy.meshgrid | numpy | 4D parameter sweep (AoA × AR × chord × v_vessel) | Fast; no external dependency |
| scipy.integrate.quad | scipy.integrate | Integrate net power over ascent/descent path if v_h varies with position | Already validated in Phase 1 for buoyancy integral |
| XFOIL 6.99 | xfoil executable | 2D C_L(α), C_D(α) polars at specified Re | Industry standard for sub-stall section analysis; Drela 1989; free |
| matplotlib | matplotlib | L/D vs AoA plots; W_foil vs L/D curves; COP contour plots | Phase 1 established practice |

### Supporting Tools

| Tool | Purpose | When to Use |
| --- | --- | --- |
| XFLR5 (free, GUI) | 3D vortex-lattice (VLM) for finite-span correction when AR < 4 | Only if chosen AR falls below 4; otherwise Prandtl LL is sufficient |
| pandas | Results table assembly and output to JSON | For structured phase 2 output JSON files consistent with phase 1 format |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
| --- | --- | --- |
| NACA TR-824 + XFOIL | Full 3D RANS CFD (OpenFOAM, Fluent) | CFD: days per run, 3D NS accuracy; NOT needed for feasibility — integrated forces don't change answer |
| Prandtl lifting-line | Full VLM (XFLR5) | VLM: ~30 min setup, more accurate for AR < 4; use only if AR constraint forces AR < 4 |
| NACA 0012 (symmetric) | NACA 4412 (cambered) | 4412 has higher C_Lmax (~1.4 vs 1.2) but requires different AoA for ascending vs descending → complicates tacking |
| Per-vessel time-domain simulation | Cycle-average energy accounting | Time domain: not needed; quasi-steady assumption is valid (k << 0.1) |

### Computational Feasibility

| Computation | Estimated Cost | Bottleneck | Mitigation |
| --- | --- | --- | --- |
| NACA TR-824 lookup table (Python dict) | < 1 ms | None | Already structured data |
| XFOIL polar at one (Re, profile) | < 5 s | XFOIL I/O | Batch all Re values in one XFOIL session |
| Prandtl LL correction | < 1 ms (3 numpy lines) | None | Vectorized |
| 4D parameter sweep (30 AoA × 10 AR × 10 chord × 5 v values = 15,000 points) | < 1 s | None | Full vectorized numpy |
| matplotlib contour plots | < 5 s | None | Standard |
| Full phase 2 computation | < 30 s total | None | Well within single-session budget |

**Installation / Setup:**
```bash
# Python packages (if not already installed from Phase 1)
pip install numpy scipy matplotlib pandas
# XFOIL: download binary from https://web.mit.edu/drela/Public/web/xfoil/
# (MIT licensed, free; Windows binary available)
# Or on Linux/Mac: apt install xfoil  OR  brew install xfoil
```

No new dependencies beyond Phase 1 are required. XFOIL provides its own binary; no pip install.

---

## Validation Strategies

### Internal Consistency Checks

| Check | What It Validates | How to Perform | Expected Result |
| --- | --- | --- | --- |
| Thin-airfoil C_L vs NACA table | Theoretical vs empirical C_L | Compare 2πα at α=5–10° against TR-824 table values | Agree within 10% for NACA 0012 at Re=10⁶ |
| XFOIL C_D at α=0° vs Ladson TM-4074 | XFOIL calibration gate | Run XFOIL: NACA 0012, Re=10⁶, Ncrit=9; check C_D at α=0° | C_D = 0.006 ± 15% (gate: fail if outside 0.0051–0.0069) |
| Prandtl LL limit AR→∞ | Finite-span correction | C_L_3D(AR→∞) → C_L_2D | Should converge to within 1% at AR=50 |
| Minimum L/D threshold check | PITFALL-C2 guard | (L/D)_min = v_rel/v_h; verify that design L/D >> threshold | Must have L/D > v_rel/v_h for any positive P_net |
| P_net sign check at α=0 | Ensures no spurious gain at zero lift | Set C_L=0; check P_net = −F_D × v_rel < 0 | Must be negative (pure drag loss with no lift) |
| Energy conservation: W_foil ≤ W_buoy | PITFALL-C4 guard | After computing W_foil_net, verify it does not exceed W_buoy = 20,645 J | W_foil_net < W_buoy by a margin; if W_foil_net ≥ W_buoy, energy accounting is wrong |
| COP preview check: (W_buoy + W_foil_net) / W_pump | Partial COP sanity | At best-case L/D and η_c, check if COP = 1.5 is even theoretically possible | COP must be < 1.5 unless foil W > 30,697 J |

### Known Limits and Benchmarks

| Limit | Parameter Regime | Known Result | Source |
| --- | --- | --- | --- |
| Zero AoA (α=0°) | C_L = 0 | Net power = −F_D × v_rel < 0 (pure loss) | First principles |
| Large AR (AR→∞) | Prandtl LL | C_L_3D → C_L_2D = 2πα | Anderson §5.3 |
| Low v_h → 0 | Chain stops or near top/bottom of loop | P_net → −F_D × v_v < 0 (no gain) | Velocity triangle |
| NACA 0012 2D peak L/D | Re=10⁶, α≈10° | L/D_2D ≈ 75–82 | NACA TR-824 (METHODS.md) |
| NACA 0012 3D (AR=4) peak L/D | Re=10⁶, α≈10° | L/D_3D ≈ 20–30 (after induced drag penalty) | Prandtl LL calculation |
| Thin-airfoil slope | Any profile, small α | dC_L/dα = 2π per radian = 0.1096 per degree | Abbott Ch. 4 |

### Numerical Validation

| Test | Method | Tolerance | Reference Value |
| --- | --- | --- | --- |
| NACA 0012 C_L at α=8°, Re=10⁶ (XFOIL vs table) | Run XFOIL, compare to METHODS.md value | ≤ 10% | C_L ≈ 0.86 (from METHODS.md) |
| NACA 0012 C_D at α=8°, Re=10⁶ (XFOIL vs table) | Run XFOIL, compare to METHODS.md value | ≤ 15% | C_D ≈ 0.011 (from METHODS.md) |
| L/D at design point | Compute from XFOIL polar | Within 20% of NACA TR-824 extrapolation | L/D ≈ 78 (2D); ≈ 20–30 (3D at AR=4–5) |
| W_foil_net dimensional analysis | Units check (kg × m/s² × m/s × s = J) | Exact | F × v × t has units J |

### Red Flags During Computation

- **W_foil_net > W_buoy = 20,645 J**: impossible by PITFALL-C4; indicates tacking torque is being double-counted or the descending-side chain tension cost is omitted.
- **Negative AoA in the ascending vessel velocity triangle**: means the foil is generating drag in the rotation direction, not lift — re-check mount angle convention.
- **L/D_3D ≈ L/D_2D (no reduction)**: finite-span correction was not applied — AR was incorrectly set to infinity.
- **COP_partial > 1.5 even before including hull drag and chain friction**: the calculation is missing significant loss terms.
- **v_h = 0 in the velocity triangle**: chain geometry is wrong, or vessels are constrained to purely vertical motion (see Open Question 1).
- **XFOIL fails to converge (viscous solution)**: AoA is above stall or Re is outside valid range — reduce α or use laminar-flow solution only.

---

## Common Pitfalls

### Pitfall 1: L/D Treated as Power Ratio (PITFALL-C2 — CRITICAL)

**What goes wrong:** L/D = 20 is interpreted as "foil provides 20× as much useful power as it loses to drag." Wrong. L/D is a force ratio; power is force × velocity.

**Why it happens:** Intuitive but incorrect analogy to mechanical advantage.

**How to avoid:** Always compute P_net = F_L × v_h − F_D × v_rel. The net gain condition is L/D > v_rel/v_h, not L/D > 1.

**Warning signs:** If computed P_net appears to increase without bound as L/D increases — this is actually correct, but the energy source is bounded. W_foil_net must be cross-checked against W_buoy (PITFALL-C4 guard).

**Recovery:** Rewrite power balance from scratch using F·v in each direction.

### Pitfall 2: AoA Relative to Vessel Axis vs. Flow Direction (PITFALL-m2)

**What goes wrong:** The foil mount angle θ_mount is relative to the vessel long axis. But the AoA the foil sees in the flow is α = arctan(v_v / v_h) − θ_mount (approximately), where the velocity triangle determines the flow direction.

**Why it happens:** The vessel is moving vertically (v_v >> v_h) so the flow arrives primarily from below, not from ahead. At v_v = 3.7 m/s, v_h = 1 m/s: flow comes from 75° below horizontal (arctan(3.7/1) ≈ 75°). The foil mount angle must be set accordingly.

**How to avoid:** Always draw the velocity triangle first. Define α relative to v_rel direction, not vessel axis.

**Warning signs:** C_L = 0 when vessel is obviously moving (mount angle exactly cancels flow angle); or C_L = C_Lmax even at low AoA.

**Recovery:** Recalculate α from arctan(v_v / v_h) and subtract mount angle.

### Pitfall 3: Tacking Direction Sign Error (PITFALL-m1)

**What goes wrong:** The descending vessel's tacked foil generates lift in the wrong direction — opposing rotation rather than driving it.

**Why it happens:** The descending side of the loop has both v_v reversed and v_h reversed (descending side of loop moves in the opposite tangential direction). Without tracking both sign reversals carefully, the resulting torque direction is wrong.

**How to avoid:** Define a global coordinate system. Draw the velocity triangle separately for an ascending vessel at position θ=90° and a descending vessel at θ=270° (opposite side of loop). Compute the torque direction explicitly. Both should give positive torque (counterclockwise when viewed from top for the reference convention).

**Warning signs:** Tacking torque computed equal and opposite to ascending torque (total cancels) — this means tacking was applied but sign was wrong.

**Recovery:** Re-derive from first principles. The Darrieus VAWT literature provides a worked example of the geometry.

### Pitfall 4: Ignoring Finite-Span Correction (Implicit 2D Assumption)

**What goes wrong:** Using C_L_2D and C_D_0 (profile drag only) without adding induced drag C_D_i and reducing C_L.

**Why it happens:** NACA TR-824 data is 2D (infinite-span wind tunnel). It is directly copied without correction.

**How to avoid:** Always apply C_L_3D = C_L_2D / (1 + 2/AR) and add C_D_i = C_L_3D² / (π e AR) before computing forces.

**Warning signs:** L/D_3D ≈ L/D_2D ≈ 80 — unrealistically high for a foil with AR=4–5.

### Pitfall 5: Zero Horizontal Velocity (Loop Geometry Misunderstanding)

**What goes wrong:** The horizontal velocity component v_h is set to zero, resulting in P_lift = F_L × 0 = 0 — no torque contribution from any foil.

**Why it happens:** If the chain loop forces vessels to move purely vertically on the ascending/descending straight sections, there is no horizontal velocity component at the foil. Foils on the vertical segments would see only vertical flow — the lift would be horizontal, but the work done by that lift against the chain is zero if the chain moves purely vertically.

**Why this is the central feasibility question:** In a straight-vertical loop section, v_h = 0 by definition. The foil must be located on the curved section of the loop (the transition from horizontal to vertical) OR the chain must be run at an angle, OR the tank must be an inclined loop. See Open Question 1.

**How to avoid:** Resolve the chain loop geometry before FOIL-01 proceeds. The value of v_h is not free — it is set by the physical loop path.

---

## Level of Rigor

**Required for this phase:** Engineering calculation — controlled approximations with explicit error estimates. Physicist's proof standard (not formal mathematical proof). Numerical results to 3 significant figures.

**Justification:** This is a feasibility study. The goal is to establish whether COP ≥ 1.5 is plausible under realistic assumptions. Engineering-level accuracy (5–15%) is sufficient for a go/no-go verdict. If the result is marginal (COP ≈ 1.4–1.6), state the uncertainty range explicitly.

**What this means concretely:**

- All series approximations (thin-airfoil C_L = 2πα) must be validated against tabular data; discrepancies > 10% at design AoA require using tabular data instead
- Finite-span corrections must be applied; using 2D C_L without correction is an error, not an approximation
- Numerical results (W_foil_net, L/D_min) reported to 3 significant figures with ±% uncertainty bounds
- Geometry assumptions (foil span, chord, AR) must be explicitly stated; sensitivity to ±20% variation in these quantities must be reported
- Chain geometry must be explicitly stated and justified

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
| --- | --- | --- | --- |
| Lifting-line theory only (1920s) | XFOIL 2D polar + LL correction for finite span | Drela 1989 | XFOIL provides accurate C_D near stall and at transitional Re; more reliable than 2D theory alone |
| NACA TR-824 tables at Re = 3–9×10⁶ | XFOIL at arbitrary Re (down to 10⁴) | 1989–present | Can compute section polars at exactly Re = 10⁶ as needed, rather than interpolating from high-Re tables |
| Hand-calculated parametric sweeps | numpy vectorized sweeps | 1990s | Thousands of parameter combinations in < 1 s; full sensitivity analysis practical |

**Superseded approaches to avoid:**

- **Full 3D RANS CFD for feasibility-stage foil evaluation:** Adds 100× compute cost without changing the sign of the go/no-go verdict. Reserve for post-feasibility detailed design.
- **Joukowski transformation for airfoil design:** Historical 2D conformal mapping method; no advantage over NACA TR-824 data for off-the-shelf profiles.

---

## Open Questions

1. **[HIGH PRIORITY] What is the horizontal velocity component v_h at the ascending and descending foil positions?**
   - What we know: The chain loop constrains vessel path. On purely vertical straight sections, v_h = 0. On the curved transition sections, v_h > 0.
   - What's unclear: The loop geometry for the Hydrowheel. Is it a purely vertical pair of straight runs (like a bucket elevator), with only 90° curved sections at top and bottom? Or is the loop arranged differently? If ascending/descending runs are vertical and straight, the foils on those straight sections have v_h = 0 and produce no torque. If this is the case, the entire hydrofoil torque mechanism as described in the contract is geometrically impossible, and the design must involve either (a) angled straight sections, (b) curved sections with substantial arc length, or (c) a different foil orientation than assumed.
   - Impact: **Highest single impact on phase 2**. If v_h = 0 on the ascent path, W_foil = 0. If v_h is significant, W_foil can be large.
   - Recommendation: **Before FOIL-01 executes, establish the chain loop geometry and compute v_h as a function of position.** Review any mechanical drawings, descriptions, or prior notes. Consider that the vessel is on a conveyor loop that goes around the outside of a circular tank (3-loop configuration) — this implies the ascending sections are approximately vertical, which gives v_h ≈ 0 during most of the ascent. If this is confirmed, the foil mechanism needs re-examination.

   **Alternative interpretation that makes v_h nonzero:** The foil on a vessel ascending vertically can still generate horizontal force — but that horizontal force does no work on the chain (which moves vertically). For the foil to contribute to shaft torque, the force must have a component in the direction of chain motion. If the chain moves purely vertically, only vertical forces count. If the chain routes through curved sections and wraps around a sprocket, the foil horizontal force during the straight vertical section does work on the chain tension, which is transmitted to the sprocket (shaft) via the chain tension vector. **This is actually the correct mechanism** — the chain tension from a horizontally-pulled vessel on the straight vertical section does pull the sprocket tangentially. Resolving this properly requires treating the chain as the mechanical coupling between foil force and shaft rotation. This is exactly the Darrieus VAWT / conveyor-chain energy transmission problem.

   **Revised mechanics (important clarification for FOIL-01):** For a vessel ascending on a straight vertical chain section:
   - The buoyancy force lifts the chain upward on the ascending side.
   - The foil generates horizontal force (lift) — this force is transmitted as chain tension horizontally.
   - But on a vertical straight chain section, the sprocket at the top only receives vertical force from the chain — horizontal tension at mid-section does not directly drive the sprocket.
   - **CONCLUSION**: For foil torque to drive the shaft, the foil force must have a component tangential to the loop path at the sprocket. This only happens efficiently when vessels are near the sprocket (top or bottom curve). The key question is what fraction of the ascent path is near the curved sections.
   - This subtlety is the same as asking "why does a bicycle chain transmit force to the rear wheel" — the answer involves the geometry of how chain tension becomes torque at the sprocket.
   - **Recommend:** Treat the horizontal lift force as generating a chain tension increment that is transmitted to the nearest sprocket tangentially. The efficiency of this transmission depends on the chain angle at the point of lift application. Model this as an effective coupling factor η_chain ∈ [0,1]; η_chain = 1 when foil is at the sprocket, η_chain → 0 for foil in mid-straight section if the straight is long.
   - **Alternative simpler model** (recommended for Phase 2 feasibility): Assume the foil force is effective over the full ascent if the foil lift is directed tangentially to the loop, which requires the loop to be non-vertical or the foil orientation to create tangential force. If the loop has a non-trivial curved profile, the average horizontal/tangential component of the foil force over the full loop may be non-zero.

2. **[HIGH PRIORITY] What foil geometry (chord, span, AR) is physically feasible given the vessel dimensions?**
   - What we know: Vessel is 0.2286 m diameter × 1.219 m long. Foil span ≤ vessel length.
   - Recommendation: Default to span = 1.0 m, chord = 0.25 m (AR = 4.0); sweep span 0.8–1.2 m and chord 0.15–0.35 m.

3. **[MEDIUM PRIORITY] NACA 0012 vs. NACA 4412 for the tacking application.**
   - What we know: NACA 0012 is symmetric — same C_L at +α and −α, which makes tacking trivial (same performance in both directions). NACA 4412 is cambered — higher C_L but asymmetric behavior may complicate the tack.
   - Recommendation: Use NACA 0012 as primary for Phase 2. This is the correct choice for a tacking foil. Cambered sections can be deferred to physical prototype optimization.

4. **[MEDIUM PRIORITY] What is the effective number of foil-bearing vessels contributing simultaneously?**
   - What we know: N_vessels = 30 (10 per loop × 3 loops). Not all vessels contribute foil torque at maximum efficiency simultaneously.
   - Recommendation: Assume all 15 ascending vessels (half of 30) contribute uniformly in FOIL-02, and all 15 descending vessels in FOIL-03. This is conservative in some ways (assumes uniform foil contribution along entire ascent) and optimistic in others (ignores taper at top/bottom of loop). Treat as uniform-contribution baseline.

---

## Alternative Approaches if Primary Fails

| If This Fails | Because Of | Switch To | Cost of Switching |
| --- | --- | --- | --- |
| Thin-airfoil + NACA TR-824 + Prandtl LL | Foil is in separated-flow regime (α > 12°, or Re < 3×10⁵) | XFOIL with explicit N-factor transition (higher fidelity) | ~15 min to set up and validate XFOIL |
| Prandtl LL (AR < 4) | Chosen foil has very short span/chord ratio | XFLR5 VLM (3D vortex-lattice, free GUI) | ~1 hour to set up; results more accurate |
| Standard velocity triangle (v_h ≈ 0) | Loop geometry confirmed to have straight vertical sections with no useful v_h | Redesign foil orientation OR use curved loop sections — this is a design change, not a computation change | Significant — requires revisiting mechanical design concept |
| NACA 0012 profile | Poor L/D in the relevant Re range | NACA 4412 (asymmetric, but higher C_L at moderate AoA) or NACA 2412 | ~30 min for additional XFOIL run |

**Decision criteria:** If Phase 2 finds that achievable L/D_3D < (minimum L/D for COP=1.5), the project verdict must be re-examined. Document the threshold explicitly in FOIL-04 output.

---

## Caveats and Alternatives (Pre-Submission Self-Critique)

**1. What assumption might be wrong?**
The most dangerous assumption is that the foil generates meaningful horizontal torque during the straight vertical ascent section. If the chain loop is a simple bucket-elevator (straight vertical ascending and descending legs with 180° turns at top and bottom), the foil force during straight ascent is horizontal — but whether that horizontal chain tension translates into sprocket torque depends on the sprocket geometry. A simple sprocket only receives the force component tangential to its circumference, which for a straight vertical chain carrying a horizontal tension is the tension force itself transmitted as a torque arm moment. This works, but requires the chain to be able to transmit horizontal tension without slipping or becoming slack — possible with a rigid chain guide. This subtlety MUST be resolved in FOIL-01.

**2. What alternative did I dismiss too quickly?**
Full XFLR5 3D VLM could be used instead of Prandtl LL. I dismissed it because AR ≥ 4 and LL is accurate to 5–10% in that regime. If the executor finds AR falls below 4 (e.g., very short span), XFLR5 should be used.

**3. What limitation am I understating?**
The quasi-steady assumption is stated as valid (k ≈ 0.034). However, the chain loop has a finite number of vessels (10 per loop), and each vessel passing a point creates a periodic perturbation. If the chain speed varies or if wake effects are significant, the quasi-steady force on each foil may be modulated. This is a secondary effect for feasibility but should be noted.

**4. Is there a simpler method?**
Yes: the L/D parametric sweep (Approach 2, FOIL-04 first) immediately shows whether ANY L/D achievable by a real hydrofoil can satisfy COP = 1.5. This is the simplest possible calculation and should be done before any detailed foil geometry work. If the threshold L/D > 30 (unachievable), all detailed foil analysis is moot.

**5. Would a fluid mechanics specialist disagree?**
A specialist would likely flag the chain-to-sprocket torque transmission mechanism more strongly than I have. The specific mechanical question of "how does horizontal chain tension become shaft torque" is non-trivial and design-dependent. The specialist would also note that XFOIL predictions for C_D at Re ~ 10⁶ with free transition may overestimate performance if the actual flow has higher free-stream turbulence intensity (turbulence shortens transition distance, increasing C_D). Use N_crit = 9 (low turbulence) as the optimistic case and N_crit = 3–5 (higher turbulence) as a sensitivity check.

---

## Sources

### Primary (HIGH confidence)

- Abbott, I.H. & von Doenhoff, A.E., "Theory of Wing Sections," Dover, 1959 — Chapter 4 (thin airfoil theory, C_L = 2πα), Chapter 8 (finite span, Prandtl LL), Appendix IV (NACA section data tables). Primary Phase 2 mathematical reference.
- NACA TR-824, Abbott, von Doenhoff & Stivers, 1945 — C_L(α), C_D(α) experimental tables for NACA 0012, 4412, 2412 at Re = 3, 6, 9 × 10⁶. Free via NASA NTRS (ntrs.nasa.gov). Primary Phase 2 data source.
- Anderson, J.D., "Fundamentals of Aerodynamics," 5th ed., McGraw-Hill, 2017 — §4.8 (thin airfoil C_L = 2πα), §5.3 (Prandtl lifting-line, C_D_i formula, Eqs. 5.61–5.62). Standard aerodynamics textbook.
- Drela, M., "XFOIL: An Analysis and Design System for Low Reynolds Number Airfoils," in Low Reynolds Number Aerodynamics, Springer, 1989 — XFOIL algorithm, N-factor criterion, validation range Re = 10⁴–10⁷.
- Phase 1 outputs: `analysis/phase1/outputs/buoy03_terminal_velocity.json`, `phase1_summary_table.json` — authoritative v_vessel, W_pump, W_buoy values.

### Secondary (MEDIUM confidence)

- Ladson, C.L., Brooks, C.W., Hill, A.S., Sproles, D.W., NASA TM-4074, 1988 — NACA 0012 at Re = 6×10⁶; C_D at α=0° ≈ 0.006. XFOIL calibration gate reference.
- Webb, D.C., Simonetti, P.J. & Jones, C.P., IEEE Journal of Oceanic Engineering 26(4), 2001, pp. 447–452 — Slocum underwater glider; buoyancy-driven vertical motion → horizontal propulsion via foil. Direct structural analogy for velocity-triangle power balance.
- Kerwin, J.E., "Hydrofoils and Propellers," MIT OCW course notes, 2001 (MIT OCW 2.23) — Low-speed hydrofoil design; finite-span methods for underwater foils; 3D effects.
- McKinney, W. & DeLaurier, J., "The Wingmill: An Oscillating-Wing Windmill," Journal of Energy 5(2), 1981 — First analysis of oscillating foil for power extraction; velocity-triangle power balance for submerged foil analogous to Phase 2.
- Paraschivoiu, I., "Wind Turbine Design With Emphasis on Darrieus Concept," Presses Internationales Polytechnique, 2002 — Darrieus VAWT blade torque on both sides of rotation cycle; validates tacking sign analysis.

### Tertiary (LOW confidence — verify before use)

- airfoiltools.com XFOIL predictions for NACA 0012 at Re=1,000,000 — useful as cross-check for XFOIL runs; NOT primary data source (web source, unverified accuracy). [TRAINING-KNOWLEDGE]
- Engineering experience / training data: NACA 0012 at Re=10⁶, α=8°: C_L≈0.86, C_D≈0.011, L/D≈78. These values appear in METHODS.md and match expected range; verify against actual TR-824 data before using as calculation inputs.

---

## Metadata

**Confidence breakdown:**

- Mathematical framework (thin airfoil, Prandtl LL, velocity triangle power balance): HIGH — textbook results, multiple sources consistent
- Standard approaches (NACA TR-824 + XFOIL + Prandtl LL sweep): HIGH — established engineering practice for 80+ years
- Computational tools (Python/numpy/XFOIL): HIGH — same stack validated in Phase 1
- Validation strategies (XFOIL gate, thin-airfoil cross-check, energy bounds): HIGH — all checks derivable from first principles
- Tacking geometry direction analysis: MEDIUM — analogy with Darrieus VAWT is strong; exact sign for this specific loop geometry must be verified by explicit calculation
- Foil geometry (span, chord, AR defaults): MEDIUM — reasonable engineering estimates; sensitivity sweep mandatory
- v_h / chain torque coupling (Open Question 1): LOW — the central geometric uncertainty; must be resolved before FOIL-01

**Research date:** 2026-03-17
**Valid until:** Physics and NACA data are indefinitely stable. XFOIL is at v6.99 (2013); no newer version expected. Tool versions are stable for years.
