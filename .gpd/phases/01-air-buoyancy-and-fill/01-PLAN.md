---
phase: 01-air-buoyancy-and-fill
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - analysis/phase1/thrm_buoy_setup.py
  - analysis/phase1/outputs/thrm01_compression_work.json
  - analysis/phase1/outputs/buoy01_force_profile.json
  - analysis/phase1/outputs/plots/P1-1_profiles.png
  - analysis/phase1/outputs/plots/P1-4_pump_energy.png
interactive: false

conventions:
  units: "SI throughout: Pa, m³, J, m/s, kg, N"
  pressure: "Absolute pressure; P(z) = P_atm + rho_w * g * (H - z); z = 0 at tank bottom"
  volume: "Boyle's law: V(z) = V_surface * P_atm / P(z); ideal gas"
  energy_sign: "W > 0 means energy input (pumping); W > 0 means energy output (buoyancy) when labeled as output"
  imperial_crosscheck: "Parenthetical only; SI is authoritative"

dimensional_check:
  W_iso: "[Pa * m³] = [J]"
  W_adia: "[Pa * m³] = [J]"
  W_pump: "[J]; W_pump = W_adia / eta_c where eta_c is dimensionless"
  F_b: "[kg/m³ * m/s² * m³] = [N]"
  P_z: "[Pa]"
  V_z: "[m³]"

approximations:
  - name: "ideal gas"
    parameter: "P_r = 2.770 (below 3 atm)"
    validity: "Compressibility Z ≈ 1.000 for air at < 3 atm; error < 0.1%"
    breaks_when: "P > 50 atm or T near liquefaction"
    check: "W_iso computed from P_atm * V_surface * ln(P_r) matches expected 20,640 J to < 0.1%"
  - name: "isothermal expansion during ascent"
    parameter: "Ascent time ~5–9 s at 2–4 m/s; thermal equilibration with water is rapid for small vessel"
    validity: "Biot number suggests near-isothermal; error in W_buoy estimate < 5%"
    breaks_when: "Ascent is much faster than thermal equilibration; high-speed operation"
    check: "W_buoy integral matches W_iso to < 1% (mandatory gate in Plan 02)"
  - name: "hydrostatic pressure profile"
    parameter: "Static fluid; no significant flow-induced pressure gradients along vertical"
    validity: "Flow velocities << sonic; valid for all operating conditions"
    breaks_when: "Never in this system"
    check: "P(0) = 280,500 Pa; P(H) = 101,325 Pa verified numerically"

contract:
  scope:
    question: "What are the thermodynamic energy bounds for one compression cycle, and what does the buoyancy force profile look like along the full 60 ft ascent?"
  claims:
    - id: claim-compression-bounds
      statement: "W_iso = 20,640 J and W_adia = 24,040 J are the thermodynamic lower and upper bounds for one compression cycle; W_pump = W_adia / eta_c is in the range 28,188–36,861 J for eta_c = 0.65–0.85"
      deliverables: [deliv-thrm01-table]
      acceptance_tests: [test-wiso-value, test-wadia-value, test-wpump-table]
      references: [ref-conventions-thrm]
    - id: claim-buoy-force-profile
      statement: "F_b(z) = rho_w * g * V_surface * P_atm / P(z) increases monotonically from 707.6 N at z=0 to 1959.8 N at z=H; this is the integrand for Plan 02's mandatory gate"
      deliverables: [deliv-buoy01-profile]
      acceptance_tests: [test-fb-endpoints, test-fb-monotone]
      references: [ref-conventions-buoy]
    - id: claim-fill-volumes
      statement: "V_depth = 0.07228 m³ at depth and V_surface = 0.2002 m³ at surface; fill target is that injected air at P_bottom expands exactly to V_surface at z=H"
      deliverables: [deliv-thrm02-volumes]
      acceptance_tests: [test-vdepth, test-vsurface]
      references: [ref-conventions-boyle]
    - id: claim-cop-ceiling
      statement: "COP_ideal_max = W_iso / W_pump < 1.0 for all eta_c; buoyancy alone cannot achieve the 1.5 W/W target; hydrofoil contribution is required"
      deliverables: [deliv-thrm01-table]
      acceptance_tests: [test-cop-below-one]
      references: [ref-conventions-balance]
  deliverables:
    - id: deliv-thrm01-table
      kind: code_output
      path: "analysis/phase1/outputs/thrm01_compression_work.json"
      description: "Table of W_iso, W_adia, W_pump(eta_c) for eta_c in {0.65, 0.70, 0.75, 0.80, 0.85}, plus COP_ideal_max per row"
      must_contain: ["W_iso", "W_adia", "W_pump", "COP_ideal_max", "eta_c"]
    - id: deliv-thrm02-volumes
      kind: code_output
      path: "analysis/phase1/outputs/thrm01_compression_work.json"
      description: "V_depth, V_surface, P_r, fill target condition statement"
      must_contain: ["V_depth", "V_surface", "P_r", "fill_condition"]
    - id: deliv-buoy01-profile
      kind: code_output
      path: "analysis/phase1/outputs/buoy01_force_profile.json"
      description: "F_b(z) at z = {0, H/4, H/2, 3H/4, H} with P(z) and V(z); plot P1-1"
      must_contain: ["z_m", "P_z_Pa", "V_z_m3", "F_b_N"]
  references:
    - id: ref-conventions-thrm
      source: ".gpd/CONVENTIONS.md §3 Air Thermodynamics and §9 Energy and Work Notation"
      anchor: "W_iso = 101325 * 0.2002 * ln(2.770) = 20,640 J (test value in CONVENTIONS.md)"
    - id: ref-conventions-buoy
      source: ".gpd/CONVENTIONS.md §6 Volume Notation and §7 Force Notation"
      anchor: "F_b(z=H) = 998.2 * 9.807 * 0.2002 = 1959 N (test value in CONVENTIONS.md)"
    - id: ref-conventions-boyle
      source: ".gpd/CONVENTIONS.md §6 Volume Notation"
      anchor: "V_depth = V_surface / P_r = 0.2002 / 2.770 = 0.07228 m³ (test value)"
    - id: ref-conventions-balance
      source: ".gpd/CONVENTIONS.md §14 System Energy Balance Structure — Mandatory Check 3"
      anchor: "COP = 1.0 for ideal isothermal, no drag, no losses (First Law check)"
  acceptance_tests:
    - id: test-wiso-value
      subject: claim-compression-bounds
      kind: numerical
      procedure: "Compute W_iso = P_atm * V_surface * ln(P_r) with the locked parameter values. Compare to 20,640 J."
      pass_condition: "abs(W_iso - 20640) / 20640 < 0.001 (0.1%)"
      evidence_required: [deliv-thrm01-table]
    - id: test-wadia-value
      subject: claim-compression-bounds
      kind: numerical
      procedure: "Compute W_adia = 3.5 * P_atm * V_surface * (P_r^0.2857 - 1). Compare to 24,040 J."
      pass_condition: "abs(W_adia - 24040) / 24040 < 0.001 (0.1%)"
      evidence_required: [deliv-thrm01-table]
    - id: test-wpump-table
      subject: claim-compression-bounds
      kind: numerical
      procedure: "For eta_c = 0.70: W_pump should be ~34,228 J. For eta_c = 0.85: W_pump should be ~28,188 J. Confirm W_pump > W_iso for all eta_c."
      pass_condition: "W_pump(0.70) in [33,900, 34,600] J; W_pump(0.85) in [27,900, 28,500] J; W_pump > W_iso for all rows"
      evidence_required: [deliv-thrm01-table]
    - id: test-cop-below-one
      subject: claim-cop-ceiling
      kind: physics_consistency
      procedure: "Verify COP_ideal_max = W_iso / W_pump < 1.0 for all eta_c rows. The highest COP occurs at eta_c = 0.85; confirm it is still < 1.0."
      pass_condition: "max(COP_ideal_max) < 1.0 across all eta_c values; specifically COP at eta_c=0.85 ≈ 0.732 < 1.0"
      evidence_required: [deliv-thrm01-table]
    - id: test-fb-endpoints
      subject: claim-buoy-force-profile
      kind: numerical
      procedure: "Evaluate F_b at z=0 and z=H. At z=0: V = V_depth = 0.07228 m³, F_b = 998.2*9.807*0.07228. At z=H: V = V_surface = 0.2002 m³, F_b = 998.2*9.807*0.2002."
      pass_condition: "F_b(z=0) = 707.6 ± 4 N; F_b(z=H) = 1959.8 ± 10 N"
      evidence_required: [deliv-buoy01-profile]
    - id: test-fb-monotone
      subject: claim-buoy-force-profile
      kind: physics_consistency
      procedure: "Verify F_b(z) is strictly increasing from z=0 to z=H. As z increases, P(z) decreases, so V(z) increases, so F_b = rho_w*g*V(z) increases."
      pass_condition: "F_b values at z = {0, H/4, H/2, 3H/4, H} are strictly increasing"
      evidence_required: [deliv-buoy01-profile]
    - id: test-vdepth
      subject: claim-fill-volumes
      kind: numerical
      procedure: "Compute V_depth = V_surface * P_atm / P_bottom = 0.2002 * 101325 / 280500. Compare to 0.07228 m³."
      pass_condition: "abs(V_depth - 0.07228) < 0.0001 m³"
      evidence_required: [deliv-thrm02-volumes]
    - id: test-vsurface
      subject: claim-fill-volumes
      kind: numerical
      procedure: "Verify that V(z=H) = V_surface exactly by Boyle's law: V(H) = V_surface * P_atm / P(H) = V_surface * P_atm / P_atm = V_surface."
      pass_condition: "V(z=H) == V_surface to machine precision"
      evidence_required: [deliv-thrm02-volumes]
  forbidden_proxies:
    - "Do NOT report W_iso = 20,640 J as the pump energy input in any COP or efficiency calculation. The pump energy is W_pump = W_adia / eta_c, which is 28,188–36,861 J. W_iso is the thermodynamic minimum for a reversible isothermal compressor, which does not exist in practice. (Pitfall M1)"
    - "Do NOT use constant-volume buoyancy (F_b = rho_w * g * V_surface = constant). The volume changes during ascent. The constant-volume formula F_b_const * H = 1959.8 * 18.288 = 35,851 J overestimates by 74% relative to the correct integral W_iso = 20,640 J. (Pitfall C1)"
    - "Do NOT present buoyancy work (W_buoy ≈ W_iso) as evidence of net positive energy. Buoyancy ≈ pumping is the expected thermodynamic baseline — it means break-even, not success. Success requires W_buoy + W_hydrofoil > W_pump."
    - "Do NOT conflate THRM-03 jet recovery with buoyancy work. Jet recovery from the expanding air at the open bottom is already inside the buoyancy integral — it is the same thermodynamic expansion. Including it as a separate additive term would double-count. (Pitfall C6)"
  uncertainty_markers:
    weakest_anchors:
      - "gamma = 1.4 for moist air: actual gamma is slightly lower for humid air; error < 1% on W_adia"
      - "P_r = 2.770 depends on rho_w and H; rho_w at temperatures other than 20°C shifts by < 0.3%"
    disconfirming_observations:
      - "If W_iso computed from the formula exceeds 22,000 J, the constant-volume error (Pitfall C1) has been applied to the compression formula as well as the buoyancy integral — stop and recheck"
      - "If COP_ideal_max at any eta_c is >= 1.0, the energy balance sign convention is wrong — pumping cost is not being applied correctly; stop and recheck"
      - "If F_b(z=0) > F_b(z=H), the pressure profile has the wrong sign for z; the CONVENTIONS.md z-convention (z=0 at bottom) has been violated"

estimated_execution:
  total_minutes: 40
  breakdown:
    - task: 1
      minutes: 20
      note: "Sanity checks + compression work table (closed-form evaluations, 5-row eta_c sweep)"
    - task: 2
      minutes: 20
      note: "Buoyancy force profile at 5 z-points + THRM-02 volume confirmation + 2 plots"

patterns_consulted:
  insights: []
  error_patterns: []
  adjustments_made:
    - "Explicit constant-volume anti-pattern sentinel included per Pitfall C1 in PITFALLS.md"
    - "COP_ideal_max < 1.0 check included to guard against sign errors in energy accounting"
---

<objective>
Establish the thermodynamic compression work bounds (THRM-01, THRM-02, THRM-03) and compute the buoyancy force profile along the full ascent (BUOY-01).

Purpose: This plan produces the foundational numbers that every downstream calculation depends on. W_iso and W_adia establish the pumping energy baseline — the denominator of the COP. The F_b(z) profile is the integrand for Plan 02's mandatory identity gate. Getting these right, with explicit unit and dimensional checks, is the non-negotiable precondition for all Phase 1 and Phase 2 work.

THRM-03 note: Jet propulsion recovery from the expanding air at the open vessel bottom is thermodynamically identical to the buoyancy expansion work — it is not an additional energy source. The buoyancy integral already accounts for all work done by the expanding gas column. THRM-03 is satisfied by documenting this equivalence explicitly, preventing double-counting in the system balance (Pitfall C6).

Output: thrm01_compression_work.json (W_iso, W_adia, W_pump table, COP_ideal_max, V_depth/V_surface, P_r), buoy01_force_profile.json (F_b(z) at 5 heights), plots P1-1 and P1-4.
</objective>

<execution_context>
@C:/Users/garth/.claude/get-physics-done/workflows/execute-plan.md
@C:/Users/garth/.claude/get-physics-done/templates/summary.md
</execution_context>

<context>
@.gpd/PROJECT.md
@.gpd/ROADMAP.md
@.gpd/CONVENTIONS.md
@.gpd/phases/01-air-buoyancy-and-fill/01-EXPERIMENT-DESIGN.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: Sanity checks and compression work (THRM-01, THRM-02, THRM-03)</name>
  <files>analysis/phase1/thrm_buoy_setup.py, analysis/phase1/outputs/thrm01_compression_work.json</files>
  <action>
    Create analysis/phase1/ directory structure. Create thrm_buoy_setup.py with the following sections executed in order:

    SECTION 1 — CONSTANTS (read directly from CONVENTIONS.md; no magic numbers):
      P_atm = 101325 Pa; rho_w = 998.2 kg/m³; g = 9.807 m/s²; H = 18.288 m
      V_surface = 0.2002 m³; gamma = 1.4; nu_w = 1.004e-6 m²/s
      d_vessel = 0.457 m; A_frontal = 0.1640 m²; R_tank = 3.66 m

    SECTION 2 — DERIVED CONSTANTS (compute and assert, do not hardcode):
      P_bottom = P_atm + rho_w * g * H
      P_r = P_bottom / P_atm
      V_depth = V_surface * P_atm / P_bottom
      Assert P_bottom within 100 Pa of 280,500; assert P_r within 0.005 of 2.770;
      assert V_depth within 0.0001 m³ of 0.07228.

    SECTION 3 — SANITY CHECKS (all 6 from EXPERIMENT-DESIGN.md Section 6):
      Check 1: P(z=0) = 280,500 ± 100 Pa; P(z=H) = P_atm exactly
      Check 2: V(z=0) = V_depth ± 0.0001 m³; V(z=H) = V_surface exactly
      Check 3: W_iso_calc = P_atm * V_surface * math.log(P_r); assert within 21 J of 20,640
      Check 4: W_wrong = rho_w * g * V_surface * H (constant-volume error = ~35,850 J);
               assert overestimate ratio in [0.70, 0.80] (should be ~73.6%); DO NOT use W_wrong elsewhere
      Check 5: Re_nominal = rho_w * 3.0 * d_vessel / nu_w; assert Re in [1e5, 1e7]
      Check 6: arc_length = 2 * pi * R_tank / 4; assert within 0.005 m of 5.749;
               t_fill_3ms = arc_length / 3.0; assert within 0.005 s of 1.916

    SECTION 4 — THRM-01: COMPRESSION WORK TABLE:
      W_iso = P_atm * V_surface * math.log(P_r)     [isothermal minimum]
      W_adia = (gamma / (gamma - 1)) * P_atm * V_surface * (P_r**((gamma-1)/gamma) - 1)
             = 3.5 * P_atm * V_surface * (P_r**0.2857 - 1)    [adiabatic upper bound]
      Assert W_iso in [20,619, 20,661] J (±0.1%)
      Assert W_adia in [24,016, 24,064] J (±0.1%)
      Assert W_adia / W_iso in [1.158, 1.168] (expected ~1.165; adiabatic penalty)
      Assert W_adia > W_iso (adiabatic work is always greater than isothermal)

      For eta_c in [0.65, 0.70, 0.75, 0.80, 0.85]:
        W_pump = W_adia / eta_c
        COP_ideal_max = W_iso / W_pump
        Assert W_pump > W_iso for every eta_c (real pump always costs more than reversible minimum)
        Assert COP_ideal_max < 1.0 for every eta_c (buoyancy alone cannot break even)

      Print result table to stdout and save to thrm01_compression_work.json.

    SECTION 5 — THRM-02: FILL VOLUMES:
      Document V_depth = 0.07228 m³ and V_surface = 0.2002 m³ with the fill condition:
      "Air injected at P_bottom occupies V_depth = V_surface / P_r. As vessel ascends, air
       expands isothermally. At z=H: V(H) = V_surface * P_atm / P_atm = V_surface — vessel
       is exactly full. Fill target: inject V_depth of air at P_bottom into open-bottom vessel."
      Include V_depth in ft³ = V_depth / 0.02832 = 2.553 ft³ (imperial cross-check).
      Add fill_condition field to JSON output.

    SECTION 6 — THRM-03: JET RECOVERY ACCOUNTING:
      Add a section to the JSON output explaining that W_jet = 0 as a separate line item
      because jet recovery from the expanding open-bottom air column is contained within the
      buoyancy integral W_buoy = integral F_b(z) dz. The F_b(z) integrand includes the full
      buoyancy force at each height, which already accounts for the gas expansion pressure.
      Adding W_jet separately would double-count Pitfall C6. Document: "W_jet is NOT an
      additional energy source; it is the same thermodynamic expansion already in W_buoy."

    Dimensional checks to embed as comments:
      [W_iso] = [Pa * m³] = [N/m² * m³] = [N*m] = [J] — correct
      [W_adia] = same as W_iso — correct
      [W_pump] = [J / dimensionless] = [J] — correct
      [COP_ideal_max] = [J / J] = dimensionless — correct
  </action>
  <verify>
    1. Sanity check assertions pass (all 6 from EXPERIMENT-DESIGN.md Section 6): P endpoints, V endpoints, W_iso closed form, constant-volume sentinel, Re regime, arc length
    2. W_iso = 20,640 ± 21 J (within 0.1% of CONVENTIONS.md test value)
    3. W_adia = 24,040 ± 24 J (within 0.1% of CONVENTIONS.md test value)
    4. W_adia / W_iso in [1.158, 1.168]; expected 1.165 from gamma=1.4, P_r=2.770
    5. W_pump(eta_c=0.70) in [33,900, 34,600] J; W_pump(eta_c=0.85) in [27,900, 28,500] J
    6. COP_ideal_max < 1.0 for all 5 eta_c values (confirms buoyancy alone cannot reach 1.5 W/W)
    7. V_depth = 0.07228 ± 0.0001 m³ = 2.553 ± 0.004 ft³ (imperial cross-check)
    8. THRM-03 jet recovery explicitly flagged as W_jet = 0 separate line item with double-counting warning
    9. JSON output file exists and contains all required fields
  </verify>
  <done>thrm01_compression_work.json written with W_iso, W_adia, W_pump table (5 rows), COP_ideal_max (all < 1.0), V_depth, V_surface, P_r, fill_condition statement, and W_jet double-counting note. All 6 sanity checks pass. All assert statements in code pass without exception.</done>
</task>

<task type="auto">
  <name>Task 2: Buoyancy force profile (BUOY-01) and diagnostic plots</name>
  <files>analysis/phase1/thrm_buoy_setup.py, analysis/phase1/outputs/buoy01_force_profile.json, analysis/phase1/outputs/plots/P1-1_profiles.png, analysis/phase1/outputs/plots/P1-4_pump_energy.png</files>
  <action>
    Continue in thrm_buoy_setup.py (append after SECTION 6).

    SECTION 7 — BUOY-01: BUOYANCY FORCE PROFILE:
      Define the integrand functions (these will also be used in Plan 02's scipy.quad integration):

        def P_z(z):
            """Absolute pressure at height z. z=0 at bottom, z=H at surface."""
            return P_atm + rho_w * g * (H - z)

        def V_z(z):
            """Air volume at height z via Boyle's law (isothermal)."""
            return V_surface * P_atm / P_z(z)

        def F_b_z(z):
            """Buoyancy force at height z."""
            return rho_w * g * V_z(z)

      Evaluate at z_points = [0, H/4, H/2, 3*H/4, H] = [0, 4.572, 9.144, 13.716, 18.288]:

        Expected values (from EXPERIMENT-DESIGN.md Section 4, Task BUOY-02 table):
          z=0:      P = 280,500 Pa; V = 0.07228 m³; F_b = 707.6 N
          z=H/4:    P = 235,594 Pa; V = 0.08607 m³; F_b = 842.7 N
          z=H/2:    P = 190,688 Pa; V = 0.10635 m³; F_b = 1041.3 N
          z=3H/4:   P = 145,782 Pa; V = 0.13923 m³; F_b = 1363.6 N
          z=H:      P = 101,325 Pa; V = 0.20020 m³; F_b = 1959.8 N

      Assert at each z-point:
        - P(z) is within 100 Pa of expected
        - V(z) is within 0.001 m³ of expected
        - F_b(z) is within 5 N of expected
        - F_b(z) values are strictly increasing (monotone check)

      Compute F_b_avg = W_iso / H = 20640 / 18.288 = 1128.9 N (energy-weighted average)
      Assert F_b(0) < F_b_avg < F_b(H) (average lies between min and max — basic sanity)

      Dimensional check: [F_b] = [kg/m³ * m/s² * m³] = [kg * m/s²] = [N] — correct

      Save to buoy01_force_profile.json with fields: z_m, P_z_Pa, V_z_m3, F_b_N (array of 5 points),
      plus F_b_avg_N, W_iso_J, H_m.

      Include note on open-bottom vessel: "V(z) is the air column volume; the remaining
      vessel volume V_surface - V(z) is water. At z=0, the vessel is 36.1% air and 63.9%
      water by volume."

    SECTION 8 — PLOT P1-1: PROFILES vs z:
      Three-panel or dual-y-axis plot showing P(z), V(z), and F_b(z) vs z over z in [0, H].
      Use 200 z-points (dense). Label axes with units. Grid on.
      Title: "Hydrostatic profiles along ascent path"
      Annotate: z=0 (bottom, P_bottom, V_depth), z=H (surface, P_atm, V_surface)
      Confirm all three curves are monotone increasing or decreasing as expected:
        P(z): decreasing (from P_bottom to P_atm) — correct
        V(z): increasing (from V_depth to V_surface) — correct
        F_b(z): increasing (from F_b_min to F_b_max) — correct
      Save as plots/P1-1_profiles.png (150 dpi minimum).

    SECTION 9 — PLOT P1-4: PUMP ENERGY vs ETA_C:
      Bar or line chart of W_pump(eta_c) for eta_c in [0.65, 0.70, 0.75, 0.80, 0.85].
      Add horizontal reference lines for W_iso = 20,640 J and W_adia = 24,040 J.
      Add right-hand y-axis for COP_ideal_max = W_iso / W_pump.
      Annotate the COP target of 1.5 as a dashed horizontal line on the right axis.
      Title: "Pump energy and ideal-maximum COP vs compressor efficiency"
      All W_pump bars should be clearly above W_adia (since eta_c < 1.0 always means W_pump > W_adia).
      Save as plots/P1-4_pump_energy.png (150 dpi minimum).

    Final assertion in code:
      Assert plots directory exists and both PNG files were created.
  </action>
  <verify>
    1. F_b(z=0) = 707.6 ± 4 N; F_b(z=H) = 1959.8 ± 10 N (CONVENTIONS.md test values)
    2. F_b values at all 5 z-points are strictly increasing (monotone)
    3. F_b_avg = 1128.9 ± 5 N; lies between F_b(0) and F_b(H)
    4. V(z=0) = V_depth = 0.07228 ± 0.0001 m³; V(z=H) = V_surface = 0.2002 m³ exactly
    5. P(z=0) = 280,500 ± 100 Pa; P(z=H) = 101,325 Pa exactly
    6. buoy01_force_profile.json exists with required fields and 5-point arrays
    7. P1-1_profiles.png and P1-4_pump_energy.png both created
    8. Plot P1-1: all three profile curves are monotone (P decreasing, V and F_b increasing)
    9. Plot P1-4: all W_pump bars above W_adia reference line; COP_ideal_max all below 1.0 on right axis
  </verify>
  <done>buoy01_force_profile.json written with F_b(z) at 5 heights confirmed to match EXPERIMENT-DESIGN.md expected values within tolerance. Plots P1-1 and P1-4 saved as PNG. Open-bottom vessel air fraction documented. F_b(z) function defined and validated, ready for scipy.quad integration in Plan 02.</done>
</task>

</tasks>

<verification>
Overall physics consistency checks for this plan:
- Dimensional consistency: W = [Pa][m³] = [J]; F = [kg/m³][m/s²][m³] = [N]
- First Law check: COP_ideal_max = W_iso / W_pump < 1.0 for all eta_c (cannot extract more work than you put in via this ideal route alone)
- Boyle's law self-consistency: V(z=H) * P_atm = V(z=0) * P_bottom = V_surface * P_atm (all equal)
- Monotonicity: F_b is monotone increasing during ascent (pressure decreasing → volume increasing → buoyancy increasing)
- THRM-03 double-counting guard: W_jet confirmed to be zero as a separate line item; it is contained in W_buoy
- Constant-volume anti-pattern sentinel: W_wrong = rho_w * g * V_surface * H ~ 35,850 J is explicitly computed and confirmed to be ~74% above W_iso, then discarded
</verification>

<success_criteria>
- W_iso = 20,640 ± 21 J and W_adia = 24,040 ± 24 J confirmed against CONVENTIONS.md test values
- W_pump table (5 rows over eta_c) written to JSON; all entries above W_adia; COP_ideal_max all < 1.0
- V_depth = 0.07228 m³ and fill condition statement documented (THRM-02 complete)
- THRM-03 jet recovery documented as W_jet = 0 separate line item with Pitfall C6 explanation
- F_b(z) profile at 5 heights matches EXPERIMENT-DESIGN.md expected values to within tolerance
- All 6 sanity checks from EXPERIMENT-DESIGN.md Section 6 pass without exception
- Both plots (P1-1 profiles, P1-4 pump energy) created and visually correct
</success_criteria>

<output>
After completion, create `.gpd/phases/01-air-buoyancy-and-fill/01-01-SUMMARY.md`
</output>
