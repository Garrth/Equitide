# Phase 2: Hydrofoil & Torque — Context

**Gathered:** 2026-03-17
**Status:** Ready for planning (CRITICAL: plans written before this context; plans must be revised to match the correct geometry below)

<domain>
## Phase Boundary

Compute the hydrofoil lift/drag forces and shaft torque for the rotating 3-arm Hydrowheel system, sweep the tip-speed ratio λ to find the minimum L/D and minimum λ for COP ≥ 1.5, and confirm that tacked foils on descending vessels generate torque in the same direction as ascending foils.

Requirements: FOIL-01, FOIL-02, FOIL-03, FOIL-04

</domain>

<contract_coverage>
## Contract Coverage

- **claim-foil-forces**: Lift and drag forces computed for NACA 0012 at AoA 5–10°, L/D range 5–30, and λ range 0.5–5. PASS only if velocity triangle correctly uses v_tangential = ω × r as v_h (NOT derived from chain-loop model).
- **claim-ascending-torque**: Net shaft torque from ascending vessel foils per cycle computed. Requires correct rotating-arm geometry: Torque = (L sin β − D cos β) × r × N_ascending_vessels.
- **claim-descending-torque**: Tacked foil on descending vessel confirmed to produce torque in SAME direction as ascending. Requires explicit vector geometry check in rotating-arm frame.
- **claim-min-ld**: Minimum L/D (≤ 20 for prototype green light) and minimum λ for COP ≥ 1.5 identified. Both must be assessed against realistic constraints (L/D achievable by NACA foils at Re ∼ 10⁶; λ achievable by arm rotation at r = 3.66 m).
- **False progress to reject**: Using the chain-loop geometry model (v_h from curved arc or angled straight sections) instead of v_tangential = ω × r. Using L/D as a power multiplier (Pitfall C2). Using v = 3.0 m/s hardcoded instead of Phase 1 JSON value (Pitfall C7).

</contract_coverage>

<user_guidance>
## User Guidance To Preserve

- **User-stated observables:** COP ≥ 1.5 at some achievable λ with L/D ≤ 20 is the prototype green-light criterion. Required L/D > 25 is a stop condition.
- **User-stated deliverables:** Parametric table of (λ, L/D) → COP; minimum λ and minimum L/D for COP ≥ 1.5; phase2_summary_table.json for Phase 3/4 loading.
- **Must-have references / prior outputs:** analysis/phase1/outputs/buoy03_terminal_velocity.json (v_loop = v_terminal), analysis/phase1/outputs/phase1_summary_table.json (W_pump, W_buoy); NACA TR-824 for C_L/C_D data.
- **Stop / rethink conditions:** (a) COP < 1.0 for ALL λ values — concept not viable; (b) required λ_min for COP ≥ 1.5 implies v_tangential > physically achievable arm tip speed — arm must be longer or vessel speed higher; (c) required L/D > 25 — no standard NACA foil achieves this at this Re.

</user_guidance>

<decisions>
## Methodological Decisions

### Geometry — This is the Central Revision to the Existing Plans

The Hydrowheel is a **vertical-axis rotary machine**, NOT a simple bucket-elevator chain drive.

- **3 horizontal arms**, spaced 120° apart, radiating from a central vertical shaft
- Each arm carries **one vertical oval loop** with 10 vessels on a fixed chain
- Arms rotate together at angular velocity ω around the central shaft
- **Power takeoff is rotational** (shaft torque × ω), not linear chain work
- r ≈ **3.66 m** (12 ft) = arm length from shaft centerline to loop centerline (Phase 2 nominal; sweep r to optimize)

**Vessel speeds:**

- All 10 vessels in each loop travel at the **same loop speed v_loop** (fixed chain — ascending vessels go up at v_loop; descending vessels go down at v_loop)
- v_loop ≈ v_terminal from Phase 1 = **3.7137 m/s** (nominal); load from buoy03_terminal_velocity.json
- v_tangential = **ω × r** (arm tip velocity; horizontal, tangential to rotation circle)
- The two speeds are NOT directly coupled by the chain geometry — ω is an independent design variable

**The chain-loop geometry analysis planned in Plan 01 Task 1 (Models A, B, C) is INCORRECT for this design. Replace entirely with the rotating-arm model above.**

### Tip-Speed Ratio (Key Design Parameter)

λ = v_tangential / v_loop = ω × r / v_loop is the primary free parameter for Phase 2.

- **Sweep λ from 0.5 to 5** (or wider if needed)
- For each λ: compute v_tangential = λ × v_loop, then all foil forces and COP
- Find the **minimum λ** for COP ≥ 1.5 and corresponding ω = λ × v_loop / r
- Report whether that ω is physically achievable

Analogy: λ is the tip-speed ratio in VAWT analysis. Optimal λ maximizes shaft power.

### Velocity Triangle (Replaces Chain-Loop v_h Derivation)

For an ascending vessel:

- **v_rel = √(v_loop² + v_tangential²)** — resultant velocity
- **β = arctan(v_loop / v_tangential)** — angle of approach from horizontal (NOT from vertical)
- **AoA_effective = β − mount_angle** — actual angle of attack on foil
- For AoA = 7° (design): mount_angle = β − 7°

For a descending vessel (after tack-flip):

- Same v_rel magnitude (|v_loop| same magnitude, v_tangential same magnitude)
- Flow attacks from forward-and-ABOVE (descending; β measured from horizontal toward above)
- After tack, foil generates lift in same tangential direction as ascending case

**Force decomposition:**

- Tangential force: F_tan = L × sin β − D × cos β (drives shaft rotation)
- Vertical force: F_vert = −L × cos β − D × sin β (opposes ascent for ascending vessel; CHECK SIGN for descending)
- Minimum L/D for net tangential gain: (L/D)_min = v_rel/v_tangential = √(1 + 1/λ²)
  - At λ=1: (L/D)_min = √2 ≈ 1.41 — trivially achieved by any real foil
  - At λ=0.5: (L/D)_min = √5 ≈ 2.24 — still trivial
  - Note: this L/D threshold is MUCH lower than previously assumed in the plans

**Foil mount angle:** Fixed for Phase 2 (design for optimal AoA at nominal λ). Compute mount_angle = arctan(1/λ_design) − AoA_target; sweep AoA_target ∈ [5°, 10°].

### Foil Geometry

- Profile: **NACA 0012** (symmetric; flex-tacking compatible)
- Tacking: **Flexible foil that passively takes the correct tack** (like a sail) — no rigid flip mechanism. An active cam/spring mechanism assists at the top and bottom transition points.
- Span: 1.0 m (nominal; sweep 0.8–1.2 m)
- Chord: 0.25 m (nominal; sweep 0.15–0.35 m)
- AR = span²/A_foil = span/chord ≈ 4 (nominal)
- **AoA from velocity triangle** relative to v_rel direction, NOT relative to vessel axis (Pitfall m2)

### Contributing Vessel Count

Per arm: 4 ascending + 4 descending = **8 contributing foils** (2 vessels per arm in transition at top and bottom of loop).
Total: 8 × 3 arms = **24 contributing foils** (not 30; 6 total are in transition).

### Descending Vessel Tacking

- Descending vessel moves at **v_loop downward + v_tangential** — flow arrives from forward-and-above
- **Flexible foil tacks passively** to face the new flow direction; assisted by active cam/spring at transition
- After tack: foil generates tangential lift force in **SAME rotation direction** as ascending vessel — explicit vector geometry verification required in FOIL-03 (do NOT assume)
- Expected **symmetric contribution**: W_foil_descending ≈ W_foil_ascending (same |v_rel|, same |β|, same foil area)
- Energy cost of active tacking mechanism: estimate and include in Phase 2 energy balance (expected to be small)

### Foil Vertical Force Effect on v_loop

The foil vertical force component (−L cos β − D sin β per ascending vessel) opposes ascent and reduces v_loop below the Phase 1 no-foil terminal velocity.

- **First-order correction only** for Phase 2: compute the foil vertical force at design operating point; if magnitude < 20% of buoyancy force F_b_avg, use Phase 1 v_terminal as v_loop baseline; document the fractional correction.
- Full coupled solution deferred to Phase 4.

### Operating Point Approach

1. Use v_loop = Phase 1 v_terminal (from JSON) as baseline
2. **Sweep λ = v_tangential/v_loop** over [0.3, 5.0] in steps of 0.1
3. For each λ: compute v_tangential = λ × v_loop, v_rel, β, F_tan, W_foil_per_vessel, COP_partial
4. Find **λ_min_for_COP_1.5** (first λ where COP ≥ 1.5) and corresponding ω_min = λ_min × v_loop / r
5. Report: is ω_min physically achievable? (No hard upper limit specified yet; flag for user if ω_min implies unreasonably fast rotation)
6. Also find **L/D_min_for_COP_1.5** at each λ (minimum L/D such that COP ≥ 1.5 for THAT λ)

### Agent's Discretion

- XFOIL validation gate (optional; use NACA TR-824 tabulated values as primary)
- Whether to solve for the coupled (v_loop, ω) system or use first-order correction
- Exact sweep resolution for λ and L/D
- Python script structure and output file layout within analysis/phase2/

</decisions>

<assumptions>
## Physical Assumptions

- **v_loop ≈ v_terminal from Phase 1**: Foil vertical force is a first-order correction to v_loop. Justified if foil drag per vessel << buoyancy force. | Breaks down if foil drag is large (large chord, low λ, high AoA).
- **All vessels in one arm travel at the same speed v_loop**: True by chain constraint (rigid chain). | Breaks down if chain has significant elasticity (not physical for this design).
- **Quasi-steady foil forces**: Reduced frequency k = ω × c / (2 × v_rel) ≈ 0.034 << 0.1 at nominal λ. | Breaks down if k > 0.1 (unsteady corrections needed; not expected here).
- **Prandtl lifting-line valid**: AR ≥ 4 for standard foil geometry. | Breaks down at AR < 3 (use XFLR5 instead).
- **Tacking is perfect (no transition energy loss)**: Optimistic bound. | Active mechanism energy cost should be estimated; if significant, include as loss in COP.
- **f_corot = 0 (no co-rotation)**: Conservative baseline. Phase 3 will parametrize water co-rotation.

</assumptions>

<limiting_cases>
## Expected Limiting Behaviors

- **λ → 0** (arm not rotating): v_tangential → 0; β → 90°; F_tan → L × sin(90°) − D × cos(90°) = L (full lift in tangential direction, zero drag penalty!). But power → F_tan × v_tangential → 0. No shaft power despite maximum tangential force. (Same as Betz limit: zero power at zero speed.)
- **λ → ∞** (arm rotating very fast): β → 0; F_tan → L × 0 − D × 1 = −D < 0 (drag opposes rotation). AoA → 0 → L → 0; system stalls. Shaft power → 0.
- **Optimal λ** between these extremes: maximum shaft power. The sweep must capture this optimum.
- **L/D → 1** (at large λ, threshold L/D → 1): Any real foil exceeds L/D = 1 easily. Net gain is positive for all λ where L/D > (L/D)_min = √(1 + 1/λ²).
- **α = 0°** → C_L = 0 → F_L = 0 → P_net = −F_D × v_rel < 0 (pure drag loss). This is the AoA sanity check.
- **COP_partial(W_foil = 0)** = W_buoy / W_pump = 20,644.62 / 34,227.8 = **0.6032** — this is the anchor from Phase 1. Any result must reproduce this when L = 0.

</limiting_cases>

<anchor_registry>
## Active Anchor Registry

- **analysis/phase1/outputs/buoy03_terminal_velocity.json**: v_loop baseline (v_terminal nominal = 3.7137 m/s)
  - Why it matters: v_loop sets the scale for all foil forces and the λ sweep. Do NOT hardcode 3.0 m/s (Pitfall C7).
  - Carry forward: planning, execution, verification
  - Required action: read, load, use

- **analysis/phase1/outputs/phase1_summary_table.json**: W_pump, W_buoy, W_foil_net target
  - Why it matters: COP formula denominator (W_pump) and numerator anchor (W_buoy). W_foil target = 1.5 × W_pump − W_buoy = 30,697 J per vessel at η_c=0.70.
  - Carry forward: planning, execution, verification
  - Required action: read, load, use

- **NACA TR-824** (Abbott, von Doenhoff & Stivers, 1945 — NASA NTRS): C_L(α), C_D(α) at Re ∼ 10⁶
  - Why it matters: Primary 2D section polars for force computation.
  - Carry forward: execution, verification
  - Required action: cite, embed tabulated values in analysis script

- **Rotating-arm geometry (this CONTEXT.md)**: v_tangential = ω × r = λ × v_loop
  - Why it matters: Replaces the incorrect chain-loop geometry analysis in Plans 01-02. Executor MUST use this geometry, not the Model A/B/C in the existing plans.
  - Carry forward: execution (Plan 01 Task 1 MUST be revised)
  - Required action: use, replace existing model

</anchor_registry>

<skeptical_review>
## Skeptical Review

- **Weakest anchor:** The arm length r = 3.66 m is the full tank radius — loops at the wall. Mechanically, this requires loops to travel in a large-radius circle. The actual usable r may be smaller due to structural constraints. Phase 2 should sweep r down to 2.0 m as a sensitivity check.
- **Unvalidated assumptions:** Water co-rotation is set to zero (f_corot = 0). In reality, as the arms rotate, they will drag the water tangentially. Some co-rotation will develop naturally, which REDUCES v_tangential (water moves with the arm → less relative flow → less AoA). This is the mechanism Phase 3 quantifies.
- **Competing explanation:** If the water co-rotates significantly, the effective λ_eff = (v_tangential − v_water) / v_loop < λ. The concept may REQUIRE water not to co-rotate — which may be a design challenge. Phase 3 must address this.
- **Disconfirming check:** If the optimal λ for max shaft power corresponds to ω_opt = 0.1 rpm (very slow), then v_tangential = 0.1 × (2π/60) × 3.66 = 0.038 m/s — much less than v_loop = 3.7 m/s. This would mean β ≈ 89°, foil nearly perpendicular to flow, tiny tangential force, large drag. This would be a design failure.
- **False progress to reject:** COP_partial > 1.5 computed while ignoring the foil vertical force drag reduction on v_loop. The foil drag reduces v_loop, which reduces W_buoy, which reduces COP. This coupling must be estimated, not ignored.

</skeptical_review>

<deferred>
## Deferred Ideas

- **Co-rotation of water**: The arm rotation will naturally entrain water. How much co-rotation develops and how quickly? This could significantly reduce the effective v_tangential experienced by the foils. Scope of Phase 3.
- **Optimal arm length r**: Phase 2 sweeps r from 2.0–3.66 m. Full optimization is Phase 4.
- **Foil profile optimization (NACA 4412 vs 0012)**: Cambered profiles give higher L/D at fixed AoA but complicate tacking. Deferred to prototype optimization.
- **Tack-flip energy cost**: Active cam/spring mechanism energy cost. Estimate in Phase 2; detailed design is prototype scope.
- **Centripetal effects on vessel**: At ω × r, the vessel experiences centrifugal force (outward). At ω = 1 rpm, a = ω² × r = (2π/60)² × 3.66 = 0.04 m/s² (0.4% of g). Negligible; flag if ω > 10 rpm.
- **Multi-foil interactions**: If each vessel has multiple foils (e.g., two foils for upward + downward forces), performance could improve. Post-prototype.

</deferred>

---

_Phase: 02-hydrofoil-torque_
_Context gathered: 2026-03-17_
