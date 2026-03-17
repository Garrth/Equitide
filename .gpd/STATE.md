# Research State

## Project Reference

See: .gpd/PROJECT.md (updated 2026-03-16)

**Core research question:** Can this buoyancy + hydrofoil engine produce at least 1.5W of shaft power for every 1W of air pumping input?
**Current focus:** Phase 1 — Air, Buoyancy & Fill

## Current Position

**Current Phase:** 1
**Current Phase Name:** Air, Buoyancy & Fill
**Total Phases:** 4
**Current Plan:** 0
**Total Plans in Phase:** 0
**Status:** Ready to plan
**Last Activity:** 2026-03-16
**Last Activity Description:** Project initialized

**Progress:** [░░░░░░░░░░] 0%

## Active Calculations

None yet.

## Intermediate Results

- Pumping energy (isothermal, single vessel): ~20.6 kJ — from scoping conversation
- Pumping energy (adiabatic, single vessel): ~24.0 kJ — from scoping conversation
- Vessel volume: 7.069 ft³ (π × 0.75² × 4)
- Pressure at 60 ft depth: 2.770 atm (40.70 psi, fresh water)
- Volume at depth: 2.553 ft³ (vessel is 36% air / 64% water when initially charged)

## Open Questions

- Final loop geometry (needed to compute fill window duration and vessel spacing)
- Hydrofoil chord length, span, and profile for L/D parametric estimate
- Co-rotation achievement mechanism and energy cost
- Does 3 m/s vessel velocity hold under hydrofoil drag loading?

## Performance Metrics

| Label | Duration | Tasks | Files |
| ----- | -------- | ----- | ----- |
| -     | -        | -     | -     |

## Accumulated Context

### Decisions

- [Init]: Use actual cylinder volume (7.069 ft³), not user estimate
- [Init]: Fill target = air fills vessel exactly at surface (V_air_surface = V_vessel)
- [Init]: Fill window = 1/4 loop circumference at 3 m/s
- [Init]: Fresh water, bottom of vessel at 60 ft depth
- [Init]: Analyze components separately before system balance (user methodology)

### Active Approximations

- Ideal gas law for air compression/expansion
- Fresh water density = 1000 kg/m³ (62.4 lb/ft³)
- 1 atm = 33.9 ft fresh water

### Pending Todos

None yet.

### Blockers/Concerns

- Loop geometry not yet specified — needed for fill window calculation (Phase 1)

## Session Continuity

**Last session:** 2026-03-16
**Stopped at:** Project initialized
**Resume file:** —
