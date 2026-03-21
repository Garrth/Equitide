# Roadmap: Hydrowheel Buoyancy Engine

## Milestones

- **v1.0 Feasibility Study** — Phases 1–4 (completed 2026-03-19) — NO_GO: COP ∈ [0.811, 1.186]; reversed foil mounting invalid design path (kinematic: F_vert opposes motion on both loop halves regardless of orientation)
- **v1.1 AoA Parametric Sweep** — Phases 5–6 (completed 2026-03-21) — NO_GO: COP_max = 1.210 at (η_c=0.85, loss=5%, AoA=2°); η_c*=1.054 exceeds isothermal limit; AoA optimization cannot reach COP=1.5
- **v1.2 Purge Thrust and Tail Foil** — Phases 7–8 (in progress) — GO vs COP = 1.0 threshold (verdict pending)
- **v1.3 Differential Rotation Analysis** — Phases 9–10 (completed 2026-03-21) — NO_GO: COP(r) monotone decreasing; r*=1.0; gain=0.000; multiplicative response geometrically impossible (enhanced-both)

---

## Phases

<details>
<summary>v1.0 Feasibility Study (Phases 1–4) — COMPLETED 2026-03-19</summary>

- [x] Phase 1: Air, Buoyancy & Fill (3/3 plans) — completed 2026-03-17
- [x] Phase 2: Hydrofoil & Torque (2/2 plans) — completed 2026-03-17
- [x] Phase 3: Co-rotation (2/2 plans) — completed 2026-03-18
- [x] Phase 4: System Energy Balance (2/2 plans) — completed 2026-03-18

Full phase details: `.gpd/milestones/v1.0-ROADMAP.md`

</details>

---

<details>
<summary>v1.1 AoA Parametric Sweep (Phases 5–6) — COMPLETED 2026-03-21</summary>

- [x] Phase 5: AoA Sweep Formulation and Anchor Validation (1/1 plans) — completed 2026-03-19
- [x] Phase 6: Full AoA Parametric Sweep and Go/No-Go Verdict (1/1 plans) — completed 2026-03-21

Full phase details: `.gpd/milestones/v1.1-ROADMAP.md`

</details>

---

## v1.2 Purge Thrust and Tail Foil (Phases 7–8)

### Contract Overview

**Central question (v1.2):** Does the Hydrowheel produce net positive energy (COP > 1.0), and what is the corrected COP when purge jet thrust and tail foil lift — two previously excluded contributions — are properly accounted for?

**Decisive outputs required:**
- W_jet_thrust per vessel per cycle (J), derived from first principles
- W_tail_foil per vessel per cycle as a function of chord (J), using NACA foil data at v_exit(z)
- Revised 9-scenario COP table at AoA = 2°, incorporating both contributions
- Verified energy accounting: no double-counting with W_buoy = W_iso identity

**Authoritative prior inputs:**
- phase1 JSON: W_iso = 20,644.6 J; V_air(z) = V_surface × P_atm / P(z); P(z) = P_atm + ρ_w × g × (H − z)
- phase5 solver: analysis/phase5/aoa_sweep_solver.py (brentq framework, validated to 0.001%)
- phase6_verdict.json: COP_max = 1.210 at (η_c=0.85, loss=5%, AoA=2°) — reference baseline
- phase4_summary_table.json: anchor values (v_loop=2.384 m/s, COP_nominal=0.925)

**Forbidden proxies:**
- fp-buoyancy-only: do not accept W_jet_thrust as additive without resolving against W_buoy = W_iso identity
- fp-individual-components: do not report favorable component results without full system balance
- Any COP increase claimed before VALD-01 energy accounting gate is closed

**User-asserted anchor (to verify):** purge jet ~20% additional upward force estimate; tail foil span = 0.457 m

---

### Phase 7: Purge Thrust and Tail Foil Derivation

**Status:** Planned (2 plans)
**Objectives:** PROP-01, PROP-02, TAIL-01, TAIL-02, VALD-01
**Dependencies:** Phase 6 complete (authoritative COP baseline); phase1 JSON (W_iso, V_air(z)); phase5 solver framework

**Plans:**
- [ ] 07-01-PLAN.md -- Open-bottom force balance (PROP-01), F_jet(z) profile (PROP-02), v_exit(z) derivation (TAIL-01), VALD-01 energy accounting gate
- [ ] 07-02-PLAN.md -- Tail foil chord parametric sweep (TAIL-02): W_tail_foil(chord) table, Re validity check, phase 8 handoff

**Goal:** The force balance for the open-bottom vessel is derived from first principles, F_jet(z) and W_jet_thrust are computed analytically, tail foil lift at purge flow velocity is quantified parametrically over chord, and the energy accounting gate confirms whether jet thrust is additive to F_buoy or a restatement of it — so that Phase 8 can incorporate both contributions without double-counting.

**Requirements:** PROP-01 resolves the additive-vs-restatement question that determines the entire framing of v1.2. PROP-02 derives F_jet(z) from first principles to replace the 20% user estimate with a physics-grounded number. TAIL-01 and TAIL-02 derive the tail foil energy at the purge jet exit velocity. VALD-01 closes the energy accounting gate — this is the load-bearing prerequisite for any COP claim in Phase 8.

**Contract Coverage:**
- Decisive output: analytic resolution of PROP-01 (additive or restatement); F_jet(z) profile and W_jet_thrust in J; W_tail_foil(chord) table
- Required anchor: W_iso = 20,644.6 J (phase1 JSON) — used as ceiling for VALD-01 gate
- Required anchor: V_air(z) and P(z) from phase1 JSON — inputs to mass flux derivation
- User-asserted anchor: "~20% additional upward force" — to be verified or refuted by PROP-02
- User-asserted anchor: tail foil span = 0.457 m — held fixed; chord is the sweep variable
- Forbidden proxy: claiming jet is additive without closing VALD-01 first

**Success Criteria:**

1. F_jet(z) is derived from the open-bottom force balance: the isothermal expansion rate dV_air/dt at each height z gives the water ejection mass flux ṁ_w(z) = ρ_w × v_vessel × dV_air/dz; exit velocity v_exit(z) = ṁ_w(z) / (ρ_w × A_opening); reaction force F_jet(z) = ṁ_w(z) × v_exit(z); all terms carry correct SI dimensions throughout [N at each z]

2. VALD-01 energy accounting gate is closed before Phase 8 begins: the comparison (W_buoy + W_jet_thrust) vs W_iso is computed and documented; if W_jet_thrust = 0 (jet already inside buoyancy integral), the gate outcome is stated explicitly; if W_jet_thrust > 0 (genuinely additive), a first-principles justification is provided that does not violate W_buoy = W_iso identity from v1.0

3. The 20% upward force estimate is verified or refuted: W_jet_thrust is computed numerically and compared to 0.20 × W_buoy = 0.20 × 20,644.6 J = 4,128.9 J; the ratio W_jet_thrust / W_buoy is reported to 3 significant figures

4. Tail foil lift integral W_tail_foil is computed at v_exit(z) for NACA 0012 (or NACA 4-digit series at appropriate Reynolds number); span fixed at 0.457 m; chord swept from 0.05 m to 0.457 m; W_tail_foil(chord) is reported in J per vessel per cycle; units confirmed [N × m = J] throughout

5. Reynolds number at v_exit(z) is confirmed to lie in the regime where NACA tabulated C_L and C_D data are applicable (Re > 10^4 for thin foil in water); if v_exit is very low, the limitation is documented explicitly

**Backtracking Triggers:**
- If VALD-01 shows (W_buoy + W_jet_thrust) > W_iso by more than numerical integration error (< 0.01%): energy accounting inconsistency — halt and revise open-bottom force model before Phase 8
- If F_jet(z) derivation reveals jet is entirely inside W_buoy (W_jet_thrust = 0): tail foil still proceeds on its own; Phase 8 must use VALD-01 outcome, not the 20% estimate
- If v_exit at all heights is so low (< 0.01 m/s) that tail foil generates negligible lift (W_tail_foil < 1 J): document and proceed; Phase 8 will show zero contribution from tail foil

---

### Phase 8: Revised System Verdict

**Status:** Pending
**Objectives:** PROP-03, TAIL-03, VALD-02, VALD-03
**Dependencies:** Phase 7 complete — specifically VALD-01 gate closed; W_jet_thrust and W_tail_foil(chord) delivered

**Goal:** The Phase 5 brentq solver is extended to incorporate W_jet_thrust and W_tail_foil; a revised 9-scenario COP table is produced; and the minimum and maximum COP margin above 1.0 are quantified, delivering the final v1.2 go/no-go verdict against the net-positive threshold.

**Requirements:** PROP-03 incorporates F_jet(z) into the coupled force balance so the corrected v_loop reflects the jet thrust contribution. TAIL-03 confirms AoA_optimal sensitivity at (1°, 2°, 3°) with tail foil included. VALD-02 delivers the full revised 9-scenario COP table. VALD-03 closes the v1.2 verdict with minimum and maximum COP margins above 1.0.

**Contract Coverage:**
- Decisive output: revised 9-scenario COP table (η_c ∈ {0.65, 0.70, 0.85} × loss_frac ∈ {0.05, 0.10, 0.15}) at AoA = 2°, including W_jet_thrust + W_tail_foil
- Decisive output: COP margin above 1.0 per scenario — minimum margin (worst case) and maximum margin (best case)
- Required anchor: Phase 6 COP table (phase6_verdict.json) — cross-check: at zero jet/tail contribution, Phase 8 solver must reproduce Phase 6 values to 0.5%
- Required anchor: phase5 brentq solver (analysis/phase5/aoa_sweep_solver.py) — extended, not replaced
- Forbidden proxy: fp-individual-components (reporting W_jet or W_tail alone without full system balance)
- Forbidden proxy: reporting COP increase without verifying VALD-01 non-double-counting

**Success Criteria:**

1. The Phase 5 brentq solver is extended with F_jet(z) included in the upward force balance; at zero jet (F_jet = 0), the extended solver reproduces Phase 6 anchor values (v_loop, COP_nominal) to within 0.5% — continuity check passes before any new results are accepted

2. AoA_optimal sensitivity confirmed: COP is computed at AoA = 1°, 2°, 3° with full W_jet + W_tail included; if AoA_optimal shifts from 2°, the new optimum is identified and documented; if it remains at 2°, scenario-independence is re-confirmed

3. Full revised 9-scenario COP table is produced at AoA_optimal: all nine (η_c, loss_frac) combinations, COP reported to 4 significant figures, matching Phase 6 precision; table includes explicit columns for W_jet_thrust and W_tail_foil contributions so the incremental effect of each is visible

4. GO/NO_GO verdict against COP = 1.0 threshold is delivered for each of the 9 scenarios: minimum-margin scenario (worst case) and maximum-margin scenario (best case) are identified explicitly; verdict states whether all 9, some, or none exceed COP = 1.0

5. Dimensional consistency: all energy terms in the revised COP formula carry units of [J per vessel per cycle]; COP is dimensionless; W_pump denominator is unchanged from Phase 6 (W_pump = W_adia / η_c)

**Backtracking Triggers:**
- If the continuity check (criterion 1) fails by > 0.5%: debug the extended solver before running the sweep; do not accept verdict from a solver that cannot reproduce the Phase 6 baseline
- If AoA_optimal shifts significantly (> 2° from 2°): re-run full AoA sweep at the new optimum before reporting the final COP table; a shifted optimum could change the verdict
- If all 9 scenarios yield COP < 1.0 after adding both contributions: concept fails the net-positive threshold at current geometry; document explicitly and do not soften the verdict

---

---

## v1.3 Differential Rotation Analysis (Phases 9–10)

### Contract Overview

**Central question (v1.3):** If v_water_tangential > v_arm_tangential (water rotating faster than arm assembly), does the shifted apparent flow vector act as a COP multiplier (both higher torque and lower F_vert), an additive boost (more dynamic pressure only), or a negative (stall trigger)?

**Decisive outputs required:**
- AoA_eff(r) and |v_rel|(r) table for r ∈ [1.0, 1.5] at 0.05 increments; stall boundary r_stall
- Force classification table: Γ_h(r) and F_vert(r) vs baseline (r=1.0); response type label
- COP(r) sweep with optimal r* and gain relative to co-rotation baseline; continuity check at r=1.0

**Authoritative prior inputs:**
- phase5 solver: analysis/phase5/aoa_sweep_solver.py (brentq framework, validated to 0.001%)
- phase6_verdict.json: COP at (η_c=0.85, loss=5%, AoA=2°) = 1.210 — continuity anchor
- Phase 5/6 NACA 0012 C_L/C_D interpolator (identical scheme, not re-implemented)

**Forbidden proxies:**
- fp-multiplier-claim: do not classify response as multiplicative without computing F_vert(r) simultaneously with Γ_h(r)
- fp-no-continuity: do not accept COP(r) results before the continuity check at r=1.0 reproduces Phase 6 values to 0.5%
- fp-reimplemented-naca: do not re-implement the NACA interpolator; import from Phase 5/6

**Scope boundary:** No energy accounting for differential rotation — wave energy treated as externally supplied at zero cost.

---

### Phase 9: Differential Rotation Geometry and Force Analysis

**Status:** Completed (2026-03-21) — enhanced-both response; r_stall_onset=1.31; Γ_h up to 4.48×, |F_vert| up to 3.41×; NOT multiplicative
**Objectives:** WAVE-01, WAVE-02
**Dependencies:** Phase 6 complete (AoA=2° baseline, NACA interpolator); Phase 8 complete (v1.2 verdict established)

**Goal:** The apparent flow vector geometry at each speed ratio r is derived from the rotating-arm kinematics established in Phase 5; foil forces (lift, drag, horizontal torque, F_vert) are computed at each r using the Phase 5/6 NACA interpolator; and the force response is classified as multiplicative, additive, or negative relative to the co-rotation baseline (r=1.0).

**Success Criteria:**

1. At r=1.0, AoA_eff and forces reproduce Phase 6 values to within 0.5% — baseline continuity confirmed before any r≠1 results are accepted

2. AoA_eff(r) and |v_rel|(r) are derived from vector geometry (not guessed); the tangential velocity component Δv = (r−1) × v_arm_tangential adds in the plane of rotation; the vertical component v_rel_vertical = v_loop is unchanged (geometric proof required)

3. Stall boundary r_stall is identified: the smallest r where AoA_eff(r) ≥ AoA_stall (NACA 0012 stall ≈ 12–14°); all r values below r_stall are marked valid

4. Force classification table produced: Γ_h(r) / Γ_h(r=1.0) and F_vert(r) / F_vert(r=1.0) at each valid r; response type determined (multiplicative: Γ_h ratio > 1 AND F_vert ratio < 1; additive: Γ_h ratio > 1 AND F_vert ratio ≈ 1; negative: beyond r_stall)

5. Dimensional check: all forces [N], all torques [N·m], all speed ratios dimensionless; v_tangential_net = v_water_tangential − v_arm_tangential [m/s]

**Backtracking Triggers:**
- If r=1.0 baseline fails continuity check: debug vector geometry before proceeding
- If v_rel_vertical is not preserved (geometrically impossible): halt and re-derive the rotating-arm frame

---

### Phase 10: COP Sweep and Differential Rotation Verdict

**Status:** Completed (2026-03-21) — NO_GO; COP(r) monotone decreasing; r*=1.0; gain=0.000; gap to 1.5 = 0.556
**Objectives:** WAVE-03
**Dependencies:** Phase 9 complete — AoA_eff(r), |v_rel|(r), force components at each r

**Plans:**
- [x] 10-01-PLAN.md -- Extended brentq solver at each r; COP(r) sweep at 11 points; r* identification; v1.3 verdict (completed 2026-03-21)

**Goal:** The Phase 5/6 brentq solver is extended with the differential rotation force contributions; COP(r) is computed across the full r ∈ [1.0, 1.5] sweep; the optimal speed ratio r* is identified if a maximum exists; and the v1.3 verdict characterizes the COP response type.

**Success Criteria:**

1. Continuity check at r=1.0: extended solver reproduces Phase 6 COP_nominal to within 0.5% before any r≠1 results are accepted

2. COP(r) computed at 11 points (r = 1.00, 1.05, 1.10, ..., 1.50); COP reported to 4 significant figures; W_pump denominator unchanged from Phase 6

3. Optimal r* identified: if COP(r) has an interior maximum in [1.0, 1.5], r* is located via bisection or Brent's method; if no interior maximum (monotone or stall-limited), the behavior is documented explicitly

4. COP gain = COP(r*) − COP(r=1.0) reported to 3 significant figures; verdict classifies overall response as multiplicative / additive / negative

5. If COP(r*) > COP_v1.2_best_case: flag as significant result; if COP(r*) ≤ COP_v1.2_best_case: document and do not oversell

**Backtracking Triggers:**
- If continuity check fails by > 0.5%: debug the r-extension before accepting any results
- If r_stall < 1.1: water rotation has essentially no safe operating window; document and report zero gain

---

## Phase Dependencies

| Phase | Depends On | Enables | Critical Path? |
| ----- | ---------- | ------- | :---: |
| 7 - Purge Thrust and Tail Foil Derivation | Phase 6 (baseline COP); phase1 JSON; phase5 solver | Phase 8 | Yes |
| 8 - Revised System Verdict | Phase 7 (VALD-01 gate; W_jet_thrust; W_tail_foil) | Phase 9 | Yes |
| 9 - Differential Rotation Geometry and Force Analysis | Phase 8 complete (v1.2 verdict); Phase 5/6 solver + NACA interpolator | Phase 10 | Yes |
| 10 - COP Sweep and Differential Rotation Verdict | Phase 9 (AoA_eff(r), force table) | — | Yes |

**v1.2 critical path:** 7 → 8 (sequential; Phase 8 cannot begin until VALD-01 is closed in Phase 7)
**v1.3 critical path:** 9 → 10 (sequential; Phase 10 depends on Phase 9 force table)

## Risk Register

| Phase | Top Risk | Probability | Impact | Mitigation |
| ----- | -------- | :---------: | :----: | ---------- |
| 7 | W_jet_thrust = 0 (jet inside buoyancy integral; not additive) | HIGH | MEDIUM | Document as VALD-01 outcome; tail foil still computed; Phase 8 proceeds with honest zero |
| 7 | v_exit too low for meaningful tail foil lift | MEDIUM | MEDIUM | Compute Re at v_exit; if Re < 10^4 document limitation; Phase 8 shows zero tail foil contribution |
| 8 | Extended solver fails continuity check vs Phase 6 | LOW | HIGH | Backtrack trigger: debug before accepting any result; do not proceed past criterion 1 |
| 8 | All 9 scenarios still below COP = 1.0 | MEDIUM | HIGH | Report honestly; document which design changes (depth, vessel count) would cross threshold |

---

## Risk Register

| Phase | Top Risk | Probability | Impact | Mitigation |
| ----- | -------- | :---------: | :----: | ---------- |
| 9 | r_stall close to 1.0 — almost no valid speed ratio range | LOW | HIGH | Check AoA_eff at r=1.1 first; if stall, report and close |
| 9 | v_rel_vertical not preserved (incorrect frame derivation) | LOW | HIGH | Geometric proof required in plan; backtrack trigger |
| 10 | COP(r) monotone decreasing — stall dominates before any gain | MEDIUM | MEDIUM | Report honestly; differential rotation is not beneficial |
| 10 | COP gain < 0.01 (negligible) | MEDIUM | MEDIUM | Report; v1.3 closes with "no significant multiplier found" |

---

## Progress

| Milestone | Phases | Plans | Status | Date |
| --------- | ------ | ----- | ------ | ---- |
| v1.0 Feasibility Study | 1–4 | 9/9 | Complete (NO_GO) | 2026-03-19 |
| v1.1 AoA Parametric Sweep | 5–6 | 2/2 | Complete (NO_GO) | 2026-03-21 |
| v1.2 Purge Thrust and Tail Foil | 7–8 | 0/4 | In Progress | — |
| v1.3 Differential Rotation Analysis | 9–10 | 2/2 | Complete (NO_GO) | 2026-03-21 |
