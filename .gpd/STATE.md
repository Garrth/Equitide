# Research State

## Project Reference

See: .gpd/PROJECT.md (updated 2026-03-16)

**Core research question:** Can this buoyancy + hydrofoil engine produce at least 1.5W of shaft power for every 1W of air pumping input?
**Current focus:** Phase 2 — Hydrofoil & Torque

## Current Position

**Current Phase:** 2
**Current Phase Name:** Hydrofoil & Torque
**Total Phases:** 4
**Current Plan:** 0
**Total Plans in Phase:** TBD
**Status:** Phase 1 complete — ready to plan Phase 2
**Last Activity:** 2026-03-17
**Last Activity Description:** Phase 1 all 3 plans complete, verified 12/12, consistent

**Progress:** [██░░░░░░░░] 25%

## Active Calculations

None — between phases.

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

## Open Questions

- Hydrofoil chord length, span, and profile for L/D parametric estimate
- Co-rotation achievement mechanism and energy cost
- Does 3 m/s vessel velocity hold under hydrofoil drag loading?
- What is the chain coupling force F_chain in practice? (affects v_terminal)

## Performance Metrics

| Label | Duration | Tasks | Files |
| ----- | -------- | ----- | ----- |
| Phase 1 Plan 01 | ~35 min | 2 | 6 |
| Phase 1 Plan 02 | ~20 min | 2 | 6 |
| Phase 1 Plan 03 | ~25 min | 2 | 7 |

## Accumulated Context

### Decisions

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

### Active Approximations

- Ideal gas law for air compression/expansion (Z ≈ 1 at < 3 atm; error < 0.1%)
- Fresh water density = 998.2 kg/m³ (20°C; CRC Handbook)
- Isothermal ascent for buoyancy work (valid for slow ascent in large water body)
- F_b_avg = W_iso/H for terminal velocity (energy-weighted average; correct for energy accounting)
- C_D = 0.8–1.2 for blunt cylinder (Hoerner; self-consistent with Re ~ 10⁶)
- Circular loop geometry for fill arc (1/4 circumference; ±5% uncertainty)

### Pending Todos

- Update CONVENTIONS.md W_adia display value from 24,040 J to 23,960 J (documentation)

### Blockers/Concerns

None — Phase 1 complete.

## Session Continuity

**Last session:** 2026-03-17
**Stopped at:** Phase 1 complete — verified, consistent
**Resume file:** —
