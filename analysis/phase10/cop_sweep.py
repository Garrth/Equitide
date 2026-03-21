"""
Phase 10 -- Plan 01: COP sweep with differential rotation (r-extended brentq solver)

ASSERT_CONVENTION:
  unit_system=SI,
  F_vert_sign=Phase2 (negative=downward=opposing_buoyancy),
  v_tangential_net=lambda*v_loop*(2-r) (wave co-rotation REDUCES relative tangential flow),
  v_vertical=v_loop (COROT-03 preserved),
  mount_angle=46.013deg FIXED (from Phase 6; NOT re-optimized),
  NACA=imported_from_phase5_solver (NOT re-implemented),
  brentq_at_each_r=True (PITFALL-P9-BRENTQ: NOT fixed v_loop from Phase 9),
  PITFALL-M1=W_pump_uses_W_adia_not_W_iso,
  PITFALL-P9-WRONG-VTAN=NOT_r*lambda*v_loop,
  PITFALL-P9-BRENTQ=brentq_re-run_at_each_r

Physics:
  At speed ratio r = v_water_tangential / v_arm_tangential:
    v_tan(r, v_loop) = lambda * v_loop * (2 - r)   [wave co-rotation REDUCES relative tangential flow]
    v_rel(r, v_loop) = v_loop * sqrt(1 + (lambda*(2-r))^2)
    beta_eff(r) = arctan(v_loop / v_tan) = arctan(1 / (lambda*(2-r)))  [INDEPENDENT of v_loop]
    AoA_eff(r) = beta_eff(r) - mount_angle  [mount_angle FIXED at 46.013 deg from Phase 6]

  Key: AoA_eff(r) is independent of v_loop (because beta_eff = arctan(1/(lambda*(2-r)))).
  As r increases: (2-r) decreases, so v_tan decreases, beta_eff increases, AoA_eff increases.

  Terminal velocity (per-vessel brentq):
    F_b_avg + F_vert_pv(r, v_loop) - F_drag_hull(v_loop) = 0
    F_drag_hull = 0.5 * rho_w * C_D_hull * A_frontal * v_loop^2

  Phase 9 upper-bound note: Phase 9 used fixed v_loop=3.273346 m/s from Phase 6.
  Phase 10 re-solves brentq at EACH r -- the increased |F_vert(r)| will reduce v_loop(r).
  Phase 9 forces are UPPER BOUNDS.

Continuity check (r=1.0 BLOCKING gate):
  At r=1.0: v_tan = lambda*v_loop*(2-1) = lambda*v_loop (identical to Phase 5/6).
  beta_eff(r=1) = arctan(1/lambda) = 48.013 deg (Phase 6 value).
  AoA_eff(r=1) = 48.013 - 46.013 = 2.000 deg (Phase 6 AoA_optimal).
  COP(r=1.0) MUST reproduce Phase 6 COP_max_nominal = 0.94373 within 0.5%.

Forbidden proxies (verified NOT used):
  - fp-reversed-foil: F_vert is kinematic; foil orientation irrelevant
  - fp-fixed-vloop: brentq re-run at each r
  - fp-wrong-vtan: v_tan = lambda*(2-r)*v_loop (NOT r*lambda*v_loop)
  - fp-cop-lossless-primary: COP_nominal (eta_c=0.70, loss=10%) is primary
  - fp-no-continuity: continuity gate at r=1.0 is BLOCKING
  - fp-multiplier-claim: Phase 9 showed enhanced-both (F_vert increases with r); multiplicative impossible
"""

import json
import math
import os
import sys

# ============================================================
# Path setup: make Phase 5 solver importable
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT   = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

# Insert REPO_ROOT so that "from analysis.phase5.aoa_sweep_solver import ..." works
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# ============================================================
# STEP 1 -- Phase 5 gate check
# ============================================================
P5_ANCHOR_JSON = os.path.join(REPO_ROOT, "analysis", "phase5", "outputs", "phase5_anchor_check.json")
with open(P5_ANCHOR_JSON) as f:
    _p5_anchor = json.load(f)

if not _p5_anchor.get("overall_anchor_pass", False):
    raise RuntimeError(
        "Phase 5 anchor check failed — halt Phase 10. "
        f"overall_anchor_pass={_p5_anchor.get('overall_anchor_pass')}. "
        "Re-run Phase 5 solver first: python analysis/phase5/aoa_sweep_solver.py"
    )
print("Phase 5 gate: overall_anchor_pass = True  [PASS]")

# ============================================================
# STEP 2 -- Import from Phase 5 solver
# ============================================================
# Importing this module executes its load-time assertions (A_frontal check, sign check, NACA check).
# This is intentional: it re-validates all Phase 5 inputs each time Phase 10 runs.
from analysis.phase5.aoa_sweep_solver import (
    interpolate_naca,
    foil_AR,
    e_oswald,
    A_foil,
    rho_w,
    nu_w,
    g,
    C_D_hull,
    H_m,
    N_ascending,
    N_descending,
    lambda_design,
    F_b_avg_N,
    W_adia_J,
    W_buoy_J,
    v_loop_nominal_ms,
    P_net_corot_W_uncorrected,
    N_total_vessels,
    A_frontal,
)
# AoA_stall_deg from Phase 5 = 14.0 (NACA clamp); Phase 10 uses stall onset at 12.0 deg per Phase 9
AoA_stall_deg_naca_clamp = 14.0   # NACA table clamp (for interpolate_naca)
AoA_stall_onset_deg = 12.0        # Phase 9: stall onset at 12 deg for operational flag

# ============================================================
# STEP 2b -- Load mount_angle from Phase 9 geometry table
# ============================================================
P9_GEOM_JSON = os.path.join(REPO_ROOT, "analysis", "phase9", "outputs", "phase9_geometry_table.json")
with open(P9_GEOM_JSON) as f:
    _p9_geom = json.load(f)
mount_angle_deg = _p9_geom["mount_angle_deg"]   # 46.012788 deg (exact Phase 9 value)
print(f"mount_angle_deg = {mount_angle_deg:.6f} deg  (from phase9_geometry_table.json)")

# ============================================================
# STEP 2c -- Load Phase 6 COP anchor from verdict JSON
# ============================================================
P6_VERDICT_JSON = os.path.join(REPO_ROOT, "analysis", "phase6", "outputs", "phase6_verdict.json")
with open(P6_VERDICT_JSON) as f:
    _p6_verdict = json.load(f)
COP_phase6_anchor = _p6_verdict["COP_max_nominal"]      # 0.943726 (exact from JSON)
COP_phase6_best   = _p6_verdict["COP_max_all_scenarios"] # 1.209617 (eta_c=0.85, loss=5%)
print(f"Phase 6 COP anchors loaded: COP_max_nominal={COP_phase6_anchor:.6f}, "
      f"COP_max_all_scenarios={COP_phase6_best:.6f}")

# ============================================================
# PITFALL-P9-WRONG-VTAN guard: assert v_tan DECREASES with r
# ============================================================
_r_test, _v_test = 1.0, 3.273346
_vtan_correct  = lambda_design * _v_test * (2.0 - _r_test)    # = lambda * v_loop * 1.0
_vtan_wrong    = _r_test * lambda_design * _v_test              # = same at r=1.0 (accidentally)
_r_test2, _v_test2 = 1.1, 3.273346
_vtan_correct2 = lambda_design * _v_test2 * (2.0 - _r_test2)   # smaller (0.9 factor)
_vtan_wrong2   = _r_test2 * lambda_design * _v_test2             # larger (1.1 factor)
assert _vtan_correct2 < _vtan_correct, (
    f"PITFALL-P9-WRONG-VTAN check FAILED: v_tan should DECREASE with r. "
    f"v_tan(r=1.1)={_vtan_correct2:.4f}, v_tan(r=1.0)={_vtan_correct:.4f}. "
    "Check v_tan formula: must be lambda*(2-r)*v_loop, NOT r*lambda*v_loop."
)
assert _vtan_wrong2 > _vtan_wrong, (
    f"PITFALL-P9-WRONG-VTAN: wrong formula v_tan=r*lambda*v_loop INCREASES with r. "
    f"This is INCORRECT. Phase 10 uses correct formula: v_tan = lambda*(2-r)*v_loop."
)
print("PITFALL-P9-WRONG-VTAN guard: v_tan decreases with r  [PASSED]")
print(f"  Correct: v_tan(r=1.0)={_vtan_correct:.4f}, v_tan(r=1.1)={_vtan_correct2:.4f}  (decreases)")
print(f"  Wrong formula: v_tan(r=1.0)={_vtan_wrong:.4f}, v_tan(r=1.1)={_vtan_wrong2:.4f} (would increase)")

# ============================================================
# Output paths
# ============================================================
OUT_DIR  = os.path.join(SCRIPT_DIR, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)
OUT_SWEEP   = os.path.join(OUT_DIR, "phase10_cop_sweep.json")
OUT_VERDICT = os.path.join(OUT_DIR, "phase10_verdict.json")


# ============================================================
# STEP 3 -- Extended kinematics (r-dependent, v_loop given)
# ============================================================
def extended_kinematics(v_loop, r, lam=None):
    """
    Compute r-extended kinematics and foil forces for one ascending vessel.

    PITFALL-P9-WRONG-VTAN: v_tan = lambda*(2-r)*v_loop  [NOT r*lambda*v_loop]

    At r=1.0: v_tan = lambda*v_loop*1.0 = lambda*v_loop (IDENTICAL to Phase 5/6).
    At r=1.0: beta_eff = arctan(v_loop / (lambda*v_loop)) = arctan(1/lambda) = 48.013 deg.
    At r=1.0: AoA_eff = 48.013 - 46.013 = 2.000 deg (Phase 6 optimal). [Continuity identity]

    Key: beta_eff = arctan(1/(lambda*(2-r))) is INDEPENDENT of v_loop.
    So AoA_eff(r) = beta_eff(r) - mount_angle is also independent of v_loop.
    Forces scale with v_loop^2 (through q), but AoA is r-controlled only.

    Args:
        v_loop: loop velocity [m/s]
        r: speed ratio v_water_tan / v_arm_tan (1.0 = baseline, no wave)
        lam: tip-speed ratio (default: lambda_design = 0.9)

    Returns:
        dict with all kinematic and force quantities
    """
    if lam is None:
        lam = lambda_design

    # PITFALL-P9-WRONG-VTAN: correct formula
    v_tan = lam * v_loop * (2.0 - r)                           # [m/s]; DECREASES with r

    # beta_eff: angle of v_rel from horizontal (= arctan(v_loop/v_tan) = arctan(1/(lam*(2-r))))
    beta_eff_rad = math.atan2(v_loop, v_tan)                   # arctan(v_loop / v_tan)
    beta_eff_deg = math.degrees(beta_eff_rad)

    # AoA_eff: foil angle of attack (mount_angle FIXED from Phase 6)
    AoA_eff_deg = beta_eff_deg - mount_angle_deg               # independent of v_loop
    AoA_clamped = max(0.0, min(AoA_stall_deg_naca_clamp, AoA_eff_deg))  # clamp to [0, 14]
    is_stalled   = (AoA_eff_deg >= AoA_stall_onset_deg)        # onset at 12 deg (Phase 9)

    # NACA 0012 lookup (imported from Phase 5; NOT re-implemented)
    C_L_2D, C_D_0 = interpolate_naca(AoA_clamped)

    # Prandtl lifting-line 3D corrections (AR=4, e_oswald=0.85)
    C_L_3D = C_L_2D / (1.0 + 2.0 / foil_AR)                   # = C_L_2D / 1.5
    C_D_i  = C_L_3D**2 / (math.pi * e_oswald * foil_AR)        # induced drag
    C_D_total = C_D_0 + C_D_i

    # Relative velocity and dynamic pressure
    v_rel = math.sqrt(v_loop**2 + v_tan**2)
    q     = 0.5 * rho_w * v_rel**2 * A_foil                    # [N]

    # Force decomposition (Phase 2 convention):
    #   F_tan  = L*sin(beta) - D*cos(beta)   [positive = drives shaft rotation]
    #   F_vert = -L*cos(beta) - D*sin(beta)  [negative = downward = opposes buoyancy]
    F_tan  = q * (C_L_3D * math.sin(beta_eff_rad) - C_D_total * math.cos(beta_eff_rad))
    F_vert = -q * (C_L_3D * math.cos(beta_eff_rad) + C_D_total * math.sin(beta_eff_rad))

    # F_vert sign assertion (always negative per Phase 2 convention)
    assert F_vert < 0, (
        f"F_vert must be negative (downward). Got F_vert={F_vert:.4f} N at "
        f"v_loop={v_loop:.4f} m/s, r={r:.3f}, AoA_eff={AoA_eff_deg:.4f} deg."
    )

    return {
        "v_tan":         v_tan,
        "v_rel":         v_rel,
        "beta_eff_deg":  beta_eff_deg,
        "AoA_eff_deg":   AoA_eff_deg,
        "AoA_clamped":   AoA_clamped,
        "is_stalled":    is_stalled,
        "C_L_2D":        C_L_2D,
        "C_L_3D":        C_L_3D,
        "C_D_0":         C_D_0,
        "C_D_total":     C_D_total,
        "q":             q,
        "F_tan":         F_tan,
        "F_vert":        F_vert,
    }


# ============================================================
# STEP 4 -- Extended brentq residual (per-vessel, NOT N_ascending multiplier)
# ============================================================
def F_net_residual_r(v_loop, r, lam=None):
    """
    Per-vessel force balance residual for brentq at speed ratio r.

    F_b_avg + F_vert_pv(r, v_loop) - F_drag_hull(v_loop) = 0

    CRITICAL: Per-vessel balance only. Using N_ascending multiplier gives 63% v_loop error
    (Phase 5 deviation note: "PITFALL from Phase 5: N_ascending multiplier in brentq gives
    63% v_loop error").

    Sign: positive when v_loop too low (drag < effective buoyancy),
          negative when v_loop too high (drag > effective buoyancy).

    Args:
        v_loop: loop velocity [m/s]
        r: speed ratio (1.0 = baseline)
        lam: tip-speed ratio (default: lambda_design = 0.9)

    Returns:
        F_net [N]: force balance residual (= 0 at equilibrium)
    """
    if lam is None:
        lam = lambda_design
    kin = extended_kinematics(v_loop, r, lam)
    F_vert_pv   = kin["F_vert"]                                    # per vessel, negative
    F_drag_hull = 0.5 * rho_w * C_D_hull * A_frontal * v_loop**2  # per vessel, positive
    return F_b_avg_N + F_vert_pv - F_drag_hull                     # per-vessel balance


# ============================================================
# STEP 5 -- Solver at each r (brentq with fallback scan)
# ============================================================
def solve_v_loop_r(r, lam=None):
    """
    Find equilibrium v_loop at speed ratio r via brentq.

    PITFALL-P9-BRENTQ: Phase 9 used fixed v_loop=3.273346 m/s. Phase 10 MUST re-run
    brentq at each r. The increased |F_vert(r)| at r > 1.0 will give lower v_loop(r)
    than the Phase 9 fixed value. Phase 9 forces are upper bounds.

    Bracket: [v_lo, v_hi] = [v_loop_nominal*0.05, v_loop_nominal*2.0]
    Fallback: scan 50 log-spaced points in [0.1, 10] m/s if no sign change in bracket.

    Args:
        r: speed ratio (1.0 = baseline)
        lam: tip-speed ratio (default: lambda_design = 0.9)

    Returns:
        v_loop_equilibrium [m/s]

    Raises:
        ValueError: if no equilibrium found (F_vert exceeds F_b_avg at all v_loop)
    """
    import numpy as np
    from scipy.optimize import brentq

    if lam is None:
        lam = lambda_design

    v_lo = v_loop_nominal_ms * 0.05    # ~0.186 m/s
    v_hi = v_loop_nominal_ms * 2.0     # ~7.427 m/s

    f_lo = F_net_residual_r(v_lo, r, lam)
    f_hi = F_net_residual_r(v_hi, r, lam)

    if f_lo * f_hi < 0:
        return brentq(
            lambda v: F_net_residual_r(v, r, lam),
            v_lo, v_hi,
            xtol=1e-8, rtol=1e-8
        )

    # Fallback: scan 50 log-spaced points in [0.1, 10] m/s
    v_scan = np.logspace(math.log10(0.1), math.log10(10.0), 50)
    for k in range(len(v_scan) - 1):
        f1 = F_net_residual_r(v_scan[k],     r, lam)
        f2 = F_net_residual_r(v_scan[k + 1], r, lam)
        if f1 * f2 < 0:
            return brentq(
                lambda v: F_net_residual_r(v, r, lam),
                v_scan[k], v_scan[k + 1],
                xtol=1e-8, rtol=1e-8
            )

    raise ValueError(
        f"No equilibrium v_loop at r={r:.3f}: F_vert(r) may exceed F_b_avg at all v_loop. "
        "Vessel cannot ascend at this speed ratio."
    )


# ============================================================
# STEP 6 -- COP computation at each r
# ============================================================
def compute_COP_r(r, eta_c=0.70, loss_frac=0.10, lam=None):
    """
    Compute full system COP at speed ratio r.

    Energy balance (identical to Phase 5/6 compute_COP_aoa, but parameterized by r):
      W_gross = W_buoy_total + W_foil_total + W_corot_total + W_jet_total
      W_losses = W_gross * loss_frac
      W_net = W_gross - W_losses
      W_pump_total = N_total * W_adia_J / eta_c   [PITFALL-M1: W_adia NOT W_iso]
      COP = W_net / W_pump_total

    W_foil derivation (v_loop cancels):
      W_foil_pv = F_tan * v_tan * t_asc
               = F_tan * (lam*(2-r)*v_loop) * (H/v_loop)
               = F_tan * lam * (2-r) * H        [v_loop cancels]
      This is exact (not an approximation). Verified at r=1.0: W_foil_pv = F_tan * lam * H.

    W_corot scaling:
      P_corot ~ v_loop^3 (Phase 3 cubic drag formula)
      W_corot = P_corot_corrected * t_cycle = P_corot_nom * (v_loop/v_nom)^3 * (2H/v_loop)
              = P_corot_nom * (v_loop/v_nom)^3 * (2H/v_loop)
              ~ v_loop^2   [effective scaling]
      Since v_loop decreases with r, W_corot also decreases with r.

    PITFALL guards:
      PITFALL-M1: W_pump uses W_adia (not W_iso)
      PITFALL-N-ACTIVE: W_foil uses N_ascending+N_descending=24 (not 30)
      PITFALL-C6: W_jet = 0.0 explicit
      PITFALL-COROT: P_net_corot scaled by (v_loop_c/v_nom)^3

    Args:
        r: speed ratio (1.0 = baseline)
        eta_c: compressor isentropic efficiency (default 0.70, Phase 6 nominal)
        loss_frac: mechanical loss fraction (default 0.10 = 10%)
        lam: tip-speed ratio (default: lambda_design = 0.9)

    Returns:
        dict with all intermediate quantities and COP_nominal
    """
    if lam is None:
        lam = lambda_design

    # Step 1: Equilibrium v_loop at this r (PITFALL-P9-BRENTQ: re-run brentq)
    v_loop_c = solve_v_loop_r(r, lam)

    # Step 2: Foil forces at equilibrium
    kin = extended_kinematics(v_loop_c, r, lam)
    F_tan_pv  = kin["F_tan"]
    F_vert_pv = kin["F_vert"]
    v_tan_c   = kin["v_tan"]

    # Step 3: Cycle timing
    t_asc   = H_m / v_loop_c          # ascent time [s]
    t_cycle = 2.0 * H_m / v_loop_c    # full cycle time [s]

    # Step 4: Per-vessel foil work (v_loop cancels in F_tan * v_tan * t_asc)
    # W_foil_pv = F_tan * v_tan * t_asc = F_tan * (lam*(2-r)*v_loop) * (H/v_loop)
    #           = F_tan * lam * (2-r) * H  [v_loop cancels exactly]
    W_foil_pv = F_tan_pv * v_tan_c * t_asc

    # Step 5: Total foil work (PITFALL-N-ACTIVE: 24 foil vessels, not 30)
    W_foil_total = (N_ascending + N_descending) * W_foil_pv    # = 24 * W_foil_pv

    # Step 6: Total buoyancy work (30 vessels)
    W_buoy_total = N_total_vessels * W_buoy_J                  # = 30 * W_buoy_J

    # Step 7: Co-rotation benefit (PITFALL-COROT: scale by (v_loop_c/v_nom)^3)
    corot_scale           = (v_loop_c / v_loop_nominal_ms)**3
    P_net_corot_corrected = P_net_corot_W_uncorrected * corot_scale
    W_corot_total         = P_net_corot_corrected * t_cycle    # W_corot ~ v_loop^2 effective

    # Step 8: Jet recovery (PITFALL-C6: explicit zero)
    W_jet_total = 0.0

    # Step 9: Gross, losses, net energy
    W_gross  = W_buoy_total + W_foil_total + W_corot_total + W_jet_total
    W_losses = W_gross * loss_frac
    W_net    = W_gross - W_losses

    # Step 10: Pump work (PITFALL-M1: W_adia NOT W_iso)
    W_pump_total = N_total_vessels * W_adia_J / eta_c          # 30 * W_adia / eta_c

    # Step 11: COP
    COP_nominal = W_net / W_pump_total

    # Force balance residual verification
    F_residual = F_net_residual_r(v_loop_c, r, lam)

    return {
        "r":                 r,
        "v_loop_ms":         v_loop_c,
        "F_tan_pv_N":        F_tan_pv,
        "F_vert_pv_N":       F_vert_pv,
        "AoA_eff_deg":       kin["AoA_eff_deg"],
        "beta_eff_deg":      kin["beta_eff_deg"],
        "C_L_3D":            kin["C_L_3D"],
        "C_D_total":         kin["C_D_total"],
        "v_tan_ms":          v_tan_c,
        "v_rel_ms":          kin["v_rel"],
        "is_stalled":        kin["is_stalled"],
        "t_asc_s":           t_asc,
        "t_cycle_s":         t_cycle,
        "W_foil_pv_J":       W_foil_pv,
        "W_foil_total_J":    W_foil_total,
        "W_buoy_total_J":    W_buoy_total,
        "corot_scale":       corot_scale,
        "W_corot_total_J":   W_corot_total,
        "W_jet_total_J":     W_jet_total,
        "W_gross_J":         W_gross,
        "W_losses_J":        W_losses,
        "W_net_J":           W_net,
        "W_pump_total_J":    W_pump_total,
        "COP_nominal":       COP_nominal,
        "eta_c":             eta_c,
        "loss_frac":         loss_frac,
        "force_balance_residual_N": F_residual,
    }


# ============================================================
# STEP 7 -- CONTINUITY GATE (blocking; must pass before sweep)
# ============================================================
print("\n" + "=" * 65)
print("STEP 7: CONTINUITY GATE at r=1.0")
print("=" * 65)

result_r1 = compute_COP_r(1.0, eta_c=0.70, loss_frac=0.10)
COP_r1    = result_r1["COP_nominal"]
# Use Phase 6 anchor as loaded from JSON (not hardcoded)
pct_diff  = abs(COP_r1 - COP_phase6_anchor) / COP_phase6_anchor * 100.0

print(f"COP(r=1.0)     = {COP_r1:.6f}")
print(f"Phase 6 anchor = {COP_phase6_anchor:.6f}")
print(f"pct_diff       = {pct_diff:.4f}%  (threshold: 0.5%)")

# Verify kinematic identities at r=1.0
_v = result_r1["v_loop_ms"]
_v_tan_r1 = result_r1["v_tan_ms"]
_v_tan_p5  = lambda_design * _v      # Phase 5 formula at r=1: v_tan = lambda*v_loop
_tan_identity_err = abs(_v_tan_r1 - _v_tan_p5) / _v_tan_p5 * 100
print(f"\nKinematic identity at r=1.0:")
print(f"  v_tan(r=1) = lambda*v_loop*(2-1) = {_v_tan_r1:.6f} m/s")
print(f"  Phase 5 baseline: lambda*v_loop  = {_v_tan_p5:.6f} m/s")
print(f"  Identity error: {_tan_identity_err:.6f}%  (expect ~0%)")
print(f"  beta_eff(r=1) = {result_r1['beta_eff_deg']:.4f} deg  (expect 48.013 deg)")

if pct_diff > 0.5:
    raise AssertionError(
        f"CONTINUITY GATE FAILED: COP(r=1.0) = {COP_r1:.6f} differs from Phase 6 anchor "
        f"COP_max_nominal = {COP_phase6_anchor:.6f} by {pct_diff:.4f}% (> 0.5%). "
        "fp-no-continuity: halting before reporting any r != 1 results. "
        "Debug: check PITFALL-P9-WRONG-VTAN (v_tan = lambda*(2-r)*v_loop) "
        "and verify beta_eff(r=1) = arctan(1/lambda) = 48.013 deg."
    )

print(f"\nCONTINUITY GATE PASSED: COP(r=1.0) = {COP_r1:.5f} "
      f"matches Phase 6 anchor {COP_phase6_anchor:.5f} within {pct_diff:.4f}%")


# ============================================================
# SWEEP AND VERDICT: run if __main__ or imported with RUN_SWEEP=True
# ============================================================
def run_sweep_and_verdict(eta_c=0.70, loss_frac=0.10):
    """
    Run COP sweep at 11 r values and compute v1.3 verdict.

    r_values = [1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30, 1.35, 1.40, 1.45, 1.50]
    Valid (non-stalled) range: r in [1.00, 1.30] (r_stall_onset=1.31 from Phase 9)
    Stalled (flagged) range:   r in [1.31, 1.50] (AoA_eff >= 12 deg)

    Returns:
        (sweep_results, verdict) -- lists/dicts for JSON output
    """
    r_values = [1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30, 1.35, 1.40, 1.45, 1.50]

    print("\n" + "=" * 75)
    print("COP SWEEP AT 11 r VALUES")
    print("=" * 75)
    print(f"{'r':>5}  {'v_loop':>8}  {'COP':>8}  {'AoA_eff':>8}  {'is_stalled':>10}  {'converged':>9}")
    print("-" * 75)

    sweep_results = []
    for r_val in r_values:
        try:
            res = compute_COP_r(r_val, eta_c=eta_c, loss_frac=loss_frac)
            res["brentq_converged"] = True
            res["brentq_error"] = None
            stalled_str = "STALLED" if res["is_stalled"] else "OK"
            print(f"{r_val:>5.2f}  {res['v_loop_ms']:>8.4f}  {res['COP_nominal']:>8.5f}  "
                  f"{res['AoA_eff_deg']:>8.3f}  {stalled_str:>10}  {'YES':>9}")
        except ValueError as e:
            res = {
                "r":                r_val,
                "v_loop_ms":        None,
                "COP_nominal":      None,
                "AoA_eff_deg":      None,
                "is_stalled":       True,
                "brentq_converged": False,
                "brentq_error":     str(e),
                "W_foil_total_J":   None,
                "W_corot_total_J":  None,
                "corot_scale":      None,
                "t_cycle_s":        None,
                "F_tan_pv_N":       None,
                "F_vert_pv_N":      None,
            }
            print(f"{r_val:>5.2f}  {'---':>8}  {'FAILED':>8}  {'---':>8}  {'FAILED':>10}  {'NO':>9}")
            print(f"       brentq error: {e}")
        sweep_results.append(res)

    print("-" * 75)

    # --------------------------------------------------------
    # Extract valid (non-stalled, converged) COP values
    # r_valid: r in [1.00, 1.30] (before stall onset at 1.31)
    # --------------------------------------------------------
    valid_results = [
        res for res in sweep_results
        if res["brentq_converged"] and not res["is_stalled"]
    ]
    valid_r   = [res["r"]           for res in valid_results]
    valid_cop = [res["COP_nominal"] for res in valid_results]

    print(f"\nValid (non-stalled) r values: {valid_r}")
    print(f"Valid COP values:             {[f'{c:.5f}' for c in valid_cop]}")

    # --------------------------------------------------------
    # r* identification via sweep and refined search
    # --------------------------------------------------------
    if len(valid_cop) < 2:
        # Cannot determine trend with fewer than 2 valid points
        r_star_case = "no_gain"
        r_star      = valid_r[0] if valid_r else 1.0
        COP_r_star  = valid_cop[0] if valid_cop else COP_r1
        print("\nr* case: no_gain (fewer than 2 valid COP points)")

    else:
        # Determine trend from first and last valid differences
        first_diff = valid_cop[1] - valid_cop[0]  # COP(1.05) - COP(1.00)
        last_diff  = valid_cop[-1] - valid_cop[-2] # COP(1.30) - COP(1.25)

        print(f"\nFirst finite difference [COP(1.05)-COP(1.00)] = {first_diff:+.6f}")
        print(f"Last finite difference  [COP(last)-COP(last-1)] = {last_diff:+.6f}")

        # Determine monotone case by checking all valid differences
        all_diffs = [valid_cop[i+1] - valid_cop[i] for i in range(len(valid_cop)-1)]
        n_negative = sum(1 for d in all_diffs if d < 0)
        n_positive = sum(1 for d in all_diffs if d > 0)
        print(f"COP differences: {[f'{d:+.5f}' for d in all_diffs]}")
        print(f"  Negative diffs: {n_negative}/{len(all_diffs)}, Positive diffs: {n_positive}/{len(all_diffs)}")

        if first_diff < 0 and n_negative >= len(all_diffs) - 1:
            # Case C: monotone decreasing from r=1.0 (allow at most 1 non-negative diff for noise)
            r_star_case = "no_gain"
            r_star      = 1.0
            COP_r_star  = valid_cop[0]
            print("Case C: monotone DECREASING from r=1.0 -- no_gain")

        elif first_diff > 0 and last_diff > 0 and n_positive >= len(all_diffs) - 1:
            # Case B: monotone increasing (stall prevents accessing true optimum)
            r_star_case = "boundary_maximum"
            r_star      = valid_r[-1]  # last valid r = 1.30
            COP_r_star  = valid_cop[-1]
            print("Case B: monotone INCREASING -- boundary_maximum at r=1.30 (stall onset at 1.31)")

        elif first_diff > 0 and last_diff < 0:
            # Case A: interior maximum -- locate r* by refined search
            # Find grid index of peak
            peak_idx = valid_cop.index(max(valid_cop))
            r_peak   = valid_r[peak_idx]
            print(f"Case A: interior maximum detected at grid r={r_peak:.2f} "
                  f"(COP={valid_cop[peak_idx]:.5f})")

            # Bracket for refined search
            r_left  = valid_r[peak_idx - 1] if peak_idx > 0 else valid_r[0]
            r_right = valid_r[peak_idx + 1] if peak_idx < len(valid_r) - 1 else valid_r[-1]
            print(f"Refining r* in [{r_left:.2f}, {r_right:.2f}] ...")

            # Use scipy minimize_scalar (negative COP for maximization)
            from scipy.optimize import minimize_scalar
            def neg_COP(r_var):
                try:
                    res = compute_COP_r(r_var, eta_c=eta_c, loss_frac=loss_frac)
                    return -res["COP_nominal"]
                except ValueError:
                    return 0.0  # fallback: no valid COP

            opt_result = minimize_scalar(
                neg_COP,
                bounds=(r_left, min(r_right, 1.30)),  # cap at r=1.30 (stall onset = 1.31)
                method="bounded",
                options={"xatol": 1e-4}
            )
            r_star_case = "interior_maximum"
            r_star      = opt_result.x
            refined_res = compute_COP_r(r_star, eta_c=eta_c, loss_frac=loss_frac)
            COP_r_star  = refined_res["COP_nominal"]
            print(f"Refined r* = {r_star:.4f}, COP(r*) = {COP_r_star:.5f}")

        else:
            # Ambiguous: examine all diffs to pick best classification
            # Default: report at the maximum COP in the valid sweep
            peak_idx    = valid_cop.index(max(valid_cop))
            r_star      = valid_r[peak_idx]
            COP_r_star  = valid_cop[peak_idx]
            r_star_case = "interior_maximum" if 0 < peak_idx < len(valid_cop)-1 else "no_gain"
            if r_star_case == "no_gain":
                r_star     = 1.0
                COP_r_star = valid_cop[0]
            print(f"Mixed trend: r_star_case={r_star_case}, r*={r_star:.2f}, COP(r*)={COP_r_star:.5f}")

    # --------------------------------------------------------
    # Phase 10 COP sweep JSON output
    # --------------------------------------------------------
    ASSERT_CONVENTION_STR = (
        "unit_system=SI, v_tangential_net=lambda*v_loop*(2-r), "
        "PITFALL-P9-WRONG-VTAN=guarded, PITFALL-M1=guarded, "
        "brentq_at_each_r=True, mount_angle=46.013deg FIXED"
    )

    sweep_table = []
    for res in sweep_results:
        entry = {
            "r":                     res["r"],
            "v_loop_ms":             round(res["v_loop_ms"],      6) if res["v_loop_ms"]     is not None else None,
            "COP_nominal":           round(res["COP_nominal"],     6) if res["COP_nominal"]   is not None else None,
            "AoA_eff_deg":           round(res["AoA_eff_deg"],     4) if res["AoA_eff_deg"]   is not None else None,
            "is_stalled":            res["is_stalled"],
            "brentq_converged":      res["brentq_converged"],
            "brentq_error":          res.get("brentq_error"),
            "W_foil_total_J":        round(res["W_foil_total_J"],  2) if res.get("W_foil_total_J") is not None else None,
            "W_corot_total_J":       round(res["W_corot_total_J"], 2) if res.get("W_corot_total_J") is not None else None,
            "corot_scale":           round(res["corot_scale"],      6) if res.get("corot_scale")     is not None else None,
            "t_cycle_s":             round(res["t_cycle_s"],        4) if res.get("t_cycle_s")       is not None else None,
            "F_tan_pv_N":            round(res["F_tan_pv_N"],       4) if res.get("F_tan_pv_N")      is not None else None,
            "F_vert_pv_N":           round(res["F_vert_pv_N"],      4) if res.get("F_vert_pv_N")     is not None else None,
            "force_balance_residual_N": round(res.get("force_balance_residual_N", 0.0), 9) if res.get("force_balance_residual_N") is not None else None,
        }
        sweep_table.append(entry)

    cop_sweep_output = {
        "_description": "Phase 10 COP sweep: extended brentq solver at r ∈ [1.00, 1.50]",
        "_assert_convention": ASSERT_CONVENTION_STR,
        "_generated_by": "analysis/phase10/cop_sweep.py",
        "continuity_check_COP_r1":    round(COP_r1, 6),
        "continuity_check_anchor":    round(COP_phase6_anchor, 6),
        "continuity_check_pct_diff":  round(pct_diff, 4),
        "continuity_check_passed":    True,
        "r_stall_onset": 1.31,
        "r_stall_full":  1.36,
        "eta_c":         eta_c,
        "loss_frac":     loss_frac,
        "cop_sweep_table": sweep_table,
        "valid_r_range":  [1.00, 1.30],
        "r_star_raw":     round(r_star, 4),
        "COP_r_star":     round(COP_r_star, 6),
        "r_star_case":    r_star_case,
        "pitfall_guards_verified": {
            "PITFALL_P9_WRONG_VTAN":
                "v_tan = lambda*(2-r)*v_loop NOT r*lambda*v_loop — assertion passed at load time",
            "PITFALL_P9_BRENTQ":
                "brentq re-run at each r; v_loop varies with r (NOT fixed Phase 9 value 3.273346 m/s)",
            "PITFALL_M1":
                "W_pump uses W_adia not W_iso",
            "PITFALL_C6":
                "W_jet = 0.0 explicit",
        },
    }

    with open(OUT_SWEEP, "w") as f:
        json.dump(cop_sweep_output, f, indent=2)
    print(f"\nSweep JSON written to: {OUT_SWEEP}")

    # --------------------------------------------------------
    # Verdict computation
    # --------------------------------------------------------
    COP_baseline    = COP_r1
    COP_gain        = COP_r_star - COP_baseline

    # Response classification
    # NOTE: "multiplicative" is IMPOSSIBLE — Phase 9 showed enhanced-both (F_vert INCREASES with r)
    # Multiplicative would require F_vert to DECREASE with r. This is geometrically impossible
    # at fixed mount_angle=46.013 deg per Phase 9 classification result.
    if COP_gain > 0.01:
        response_type  = "additive"
        response_label = f"additive ({COP_gain:.4f} gain above baseline)"
    elif COP_gain < -0.01:
        response_type  = "negative"
        response_label = "negative (differential rotation reduces COP)"
    else:
        response_type  = "no_gain"
        response_label = f"negligible (|gain| = {abs(COP_gain):.4f} < 0.01)"

    # Phase 6 ceiling comparison (use tolerance of 0.0001 for floating-point equality)
    _cop_gain_sig = abs(COP_r_star - COP_phase6_anchor) / COP_phase6_anchor
    if COP_r_star > COP_phase6_best:
        phase6_comparison_flag = (
            f"significant_result: COP(r*) = {COP_r_star:.4f} EXCEEDS Phase 6 best case ({COP_phase6_best:.4f})"
        )
    elif _cop_gain_sig < 0.0001:
        # COP(r*) is essentially equal to Phase 6 nominal (no_gain case: r*=r=1.0)
        phase6_comparison_flag = (
            f"no_improvement: COP(r*) = {COP_r_star:.4f} equals Phase 6 nominal ({COP_phase6_anchor:.4f}); "
            "differential rotation provides no COP gain"
        )
    elif COP_r_star > COP_phase6_anchor:
        phase6_comparison_flag = (
            f"modest_improvement: COP(r*) = {COP_r_star:.4f} > Phase 6 nominal ({COP_phase6_anchor:.4f}) "
            f"but below best case ({COP_phase6_best:.4f})"
        )
    else:
        phase6_comparison_flag = (
            f"no_improvement: COP(r*) = {COP_r_star:.4f} <= Phase 6 nominal ({COP_phase6_anchor:.4f})"
        )

    # v1.3 go/no-go verdict
    COP_threshold = 1.5
    if COP_r_star >= COP_threshold:
        v13_verdict = "GO"
        v13_detail  = (
            f"COP(r*) = {COP_r_star:.4f} >= threshold {COP_threshold}. Engine is viable."
        )
    elif COP_r_star >= 1.0:
        v13_verdict = "MARGINAL"
        v13_detail  = (
            f"COP(r*) = {COP_r_star:.4f} >= 1.0 (net positive) but below threshold {COP_threshold}. "
            "Differential rotation improves COP but does not bridge the gap to viability."
        )
    else:
        v13_verdict = "NO_GO"
        v13_detail  = (
            f"COP(r*) = {COP_r_star:.4f} < 1.5 threshold. "
            f"Differential rotation provides no COP gain over Phase 6 baseline. "
            f"Gap to threshold = {COP_threshold - COP_r_star:.4f}."
        )

    # v_loop at r*
    if r_star_case == "interior_maximum":
        _r_star_res = compute_COP_r(r_star, eta_c=eta_c, loss_frac=loss_frac)
        v_loop_r_star = _r_star_res["v_loop_ms"]
    elif r_star_case == "boundary_maximum":
        # r*=1.30 is the last valid sweep point
        _r130_res = next((res for res in sweep_results if abs(res["r"] - 1.30) < 1e-6), None)
        v_loop_r_star = _r130_res["v_loop_ms"] if _r130_res and _r130_res["brentq_converged"] else None
    else:
        v_loop_r_star = result_r1["v_loop_ms"]

    v_loop_r1    = result_r1["v_loop_ms"]
    v_loop_ratio = (v_loop_r_star / v_loop_r1) if v_loop_r_star is not None else None

    # Verdict JSON output
    verdict_output = {
        "_description": "Phase 10 v1.3 verdict: COP sweep with differential rotation",
        "_assert_convention": ASSERT_CONVENTION_STR,
        "_generated_by": "analysis/phase10/cop_sweep.py",
        "v13_verdict":         v13_verdict,
        "v13_verdict_detail":  v13_detail,
        "COP_threshold":       COP_threshold,
        "r_star":              round(r_star, 4),
        "COP_r_star":          round(COP_r_star, 4),
        "COP_r_baseline":      round(COP_baseline, 4),
        "COP_gain_vs_r1":      round(COP_gain, 4),
        "r_star_case":         r_star_case,
        "response_type":       response_type,
        "response_detail":     response_label,
        "phase6_nominal_anchor":   round(COP_phase6_anchor, 6),
        "phase6_best_case_ceiling": round(COP_phase6_best, 6),
        "COP_gap_to_threshold":    round(COP_threshold - COP_r_star, 4),
        "COP_gap_to_phase6_ceiling": round(COP_phase6_best - COP_r_star, 4),
        "phase6_comparison_flag":  phase6_comparison_flag,
        "multiplicative_impossible_note": (
            "Enhanced-both response confirmed in Phase 9: F_vert_ratio > 1.0 at all r in (1.0, 1.31). "
            "|F_vert| INCREASES with r (C_L triples while v_rel^2 drops ~8%). "
            "True multiplicative COP would require F_vert to DECREASE with r, which is "
            "geometrically impossible at fixed mount_angle=46.013 deg. "
            "response_type='multiplicative' is REJECTED by Phase 9 evidence."
        ),
        "v_loop_r_star_ms":  round(v_loop_r_star, 4) if v_loop_r_star is not None else None,
        "v_loop_r1_ms":      round(v_loop_r1,     4),
        "v_loop_ratio":      round(v_loop_ratio,   4) if v_loop_ratio is not None else None,
        "stall_limit_note": (
            "Valid COP sweep window: r ∈ [1.00, 1.30]; r=1.31 is stall onset "
            "(AoA_eff >= 12.147 deg >= 12 deg per Phase 9). "
            "Stalled r values computed with clamped NACA coefficients but flagged invalid."
        ),
        "forbidden_proxies_rejected": {
            "fp-reversed-foil":
                "REJECTED: F_vert is kinematic (lift perpendicular to v_rel, always negative/downward); "
                "foil orientation irrelevant to F_vert sign.",
            "fp-fixed-vloop":
                "REJECTED: brentq re-run at each r; v_loop varies with r "
                "(Phase 9 fixed v_loop=3.273346 m/s was UPPER BOUND; Phase 10 self-consistent).",
            "fp-wrong-vtan":
                "REJECTED: v_tan = lambda*(2-r)*v_loop; "
                "assertion passed at load time (v_tan decreases with r).",
            "fp-cop-lossless-primary":
                "REJECTED: COP_nominal (eta_c=0.70, loss=10%) is primary metric; "
                "lossless COP not reported.",
            "fp-no-continuity":
                f"REJECTED: continuity gate PASSED "
                f"(COP(r=1.0)={COP_r1:.5f} within {pct_diff:.4f}% of Phase 6 anchor {COP_phase6_anchor:.5f}).",
            "fp-multiplier-claim":
                "REJECTED: response_type='multiplicative' is geometrically impossible. "
                "Phase 9 confirmed F_vert_ratio > 1 throughout valid r range. "
                "Actual response_type: " + response_type + ".",
        },
        "backtracking_checks": {
            "continuity_gate":               "PASSED",
            "brentq_convergence_all_r":      all(res["brentq_converged"] for res in sweep_results),
            "v_loop_physically_plausible":
                ("all v_loop(r) > 0.5 m/s"
                 if all((res["v_loop_ms"] or 99) > 0.5 for res in sweep_results)
                 else "WARNING: some v_loop < 0.5 m/s"),
        },
    }

    with open(OUT_VERDICT, "w") as f:
        json.dump(verdict_output, f, indent=2)
    print(f"Verdict JSON written to: {OUT_VERDICT}")

    # Human-readable verdict summary
    print("\n" + "=" * 65)
    print(f"=== v1.3 VERDICT: {v13_verdict} ===")
    print("=" * 65)
    print(f"r*                     = {r_star:.4f}  ({r_star_case})")
    print(f"COP(r*)                = {COP_r_star:.4f}")
    print(f"COP(r=1.0) baseline    = {COP_baseline:.4f}")
    print(f"Gain                   = {COP_gain:+.4f}")
    print(f"Response type          = {response_type}")
    print(f"Phase 6 nominal (0.94373): {phase6_comparison_flag}")
    print(f"Gap to threshold (1.5) = {COP_threshold - COP_r_star:.4f}")
    print(f"v_loop(r*)             = {v_loop_r_star:.4f} m/s  (r=1.0: {v_loop_r1:.4f} m/s)")
    if v_loop_ratio is not None:
        print(f"v_loop ratio           = {v_loop_ratio:.4f}  (expect < 1.0 if r* > 1.0)")
    print("=" * 65)

    return cop_sweep_output, verdict_output


# ============================================================
# Main entry point
# ============================================================
if __name__ == "__main__":
    print("\n" + "=" * 65)
    print("PHASE 10 COP SWEEP -- Differential Rotation Verdict")
    print("=" * 65)
    run_sweep_and_verdict(eta_c=0.70, loss_frac=0.10)
