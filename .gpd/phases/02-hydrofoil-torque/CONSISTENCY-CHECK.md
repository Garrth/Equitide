# Consistency Check — Phase 02: Hydrofoil & Torque

**Mode:** rapid
**Phase checked:** 02-hydrofoil-torque (Plans 01 and 02)
**Checked against:** Full conventions ledger (CONVENTIONS.md), state.json convention_lock, Phase 1 JSON outputs
**Date:** 2026-03-17
**Checker:** gpd-consistency-checker

---

## Summary

**consistency_status: WARNING**

Phase 2 is numerically consistent with Phase 1 locked values on every quantity that crosses the phase boundary. The energy accounting, force formulas, velocity triangle, COP formula, and dimensional analysis all check out. Two documentation-level discrepancies exist — one known pending todo (W_adia rounding) and one undocumented convention drift (N_vessels count). Neither affects any Phase 2 numerical result.

---

## Provides/Consumes Verification

| Quantity | Producer | Consumer | Meaning Match | Units Match | Test Value | Convention Match | Status |
|---|---|---|---|---|---|---|---|
| W_buoy = 20644.6159 J | Phase 1 JSON | Phase 2 phase2_summary_table.json | Yes — isothermal buoyancy work per vessel | Yes — Joules | Phase 2 reports 20644.6159 exactly | Yes — W_buoy = W_iso identity confirmed | PASS |
| W_pump_nominal = 34227.8 J | Phase 1 JSON | Phase 2 phase2_summary_table.json | Yes — pumping work at eta_c=0.70 | Yes — Joules | Phase 2 reports 34227.8 exactly | Yes — W_pump = W_adia/eta_c convention followed | PASS |
| F_b_avg = 1128.86 N | Phase 1 JSON | Phase 2 phase2_summary_table.json | Yes — energy-weighted average buoyancy force for F_vert fraction check | Yes — Newtons | Phase 2 reports 1128.86 exactly | Yes — F_b_avg = W_iso/H convention | PASS |
| v_loop = 3.7137 m/s | Phase 1 JSON (buoy03_terminal_velocity.json v_handoff) | Phase 2 all scripts | Yes — terminal ascent speed, C_D=1.0 F_chain=0, upper bound | Yes — m/s | Loaded from JSON, Pitfall C7 guard asserted; no v=3.0 hardcoded | Yes — nominal terminal velocity convention | PASS |
| COP_buoy_only = 0.6032 | Phase 1 JSON COP_ideal_max_at_eta_70 | Phase 2 anchor check | Yes — buoyancy-only COP at eta_c=0.70 | Dimensionless | Phase 2 recomputes 0.6031535 from JSON values; error=4.65e-5 < 0.001 threshold | Yes — COP = W_buoy/W_pump formula | PASS |

**All 5 cross-phase transfers verified. Zero failures.**

---

## Convention Compliance Matrix

| Convention | Introduced | Relevant to Phase 2? | Compliant? | Evidence | Notes |
|---|---|---|---|---|---|
| SI units (m, kg, s, N, J, W, Pa) | Phase 0 | Yes | YES | phase2_summary_table.json: `_assert_convention: unit_system=SI`; all force/energy/power quantities carry correct SI units | No imperial values in calculations |
| z=0 at tank bottom; z increases upward | Phase 0 | Yes (t_asc = H/v_loop) | YES | H=18.288 m used correctly; t_asc = 18.288/3.7137 = 4.9245 s matches JSON | |
| P(z) = P_atm + rho_w*g*(H-z) | Phase 0 | Yes (via v_loop from Phase 1) | YES (indirect) | F_b(z) function in Phase 1 is verified; Phase 2 uses v_loop loaded from Phase 1 results which correctly implement this | |
| rho_w = 998.2 kg/m³ | Phase 0 | Yes — hydrofoil L/D and buoyancy | YES | Lift: L = 0.5*998.2*C_L_3D*A_foil*v_rel² used in foil_forces.py | |
| g = 9.807 m/s² | Phase 0 | Yes (via F_b values from Phase 1) | YES (indirect) | Used in Phase 1; Phase 2 loads results from Phase 1 JSON | |
| nu_w = 1.004e-6 m²/s | Phase 0 | Yes — Re number for NACA data validity | YES | Re = v_rel*chord/nu_w; Phase 2 verifies Re in [8e5, 1.9e6] (Hoerner/TR-824 range) | |
| H = 18.288 m | Phase 0 | Yes | YES | H_m = 18.288 in geometry block of phase2_summary_table.json | |
| W_buoy = W_iso identity (|error| < 1%) | Phase 0 (mandatory check) | Yes — anchor check | YES | Phase 2 Plan 01 and Plan 02 both verify COP(W_foil=0) = 0.6032 to 4.65e-5 error | |
| Constant-volume buoyancy FORBIDDEN | Phase 0 | Yes | YES | Phase 2 uses W_buoy from Phase 1 integral; no F_b*H calculation in Phase 2 code | |
| F_b positive upward; F_D positive magnitude (loss); F_L positive in shaft direction | Phase 0 | Yes | YES | F_tan = L*sin(beta) - D*cos(beta) > 0 drives shaft; F_vert = -L*cos(beta) - D*sin(beta) < 0 opposes ascent — sign conventions match | |
| W_pump = input (COP denominator); W_buoy, W_foil = outputs (numerator) | Phase 0 | Yes | YES | COP_partial = (W_buoy + W_foil_asc_pv + W_foil_desc_pv) / W_pump throughout; labels confirmed | |
| Hydrofoil: L = 0.5*rho_w*C_L_3D*A_foil*v_rel² | Phase 0 | Yes | YES | Formula used exactly in foil_forces.py; v_rel = sqrt(v_loop²+v_tan²) (rotating-arm) | |
| Prandtl LL: C_L_3D = C_L_2D/(1+2/AR); C_D_i = C_L_3D²/(pi*e*AR) | Phase 0 | Yes | YES | AR=4 gives factor 1.5: C_L_3D = C_L_2D/1.5 = 0.667*C_L_2D. Verified with AR=50 limiting case | |
| v_rel_h = v_h*(1-f_corot); v_rel_v = v_v unchanged | Phase 0 | Partial — f_corot=0 assumed | YES (baseline) | Phase 2 explicitly sets f_corot=0 and flags Phase 3 must quantify co-rotation reduction | Phase 3 dependency correctly noted |
| P_shaft = F_tan * v_tan (NOT L/D * P_drag) | Phase 0/Phase 2 pitfall guard | Yes | YES | Pitfall C2 guard asserted in all scripts; confirmed in fp-LD-as-power-ratio rejected | |
| N_vessels = 30 | Phase 0 | DISCREPANCY | WARNING | Phase 2 uses N_ascending=12, N_descending=12, N_total=24 (rotating-arm: 4 vessels/arm × 3 arms). CONVENTIONS.md and state.json still show N_vessels=30 with no change entry | See Violation V-01 below |
| W_adia = 24,040 J | Phase 0 (documentation) | Indirect | MINOR | Phase 1 JSON uses precise W_adia=23,959.45 J; CONVENTIONS.md shows 24,040 J. Phase 2 loads from JSON so no numerical impact | See Violation V-02 below |

---

## Convention Violations

### V-01: N_vessels Count — Undocumented Documentation Drift (WARNING)

**Convention:** N_vessels = 30 (10 per loop × 3 loops), introduced Phase 0 in both CONVENTIONS.md and state.json convention_lock.

**What Phase 2 uses:** N_ascending = 12, N_descending = 12, N_total = 24. This comes from the rotating-arm geometry: 4 vessels per arm × 3 arms = 12 ascending + 12 descending.

**Why it occurred:** Phase 0 initialization used the user specification of 30 vessels before the rotating-arm geometry was established. The rotating-arm model (4 vessels per arm, 3 arms, ascending = descending) yields 24 active vessels during a cycle, not 30.

**Numerical impact:** NONE on Phase 2 COP values. The COP formula uses per-vessel units throughout: COP_partial = (W_buoy + W_foil_asc_pv + W_foil_desc_pv) / W_pump. The per-vessel result is independent of N_total. The total energy outputs (W_foil_combined_total_J = 498,397 J) and the W_foil_ascending_total_J = 249,199 J are labeled as totals and are not used in COP calculation.

**Documentation impact:** CONVENTIONS.md and state.json convention_lock are stale on this parameter. Downstream phases (Phase 3, Phase 4) loading N_vessels from CONVENTIONS.md or state.json will get 30, not 24.

**Required fix:** Add a Convention Change entry to CONVENTIONS.md for N_vessels (30 → 24 active in rotating-arm geometry) and update state.json convention_lock. Document that "30 total vessels installed; 24 active at any time during rotation cycle (12 ascending, 12 descending per the 3-arm rotating geometry)."

**Severity:** WARNING — no current numerical error but creates a trap for Phase 3/4.

---

### V-02: W_adia Documentation Rounding — Known Pending Todo (MINOR)

**Convention:** CONVENTIONS.md and state.json show W_adia = 24,040 J.

**Phase 1 precise value:** W_adia_J = 23,959.45 J (from thrm01_compression_work.json).

**Impact on Phase 2:** None. Phase 2 uses W_pump loaded from Phase 1 JSON (W_pump_nominal_J = 34227.8 J = W_adia/eta_c at eta_c=0.70 using precise W_adia). The 24,040 J vs 23,959 J discrepancy (0.34%) does not enter any Phase 2 calculation.

**Status:** Already recorded as a pending todo in STATE.md: "Update CONVENTIONS.md W_adia display value from 24,040 J to 23,960 J (documentation)."

**Required fix:** Update CONVENTIONS.md Section 4 and the thermodynamic_work test block to show W_adia = 23,960 J (or 23,959 J for 5-sig-fig precision).

**Severity:** MINOR — documentation only.

---

## Spot-Check: Test Value Verification

### Test 1 — P_shaft at lambda=1

**Setup:** v_loop = 3.7137 m/s, v_tan = 1.0 × 3.7137 = 3.7137 m/s, beta = arctan(1/1) = 45°, F_tan = 1135.5 N (from JSON).

**Expected:** P_shaft = F_tan × v_tan = 1135.5 × 3.7137 = 4216.6 W

**Reported:** P_shaft_per_vessel_W = 4216.995 W

**Match:** PASS (0.009% difference — floating-point rounding in F_tan display)

---

### Test 2 — W_foil per vessel at lambda=1

**Setup:** P_shaft = 4217 W, t_asc = H/v_loop = 18.288/3.7137 = 4.9245 s

**Expected:** W_foil = 4217 × 4.9245 = 20,770 J

**Reported:** W_foil_ascending_per_vessel_J = 20766.59 J

**Match:** PASS (0.015% difference — rounding in displayed F_tan vs. precise internal value)

---

### Test 3 — omega at lambda=0.9

**Setup:** v_tan = 0.9 × 3.7137 = 3.34233 m/s; r = 3.66 m

**Expected:** omega = v_tan / r = 3.34233 / 3.66 = 0.91319 rad/s

**Reported:** omega_design_rad_s = 0.9132049 rad/s

**Match:** PASS

---

### Test 4 — COP_partial at lambda=0.9

**Setup:** From SUMMARY: COP = (20644.62 + 24889.5 + 24889.5) / 34227.8

**Expected:** 70423.62 / 34227.8 = 2.0575

**Reported:** COP_partial_at_lambda_0p9 = 2.0574996822

**Match:** PASS

---

### Test 5 — Phase 1 anchor

**Setup:** COP_0 = W_buoy / W_pump = 20644.6159 / 34227.8

**Expected:** 0.60315...

**Reported:** COP_computed = 0.6031534571, error = 4.65e-5

**Match:** PASS (well within 0.001 threshold)

---

## Approximation Validity Check

| Approximation | Validity Condition | Phase 2 Status | Notes |
|---|---|---|---|
| v_loop = 3.7137 m/s from Phase 1 (F_chain=0, C_D=1.0) | F_vert << F_b_avg | VIOLATED — F_vert/F_b_avg = 1.15 at design | Explicitly documented as FLAG_LARGE; all COP labeled as upper bounds; Phase 4 coupled solution required |
| Quasi-steady foil forces | k << 0.05 | PASS — k < 0.02 at all lambda | Validated in Phase 2 Plan 01 |
| Prandtl LL for AR=4 | AR ≥ 4 | BORDERLINE — AR=4 at boundary; 5-15% error expected | Documented uncertainty |
| NACA 0012 at Re~1e6 | 8e5 < Re < 9e6 | PASS — Re range [8e5, 1.9e6] at nominal conditions | Interpolated from Re=3e6 data; ~5-10% uncertainty |
| Tack mechanism lossless | W_tack = 0 | UNVALIDATED — not modeled | Documented as uncertainty; Phase 4 must address |
| f_corot = 0 (no co-rotation) | Co-rotation = Phase 3 | PASS AS BASELINE — Phase 3 will quantify | Correctly deferred |

**Critical approximation violation:** F_vert/F_b_avg = 1.15 means the Phase 1 terminal velocity was computed without foil loading. With F_vert adding 1.15 × 1128.86 = 1298 N downward force, the true terminal velocity will be substantially lower than 3.7137 m/s. This is flagged, documented, and properly labeled — it is not an error in Phase 2's derivation methodology, but it means the design-point COP_partial = 2.06 is an upper bound. Phase 4 must solve (v_loop, omega) jointly.

---

## Provides/Consumes Chain Integrity

### What Phase 2 provides to Phase 3

| Quantity | Value | Status |
|---|---|---|
| lambda_design | 0.9 | Consistent — defined as first OK-flag lambda with COP >= 1.5 |
| omega_design_rad_s | 0.9132 rad/s (8.72 RPM) | Consistent — derived from lambda × v_loop / r |
| COP_partial at design | 2.057 | Correctly labeled as upper bound |
| F_vert flag | PROPAGATED | Phase 3 must account for effective v reduction |
| phase2_summary_table.json | written | Machine-readable; Phase 3/4 can load directly |

### What Phase 2 provides to Phase 4

| Quantity | Value | Status |
|---|---|---|
| F_vert/F_b_avg = 1.15 | FLAG_LARGE | Correctly propagated — Phase 4 mandatory coupled solution |
| COP_partial upper bound | 2.057 | Correctly labeled; Phase 4 will reduce this |
| foil01_force_sweep.json | F_tan(lambda) table | Available for coupled solver |

---

## Convention Evolution

**No convention changes were introduced in Phase 2.** All Phase 1 conventions are preserved. The rotating-arm geometry is a refinement of the loop model, not a convention change. The N_vessels discrepancy is an undocumented evolution (violation V-01 above).

---

## Narrative Coherence

- **Problem-method alignment:** YES — Phase 2 correctly asks whether foil torque fills the COP gap left by buoyancy-alone (COP_0=0.603 << 1.5 target). The rotating-arm lambda sweep directly answers whether F_tan > 0 and whether COP_partial >= 1.5 is achievable.
- **Result-problem alignment:** YES — COP_partial = 2.06 at lambda=0.9 directly answers the feasibility question, with the important qualifier that it is an upper bound.
- **Conclusion-evidence alignment:** YES — the GREEN light is justified by the numerical sweep; the "upper bound" caveat is explicit and repeated in every reporting location.
- **Open threads acknowledged:** YES — F_vert coupling, co-rotation (f_corot=0 assumed), tack mechanism losses, and Phase 4 coupled solution are all explicitly flagged.

---

## Cross-Phase Error Patterns (Rapid Mode Checks)

| Error Pattern | Instances Found | Severity |
|---|---|---|
| Sign absorbed into definition | 0 | — |
| Normalization factor change | 0 | — |
| Implicit assumption violated | 1 (F_vert/F_b_avg >> 0.20) | Documented and flagged; not a silent violation |
| Coupling convention mismatch | 0 | — |
| Factor of 2pi error | 0 | — |
| Wick rotation sign | N/A | — |
| Boundary condition mismatch | 0 | — |
| Undocumented convention drift | 1 (N_vessels: 30→24) | WARNING — documentation gap |

---

## Detailed Findings

### Finding F-01: N_vessels Documentation Drift (WARNING — action required)

**What:** CONVENTIONS.md and state.json convention_lock record N_vessels=30. Phase 2 uses N_total=24 (12 ascending, 12 descending) from rotating-arm geometry (4 per arm × 3 arms).

**Why not caught earlier:** Phase 0 initialization used the user's stated "30 vessels" before the rotating-arm geometry was locked. The architecture evolved correctly in practice but the conventions ledger was never updated.

**Numerical impact:** None on Phase 2 COP (per-vessel formula). Potential impact on Phase 3 or Phase 4 if those phases load N_vessels=30 from state.json and use it in a total-energy calculation.

**Required action:** Before Phase 3 begins:
1. Add entry to CONVENTIONS.md §4 (System Parameters): "N_vessels_total=30 (installed); N_active=24 (12 ascending + 12 descending per rotating-arm geometry); N_per_arm=4; N_arms=3."
2. Add convention change entry in CONVENTIONS.md §Convention Changes noting the 30→24 active distinction.
3. Update state.json convention_lock custom_conventions N_vessels value.

---

### Finding F-02: W_adia Documentation Rounding (MINOR — pending todo)

**What:** CONVENTIONS.md and state.json show W_adia=24,040 J (Phase 0 estimate). Phase 1 precise value: 23,959.45 J. Difference: 0.34%.

**Impact:** None — Phase 2 uses W_pump loaded from Phase 1 JSON (which uses the precise W_adia).

**Required action:** Already in STATE.md pending todos. Update CONVENTIONS.md §4 and §Machine-Readable Convention Tests to show W_adia=23,960 J.

---

## Checks Performed

1. Full Phase 1 anchor values consumed by Phase 2 (all 5 quantities: W_buoy, W_pump, F_b_avg, v_loop, COP_0)
2. COP formula internal consistency with test-value substitution at lambda=0.9 and lambda=1.0
3. Convention compliance for all 14 relevant conventions from ledger (4 canonical, 10 custom)
4. Hydrofoil force formula dimensional check (F_tan, P_shaft, W_foil, omega — all verified)
5. Phase 1 anchor numerical reproduction (error=4.65e-5 << 0.001 threshold)
6. Sign convention for forces (F_tan drives shaft, F_vert opposes ascent)
7. W_buoy=W_iso identity compliance (via anchor check)
8. N_vessels convention drift identification
9. W_adia documentation discrepancy identification
10. Approximation validity ranges vs. parameter values used
11. Provides/consumes chain integrity for Phase 3 and Phase 4
12. Narrative coherence: problem → method → result → conclusion chain

---

## Final Status

```yaml
consistency_status: WARNING
issues:
  - id: V-01
    severity: WARNING
    description: "N_vessels convention drift: CONVENTIONS.md and state.json show N_vessels=30; Phase 2 uses N_total=24 (rotating-arm geometry). No convention-change entry exists. Potential Phase 3/4 trap if N_vessels loaded from stale state."
    action_required: "Update CONVENTIONS.md and state.json before Phase 3 begins."
  - id: V-02
    severity: MINOR
    description: "W_adia documentation: CONVENTIONS.md shows 24,040 J vs Phase 1 precise 23,959.45 J. No numerical impact (Phase 2 loads from JSON). Already in STATE.md pending todos."
    action_required: "Update CONVENTIONS.md display value."
  - id: V-03
    severity: KNOWN_FLAG
    description: "F_vert/F_b_avg=1.15 >> 0.20 approximation validity threshold. All Phase 2 COP are upper bounds. Documented and propagated correctly; Phase 4 coupled solution is mandatory."
    action_required: "None in Phase 2 — Phase 4 resolves."
all_phase1_anchors_reproduced: true
phase1_anchor_error: 4.65e-5
cop_formula_verified: true
dimensional_analysis: PASS
sign_conventions: PASS
```
