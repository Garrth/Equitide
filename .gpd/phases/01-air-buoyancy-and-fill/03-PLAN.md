---
phase: 01-air-buoyancy-and-fill
plan: 03
type: execute
wave: 3
depends_on: ["01-01", "01-02"]
files_modified:
  - analysis/phase1/fill_feasibility.py
  - analysis/phase1/outputs/fill01_window.json
  - analysis/phase1/outputs/fill02_flow_rate.json
  - analysis/phase1/outputs/fill03_feasibility.json
  - analysis/phase1/outputs/phase1_summary_table.json
  - docs/phase1_results.md
interactive: false

conventions:
  units: "SI primary (m, m³, m/s, m³/s, J, Pa); CFM and SCFM in parentheses for compressor specification"
  flow_rate_at_depth: "Q_depth is volumetric flow rate at P_bottom = 280,500 Pa (the actual delivery pressure)"
  scfm_definition: "SCFM = standard cubic feet per minute at P_atm = 101,325 Pa and 20°C; commercial compressor rating unit"
  conversion: "1 m³/s = 2118.88 CFM; Q_free_SCFM = Q_depth_CFM * P_r = Q_depth_CFM * 2.770"
  fill_arc: "Fill window = 1/4 loop circumference = 2*pi*R_tank/4; vessel travels this arc during fill; time = arc / v_vessel"
  velocity_source: "v_vessel values from buoy03_terminal_velocity.json v_handoff range; do NOT use v=3.0 m/s fixed value (Pitfall C7)"

dimensional_check:
  t_fill: "[m / (m/s)] = [s]"
  Q_depth: "[m³ / s] = [m³/s]"
  Q_CFM: "[m³/s * 2118.88 CFM/(m³/s)] = [CFM]"
  Q_SCFM: "[CFM * P_r] = [SCFM]; P_r dimensionless"
  arc_length: "[m]"
  P_delivery_psig: "[(Pa - 101325) / 6894.76] = [psig]"

approximations:
  - name: "circular loop geometry"
    parameter: "Loop approximated as circle of radius R_tank = 3.66 m; arc = 2*pi*R_tank/4"
    validity: "Real loop shape (chain loop around sprockets) differs from circle; arc length uncertainty ±5%"
    breaks_when: "Never for this feasibility level"
    check: "Arc = 5.749 m confirmed in Plan 01 sanity checks"
  - name: "uniform velocity during fill"
    parameter: "v_vessel is taken as constant over the fill arc"
    validity: "Terminal velocity is an equilibrium; the vessel is near terminal during most of the ascent"
    breaks_when: "Fill arc is at the very beginning of ascent where vessel is still accelerating"
    check: "Sensitivity: t_fill computed at full v_range [2.0, 4.0] m/s; lower velocity is conservative"
  - name: "instantaneous ideal fill"
    parameter: "Air fills the vessel to exactly V_depth within t_fill with no pressure losses in the delivery hose"
    validity: "This is a feasibility-level assessment; Phase 4 adds 10–20% pipe friction factor to W_pump"
    breaks_when: "Never for this go/no-go assessment; pipe friction noted as add-on"
    check: "FILL-03 feasibility note explicitly flags pipe friction as not included here (Pitfall M5)"

contract:
  scope:
    question: "Is it physically feasible to fill the vessel with air within the 1/4-loop window, and what class of commercial compressor is required?"
  claims:
    - id: claim-fill-window
      statement: "The fill window duration is t_fill = 5.749 / v_vessel; at v_vessel in [2.0, 4.0] m/s, t_fill ranges from 1.437 s to 2.875 s. At the nominal terminal velocity of 3.714 m/s, t_fill = 1.548 s."
      deliverables: [deliv-fill-window]
      acceptance_tests: [test-arc-length, test-tfill-3ms, test-tfill-range]
      references: [ref-plan01-sanity, ref-plan02-velocity]
    - id: claim-flow-rate
      statement: "The required air flow rate spans Q_free = 147–295 SCFM across the plausible velocity range [2.0, 4.0] m/s. At the nominal terminal velocity (3.714 m/s), Q_free = 274 SCFM at delivery pressure P_bottom = 280,500 Pa = 40.7 psig."
      deliverables: [deliv-flow-rate]
      acceptance_tests: [test-qfree-3ms, test-qfree-range, test-unit-consistency]
      references: [ref-plan01-vdepth]
    - id: claim-fill-feasible
      statement: "The required flow rates (147–295 SCFM at ~40 psig) are achievable with mid-to-large industrial compressed air equipment. Fill is declared commercially feasible across the full v_vessel range."
      deliverables: [deliv-feasibility]
      acceptance_tests: [test-feasibility-verdict]
      references: [ref-compressor-class]
    - id: claim-phase1-complete
      statement: "Phase 1 delivers: W_iso = 20,640 J, W_pump range = 28,188–36,861 J, W_buoy = W_iso (identity confirmed), v_terminal range = [2.53, 4.15] m/s, fill feasibility = GO. All 9 requirements (THRM-01 through FILL-03) are satisfied."
      deliverables: [deliv-summary-table, deliv-results-doc]
      acceptance_tests: [test-all-requirements]
      references: [ref-plan01-output, ref-plan02-output]
  deliverables:
    - id: deliv-fill-window
      kind: code_output
      path: "analysis/phase1/outputs/fill01_window.json"
      description: "t_fill at each v_vessel in [2.0, 2.5, 3.0, 3.5, 3.714, 4.0] m/s; arc_length used"
      must_contain: ["arc_length_m", "v_vessel_ms", "t_fill_s"]
    - id: deliv-flow-rate
      kind: code_output
      path: "analysis/phase1/outputs/fill02_flow_rate.json"
      description: "Q_depth (m³/s), Q_depth (CFM), Q_free (SCFM) at each v_vessel; delivery pressure in Pa and psig"
      must_contain: ["Q_depth_m3s", "Q_depth_CFM", "Q_free_SCFM", "P_delivery_psig"]
    - id: deliv-feasibility
      kind: code_output
      path: "analysis/phase1/outputs/fill03_feasibility.json"
      description: "Per-velocity feasibility verdict, compressor class, pipe friction caveat, binary go/no-go"
      must_contain: ["feasible", "compressor_class", "pipe_friction_note", "go_nogo"]
    - id: deliv-summary-table
      kind: code_output
      path: "analysis/phase1/outputs/phase1_summary_table.json"
      description: "All key Phase 1 results in one table: W_iso, W_pump range, W_buoy, v_terminal range, t_fill range, Q_free range, fill feasibility"
      must_contain: ["W_iso_J", "W_pump_min_J", "W_pump_max_J", "identity_error_pct", "v_terminal_nominal_ms", "Q_free_nominal_SCFM", "fill_go_nogo"]
    - id: deliv-results-doc
      kind: markdown
      path: "docs/phase1_results.md"
      description: "Human-readable Phase 1 results summary with component table, key findings, and Phase 2 handoff"
      must_contain: ["W_iso", "W_pump", "v_terminal", "fill feasibility", "COP break-even", "Phase 2 inputs"]
  references:
    - id: ref-plan01-sanity
      source: ".gpd/phases/01-air-buoyancy-and-fill/01-01-SUMMARY.md"
      anchor: "Arc length = 5.749 m confirmed in Plan 01 sanity check 6"
    - id: ref-plan02-velocity
      source: ".gpd/phases/01-air-buoyancy-and-fill/01-02-SUMMARY.md and buoy03_terminal_velocity.json"
      anchor: "v_handoff: nominal 3.714 m/s, conservative 3.075 m/s, range [2.530, 4.152] m/s"
    - id: ref-plan01-vdepth
      source: ".gpd/phases/01-air-buoyancy-and-fill/01-01-SUMMARY.md and thrm01_compression_work.json"
      anchor: "V_depth = 0.07228 m³ is the air volume to inject at P_bottom = 280,500 Pa per cycle"
    - id: ref-compressor-class
      source: ".gpd/phases/01-air-buoyancy-and-fill/01-EXPERIMENT-DESIGN.md Section 4 FILL-03"
      anchor: "Commercial single-stage reciprocating and rotary-screw compressors rated 40–125 psig span 10–500 SCFM; 147–295 SCFM achievable with medium-industrial units"
    - id: ref-plan01-output
      source: "analysis/phase1/outputs/thrm01_compression_work.json"
      anchor: "W_iso, W_adia, W_pump table, COP_ideal_max table"
    - id: ref-plan02-output
      source: "analysis/phase1/outputs/buoy02_identity_gate.json, analysis/phase1/outputs/buoy03_terminal_velocity.json"
      anchor: "Identity gate passed; 15-point terminal velocity table"
  acceptance_tests:
    - id: test-arc-length
      subject: claim-fill-window
      kind: numerical
      procedure: "Compute arc_length = 2 * pi * R_tank / 4. Compare to 5.749 m."
      pass_condition: "abs(arc_length - 5.749) < 0.005 m"
      evidence_required: [deliv-fill-window]
    - id: test-tfill-3ms
      subject: claim-fill-window
      kind: numerical
      procedure: "Compute t_fill at v = 3.0 m/s. Compare to 1.916 s."
      pass_condition: "abs(t_fill(3.0) - 1.916) < 0.005 s"
      evidence_required: [deliv-fill-window]
    - id: test-tfill-range
      subject: claim-fill-window
      kind: numerical
      procedure: "Verify t_fill values at v=2.0 and v=4.0 m/s match expected range. Verify t_fill is monotone decreasing with v."
      pass_condition: "t_fill(2.0) in [2.85, 2.90] s; t_fill(4.0) in [1.43, 1.45] s; t_fill strictly decreasing with v"
      evidence_required: [deliv-fill-window]
    - id: test-qfree-3ms
      subject: claim-flow-rate
      kind: numerical
      procedure: "Compute Q_free at v = 3.0 m/s: Q_depth = V_depth / t_fill(3.0) = 0.07228 / 1.916; convert to SCFM via P_r. Compare to 221 SCFM."
      pass_condition: "Q_free(3.0 m/s) in [215, 228] SCFM (±3% of 221 SCFM)"
      evidence_required: [deliv-flow-rate]
    - id: test-qfree-range
      subject: claim-flow-rate
      kind: numerical
      procedure: "Verify Q_free at v=2.0 m/s ≈ 147 SCFM and at v=4.0 m/s ≈ 295 SCFM. Verify Q_free is monotone increasing with v."
      pass_condition: "Q_free(2.0) in [142, 152] SCFM; Q_free(4.0) in [288, 302] SCFM; monotone increasing"
      evidence_required: [deliv-flow-rate]
    - id: test-unit-consistency
      subject: claim-flow-rate
      kind: dimensional
      procedure: "Verify unit conversion chain: Q_depth [m³/s] * 2118.88 [CFM/(m³/s)] = Q_depth [CFM]. Q_depth [CFM] * P_r [dimensionless] = Q_free [SCFM]. Check at v=3.0 m/s: Q_depth = 0.03772 m³/s = 79.9 CFM; Q_free = 79.9 * 2.770 = 221 SCFM."
      pass_condition: "0.03772 * 2118.88 = 79.9 ± 0.5 CFM; 79.9 * 2.770 = 221 ± 2 SCFM"
      evidence_required: [deliv-flow-rate]
    - id: test-feasibility-verdict
      subject: claim-fill-feasible
      kind: physics_consistency
      procedure: "Verify all velocity points in [2.0, 4.0] m/s receive a 'feasible' verdict. Verify delivery pressure is correctly computed as P_bottom - P_atm in psig = (280500 - 101325) / 6894.76 ≈ 26.0 psig. Note: delivery pressure is absolute 40.7 psi or gauge 26.0 psig; confirm which is reported and that compressor spec refers to gauge."
      pass_condition: "All v_vessel points marked feasible; delivery pressure = 40.7 psia = 26.0 psig correctly distinguished; pipe friction caveat present in JSON"
      evidence_required: [deliv-feasibility]
    - id: test-all-requirements
      subject: claim-phase1-complete
      kind: completeness
      procedure: "Verify phase1_summary_table.json contains results covering all 9 requirements: THRM-01 (W_iso, W_adia, W_pump), THRM-02 (V_depth, V_surface), THRM-03 (W_jet=0 documented), BUOY-01 (F_b profile), BUOY-02 (identity gate), BUOY-03 (v_terminal table), FILL-01 (t_fill), FILL-02 (Q_free), FILL-03 (feasibility verdict)."
      pass_condition: "All 9 requirement IDs appear in the summary document with their key outputs"
      evidence_required: [deliv-summary-table, deliv-results-doc]
  forbidden_proxies:
    - "Do NOT fix v_vessel = 3.0 m/s for fill calculations. The fill window and flow rate must be computed across the full velocity range from buoy03_terminal_velocity.json [2.0, 4.0] m/s. The 3.0 m/s value is the user's preliminary estimate, not a physics-derived result. (Pitfall C7)"
    - "Do NOT use Q_depth (flow rate at depth pressure) as the compressor rating. Compressors are rated in SCFM (free air). Q_free = Q_depth_CFM * P_r. Specifying a compressor as 80 CFM when the system needs 221 SCFM would be a factor of 2.77 undersizing error."
    - "Do NOT omit the pipe friction caveat. The fill calculation assumes ideal delivery with no line losses. Real systems add 10–20% to required pump energy. This is noted here; it is added to the COP denominator in Phase 4. (Pitfall M5)"
    - "Do NOT report fill feasibility as a COP contribution. Fill feasibility answers the question 'can we physically fill the vessel in time?' It does not contribute energy to the output side of the balance. The compressor energy is entirely on the input side."
  uncertainty_markers:
    weakest_anchors:
      - "Loop arc length: modeled as 1/4 of a perfect circle (C_loop/4 = 5.749 m). The actual loop around two sprockets is flatter at the top and bottom. Uncertainty ±5% on arc length → ±5% on t_fill and Q_free."
      - "Compressor availability at 40 psig and 200–300 SCFM: based on general knowledge of compressed air market. Actual procurement depends on availability, cost, and power draw. Phase 4 will assess compressor power as part of total system power balance."
      - "Delivery pressure is P_bottom = 280,500 Pa = 40.7 psia = 26.0 psig. Standard compressed air ratings sometimes use 100 psig as a reference point. A compressor rated at 221 SCFM at 100 psig will deliver less SCFM at 40 psig (higher delivery volume at lower pressure). This works in the system's favor — a smaller compressor is needed than the 100-psig rating might suggest."
    disconfirming_observations:
      - "If Q_free at any v_vessel point exceeds 400 SCFM, raise a fill feasibility concern. This would require industrial-scale compressors and may be cost-prohibitive. The expected maximum is ~295 SCFM at 4.0 m/s."
      - "If t_fill is less than 1.0 s at any point in the velocity range, reconsider whether a practical fill valve can open, fill, and close that fast. The expected minimum at 4.0 m/s is 1.437 s — above mechanical valve speeds of 0.1–0.5 s."
      - "If computed P_delivery (psig) is significantly different from 26 psig, recheck the absolute vs gauge pressure conversion: P_gauge = P_absolute - P_atm = 280500 - 101325 = 179175 Pa = 26.0 psig."

estimated_execution:
  total_minutes: 40
  breakdown:
    - task: 1
      minutes: 20
      note: "Fill window and flow rate calculations, unit conversions, sweep over v_range"
    - task: 2
      minutes: 20
      note: "Feasibility assessment, Phase 1 summary table, results document"

patterns_consulted:
  insights: []
  error_patterns: []
  adjustments_made:
    - "Explicit note on SCFM vs CFM-at-depth distinction to prevent factor of P_r undersizing error"
    - "Velocity range sourced from Plan 02 JSON output, not hardcoded, per Pitfall C7"
    - "Pipe friction caveat (Pitfall M5) documented as forward pointer to Phase 4 pump energy"
    - "Absolute vs gauge pressure distinguished explicitly in FILL-03 feasibility assessment"
---

<objective>
Compute the fill window duration (FILL-01), required air flow rate in SCFM (FILL-02), and assess practical feasibility against commercial compressor capabilities (FILL-03). Consolidate all Phase 1 results into a phase summary.

Purpose: The fill feasibility calculation closes the air/buoyancy subsystem analysis. It answers whether the physical injection system can keep up with the vessel throughput. The velocity range from Plan 02 (BUOY-03) drives this calculation — using only v = 3.0 m/s would understate the flow rate requirement at the nominal terminal velocity (3.71 m/s). The Phase 1 summary table locks the handoff values for Phases 2 and 3.

Output: fill01_window.json, fill02_flow_rate.json, fill03_feasibility.json, phase1_summary_table.json, docs/phase1_results.md.
</objective>

<execution_context>
@C:/Users/garth/.claude/get-physics-done/workflows/execute-plan.md
@C:/Users/garth/.claude/get-physics-done/templates/summary.md
</execution_context>

<context>
@.gpd/PROJECT.md
@.gpd/CONVENTIONS.md
@.gpd/phases/01-air-buoyancy-and-fill/01-EXPERIMENT-DESIGN.md
@.gpd/phases/01-air-buoyancy-and-fill/01-01-SUMMARY.md
@.gpd/phases/01-air-buoyancy-and-fill/01-02-SUMMARY.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: Fill window and flow rate (FILL-01, FILL-02)</name>
  <files>analysis/phase1/fill_feasibility.py, analysis/phase1/outputs/fill01_window.json, analysis/phase1/outputs/fill02_flow_rate.json</files>
  <action>
    Create analysis/phase1/fill_feasibility.py.

    STEP 1 — LOAD UPSTREAM RESULTS:
      Load from buoy03_terminal_velocity.json:
        v_handoff = data["v_handoff"]
        v_nominal = v_handoff["nominal"]        # 3.714 m/s (C_D=1.0, F_chain=0)
        v_conservative = v_handoff["conservative"]  # 3.075 m/s
        v_range = v_handoff["range"]            # [2.530, 4.152]

      Load from thrm01_compression_work.json:
        V_depth = data["V_depth_m3"]            # 0.07228 m³
        P_r = data["P_r"]                       # 2.770
        P_bottom = data["P_bottom_Pa"]          # 280,500 Pa

      DO NOT HARDCODE these values. Read from JSON files.
      Assert V_depth in [0.0720, 0.0726] m³; assert P_r in [2.760, 2.780]; assert P_bottom in [280000, 281000] Pa.

    STEP 2 — FILL-01: FILL WINDOW DURATION:
      Constants:
        R_tank = 3.66 m  (from CONVENTIONS.md §4)
        arc_length = 2 * math.pi * R_tank / 4
        Assert abs(arc_length - 5.749) < 0.005 m

      Velocity sweep: v_list = [2.0, 2.5, 3.0, 3.5, v_nominal, 4.0]
        (Include the physics-derived nominal terminal velocity as an explicit data point)

      For each v in v_list:
        t_fill = arc_length / v
        Assert t_fill > 0.5, "Fill window < 0.5 s — valve actuation concern"
        Assert t_fill < 10.0, "Fill window > 10 s — unreasonably slow vessel"

      Cross-checks:
        Assert abs(arc_length / 3.0 - 1.916) < 0.005 (t_fill at 3 m/s matches CONVENTIONS.md)
        Assert arc_length / 2.0 > arc_length / 4.0 (slower vessel → longer window — obvious but check)

      Dimensional check: [arc_length / v] = [m / (m/s)] = [s] — correct

      Save fill01_window.json: arc_length_m, v_vessel_ms (list), t_fill_s (list)

    STEP 3 — FILL-02: REQUIRED FLOW RATE:
      For each (v, t_fill) pair from FILL-01:
        Q_depth_m3s = V_depth / t_fill              # m³/s at P_bottom
        Q_depth_CFM = Q_depth_m3s * 2118.88         # CFM at depth pressure
        Q_free_SCFM = Q_depth_CFM * P_r             # SCFM (free air equivalent at P_atm)

      Cross-check unit conversion at v = 3.0 m/s:
        Assert abs(Q_depth_m3s - 0.03772) < 0.001 at v=3.0
        Assert abs(Q_depth_CFM - 79.9) < 1.0 at v=3.0
        Assert abs(Q_free_SCFM - 221) < 3 at v=3.0

      Note on delivery pressure:
        P_delivery_psia = P_bottom / 6894.76          # psia (absolute)
        P_delivery_psig = (P_bottom - 101325) / 6894.76  # psig (gauge — what compressor specs use)
        Assert abs(P_delivery_psia - 40.70) < 0.10
        Assert abs(P_delivery_psig - 26.0) < 0.5
        Document both: "Delivery pressure = 40.7 psia = 26.0 psig.
                        Commercial compressor specs use gauge pressure (psig).
                        This is below the standard 40 psig or 100 psig compressor spec ratings;
                        the system operates in the easily-achievable range."

      Dimensional checks:
        [Q_depth_m3s] = [m³] / [s] = [m³/s] — correct
        [Q_depth_CFM] = [m³/s * 2118.88 CFM/(m³/s)] — correct
        [Q_free_SCFM] = [CFM * P_r] = [CFM * (P_bottom/P_atm)] = [SCFM] — correct
          The P_r factor converts "compressed air at depth" to "equivalent free air volume per unit time"
          using Boyle's law: Q_free * P_atm = Q_depth * P_bottom (mass-equivalent at standard conditions)

      Save fill02_flow_rate.json: for each v_vessel: v_ms, t_fill_s, Q_depth_m3s, Q_depth_CFM,
        Q_free_SCFM, P_delivery_psia, P_delivery_psig
  </action>
  <verify>
    1. arc_length = 5.749 ± 0.005 m
    2. t_fill at v=3.0 m/s = 1.916 ± 0.005 s (CONVENTIONS.md cross-check)
    3. t_fill at v=2.0 m/s in [2.85, 2.90] s; t_fill at v=4.0 m/s in [1.43, 1.45] s
    4. t_fill is monotone decreasing with v (all 6 values)
    5. Q_depth = 0.03772 ± 0.001 m³/s at v=3.0 m/s
    6. Q_free = 221 ± 3 SCFM at v=3.0 m/s (matches CONVENTIONS.md Appendix B test value)
    7. Q_free at v=2.0 m/s in [142, 152] SCFM; at v=4.0 m/s in [288, 302] SCFM
    8. Q_free monotone increasing with v (all 6 values)
    9. P_delivery_psia = 40.70 ± 0.10; P_delivery_psig = 26.0 ± 0.5
    10. All assertion checks pass; no hardcoded constants (all loaded from JSON)
    11. Both JSON files created with correct fields
  </verify>
  <done>fill01_window.json written with t_fill at 6 velocity points. fill02_flow_rate.json written with Q_free in SCFM at each velocity point, delivery pressure in both psia and psig, unit conversion verified at v=3.0 m/s reference point. FILL-01 and FILL-02 requirements satisfied.</done>
</task>

<task type="auto">
  <name>Task 2: Feasibility assessment and Phase 1 summary (FILL-03 + integration)</name>
  <files>analysis/phase1/fill_feasibility.py, analysis/phase1/outputs/fill03_feasibility.json, analysis/phase1/outputs/phase1_summary_table.json, docs/phase1_results.md</files>
  <action>
    Continue in fill_feasibility.py (append after STEP 3).

    STEP 4 — FILL-03: FEASIBILITY ASSESSMENT:
      For each (v_vessel, Q_free_SCFM) from FILL-02:
        Classify compressor class:
          if Q_free_SCFM < 50:   compressor_class = "Small portable (<50 SCFM)"
          elif Q_free_SCFM < 150: compressor_class = "Large portable / small industrial (50–150 SCFM)"
          elif Q_free_SCFM < 300: compressor_class = "Medium industrial rotary screw (150–300 SCFM)"
          elif Q_free_SCFM < 600: compressor_class = "Large industrial (300–600 SCFM)"
          else:                   compressor_class = "Very large industrial (>600 SCFM) — flag for review"

        feasible = Q_free_SCFM <= 300  # conservatively; 300 SCFM is the upper range of standard mid-industrial
        (All expected values 147–295 SCFM are below this threshold)

      Deliver pressure note (one entry in JSON, not per row):
        "Delivery pressure is 40.7 psia (26.0 psig). This is within the rated range of standard
         single-stage reciprocating and rotary-screw compressors (typical max 100–175 psig for these
         classes). No special high-pressure equipment is required."

      Pipe friction caveat (mandatory per Pitfall M5):
        pipe_friction_note = "This analysis assumes ideal air delivery with no line losses.
         Real installation adds 10–20% to pump energy for pipe friction, check valves,
         and nozzle losses. Phase 4 COP calculation will include a pipe friction factor
         of 1.10–1.20 × W_adia / eta_c. This does NOT affect fill feasibility — a larger
         compressor rating margin already covers line losses."

      go_nogo:
        if all(entry["feasible"] for entry in fill_results):
            verdict = "GO"
            verdict_note = "All velocity cases are commercially feasible. Fill system is not a blocking constraint."
        else:
            verdict = "FLAG"
            verdict_note = "One or more velocity cases exceed 300 SCFM. Review before proceeding."

      Assert verdict == "GO" (expected; all values in 147–295 SCFM)

      Save fill03_feasibility.json: per-velocity table (v, Q_free, compressor_class, feasible),
        delivery_pressure_note, pipe_friction_note, go_nogo verdict, verdict_note

    STEP 5 — PHASE 1 SUMMARY TABLE:
      Load all Plan 01 and Plan 02 results from JSON files.
      Assert identity gate passed (buoy02_identity_gate.json: gate_passed == True) before writing summary.

      Build phase1_summary_table.json with the following fields:
        phase: "01-air-buoyancy-and-fill"
        completion_date: (today's date)
        requirements_satisfied: ["THRM-01", "THRM-02", "THRM-03", "BUOY-01", "BUOY-02", "BUOY-03",
                                  "FILL-01", "FILL-02", "FILL-03"]

        # THRM-01 results
        W_iso_J: (from Plan 01 JSON)
        W_adia_J: (from Plan 01 JSON)
        W_pump_min_J: (W_adia / 0.85; eta_c=0.85)
        W_pump_max_J: (W_adia / 0.65; eta_c=0.65)
        W_pump_nominal_J: (W_adia / 0.70; eta_c=0.70)

        # THRM-02 results
        V_depth_m3: (from Plan 01 JSON)
        V_surface_m3: 0.2002
        P_r: (from Plan 01 JSON)
        fill_condition: "Air injected at depth expands to exactly V_surface at surface"

        # THRM-03 results
        W_jet_separate: 0
        W_jet_note: "Jet recovery is contained within W_buoy integral; no separate line item (Pitfall C6)"

        # BUOY-01 results
        F_b_min_N: 707.6   (at z=0)
        F_b_max_N: 1959.8  (at z=H)
        F_b_avg_N: (W_iso / H)

        # BUOY-02 results
        W_buoy_J: (from Plan 02 JSON)
        identity_error_pct: (from Plan 02 JSON, as percentage)
        identity_gate: "PASS"

        # BUOY-03 results
        v_terminal_nominal_ms: (from Plan 02 JSON)
        v_terminal_conservative_ms: (from Plan 02 JSON)
        v_terminal_range_ms: (from Plan 02 JSON)

        # FILL-01 results
        arc_length_m: 5.749
        t_fill_at_nominal_s: (at v_nominal)
        t_fill_range_s: [t_fill at 2.0 m/s, t_fill at 4.0 m/s]

        # FILL-02 results
        Q_free_at_nominal_SCFM: (at v_nominal)
        Q_free_range_SCFM: [Q_free at 2.0 m/s, Q_free at 4.0 m/s]

        # FILL-03 results
        fill_go_nogo: "GO"
        compressor_class_at_nominal: (from fill03 JSON)

        # COP ceiling (forwarded from THRM-01)
        COP_ideal_max_at_eta_70: (from Plan 01 JSON)
        COP_break_even_statement: "W_buoy = W_iso confirms break-even; buoyancy alone COP < 1.0;
                                   hydrofoil contribution required for COP >= 1.5"

        # Phase 2 handoff values
        phase2_inputs:
          v_vessel_nominal_ms: (v_nominal)
          v_vessel_conservative_ms: (v_conservative)
          v_vessel_range_ms: (v_range)
          W_pump_table: "see thrm01_compression_work.json"
          F_b_z_function: "verified; use P(z) = P_atm + rho_w*g*(H-z); V(z) = V_surface*P_atm/P(z)"

    STEP 6 — PHASE 1 RESULTS DOCUMENT:
      Create docs/ directory if it does not exist.
      Write docs/phase1_results.md with the following sections:

        # Phase 1 Results: Air, Buoyancy & Fill

        ## Key Results
        | Quantity | Value | Notes |
        | W_iso (isothermal compression) | 20,640 J | Lower bound for compression work |
        | W_adia (adiabatic compression) | 24,040 J | Upper bound; +16.5% vs isothermal |
        | W_pump (at eta_c = 0.70–0.85) | 28,188–34,228 J | Actual pump energy input |
        | W_buoy (buoyancy work integral) | W_iso (identity confirmed) | < 1% difference |
        | COP with buoyancy only | 0.60–0.73 | Below 1.0; break-even not achieved |
        | v_terminal (C_D=1.0, F_chain=0) | 3.714 m/s | Nominal upper bound |
        | v_terminal range | 2.53–4.15 m/s | Over full C_D × F_chain space |
        | Fill window (at 3.714 m/s) | 1.548 s | 1/4 loop at nominal terminal velocity |
        | Q_free at nominal velocity | 274 SCFM | Commercial medium-large industrial |
        | Fill feasibility | GO | 147–295 SCFM achievable at 26 psig |

        ## Thermodynamic Identity (BUOY-02 Mandatory Gate)
        (Explain the W_buoy = W_iso identity and what it means for the project)

        ## What This Means for the Project
        The buoyancy cycle alone cannot achieve COP = 1.5. At the best compressor efficiency
        (eta_c = 0.85), COP_max = W_iso / W_pump = 0.732. Reaching 1.5 requires additional
        energy extraction — specifically the hydrofoil torque analyzed in Phase 2.

        ## Phase 2 Inputs
        - v_vessel: use 3.714 m/s (nominal) or 3.075 m/s (conservative); sweep [2.53, 4.15] m/s
        - W_pump per cycle: see thrm01_compression_work.json
        - F_b(z) function: verified and ready for Phase 2 force balance

        ## Pitfall Guards Applied
        - C1: Variable-volume buoyancy integral used; constant-volume overestimate = 74% documented
        - C6: W_jet = 0 as separate line item; jet recovery is inside W_buoy integral
        - C7: v_vessel locked from BUOY-03 result, not from user estimate of 3.0 m/s
        - M1: W_pump = W_adia/eta_c used; W_iso is NOT the pump energy
        - M5: Pipe friction = 10-20% add-on noted; applies to Phase 4 COP, not fill feasibility
  </action>
  <verify>
    1. fill03_feasibility.json: all v_vessel points marked feasible; go_nogo = "GO"
    2. Delivery pressure = 40.7 psia = 26.0 psig in JSON (both values present and correct)
    3. pipe_friction_note present in JSON (Pitfall M5 documented)
    4. phase1_summary_table.json: all 9 requirement IDs listed in requirements_satisfied
    5. phase1_summary_table.json: W_iso, W_pump range, W_buoy, identity_gate="PASS", v_terminal range, Q_free range, fill_go_nogo="GO" all present
    6. COP_break_even_statement present in summary table
    7. phase2_inputs dict present with v_vessel values loaded from Plan 02 JSON (not hardcoded)
    8. docs/phase1_results.md created with all required sections
    9. Pitfall guards C1, C6, C7, M1, M5 all documented in the results document
    10. No hardcoded upstream values — all loaded from JSON output files of Plans 01 and 02
  </verify>
  <done>fill03_feasibility.json written with GO verdict for all velocity cases. phase1_summary_table.json written with all 9 requirements covered, all key values loaded from upstream JSON files. docs/phase1_results.md written with component table, identity gate explanation, Phase 2 inputs, and pitfall guards. Phase 1 complete.</done>
</task>

</tasks>

<verification>
Overall physics consistency checks for this plan:
- Unit conversions: Q [m³/s] → CFM via factor 2118.88; CFM at depth → SCFM via P_r (Boyle's law mass equivalence)
- Delivery pressure in psia vs psig: P_bottom = 280,500 Pa = 40.7 psia; P_gauge = 280,500 - 101,325 = 179,175 Pa = 26.0 psig
- Fill window monotonicity: t_fill = arc/v decreases as v increases — correct (faster vessel means shorter window, larger Q required)
- Fill flow rate monotonicity: Q = V_depth / t_fill increases as v increases — consistent with above
- Q_free = Q_depth_CFM * P_r: physically this is Boyle's law applied to flow rates; mass-equivalent free air
- Phase 1 completeness: all 9 requirements (THRM-01 through FILL-03) have outputs in the summary table
- No upstream values hardcoded: all loaded from Plan 01 and 02 JSON outputs, ensuring propagation of any corrections
</verification>

<success_criteria>
- FILL-01: t_fill at v=3.0 m/s = 1.916 s, at v=3.714 m/s = 1.548 s; range [1.437, 2.875] s across [4.0, 2.0] m/s
- FILL-02: Q_free at v=3.0 m/s = 221 SCFM; at v=3.714 m/s = 274 SCFM; range 147–295 SCFM; unit chain verified
- FILL-03: GO verdict for all velocity cases; delivery pressure = 40.7 psia = 26.0 psig; pipe friction noted
- phase1_summary_table.json: all 9 requirements covered, Phase 2 handoff values loaded from upstream JSON
- docs/phase1_results.md: human-readable summary with component table, break-even explanation, Phase 2 inputs
- No hardcoded values from upstream plans; all data loaded from JSON output files
</success_criteria>

<output>
After completion, create `.gpd/phases/01-air-buoyancy-and-fill/01-03-SUMMARY.md`
</output>
