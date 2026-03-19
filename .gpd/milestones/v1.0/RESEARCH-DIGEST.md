# Research Digest: v1.0 Feasibility Study

Generated: 2026-03-19
Milestone: v1.0
Phases: 1–4

## Narrative Arc

The study set out to determine whether a buoyancy + hydrofoil engine could achieve COP ≥ 1.5
(1.5 W shaft output per 1 W pumping input) by combining four energy mechanisms: buoyancy work,
dual-direction hydrofoil torque, co-rotation drag reduction, and jet recovery. Phase 1
established the thermodynamic foundation — pumping energy bounds (W_iso = 20,644.6 J,
W_adia = 23,959.5 J per vessel cycle) and confirmed via the buoyancy integral identity that
buoyancy alone cannot exceed COP = 0.73; the hydrofoil must contribute. Phase 2 showed that
the rotating-arm NACA 0012 configuration produces positive tangential force on both ascending
and descending vessels (tacking geometry verified by vector analysis), giving COP_partial = 2.06
at the design tip-speed ratio λ = 0.9 — but also flagged a critical coupling: the vertical foil
force F_vert = −663.9 N (downward) is 115% of the mean buoyancy force, meaning the Phase 1
terminal velocity is an upper bound requiring a self-consistent correction. Phase 3 confirmed
that co-rotation of the water body eliminates 46.8 kW of drag at a maintenance cost of only
720 W, and proved geometrically that vertical relative velocity (and thus lift) is preserved
for all co-rotation fractions. Phase 4 closed the loop: the coupled (v_loop, ω) solution
via brentq iteration gives v_loop = 2.384 m/s — 36% below the Phase 1 upper bound — and because
co-rotation drag savings scale as v³, they collapse by a factor of 0.264, driving
COP_nominal to 0.925. Across all nine sensitivity scenarios (η_c = 0.65–0.85, losses
5–15%), the corrected COP range is [0.811, 1.186], with only the most optimistic case (η_c =
0.85, 5% loss) approaching 1.2. The verdict is NO_GO under the current foil orientation.
The decisive design path identified is reversed foil mounting, which would make F_vert upward
— assisting buoyancy, increasing v_loop, and restoring co-rotation savings.

## Key Results

| Phase | Result | Value | Validity Range | Confidence |
|-------|--------|-------|----------------|------------|
| 1 | Isothermal compression work | W_iso = 20,644.6 J/cycle | Ideal gas, 60 ft, P_r = 2.7669 | High |
| 1 | Adiabatic compression bound | W_adia = 23,959.5 J/cycle | γ = 1.4, same conditions | High |
| 1 | Terminal velocity (nominal) | v_nominal = 3.714 m/s | C_D = 1.0, F_chain = 0 | Medium |
| 1 | Fill feasibility | GO — 274 SCFM at 26 psig | v_nominal; medium industrial compressor | High |
| 1 | COP ceiling (buoyancy only) | COP_ideal_max = 0.560–0.732 | η_c = 0.65–0.85 | High |
| 2 | Design tip-speed ratio | λ = 0.9 (ω = 0.913 rad/s, 8.72 RPM) | Fixed mount angle 38° | High |
| 2 | Combined COP (partial, upper bound) | COP_partial = 2.057 at λ = 0.9 | 24 vessels, pre-F_vert correction | Medium (upper bound) |
| 2 | F_vert coupling flag | F_vert/F_b_avg = 1.15 >> 0.20 | All λ near design point | High |
| 3 | Co-rotation operating point | f_stall = 0.294, P_net = 46.8 kW saved | Smooth-cylinder stall limit | Medium |
| 3 | Lift preservation | v_rel_vertical = v_loop (exact) for all f | Geometric proof | High |
| 4 | Corrected vessel velocity | v_loop = 2.384 m/s | Self-consistent brentq solution | High |
| 4 | System COP (corrected) | COP_nominal = 0.925 | η_c = 0.70, loss = 10% | High |
| 4 | Full sensitivity range | COP ∈ [0.811, 1.186] | 9 scenarios | High |
| 4 | Verdict | **NO_GO** — COP < 1.5 in all scenarios | Current foil orientation | High |

## Methods Employed

- **Phase 1:** Closed-form isothermal work: W_iso = P_atm · V_surface · ln(P_r)
- **Phase 1:** Closed-form adiabatic work: W_adia = [γ/(γ−1)] · P_atm · V_surface · (P_r^((γ−1)/γ) − 1)
- **Phase 1:** scipy.integrate.quad buoyancy identity gate — |W_buoy − W_iso|/W_iso < 1% (two tolerances)
- **Phase 1:** Terminal velocity force balance: v_t = √(2·(F_b_avg − F_chain)/(ρ_w · C_D · A_frontal))
- **Phase 1:** Fill window and SCFM analysis with Boyle's law mass equivalence
- **Phase 2:** Rotating-arm velocity triangle (λ formulation); NACA 0012 polar (TR-824)
- **Phase 2:** Prandtl lifting-line 3D correction: C_L_3D = C_L_2D/(1 + 2/AR); C_D_i = C_L_3D²/(π·e·AR)
- **Phase 2:** Explicit tacking vector geometry (not symmetry assumption); Darrieus VAWT analogy confirmed
- **Phase 2:** λ sweep parameterization over [0.3, 5.0]
- **Phase 3:** Self-consistent angular momentum balance via brentq root-finding
- **Phase 3:** Prandtl 1/5-power turbulent wall friction (Schlichting §21.2) for P_corot
- **Phase 3:** Cubic drag saving formula: P_drag_saved = P_drag_full · [1 − (1 − f)³]
- **Phase 3:** P_net(f) parametric sweep (200 points) with ±50% P_corot uncertainty bracketing
- **Phase 3:** Kinematic velocity decomposition for lift preservation (geometric proof)
- **Phase 4:** Fixed-point and brentq iteration for coupled (v_loop, ω) solution
- **Phase 4:** Co-rotation velocity correction: scale = (v_loop_corr/v_loop_nom)³
- **Phase 4:** Dual COP table (uncorrected + corrected); lossless gate diagnostic with alternative buoy-iso gate
- **Phase 4:** Sensitivity slices over η_c, loss_fraction, and f_corot (9 scenarios)

## Convention Evolution

| Phase | Convention | Description | Status |
|-------|-----------|-------------|--------|
| Phase 1 | Coordinate system | z = 0 at tank bottom, z = H = 18.288 m at surface | Active |
| Phase 1 | Unit system | SI primary (m, kg, s, N, J, W, Pa); Imperial in parentheses | Active |
| Phase 1 | Buoyancy integral rule | Always integrate F_b(z) = ρ_w·g·V_surface·P_atm/P(z); never constant-volume | Active |
| Phase 1 | Energy sign convention | W_pump = denominator; W_buoy, W_foil = numerator; losses subtracted | Active |
| Phase 1 | Precise vs. rounded | P_r = 2.7669 (precise, used in code); 2.770 in CONVENTIONS.md (display only) | Active |
| Phase 2 | Hydrofoil force convention | L, D from 3D-corrected NACA polars; v_rel = vessel velocity relative to water | Active |
| Phase 2 | Force sign convention | F_b positive upward; F_vert positive = upward (assist buoyancy) | Active |
| Phase 2 | COP partial label | COP_partial required everywhere; no bare COP without qualifier | Active |
| Phase 3 | Co-rotation convention | v_rel_h = v_h·(1 − f); v_rel_v = v_v unchanged; f ∈ [0, 1] | Active |
| Phase 4 | COP formula (final) | COP = (W_buoy + W_foil_asc + W_foil_desc − W_drag − W_corot − W_friction) / W_pump | Active |

## Figures and Data Registry

| File | Phase | Description | Paper-ready? |
|------|-------|-------------|--------------|
| analysis/phase1/outputs/plots/P1-1_profiles.png | 1 | P(z), V(z), F_b(z) vs z — monotone profiles | No |
| analysis/phase1/outputs/plots/P1-4_pump_energy.png | 1 | W_pump vs η_c with COP_ideal_max right axis | No |
| analysis/phase1/outputs/thrm01_compression_work.json | 1 | W_iso, W_adia, W_pump table, fill volumes, COP ceiling | — |
| analysis/phase1/outputs/buoy01_force_profile.json | 1 | F_b(z) at 5 heights, F_b_avg | — |
| analysis/phase1/outputs/phase1_summary_table.json | 1 | All 9 Phase 1 requirements, Phase 2 handoff values | — |
| docs/phase1_results.md | 1 | Human-readable Phase 1 summary | No |
| analysis/phase2/outputs/foil01_force_sweep.json | 2 | NACA 0012 F_tan, F_vert, COP_partial vs λ sweep | — |
| analysis/phase2/outputs/phase2_summary_table.json | 2 | All 4 Phase 2 requirements, Phase 3/4 handoff | — |
| docs/phase2_results.md | 2 | Human-readable Phase 2 summary | No |
| analysis/phase3/outputs/corot01_angular_momentum_model.json | 3 | f_ss, f_stall, P_corot, spin-up time | — |
| analysis/phase3/outputs/corot03_lift_preservation.json | 3 | Geometric lift preservation proof | — |
| analysis/phase3/outputs/phase3_summary_table.json | 3 | All COROT requirements, Phase 4 inputs | — |
| docs/phase3_results.md | 3 | Human-readable Phase 3 summary | No |
| analysis/phase4/outputs/sys02_energy_balance.json | 4 | Full signed energy balance, uncorrected COP table | — |
| analysis/phase4/outputs/sys03_sensitivity_verdict.json | 4 | Corrected COP table (9 scenarios), sensitivity slices, verdict | — |
| analysis/phase4/outputs/phase4_summary_table.json | 4 | Complete Phase 4 archive, all SYS requirements | — |
| docs/phase4_results.md | 4 | Human-readable Phase 4 summary with component table | No |

## Open Questions

1. At what foil angle of attack does F_vert = 0 (neutral vertical force), and what is the resulting COP at that operating point?
2. Is there an AoA where F_vert is slightly upward-assisting while maintaining meaningful horizontal torque, and does that operating point achieve COP ≥ 1.5?
3. What is the chain coupling force F_chain in practice? (affects v_terminal baseline)
4. Final loop geometry (needed for precise fill window duration)
5. Co-rotation achievement mechanism in practice (startup procedure, energy cost during transient)

## Dependency Graph

    Phase 1 "Air, Buoyancy & Fill"
      provides: W_iso, W_adia, W_pump table, v_nominal, v_range, fill GO verdict
      requires: (none — first phase)
    → Phase 2 "Hydrofoil & Torque"
      provides: COP_partial = 2.057 (upper bound), F_vert flag, λ_design = 0.9, λ_max = 1.2748
      requires: v_vessel range from Phase 1, W_pump table
    → Phase 3 "Co-rotation"
      provides: f_stall = 0.294, P_net = 46.8 kW, lift preservation proof
      requires: ω_design from Phase 2, hydrofoil drag values, F_vert flag
    → Phase 4 "System Energy Balance"
      provides: v_loop_corrected = 2.384 m/s, COP_nominal = 0.925, NO_GO verdict
      requires: All Phase 1–3 results; coupled (v_loop, ω) solution mandatory

## Mapping to Original Objectives

| Requirement | Status | Fulfilled by | Key Result |
|-------------|--------|-------------|------------|
| THRM-01: Pumping energy bounds | Complete | Phase 1 Plan 01 | W_iso=20,644.6 J, W_adia=23,959.5 J |
| THRM-02: Fill volumes | Complete | Phase 1 Plan 01 | V_depth=0.07236 m³, V_surface=0.2002 m³ |
| THRM-03: Jet recovery | Complete | Phase 1 Plan 01 | W_jet = 0 (contained in W_buoy; no separate term) |
| BUOY-01: Buoyancy force profile | Complete | Phase 1 Plan 01 | F_b(z): 708.3 N → 1959.8 N; monotone |
| BUOY-02: Buoyancy work identity | Complete | Phase 1 Plan 02 | |W_buoy − W_iso|/W_iso = 2×10⁻⁷%; gate PASSED |
| BUOY-03: Terminal velocity | Complete | Phase 1 Plan 02 | v_nominal = 3.714 m/s; 3 m/s is conservative |
| FILL-01: Fill window duration | Complete | Phase 1 Plan 03 | t_fill = 1.548 s at nominal; arc = 5.749 m |
| FILL-02: Required flow rate | Complete | Phase 1 Plan 03 | 274 SCFM at 26 psig (nominal) |
| FILL-03: Fill feasibility | Complete | Phase 1 Plan 03 | GO — medium industrial compressor sufficient |
| FOIL-01: Lift/drag forces | Complete | Phase 2 Plan 01 | NACA 0012; F_tan > 0 for λ ∈ [0.3, 1.27] |
| FOIL-02: Ascending torque | Complete | Phase 2 Plan 01 | W_foil_asc = 20,767 J/vessel at λ = 1 |
| FOIL-03: Descending tacking | Complete | Phase 2 Plan 02 | F_tan_desc = 1135.5 N; same direction confirmed |
| FOIL-04: Minimum L/D | Complete | Phase 2 Plan 02 | λ_min = 0.9 for COP ≥ 1.5 (pre-correction) |
| COROT-01: Co-rotation model | Complete | Phase 3 Plan 01 | f_stall = 0.294, f_ss_upper = 0.635 |
| COROT-02: Drag reduction | Complete | Phase 3 Plan 02 | P_drag_saved = 47.5 kW at f_stall |
| COROT-03: Lift preservation | Complete | Phase 3 Plan 01 | v_rel_vertical = v_loop for all f (geometric proof) |
| SYS-01: Complete energy balance | Complete | Phase 4 Plan 01 | All components; v_loop = 2.384 m/s (corrected) |
| SYS-02: Energy ratio | Complete | Phase 4 Plan 01 | COP_nominal = 0.925; uncorrected = 1.39 |
| SYS-03: Go/no-go verdict | Complete | Phase 4 Plan 02 | **NO_GO** — COP ∈ [0.811, 1.186], all < 1.5 |
