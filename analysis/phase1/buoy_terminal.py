# -*- coding: utf-8 -*-
"""
Hydrowheel Phase 1 -- Buoyancy Identity Gate and Terminal Velocity Sweep
=========================================================================

BUOY-02: Mandatory identity gate -- W_buoy = integral_0^H F_b(z) dz must equal W_iso
         to within 1%. This is the single most critical validation in Phase 1.
         If this gate fails, DO NOT proceed to Plan 03.

BUOY-03: Terminal velocity sweep -- 5 C_D x 3 F_chain = 15 grid points.
         Replaces the preliminary v_vessel = 3.0 m/s with a physics-derived range.
         Locked handoff values for Plan 03 fill calculations.

ASSERT_CONVENTION: unit_system=SI, coordinate_system=z=0_at_bottom_z_up,
                   pressure=P_atm+rho_w*g*(H-z)_absolute,
                   buoyancy=variable_volume_F_b=rho_w*g*V(z),
                   velocity_Re=v*d_vessel/nu_w_kinematic_only,
                   energy_sign=W_pump_input_W_buoy_output,
                   force_sign=F_b_positive_upward_F_drag_positive_magnitude

Dimensional checks:
  [W_buoy] = [N * m] = [J]  -- F_b(z) in N times dz in m
  [F_drag] = [kg/m3 * m2 * m2/s2] = [N]  -- 0.5*rho_w*C_D*A*v^2
  [v_terminal] = [sqrt(N / (kg/m3 * m2))] = [sqrt(m2/s2)] = [m/s]
  [Re] = [m/s * m / (m2/s)] = dimensionless

Author: gpd-executor (Phase 01, Plan 02)
Date: 2026-03-18
Reproducibility: scipy.integrate.quad (deterministic); no random elements.
Libraries: Python 3.x, scipy, numpy, matplotlib, json, math, os
"""

import math
import json
import os
import sys

# Force UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

try:
    import scipy.integrate
except ImportError:
    raise ImportError("scipy is required: pip install scipy")

try:
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')  # non-interactive backend for headless execution
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("WARNING: matplotlib not installed -- plots will be skipped. pip install matplotlib numpy")

# ============================================================
# SECTION 1: CONSTANTS (same locked values as thrm_buoy_setup.py)
# ============================================================

# Water and gravity
rho_w    = 998.2       # [kg/m3] fresh water at 20 deg C (CRC Handbook)
g        = 9.807       # [m/s2]  standard gravity
nu_w     = 1.004e-6    # [m2/s]  kinematic viscosity, fresh water 20 deg C

# Geometry
H        = 18.288      # [m]  water depth = 60 ft (user spec)
d_vessel = 0.457       # [m]  vessel outer diameter = 18 in
A_frontal = 0.1640     # [m2] pi/4 * d_vessel^2 (frontal area for hull drag)

# Thermodynamics
P_atm    = 101325      # [Pa] atmospheric pressure = 1.000 atm standard

# Volume
V_surface = 0.2002     # [m3] full vessel internal volume = 7.069 ft3

# ============================================================
# SECTION 2: DERIVED CONSTANTS
# ============================================================

P_bottom = P_atm + rho_w * g * H    # [Pa] absolute pressure at tank bottom
P_r = P_bottom / P_atm              # [-] pressure ratio (dimensionless)
V_depth = V_surface * P_atm / P_bottom  # [m3] air volume at depth (Boyle's law)

print(f"Derived constants:")
print(f"  P_bottom = {P_bottom:.2f} Pa = {P_bottom/P_atm:.6f} atm")
print(f"  P_r      = {P_r:.6f}")
print(f"  V_depth  = {V_depth:.6f} m3")

# ============================================================
# SECTION 3: LOAD W_iso FROM PLAN 01 OUTPUT
# Do not hardcode. Read from thrm01_compression_work.json.
# ============================================================

_outputs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
_thrm01_path = os.path.join(_outputs_dir, "thrm01_compression_work.json")

with open(_thrm01_path, "r", encoding="utf-8") as f:
    _thrm01 = json.load(f)

W_iso = _thrm01["THRM_01_compression_work"]["W_iso_J"]
W_pump_table = _thrm01["THRM_01_compression_work"]["W_pump_table"]

print(f"\nLoaded from thrm01_compression_work.json:")
print(f"  W_iso = {W_iso:.2f} J")

# Sanity check: W_iso must be within 0.1% of 20640 J
assert abs(W_iso - 20640) / 20640 < 0.001, \
    f"W_iso={W_iso:.1f} J not within 0.1% of 20640 J. Check thrm01 output."
print(f"  W_iso assertion passed: within 0.1% of 20640 J")

# Also confirm W_iso is in [20619, 20661] J (plan spec)
assert 20619 <= W_iso <= 20661, \
    f"W_iso={W_iso:.1f} J outside [20619, 20661] J. Check thrm01 output."
print(f"  W_iso range assertion passed: in [20619, 20661] J")

# ============================================================
# SECTION 4: INTEGRAND FUNCTIONS
# Same functions validated in Plan 01 (thrm_buoy_setup.py).
# Redeclared here for self-contained integration.
# ============================================================

def P_z(z):
    """Absolute hydrostatic pressure at height z [Pa].
    Convention: z=0 at tank bottom, z=H at water surface.
    P(z) = P_atm + rho_w * g * (H - z)
    P(0) = P_bottom (max pressure, air injection depth)
    P(H) = P_atm   (surface pressure)
    """
    return P_atm + rho_w * g * (H - z)


def V_z(z):
    """Air volume in vessel at height z [m3] via Boyle's law (isothermal).
    V(z) = V_surface * P_atm / P(z)
    V(0) = V_depth  (minimum, compressed)
    V(H) = V_surface (maximum, fully expanded)
    """
    return V_surface * P_atm / P_z(z)


def F_b_z(z):
    """Buoyancy force on ascending vessel at height z [N].
    F_b(z) = rho_w * g * V(z)  -- variable-volume buoyancy
    NOTE: This uses the expanding air volume V(z), NOT the constant V_surface.
    Using constant V_surface (Pitfall C1) overestimates by ~74%.
    """
    return rho_w * g * V_z(z)


# Verify endpoint values are consistent with Plan 01 results
_fb_at_0 = F_b_z(0)
_fb_at_H = F_b_z(H)
print(f"\nIntegrand endpoint verification:")
print(f"  F_b(z=0) = {_fb_at_0:.2f} N  (Plan 01 result: 708.3 N)")
print(f"  F_b(z=H) = {_fb_at_H:.2f} N  (Plan 01 result: 1959.8 N)")

assert abs(_fb_at_0 - 707.6) < 5, \
    f"F_b(z=0)={_fb_at_0:.1f} N inconsistent with Plan 01 (expected ~707.6 N, tolerance 5 N)"
assert abs(_fb_at_H - 1959.8) < 10, \
    f"F_b(z=H)={_fb_at_H:.1f} N inconsistent with Plan 01 (expected ~1959.8 N, tolerance 10 N)"
print("  Endpoint assertions PASSED")

# ============================================================
# SECTION 5: SCIPY.QUAD INTEGRATION AT TWO TOLERANCES
# ============================================================

print("\n" + "="*60)
print("BUOY-02: BUOYANCY INTEGRAL IDENTITY GATE")
print("="*60)

# --- LOOSE tolerance (documentation pass: physics check, not numerics) ---
W_buoy_loose, err_loose = scipy.integrate.quad(
    F_b_z, 0, H,
    limit=100,
    epsabs=1e-2,
    epsrel=1e-2
)
rel_error_loose = abs(W_buoy_loose - W_iso) / W_iso

print(f"\nLoose tolerance (epsabs=1e-2, epsrel=1e-2):")
print(f"  W_buoy_loose = {W_buoy_loose:.4f} J")
print(f"  error estimate = {err_loose:.2e} J")
print(f"  |W_buoy_loose - W_iso| / W_iso = {rel_error_loose*100:.4f}%")

# --- PRODUCTION tolerance ---
W_buoy, err_tight = scipy.integrate.quad(
    F_b_z, 0, H,
    limit=100,
    epsabs=1e-6,
    epsrel=1e-8
)
rel_error_tight = abs(W_buoy - W_iso) / W_iso

print(f"\nProduction tolerance (epsabs=1e-6, epsrel=1e-8):")
print(f"  W_buoy = {W_buoy:.4f} J")
print(f"  error estimate = {err_tight:.2e} J")
print(f"  |W_buoy - W_iso| / W_iso = {rel_error_tight*100:.4f}%")

# --- RED FLAG SENTINEL (Pitfall C1 guard) ---
# If W_buoy > 25000 J, the constant-volume integrand was used by mistake.
# Correct value is ~20,645 J; constant-volume gives ~35,841 J.
assert W_buoy < 25000, (
    f"PITFALL C1 DETECTED: W_buoy={W_buoy:.0f} J > 25000 J. "
    f"Constant-volume integrand detected. "
    f"Fix: integrand must use V(z)=V_surface*P_atm/P(z), not constant V_surface."
)
print(f"\nPitfall C1 sentinel: W_buoy={W_buoy:.0f} J < 25000 J -- CLEAR")

# --- LOW VALUE SENTINEL (gauge-pressure guard) ---
assert W_buoy > 18000, (
    f"GAUGE PRESSURE ERROR: W_buoy={W_buoy:.0f} J < 18000 J. "
    f"Likely cause: gauge pressure used instead of absolute pressure in P(z). "
    f"Fix: P(z) = P_atm + rho_w*g*(H-z), not rho_w*g*(H-z) alone."
)
print(f"Gauge pressure sentinel: W_buoy={W_buoy:.0f} J > 18000 J -- CLEAR")

# --- MANDATORY GATE (hard stop if fails) ---
assert rel_error_tight < 0.01, (
    f"IDENTITY GATE FAIL: W_buoy={W_buoy:.1f} J vs W_iso={W_iso:.1f} J, "
    f"relative error={rel_error_tight*100:.3f}% > 1%. "
    f"DO NOT PROCEED to Plan 03. Diagnose pressure or volume function."
)

print(f"\nIDENTITY GATE PASS: W_buoy = {W_buoy:.1f} J, W_iso = {W_iso:.1f} J, "
      f"relative error = {rel_error_tight*100:.4f}%")

# Both tolerances must pass
assert rel_error_loose < 0.01, (
    f"GATE FAIL AT LOOSE TOLERANCE: rel_error_loose={rel_error_loose*100:.3f}% > 1%. "
    f"This should not fail if production tolerance passes -- investigate."
)
print(f"LOOSE TOLERANCE GATE PASS: rel_error_loose = {rel_error_loose*100:.4f}%")

# scipy.integrate.quad error estimate should be << 1 J
assert err_tight < 1.0, (
    f"Integration error estimate {err_tight:.2e} J is unexpectedly large (> 1 J). "
    f"Increase limit or check integrand for pathologies."
)
print(f"Integration error estimate = {err_tight:.2e} J (expected << 1 J) -- OK")

# ============================================================
# SECTION 6: ANALYTICAL CROSS-CHECK
# Substitution derivation: W_buoy = W_iso exactly (analytical)
# ============================================================

# Verify the analytical result numerically:
# W_iso_analytical = P_atm * V_surface * ln(P_bottom / P_atm)
W_iso_check = P_atm * V_surface * math.log(P_bottom / P_atm)
print(f"\nAnalytical check: P_atm * V_surface * ln(P_r) = {W_iso_check:.4f} J")
print(f"  W_iso from JSON = {W_iso:.4f} J")
print(f"  Difference      = {abs(W_iso_check - W_iso):.4f} J (machine precision)")

# The analytical derivation (for JSON documentation):
analytical_derivation = (
    "SUBSTITUTION DERIVATION: W_buoy = integral_0^H F_b(z) dz = W_iso (exact). "
    "Step 1: Write integrand: F_b(z) = rho_w * g * V_surface * P_atm / P(z) "
    "where P(z) = P_atm + rho_w*g*(H-z). "
    "Step 2: Factor constant: W_buoy = rho_w*g*V_surface*P_atm * integral_0^H 1/P(z) dz. "
    "Step 3: Change variable u = P(z), du = d/dz[P_atm + rho_w*g*(H-z)] dz = -rho_w*g dz. "
    "Therefore dz = -du/(rho_w*g). "
    "Limits: z=0 => u=P_bottom; z=H => u=P_atm. "
    "Step 4: Substitute: W_buoy = rho_w*g*V_surface*P_atm * integral_{P_bottom}^{P_atm} (1/u) * (-du/(rho_w*g)) "
    "= V_surface*P_atm * integral_{P_atm}^{P_bottom} (1/u) du "
    "= V_surface*P_atm * [ln(u)]_{P_atm}^{P_bottom} "
    "= V_surface*P_atm * (ln(P_bottom) - ln(P_atm)) "
    "= P_atm * V_surface * ln(P_bottom/P_atm) "
    "= P_atm * V_surface * ln(P_r) = W_iso. "
    "QED: W_buoy = W_iso exactly for any ideal isothermal expansion."
)

# ============================================================
# SECTION 7: COP BREAK-EVEN STATEMENT
# ============================================================

# Use nominal W_pump at eta_c = 0.70 (mid-range compressor efficiency)
W_pump_nominal = None
for row in W_pump_table:
    if abs(row["eta_c"] - 0.70) < 1e-9:
        W_pump_nominal = row["W_pump_J"]
        break
assert W_pump_nominal is not None, "eta_c=0.70 row not found in W_pump_table"

COP_at_identity = W_buoy / W_pump_nominal

cop_statement = (
    f"W_buoy = {W_buoy:.1f} J APPROXIMATELY EQUALS W_iso = {W_iso:.1f} J "
    f"(relative error {rel_error_tight*100:.4f}%). "
    f"This confirms thermodynamic BREAK-EVEN: buoyancy work equals minimum pumping cost (isothermal). "
    f"COP = W_buoy / W_pump(eta_c=0.70) = {W_buoy:.1f} / {W_pump_nominal:.1f} = {COP_at_identity:.4f} < 1.0. "
    f"THIS IS NOT NET POSITIVE ENERGY. "
    f"Break-even means the system recovers exactly the thermodynamic minimum pumping work -- "
    f"it does NOT generate surplus energy. "
    f"All energy gain above break-even must come from hydrofoil work (Phase 2). "
    f"Reporting W_buoy = W_iso as a 'success' without the hydrofoil contribution would be false progress. "
    f"The COP_ideal_max (buoyancy only, no losses) is {COP_at_identity:.4f}, well below the 1.5 target."
)

print(f"\nCOP break-even statement:")
print(f"  COP = W_buoy / W_pump(eta_c=0.70) = {COP_at_identity:.4f}")
print(f"  This is break-even (buoyancy alone), NOT net positive.")

# ============================================================
# SECTION 8: SAVE BUOY-02 OUTPUT JSON
# ============================================================

buoy02_output = {
    "_description": "BUOY-02: Buoyancy integral identity gate",
    "_units": "SI throughout: J, Pa, m, dimensionless",
    "_assert_convention": (
        "unit_system=SI, coordinate_system=z=0_at_bottom, "
        "pressure=absolute_Pa, buoyancy=variable_volume_F_b=rho_w*g*V(z)"
    ),
    "W_buoy_J": round(W_buoy, 4),
    "W_iso_J": round(W_iso, 4),
    "relative_error_tight": round(rel_error_tight, 8),
    "relative_error_loose": round(rel_error_loose, 8),
    "relative_error_pct_tight": round(rel_error_tight * 100, 6),
    "relative_error_pct_loose": round(rel_error_loose * 100, 6),
    "err_estimate_tight_J": round(err_tight, 10),
    "err_estimate_loose_J": round(err_loose, 6),
    "gate_passed": True,
    "gate_criteria": "|W_buoy - W_iso| / W_iso < 0.01 (1%)",
    "scipy_settings_tight": {"epsabs": 1e-6, "epsrel": 1e-8, "limit": 100},
    "scipy_settings_loose": {"epsabs": 1e-2, "epsrel": 1e-2, "limit": 100},
    "pitfall_C1_check": {
        "W_buoy_constant_volume_would_be": round(rho_w * g * V_surface * H, 1),
        "sentinel": "W_buoy < 25000 J",
        "sentinel_passed": W_buoy < 25000,
        "note": "Constant-volume integrand (Pitfall C1) would give ~35,841 J (~74% overestimate). Actual integral uses variable-volume F_b(z) = rho_w*g*V_surface*P_atm/P(z)."
    },
    "analytical_derivation": analytical_derivation,
    "analytical_check_J": round(W_iso_check, 4),
    "cop_statement": cop_statement,
    "W_pump_nominal_J": round(W_pump_nominal, 2),
    "COP_at_identity": round(COP_at_identity, 6),
    "integrand_functions": {
        "P_z": "P_atm + rho_w * g * (H - z)",
        "V_z": "V_surface * P_atm / P_z(z)",
        "F_b_z": "rho_w * g * V_z(z)"
    },
    "endpoint_verification": {
        "F_b_at_z0_N": round(_fb_at_0, 3),
        "F_b_at_zH_N": round(_fb_at_H, 3),
        "plan01_F_b_z0": 708.3,
        "plan01_F_b_zH": 1959.8
    }
}

_buoy02_path = os.path.join(_outputs_dir, "buoy02_identity_gate.json")
with open(_buoy02_path, "w", encoding="utf-8") as f:
    json.dump(buoy02_output, f, indent=2, ensure_ascii=False)
print(f"\nSaved: {_buoy02_path}")

# ============================================================
# SECTION 9: PLOT P1-2 -- BUOYANCY INTEGRAL
# ============================================================

if MATPLOTLIB_AVAILABLE:
    _plots_dir = os.path.join(_outputs_dir, "plots")
    os.makedirs(_plots_dir, exist_ok=True)

    # Dense z grid for smooth plot
    z_plot = np.linspace(0, H, 200)
    fb_plot = np.array([F_b_z(zi) for zi in z_plot])
    F_b_avg = W_iso / H  # energy-weighted average buoyancy force [N]

    fig, ax = plt.subplots(figsize=(8, 5))

    # Fill the area under the F_b(z) curve (represents W_buoy)
    ax.fill_between(z_plot, 0, fb_plot, alpha=0.25, color='royalblue', label='_nolegend_')
    ax.plot(z_plot, fb_plot, color='royalblue', linewidth=2.0,
            label=r'$F_b(z) = \rho_w g V(z)$ (variable-volume buoyancy)')

    # Average buoyancy force reference line
    ax.axhline(F_b_avg, color='darkorange', linewidth=1.5, linestyle='--',
               label=f'$F_{{b,avg}} = W_{{iso}}/H = {F_b_avg:.1f}$ N')

    # Annotation for the integral value
    ax.annotate(
        f'$W_{{buoy}} = \\int_0^H F_b(z)\\,dz$\n'
        f'$= {W_buoy:.0f}$ J $= W_{{iso}}$ (identity confirmed)',
        xy=(H * 0.5, (fb_plot[100] + F_b_avg) / 2),
        xytext=(H * 0.15, fb_plot.max() * 0.6),
        fontsize=9,
        arrowprops=dict(arrowstyle='->', color='black', lw=1.0),
        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.8)
    )

    # Endpoint annotations
    ax.annotate(f'$F_b(0) = {_fb_at_0:.0f}$ N', xy=(0, _fb_at_0),
                xytext=(H * 0.05, _fb_at_0 + 80), fontsize=8,
                arrowprops=dict(arrowstyle='->', color='royalblue', lw=0.8))
    ax.annotate(f'$F_b(H) = {_fb_at_H:.0f}$ N', xy=(H, _fb_at_H),
                xytext=(H * 0.70, _fb_at_H - 150), fontsize=8,
                arrowprops=dict(arrowstyle='->', color='royalblue', lw=0.8))

    ax.set_xlabel('Height above tank bottom $z$ (m)', fontsize=11)
    ax.set_ylabel('Buoyancy force $F_b(z)$ (N)', fontsize=11)
    ax.set_title('Buoyancy force profile and work integral — identity gate\n'
                 r'($W_{buoy} = W_{iso}$: thermodynamic break-even confirmed)', fontsize=11)
    ax.legend(fontsize=9, loc='upper left')
    ax.grid(True, alpha=0.4)
    ax.set_xlim(0, H)
    ax.set_ylim(0, fb_plot.max() * 1.12)

    plt.tight_layout()
    _p12_path = os.path.join(_plots_dir, "P1-2_buoyancy_integral.png")
    plt.savefig(_p12_path, dpi=150)
    plt.close()
    print(f"Saved: {_p12_path}")
else:
    print("WARNING: matplotlib not available -- P1-2 plot skipped")

# ============================================================
# SECTION 10: BUOY-03 -- TERMINAL VELOCITY SWEEP
# 15 grid points: 5 C_D x 3 F_chain
# ============================================================

print("\n" + "="*60)
print("BUOY-03: TERMINAL VELOCITY SWEEP (15 points: 5 C_D x 3 F_chain)")
print("="*60)

# Force balance at terminal velocity v_t:
#   F_net = 0  =>  F_b_avg = F_drag(v_t) + F_chain
#   0.5 * rho_w * C_D * A_frontal * v_t^2 = F_b_avg - F_chain
#   v_t = sqrt(2 * (F_b_avg - F_chain) / (rho_w * C_D * A_frontal))
#
# This is ANALYTIC (single evaluation). F_b_avg is constant (not velocity-dependent).
# The "iterations" field is retained as 1 (one function evaluation) for clarity.
#
# Re = v_t * d_vessel / nu_w   (kinematic viscosity only; no rho_w factor)
# [Re] = [m/s * m / (m2/s)] = dimensionless -- confirmed

F_b_avg = W_iso / H   # [N] energy-weighted average buoyancy force

# Verify F_b_avg is consistent with W_iso / H = 1128.9 N
assert abs(F_b_avg - 1128.9) < 5, \
    f"F_b_avg={F_b_avg:.2f} N inconsistent with expected ~1128.9 N"
print(f"\nF_b_avg = W_iso / H = {W_iso:.2f} / {H} = {F_b_avg:.4f} N")
print(f"F_b_avg assertion PASSED (within 5 N of 1128.9 N)")

# Parameter grid
C_D_values     = [0.8, 0.9, 1.0, 1.1, 1.2]
F_chain_values = [0.0, 200.0, 500.0]

print(f"\nSweeping C_D in {C_D_values}")
print(f"Sweeping F_chain in {F_chain_values} N")

results = []
for C_D in C_D_values:
    for F_chain in F_chain_values:
        F_net_drive = F_b_avg - F_chain

        if F_net_drive <= 0:
            # Chain tension exceeds buoyancy -- vessel cannot ascend
            v_t = None
            Re = None
            n_iter = 0
            feasible = False
            print(f"  C_D={C_D:.1f}, F_chain={F_chain:.0f} N: INFEASIBLE "
                  f"(F_net_drive={F_net_drive:.1f} N <= 0)")
        else:
            # Analytic single-step result (labeled n_iter=1)
            # [v_t] = [sqrt(N / (kg/m3 * m2))] = [sqrt(m2/s2)] = [m/s] -- dimensional check
            v_t = math.sqrt(2.0 * F_net_drive / (rho_w * C_D * A_frontal))
            n_iter = 1
            # Re = v * d / nu  (kinematic viscosity; no rho_w factor)
            Re = v_t * d_vessel / nu_w
            feasible = True

            # Validation assertions for each feasible grid point
            assert v_t > 0, f"v_terminal <= 0 at C_D={C_D}, F_chain={F_chain}"
            assert 1.0 <= v_t <= 10.0, \
                (f"v_terminal={v_t:.2f} m/s outside [1, 10] at "
                 f"C_D={C_D}, F_chain={F_chain}")
            assert 1e5 <= Re <= 1e7, \
                (f"Re={Re:.2e} outside [1e5, 1e7] C_D regime at "
                 f"C_D={C_D}, F_chain={F_chain}")

        results.append({
            "C_D": C_D,
            "F_chain_N": F_chain,
            "v_terminal_ms": round(v_t, 4) if v_t is not None else None,
            "Re": round(Re, 0) if Re is not None else None,
            "iterations": n_iter,
            "feasible": feasible,
            "F_net_drive_N": round(F_net_drive, 4)
        })

print(f"\nAll {len(results)} grid points computed.")
print(f"Feasible points: {sum(r['feasible'] for r in results)}")

# ============================================================
# SECTION 11: PRINT SUMMARY TABLES
# ============================================================

print("\nTable 1: v_terminal (m/s) for F_chain = 0 (upper bound, isolated vessel):")
print(f"  {'C_D':>6}  {'v_t (m/s)':>12}  {'Re':>12}")
for r in results:
    if r["F_chain_N"] == 0.0 and r["feasible"]:
        print(f"  {r['C_D']:>6.1f}  {r['v_terminal_ms']:>12.4f}  {r['Re']:>12.3e}")

# Verify key benchmark values (EXPERIMENT-DESIGN.md expected values within 0.05 m/s)
for r in results:
    if r["F_chain_N"] == 0.0 and r["feasible"]:
        if abs(r["C_D"] - 0.8) < 1e-9:
            assert abs(r["v_terminal_ms"] - 4.152) < 0.05, \
                f"C_D=0.8 F_chain=0: v_t={r['v_terminal_ms']:.3f} m/s, expected 4.152 +/-0.05 m/s"
            print(f"  Benchmark PASS: C_D=0.8 v_t={r['v_terminal_ms']:.3f} m/s (expected ~4.152)")
        if abs(r["C_D"] - 1.0) < 1e-9:
            assert abs(r["v_terminal_ms"] - 3.714) < 0.05, \
                f"C_D=1.0 F_chain=0: v_t={r['v_terminal_ms']:.3f} m/s, expected 3.714 +/-0.05 m/s"
            print(f"  Benchmark PASS: C_D=1.0 v_t={r['v_terminal_ms']:.3f} m/s (expected ~3.714)")
        if abs(r["C_D"] - 1.2) < 1e-9:
            assert abs(r["v_terminal_ms"] - 3.390) < 0.05, \
                f"C_D=1.2 F_chain=0: v_t={r['v_terminal_ms']:.3f} m/s, expected 3.390 +/-0.05 m/s"
            print(f"  Benchmark PASS: C_D=1.2 v_t={r['v_terminal_ms']:.3f} m/s (expected ~3.390)")

print("\nTable 2: v_terminal (m/s) -- full 3x5 grid (rows=F_chain, cols=C_D):")
header = "F_chain \\ C_D  |" + "".join(f"  {cd:5.1f}" for cd in C_D_values)
print("  " + header)
print("  " + "-" * len(header))
for F_chain in F_chain_values:
    row_str = f"  {F_chain:12.0f} N |"
    for C_D in C_D_values:
        match = [r for r in results if abs(r["C_D"]-C_D)<1e-9 and abs(r["F_chain_N"]-F_chain)<1e-9]
        r = match[0]
        if r["feasible"]:
            row_str += f"  {r['v_terminal_ms']:5.3f}"
        else:
            row_str += f"  {'N/A':>5}"
    print(row_str)

# Physics consistency checks:
# 1. v_terminal strictly decreases as C_D increases at each F_chain level
# 2. v_terminal strictly decreases as F_chain increases at each C_D level
print("\nPhysics consistency checks:")
for F_chain in F_chain_values:
    vt_for_cd = [r["v_terminal_ms"] for r in results
                 if abs(r["F_chain_N"]-F_chain)<1e-9 and r["feasible"]]
    if len(vt_for_cd) >= 2:
        is_decreasing = all(vt_for_cd[i] > vt_for_cd[i+1] for i in range(len(vt_for_cd)-1))
        assert is_decreasing, \
            f"v_terminal is NOT strictly decreasing with C_D at F_chain={F_chain} N. Values: {vt_for_cd}"
        print(f"  PASS: v_terminal strictly decreasing with C_D at F_chain={F_chain:.0f} N")

for C_D in C_D_values:
    vt_for_fchain = [r["v_terminal_ms"] for r in results
                     if abs(r["C_D"]-C_D)<1e-9 and r["feasible"]]
    if len(vt_for_fchain) >= 2:
        is_decreasing = all(vt_for_fchain[i] > vt_for_fchain[i+1] for i in range(len(vt_for_fchain)-1))
        assert is_decreasing, \
            f"v_terminal is NOT strictly decreasing with F_chain at C_D={C_D}. Values: {vt_for_fchain}"
        print(f"  PASS: v_terminal strictly decreasing with F_chain at C_D={C_D:.1f}")

# ============================================================
# SECTION 12: KEY FINDING AND DOWNSTREAM HANDOFF VALUES
# ============================================================

# Extract key handoff values (Plan 03 will use these)
v_nominal_result = [r for r in results if abs(r["C_D"]-1.0)<1e-9 and abs(r["F_chain_N"]-0.0)<1e-9]
v_conservative_result = [r for r in results if abs(r["C_D"]-1.2)<1e-9 and abs(r["F_chain_N"]-200.0)<1e-9]

assert len(v_nominal_result) == 1, "Could not find nominal grid point (C_D=1.0, F_chain=0)"
assert len(v_conservative_result) == 1, "Could not find conservative grid point (C_D=1.2, F_chain=200)"

v_nominal = v_nominal_result[0]["v_terminal_ms"]
v_conservative = v_conservative_result[0]["v_terminal_ms"]

# Full range: max and min over all feasible points
feasible_vt = [r["v_terminal_ms"] for r in results if r["feasible"]]
v_range = [round(min(feasible_vt), 4), round(max(feasible_vt), 4)]

v_handoff = {
    "v_vessel_nominal_ms": v_nominal,
    "v_vessel_nominal_source": "C_D=1.0, F_chain=0 N (isolated vessel, center C_D estimate)",
    "v_vessel_conservative_ms": v_conservative,
    "v_vessel_conservative_source": "C_D=1.2, F_chain=200 N (high drag, light coupling)",
    "v_vessel_range_ms": v_range,
    "v_vessel_range_source": "Full C_D=[0.8,1.2], F_chain=[0,500] N envelope (feasible points only)",
    "plan03_instruction": (
        "Use full range [v_min, v_max] = v_vessel_range_ms for fill window calculations. "
        "Do NOT fix v = 3.0 m/s (Pitfall C7). "
        "Nominal (3.714 m/s) and conservative (3.075 m/s) values bracket the expected operating range."
    ),
    "user_baseline_ms": 3.0,
    "user_baseline_within_range": v_range[0] <= 3.0 <= v_range[1]
}

print(f"\nHandoff values for Plan 03 (fill calculations):")
print(f"  v_nominal = {v_nominal:.3f} m/s (C_D=1.0, F_chain=0)")
print(f"  v_conservative = {v_conservative:.3f} m/s (C_D=1.2, F_chain=200N)")
print(f"  v_range = {v_range} m/s (full envelope)")
print(f"  User estimate 3.0 m/s within range: {v_handoff['user_baseline_within_range']}")

# Reynolds number summary
re_all = [r["Re"] for r in results if r["feasible"]]
re_summary = (
    f"All Re values in range [{min(re_all):.3e}, {max(re_all):.3e}]. "
    f"At F_chain=0: Re in [{min(r['Re'] for r in results if r['feasible'] and r['F_chain_N']==0.0):.3e}, "
    f"{max(r['Re'] for r in results if r['feasible'] and r['F_chain_N']==0.0):.3e}]. "
    f"All values within [1e5, 1e7] -- Hoerner C_D=0.8-1.2 blunt cylinder regime is self-consistent "
    f"(turbulent flow around blunt body at these Reynolds numbers). "
    f"Expected range: ~1.1e6 to 1.9e6."
)
print(f"\nRe summary: {re_summary}")

# ============================================================
# SECTION 13: SAVE BUOY-03 OUTPUT JSON
# ============================================================

buoy03_output = {
    "_description": "BUOY-03: Terminal velocity sweep -- 15 grid points (5 C_D x 3 F_chain)",
    "_units": "SI throughout: m/s, N, dimensionless",
    "_assert_convention": (
        "unit_system=SI, F_b_avg=W_iso/H_energy_weighted_average, "
        "Re=v*d_vessel/nu_w_kinematic_only, "
        "v_terminal=steady_state_magnitude_positive_upward"
    ),
    "F_b_avg_N": round(F_b_avg, 4),
    "F_b_avg_source": "W_iso / H = energy-weighted average buoyancy force",
    "W_iso_J": round(W_iso, 4),
    "H_m": H,
    "parameters": {
        "C_D_values": C_D_values,
        "F_chain_values_N": F_chain_values,
        "rho_w_kg_m3": rho_w,
        "nu_w_m2_s": nu_w,
        "d_vessel_m": d_vessel,
        "A_frontal_m2": A_frontal
    },
    "force_balance": (
        "At terminal velocity v_t: F_net = 0. "
        "F_b_avg - F_drag(v_t) - F_chain = 0. "
        "0.5*rho_w*C_D*A_frontal*v_t^2 = F_b_avg - F_chain. "
        "v_t = sqrt(2*(F_b_avg - F_chain)/(rho_w*C_D*A_frontal)). "
        "Note: This is analytic (single evaluation); F_b_avg is independent of v_t."
    ),
    "results": results,
    "v_handoff": v_handoff,
    "reynolds_summary": re_summary,
    "benchmark_checks": {
        "C_D_08_F0_expected_ms": 4.152,
        "C_D_10_F0_expected_ms": 3.714,
        "C_D_12_F0_expected_ms": 3.390,
        "tolerance_ms": 0.05,
        "all_benchmarks_passed": True
    },
    "physics_consistency": {
        "v_decreases_with_C_D_verified": True,
        "v_decreases_with_F_chain_verified": True,
        "all_Re_in_valid_regime_1e5_1e7": True,
        "all_v_in_1_to_10_ms": True,
        "all_iterations_eq_1_analytic": True
    },
    "plan03_gate": (
        "AUTHORIZED: Identity gate (BUOY-02) PASSED. "
        "Plan 03 may execute using v_handoff range. "
        "Use v_vessel_range_ms = v_vessel_range for fill window sweep. "
        "Pitfall C7: do NOT fix v = 3.0 m/s."
    )
}

_buoy03_path = os.path.join(_outputs_dir, "buoy03_terminal_velocity.json")
with open(_buoy03_path, "w", encoding="utf-8") as f:
    json.dump(buoy03_output, f, indent=2, ensure_ascii=False)
print(f"\nSaved: {_buoy03_path}")

# ============================================================
# SECTION 14: PLOT P1-3 -- TERMINAL VELOCITY SENSITIVITY
# ============================================================

if MATPLOTLIB_AVAILABLE:
    fig, ax = plt.subplots(figsize=(8, 5))

    colors = ['royalblue', 'darkorange', 'forestgreen']
    markers = ['o', 's', '^']

    for i, F_chain in enumerate(F_chain_values):
        cd_vals = []
        vt_vals = []
        for r in results:
            if abs(r["F_chain_N"] - F_chain) < 1e-9 and r["feasible"]:
                cd_vals.append(r["C_D"])
                vt_vals.append(r["v_terminal_ms"])
        ax.plot(cd_vals, vt_vals,
                color=colors[i], marker=markers[i], markersize=7,
                linewidth=2.0, label=f'$F_{{chain}}$ = {F_chain:.0f} N')

    # Reference lines
    ax.axhline(3.0, color='black', linewidth=1.2, linestyle='--', alpha=0.7,
               label='User estimate (3.0 m/s)')
    ax.axhline(2.0, color='crimson', linewidth=1.0, linestyle=':', alpha=0.7,
               label='Min feasible fill bound (2.0 m/s)')

    ax.set_xlabel('Hull drag coefficient $C_D$', fontsize=11)
    ax.set_ylabel('Terminal velocity $v_{terminal}$ (m/s)', fontsize=11)
    ax.set_title('Terminal velocity sensitivity to $C_D$ and chain tension', fontsize=11)
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(True, alpha=0.4)
    ax.set_xlim(0.75, 1.25)
    ax.set_ylim(1.5, 4.5)

    plt.tight_layout()
    _p13_path = os.path.join(_plots_dir, "P1-3_terminal_velocity.png")
    plt.savefig(_p13_path, dpi=150)
    plt.close()
    print(f"Saved: {_p13_path}")
else:
    print("WARNING: matplotlib not available -- P1-3 plot skipped")

# ============================================================
# SECTION 15: FINAL SUMMARY
# ============================================================

print("\n" + "="*60)
print("PLAN 02 COMPLETE -- ALL GATES PASSED")
print("="*60)
print(f"\nBUOY-02 Identity Gate:")
print(f"  W_buoy = {W_buoy:.4f} J")
print(f"  W_iso  = {W_iso:.4f} J")
print(f"  Relative error = {rel_error_tight*100:.4f}% (gate: < 1%)")
print(f"  Gate PASSED at both production and loose tolerances")
print(f"\nBUOY-03 Terminal Velocity (C_D=1.0, F_chain=0):")
print(f"  v_nominal = {v_nominal:.3f} m/s")
print(f"  v_conservative = {v_conservative:.3f} m/s (C_D=1.2, F_chain=200N)")
print(f"  v_range = [{v_range[0]:.3f}, {v_range[1]:.3f}] m/s")
print(f"\nPlan 03 (fill calculations) is now AUTHORIZED.")
print(f"Use v_handoff range, NOT fixed v=3.0 m/s (Pitfall C7).")
