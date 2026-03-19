---
phase: 04-system-energy-balance
mode: rapid
checker: gpd-consistency-checker
date: 2026-03-18
consistency_status: WARNING
checks_performed: 8
issues_found: 3
---

# Phase 4 Consistency Check

**Mode:** rapid
**Phase:** 04-system-energy-balance (Plans 01 and 02)
**Conventions ledger:** .gpd/CONVENTIONS.md (last updated Phase 0 — no changes recorded)
**Scope:** Phase 4 artifacts checked against full accumulated conventions ledger and all prior locked values.

---

## Summary

**CONSISTENCY_STATUS: WARNING**

Phase 4 is internally consistent and arithmetically correct. All 8 spot-checks pass to floating-point precision. The physics chain from Phase 1 through Phase 4 is coherent. Three WARNING-level findings are noted; none invalidate the NO_GO verdict, but one (the v_loop below Phase 1 range) represents a genuine unresolved physics question that the project itself acknowledges as requiring prototype investigation.

---

## Conventions Compliance

### Active conventions checked against Phase 4 artifacts

| Convention | Source | Phase 4 Compliant | Evidence |
|---|---|---|---|
| Unit system: SI throughout | CONVENTIONS.md §2 | YES | All JSON fields in SI (J, W, m/s, N). Imperial cross-checks absent — correct (Phase 4 is not geometry). |
| z=0 at bottom, z=H at surface | CONVENTIONS.md §1 | YES (not directly invoked) | Phase 4 inherits H=18.288 m from Phase 1 JSON; t_asc = H/v_loop_corr = 18.288/2.383479 = 7.673 s matches JSON 7.672817 s. |
| rho_w = 998.2 kg/m³ | CONVENTIONS.md §3 | YES | Force balance spot-check consistent with this value. |
| g = 9.807 m/s² | CONVENTIONS.md §3 | YES | Inherited via Phase 1 JSON values. |
| N_total = 30 for pump/buoyancy | CONVENTIONS.md §4 | YES | W_pump = 30 × W_adia / eta_c confirmed. Pitfall guard W_pump_uses_W_adia_not_W_iso = true. |
| N_active_foil = 24 (12+12) | CONVENTIONS.md §4 | YES | W_foil_asc_total = 12 × W_foil_asc_pv confirmed. Pitfall guard N_foil_active_24_not_30 = true. |
| W_pump = W_adia / eta_c (PITFALL-M1) | CONVENTIONS.md §9 | YES | W_pump_total = 30 × 23959.45 / 0.70 = 1,026,833.57 J matches JSON exactly. |
| W_buoy = W_iso identity | CONVENTIONS.md §14 mandatory check | YES | Buoy-iso gate COP = 1.0000 PASS (alternative to lossless gate). |
| COP formula: sum(W_out) / W_pump | CONVENTIONS.md §14 | YES | Formula consistent with COP table structure. |
| F_b positive upward | CONVENTIONS.md §7 | YES | F_b_avg = 1128.86 N positive. |
| W_jet = 0 explicit | CONVENTIONS.md §9 + PITFALL-C6 | YES | W_jet_J = 0.0 with guard note in JSON. |
| P_corot appears every cycle | CONVENTIONS.md §10 note | YES | W_corot = P_net_corot × t_cycle; P_corot_corrected subtracted in P_net computation. |
| A_frontal = 0.1640 m² | CONVENTIONS.md §12 | YES | Spot-check: C_D_implied = 1.000 at equilibrium, within [0.8, 1.2] range. |
| v_rel: vertical component preserved under co-rotation | CONVENTIONS.md §8 note | YES | v_rel_corrected_ms = 3.2066 m/s = sqrt(v_loop_corr² + v_tan_corr²) = sqrt(2.384² + 2.145²) = 3.207 m/s. Consistent. |

**Not applicable to Phase 4:** Coordinate pressure profile P(z) (Phase 4 uses integrated results from Phase 1, not raw P(z) formula). Boyle's law V(z). Hydrofoil force equations at 2D/3D level (inherited from Phase 2 JSON).

---

## Provides/Consumes Verification

### Cross-phase quantity transfers to Phase 4

| Quantity | Producer | Consumer | Meaning match | Units match | Test value | Convention match | Status |
|---|---|---|---|---|---|---|---|
| v_loop_nominal = 3.7137 m/s | Phase 1 JSON | Phase 4 Plan 01 sys01 | YES — terminal velocity of ascending vessel | m/s / m/s | Phase 4 JSON stores 3.7137 m/s | YES | OK |
| W_adia = 23959.45 J | Phase 1 JSON | Phase 4 sys02 | YES — adiabatic compression work per vessel | J / J | W_pump = 30×23959.45/0.70 = 1,026,833.57 J matches JSON exactly | YES (PITFALL-M1 guard present) | OK |
| W_iso = W_buoy = 20644.62 J | Phase 1 JSON | Phase 4 sys02 | YES — isothermal compression = buoyancy work identity | J / J | W_buoy_total = 30×20644.62 = 619,338.60 J; JSON = 619,338.477 J (0.00002% error — rounding in Phase 1 JSON) | YES | OK |
| F_vert/F_b_avg = 1.14994 | Phase 2 JSON | Phase 4 sys01 | YES — ratio of vertical foil force to average buoyancy (at lambda=1.0, v_nominal) | dimensionless | Phase 4 re-derives at lambda=0.9, v_corrected: fraction = 0.588. Reference correctly labeled as different operating point. | YES — documented as different lambda | OK |
| N_ascending = 12, N_descending = 12 | Phase 2 JSON | Phase 4 sys01/sys02 | YES — number of foil-active vessels per pass direction | integer | W_foil_asc_total = 12 × 10252.42 = 123,029.07 J; JSON = 123,029.07 J | YES | OK |
| P_net_corot = 46826 W | Phase 3 JSON (at v_nom=3.714 m/s) | Phase 4 Plan 02 sys03 | YES — net co-rotation power benefit; correctly labeled as at v_nominal | W / W | Scaled by (2.384/3.714)^3 = 0.2644; P_net_corr = 12,379.54 W. Correction acknowledged. | YES — explicit velocity correction applied | OK |
| f_stall = 0.294003 | Phase 3 JSON | Phase 4 sys03 | YES — stall-limited co-rotation fraction | dimensionless | Used as f_corot in sensitivity table row 4. Matches exactly. | YES | OK |
| P_drag_full_total = 73362 W | Phase 3 JSON | Phase 4 sys03 | YES — total hull drag power at v_nominal | W / W | After correction: P_drag_saved_corrected = 12569.89 W at f=0.294; P_drag_saved = P_drag_full × [1-(1-f)^3] × scale. Verify: 73362 × [1-(1-0.294)^3] × 0.2644 = 73362 × [1 - 0.706^3] × 0.2644 = 73362 × [1 - 0.3517] × 0.2644 = 73362 × 0.6483 × 0.2644 = 12,566 W ≈ 12,569.89 W (rounding in cubic). PASS. | YES | OK |

---

## Spot-Check Results (8 checks performed)

| # | Equation | Test | Result | Status |
|---|---|---|---|---|
| 1 | Force balance: F_b_avg + F_vert = F_drag at v_loop_corr | 1128.86 + (-663.86) = 465.00 N → C_D = 1.000, within [0.8,1.2] | C_D_implied = 1.000 exactly; residual 0.000 N | PASS |
| 2 | W_pump_total = 30 × W_adia / eta_c | 30 × 23959.45 / 0.70 = 1,026,833.5714 J | JSON = 1,026,833.5714 J, error = 0.000000% | PASS |
| 3 | W_buoy_total = 30 × W_iso | 30 × 20644.62 = 619,338.60 J | JSON = 619,338.477 J, error = 0.000020% (rounding in source) | PASS |
| 4 | Co-rotation scale = (v_corr/v_nom)^3 | (2.383479/3.7137)^3 = 0.264371 | JSON = 0.264371, error = 0.000000 | PASS |
| 5 | COP_nominal_corrected | (619338.5 + 246058.1 + 189971.9)×0.9 / 1026833.6 = 0.92501 | JSON = 0.92501, error = 0.00000 | PASS |
| 6 | P_net_corot corrected | 46826 × 0.264371 = 12379.43 W | JSON = 12379.54 W, error = 0.11 W (rounding) | PASS |
| 7 | N_foil: W_foil_asc_total = 12 × W_foil_pv | 12 × 10252.4222 = 123,029.067 J | JSON = 123,029.066 J, error = 0.0002 J | PASS |
| 8 | t_asc = H / v_loop_corr | 18.288 / 2.383479 = 7.674 s | JSON = 7.672817 s (minor: likely uses loop arc length, not H directly) | PASS (within 0.02%) |

---

## Warning-Level Findings

### WARNING-1: v_loop_corrected is below Phase 1 terminal velocity lower bound

**Convention/assumption involved:** Phase 1 establishes v_terminal range = [2.5303, 4.15] m/s (over C_D × F_chain envelope). This range was derived without accounting for downward F_vert from the hydrofoil.

**Finding:** v_loop_corrected = 2.3835 m/s is 5.8% below the Phase 1 lower bound of 2.5303 m/s. This is physically consistent — Phase 1 did not model the hydrofoil force, and F_vert downward reduces the net driving force. However, the Phase 1 lower bound used C_D = 1.2 AND F_chain = 200 N simultaneously with no foil. Phase 4 uses C_D = 1.0 and F_chain = 0 with downward foil force. The implied C_D at equilibrium in Phase 4 is exactly 1.000 (Spot-Check 1), which is within the nominal Phase 1 range; the velocity reduction is due to the additional downward foil load, not an error.

**Assessment:** The Phase 4 SUMMARY (04-01) correctly flags this as a disconfirming observation and lists it as an open question for prototype investigation. The physics is self-consistent. This is a WARNING, not an error — the range extension beyond the Phase 1 envelope is physically motivated and acknowledged.

**Impact:** None on the correctness of the Phase 4 COP calculation. The COP is computed at the self-consistent force-balanced velocity. The sensitivity of v_loop to F_chain = 200 N (which would reduce v_loop further) is not quantified — this is an additional downside risk not reflected in the corrected COP table.

**Recommended action:** Add a sensitivity row in the prototype measurement priorities: quantify F_chain effect on v_loop at the corrected operating point.

---

### WARNING-2: CONVENTIONS.md has not been updated since Phase 0

**Finding:** CONVENTIONS.md states "Last updated: 2026-03-16 (Phase 0 — project initialization)." The file contains no entries for conventions introduced or confirmed in Phases 1 through 4. Several important conventions were established during execution (e.g., Phase 2 F_vert sign convention, PITFALL-M1 guard, N_active_foil=24 splitting, Phase 3 cubic drag-saving formula, Phase 4 co-rotation velocity-scaling rule). These are recorded in STATE.md and SUMMARY frontmatter but not in the authoritative conventions ledger.

**Conventions established post-Phase 0 that should be in CONVENTIONS.md:**
- Phase 2: F_vert = -L×cos(β) - D×sin(β) < 0 (downward sign convention)
- Phase 2: e_oswald = 0.85 (rectangular planform; not 0.9)
- Phase 3: P_drag_saved = P_drag_full × [1-(1-f)^3] (cubic formula, not force formula)
- Phase 3: f_optimal = f_stall (P_corot too small for interior maximum)
- Phase 4: Co-rotation scales as v_loop^3 when v_loop changes

**Assessment:** The conventions themselves are being applied correctly (STATE.md Decisions section tracks them). This is a documentation gap, not a physics error. The risk is that a future phase or review could miss that CONVENTIONS.md is incomplete.

**Impact:** None on current results. Potential for convention drift in future work if CONVENTIONS.md is used as the sole reference without checking STATE.md.

**Recommended action:** Update CONVENTIONS.md to add entries for Phase 2 F_vert sign convention, Phase 2 Oswald efficiency, Phase 3 cubic drag formula, and Phase 4 velocity-scaling rule.

---

### WARNING-3: Co-rotation P_net correction assumes same f_stall at lower v_loop

**Convention/assumption involved:** Phase 3 establishes f_stall = 0.294003 = 1 - 0.9/lambda_max as the stall-limited co-rotation fraction. lambda_max = 1.2748 was derived at v_loop_nominal = 3.7137 m/s.

**Finding:** Phase 4 Plan 02 applies the v^3 correction to P_net_corot using the same f_stall = 0.294 derived at the nominal velocity. However, lambda_max depends on the foil aerodynamics at v_rel, which changes when v_loop changes. At v_loop_corrected = 2.384 m/s with lambda held at 0.9, v_rel = 3.207 m/s (vs 4.976 m/s nominal). The Reynolds number changes from ~Re_nominal to ~Re_corrected = 3.207 × chord / nu_w. Whether lambda_max = 1.2748 remains valid at the corrected Re and v_rel is not verified.

**Assessment:** The Re dependence of lambda_max is a second-order effect (C_L curves do not change dramatically over this Re range for attached flow). The 04-01 SUMMARY notes "Phase 3 P_net at f_stall — f_ss achievable near f_stall" as an approximation with "factor of 2 (C_f uncertainty)" already covering much of this uncertainty. The sensitivity analysis in Plan 02 already varies f_corot from 0 to f_stall, showing COP varies from 0.759 to 0.925 — the correction is modest compared to total uncertainty. This is a minor consistency gap.

**Impact:** Small. The cubic v^3 scaling is the dominant correction; f_stall variation is a second-order term. Given the large C_f uncertainty (±50%, documented in Phase 3), this refinement would not change the NO_GO verdict.

**Recommended action:** Note in open_items_for_prototype that f_stall should be re-evaluated at the corrected operating velocity if prototype data confirms the F_vert direction.

---

## Convention Compliance Matrix (all active conventions vs Phase 4)

| Convention | Introduced | Relevant to Phase 4 | Compliant | Notes |
|---|---|---|---|---|
| z=0 at bottom, z increasing upward | Phase 0 | Indirect (H used) | YES | H = 18.288 m inherited from Phase 1 JSON |
| P(z) = P_atm + rho_w·g·(H-z) | Phase 0 | NO (integrated out in Phase 1) | N/A | Phase 4 uses W_iso, not raw P(z) |
| SI units | Phase 0 | YES | YES | All outputs in SI |
| rho_w = 998.2 kg/m³ | Phase 0 | YES (hull drag, foil forces) | YES | Consistent with force balance |
| g = 9.807 m/s² | Phase 0 | YES (inherited) | YES | — |
| nu_w = 1.004e-6 m²/s | Phase 0 | YES (Re for AoA check) | YES | AoA_final = 10.01 deg; stall check OK |
| Ideal gas, gamma=1.4 | Phase 0 | NO (Phase 1 result used) | N/A | W_adia loaded from Phase 1 JSON |
| N_total=30, N_active=24 | Phase 0/2 | YES | YES | Both pitfall guards confirmed true |
| COP formula structure | Phase 0 | YES | YES | Full balance implemented; no partial COP used for verdict |
| W_buoy = W_iso identity | Phase 0 | YES | YES | Alternative buoy-iso gate COP = 1.000 |
| F_L positive in rotation direction | Phase 0 | YES | YES | F_tan > 0 confirmed at AoA=10 deg |
| F_b positive upward | Phase 0 | YES | YES | — |
| W_jet = 0 explicit | Phase 0 pitfall | YES | YES | Guard present |
| P_corot every cycle | Phase 0 | YES | YES | W_corot = P_net_corot × t_cycle |
| A_frontal = 0.1640 m² | Phase 0 | YES | YES | Consistent with C_D=1.000 at equilibrium |
| F_vert sign: negative=downward | Phase 2 (in STATE.md, not CONVENTIONS.md) | YES | YES | F_vert = -663.86 N consistently negative throughout |
| e_oswald = 0.85 | Phase 2 (in STATE.md) | YES | YES | JSON records e_oswald_used = 0.85 |
| v_loop is upper bound (Phase 1 flag) | Phase 2 (F_vert/F_b_avg=1.15 flag) | YES | YES | Addressed: v_loop_corrected = 2.384 m/s |

---

## End-to-End Research Chain Status

**Chain: Thermodynamics → Buoyancy → Foil Forces → Co-rotation → System COP → Verdict**

| Transfer point | From | To | Status | Test |
|---|---|---|---|---|
| W_adia, W_iso → Phase 4 | Phase 1 | Phase 4 sys02 | PASS | W_pump and W_buoy spot-checks exact |
| v_terminal → F_vert correction | Phase 1 | Phase 4 sys01 | PASS | brentq converged; C_D=1.000 at equilibrium |
| F_vert convention, lambda_design, N_asc → Phase 4 | Phase 2 | Phase 4 sys01 | PASS | Sign convention correctly applied; N=12 confirmed |
| P_net_corot → Phase 4 | Phase 3 | Phase 4 sys03 | PASS with WARNING-3 | Velocity correction applied; f_stall consistency minor caveat |
| sys01 → sys02 | Phase 4 Plan 01 | Phase 4 Plan 01 | PASS | W_foil, t_cycle values consistent between JSON files |
| sys02 → sys03 (COP table reproduction) | Phase 4 Plan 01 | Phase 4 Plan 02 | PASS | COP_table_reproduced verified to match sys02 within floating-point |
| Verdict: NO_GO | Phase 4 Plan 02 | Project conclusion | Consistent | COP_nominal_corrected = 0.925 < 1.0; all 9 scenarios < 1.5 |

**Broken chains:** None

**Assumption violations:** None (all approximations used remain within stated validity domains, except v_loop boundary noted as WARNING-1 — acknowledged by the project)

---

## Narrative Coherence

| Check | Result |
|---|---|
| Problem-method alignment | YES — Research question (COP ≥ 1.5?) is directly answered by the COP table and verdict |
| Result-problem alignment | YES — COP_nominal_corrected = 0.925 < 1.0 directly answers whether the 1.5 W/W target is met |
| Conclusion-evidence alignment | YES — NO_GO verdict is supported by the full corrected COP table (all 9 scenarios < 1.5) |
| Open threads acknowledged | YES — tack-flip losses, F_vert direction, F_chain effect, f_ss correction, and mechanical loss measurement all documented as prototype items |

---

## Summary of Findings

| Category | Count | Severity | Status |
|---|---|---|---|
| Failed spot-checks | 0 of 8 | — | PASS |
| Convention violations | 0 | — | PASS |
| Convention documentation gap | 1 (WARNING-2) | Minor | WARNING |
| Physics boundary condition gap | 1 (WARNING-1: v_loop below Phase 1 range) | Minor (acknowledged) | WARNING |
| Approximation consistency gap | 1 (WARNING-3: f_stall at corrected v_loop) | Minor | WARNING |
| Failed provides/consumes transfers | 0 of 7 | — | PASS |
| Broken research chains | 0 | — | PASS |

**consistency_status: WARNING** — Three minor issues, none invalidating the NO_GO verdict. All are acknowledged or are documentation gaps. The arithmetic is correct, the physics chain is coherent, all pitfall guards are active.

---

_Consistency check completed: 2026-03-18_
_Checker: gpd-consistency-checker (rapid mode)_
