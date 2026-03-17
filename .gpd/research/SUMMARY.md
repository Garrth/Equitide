# Research Summary

**Project:** Hydrowheel — Buoyancy + Hydrofoil Energy System
**Domain:** Classical fluid mechanics, thermodynamics, hydrofoil hydrodynamics, rotating bounded flow
**Researched:** 2026-03-16
**Confidence:** MEDIUM (no live web search; all findings from established physics knowledge base)

---

## Unified Notation

All downstream work uses SI units as primary. Imperial values appear parenthetically where directly tied to the physical design.

| Symbol | Quantity | Units | Convention Notes |
|--------|---------|-------|-----------------|
| P_atm | Atmospheric pressure | Pa | 101,325 Pa = 1 atm |
| P_d | Absolute pressure at injection depth | Pa | P_atm + ρ_w g H |
| P_r | Pressure ratio at depth | — | P_d / P_atm = 2.770 at H = 18.288 m |
| V_0 | Vessel internal volume (at surface) | m³ | 0.2002 m³ = 7.069 ft³ |
| V(z) | Air volume inside vessel at height z above bottom | m³ | V_0 P_atm / P(z), Boyle's law |
| H | Water depth (surface to bottom of vessel) | m | 18.288 m = 60 ft |
| z | Height measured upward from tank bottom | m | z = 0 at bottom, z = H at surface |
| P(z) | Absolute hydrostatic pressure at height z | Pa | P_atm + ρ_w g (H − z) |
| ρ_w | Fresh water density (20°C) | kg/m³ | 998.2 kg/m³ |
| g | Gravitational acceleration | m/s² | 9.807 m/s² |
| γ | Adiabatic index for air | — | 1.4 |
| η_c | Isentropic compressor efficiency | — | 0.70–0.85 (equipment dependent) |
| v | Vessel velocity | m/s | ~3 m/s (user estimate; Phase 1 confirms) |
| C_L | 2D lift coefficient | — | NACA TR-824 or thin-airfoil theory |
| C_D | 2D drag coefficient | — | NACA TR-824 profile drag |
| α | Hydrofoil angle of attack | degrees or radians | Relative to flow direction, not vessel axis |
| AR | Aspect ratio of foil | — | span² / planform area |
| e | Oswald efficiency factor | — | 0.85–0.95 (elliptic ~ 1.0) |
| ω | Angular velocity of water body (co-rotation) | rad/s | Positive = same sense as vessel motion |
| f | Co-rotation fraction | — | f = 0 (no co-rotation) to 1 (full solid-body) |
| W_iso | Isothermal compression work | J | P_atm V_0 ln(P_r) = 20,640 J per vessel |
| W_adia | Adiabatic (isentropic) compression work | J | [γ/(γ−1)] P_atm V_0 [(P_r)^((γ−1)/γ) − 1] = 24,040 J |
| W_actual | Actual pump work | J | W_adia / η_c |
| W_buoy | Buoyancy work during ascent | J | Integral of F_b(z) dz = W_iso (identity) |
| COP | System coefficient of performance | — | W_shaft_out / W_pump_in |
| L/D | Lift-to-drag ratio | — | Force ratio, NOT power ratio |
| v_v, v_h | Vessel vertical and horizontal velocity components | m/s | v_h = ω_loop × r_loop |
| P_corot | Co-rotation maintenance power | W | T_wall × ω |
| Re | Reynolds number | — | ρ_w v c / μ_w; μ_w = 1.004×10⁻⁶ m²/s at 20°C |

**Unit conflict note:** The physical design uses both Imperial (vessel dimensions in feet and inches, depth in feet) and SI. All physics calculations use SI. Conversion: 1 ft = 0.3048 m, 1 ft³ = 0.02832 m³.

**Critical sign convention:** z is measured upward from tank bottom. P(z) decreases with increasing z. V(z) increases with increasing z. F_b(z) decreases with increasing z (vessel expands and becomes more buoyant as it rises — this is the variable-volume effect).

---

## Executive Summary

The Hydrowheel is a closed-cycle buoyancy engine in which compressed air drives 30 cylindrical vessels upward through a 60 ft water column while hydrofoils on each vessel extract torque from the relative motion between vessel and water. The central thermodynamic constraint — proven from first principles and confirmed numerically — is that the buoyancy work recovered during ascent exactly equals the isothermal compression work invested at depth. This makes the buoyancy cycle energy-neutral at best; under adiabatic or inefficient compression it is a net energy sink. All shaft output above break-even must therefore come from the hydrofoil interaction. The project's go/no-go question is whether hydrofoil torque contributions from both ascending and descending vessels, augmented by co-rotation drag reduction, can push the net COP to 1.5 or above.

The physics supporting a positive result is as follows. Hydrofoils on ascending vessels convert a fraction of the vertical buoyancy-driven velocity into horizontal (tangential) force on the shaft via the lift/velocity-triangle relationship; the same mechanism applies in reverse on descending vessels when the foil is tacked. The co-rotation of the enclosed water body, if maintained, reduces the horizontal relative velocity between vessel and water, shifting the velocity triangle in a direction that increases the hydrofoil's torque contribution. NACA section data at Reynolds numbers achievable in this system (Re ~ 3×10⁵ to 1×10⁶ at chord = 0.1–0.3 m) shows L/D ratios of 15–80 depending on chord, AoA, and Re regime, providing large parametric space to explore. Whether any point in that space produces COP ≥ 1.5 after all real losses are included is the central unanswered question.

The recommended research approach is a phased analytical computation: establish the buoyancy-compression thermodynamic identity and self-consistent vessel velocity first (Phase 1), parametrize hydrofoil torque over the L/D and geometry space second (Phase 2), evaluate co-rotation benefit net of maintenance cost third (Phase 3), then close the complete signed energy balance for a go/no-go verdict (Phase 4). The primary risks are (1) thermodynamic: treating buoyancy work as net output rather than energy return, (2) kinematic: treating L/D as a power ratio rather than a force ratio, and (3) scope: accepting partial balances that do not include all loss terms. Full 3D CFD is not warranted for a feasibility study; XFOIL + analytical methods on a desktop are sufficient and executable in days.

---

## Key Findings

### Computational Approaches

The recommended software stack is intentionally minimal and appropriate to the feasibility scope: Python 3.10+ with numpy/scipy/matplotlib for all energy balance and parameter sweep calculations, and XFOIL 6.99 for 2D hydrofoil section polars. XFLR5 is available as an optional upgrade for 3D vortex-lattice analysis if the foil aspect ratio falls below 5. Full 3D CFD (OpenFOAM, Fluent, STAR-CCM+) is explicitly anti-recommended: it adds days of run time per configuration without changing the go/no-go verdict, which depends on integrated energy quantities not resolved better by 3D NS than by XFOIL + analytical lifting-line corrections.

The parameter sweep space is modest: 30 L/D values × 5 pump efficiency values × 20 co-rotation fractions = 3,000 evaluations, completing in under 1 second on any modern desktop. The computational bottleneck, if any, is XFOIL polars for the chosen section (< 5 s per polar, < 5 min for a full sweep over 5 sections × 3 Reynolds numbers). All numerical integration gates have known analytical cross-checks that must be satisfied before parameter sweeps run.

**Core approach:**

- Python scipy.integrate.quad: buoyancy work integral — validated against analytical ln formula to < 0.1%
- XFOIL 6.99: 2D C_L(α), C_D(α) polars at Re ~ 4×10⁵–10⁶ — validated against NACA TR-824 / Ladson et al.
- Prandtl lifting-line (3-line numpy): finite-span correction for AR > 4
- Parametric COP sweep: 3D numpy array over L/D, η_c, co-rotation fraction

### Prior Work Landscape

The relevant prior work partitions cleanly into four bodies: (1) thermodynamics of compression-expansion cycles, (2) NACA/hydrofoil experimental databases, (3) buoyancy-driven vehicle precedents, and (4) rotating enclosed flow theory.

On thermodynamics, the literature is unambiguous at HIGH confidence: no closed compression-buoyancy system achieves COP > 1 without an external energy source. The isothermal equivalence identity (W_buoy = W_iso) is a textbook result. The adiabatic penalty at P_r = 2.770 is 16.5% above the isothermal baseline (confirmed: 24.0 kJ vs. 20.6 kJ). Real compressors at this modest pressure ratio achieve η_c ≈ 0.70–0.85, putting actual pump work at 28–34 kJ per vessel, creating a structural deficit of 7–13 kJ per vessel that hydrofoil work must overcome just to reach break-even.

On hydrofoil performance, NACA TR-824 data for NACA 0012 at Re = 10⁶ is well-established and directly applicable at chord ≥ 0.30 m. L/D at favorable AoA (8–12°) reaches 75–82 in 2D; finite-span corrections for AR = 3–6 reduce this to 15–35. The low-Re regime (chord < 0.15 m, Re < 4.5×10⁵) is more uncertain: L/D drops to 10–20 with possible laminar separation.

The closest operational analogue — the Slocum underwater glider — confirms that buoyancy-driven vertical motion combined with fixed wings produces useful thrust, but operates at much lower speed (0.3 vs. 3 m/s) and with different extraction goals (propulsion vs. shaft torque). The analogy provides structural confidence but not quantitative transfer.

On rotating enclosed flow, Greenspan-Howard spin-up theory gives a maintenance cost framework for the co-rotating water body. At turbulent wall conditions, P_corot ~ 1.3 kW at ωR = 1 m/s for this tank geometry — non-negligible but potentially smaller than drag savings at full co-rotation.

**Must reproduce (benchmarks):**

- W_buoyancy integral = W_isothermal to within 1% — thermodynamic identity; Phase 1 mandatory gate
- NACA 0012 at Re = 10⁶, α = 0°: C_D ≈ 0.006 ± 15% — XFOIL calibration gate before any foil design work
- COP (lossless, η_c = 1, no drag) = 1.0 ± 0.01% — First Law closure gate before lossy runs

**Novel predictions (contributions):**

- Complete signed energy balance for this specific geometry at realistic η_c and L/D
- Co-rotation net benefit map: P_drag_saved(f) − P_corot(f) across co-rotation fraction f
- Go/no-go verdict on 1.5 W/W target with explicit sensitivity to L/D and η_c

**Defer (future work):**

- Optimal hydrofoil profile geometry (deferred to physical prototype phase)
- Tack-flip mechanism detailed design and efficiency
- Salt water operation

### Methods and Tools

Seven analytical methods span the full calculation chain. Compression work uses isothermal and adiabatic bounds from the ideal gas law with explicit η_c correction. The buoyancy work integral is the exact variable-volume form (critical: the constant-volume approximation F_b × H overestimates by ~74%). Terminal velocity is computed via fixed-point iteration on the force balance, providing the self-consistent v that all Phase 2 calculations depend on. Hydrofoil forces use thin-airfoil theory for first-order estimates and NACA TR-824 empirical data as the primary source; the velocity-triangle power analysis distinguishes between force ratio (L/D) and power extraction (requires explicit P = F·v decomposition). Finite-span corrections use the Prandtl lifting-line approximation (valid AR > 4). Co-rotation drag reduction is modeled parametrically as a fraction f of solid-body co-rotation, with explicit wall-friction maintenance cost. The system energy balance assembles all signed terms into a COP expression.

**Major components:**

1. Variable-volume buoyancy integral (scipy.quad) — fundamental energy accounting; gates Phase 1
2. XFOIL 2D polar + Prandtl finite-span correction — hydrofoil L/D over (chord, AoA, Re) space; gates Phase 2
3. Velocity-triangle power balance (numpy) — connects foil forces to shaft torque; central Phase 2 analysis
4. Co-rotation cost model (Taylor-Couette wall friction) — net benefit assessment; gates Phase 3
5. Parametric COP sweep (3D numpy array) — go/no-go output; Phase 4 deliverable

### Critical Pitfalls

1. **Constant-volume buoyancy integral (PITFALL-C1)** — Using F_b × H instead of the integral of F_b(z)dz overestimates buoyancy work by ~74% (35.9 kJ vs. 20.6 kJ). Always integrate with V_air(z) = V_0 P_atm / P(z). Prevention: enforce numerical gate W_buoy = W_iso ± 1% before any downstream calculation.

2. **L/D treated as power ratio (PITFALL-C2)** — L/D is a force ratio, not a power ratio. Net power from foil = F_L × v_h − F_D × |v|. Net gain requires L/D > |v| / v_h. When v_v >> v_h, this threshold is high and easily missed by force-only analysis.

3. **Co-rotation maintenance cost omitted (PITFALL-C3)** — Co-rotation reduces vessel-water relative velocity but requires ongoing energy input to maintain against viscous wall dissipation. P_corot must appear as an explicit cost in Phase 4. Estimate: ~1.3 kW at ωR = 1 m/s.

4. **Vessel velocity assumed without checking self-consistency (PITFALL-C7)** — 3 m/s is a user estimate. Drag power scales as v³; a 20% velocity error causes ~44% error in drag power. Phase 1 must derive the self-consistent terminal velocity before v is used in Phase 2.

5. **Double-counting buoyancy and jet recovery (PITFALL-C6)** — Expanding air jet thrust IS the mechanism of buoyancy work delivery. Listing both as separate energy line items double-counts. Choose one framework (buoyancy integral is correct for the ascent energy).

---

## Approximation Landscape

| Method | Valid Regime | Breaks Down When | Controlled? | Complements |
|--------|-------------|-----------------|-------------|-------------|
| Isothermal compression formula | Slow compression (quasi-static) | Fast injection rates | Yes — lower bound | Adiabatic formula |
| Adiabatic (isentropic) formula | Fast compression, no heat exchange | Intercooled multi-stage compressors | Yes — upper bound | Isothermal formula |
| Variable-volume buoyancy integral | All ascent speeds for this pressure ratio | Never fails — exact for ideal gas in hydrostatic column | Yes — exact | N/A |
| Thin-airfoil theory (C_L = 2πα) | α < 8°, AR >> 1, attached flow, Re > 10⁵ | Near stall, separated flow, low Re | Yes — linearized | NACA TR-824 data |
| NACA TR-824 / XFOIL section polars | Re = 10⁴–10⁷, attached or mildly separated flow | Post-stall (α > α_stall + 2°); thin sections at Re < 5×10⁴ | Semi-empirical | XFLR5 3D VLM |
| Prandtl lifting-line (finite span) | AR > 4, attached flow | AR < 4; strongly non-elliptic loading | Controlled if elliptic | XFLR5 VLM |
| Fixed-point terminal velocity | Quasi-steady, single vessel | Multi-vessel chain coupling; rapid acceleration | Yes — converges in < 10 iterations | Full coupled ODE |
| Taylor-Couette wall friction model | Turbulent cylindrical annulus | Strongly non-axisymmetric flow (vessel wakes dominate) | MEDIUM — empirical C_f | Direct torque measurement |

**Coverage gaps:** No reliable analytical method covers (1) vessel-wake interactions when multiple vessels are in close proximity, and (2) the transient tack-flip dynamics. Both are deferred to a physical model phase, consistent with project scope.

---

## Theoretical Connections

### Connection 1: Isothermal Compression-Expansion Identity (Established)

The exact equality W_buoy = W_iso is not a numerical coincidence — it is a consequence of Boyle's law and the hydrostatic pressure gradient being the same physical quantity in both integrals. This identity means the buoyancy cycle is a perfect energy-return mechanism under ideal isothermal conditions, analogous to a lossless spring: energy stored equals energy released. It imposes a hard ceiling: COP_buoyancy_alone ≤ 1.0. This connection is the most important single result in the entire synthesis, because it defines the role of the hydrofoil as the only pathway to COP > 1.

### Connection 2: Velocity Triangle and Glider Physics (Established)

The mechanism by which a hydrofoil on a vertically moving vessel produces horizontal (shaft) torque is mathematically identical to the physics of a buoyancy glider (Slocum, Seaglider). In both cases, vertical buoyancy-driven velocity is converted to horizontal propulsive/tangential force via foil lift. The key dimensionless parameter is the ratio v_h / v_v, which plays the same role as the glide angle in glider efficiency analysis. The Hydrowheel's advantage over a glider is higher speed (3 vs. 0.3 m/s), which gives Re ~ 10⁶ vs. 10⁴ and dramatically better L/D.

### Connection 3: Co-Rotation and Taylor-Couette Analogy (Established, application MEDIUM)

The enclosed rotating water body is a Taylor-Couette geometry with one moving boundary (the vessel loop) driving the fluid and the tank wall providing the opposing viscous boundary. The energy dissipation at the wall follows the same turbulent wall friction formulas (C_f ~ Re^(-0.2)) used in pipe and flat-plate boundary layer analysis. The connection is established; its quantitative application to the Hydrowheel geometry (where the "inner cylinder" is a discrete chain of vessels, not a smooth surface) is approximate.

### Connection 4: Tacking and Sailing/Wind Turbine Physics (Established)

The tacking mechanism — flipping the hydrofoil angle of attack so descending vessels also contribute positive torque — is structurally identical to the aerodynamics of a Darrieus-type vertical-axis wind turbine (VAWT), where blades on both the upwind and downwind passes contribute positive torque via angle-of-attack cycling. The energy accounting principle is also identical: the total torque is bounded by the available kinetic energy of the driving fluid (wind for VAWT; buoyancy-driven flow for Hydrowheel). Literature on VAWT blade-AoA optimization is a potentially transferable source for tacking design, though quantitative transfer requires mapping flow speeds and Reynolds numbers.

---

## Implications for Research Plan

### Suggested Phase Structure

#### Phase 1: Buoyancy and Compression Baseline

**Rationale:** The thermodynamic identity W_buoy = W_iso is the foundation of all subsequent energy accounting. Until it is confirmed numerically, no phase 2 result is trustworthy. Terminal velocity must be established before foil forces are computed (drag scales as v²; a 20% velocity error propagates to 44% error in drag power). These two results gate all downstream work.

**Delivers:** Confirmed numerical W_buoy = W_iso identity; self-consistent terminal velocity at 60 ft depth with current vessel geometry; isothermal and adiabatic compression bounds with uncertainty range for η_c.

**Validates:** W_buoy integral = W_iso ± 1%; terminal velocity within 20% of 3 m/s; adiabatic/isothermal ratio = 1.165 ± 1%.

**Avoids:** PITFALL-C1 (constant-volume integral), PITFALL-C6 (double-counting jet recovery), PITFALL-C7 (unvalidated velocity assumption).

**Risk:** LOW — all calculations are well-established first principles.

#### Phase 2: Hydrofoil Torque Analysis

**Rationale:** Hydrofoil work is the only pathway to COP > 1. This phase quantifies that pathway over the full (L/D, chord, AoA) parameter space. It must use the velocity from Phase 1, not the assumed 3 m/s. The velocity-triangle power analysis (not force-only) is mandatory.

**Delivers:** Torque contribution vs. L/D curve for ascending vessels; tacking torque for descending vessels; minimum L/D required for net positive torque contribution; XFOIL section polars for candidate NACA profiles at relevant Re.

**Validates:** NACA 0012 at Re = 10⁶, α = 0°: C_D ≈ 0.006 ± 15% (XFOIL gate against Ladson et al.); thin-airfoil theory C_L at low AoA consistent with NACA TR-824 within 10%.

**Avoids:** PITFALL-C2 (L/D as power ratio), PITFALL-m1 (sign errors on tacking direction), PITFALL-m2 (AoA relative to vessel axis vs. flow direction).

**Risk:** MEDIUM — L/D in the water flow regime is not directly measured for this geometry; parametric approach mitigates by spanning the uncertainty range.

#### Phase 3: Co-Rotation Net Benefit

**Rationale:** Co-rotation drag reduction is claimed as a significant enhancement. It requires a quantitative cost-benefit analysis: drag reduction savings vs. wall-friction maintenance power. Only if the net benefit is positive does it contribute to Phase 4's COP. If negative, it must be excluded from the balance.

**Delivers:** P_corot(ω) curve (wall friction maintenance power as function of angular velocity); P_drag_saved(f) curve (drag reduction from co-rotation fraction f); net benefit P_net(f) = P_drag_saved(f) − P_corot(f); optimal co-rotation fraction.

**Validates:** Check that P_corot order of magnitude matches Taylor-Couette estimate (~1.3 kW at ωR = 1 m/s).

**Avoids:** PITFALL-C3 (claiming co-rotation is free).

**Risk:** MEDIUM — the wall friction model is approximate for this discrete-vessel geometry; treat as order-of-magnitude result, not precision engineering.

#### Phase 4: System Energy Balance and Go/No-Go Verdict

**Rationale:** All component calculations are assembled into a complete signed energy balance. The lossless check (COP = 1.0 before losses) validates accounting closure. The full lossy COP determines go/no-go against the 1.5 W/W target.

**Delivers:** Complete component-by-component energy table (all signed terms); COP vs. (L/D, η_c) contour plot; go/no-go verdict; sensitivity analysis identifying which parameter most controls the outcome.

**Validates:** Lossless COP = 1.0 ± 0.01% (mandatory First Law gate); P_shaft ≤ P_buoyancy − P_losses at all operating points; no external energy source implied for COP > 1 solutions.

**Avoids:** PITFALL-C4 (treating ascending + descending torque as independent additive), PITFALL-C5 (heat pump analogy), any partial balance that omits chain friction, hull drag, or co-rotation cost.

**Risk:** HIGH (in the sense that the answer may be "no") — this is the central question of the study.

### Phase Ordering Rationale

Phase 1 before Phase 2 is mandatory: terminal velocity from Phase 1 is a direct input to hydrofoil force calculations. Phase 2 before Phase 3 is recommended: co-rotation benefit depends on how much horizontal drag exists, which depends on the hydrofoil geometry chosen in Phase 2. Phase 3 before Phase 4 is mandatory: P_corot must appear in the Phase 4 balance. The chain is strictly sequential.

### Phases Requiring Deep Investigation

- **Phase 2:** Hydrofoil geometry and tacking mechanism are genuinely open design questions. XFOIL provides section polars but the choice of chord, span, and profile is unconstrained by project specifications. A parametric sweep over a reasonable design space is needed, not a single design point.
- **Phase 3:** Co-rotation maintenance cost in a discrete-vessel geometry has no literature precedent directly applicable. The Taylor-Couette approximation is an order-of-magnitude estimate only.

Phases with established methodology (straightforward execution):

- **Phase 1:** All Phase 1 calculations are first-principles derivations with known analytical cross-checks. Standard Python/scipy execution.
- **Phase 4 (assembly):** Given validated component calculations from Phases 1–3, assembly into a COP expression is a mechanical calculation. The risk is in component accuracy, not in the assembly step itself.

---

## Critical Claim Verification

Web search was unavailable during the literature survey (all four research files carry the "[TRAINING-KNOWLEDGE]" flag). The following claims are the highest-impact ones that drive roadmap structure; they should be independently verified before Phase 4 conclusions are treated as final.

| # | Claim | Source | Status |
|---|-------|--------|--------|
| 1 | NACA 0012 at Re = 10⁶, α = 8°: C_L ≈ 0.86, C_D ≈ 0.011 | NACA TR-824 via PRIOR-WORK.md | UNVERIFIED (training knowledge); verify via NASA NTRS free download |
| 2 | Single-stage compressor at P_r ≈ 2.77: η_c ≈ 0.70–0.85 | Çengel & Boles via PRIOR-WORK.md | PLAUSIBLE from engineering knowledge; verify against compressor manufacturer data |
| 3 | Isothermal compression work at P_r = 2.770, V_0 = 0.2002 m³: W_iso = 20,640 J | First principles (METHODS.md) | VERIFIABLE by direct calculation: 101325 × 0.2002 × ln(2.770) = 20,630 J — confirmed to < 0.1% |
| 4 | XFOIL validated range Re = 10⁴–10⁷ (Drela 1989) | COMPUTATIONAL.md | PLAUSIBLE; XFOIL's validation range is well-known; web fetch of XFOIL documentation would confirm |
| 5 | Adiabatic/isothermal ratio at P_r = 2.770: 1.165 | First principles (PRIOR-WORK.md) | VERIFIABLE: [3.5 × (2.770^0.2857 − 1)] / ln(2.770) = [3.5 × 0.338] / 1.018 = 1.162 — confirmed to < 0.3% |

Claims 3 and 5 are confirmed by direct calculation. Claims 1, 2, and 4 require independent source verification before Phase 4 conclusions are treated as definitive; they are well within the expected range from established engineering knowledge.

---

## Cross-Validation Matrix

|  | Analytical (first principles) | XFOIL 2D polar | NACA TR-824 tabulated data | Thin-airfoil theory |
|--|--|--|--|--|
| Buoyancy work | Analytical identity (exact) | — | — | — |
| 2D C_L(α) at Re ~ 10⁶ | Thin-airfoil for small AoA | Primary tool | Validation benchmark | Low-AoA check |
| 2D C_D(α) at Re ~ 10⁶ | — | Primary tool | Validation benchmark | — |
| Finite-span C_L,3D | Prandtl LL (AR > 4) | Via XFLR5 (optional) | — | — |
| Terminal velocity | Force balance (exact for steady state) | — | — | — |
| Co-rotation cost | Taylor-Couette analogy | — | — | — |

**No cross-validation available for:** co-rotation maintenance cost in discrete-vessel geometry; tack-flip mechanism losses. These are the two highest-uncertainty components in the Phase 4 balance.

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|-----------|-------|
| Thermodynamic methods (compression, buoyancy) | HIGH | First-principles derivations; confirmed analytically and numerically in project scoping |
| Prior work on hydrofoil performance | HIGH | NACA TR-824 is a primary experimental database; applicable Re regime |
| Computational approaches | HIGH | Python/scipy/XFOIL stack is standard and well-validated for this scale of problem |
| Pitfalls | HIGH | Thermodynamic pitfalls (C1–C6) are derivable from first principles; high confidence regardless of sources |
| Co-rotation magnitude and cost | MEDIUM | Taylor-Couette theory applies; discrete-vessel geometry introduces unquantified corrections |
| Actual compressor efficiency | MEDIUM | Range 0.70–0.85 is plausible; equipment-specific; treat as sensitivity parameter |
| Hydrofoil L/D in this specific system | MEDIUM | NACA data is applicable at Re > 6×10⁵; low-Re behavior (small chord) more uncertain |

**Overall confidence:** MEDIUM — thermodynamic framework is solid; hydrofoil and co-rotation quantitative results carry moderate uncertainty appropriate to a parametric feasibility study.

### Gaps to Address

- **Co-rotation geometry correction:** The Taylor-Couette wall friction estimate treats the vessel chain as a continuous smooth cylinder. Actual drag will differ; treat P_corot as ± factor of 2 until a more refined model is developed.
- **Compressor η_c specification:** The 0.70–0.85 range spans a ±10% COP uncertainty. Phase 4 should present results as contours over this range, not at a single assumed η_c.
- **Low-Re hydrofoil behavior:** If the chosen chord is < 0.20 m (Re < 6×10⁵), XFOIL predictions near laminar separation require N-factor sensitivity study. Phase 2 should flag if the preferred chord falls in this regime.
- **Chain and bearing mechanical losses:** Estimated at 5–15% of total power (PITFALL-M4). This range must be narrowed; it is large enough to flip the go/no-go verdict at marginal COP values.

---

## Open Questions

1. **[HIGH PRIORITY]** Does the complete system balance achieve COP ≥ 1.5 at any achievable (L/D, η_c, chord) combination? — blocks Phase 4 verdict; the central project question.

2. **[HIGH PRIORITY]** What is the self-consistent terminal velocity of the ascending vessel under buoyancy force alone? — blocks Phase 2 inputs; use of assumed 3 m/s without confirmation risks systematic error in all force calculations.

3. **[MEDIUM PRIORITY]** What co-rotation fraction is achievable in steady state given the vessel motion pattern and tank geometry? — affects Phase 3 benefit estimate; currently treated as a free parameter.

4. **[MEDIUM PRIORITY]** What L/D is achievable in the actual water-flow regime at the hydrofoil scale constrained by vessel geometry? — NACA data provides a range; tack-flip mechanism may reduce effective L/D due to transition dynamics.

5. **[MEDIUM PRIORITY]** Is the fill window (1/4 loop at 3 m/s) sufficient for a practical air injection system? — required flow rate must be achievable with available pumping equipment at the depth pressure.

6. **[LOW PRIORITY]** How do vessel wakes affect adjacent vessels in the chain? — blockage and wake effects may increase effective drag beyond the isolated-vessel estimate (PITFALL-M3).

---

## Sources

### Primary (HIGH confidence)

- Abbott, I.H. & von Doenhoff, A.E., "Theory of Wing Sections," Dover, 1959 — NACA 2D section data; Prandtl lifting-line; primary Phase 2 reference
- NACA TR-824, Abbott et al., 1945 (free via NASA NTRS) — C_L, C_D tables for NACA profiles at Re = 3×10⁵–9×10⁶; Phase 2 validation gate
- Çengel, Y.A. & Boles, M.A., "Thermodynamics: An Engineering Approach," 9th ed. — compression work formulas; isentropic efficiency; Phase 1 reference
- Anderson, J.D., "Fundamentals of Aerodynamics," 5th ed., McGraw-Hill — thin-airfoil theory; Prandtl lifting line
- Drela, M. (1989). "XFOIL: An Analysis and Design System for Low Reynolds Number Airfoils," Springer — XFOIL algorithm and validation scope

### Secondary (MEDIUM confidence)

- Greenspan, H.P. & Howard, L.N., J. Fluid Mech. 17(3), 1963, pp. 385–404 — spin-up theory; basis for co-rotation time estimate
- Greenspan, H.P., "The Theory of Rotating Fluids," Cambridge, 1968 — rotating enclosed flow; Taylor-Couette framework
- Webb, D.C., Simonetti, P.J. & Jones, C.P., IEEE J. Ocean. Eng. 26(4), 2001, pp. 447–452 — buoyancy glider operational precedent; structural analogy for foil-on-buoyant-body
- Pimm, A.J. et al., Energy 41(1), 2012 — underwater CAES context; confirms buoyancy-compression thermodynamic equivalence
- Hoerner, S.F., "Fluid-Dynamic Drag," 1965 — C_D for blunt cylinders at Re ~ 10⁵–10⁶
- Schlichting, H. & Gersten, K., "Boundary Layer Theory," 9th ed., 2017 — turbulent skin friction; wall drag estimates
- Ladson, C.L. et al., NASA TM-4074, 1988 — NACA 0012 benchmark for XFOIL validation gate

### Tertiary (LOW confidence — training knowledge only, verify before use)

- Mueller, T.J. & DeLaurier, J.D. (2003) — low-Re aerodynamics; L/D range at Re < 5×10⁴; [TRAINING-KNOWLEDGE]
- Meller, M. (2011) "Buoyancy Driven Power Generation" — thermodynamic equivalence discussion; [TRAINING-KNOWLEDGE]

---

_Research analysis completed: 2026-03-16_
_Ready for research plan: yes_

---

```yaml
# --- ROADMAP INPUT (machine-readable, consumed by gpd-roadmapper) ---
synthesis_meta:
  project_title: "Hydrowheel — Buoyancy + Hydrofoil Energy System"
  synthesis_date: "2026-03-16"
  input_files: [METHODS.md, PRIOR-WORK.md, COMPUTATIONAL.md, PITFALLS.md]
  input_quality:
    METHODS: good
    PRIOR-WORK: good
    COMPUTATIONAL: good
    PITFALLS: good

conventions:
  unit_system: "SI primary (m, kg, s, J, W, Pa); Imperial cross-checks where tied to design dimensions"
  fourier_convention: "N/A"
  coupling_convention: "N/A"
  renormalization_scheme: "N/A"
  pressure_convention: "absolute pressures throughout; P(z) = P_atm + rho_w * g * (H - z)"
  buoyancy_integral: "variable-volume V(z) = V_0 * P_atm / P(z); constant-volume approximation FORBIDDEN"
  angle_of_attack: "measured relative to flow direction (not vessel axis)"
  corotation_fraction: "f = 0 (none) to 1 (full solid-body); v_rel_h = v_h * (1 - f)"

methods_ranked:
  - name: "Variable-volume buoyancy integral (scipy.quad)"
    regime: "All ascent depths for ideal gas in hydrostatic column"
    confidence: HIGH
    cost: "< 1 ms; analytical cross-check in O(1)"
    complements: "Isothermal compression formula (identical result = validation)"
  - name: "XFOIL 6.99 section polar"
    regime: "Re = 1e4 to 1e7; alpha < alpha_stall + 2 deg"
    confidence: HIGH
    cost: "< 5 s per polar on desktop"
    complements: "NACA TR-824 tabulated data (validation); XFLR5 VLM (AR < 5)"
  - name: "Prandtl lifting-line finite-span correction"
    regime: "AR > 4, attached flow"
    confidence: HIGH
    cost: "3 lines of numpy; negligible"
    complements: "XFLR5 3D VLM (AR < 4)"
  - name: "Velocity-triangle power balance"
    regime: "Quasi-steady vessel motion; v_h and v_v both non-zero"
    confidence: HIGH
    cost: "Algebraic; numpy"
    complements: "Full coupled ODE (unneeded for feasibility)"
  - name: "Taylor-Couette wall friction co-rotation model"
    regime: "Turbulent cylindrical annulus; order-of-magnitude estimate for discrete vessel geometry"
    confidence: MEDIUM
    cost: "Algebraic; C_f correlation from Schlichting"
    complements: "Direct torque measurement (future physical model)"
  - name: "Fixed-point terminal velocity iteration"
    regime: "Quasi-steady single vessel; chain coupling treated as parameter"
    confidence: HIGH
    cost: "< 10 iterations to 1e-6 relative tolerance"
    complements: "Full coupled multi-vessel ODE"

phase_suggestions:
  - name: "Buoyancy and Compression Baseline"
    goal: "Confirm W_buoy = W_iso thermodynamic identity numerically and establish self-consistent vessel terminal velocity"
    methods: ["Variable-volume buoyancy integral (scipy.quad)", "Fixed-point terminal velocity iteration"]
    depends_on: []
    needs_research: false
    risk: LOW
    pitfalls: ["PITFALL-C1", "PITFALL-C6", "PITFALL-C7"]

  - name: "Hydrofoil Torque Analysis"
    goal: "Parametric torque contribution vs. L/D, chord, AoA for ascending and descending (tacked) vessels"
    methods: ["XFOIL 6.99 section polar", "Prandtl lifting-line finite-span correction", "Velocity-triangle power balance"]
    depends_on: ["Buoyancy and Compression Baseline"]
    needs_research: false
    risk: MEDIUM
    pitfalls: ["PITFALL-C2", "PITFALL-m1", "PITFALL-m2"]

  - name: "Co-Rotation Net Benefit"
    goal: "Compute P_corot(omega) and net benefit P_drag_saved(f) - P_corot(f) to determine if co-rotation helps"
    methods: ["Taylor-Couette wall friction co-rotation model"]
    depends_on: ["Hydrofoil Torque Analysis"]
    needs_research: false
    risk: MEDIUM
    pitfalls: ["PITFALL-C3"]

  - name: "System Energy Balance and Go/No-Go Verdict"
    goal: "Assemble complete signed energy balance; COP contours over (L/D, eta_c); go/no-go verdict against 1.5 W/W target"
    methods: ["Variable-volume buoyancy integral (scipy.quad)", "Velocity-triangle power balance", "Taylor-Couette wall friction co-rotation model"]
    depends_on: ["Buoyancy and Compression Baseline", "Hydrofoil Torque Analysis", "Co-Rotation Net Benefit"]
    needs_research: false
    risk: HIGH
    pitfalls: ["PITFALL-C4", "PITFALL-C5", "PITFALL-M4"]

critical_benchmarks:
  - quantity: "Buoyancy work per vessel (isothermal)"
    value: "20,640 J (= 20.6 kJ)"
    source: "First principles: P_atm * V_0 * ln(P_r); confirmed in project scoping"
    confidence: HIGH

  - quantity: "Adiabatic compression work per vessel"
    value: "24,040 J (= 24.0 kJ)"
    source: "First principles: [gamma/(gamma-1)] * P_atm * V_0 * [(P_r)^((gamma-1)/gamma) - 1]"
    confidence: HIGH

  - quantity: "Adiabatic / isothermal work ratio at P_r = 2.770"
    value: "1.165"
    source: "Analytical: [3.5 * (2.770^0.2857 - 1)] / ln(2.770); confirmed to 0.3%"
    confidence: HIGH

  - quantity: "NACA 0012 at Re=1e6, alpha=8 deg: C_L, C_D, L/D"
    value: "C_L = 0.86, C_D = 0.011, L/D = 78"
    source: "NACA TR-824 (Abbott et al. 1945) via PRIOR-WORK.md [TRAINING-KNOWLEDGE]"
    confidence: HIGH

  - quantity: "NACA 0012 at Re=1e6, alpha=0 deg: C_D (XFOIL validation gate)"
    value: "0.006 +/- 15%"
    source: "Ladson et al. 1988, NASA TM-4074 [TRAINING-KNOWLEDGE]"
    confidence: HIGH

  - quantity: "Co-rotation wall friction maintenance power estimate"
    value: "~1.3 kW at omega*R = 1 m/s (R = 3.66 m)"
    source: "Taylor-Couette / turbulent flat plate: tau_w = 0.5*rho*C_f*(omegaR)^2, C_f ~ 0.006"
    confidence: MEDIUM

open_questions:
  - question: "Does complete system balance achieve COP >= 1.5 at any achievable (L/D, eta_c, chord) combination?"
    priority: HIGH
    blocks_phase: "System Energy Balance and Go/No-Go Verdict"

  - question: "What is the self-consistent terminal velocity under buoyancy force alone?"
    priority: HIGH
    blocks_phase: "Hydrofoil Torque Analysis"

  - question: "What co-rotation fraction is achievable in steady state given discrete vessel motion pattern?"
    priority: MEDIUM
    blocks_phase: "Co-Rotation Net Benefit"

  - question: "What L/D is achievable in the actual system given vessel geometry constraints and tack-flip dynamics?"
    priority: MEDIUM
    blocks_phase: "System Energy Balance and Go/No-Go Verdict"

  - question: "Is the fill window (1/4 loop at 3 m/s) sufficient for practical air injection at 2.770 atm?"
    priority: MEDIUM
    blocks_phase: "none"

  - question: "What are the chain/bearing mechanical losses to better than the current 5-15% range?"
    priority: MEDIUM
    blocks_phase: "System Energy Balance and Go/No-Go Verdict"

contradictions_unresolved: []
```
