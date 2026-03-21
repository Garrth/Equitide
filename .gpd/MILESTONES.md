# Milestones

## v1.0 Feasibility Study (Shipped: 2026-03-19)

**Phases completed:** 4 phases, 9 plans, 0 tasks

**Key accomplishments:**
- Established thermodynamic compression work bounds (W_iso=20,645 J, W_adia=23,960 J), buoyancy force profile F_b(z) at 5 heights, fill volumes, and jet-recovery accounting for the Hydrowheel buoyancy engine
- Mandatory identity gate PASSED (W_buoy = W_iso to machine precision; relative error 2e-7%); 15-point terminal velocity grid establishes v_handoff=[2.530, 4.152] m/s range for Plan 03 fill calculations
- Fill feasibility confirmed GO (147–295 SCFM at 26 psig, all 6 velocity cases feasible); Phase 1 closed with all 9 requirements satisfied and phase2_inputs locked from physics-derived terminal velocity
- Rotating-arm NACA 0012 force sweep confirms F_tan > 0 for lambda in [0.3, 1.27]; ascending foils bring COP_partial to 1.21 at design point; F_vert/F_b_avg=1.15 flags coupled correction required in Phase 4
- Descending tacking CONFIRMED by explicit rotating-arm vector geometry (Darrieus analogy); combined 24-vessel COP_partial = 2.06 at lambda=0.9 — GREEN light for Phase 3; all Phase 2 COP values are upper bounds pending Phase 4 F_vert coupling
- Angular momentum balance gives f_ss_upper_bound=0.635 (stall-limited to f_eff=0.294), P_corot=22.2 kW; vertical relative velocity and hydrofoil lift confirmed geometrically preserved for all f (COROT-01, COROT-03)
- P_net(f) sweep yields net_positive verdict: co-rotation saves 46.8 kW at f_stall=0.294 with 0.72 kW maintenance cost; COP_corot=0.603 at operating point; all COROT requirements satisfied
- Coupled v_loop = 2.384 m/s (F_vert downward, Phase 2 convention); COP_system_nominal = 1.39 at eta_c=0.70, loss=10%; lossless gate diagnostic: COP_lossless = 2.20 (net energy producer confirmed)
- NO_GO (corrected): COP_nominal=0.925 after co-rotation re-scaled to v_loop=2.384 m/s; scale=(2.384/3.714)^3=0.264 reduces W_corot by 73.6%; reversed foil mounting (upward F_vert) is decisive design path

---


## v1.1 AoA Parametric Sweep (Shipped: 2026-03-21)

**Phases completed:** 2 phases (5–6), 2 plans

**Key accomplishments:**
- AoA-parameterized brentq solver derived from Phase 2 rotating-arm vector geometry; F_vert(AoA) confirmed negative (downward) for all AoA ∈ [1°, 15°] at λ=0.9
- Anchor validation PASS: solver reproduces Phase 4 anchor (v_loop=2.383484 m/s, COP=0.92501, F_vert=−663.86 N) to within 0.001% — all three VALD-01 tolerances satisfied
- Full 16-point AoA sweep [1°–15°] completed; AoA_optimal = 2.0° identified (maximizes COP: ΔW_corot gain +168 kJ slightly outpaces ΔW_foil loss −147 kJ vs AoA=10° baseline)
- Nine-scenario verdict table delivered across all η_c × loss_frac combinations; COP_max = 1.210 at (η_c=0.85, loss=5%, AoA=2°) — gap = 0.290 to threshold 1.5
- VERDICT: NO_GO — required η_c* = 1.054 exceeds isothermal compression limit (η_c = 1.0); even at ideal compression COP_max = 1.423 < 1.5; COP = 1.5 is physically unreachable at current geometry and depth

---

