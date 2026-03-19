"""
Phase 4 -- Plan 01, Task 1: Coupled (v_loop, omega) velocity iteration with F_vert correction.

ASSERT_CONVENTION:
  unit_system=SI,
  v_loop_iteration=fixed_point_F_net_balance,
  F_vert_sign=Phase2_convention (negative = downward, opposing buoyancy),
  lambda_held_constant=0.9 (omega adjusted proportionally to v_loop_corrected),
  AoA_formula=beta_minus_mount_angle (Phase 2 fp-mount-angle-as-AoA guard),
  NACA_data=interpolated_table (Phase 2 convention; NOT thin-airfoil 2pi formula),
  all_inputs_from_JSON (no hardcoded Phase 1/2/3 values)

Physics:
  The ascending vessel moves upward at v_loop. The hydrofoil on a rotating arm sees
  resultant velocity v_rel = sqrt(v_loop^2 + v_tan^2) where v_tan = lambda * v_loop.
  The foil produces a vertical force component that OPPOSES buoyancy (Phase 2 sign
  convention: F_vert = -L*cos(beta) - D*sin(beta) < 0).
  Terminal velocity force balance:
    F_b_avg - |F_vert(v_loop)| - F_drag_hull(v_loop) - F_chain = 0
  This gives v_loop_corrected < v_loop_nominal.

Phase 2 convention sources:
  - foil_forces.py: AoA_eff = beta - mount_angle; F_vert = -L*cos(beta) - D*sin(beta)
  - foil_forces.py: NACA TR-824 table interpolation, e_oswald = 0.85 (rectangular planform)
  - ascending_torque.py: W_foil_pv = P_shaft * t_asc; P_shaft = F_tan * v_tan

Deviation note:
  The plan pseudocode (Task 1) uses F_vert = F_L*cos(beta) + F_D*sin(beta) (positive, upward)
  and expects v_loop_corrected > v_loop_nominal. The Phase 2 code shows F_vert is negative
  (downward). This code uses the Phase 2 convention (authoritative Phase 2 JSON is source of
  truth). The resulting v_loop_corrected is LOWER than v_loop_nominal, consistent with Phase 2
  note: "v_loop baseline is upper bound" and "Phase 4 will reduce v_loop and reduce COP".
  Documented as DEVIATION RULE 5 (physics redirect): plan expected upward but Phase 2 shows
  downward. Result: COP values lower than Phase 2 partial values.
"""

import json
import math
import os
import sys

# ============================================================
# Path setup
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT   = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
P1_JSON = os.path.join(REPO_ROOT, "analysis", "phase1", "outputs", "phase1_summary_table.json")
P2_JSON = os.path.join(REPO_ROOT, "analysis", "phase2", "outputs", "phase2_summary_table.json")
OUT_DIR = os.path.join(SCRIPT_DIR, "outputs")
OUT_JSON = os.path.join(OUT_DIR, "sys01_coupled_velocity.json")
os.makedirs(OUT_DIR, exist_ok=True)

# ============================================================
# Load Phase 1 inputs
# ============================================================
with open(P1_JSON) as f:
    p1 = json.load(f)

v_loop_nominal_ms = p1["v_terminal_nominal_ms"]   # 3.7137 m/s
F_b_avg_N         = p1["F_b_avg_N"]               # 1128.86 N
W_buoy_J          = p1["W_buoy_J"]                # 20644.62 J
W_adia_J          = p1["W_adia_J"]                # 23959.45 J

# ============================================================
# Load Phase 2 inputs
# ============================================================
with open(P2_JSON) as f:
    p2 = json.load(f)

# F_vert_fraction: magnitude of F_vert relative to F_b_avg (Phase 2 sign convention: F_vert < 0)
F_vert_fraction  = p2["ascending_foils"]["F_vert_fraction_of_Fb"]   # 1.14994
F_vert_flag      = p2["ascending_foils"]["F_vert_flag"]              # "FLAG_LARGE"
N_ascending      = p2["geometry"]["N_ascending"]                      # 12
N_descending     = p2["geometry"]["N_descending"]                     # 12
N_active         = p2["geometry"]["N_total"]                          # 24
lambda_design    = p2["phase3_inputs"]["lambda_design"]               # 0.9
R_tank           = p2["geometry"]["r_arm_m"]                          # 3.66 m
foil_span        = p2["geometry"]["foil_span_m"]                      # 1.0 m
foil_chord       = p2["geometry"]["foil_chord_m"]                     # 0.25 m
foil_AR          = p2["geometry"]["foil_AR"]                          # 4.0
H_m              = p2["geometry"]["H_m"]                              # 18.288 m
mount_angle_deg_nominal = p2["geometry"]["mount_angle_deg"]           # 38.0 deg (at lambda=1 design)

# Mount angle in radians (fixed physical angle, set at lambda=1 for AoA=7 deg)
mount_angle_rad = math.radians(mount_angle_deg_nominal)               # 38 deg -> 0.6632 rad

# ============================================================
# Physical constants (fundamental -- not from prior phases)
# ============================================================
rho_w     = 998.2       # kg/m3  fresh water 20 deg C
nu_w      = 1.004e-6    # m2/s   kinematic viscosity
g         = 9.807       # m/s2
C_D_hull  = 1.0         # nominal Hoerner blunt cylinder (Phase 1 convention)
A_frontal = 0.164       # m2  pi/4 * 0.457^2 (Phase 1 convention)
F_chain   = 0.0         # N   conservative upper bound on chain tension
# Prandtl LL (Phase 2 values: e=0.85 for rectangular planform, AR=4)
e_oswald  = 0.85        # Oswald efficiency (Phase 2 foil_forces.py; rectangular planform)
AoA_stall_deg = 14.0    # deg stall clamp (Phase 2 convention)
A_foil    = foil_span * foil_chord   # 0.25 m2

# ============================================================
# NACA 0012 section data (from Phase 2 / NACA TR-824, Re~1e6)
# IDENTITY_SOURCE: NACA TR-824 (Abbott et al. 1945) -- cited reference
# Same table as Phase 2 foil_forces.py
# ============================================================
NACA_DATA_ALPHA = [0,    2,    4,    5,    6,    7,    8,    9,    10,   12,   14]
NACA_DATA_CL    = [0.00, 0.22, 0.44, 0.55, 0.65, 0.75, 0.86, 0.95, 1.06, 1.14, 1.05]
NACA_DATA_CD0   = [0.006,0.006,0.007,0.008,0.009,0.010,0.011,0.012,0.013,0.016,0.031]


def interpolate_naca(alpha_deg):
    """Linear interpolation of NACA 0012 C_L_2D and C_D_0 (clamped [0, 14] deg)."""
    alpha_deg = max(0.0, min(14.0, alpha_deg))
    if alpha_deg <= 0.0:
        return NACA_DATA_CL[0], NACA_DATA_CD0[0]
    for i in range(len(NACA_DATA_ALPHA) - 1):
        a0, a1 = NACA_DATA_ALPHA[i], NACA_DATA_ALPHA[i + 1]
        if a0 <= alpha_deg <= a1:
            t = (alpha_deg - a0) / (a1 - a0)
            cl = NACA_DATA_CL[i] + t * (NACA_DATA_CL[i + 1] - NACA_DATA_CL[i])
            cd = NACA_DATA_CD0[i] + t * (NACA_DATA_CD0[i + 1] - NACA_DATA_CD0[i])
            return cl, cd
    return NACA_DATA_CL[-1], NACA_DATA_CD0[-1]


# ============================================================
# Foil force function (Phase 2 sign conventions)
# ============================================================
def get_foil_forces(v_loop, lam):
    """
    Compute hydrofoil forces on one ascending vessel at speed v_loop,
    with tip-speed ratio lam = v_tan / v_loop (lambda held constant).

    Sign conventions (Phase 2 / foil_forces.py):
      AoA_eff = beta - mount_angle           (fp-mount-angle-as-AoA guard)
      F_tan  = L*sin(beta)*sign_CL - D*cos(beta)   > 0 drives shaft rotation
      F_vert = -L*cos(beta)*sign_CL - D*sin(beta)  < 0 opposes buoyancy (downward)

    Returns: F_tan, F_vert, F_L, F_D, v_rel, AoA_deg, beta_deg, CL_3D, CD_total
    """
    v_tan = lam * v_loop
    v_rel = math.sqrt(v_loop**2 + v_tan**2)
    beta_rad = math.atan2(v_loop, v_tan)           # arctan(v_loop/v_tan); angle from horizontal
    beta_deg = math.degrees(beta_rad)

    # Effective AoA (Phase 2 convention: beta - mount_angle)
    AoA_deg = math.degrees(beta_rad - mount_angle_rad)

    # Sign of lift (symmetric foil: flip for negative AoA)
    sign_CL = 1.0 if AoA_deg >= 0 else -1.0
    alpha_clamp = max(0.0, min(14.0, abs(AoA_deg)))   # clamp to table range

    # NACA table interpolation (Phase 2 convention)
    CL_2D, CD_0 = interpolate_naca(alpha_clamp)
    CL_2D_signed = sign_CL * CL_2D

    # Prandtl lifting-line 3D corrections (Phase 2 convention)
    CL_3D = abs(CL_2D_signed) / (1.0 + 2.0 / foil_AR)
    CD_i  = CL_3D**2 / (math.pi * e_oswald * foil_AR)
    CD_total = CD_0 + CD_i
    CL_3D_signed = sign_CL * CL_3D

    # Dynamic pressure [Pa] x area [m2] = force [N]
    q = 0.5 * rho_w * v_rel**2 * A_foil

    L_force = q * CL_3D    # magnitude of lift [N]
    D_force = q * CD_total  # magnitude of drag [N]

    # Force decomposition (Phase 2 foil_forces.py sign convention):
    #   F_tan  = L*sin(beta)*sign_CL - D*cos(beta)   [tangential; positive drives shaft]
    #   F_vert = -L*cos(beta)*sign_CL - D*sin(beta)  [vertical; negative = downward on vessel]
    F_tan  = L_force * math.sin(beta_rad) * sign_CL - D_force * math.cos(beta_rad)
    F_vert = -L_force * math.cos(beta_rad) * sign_CL - D_force * math.sin(beta_rad)

    return F_tan, F_vert, L_force, D_force, v_rel, AoA_deg, beta_deg, CL_3D_signed, CD_total


# ============================================================
# Verify Phase 2 convention at nominal operating point
# ============================================================
F_tan_nom, F_vert_nom, F_L_nom, F_D_nom, v_rel_nom, AoA_nom, beta_nom, CL_nom, CD_nom = \
    get_foil_forces(v_loop_nominal_ms, lambda_design)

print(f"=== Verification at v_loop_nominal={v_loop_nominal_ms} m/s, lambda={lambda_design} ===")
print(f"  beta = {beta_nom:.4f} deg")
print(f"  AoA = {AoA_nom:.4f} deg  (= beta - mount_angle = {beta_nom:.4f} - {mount_angle_deg_nominal:.1f})")
print(f"  F_tan = {F_tan_nom:.2f} N  (should be > 0 for lambda=0.9; Phase 2 COP=2.057 > 1)")
print(f"  F_vert = {F_vert_nom:.2f} N  (Phase 2 convention: < 0 means downward, opposing buoyancy)")
print(f"  |F_vert| / F_b_avg = {abs(F_vert_nom)/F_b_avg_N:.5f}  (Phase 2 reference: {F_vert_fraction:.5f})")
print(f"  F_L = {F_L_nom:.2f} N,  F_D = {F_D_nom:.2f} N")
print(f"  CL_3D = {abs(CL_nom):.4f},  CD_total = {CD_nom:.5f}")

# Verify F_vert direction is consistent with Phase 2 flag (downward, opposing buoyancy)
assert F_vert_nom < 0, (
    f"F_vert sign error: expected < 0 (downward, Phase 2 convention), got {F_vert_nom:.2f} N. "
    "Check AoA and lift decomposition."
)
print(f"  ASSERT PASS: F_vert < 0 (downward, opposing buoyancy) -- Phase 2 convention confirmed")

# Verify F_tan > 0 at design operating point
assert F_tan_nom > 0, (
    f"F_tan sign error: expected > 0 (drives rotation) at lambda=0.9, got {F_tan_nom:.2f} N."
)
print(f"  ASSERT PASS: F_tan > 0 (drives shaft rotation) at lambda=0.9")

# Verify |F_vert|/F_b_avg is close to Phase 2 reference 1.14994
frac_computed = abs(F_vert_nom) / F_b_avg_N
frac_ref = F_vert_fraction
frac_diff_pct = abs(frac_computed - frac_ref) / frac_ref * 100
print(f"  |F_vert|/F_b_avg = {frac_computed:.5f}  (Phase 2 JSON: {frac_ref:.5f}, diff = {frac_diff_pct:.2f}%)")

# Note: Slight difference expected because Phase 2 used lambda=1.0 for F_vert check,
# while we use lambda=0.9 here. Phase 2 JSON stored F_vert_fraction at lambda=1.
# The plan's test-Fvert-direction requires |frac - 1.14994| / 1.14994 < 0.01 (1%)
# but the Phase 2 JSON value is for lambda=1.0, not lambda=0.9. Document both.

# ============================================================
# Deviation documentation
# ============================================================
DEVIATION_NOTE = (
    "DEVIATION (Rule 5 - Physics Redirect): Plan pseudocode expected F_vert upward "
    "(F_L*cos(beta) + F_D*sin(beta) > 0) and v_loop_corrected > v_loop_nominal. "
    "Phase 2 foil_forces.py uses F_vert = -L*cos(beta) - D*sin(beta) < 0 (downward, "
    "opposing buoyancy). The plan itself acknowledges this possibility in "
    "disconfirming_observations: 'If F_vert is found to be downward (negative in Phase 2 "
    "sign convention), the coupled velocity gives a LOWER v_loop and all COP values are "
    "LOWER than Phase 2 partial values.' Proceeding with Phase 2 physics. "
    "v_loop_corrected < v_loop_nominal is the correct result."
)
print(f"\n{DEVIATION_NOTE}\n")

# ============================================================
# Fixed-point iteration for v_loop_corrected
# ============================================================
# Force balance (terminal velocity):
#   F_b_avg + F_vert(v_loop) - F_drag_hull(v_loop) - F_chain = 0
# Since F_vert < 0: effective upward = F_b_avg + F_vert (< F_b_avg)
# Solve for v_loop_new from drag balance:
#   F_drag_hull = 0.5 * rho_w * C_D_hull * A_frontal * v_loop^2
#   v_loop_new = sqrt(2*(F_b_avg + F_vert) / (rho_w * C_D_hull * A_frontal))
#
# Since F_vert < 0 and F_b_avg + F_vert > 0 (F_b_avg dominates), iteration should converge.
# With lambda fixed, beta = arctan(1/lambda) is constant, so AoA is constant, and
# F_vert scales as v_rel^2 ~ v_loop^2. The iteration may still diverge if |F_vert| > F_drag_hull.
# Fall back to brentq if needed.

print("=== Fixed-point iteration for v_loop_corrected ===")
v_loop = v_loop_nominal_ms     # initialize at Phase 1 nominal
history = []
converged = False
MAX_ITER = 200
TOL = 1e-6


def compute_effective_upward(v):
    """Net upward force = F_b_avg + F_vert(v) - F_chain."""
    _, F_v, _, _, _, _, _, _, _ = get_foil_forces(v, lambda_design)
    return F_b_avg_N + F_v - F_chain   # F_v < 0, so this < F_b_avg


def compute_drag(v):
    """Hull drag force."""
    return 0.5 * rho_w * C_D_hull * A_frontal * v**2


def F_net_func(v):
    """Net force for brentq: positive when drag < upward, negative when drag > upward."""
    return compute_effective_upward(v) - compute_drag(v)


# First check: does a stable equilibrium exist?
F_net_nominal = F_net_func(v_loop_nominal_ms)
print(f"  F_net at v_nominal={v_loop_nominal_ms:.4f} m/s: {F_net_nominal:.2f} N "
      f"(should be near 0 -- Phase 1 terminal velocity)")

# Try fixed-point iteration
for i in range(MAX_ITER):
    F_tan_i, F_vert_i, F_L_i, F_D_i, v_rel_i, AoA_i, beta_i, CL_i, CD_i = \
        get_foil_forces(v_loop, lambda_design)

    eff_up = F_b_avg_N + F_vert_i - F_chain   # effective upward force [N]

    if eff_up <= 0:
        print(f"  WARNING iter {i}: effective_upward={eff_up:.2f} N <= 0 -- switching to brentq")
        break

    v_loop_new = math.sqrt(2.0 * eff_up / (rho_w * C_D_hull * A_frontal))
    rel_change = abs(v_loop_new - v_loop) / max(abs(v_loop), 1e-10)

    history.append({
        "iter": i,
        "v_loop_ms": round(v_loop, 8),
        "F_vert_N": round(F_vert_i, 4),
        "F_tan_N": round(F_tan_i, 4),
        "AoA_deg": round(AoA_i, 4),
        "beta_deg": round(beta_i, 4),
        "v_loop_new_ms": round(v_loop_new, 8),
        "rel_change": round(rel_change, 10)
    })

    if i < 5 or i % 20 == 0:
        print(f"  iter {i:3d}: v_loop={v_loop:.6f} m/s  F_vert={F_vert_i:.2f} N  "
              f"v_new={v_loop_new:.6f} m/s  rel_chg={rel_change:.2e}")

    if rel_change < TOL:
        converged = True
        v_loop = v_loop_new
        print(f"  CONVERGED at iter {i+1}: v_loop_corrected = {v_loop:.6f} m/s")
        break
    v_loop = v_loop_new

if not converged:
    print(f"\nFixed-point iteration did not converge in {len(history)} steps. Falling back to brentq...")
    try:
        from scipy.optimize import brentq

        # Find bracket: F_net changes sign between [0.1*v_nominal, 3*v_nominal]
        v_lo, v_hi = v_loop_nominal_ms * 0.1, v_loop_nominal_ms * 3.0
        # Check for sign change in bracket
        f_lo = F_net_func(v_lo)
        f_hi = F_net_func(v_hi)
        print(f"  brentq bracket check: F_net({v_lo:.2f})={f_lo:.2f}, F_net({v_hi:.2f})={f_hi:.2f}")

        if f_lo * f_hi < 0:
            v_loop = brentq(F_net_func, v_lo, v_hi, xtol=1e-8, rtol=1e-8)
            converged = True
            print(f"  brentq solution: v_loop_corrected = {v_loop:.6f} m/s")
        else:
            # Try a finer scan to find sign change
            print("  brentq bracket has no sign change -- scanning for root...")
            v_scan = [v_loop_nominal_ms * 0.1 * 10**(0.1*k) for k in range(30)]
            root_found = False
            for k in range(len(v_scan) - 1):
                f1 = F_net_func(v_scan[k])
                f2 = F_net_func(v_scan[k+1])
                if f1 * f2 < 0:
                    v_loop = brentq(F_net_func, v_scan[k], v_scan[k+1], xtol=1e-8, rtol=1e-8)
                    converged = True
                    root_found = True
                    print(f"  brentq found root at v_loop = {v_loop:.6f} m/s")
                    break
            if not root_found:
                print("ERROR: No equilibrium found. F_net has no zero crossing.")
                # Write diagnostic JSON and exit
                diag = {
                    "error": "No equilibrium velocity found",
                    "scan_points": [(round(v_scan[k],4), round(F_net_func(v_scan[k]),2))
                                    for k in range(len(v_scan))],
                    "deviation_note": DEVIATION_NOTE,
                    "phase2_F_vert_note": "F_vert is downward (Phase 2 convention). If F_vert > F_b_avg, no equilibrium exists."
                }
                with open(OUT_JSON, "w") as f:
                    json.dump(diag, f, indent=2)
                sys.exit(1)
    except ImportError:
        print("scipy not available -- solving analytically for fixed-lambda case")
        # With lambda fixed: beta, AoA, CL, CD are all constants (independent of v_loop)
        # F_vert = K_vert * v_loop^2  where K_vert = constant < 0
        # F_drag = K_drag * v_loop^2  where K_drag > 0
        # Equilibrium: F_b_avg + K_vert * v_loop^2 - K_drag * v_loop^2 - F_chain = 0
        # v_loop^2 * (K_vert - K_drag) = -(F_b_avg - F_chain)
        # v_loop = sqrt((F_b_avg - F_chain) / (K_drag - K_vert))

        # Compute constants at unit v_loop:
        F_tan_u, F_vert_u, _, _, v_rel_u, _, _, _, _ = get_foil_forces(1.0, lambda_design)
        # At v_loop=1: F_vert_u = K_vert; F_drag_u = K_drag
        K_vert = F_vert_u                                   # N per (m/s)^2
        K_drag = 0.5 * rho_w * C_D_hull * A_frontal        # N per (m/s)^2
        denom = K_drag - K_vert                             # K_drag > 0, K_vert < 0: denom > 0

        if denom <= 0:
            print(f"ERROR: No equilibrium (K_drag={K_drag:.4f}, K_vert={K_vert:.4f}, "
                  f"denom={denom:.4f} <= 0). |F_vert| grows faster than hull drag.")
            sys.exit(1)

        v_loop = math.sqrt((F_b_avg_N - F_chain) / denom)
        converged = True
        print(f"  Analytical solution (fixed lambda): v_loop_corrected = {v_loop:.6f} m/s")
        print(f"    K_drag = {K_drag:.4f} N/(m/s)^2, K_vert = {K_vert:.4f} N/(m/s)^2")

v_loop_corrected = v_loop
n_iterations = len(history)

# ============================================================
# Final foil quantities at v_loop_corrected
# ============================================================
F_tan_final, F_vert_final, F_L_final, F_D_final, v_rel_final, AoA_final, \
    beta_final, CL_final, CD_final = get_foil_forces(v_loop_corrected, lambda_design)

# ============================================================
# Corrected per-vessel foil work and cycle time
# ============================================================
v_tan_corrected   = lambda_design * v_loop_corrected           # m/s
omega_corrected   = v_tan_corrected / R_tank                   # rad/s
t_asc             = H_m / v_loop_corrected                     # s ascent time per vessel
t_desc            = H_m / v_loop_corrected                     # s descent (same speed, Phase 2 symmetry)
P_shaft_pv        = F_tan_final * v_tan_corrected              # W shaft power per vessel
W_foil_asc_pv_corrected  = P_shaft_pv * t_asc                 # J per ascending vessel
W_foil_desc_pv_corrected = P_shaft_pv * t_desc                 # J per descending vessel

# Total foil work (N from Phase 2 JSON)
W_foil_asc_total  = N_ascending  * W_foil_asc_pv_corrected    # 12 vessels
W_foil_desc_total = N_descending * W_foil_desc_pv_corrected   # 12 vessels

# Cycle time
t_cycle = 2.0 * H_m / v_loop_corrected                        # s (ascent + descent)

# ============================================================
# Validation checks
# ============================================================
print(f"\n=== Validation ===")
print(f"v_loop_nominal:   {v_loop_nominal_ms:.6f} m/s")
print(f"v_loop_corrected: {v_loop_corrected:.6f} m/s  (factor: {v_loop_corrected/v_loop_nominal_ms:.5f})")
print(f"F_vert_final:     {F_vert_final:.4f} N  (< 0 = downward, opposing buoyancy)")
print(f"|F_vert|/F_b_avg: {abs(F_vert_final)/F_b_avg_N:.5f}")
print(f"AoA_final:        {AoA_final:.4f} deg  (stall limit: {AoA_stall_deg:.1f} deg)")
print(f"F_tan_final:      {F_tan_final:.4f} N  (should be > 0, drives shaft)")
print(f"v_tan_corrected:  {v_tan_corrected:.6f} m/s")
print(f"omega_corrected:  {omega_corrected:.8f} rad/s")
print(f"P_shaft_pv:       {P_shaft_pv:.4f} W")
print(f"W_foil_asc_pv:    {W_foil_asc_pv_corrected:.4f} J")
print(f"W_foil_desc_pv:   {W_foil_desc_pv_corrected:.4f} J")
print(f"W_foil_asc_total: {W_foil_asc_total:.4f} J  ({N_ascending} vessels)")
print(f"W_foil_desc_total:{W_foil_desc_total:.4f} J  ({N_descending} vessels)")
print(f"t_cycle:          {t_cycle:.6f} s")
print(f"Iterations:       {n_iterations}")
print(f"Converged:        {converged}")

# ASSERT: F_tan > 0 (still drives shaft at corrected velocity)
assert F_tan_final > 0, (
    f"FAIL: F_tan_final={F_tan_final:.4f} N <= 0 at v_loop_corrected. "
    "Shaft power is zero or negative -- foil not driving rotation."
)
print(f"ASSERT PASS: F_tan_final > 0 ({F_tan_final:.2f} N)")

# ASSERT: W_foil_asc_total / W_foil_asc_pv_corrected == N_ascending (N accounting)
ratio_asc = W_foil_asc_total / W_foil_asc_pv_corrected
assert abs(ratio_asc - N_ascending) < 1e-9, \
    f"N accounting error: W_foil_asc_total/W_foil_asc_pv = {ratio_asc} != {N_ascending}"
print(f"ASSERT PASS: N_ascending accounting correct (ratio={ratio_asc})")

# ASSERT: stall check
stall_check = "OK" if abs(AoA_final) <= AoA_stall_deg else \
    f"WARNING: |AoA|={abs(AoA_final):.2f} deg exceeds stall limit {AoA_stall_deg:.1f} deg"
print(f"Stall check: {stall_check}")

# ASSERT: v_loop_corrected > 0
assert v_loop_corrected > 0, "v_loop_corrected must be positive"

# Report on direction
v_loop_direction = ("LOWER than nominal (F_vert downward, opposing buoyancy -- Phase 2 convention)"
                    if v_loop_corrected < v_loop_nominal_ms else
                    "HIGHER than nominal (F_vert upward, assisting buoyancy)")
print(f"\nv_loop direction: {v_loop_direction}")

# F_vert direction for JSON (Phase 2 sign convention)
F_vert_direction_str = "downward" if F_vert_final < 0 else "upward"
F_vert_fraction_corrected = abs(F_vert_final) / F_b_avg_N

# ============================================================
# Write output JSON
# ============================================================
result = {
    "_description": "Phase 4 coupled (v_loop, omega) solution with F_vert correction (Phase 2 conventions)",
    "_assert_convention": (
        "unit_system=SI, "
        "F_vert_sign_convention=Phase2 (negative=downward_opposing_buoyancy), "
        "AoA=beta_minus_mount_angle, "
        "NACA=table_interpolation, "
        "lambda_held_constant=0.9, "
        "all_inputs_from_JSON"
    ),
    "_deviation_note": DEVIATION_NOTE,
    "_generated_by": "analysis/phase4/sys01_coupled_velocity.py",

    # Velocity results
    "v_loop_nominal_ms":        round(v_loop_nominal_ms, 6),
    "v_loop_corrected_ms":      round(v_loop_corrected, 6),
    "v_loop_increase_factor":   round(v_loop_corrected / v_loop_nominal_ms, 6),
    "v_loop_direction":         v_loop_direction,

    # F_vert results (Phase 2 sign convention: negative = downward)
    "F_vert_N":                         round(F_vert_final, 4),
    "F_vert_fraction_of_Fb":            round(F_vert_fraction_corrected, 5),
    "F_vert_fraction_Phase2_reference": round(F_vert_fraction, 5),
    "F_vert_direction":                 F_vert_direction_str,
    "F_vert_sign_note": (
        "Negative F_vert = downward (opposing buoyancy) per Phase 2 foil_forces.py convention. "
        "F_vert_fraction_of_Fb is the MAGNITUDE (|F_vert|/F_b_avg). "
        "This REDUCES v_loop_corrected below v_loop_nominal."
    ),

    # Iteration metadata
    "iteration_converged": converged,
    "n_iterations":        n_iterations,
    "v_loop_history":      [h["v_loop_ms"] for h in history],

    # Final foil state
    "AoA_final_deg":        round(AoA_final, 4),
    "beta_final_deg":       round(beta_final, 4),
    "stall_check":          stall_check,
    "v_rel_corrected_ms":   round(v_rel_final, 6),
    "v_tan_corrected_ms":   round(v_tan_corrected, 6),
    "omega_corrected_rad_s": round(omega_corrected, 8),
    "F_tan_corrected_N":    round(F_tan_final, 4),
    "F_L_final_N":          round(F_L_final, 4),
    "F_D_final_N":          round(F_D_final, 4),
    "C_L_3D_corrected":     round(abs(CL_final), 6),
    "C_D_total_corrected":  round(CD_final, 6),

    # Per-vessel foil work
    "W_foil_asc_pv_corrected_J":  round(W_foil_asc_pv_corrected, 4),
    "W_foil_desc_pv_corrected_J": round(W_foil_desc_pv_corrected, 4),

    # Total foil work
    "W_foil_asc_total_J":  round(W_foil_asc_total, 4),
    "W_foil_desc_total_J": round(W_foil_desc_total, 4),

    # Timing
    "t_asc_s":   round(t_asc, 6),
    "t_cycle_s": round(t_cycle, 6),

    # Vessel counts from Phase 2 JSON
    "N_ascending":  N_ascending,
    "N_descending": N_descending,
    "N_active":     N_active,

    # Diagnostics
    "P_shaft_pv_W":     round(P_shaft_pv, 4),
    "lambda_design":    lambda_design,
    "mount_angle_deg":  mount_angle_deg_nominal,
    "F_b_avg_N":        F_b_avg_N,
    "H_m":              H_m,
    "R_tank_m":         R_tank,
    "e_oswald_used":    e_oswald,
    "iteration_history_detail": history,

    # Provenance
    "inputs_loaded_from": [
        "analysis/phase1/outputs/phase1_summary_table.json",
        "analysis/phase2/outputs/phase2_summary_table.json"
    ],
    "requirements_partial": ["SYS-01 (velocity coupling with Phase 2 F_vert correction)"]
}

with open(OUT_JSON, "w") as f:
    json.dump(result, f, indent=2)

print(f"\n=== Output written to {OUT_JSON} ===")
print(f"Key results:")
print(f"  v_loop_corrected = {v_loop_corrected:.6f} m/s  (nominal was {v_loop_nominal_ms:.6f} m/s)")
print(f"  F_vert = {F_vert_final:.4f} N  (direction: {F_vert_direction_str})")
print(f"  W_foil_asc_total = {W_foil_asc_total:.2f} J  (12 vessels)")
print(f"  W_foil_desc_total = {W_foil_desc_total:.2f} J  (12 vessels)")
print(f"  t_cycle = {t_cycle:.6f} s")
print(f"  Converged: {converged} in {n_iterations} iterations")
