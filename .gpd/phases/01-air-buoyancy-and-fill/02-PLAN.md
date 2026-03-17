---
phase: 01-air-buoyancy-and-fill
plan: 02
type: execute
wave: 2
depends_on: ["01-01"]
files_modified:
  - analysis/phase1/buoy_terminal.py
  - analysis/phase1/outputs/buoy02_identity_gate.json
  - analysis/phase1/outputs/buoy03_terminal_velocity.json
  - analysis/phase1/outputs/plots/P1-2_buoyancy_integral.png
  - analysis/phase1/outputs/plots/P1-3_terminal_velocity.png
interactive: false

conventions:
  units: "SI throughout: Pa, m³, J, m, m/s, N"
  pressure: "Absolute pressure; P(z) = P_atm + rho_w * g * (H - z); z = 0 at bottom"
  volume: "Boyle's law: V(z) = V_surface * P_atm / P(z); isothermal assumption"
  force_sign: "F_b positive (upward); F_drag positive magnitude (opposes motion, enters balance as negative)"
  velocity: "v_terminal is the magnitude of the steady ascending velocity; positive"
  scipy_quad: "scipy.integrate.quad with epsabs=1e-6, epsrel=1e-8, limit=100"

dimensional_check:
  W_buoy: "[N * m] = [J]; integrand F_b(z) in N, dz in m"
  F_drag: "[kg/m³ * m² * (m/s)²] = [kg*m/s²] = [N]; C_D is dimensionless"
  v_terminal: "[m/s]; from F_net = 0 → v = sqrt(2 * F_net_drive / (rho_w * C_D * A_frontal))"
  Re: "[m/s * m / (m²/s)] = dimensionless"
  F_b_avg: "[J / m] = [N]; average force = W_iso / H"

approximations:
  - name: "isothermal ascent for buoyancy identity"
    parameter: "Vessel ascent time ~5–9 s; water temperature equilibration dominates"
    validity: "Standard engineering assumption for slow ascent in large water volume; W_buoy differs from W_iso by < 5% even if partially adiabatic"
    breaks_when: "Very fast ascent (> 10 m/s) where adiabatic heating of expanding air is significant"
    check: "|W_buoy_numerical - W_iso| / W_iso < 0.01 (mandatory gate in this plan)"
  - name: "average buoyancy force for terminal velocity"
    parameter: "F_b_avg = W_iso / H = 1128.9 N used as the driving force in force balance"
    validity: "Energy-equivalent average; gives the correct steady-state energy balance. Actual force varies from 707.6 N at z=0 to 1959.8 N at z=H — vessel accelerates continuously. Phase 1 feasibility level: average is appropriate."
    breaks_when: "Detailed trajectory analysis needed; z-dependent force balance would require ODE integration"
    check: "v_terminal from force balance is within 25% of user estimate of 3.0 m/s"
  - name: "terminal velocity = constant for drag calculation"
    parameter: "Drag force depends on instantaneous v; using v_terminal throughout is a steady-state approximation"
    validity: "Conservative estimate: the vessel spends most of its 18 m ascent near terminal velocity after a brief acceleration phase"
    breaks_when: "Chain tension varies significantly with position; not the case here"
    check: "Convergence in < 3 iterations confirms the fixed-point is well-defined"

contract:
  scope:
    question: "Is the thermodynamic identity W_buoy = W_iso satisfied to < 1%, and what is the self-consistent terminal velocity across the C_D and F_chain parameter space?"
  claims:
    - id: claim-identity-gate
      statement: "The numerical buoyancy integral W_buoy = integral_0^H F_b(z) dz equals W_iso = 20,640 J to within 1%. This confirms the thermodynamic identity and validates the pressure/volume code for all downstream use."
      deliverables: [deliv-identity-gate]
      acceptance_tests: [test-identity-1pct, test-identity-robustness]
      references: [ref-identity-derivation]
    - id: claim-terminal-velocity
      statement: "Terminal velocity of a single ascending vessel (F_chain = 0) spans 3.39–4.15 m/s over the C_D = 0.8–1.2 range. With chain coupling (F_chain = 200–500 N), velocities range from 2.53–3.77 m/s. The 3 m/s user estimate is within the plausible range for the coupled system."
      deliverables: [deliv-terminal-table]
      acceptance_tests: [test-velocity-range, test-re-regime, test-convergence]
      references: [ref-hoerner-cd]
    - id: claim-cop-ceiling-confirmed
      statement: "COP_ideal_max = W_iso / W_pump < 1.0 for all eta_c values, as established in Plan 01. This is confirmed here by citing the Plan 01 result. The implication — buoyancy alone cannot reach COP = 1.5 — is a mandatory finding, not a negative result."
      deliverables: [deliv-identity-gate]
      acceptance_tests: [test-cop-statement]
      references: [ref-plan01-thrm]
  deliverables:
    - id: deliv-identity-gate
      kind: code_output
      path: "analysis/phase1/outputs/buoy02_identity_gate.json"
      description: "W_buoy from scipy.quad at two tolerances, error vs W_iso, pass/fail gate, analytical derivation summary, COP_ideal_max reference"
      must_contain: ["W_buoy_J", "W_iso_J", "relative_error", "gate_passed", "analytical_derivation"]
    - id: deliv-terminal-table
      kind: code_output
      path: "analysis/phase1/outputs/buoy03_terminal_velocity.json"
      description: "15-point grid: 5 C_D × 3 F_chain values → v_terminal (m/s), Re, iteration count; plus F_b_avg and source formula"
      must_contain: ["C_D", "F_chain_N", "v_terminal_ms", "Re", "iterations"]
  references:
    - id: ref-identity-derivation
      source: ".gpd/phases/01-air-buoyancy-and-fill/01-EXPERIMENT-DESIGN.md Section 4 Task BUOY-02"
      anchor: "Analytical derivation: substitution u=P(z) → W_buoy = P_atm * V_surface * ln(P_bottom/P_atm) = W_iso"
    - id: ref-hoerner-cd
      source: "Hoerner, Fluid-Dynamic Drag (1965), Chapter 3: blunt cylinder Cd ~ 0.8–1.2 at Re ~ 10^5–10^6"
      anchor: "C_D = 1.0 is the center estimate for a short blunt cylinder at Re ~ 10^6; range 0.8–1.2 spans measurement uncertainty"
    - id: ref-plan01-thrm
      source: "Phase 01 Plan 01 SUMMARY — thrm01_compression_work.json"
      anchor: "W_iso = 20,640 J; W_pump(eta_c=0.70) ~ 34,228 J; COP_ideal_max < 1.0 for all eta_c"
  acceptance_tests:
    - id: test-identity-1pct
      subject: claim-identity-gate
      kind: numerical
      procedure: "Run scipy.integrate.quad(F_b_z, 0, H, epsabs=1e-6, epsrel=1e-8). Compute relative error = abs(W_buoy - W_iso) / W_iso."
      pass_condition: "relative_error < 0.01 (1%). The Python assert must not raise."
      evidence_required: [deliv-identity-gate]
    - id: test-identity-robustness
      subject: claim-identity-gate
      kind: numerical
      procedure: "Also run scipy.integrate.quad at loose tolerance (epsabs=1e-2, epsrel=1e-2). Show the 1% gate passes even at this coarse setting — confirming the gate is a physics check, not a numerical precision question."
      pass_condition: "Both tolerance settings yield W_buoy within 1% of W_iso"
      evidence_required: [deliv-identity-gate]
    - id: test-velocity-range
      subject: claim-terminal-velocity
      kind: physics_consistency
      procedure: "Verify v_terminal values at F_chain=0 span [3.39, 4.15] m/s for C_D in [1.2, 0.8]. Verify all 15 grid points are positive (ascent occurs). Verify that increasing F_chain decreases v_terminal (correct physics: more load = slower ascent)."
      pass_condition: "v_terminal(C_D=1.2, F_chain=0) in [3.3, 3.5] m/s; v_terminal(C_D=0.8, F_chain=0) in [4.1, 4.3] m/s; all 15 values positive; monotone decrease with F_chain at each C_D"
      evidence_required: [deliv-terminal-table]
    - id: test-re-regime
      subject: claim-terminal-velocity
      kind: physics_consistency
      procedure: "Compute Re = rho_w * v_terminal * d_vessel / nu_w for all 15 grid points. Confirm all are in [10^5, 10^7], the range for which Hoerner C_D = 0.8–1.2 applies."
      pass_condition: "All 15 Re values in [10^5, 10^7]; expected range ~1.1 × 10^6 to 1.9 × 10^6"
      evidence_required: [deliv-terminal-table]
    - id: test-convergence
      subject: claim-terminal-velocity
      kind: numerical
      procedure: "Report iteration count for each of the 15 grid points. The fixed-point formula has no true iteration dependency (F_b_avg is velocity-independent), so convergence in 1–2 steps is expected."
      pass_condition: "All 15 points converge in < 10 iterations (anomalous if > 10)"
      evidence_required: [deliv-terminal-table]
    - id: test-cop-statement
      subject: claim-cop-ceiling-confirmed
      kind: physics_consistency
      procedure: "Confirm that the buoy02_identity_gate.json output explicitly states: W_buoy ≈ W_iso confirms break-even; this is NOT success; success requires W_buoy + W_hydrofoil > W_pump with W_pump > W_iso."
      pass_condition: "JSON contains a cop_statement field documenting the break-even interpretation"
      evidence_required: [deliv-identity-gate]
  forbidden_proxies:
    - "Do NOT treat the passing of the buoyancy identity gate (W_buoy ≈ W_iso) as evidence that the system produces net positive energy. It is the thermodynamic break-even condition. The system COP at this stage is W_iso / W_pump < 1.0 — it is losing energy, not gaining it. All gain must come from hydrofoil work in Phase 2."
    - "Do NOT use the constant-volume integrand F_b = rho_w * g * V_surface (constant) in scipy.quad. If W_buoy comes out near 35,850 J, the Pitfall C1 error has occurred — stop immediately. The correct integrand is F_b(z) = rho_w * g * V_surface * P_atm / P(z)."
    - "Do NOT report a single terminal velocity as 'the answer' without the full C_D × F_chain sensitivity table. The 15-point grid is required. Fill calculations in Plan 03 must span this velocity range, not use 3.0 m/s as a fixed value."
    - "Do NOT proceed to Plan 03 (fill calculations) if the identity gate fails (test-identity-1pct). A failed identity gate means the pressure or volume functions are wrong, which would corrupt all fill flow rate calculations."
  uncertainty_markers:
    weakest_anchors:
      - "F_b_avg = W_iso / H is the energy-weighted average buoyancy force. The actual buoyancy force varies by a factor of 2.77 from bottom to top. Using the average for a terminal velocity calculation is correct for energy accounting but does not capture the position-dependent acceleration profile."
      - "F_chain is unknown. The 0, 200, 500 N values are sensitivity parameters, not measured values. Phase 2 hydrofoil analysis may provide a better estimate of the chain coupling force."
      - "C_D = 0.8–1.2 for a blunt cylinder is an empirical range from Hoerner. The actual vessel geometry (open-bottom cylinder) may have a slightly different C_D profile; this is a Phase 1 feasibility approximation."
    disconfirming_observations:
      - "If W_buoy from scipy.quad exceeds 25,000 J, the integrand uses constant volume (Pitfall C1). The gate will fail, correctly. Fix the integrand before proceeding."
      - "If W_buoy < 18,000 J, gauge pressure has been used instead of absolute pressure in P(z). Fix the pressure formula before proceeding."
      - "If any v_terminal in the 15-point grid is <= 0, the corresponding F_chain exceeds F_b_avg — this is a design constraint that the chain coupling cannot exceed ~1128.9 N. Flag this combination as infeasible and exclude from fill calculations."
      - "If Re for any v_terminal drops below 10^5, the C_D regime assumption (turbulent blunt cylinder) is invalid. For the expected velocity range this should not occur, but check explicitly."

estimated_execution:
  total_minutes: 45
  breakdown:
    - task: 1
      minutes: 25
      note: "scipy.quad integration at two tolerances, analytical derivation, gate assertion, plots"
    - task: 2
      minutes: 20
      note: "15-point terminal velocity grid, Re checks, iteration counting, sensitivity plot"

patterns_consulted:
  insights: []
  error_patterns: []
  adjustments_made:
    - "Hard stop before Plan 03 if identity gate fails — enforced by assert in code, documented explicitly"
    - "Constant-volume sentinel (W_buoy > 25,000 J red flag) embedded in task action per EXPERIMENT-DESIGN.md"
---

<objective>
Execute the mandatory buoyancy integral identity gate (BUOY-02) and compute the self-consistent terminal velocity across the C_D and F_chain parameter space (BUOY-03).

Purpose: The identity gate is the single most critical validation in Phase 1. It confirms that the pressure/volume/force code is internally consistent and that the thermodynamic identity W_buoy = W_iso holds. If it fails, Plans 01–03 results are suspect and fill calculations are not trustworthy. Plan 03 must not execute until this gate passes.

The terminal velocity calculation (BUOY-03) replaces the preliminary v_vessel = 3.0 m/s with a physics-derived range. This range drives the fill window and flow rate calculations in Plan 03. Using only v = 3.0 m/s without this derivation is Pitfall C7 and is forbidden.

Output: buoy02_identity_gate.json (W_buoy, relative error, gate pass/fail, COP break-even statement), buoy03_terminal_velocity.json (15-row table), plots P1-2 and P1-3.
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
</context>

<tasks>

<task type="auto">
  <name>Task 1: Buoyancy integral identity gate (BUOY-02)</name>
  <files>analysis/phase1/buoy_terminal.py, analysis/phase1/outputs/buoy02_identity_gate.json, analysis/phase1/outputs/plots/P1-2_buoyancy_integral.png</files>
  <action>
    Create analysis/phase1/buoy_terminal.py. Import constants from the previous script (or re-declare them — same locked values from CONVENTIONS.md). Import scipy.integrate, matplotlib.

    STEP 1 — LOAD RESULTS FROM PLAN 01:
      Load W_iso from thrm01_compression_work.json (do not hardcode; read the file).
      Assert W_iso in [20,619, 20,661] J (0.1% tolerance of 20,640 J).

    STEP 2 — DEFINE INTEGRAND FUNCTIONS (same as Plan 01 but now used for integration):

        def P_z(z):
            return P_atm + rho_w * g * (H - z)

        def V_z(z):
            return V_surface * P_atm / P_z(z)

        def F_b_z(z):
            return rho_w * g * V_z(z)

      Verify endpoint values one more time:
        assert abs(F_b_z(0) - 707.6) < 5, "F_b at z=0 inconsistent with Plan 01"
        assert abs(F_b_z(H) - 1959.8) < 10, "F_b at z=H inconsistent with Plan 01"

    STEP 3 — SCIPY.QUAD INTEGRATION AT TWO TOLERANCES:

      LOOSE tolerance (documentation pass):
        W_buoy_loose, err_loose = scipy.integrate.quad(F_b_z, 0, H, limit=100,
                                                         epsabs=1e-2, epsrel=1e-2)
        rel_error_loose = abs(W_buoy_loose - W_iso) / W_iso

      PRODUCTION tolerance:
        W_buoy, err_tight = scipy.integrate.quad(F_b_z, 0, H, limit=100,
                                                   epsabs=1e-6, epsrel=1e-8)
        rel_error_tight = abs(W_buoy - W_iso) / W_iso

      RED FLAG SENTINEL — check before gate:
        assert W_buoy < 25000, \
            f"PITFALL C1: W_buoy={W_buoy:.0f}J > 25000J. Constant-volume integrand detected. "
            f"Fix: integrand must use V(z)=V_surface*P_atm/P(z), not V_surface constant."

      MANDATORY GATE — hard stop if fails:
        assert rel_error_tight < 0.01, \
            f"IDENTITY GATE FAIL: W_buoy={W_buoy:.1f}J vs W_iso={W_iso:.1f}J, "
            f"relative error={rel_error_tight*100:.3f}% > 1%. "
            f"DO NOT PROCEED to Plan 03. Diagnose pressure or volume function."

      Print: "IDENTITY GATE PASS: W_buoy = {W_buoy:.1f} J, W_iso = {W_iso:.1f} J, "
             "relative error = {rel_error_tight*100:.4f}%"

    STEP 4 — ANALYTICAL CROSS-CHECK (show in output):
      Document the substitution derivation:
        "Let u = P(z), du = d/dz[P_atm + rho_w*g*(H-z)] dz = -rho_w*g dz, so dz = -du/(rho_w*g)
         When z=0: u = P_bottom. When z=H: u = P_atm.
         W_buoy = integral_0^H rho_w*g*V_surface*P_atm/P(z) dz
                = rho_w*g*V_surface*P_atm * integral_0^H 1/P(z) dz
                = V_surface*P_atm * integral_{P_bottom}^{P_atm} 1/u * (-1) du
                = V_surface*P_atm * integral_{P_atm}^{P_bottom} 1/u du
                = V_surface*P_atm * ln(P_bottom/P_atm)
                = P_atm * V_surface * ln(P_r)
                = W_iso   (exactly)"
      This derivation must appear in the JSON output and be verifiable by inspection.

    STEP 5 — COP BREAK-EVEN STATEMENT:
      From Plan 01 JSON, load W_pump table. Compute COP_at_identity = W_buoy / W_pump_table.
      Add cop_statement to output JSON:
        "W_buoy ≈ W_iso confirms thermodynamic break-even: buoyancy work equals minimum pumping
         cost. COP = W_buoy / W_pump = {W_iso}/{W_pump_nominal:.0f} = {cop:.3f} < 1.0.
         This is NOT net positive energy. All gain above break-even must come from hydrofoil
         work (Phase 2). Reporting W_buoy ≈ W_iso as success would be false progress."

    STEP 6 — SAVE OUTPUT:
      Write buoy02_identity_gate.json with:
        W_buoy_J, W_iso_J, rel_error_tight, rel_error_loose, gate_passed=True,
        err_estimate_tight, err_estimate_loose, analytical_derivation (string),
        cop_statement (string), scipy_settings (epsabs, epsrel, limit)

    STEP 7 — PLOT P1-2: BUOYANCY INTEGRAL:
      Plot F_b(z) vs z from z=0 to z=H using 200 points.
      Shade the area under the curve (the integral W_buoy).
      Add horizontal reference line at F_b_avg = W_iso / H = 1128.9 N.
      Annotate the shaded area with "W_buoy = {W_buoy:.0f} J = W_iso (identity confirmed)".
      Label x-axis: "Height above tank bottom z (m)"; y-axis: "Buoyancy force F_b(z) (N)"
      Title: "Buoyancy force profile and work integral — identity gate"
      Save as plots/P1-2_buoyancy_integral.png (150 dpi minimum).
  </action>
  <verify>
    1. Mandatory gate assertion does not raise (W_buoy within 1% of W_iso at production tolerance)
    2. rel_error_tight < 0.01 and rel_error_loose < 0.01 (gate robust to tolerance setting)
    3. W_buoy < 25,000 J (constant-volume sentinel passes; value expected ~20,640 J)
    4. W_buoy > 18,000 J (gauge-pressure sentinel; value should not be low due to absolute pressure)
    5. Analytical derivation string in JSON is complete and shows W_buoy = W_iso analytically
    6. cop_statement in JSON explicitly says W_buoy ≈ W_iso is break-even, not success
    7. scipy.integrate.quad error estimate for production run is << 1 J (expected ~1e-4 J)
    8. P1-2 plot created; shaded area visible; F_b_avg reference line shown
  </verify>
  <done>buoy02_identity_gate.json written with gate_passed=True, relative error documented, analytical derivation included, COP break-even statement present. Both tolerance runs pass. Constant-volume sentinel does not trigger. Plot P1-2 saved. Plan 03 is now authorized to proceed.</done>
</task>

<task type="auto">
  <name>Task 2: Terminal velocity sweep (BUOY-03)</name>
  <files>analysis/phase1/buoy_terminal.py, analysis/phase1/outputs/buoy03_terminal_velocity.json, analysis/phase1/outputs/plots/P1-3_terminal_velocity.png</files>
  <action>
    Continue in buoy_terminal.py (append after STEP 7).

    STEP 8 — FORCE BALANCE SETUP:
      Load W_iso from Plan 01 output.
      F_b_avg = W_iso / H    # energy-weighted average buoyancy force
      Assert abs(F_b_avg - 1128.9) < 5, "F_b_avg inconsistent with W_iso / H"

      Document the force balance:
        At terminal velocity v_t: F_net = 0
        F_b_avg - F_drag(v_t) - F_chain = 0
        0.5 * rho_w * C_D * A_frontal * v_t^2 = F_b_avg - F_chain
        v_t = sqrt(2 * (F_b_avg - F_chain) / (rho_w * C_D * A_frontal))

      Note: This is analytic, not iterative — F_b_avg does not depend on v.
      The "iteration" structure from EXPERIMENT-DESIGN.md is retained for clarity but converges in 1 step.

    STEP 9 — PARAMETER GRID SWEEP (15 points: 5 C_D × 3 F_chain):
      C_D_values = [0.8, 0.9, 1.0, 1.1, 1.2]
      F_chain_values = [0.0, 200.0, 500.0]

      results = []
      for C_D in C_D_values:
          for F_chain in F_chain_values:
              F_net_drive = F_b_avg - F_chain

              if F_net_drive <= 0:
                  v_t = None  # infeasible: chain tension exceeds buoyancy
                  Re = None
                  n_iter = 0
              else:
                  # Analytic result (single evaluation, labeled as "iteration 1"):
                  v_t = math.sqrt(2 * F_net_drive / (rho_w * C_D * A_frontal))
                  n_iter = 1
                  Re = rho_w * v_t * d_vessel / nu_w

                  # Validation assertions for each point:
                  assert v_t > 0, f"v_terminal <= 0 at C_D={C_D}, F_chain={F_chain}"
                  assert 1.0 <= v_t <= 10.0, \
                      f"v_terminal={v_t:.2f} m/s outside [1, 10] at C_D={C_D}, F_chain={F_chain}"
                  assert 1e5 <= Re <= 1e7, \
                      f"Re={Re:.2e} outside C_D regime at C_D={C_D}, F_chain={F_chain}"

              results.append({
                  "C_D": C_D, "F_chain_N": F_chain,
                  "v_terminal_ms": v_t, "Re": Re, "iterations": n_iter,
                  "feasible": F_net_drive > 0
              })

    STEP 10 — PRINT SUMMARY TABLES:
      Table 1: v_terminal for F_chain = 0 (upper bound, isolated vessel):
        C_D values: [0.8, 0.9, 1.0, 1.1, 1.2]
        Expected: [4.152, 3.915, 3.714, 3.541, 3.390] m/s approximately

      Table 2: v_terminal grid (3 rows × 5 columns, C_D vs F_chain):
        Expected: matches EXPERIMENT-DESIGN.md Section 4 Task BUOY-03 table

      For each row with F_chain=0, verify that v_terminal matches EXPERIMENT-DESIGN.md
      expected values within 0.05 m/s:
        C_D=0.8: 4.152 ± 0.05 m/s; C_D=1.0: 3.714 ± 0.05 m/s; C_D=1.2: 3.390 ± 0.05 m/s

    STEP 11 — KEY FINDING AND DOWNSTREAM HANDOFF:
      Document in the JSON output:
        "LOCKED VALUES FOR PLAN 03 (fill calculations):
         - v_vessel_nominal: 3.714 m/s (C_D=1.0, F_chain=0; upper bound for isolated vessel)
         - v_vessel_conservative: 3.075 m/s (C_D=1.2, F_chain=200N; moderate coupling)
         - v_vessel_range: [2.530, 4.152] m/s (full C_D × F_chain envelope)
         - Use full range for fill window calculations. Do NOT fix v = 3.0 m/s (Pitfall C7)."

      Reynolds number check summary:
        "All Re values in range [1.1 × 10^6, 1.9 × 10^6] at F_chain=0.
         At F_chain=500N: Re range [0.7 × 10^6, 1.3 × 10^6].
         All values within [10^5, 10^7] — Hoerner C_D = 0.8–1.2 is self-consistent."

    STEP 12 — SAVE OUTPUT:
      Write buoy03_terminal_velocity.json with:
        - results array (15 rows, all fields above)
        - F_b_avg_N, W_iso_J, H_m (source values)
        - v_handoff (dict with nominal, conservative, and range)
        - reynolds_summary (string)

    STEP 13 — PLOT P1-3: TERMINAL VELOCITY vs C_D:
      Plot v_terminal vs C_D for three F_chain curves: {0, 200, 500} N.
      Add horizontal reference line at v = 3.0 m/s (user baseline, labeled "User estimate").
      Add horizontal reference line at v = 2.0 m/s (lower fill feasibility bound, labeled "Min feasible").
      x-axis: "Hull drag coefficient C_D"; y-axis: "Terminal velocity v_terminal (m/s)"
      Label each curve with its F_chain value.
      Title: "Terminal velocity sensitivity to C_D and chain tension"
      Grid on. Save as plots/P1-3_terminal_velocity.png (150 dpi minimum).
  </action>
  <verify>
    1. All 15 grid points computed (5 C_D × 3 F_chain)
    2. All 15 Re values in [10^5, 10^7]; confirms Hoerner C_D regime is self-consistent
    3. v_terminal at (C_D=0.8, F_chain=0) = 4.152 ± 0.05 m/s
    4. v_terminal at (C_D=1.0, F_chain=0) = 3.714 ± 0.05 m/s
    5. v_terminal at (C_D=1.2, F_chain=0) = 3.390 ± 0.05 m/s
    6. v_terminal strictly decreases as C_D increases at each F_chain level (correct physics: more drag = slower)
    7. v_terminal strictly decreases as F_chain increases at each C_D level (correct physics: more load = slower)
    8. v_handoff dict in JSON contains nominal (3.714 m/s), conservative (3.075 m/s), and range [2.530, 4.152]
    9. Iteration count = 1 for all feasible points (analytic single-step result)
    10. Plot P1-3 created with 3 curves, 3.0 m/s reference line, and 2.0 m/s reference line
    11. No assertion failures in parameter sweep
  </verify>
  <done>buoy03_terminal_velocity.json written with 15-row results table, all Re values in valid regime, v_terminal matches EXPERIMENT-DESIGN.md expected values within tolerance. Locked handoff values for Plan 03 documented. Plot P1-3 saved. BUOY-03 requirement satisfied. Plan 03 may now execute using the v_handoff range.</done>
</task>

</tasks>

<verification>
Overall physics consistency checks for this plan:
- Thermodynamic identity: W_buoy = P_atm * V_surface * ln(P_r) = W_iso confirmed analytically and numerically to < 1%
- First Law check: COP = W_buoy / W_pump < 1.0 (system is not net positive at this stage — expected and documented)
- Dimensional consistency: [F_b(z) dz] = [N][m] = [J] throughout the integral
- Drag force dimensional check: [0.5 * rho_w * C_D * A * v^2] = [kg/m³ * m² * m²/s²] = [kg*m/s²] = [N]
- Terminal velocity dimensional check: [sqrt(2*F/(rho*C_D*A))] = [sqrt(N/(kg/m³ * m²))] = [sqrt(m²/s²)] = [m/s]
- Reynolds number: dimensionless = [m/s * m / (m²/s)] — confirmed
- Monotonicity of v_terminal with C_D and F_chain: strictly decreasing in both (both increase the drag/load)
- Self-consistency of C_D regime: Re values at computed v_terminal all confirm turbulent blunt cylinder regime
</verification>

<success_criteria>
- Mandatory identity gate passes: |W_buoy - W_iso| / W_iso < 1% at production tolerance (hard assert in code)
- Gate is robust: also passes at loose tolerance (1e-2, 1e-2), confirming physics, not numerics
- Analytical derivation of W_buoy = W_iso via substitution documented in JSON output
- COP break-even statement: W_buoy ≈ W_iso is explicitly documented as break-even, not success
- 15-point terminal velocity grid complete; all values in [1.0, 10.0] m/s; all Re in [10^5, 10^7]
- v_terminal at key benchmarks (C_D=0.8/1.0/1.2, F_chain=0) match EXPERIMENT-DESIGN.md expected values within 0.05 m/s
- Locked handoff values for Plan 03 written to JSON: nominal 3.714 m/s, conservative 3.075 m/s, range [2.53, 4.15] m/s
- Both plots (P1-2 integral, P1-3 sensitivity) created
</success_criteria>

<output>
After completion, create `.gpd/phases/01-air-buoyancy-and-fill/01-02-SUMMARY.md`
</output>
