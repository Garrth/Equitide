# Roadmap: Hydrowheel Buoyancy Engine

## Milestones

- **v1.0 Feasibility Study** — Phases 1–4 (completed 2026-03-19) — NO_GO: COP ∈ [0.811, 1.186]; reversed foil mounting invalid design path (kinematic: F_vert opposes motion on both loop halves regardless of orientation)
- **v1.1 AoA Parametric Sweep** — Phases 5–6 (active)

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

## v1.1 AoA Parametric Sweep — Active Phases

### Overview

The v1.0 study established a NO_GO verdict at the design AoA of approximately 10°: the self-consistent loop velocity is v_loop = 2.384 m/s (reduced 36% from the uncoupled estimate by the downward F_vert load), yielding COP_nominal = 0.925 across all nine η_c/loss scenarios. The only remaining analytical lever is AoA: smaller AoA reduces F_vert (raising v_loop and co-rotation savings) but simultaneously reduces horizontal torque. This milestone determines whether the optimal trade-off yields COP ≥ 1.5.

**Forbidden design path:** Reversed foil mounting is NOT a valid exploration direction. F_vert is a kinematic consequence of lift being perpendicular to v_rel; it opposes vessel motion on both ascending and descending loop halves regardless of foil orientation. This must not appear in any plan or calculation.

**Solver requirement:** Every AoA point in the sweep must use the same self-consistent brentq coupled solver from Phase 4 — not a fixed v_loop. Co-rotation savings must be re-scaled by (v_loop_corr/v_nom)³ at each AoA point.

**Scenario grid:** Verdict must use the same nine-scenario grid as Phase 4 (η_c ∈ {0.65, 0.70, 0.85} × mechanical loss ∈ {0.05, 0.10, 0.15}).

---

### Phase 5: AoA Sweep Formulation and Anchor Validation

**Status:** Complete ✓
**Started:** 2026-03-19
**Completed:** 2026-03-19

**Goal:** The functional relationships F_vert(AoA) and v_loop(AoA) are derived from the Phase 2 rotating-arm vector geometry, and the coupled brentq solver is verified to reproduce the Phase 4 anchor at AoA ≈ 10° before any new AoA points are computed.

**Dependencies:** Phase 4 locked values (v_loop = 2.384 m/s, COP_nominal = 0.925, F_vert = −663.9 N at AoA ≈ 10°); foil01_force_sweep.json (Phase 2); phase4_summary_table.json

**Objectives:** ANAL-01, ANAL-02, VALD-01

**Contract Coverage:**

- Decisive outputs: F_vert(AoA) analytical expression (ANAL-01); v_loop(AoA) via brentq at each AoA (ANAL-02); anchor match note (VALD-01)
- Required prior outputs: foil01_force_sweep.json (Phase 2 rotating-arm geometry), phase4_summary_table.json (Phase 4 locked anchor values)
- Key anchors: Phase 4 — v_loop = 2.384 m/s, COP_nominal = 0.925 at AoA ≈ 10°, F_vert = −663.9 N (downward)
- Forbidden proxy: F_vert = 0 at any AoA without kinematic proof; fixed v_loop instead of brentq coupled solution; claim that F_vert can be made positive by reversing foil orientation

**Success Criteria:**

1. F_vert(AoA) is expressed analytically as a function of AoA using the rotating-arm vector geometry from Phase 2, with sign convention verified: F_vert is negative (downward) for all AoA in [1°, 15°] at λ = 0.9.
2. The coupled brentq solver, when evaluated at AoA = 10.01° (Phase 4 converged value), reproduces v_loop within 0.5% of the Phase 4 anchor: |v_loop − 2.384| / 2.384 < 0.005.
3. VALD-01 anchor check passes: COP_nominal at AoA ≈ 10° is within 0.5% of the Phase 4 value of 0.925 (i.e., COP ∈ [0.920, 0.930]) — computed directly from the sweep machinery, not inferred.
4. F_vert at AoA = 10° computed by the new formulation agrees with the Phase 4 locked value of −663.9 N to within 1% (|F_vert + 663.9| / 663.9 < 0.01).
5. All intermediate quantities carry correct SI units: F_vert in N, v_loop in m/s, AoA in degrees (converted to radians internally for trigonometry).

**Backtracking Triggers:**

- If anchor check fails (COP at AoA≈10° deviates from 0.925 by more than 0.5%): halt sweep, diagnose discrepancy in F_vert(AoA) derivation or brentq convergence before proceeding to Phase 6.
- If F_vert(AoA) evaluates to positive (upward) at any AoA in [1°, 15°]: recheck vector geometry — this contradicts the Phase 4 kinematic result and must be resolved before any sweep data is trusted.

---

### Phase 6: Full AoA Parametric Sweep and Go/No-Go Verdict

**Status:** Planned (1/1 plan created)
**Started:** 2026-03-19
**Completed:** —

**Plans:** 1 plan
- [ ] 06-01-PLAN.md — Full AoA sweep (≥10 points, 1°–15°), AoA_optimal identification, nine-scenario COP grid, go/no-go verdict

**Goal:** The net COP is computed across AoA ∈ [1°, 15°] using the validated solver, the AoA at which COP is maximized is identified, and the go/no-go verdict on COP ≥ 1.5 is delivered under the same nine-scenario grid as Phase 4.

**Dependencies:** Phase 5 (validated F_vert(AoA) formulation and anchor-verified brentq solver)

**Objectives:** SWEEP-01, SWEEP-02, VERD-01

**Contract Coverage:**

- Decisive outputs: COP(AoA) table across ≥ 10 AoA points (SWEEP-01); AoA_optimal and COP_max identification (SWEEP-02); go/no-go verdict under η_c = 0.70, mechanical loss = 10%, across all nine scenarios (VERD-01)
- Required prior outputs: phase4_summary_table.json (Phase 4 anchor and scenario grid structure); foil01_force_sweep.json (Phase 2 force coefficients)
- Key anchors: W_iso = 20,644.6 J, W_pump at η_c = 0.70 = 34,228 J per vessel; Phase 4 brentq solver (carried forward from Phase 5)
- Forbidden proxies: COP at a single AoA without the full sweep; COP_lossless or Phase 2 upper-bound COP as the primary verdict metric; co-rotation benefit computed at v_nom instead of v_loop_corrected(AoA); any reference to reversed foil mounting as an improvement path

**Success Criteria:**

1. The sweep spans ≥ 10 AoA points from 1° to 15° (inclusive), with all five quantities tabulated to 4 significant figures at each point: F_vert(AoA) in N, v_loop_corrected(AoA) in m/s, horizontal torque W_foil(AoA) in J, co-rotation savings W_corot(AoA) in J (scaled by (v_loop_corrected/v_nom)³), and COP_nominal(AoA) under η_c = 0.70, loss = 10%.
2. F_vert(AoA) and W_foil(AoA) exhibit physically correct monotonic trends: F_vert magnitude decreases as AoA decreases (smaller AoA → smaller lift → smaller vertical drag component); W_foil decreases as AoA decreases (smaller AoA → smaller tangential force). Any non-monotonicity must be explained and verified.
3. AoA_optimal is identified as the angle at which COP_nominal is maximized, with the competing effects quantified: the gain in v_loop (raising co-rotation savings) versus the loss in horizontal torque, expressed as ΔW_corot(AoA) and ΔW_foil(AoA) relative to the AoA = 10° baseline.
4. The go/no-go verdict on COP ≥ 1.5 is delivered under all nine scenario combinations (η_c ∈ {0.65, 0.70, 0.85} × mechanical loss ∈ {0.05, 0.10, 0.15}), using the same table structure as Phase 4. If COP < 1.5 at all AoA points in all nine scenarios, the verdict is NO_GO and the limiting constraint is identified.
5. If COP < 1.5 at all AoA in the nine-scenario grid, the gap is quantified: the AoA and η_c / loss combination that comes closest to 1.5 is reported, and the physical reason the gap cannot be closed by AoA alone is stated (e.g., the F_vert penalty is not reducible to zero, or the horizontal torque loss outpaces the v_loop gain at small AoA).

**Backtracking Triggers:**

- If COP(AoA) is non-monotonic and the maximum occurs at an interior AoA with COP suspiciously close to 1.5: verify the sweep resolution (add intermediate AoA points) and recheck the co-rotation scaling before reporting a GO verdict.
- If the verdict is GO (COP ≥ 1.5 at some AoA): halt and confirm that the winning AoA is not in the stall region (AoA must remain below the foil stall angle, typically 12°–15° for NACA profiles at these Re), and that the brentq convergence was successful at that point, before escalating to milestone complete.

---

## Phase Dependencies

| Phase | Depends On | Enables | Critical Path? |
| ----- | ---------- | ------- | :------------: |
| 5 — AoA Formulation + Anchor | Phase 4 outputs (locked) | Phase 6 | Yes |
| 6 — Full Sweep + Verdict | Phase 5 | Milestone complete | Yes |

**Critical path:** Phase 5 → Phase 6 (2 sequential phases; no parallelism possible — Phase 6 requires Phase 5 anchor validation before any sweep data is trusted)

---

## Risk Register

| Phase | Top Risk | Probability | Impact | Mitigation |
| ----- | -------- | :---------: | :----: | ---------- |
| 5 | Anchor check fails (brentq reproduces wrong v_loop due to AoA parameterization error) | MEDIUM | HIGH | Explicit 0.5% tolerance gate; halt Phase 6 until resolved |
| 5 | F_vert(AoA) derivation inconsistent with Phase 2 vector geometry | LOW | HIGH | Cross-check at AoA=10° against Phase 4 F_vert=−663.9 N to <1% |
| 6 | COP(AoA) peaks slightly above 1.5 at an interior AoA due to numerical artifact | LOW | HIGH | Verify stall check at that AoA; add sweep resolution; confirm brentq convergence |
| 6 | Co-rotation savings collapse at low AoA (v_loop rises but λ_eff approaches stall) | MEDIUM | MEDIUM | Track λ_eff(AoA) = ω·R/v_loop_corrected(AoA); check stall boundary at each point |

---

## Progress

| Milestone | Phases | Plans | Status | Date |
| --------- | ------ | ----- | ------ | ---- |
| v1.0 Feasibility Study | 1–4 | 9/9 | Complete (NO_GO) | 2026-03-19 |
| v1.1 AoA Parametric Sweep | 5–6 | 1/TBD (Phase 5: 1/1) | Active | 2026-03-19 |
