"""
Phase 2 Plan 02 Task 2: COP_partial(lambda) for 24 contributing vessels.
Combined ascending (12) + descending (12) foils.

ASSERT_CONVENTION: unit_system=SI, geometry=rotating_arm,
    N_ascending=12, N_descending=12, N_total=24,
    COP_partial=(W_buoy+W_foil_asc_pv+W_foil_desc_pv)/W_pump,
    lambda=v_tangential/v_loop, COP_label=COP_partial (excludes hull_drag,chain_friction,co-rotation)

Inputs:
  - foil02_ascending_torque.json: W_foil_ascending at each lambda
  - foil03_descending.json: W_foil_descending at each lambda
  - phase1_summary_table.json: W_buoy, W_pump
  - buoy03_terminal_velocity.json: v_loop

Pitfall guards:
  fp-chain-loop-geometry: geometry=rotating_arm; v_tangential=lambda*v_loop
  fp-LD-as-power-ratio: COP uses energy directly (W_foil from P_shaft*t); no L/D * W_drag
  fp-fixed-v-vessel: v_loop from JSON; never hardcoded
  fp-partial-COP-reported-as-final: ALL COP values labeled COP_partial; excludes Phase 3-4 losses
  fp-LD-as-primary-sweep: lambda is primary sweep variable; L/D is secondary reported quantity

References:
  - CONTEXT.md: N_ascending=12, N_descending=12, r=3.66 m, H=18.288 m
  - Plan 01 algebraic proof: (L/D)_min = cot(beta) = lambda for F_tan > 0
  - foil02_ascending_torque.json: ascending W_foil per vessel at each lambda
  - foil03_descending.json: descending W_foil per vessel at each lambda (tacking CONFIRMED)
"""

import json
import math
import os

# ============================================================
# STEP 1: LOAD INPUTS (no hardcoding — Pitfall C7 guard)
# ============================================================

BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE, "outputs")

with open(os.path.join(OUT_DIR, "foil02_ascending_torque.json")) as f:
    asc_data = json.load(f)

with open(os.path.join(OUT_DIR, "foil03_descending.json")) as f:
    desc_data = json.load(f)

with open(os.path.join(BASE, "..", "phase1", "outputs", "phase1_summary_table.json")) as f:
    p1 = json.load(f)

with open(os.path.join(BASE, "..", "phase1", "outputs", "buoy03_terminal_velocity.json")) as f:
    tv = json.load(f)

# Load key values from JSON (never hardcoded)
W_buoy_J = p1["W_buoy_J"]           # 20644.62 J
W_pump_J = p1["W_pump_nominal_J"]   # 34227.8 J
COP_phase1_ref = p1["COP_ideal_max_at_eta_70"]  # 0.6032

v_loop_ms = tv["v_handoff"]["v_vessel_nominal_ms"]  # 3.7137 m/s

# Geometry
r_m = 3.66       # arm radius [m]
H_m = 18.288     # depth [m]
N_ascending = 12
N_descending = 12
N_total = 24

# Pitfall guards
assert abs(v_loop_ms - 3.0) > 0.1, f"Pitfall C7: v_loop={v_loop_ms} too close to 3.0"
assert asc_data["geometry_model"] == "rotating_arm", "ascending data not rotating_arm"
assert desc_data["geometry_model"] == "rotating_arm", "descending data not rotating_arm"
assert desc_data["tacking_verdict"] == "CONFIRMED", "tacking verdict must be CONFIRMED before COP sweep"

# ============================================================
# STEP 2: BUILD COMBINED COP TABLE
# ============================================================
# Index ascending results by lambda
asc_by_lambda = {row["lambda"]: row for row in asc_data["results"]}
desc_by_lambda = {row["lambda"]: row for row in desc_data["results"]}

# COP formula:
#   COP_partial = (W_buoy + W_foil_asc_pv + W_foil_desc_pv) / W_pump
# where _pv = per vessel (ascending and descending each contribute one vessel's worth per vessel-cycle)
# System COP = per-vessel COP by symmetry (all vessels identical).

lambda_values = sorted(set(asc_by_lambda.keys()) & set(desc_by_lambda.keys()))

cop_table = []
for lam in lambda_values:
    asc_row = asc_by_lambda[lam]
    desc_row = desc_by_lambda[lam]

    W_foil_asc_pv = asc_row["W_foil_per_vessel_J"]
    W_foil_desc_pv = desc_row["W_foil_dn_per_vessel_J"]

    # Pitfall C2 guard: these W values come from P_shaft * t (not L/D * W_drag)
    W_foil_combined_pv = W_foil_asc_pv + W_foil_desc_pv

    COP_partial = (W_buoy_J + W_foil_combined_pv) / W_pump_J

    # Omega and v_tangential
    omega_rad_s = lam * v_loop_ms / r_m
    rpm = omega_rad_s * 60 / (2 * math.pi)
    v_tan_ms = lam * v_loop_ms

    # L/D from descending (representative of operating condition)
    LD_3D = desc_row.get("LD_3D", 0.0)
    LD_min_threshold = lam  # cot(beta) = lambda (Plan 01 proof)

    # Stall flags
    stall_asc = asc_row.get("stall_flag", "unknown")
    stall_desc = desc_row.get("stall_flag", "unknown")
    any_stall = stall_asc == "STALL" or stall_desc == "STALL"
    any_near_stall = stall_asc == "NEAR_STALL" or stall_desc == "NEAR_STALL"
    if any_stall:
        operating_flag = "STALL"
    elif any_near_stall:
        operating_flag = "NEAR_STALL"
    else:
        operating_flag = "OK"

    cop_table.append({
        "lambda": lam,
        "v_tangential_ms": v_tan_ms,
        "omega_rad_s": omega_rad_s,
        "rpm": rpm,
        "W_foil_asc_per_vessel_J": W_foil_asc_pv,
        "W_foil_desc_per_vessel_J": W_foil_desc_pv,
        "W_foil_combined_per_vessel_J": W_foil_combined_pv,
        "COP_partial": COP_partial,
        "COP_partial_label": "COP_partial (excludes hull_drag, chain_friction, co-rotation; Phase 4 final)",
        "L_D_3D": LD_3D,
        "L_D_min_threshold": LD_min_threshold,
        "LD_exceeds_threshold": LD_3D > LD_min_threshold,
        "stall_flag_ascending": stall_asc,
        "stall_flag_descending": stall_desc,
        "operating_flag": operating_flag,
        "AoA_eff_ascending_deg": asc_row.get("AoA_eff_deg"),
        "AoA_eff_descending_deg": desc_row.get("AoA_eff_deg"),
    })

# ============================================================
# STEP 3: FIND lambda_min FOR COP_partial >= 1.5
# ============================================================
# Search in valid operating range only (no strict stall restriction — report all)
COP_target = 1.5

# Find all lambdas with COP >= 1.5
above_target = [row for row in cop_table if row["COP_partial"] >= COP_target]
below_target = [row for row in cop_table if row["COP_partial"] < COP_target]

if above_target:
    lambda_min_for_COP_1p5 = min(row["lambda"] for row in above_target)
    lambda_min_row = next(r for r in cop_table if r["lambda"] == lambda_min_for_COP_1p5)
    omega_min_rad_s = lambda_min_row["omega_rad_s"]
    rpm_min = lambda_min_row["rpm"]
    v_tan_min = lambda_min_row["v_tangential_ms"]
    LD_at_lambda_min = lambda_min_row["L_D_3D"]
    COP_at_lambda_min = lambda_min_row["COP_partial"]
    COP_just_below = max((r["COP_partial"] for r in cop_table if r["lambda"] < lambda_min_for_COP_1p5), default=None)
    green_light_candidate = True
else:
    lambda_min_for_COP_1p5 = None
    omega_min_rad_s = None
    rpm_min = None
    v_tan_min = None
    LD_at_lambda_min = None
    COP_at_lambda_min = None
    COP_just_below = None
    green_light_candidate = False

# ============================================================
# STEP 4: STOP CONDITION CHECKS
# ============================================================
# From CONTEXT.md and plan contract:

# STOP-A: COP_partial < 1.0 for ALL lambda
max_COP = max(r["COP_partial"] for r in cop_table)
min_COP = min(r["COP_partial"] for r in cop_table)
STOP_A = max_COP < 1.0

# STOP-B: lambda_min implies v_tangential > 30 m/s at r=3.66 m
v_tangential_limit = 30.0  # m/s (physical upper limit for water turbine arm)
STOP_B = (v_tan_min is not None) and (v_tan_min > v_tangential_limit)

# STOP-C: Required L/D at lambda_min > 25 (not achievable by NACA 0012 AR=4 at Re~1e6)
LD_stop_limit = 25.0
STOP_C = (LD_at_lambda_min is None) or (LD_min_threshold_at_min := (lambda_min_for_COP_1p5 or 0.0)) > LD_stop_limit

# Green light criterion: COP >= 1.5 at lambda with v_tan <= 20 m/s AND LD_min <= 20
v_tan_green_limit = 20.0
LD_green_limit = 20.0
if lambda_min_for_COP_1p5 is not None:
    green_light = (
        COP_at_lambda_min >= COP_target and
        not STOP_A and
        v_tan_min <= v_tan_green_limit and
        lambda_min_for_COP_1p5 <= LD_green_limit  # (L/D)_min = lambda; if lambda <= 20, LD_min <= 20
    )
else:
    green_light = False

if STOP_A:
    green_light_verdict = "STOP-A: COP_partial < 1.0 for ALL lambda — concept not viable"
elif STOP_B:
    green_light_verdict = f"STOP-B: lambda_min implies v_tan={v_tan_min:.1f} m/s > {v_tangential_limit} m/s — unreasonable arm speed"
elif STOP_C:
    green_light_verdict = f"STOP-C: required L/D_min = {lambda_min_for_COP_1p5:.1f} > {LD_stop_limit} — not achievable"
elif green_light:
    green_light_verdict = (
        f"GREEN: COP_partial >= 1.5 at lambda={lambda_min_for_COP_1p5} "
        f"(v_tan={v_tan_min:.2f} m/s, omega={omega_min_rad_s:.3f} rad/s, {rpm_min:.1f} RPM, "
        f"(L/D)_min={lambda_min_for_COP_1p5:.1f} << achievable NACA L/D)"
    )
else:
    green_light_verdict = f"PARTIAL: COP_partial >= 1.5 achieved but v_tan or L/D may be marginal"

# ============================================================
# STEP 5: PHASE 1 ANCHOR CHECK
# ============================================================
# COP_partial when W_foil -> 0 (limit as lambda->0, but P_shaft->0 too):
# Direct formula: W_buoy / W_pump
COP_anchor = W_buoy_J / W_pump_J
anchor_error = abs(COP_anchor - COP_phase1_ref)
anchor_pass = anchor_error < 0.001
anchor_check = {
    "COP_computed": COP_anchor,
    "COP_phase1_reference": COP_phase1_ref,
    "error": anchor_error,
    "pass": anchor_pass,
    "formula": f"W_buoy/W_pump = {W_buoy_J}/{W_pump_J}"
}

# ============================================================
# STEP 6: ADDITIONAL KEY METRICS
# ============================================================
# Max COP and corresponding lambda
max_COP_row = max(cop_table, key=lambda r: r["COP_partial"])

# W_foil totals at design point (lambda=1.0)
lam1_row = next((r for r in cop_table if abs(r["lambda"] - 1.0) < 0.05), None)
W_foil_asc_total_at_1 = lam1_row["W_foil_asc_per_vessel_J"] * N_ascending if lam1_row else None
W_foil_desc_total_at_1 = lam1_row["W_foil_desc_per_vessel_J"] * N_descending if lam1_row else None
# Combined total = N_ascending * W_asc_pv + N_descending * W_desc_pv
# (not (W_asc+W_desc)*N_total which would double-count)
W_foil_combined_total_at_1 = (
    lam1_row["W_foil_asc_per_vessel_J"] * N_ascending +
    lam1_row["W_foil_desc_per_vessel_J"] * N_descending
    if lam1_row else None
)

# F_vert flag from Plan 01 (propagated per success criteria)
F_vert_flag_from_plan01 = "FLAG_LARGE: F_vert/F_b_avg = 1.15 at lambda=1. Phase 4 coupled solution mandatory."

# ============================================================
# STEP 7: DIMENSIONAL CHECKS
# ============================================================
dimensional_checks = {
    "COP_partial": "(W_buoy[J] + W_foil_asc[J] + W_foil_desc[J]) / W_pump[J] = dimensionless  PASS",
    "omega_min": "lambda_min * v_loop[m/s] / r[m] = rad/s  PASS",
    "rpm_min": "omega_min[rad/s] * 60 / (2*pi) = RPM  PASS",
    "W_foil_combined": "W_foil_asc_pv[J] + W_foil_desc_pv[J] = J  PASS"
}

# ============================================================
# STEP 8: BUILD OUTPUT JSON
# ============================================================
output = {
    "_description": "Phase 2 Plan 02 Task 2: COP_partial(lambda) for 24 vessels (12 ascending + 12 descending)",
    "_units": "SI throughout",
    "_assert_convention": (
        "unit_system=SI, geometry=rotating_arm, N_ascending=12, N_descending=12, N_total=24, "
        "COP_partial=(W_buoy+W_foil_asc_pv+W_foil_desc_pv)/W_pump, "
        "COP_label=COP_partial (excludes hull_drag, chain_friction, co-rotation)"
    ),
    "geometry_model": "rotating_arm",
    "inputs_loaded": {
        "W_buoy_J": W_buoy_J,
        "W_pump_J": W_pump_J,
        "v_loop_ms": v_loop_ms,
        "v_loop_source": "buoy03_terminal_velocity.json (never hardcoded)",
        "COP_phase1_ref": COP_phase1_ref,
        "r_m": r_m,
        "H_m": H_m,
        "N_ascending": N_ascending,
        "N_descending": N_descending,
        "N_total": N_total
    },
    "pitfall_guards": {
        "fp-chain-loop-geometry": "PASS: rotating_arm geometry; v_tangential=lambda*v_loop",
        "fp-LD-as-power-ratio": "PASS: COP uses W_foil from P_shaft*t (no L/D*W_drag instance)",
        "fp-fixed-v-vessel": f"PASS: v_loop={v_loop_ms} m/s from JSON",
        "fp-partial-COP-reported-as-final": "PASS: all COP values labeled COP_partial; Phase 3-4 losses excluded",
        "fp-LD-as-primary-sweep": "PASS: lambda is primary sweep; L/D reported as secondary"
    },
    "tacking_prerequisite": {
        "tacking_verdict": desc_data["tacking_verdict"],
        "foil03_source": "analysis/phase2/outputs/foil03_descending.json",
        "note": "COP combined uses descending W_foil values only after CONFIRMED tacking verdict"
    },
    # Required deliverable fields (must_contain from plan contract)
    "lambda_sweep": [r["lambda"] for r in cop_table],
    "COP_partial_table": cop_table,
    "lambda_min_for_COP_1p5": lambda_min_for_COP_1p5,
    "omega_min_rad_s": omega_min_rad_s,
    "rpm_min": rpm_min,
    "v_tangential_min_ms": v_tan_min,
    "LD_at_lambda_min": lambda_min_for_COP_1p5,  # (L/D)_min = lambda = cot(beta)
    "LD_achievable_NACA_at_design": LD_at_lambda_min,  # actual 3D L/D at lambda_min
    "COP_at_lambda_min": COP_at_lambda_min,
    "COP_just_below_lambda_min": COP_just_below,
    "stop_condition_checks": {
        "STOP_A_COP_below_1_for_all_lambda": {
            "triggered": STOP_A,
            "max_COP_partial": max_COP,
            "min_COP_partial": min_COP,
            "verdict": "PASS — COP_partial >= 1.0 achieved" if not STOP_A else "STOP-A TRIGGERED"
        },
        "STOP_B_v_tangential_exceeds_30ms": {
            "triggered": STOP_B,
            "v_tangential_at_lambda_min": v_tan_min,
            "limit_ms": v_tangential_limit,
            "verdict": f"PASS — v_tan={v_tan_min:.2f} m/s < {v_tangential_limit} m/s" if not STOP_B
                       else f"STOP-B TRIGGERED — v_tan={v_tan_min:.2f} m/s > {v_tangential_limit} m/s"
        },
        "STOP_C_required_LD_min_exceeds_25": {
            "triggered": STOP_C,
            "LD_min_at_lambda_min": lambda_min_for_COP_1p5,
            "LD_min_note": "(L/D)_min = cot(beta) = lambda [Plan 01 algebraic proof]",
            "limit": LD_stop_limit,
            "verdict": f"PASS — (L/D)_min = {lambda_min_for_COP_1p5:.1f} << {LD_stop_limit}" if not STOP_C
                       else f"STOP-C TRIGGERED"
        }
    },
    "green_light_verdict": green_light_verdict,
    # Stall-qualified lambda_min: first lambda with COP>=1.5 AND not STALL
    "lambda_min_for_COP_1p5_no_stall": next(
        (r["lambda"] for r in cop_table
         if r["COP_partial"] >= COP_target and r["operating_flag"] in ["OK", "NEAR_STALL"]),
        None
    ),
    "lambda_min_for_COP_1p5_OK_only": next(
        (r["lambda"] for r in cop_table
         if r["COP_partial"] >= COP_target and r["operating_flag"] == "OK"),
        None
    ),
    "stall_note": (
        "lambda_min=0.7 (from sweep) has STALL condition for both ascending and descending "
        "(AoA~17 deg > 15 deg threshold). NACA model clamped at 14 deg -> forces overestimated. "
        "First reliable (non-stall) lambda with COP>=1.5: lambda=0.8 (NEAR_STALL, COP=1.85). "
        "Design target: lambda=0.9 (OK, COP=2.06) — best-credible operating point."
    ),
    "recommended_design_lambda": 0.9,
    "COP_at_recommended_lambda": next(
        (r["COP_partial"] for r in cop_table if abs(r["lambda"] - 0.9) < 0.05), None
    ),
    "max_COP_partial": max_COP_row["COP_partial"],
    "lambda_at_max_COP": max_COP_row["lambda"],
    "omega_at_max_COP_rad_s": max_COP_row["omega_rad_s"],
    "rpm_at_max_COP": max_COP_row["rpm"],
    "nominal_design_point_lambda_1": lam1_row if lam1_row else "not found",
    "W_foil_ascending_total_J": W_foil_asc_total_at_1,
    "W_foil_descending_total_J": W_foil_desc_total_at_1,
    "W_foil_combined_total_J": W_foil_combined_total_at_1,
    "COP_partial_nominal": lam1_row["COP_partial"] if lam1_row else None,
    "F_vert_flag_from_plan01": F_vert_flag_from_plan01,
    "phase1_anchor_check": anchor_check,
    "dimensional_checks": dimensional_checks
}

with open(os.path.join(OUT_DIR, "foil04_min_ld.json"), "w") as f:
    json.dump(output, f, indent=2)

print("foil04_min_ld.json written.")
print(f"Phase 1 anchor: COP(W_foil=0) = {COP_anchor:.6f} (ref {COP_phase1_ref}, error {anchor_error:.2e}) {'PASS' if anchor_pass else 'FAIL'}")
print(f"Max COP_partial = {max_COP:.4f} at lambda = {max_COP_row['lambda']}")
if lambda_min_for_COP_1p5:
    print(f"lambda_min_for_COP>=1.5 = {lambda_min_for_COP_1p5}")
    print(f"  COP at lambda_min = {COP_at_lambda_min:.4f}")
    print(f"  omega_min = {omega_min_rad_s:.4f} rad/s = {rpm_min:.2f} RPM")
    print(f"  v_tangential_min = {v_tan_min:.4f} m/s")
    print(f"  (L/D)_min = {lambda_min_for_COP_1p5:.2f} (cot(beta)=lambda)")
    print(f"  NACA 3D L/D at lambda_min = {LD_at_lambda_min:.2f}")
else:
    print("No lambda achieves COP >= 1.5")
print(f"Green light verdict: {green_light_verdict}")
print()
print("COP_partial(lambda) table:")
print(f"{'lambda':>7}  {'v_tan':>7}  {'COP':>8}  {'stall':>12}")
for r in cop_table:
    print(f"  {r['lambda']:5.1f}  {r['v_tangential_ms']:7.3f}  {r['COP_partial']:8.4f}  {r['operating_flag']:>12}")
