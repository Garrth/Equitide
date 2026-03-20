# Consistency Check — Phase 05 (Rapid Mode)

**Phase:** 05-aoa-sweep-formulation-and-anchor-validation
**Plan checked:** 05-01
**Mode:** rapid
**Date:** 2026-03-19
**Checker:** gpd-consistency-checker

---

## Overall Result

**consistency_status: consistent**

No convention violations, sign errors, factor mismatches, or approximation-validity breaks detected. Phase 5 is
consistent with the full accumulated conventions ledger (Phases 0–4) on all checks performed.

---

## Convention Compliance (All Accumulated Conventions)

Checked Phase 5 artifacts (aoa_sweep_solver.py, phase5_anchor_check.json, 05-01-SUMMARY.md) against every
entry in `.gpd/CONVENTIONS.md`.

| Convention | Introduced | Relevant to Phase 5? | Compliant? | Evidence |
|---|---|---|---|---|
| z = 0 at bottom, z-up | Phase 0 | No (Phase 5 uses algebraic energy balance; no direct P(z) integration) | N/A | H_m=18.288 m loaded correctly for t_cycle = 2H/v_loop |
| P(z) = P_atm + rho_w·g·(H−z) | Phase 0 | No (P(z) integral not evaluated in Phase 5) | N/A | W_buoy_J loaded from Phase 1 JSON which performed the integration |
| SI units throughout | Phase 0 | Yes | Compliant | ASSERT_CONVENTION block: "unit_system=SI". All outputs in N, m/s, J, W |
| rho_w = 998.2 kg/m³ | Phase 0 | Yes | Compliant | Hardcoded in solver: `rho_w = 998.2` (line 140); matches ledger |
| g = 9.807 m/s² | Phase 0 | Yes | Compliant | `g = 9.807` (line 141); not used in Phase 5 computations directly — only loaded quantities depend on it |
| nu_w = 1.004e-6 m²/s | Phase 0 | Marginal (no Re computed in Phase 5) | N/A | Not referenced |
| W_adia = 23,959.45 J (PITFALL-M1) | Phase 1 | Yes | Compliant | W_pump = N_total * W_adia_J / eta_c (line 470); PITFALL-M1 guard confirmed in JSON |
| F_b_avg = W_iso/H = 1128.86 N | Phase 1 | Yes | Compliant | Loaded from phase1_summary_table.json; used in per-vessel force balance |
| v_nominal = 3.7137 m/s | Phase 1 | Yes | Compliant | Loaded from phase1_summary_table.json as v_loop_nominal_ms; used for A_frontal derivation and corot scaling |
| N_active_foil = 24 (PITFALL-N-ACTIVE) | Phase 2 | Yes | Compliant | N_ascending=12, N_descending=12 used for W_foil_total; N_total=30 used for W_pump and W_buoy_total. Guards confirmed in JSON. |
| e_oswald = 0.85 (rectangular planform) | Phase 4 | Yes | Compliant | Loaded from foil01_force_sweep.json foil_geometry.e_oswald (line 99); not 0.9 |
| F_vert sign = negative (downward) | Phase 2 | Yes | Compliant | F_vert = −L·cos(β) − D·sin(β); load-time assertion `assert F_vert < 0` (line 515); JSON confirms negative at AoA = 1, 5, 10, 15 deg |
| AoA parameterization: mount_angle = beta − AoA_target (dynamic) | Phase 5 (new) | Yes | Compliant | Explicitly stated in ASSERT_CONVENTION; proxy-mount-angle-prefixed rejected; anchor confirms 0.0002% match |
| brentq solver (not fixed-point) | Phase 4 | Yes | Compliant | scipy.optimize.brentq with xtol=1e-8, rtol=1e-8; proxy-fixed-vloop rejected |
| Co-rotation P_net scaled by (v_loop/v_nom)³ (PITFALL-COROT) | Phase 4 | Yes | Compliant | `corot_scale = (v_loop_c / v_loop_nominal_ms)**3` (line 457); guard confirmed in JSON |
| W_jet = 0 (PITFALL-C6) | Phase 1 | Yes | Compliant | `W_jet_total = 0.0` explicit (line 461); guard confirmed |
| Per-vessel force balance | Phase 4 | Yes | Compliant | F_net = F_b_avg + F_vert_pv − F_drag_hull (all per-vessel); N_ascending multiplier absent from residual; confirmed by 0.0002% anchor match |
| NACA table interpolation (not thin-airfoil 2π formula) | Phase 2 | Yes | Compliant | ASSERT_CONVENTION: "NACA=table_interpolation_NACA_TR824"; interpolate_naca table data identical to Phase 4 |
| Prandtl lifting-line: C_L_3D = C_L_2D / (1 + 2/AR) | Phase 2 | Yes | Compliant | Line 260: `C_L_3D = C_L_2D / (1.0 + 2.0 / foil_AR)` with AR=4 |
| C_D_i = C_L_3D² / (π·e·AR) | Phase 2 | Yes | Compliant | Line 261: `C_D_i = C_L_3D**2 / (math.pi * e_oswald * foil_AR)` |
| All inputs loaded from JSON (not hardcoded) | Phase 4 | Yes | Compliant | 6 JSON files listed in inputs_loaded_from; N_total=30 is the only physically-constant value hardcoded (justified as physical constant) |
| lambda_design = 0.9 | Phase 2/4 | Yes | Compliant | Loaded from phase2_summary_table.json; used as default in all functions |

**Active conventions checked:** 22
**Compliant:** 19
**Not applicable:** 3
**Violations:** 0

---

## Provides/Consumes Verification

### Quantities Consumed from Earlier Phases

| Quantity | Producer | Consumer (Phase 5) | Meaning Match | Units Match | Test Value Check | Convention Match | Status |
|---|---|---|---|---|---|---|---|
| F_b_avg_N = 1128.86 N | Phase 1 JSON | Force balance residual | Yes — energy-weighted avg buoyancy per vessel | N (SI) | Test: F_b_avg + F_vert(AoA=10°) − F_drag at v=2.384 = 0 → 1128.86 − 663.86 − 465 ≈ 0 N. PASS | Per-vessel; consistent | OK |
| W_adia_J = 23,959.45 J | Phase 1 JSON | W_pump denominator | Yes — adiabatic compression work per vessel | J (SI) | W_pump = 30 × 23959.45 / 0.70 = 1,026,834 J; COP = W_net/W_pump = 0.925 consistent with Phase 4 anchor | PITFALL-M1 guard present | OK |
| v_terminal_nominal = 3.7137 m/s | Phase 1 JSON | A_frontal derivation + corot scaling | Yes — terminal velocity without foil load | m/s (SI) | A_frontal = 2×1128.86/(998.2×1.0×3.7137²) = 0.163998 m² confirmed to 0.0001% | Consistent | OK |
| W_buoy_J = 20,644.62 J | Phase 1 JSON | W_buoy_total = 30 × W_buoy_J | Yes — buoyancy work per vessel = W_iso | J (SI) | 30 × 20644.62 = 619,339 J; identity W_buoy = W_iso preserved | W_iso identity carried forward | OK |
| NACA table + e_oswald=0.85 + AR=4 | Phase 2 JSONs | get_foil_forces_aoa() | Yes — identical table values and foil geometry | Dimensionless + m | interpolate_naca(10.0) = (1.06, 0.013) exact match asserted (line 531–532) | Phase 2 convention unchanged | OK |
| N_ascending=12, N_descending=12 | Phase 2 JSON | W_foil_total | Yes — 24 foil-active vessels | Dimensionless | W_foil_total = 24 × W_foil_pv; guard N_foil_active_24_not_30 confirmed | PITFALL-N-ACTIVE maintained | OK |
| P_net_corot = 46,826 W (uncorrected) | Phase 3 JSON | Co-rotation energy term | Yes — net co-rotation benefit at v_nominal | W (SI) | Cross-check: Phase 3 vs Phase 4 summary ≤ 0.1% (runtime assert line 131–135) | Uncorrected value; v³ scaling applied correctly | OK |
| Anchor: v_loop=2.383479 m/s, F_vert=−663.859 N, COP=0.92501 | Phase 4 JSONs | VALD-01 anchor comparison | Yes — loaded dynamically from JSON; per-vessel F_vert convention confirmed | m/s, N, dimensionless | All three: 0.0002%, 0.0005%, 0.00007% errors vs tolerance 0.5%, 1.0%, 0.5% | Per-vessel convention documented in JSON note field | OK |

**All 8 consumed quantities:** meaning match, units match, test values pass, convention match. Zero failures.

### Quantities Provided to Phase 6

| Quantity | How Provided | Phase 6 Requirement | Verified Available |
|---|---|---|---|
| solve_v_loop_aoa(AoA_target_deg) | Importable function in aoa_sweep_solver.py | Called at each AoA in [1, 15] deg | Yes — module path confirmed |
| compute_COP_aoa(AoA_target_deg, eta_c, loss_frac) | Importable function | Returns COP and all intermediates | Yes — returns full dict |
| overall_anchor_pass = true | phase5_anchor_check.json | Gate: Phase 6 must not run until VALD-01 passes | Yes — JSON exists, overall_anchor_pass=true |

---

## Sign and Factor Spot-Checks

### Spot-check 1: F_vert sign (Eq. 05.1)

**Convention (Phase 2, ledger §7):** F_vert = −L·cos(β) − D·sin(β); negative = downward = opposing buoyancy.

At β = arctan(1/0.9) = 48.01°, AoA = 10°, v_loop = 2.384 m/s:
- v_rel = v_loop × √(1 + λ²) = 2.384 × √(1 + 0.81) = 2.384 × 1.3454 = 3.207 m/s
- q·A_foil = 0.5 × 998.2 × 3.207² × 0.25 = 0.5 × 998.2 × 10.285 × 0.25 = 1285.8 N
- C_L_2D(10°) = 1.06; C_L_3D = 1.06/1.5 = 0.7067
- C_D_i = 0.7067² / (π × 0.85 × 4) = 0.4994 / 10.681 = 0.04676; C_D_total = 0.013 + 0.04676 = 0.05976
- L = 1285.8 × 0.7067 = 908.7 N; D = 1285.8 × 0.05976 = 76.82 N
- F_vert = −908.7 × cos(48.01°) − 76.82 × sin(48.01°) = −908.7 × 0.6691 − 76.82 × 0.7431 = −608.1 − 57.1 = −665.2 N

Compare to JSON: F_vert_phase5_N = −663.862 N. Difference: (665.2 − 663.9)/663.9 = 0.2% (within rounding of spot-check arithmetic). **PASS**

Sign confirmed negative. Direction convention from Phase 2 fully preserved.

### Spot-check 2: Co-rotation v³ scaling (Eq. 05.3, PITFALL-COROT)

**Convention (Phase 4, ledger §10):** P_corot scales with v³ (drag power ∝ v³).

At anchor: v_loop_c = 2.383484 m/s, v_nom = 3.7137 m/s.
- Scale = (2.383484 / 3.7137)³ = (0.6418)³ = 0.26437

JSON: corot_scale_at_anchor = 0.264373. Agreement to 4 significant figures. **PASS**

Phase 4 value for corot_scale was 0.264371 (Phase 4 STATE.md). Phase 5 value 0.264373 differs by 0.0007% (within 1% tolerance gate confirmed in JSON). **PASS**

### Spot-check 3: W_pump denominator (PITFALL-M1)

**Convention (Phase 1):** W_pump uses W_adia = 23,959.45 J, not W_iso = 20,644.62 J.

At anchor (eta_c = 0.70): W_pump_total = 30 × 23,959.45 / 0.70 = 30 × 34,227.79 = 1,026,834 J.

If W_iso had been used in error: W_pump_total = 30 × 20,644.62 / 0.70 = 884,769 J — a 16% difference that would inflate COP by a factor of 1.16.

Code line 470: `W_pump_total = N_total_vessels * W_adia_J / eta_c` — W_adia_J loaded from Phase 1 JSON. Guard flag in JSON: W_pump_uses_W_adia_not_W_iso = true. **PASS**

---

## Approximation Validity Check

Checked Phase 5 parameter values against approximation validity bounds in STATE.md and CONVENTIONS.md.

| Approximation | Validity Condition | Phase 5 Parameter Value | Status |
|---|---|---|---|
| Fixed lambda = 0.9 < lambda_max | lambda_eff < lambda_max = 1.2748 (stall boundary, Phase 3) | lambda_design = 0.9; no lambda_eff variation in Phase 5 (Phase 6 task) | OK — within bounds |
| Quasi-steady foil forces (k << 0.1) | Reduced frequency k = f·c/v_rel < 0.1 | Estimated k ~ 0.02–0.05 at v_loop ≈ 2–3.5 m/s; same regime as Phase 2 validation | OK — unchanged from Phase 2 |
| NACA table Re range (~10⁶) | Re_foil ∈ [5×10⁵, 2×10⁶] | At AoA=10°, v_rel ≈ 3.2 m/s, chord=0.25 m: Re = 3.2×0.25/1.004e-6 = 7.97×10⁵. At AoA=1°, v_rel ≈ 4.65 m/s: Re = 1.16×10⁶. All within table range. | OK |
| Prandtl lifting-line validity (AR ≥ 3, no stall) | AoA < stall angle (~14°) | AoA sweep [1°, 15°]; stall clamp at 14° implemented (line 189, 254); AoA=15° clamped to 14°. Phase 5 notes this in uncertainty table. | OK — clamp applied |
| v_loop > 0 (vessel ascends) | F_b_avg + F_vert_pv > 0 at v_loop → 0 | At AoA=15° (maximum F_vert): F_vert_pv = −668 N vs F_b_avg = 1128.86 N; net = +461 N > 0. Vessel still ascends. | OK |

No approximation validity violations detected.

---

## Convention Changes

The CONVENTIONS.md "Convention Changes" table contains no entries — no formal convention changes have occurred.

Phase 5 introduces one parameterization change (AoA_target is now the free parameter instead of mount_angle being fixed at 38°). This is:
- Documented in SUMMARY.md "Convention Changes" table
- Consistent with Phase 2 vector geometry (mount_angle = beta − AoA_target is algebraically equivalent to the Phase 4 definition AoA_eff = beta − mount_angle, just inverted)
- Not a convention change in CONVENTIONS.md sense — it is a modeling choice about what is the independent variable

No conversion factors needed: the physics equations are identical; only the free parameter identity changed.

---

## Cross-Phase Dependency Chain Integrity

Traced the chain: Phase 1 terminal velocity → Phase 2 foil geometry → Phase 3 co-rotation → Phase 4 anchor → Phase 5 parameterized solver.

Every link verified by test-value substitution above. The Phase 5 anchor reproduction (0.001% error across three quantities) is strong evidence that the full chain is intact in the new solver.

One documented deviation was found and correctly resolved: the Plan pseudocode used `N_ascending × F_vert_pv` in the force balance residual. This was identified as inconsistent with Phase 4's working code (per-vessel balance). The Phase 5 code correctly uses per-vessel balance, confirmed by the 0.0002% anchor match. The deviation is documented in the SUMMARY and the code docstring. **This is not a consistency violation — it is a corrected pseudocode error caught by the anchor gate.**

---

## Issues Found

None.

---

## Summary

| Check | Result |
|---|---|
| Convention compliance (22 checks) | 19 compliant, 3 N/A, 0 violations |
| Provides/consumes pairs (8 consumed, 3 provided) | All pass |
| Sign spot-checks (3) | All pass |
| Factor spot-checks (PITFALL-M1, PITFALL-COROT, PITFALL-N-ACTIVE) | All pass |
| Approximation validity (5 conditions) | All within bounds |
| Convention evolution | 0 formal changes; 1 parameterization inversion (documented, correct) |
| Anchor validation gate | PASS (0.001% error vs 0.5–1.0% tolerance) |
| Phase 6 readiness | overall_anchor_pass = true in JSON |

**Phase 5 is consistent with the full accumulated conventions ledger. No issues block Phase 6.**

---

_Generated: 2026-03-19_
_Mode: rapid_
_Checks performed: 38_
_Issues found: 0_
