# Research State

## Project Reference

See: .gpd/PROJECT.md (updated 2026-03-21)

**Core research question:** Can this buoyancy + hydrofoil engine produce at least 1.5W of shaft power for every 1W of air pumping input?
**Current focus:** v1.2 milestone — Purge Thrust and Tail Foil Quantification; Phase 7 is the next execution target

## Current Position

**Current Phase:** 7
**Current Phase Name:** Purge Thrust and Tail Foil Derivation
**Total Phases:** 8 (v1.2 milestone)
**Current Plan:** 0 (not yet started)
**Total Plans in Phase:** TBD
**Status:** Roadmap complete — ready for Phase 7 planning
**Last Activity:** 2026-03-21
**Last Activity Description:** v1.2 roadmap created — Phase 7 (derivation + VALD-01 gate) and Phase 8 (revised verdict) defined; REQUIREMENTS.md traceability confirmed 9/9 objectives mapped

**Progress (v1.2):** [░░░░░░░░░░] 0%

## Active Calculations

None — Phase 7 not yet started.

## Intermediate Results

### Phase 1 Locked Values (authoritative — use JSON files for exact values)

- W_iso = 20,644.6 J (isothermal compression lower bound)
- W_adia = 23,959.5 J (adiabatic upper bound; CONVENTIONS.md shows 24,040 J — documentation rounding)
- W_pump range = 28,188–36,861 J (for η_c = 0.85–0.65)
- W_pump at η_c = 0.70: 34,228 J (nominal reference)
- COP_ideal_max (buoyancy alone): 0.56–0.73 for all η_c — BELOW 1.0; hydrofoil required
- W_buoy = W_iso = 20,644.6 J (identity confirmed to 2×10⁻⁵%; mandatory gate PASSED)
- V_depth = 0.07236 m³; V_surface = 0.2002 m³; P_r = 2.7669
- F_b(z=0) = 708.3 N; F_b(z=H) = 1959.8 N; F_b_avg = 1128.9 N
- v_terminal nominal = 3.714 m/s (C_D=1.0, F_chain=0)
- v_terminal conservative = 3.075 m/s (C_D=1.2, F_chain=200N)
- v_terminal range = [2.53, 4.15] m/s (full C_D × F_chain envelope)
- t_fill at nominal = 1.548 s; arc_length = 5.749 m
- Q_free at nominal = 274 SCFM; range 147–295 SCFM over [2.0, 4.0] m/s
- Fill feasibility: **GO** — 26 psig delivery pressure, medium industrial rotary screw compressor
- Re range at terminal velocity: [1.15×10⁶, 1.89×10⁶] — Hoerner C_D = 0.8–1.2 regime confirmed

### Phase 2 Inputs (from Phase 1)

- v_vessel: use 3.714 m/s nominal, 3.075 m/s conservative; sweep [2.53, 4.15] m/s
- W_pump per cycle: see analysis/phase1/outputs/thrm01_compression_work.json
- F_b(z) function: verified; P(z) = P_atm + rho_w*g*(H-z); V(z) = V_surface*P_atm/P(z)
- W_foil_net required for COP=1.5 at η_c=0.70: ≥ 30,697 J per cycle (= 1.5 × 34,228 − 20,645)

### Phase 2 Locked Values (authoritative — use JSON files for exact values)

- v_loop = 3.7137 m/s (from Phase 1 JSON; never hardcoded)
- (L/D)_min = cot(β) = λ (algebraically correct; CONTEXT.md √(1+1/λ²) is kinematic ratio, not force threshold)
- mount_angle = 38° at λ=1, AoA_target=7°; F_tan > 0 for λ ∈ [0.3, 1.27] with fixed mount
- Tacking sign CONFIRMED: explicit rotating-arm vector geometry; F_tan_D = L·sin(β) − D·cos(β) > 0 at position D
- Darrieus VAWT analogy CONFIRMED: C_T identical formula, both passes positive
- F_tan at λ=1: 1135.5 N (ascending = descending, exact symmetry); shaft torque = 4156 N·m
- W_foil_ascending per vessel at λ=1: 20,767 J; W_foil_descending per vessel: 20,766 J
- COP_partial (24 vessels, λ=0.9): **2.057** — design operating point
- COP_partial_nominal (λ=1): 1.817
- lambda_min for COP ≥ 1.5 (OK, non-stall): λ = 0.9 → ω = 0.913 rad/s = 8.72 RPM
- **FLAG: F_vert/F_b_avg = 1.15 at λ=1** >> 0.20 — all Phase 2 COP are upper bounds; Phase 4 coupled solution mandatory
- Phase 2 feasibility verdict: **GREEN** — proceed to Phase 3
- Phase 1 anchor PASS: COP(W_foil=0) = 0.6032 (error 4.65×10⁻⁵)

## Open Questions

- Is W_jet_thrust genuinely additive to W_buoy (i.e., is the purge jet force outside the Archimedes integral), or is it a restatement of work already counted in W_iso? (v1.2 primary physics question — VALD-01 gate)
- What is the first-principles magnitude of W_jet_thrust, and does it approach the ~20% upward force user estimate?
- What chord length maximizes W_tail_foil while remaining physically feasible for the vessel geometry?
- What is the COP margin above 1.0 with both contributions included, across all 9 scenarios?

### Phase 3 Locked Values (authoritative — use phase3_summary_table.json for exact values)

- phase3_verdict = **net_positive** (robust across ±50% P_corot uncertainty)
- f_stall = 0.294003 = 1 − 0.9/1.2748 (stall-limited operating boundary)
- f_ss_upper_bound = 0.635 (smooth-cylinder; actual f_ss ~0.3 after discrete-vessel correction)
- P_corot at f_stall = 720 W; P_corot_range = [360, 1440] W (±50% C_f)
- P_drag_saved at f_stall = 47,546 W; P_net = 46,826 W (co-rotation benefit dominates by ~65×)
- P_net_range at f_stall = [46,105, 47,186] W — robust net_positive across all uncertainty cases
- COP_corot at f_stall = 0.603 (foil near stall; COP decreases as lambda_eff → lambda_max)
- COP_partial Phase 2 = 2.057 (f=0 anchor PASS to 4 decimal places)
- F_vert_flag_propagated = true (F_vert/F_b_avg=1.15 >> 0.20; Phase 4 coupled solution mandatory)
- All three COROT requirements satisfied: COROT-01, COROT-02, COROT-03

### Phase 3 Intermediate Values (from Plan 01)

- f_ss_upper_bound = 0.635 (smooth-cylinder upper bound — overestimates by ~2× vs discrete-vessel geometry)
- f_eff = 0.294 (stall-limited: f_stall = 1 − 0.9/1.2748)
- f_stall = 0.294003 (consistent between corot01 and corot03 JSONs)
- P_corot_nominal = 22.19 kW; P_corot_range = [11.1, 44.4] kW (±50% C_f uncertainty)
- Re_wall = 1.22×10⁷; C_f = 0.00283 (Prandtl 1/5-power, Schlichting §21.2)
- SUMMARY.md ~1.3 kW discrepancy factor = 17.07 (documented in corot01 JSON)
- tau_spinup = 71 s (marginal quasi-steady; acceptable for steady-state analysis)
- v_rel_vertical = v_loop = 3.7137 m/s PRESERVED for all f (COROT-03 geometric proof)
- lambda_max = 1.2748 (interpolated from foil01 ascending F_tan zero-crossing)
- COROT-01 and COROT-03 requirements satisfied

### Phase 4 Locked Values (authoritative — use phase4_summary_table.json for exact values)

- phase4_verdict = **NO_GO** (corrected for v_loop = 2.384 m/s co-rotation scaling)
- v_loop_corrected = 2.3835 m/s (F_vert = −663.86 N downward; Phase 2 sign convention)
- AoA_final at convergence = 10.0128° (brentq result; not exactly 10°)
- F_vert_direction = downward (opposing buoyancy; reduces terminal velocity from 3.71 m/s)
- co-rotation_correction_scale = (2.384/3.714)³ = 0.264 (drag ∝ v³)
- P_net_corot_corrected = 12,380 W (vs Phase 3 nominal 46,826 W at v=3.71 m/s)
- COP_system_nominal_corrected = 0.925 (η_c=0.70, loss=10%)
- COP_range_corrected = [0.811, 1.186] across 9 scenarios — all below 1.5 threshold
- COP_lossless = 2.204 (lossless gate ≠ 1.0; buoy-iso gate W_buoy/W_iso = 1.000 PASS)
- All three SYS requirements satisfied: SYS-01, SYS-02, SYS-03
- Corrected: reversed foil mounting is NOT a valid design path — F_vert opposes vessel motion on both loop halves (kinematic: lift ⊥ v_rel); AoA optimization is the only remaining lever
- Prototype measurement priorities: (1) F_vert sign, (2) tack-flip loss, (3) mechanical loss fraction

### Phase 5 Locked Values (authoritative — use phase5_anchor_check.json for exact values)

- phase5_status = **anchor validated** — brentq solver reproduces Phase 4 anchor to 0.001%
- solver_module = analysis/phase5/aoa_sweep_solver.py (importable by Phase 6 and Phase 8)
- v_loop_at_anchor = 2.383484 m/s (0.0002% error vs Phase 4; tolerance 0.5%)
- F_vert_at_anchor = −663.862 N per vessel (0.0005% error vs Phase 4; tolerance 1.0%)
- COP_at_anchor = 0.92501 (0.00007% error vs Phase 4; tolerance 0.5%)
- F_vert sign confirmed negative (downward) at AoA = 1, 5, 10, 15 deg: −146.1, −472.2, −663.7, −668.0 N per vessel
- Limiting case AoA=0: v_loop=3.691 m/s (≈ v_nom, C_L=0 pure drag), F_vert=−164.7 N
- Key deviation: per-vessel force balance in F_net_residual (plan pseudocode had N_ascending multiplier — auto-corrected)
- phase6_ready = **true** (overall_anchor_pass=true in phase5_anchor_check.json)
- All three claims PASS: claim-ANAL-01, claim-ANAL-02, claim-VALD-01
- All 7 pitfall guards confirmed: PITFALL-M1, PITFALL-N-ACTIVE, PITFALL-C6, PITFALL-COROT, F_vert_sign, brentq_not_fixed, inputs_from_JSON

### Phase 6 Locked Values (authoritative — use phase6_verdict.json for exact values)

- phase6_verdict = **NO_GO** across all nine scenarios and all AoA in [1°, 15°]
- AoA_optimal = 2.0° (scenario-independent; maximizes COP by balancing W_corot gain vs W_foil loss)
- COP_max_nominal = 0.94373 at (η_c=0.70, loss=10%, AoA=2°) — 2.0% improvement over Phase 4
- COP_max_all_scenarios = 1.210 at (η_c=0.85, loss=5%, AoA=2°) — gap = 0.290 to threshold 1.5
- η_c_required_for_GO = 1.054 — exceeds isothermal limit (η_c=1.0); COP=1.5 physically unreachable
- At η_c=1.0, loss=5%: COP_max = 1.423 < 1.5 (confirms fundamental geometric constraint)
- scenario_independence = confirmed (argmax_AoA identical for all nine η_c × loss_frac combinations)
- All 3 contract claims PASS: claim-SWEEP-01, claim-SWEEP-02, claim-VERD-01
- All 9 acceptance tests PASS; all 7 pitfall guards True; all 5 forbidden proxies rejected
- tack_flip_caveat: +5% additional loss reduces COP_max from 0.944 to 0.891 (highest prototype priority)
- v1.1_milestone_status = **COMPLETE** (NO_GO; 2026-03-21)

## Performance Metrics

| Label | Duration | Tasks | Files |
| ----- | -------- | ----- | ----- |
| Phase 1 Plan 01 | ~35 min | 2 | 6 |
| Phase 1 Plan 02 | ~20 min | 2 | 6 |
| Phase 1 Plan 03 | ~25 min | 2 | 7 |
| Phase 2 Plan 01 | ~35 min | 2 | 5 |
| Phase 2 Plan 02 | ~40 min | 2 | 8 |
| Phase 3 Plan 01 | ~35 min | 2 | 4 |
| Phase 3 Plan 02 | ~45 min | 2 | 5 |
| Phase 4 Plan 01 | ~45 min | 2 | 4 |
| Phase 4 Plan 02 | ~45 min | 2 | 5 |
| Phase 5 Plan 01 | ~45 min | 2 | 3 |
| Phase 6 Plan 01 | ~45 min | 2 | 4 |

## Accumulated Context

### Decisions

- [v1.2 Roadmap 2026-03-21]: VALD-01 energy accounting gate is Phase 7's load-bearing prerequisite; Phase 8 cannot make COP claims before it is closed
- [v1.2 Roadmap 2026-03-21]: Phase 8 uses the Phase 5 brentq solver extended with F_jet(z); continuity check (reproduces Phase 6 at zero jet/tail) required before any verdict
- [v1.2 Roadmap 2026-03-21]: Tail foil span fixed at 0.457 m (vessel diameter, user-asserted anchor); chord is the sweep variable (0.05–0.457 m)
- [v1.2 Roadmap 2026-03-21]: AoA held at 2° (Phase 6 optimal) for the 9-scenario COP table; sensitivity check at 1° and 3° in TAIL-03
- [v1.2 Roadmap 2026-03-21]: Verdict threshold is COP > 1.0 (net-positive), not 1.5 (original target — confirmed unachievable at current geometry)
- [v1.2 Init]: Started milestone v1.2 — purge thrust and tail foil quantification; verdict gate COP > 1.0 (not 1.5); wave coupling deferred to v1.3
- [v1.3 Pre-plan 2026-03-21]: v1.3 = Differential Rotation Analysis; core question is whether v_water_tangential > v_arm_tangential is a COP multiplier, additive, or stall trigger; no energy accounting for rotation source; sweep r ∈ [1.0, 1.5]; Phases 9–10
- [Init]: Use actual cylinder volume (7.069 ft³), not user estimate
- [Init]: Fill target = air fills vessel exactly at surface (V_air_surface = V_vessel)
- [Init]: Fill window = 1/4 loop circumference at 3 m/s
- [Init]: Fresh water, bottom of vessel at 60 ft depth
- [Init]: Analyze components separately before system balance (user methodology)
- [Phase 1 Plan 01]: Use precise P_r=2.7669 (not rounded 2.770) for all calculations
- [Phase 1 Plan 01]: W_adia = 23,960 J (precise); CONVENTIONS.md 24,040 J is documentation rounding
- [Phase 1 Plan 01]: Re = v*d/nu_w (kinematic viscosity; no rho_w factor)
- [Phase 1 Plan 01]: W_jet = 0 as explicit separate line item (Pitfall C6 guard)
- [Phase 1 Plan 02]: F_b_avg = W_iso/H used as energy-weighted average driving force for terminal velocity
- [Phase 1 Plan 02]: v_handoff conservative = C_D=1.2, F_chain=200N
- [Phase 1 Plan 03]: P_bottom = 280,352.6 Pa (precise from JSON), not rounded 280,500 Pa
- [Phase 1 Plan 03]: Feasibility threshold 300 SCFM; all expected values below this
- [Phase 2 Plan 01]: (L/D)_min = cot(β) = λ (not √(1+1/λ²)); algebraic proof in foil01_force_sweep.json
- [Phase 2 Plan 01]: COP formula uses per-vessel units: (W_buoy + W_foil_pv) / W_pump
- [Phase 2 Plan 01]: Fixed mount_angle=38° at λ=1; F_tan > 0 only for λ ∈ [0.3, 1.27] with fixed mount
- [Phase 2 Plan 01]: F_vert/F_b_avg = 1.15 >> 0.20 — Phase 4 coupled solution mandatory before final COP
- [Phase 2 Plan 02]: Tacking sign CONFIRMED by explicit vector geometry (not assumed); Darrieus analogy confirmed
- [Phase 2 Plan 02]: Design operating point λ=0.9, ω=0.913 rad/s, 8.72 RPM, v_tan=3.34 m/s
- [Phase 2 Plan 02]: lambda_min for COP≥1.5 reported at 3 levels: any(λ=0.7 stall), non-stall(λ=0.8), OK-only(λ=0.9)
- [Phase 3 Plan 01]: f_eff = 0.294 (stall-limited from f_ss_upper_bound=0.635); P_corot = 22.19 kW for Phase 3 Plan 02
- [Phase 3 Plan 01]: C_f = 0.00283 at Re=1.22e7 (not 0.00181 as in plan notes — formula correct, note imprecise)
- [Phase 3 Plan 01]: lambda_max = 1.2748 (interpolated from foil01 ascending F_tan zero-crossing)
- [Phase 3 Plan 02]: CUBIC power saving formula P_drag_saved = P_drag_full × [1−(1−f)³] — not force formula (1−f)²
- [Phase 3 Plan 02]: f_optimal = f_stall = 0.294003 (P_corot too small to create interior maximum; stall bounds sweep)
- [Phase 3 Plan 02]: COP_corot per-vessel formula — no N_ascending multiplier (all quantities are per-vessel ratios)
- [Phase 3 Plan 02]: Phase 3 verdict = net_positive; P_corot negligible vs drag saved; Phase 4 F_vert coupling mandatory
- [Phase 4 Plan 01]: F_vert is downward (Phase 2 sign convention) — v_loop and COP LOWER than Phase 2 partial values
- [Phase 4 Plan 01]: Lossless COP gate (COP=1.0) does not apply to multi-source machine; use buoy-iso gate (W_buoy/W_iso=1.000)
- [Phase 4 Plan 01]: Fixed-point iteration diverges at constant lambda; brentq is the correct solver
- [Phase 4 Plan 01]: e_oswald = 0.85 (Phase 2 rectangular planform, not 0.9 from plan pseudocode)
- [Phase 4 Plan 02]: Co-rotation P_net must be scaled by (v_loop_corr/v_loop_nom)³ = 0.264 at corrected velocity
- [Phase 4 Plan 02]: Verdict = NO_GO (corrected COP_nominal=0.925); reversed foil mounting is NOT a valid design path — F_vert opposes motion on both sides (kinematic); AoA optimization is the correct v1.1 investigation
- [v1.1 Roadmap]: Phase 5 = formulation + anchor validation; Phase 6 = full sweep + verdict; anchor check (VALD-01) is the first computation in Phase 5 before any new AoA points are computed
- [Phase 5 Plan 01]: Per-vessel force balance in F_net_residual — plan pseudocode had N_ascending multiplier (gives 63% v_loop error); correct is per-vessel (confirmed by anchor match to 0.0002%)
- [Phase 5 Plan 01]: F_vert_N in Phase 4 JSON stores per-vessel value; anchor comparison uses per-vessel throughout
- [Phase 5 Plan 01]: e_oswald=0.85 loaded from foil01_force_sweep.json (not from phase2_summary_table.json)
- [Phase 5 Plan 01]: AoA parameterization confirmed: mount_angle = beta_deg - AoA_target_deg computed dynamically at each brentq evaluation; NOT pre-fixed at 38 deg
- [Phase 6 Plan 01]: AoA_optimal = 2.0° (not 10° from Phase 4); co-rotation gain at low AoA slightly outweighs foil torque loss, but only by ~2% COP
- [Phase 6 Plan 01]: NACA monotonicity restricted to AoA < 12° — C_L peaks at 12° (C_L=1.14) and drops toward stall at 14° (C_L=1.05); physical near-stall feature, not a bug
- [Phase 6 Plan 01]: η_c* = 1.054 required for GO — exceeds isothermal limit; COP=1.5 not achievable at current geometry; v1.2 must change design (depth, vessel count, or geometry)
- [Phase 6 Plan 01]: Scenario-independence confirmed — argmax_AoA COP identical for all nine (η_c, loss_frac) combinations (algebraically exact: only W_gross(AoA) depends on AoA)

### Active Approximations

- Ideal gas law for air compression/expansion (Z ≈ 1 at < 3 atm; error < 0.1%)
- Fresh water density = 998.2 kg/m³ (20°C; CRC Handbook)
- Isothermal ascent for buoyancy work (valid for slow ascent in large water body)
- F_b_avg = W_iso/H for terminal velocity (energy-weighted average; correct for energy accounting)
- C_D = 0.8–1.2 for blunt cylinder (Hoerner; self-consistent with Re ~ 10⁶)
- Circular loop geometry for fill arc (1/4 circumference; ±5% uncertainty)
- Quasi-steady foil forces (k ~ 0.01–0.05 << 0.1; validated)
- Prandtl lifting-line elliptic load (AR=4; C_L_3D = C_L_2D/1.5)
- Phase 3 P_net_corot at v_loop_nominal only — scaled by (v_corr/v_nom)³ for self-consistent balance (applied in Phase 4; must be re-applied at each AoA in Phase 6)

### Pending Todos

- Plan Phase 7 (Purge Thrust and Tail Foil Derivation) — PROP-01, PROP-02, TAIL-01, TAIL-02, VALD-01
- After Phase 7: plan Phase 8 (Revised System Verdict) — PROP-03, TAIL-03, VALD-02, VALD-03
- After Phase 8 complete: plan Phase 9 (Differential Rotation Geometry — WAVE-01, WAVE-02)
- After Phase 9 complete: plan Phase 10 (COP Sweep and Verdict — WAVE-03)

### Blockers/Concerns

- None — v1.2 roadmap complete; Phase 7 planning is the next step; v1.3 pre-planned (Phases 9–10)

## Session Continuity

**Last session:** 2026-03-21
**Stopped at:** v1.2 roadmap created — ready for Phase 7 planning
**Resume file:** analysis/phase5/aoa_sweep_solver.py (Phase 7 solver extension starting point); phase6_verdict.json (COP baseline reference)
