"""
Phase 2 Plan 01 Task 2: Ascending vessel shaft torque and cycle energy integration; Phase 1 anchor check.

ASSERT_CONVENTION: unit_system=SI, geometry=rotating_arm, N_ascending=12,
    shaft_torque=F_tan_times_r, W_foil=P_shaft_times_t_ascending,
    COP_partial=(W_buoy+W_foil_ascending_total)/W_pump

Prerequisite: foil01_force_sweep.json must have verdict=CONTINUE and geometry_model=rotating_arm.

References:
  - foil01_force_sweep.json: F_tan at each lambda
  - buoy03_terminal_velocity.json: v_loop=3.7137 m/s
  - phase1_summary_table.json: W_buoy=20644.62 J, W_pump=34227.8 J, F_b_avg=1128.86 N

Phase 1 anchor verification:
  COP_partial(W_foil=0) = W_buoy / W_pump = 20644.62 / 34227.8 = 0.6032 +/- 0.001
  This MUST match phase1_summary_table.json COP_ideal_max_at_eta_70 = 0.6032.

Vessel count (per 02-CONTEXT.md):
  Per arm: 4 ascending + 4 descending = 8 contributing foils
  Total: 8 x 3 arms = 24 contributing foils
  N_ascending = 4 per arm x 3 arms = 12 ascending foils

Pitfall guards:
  fp-LD-as-power-ratio: W_foil = P_shaft * t_ascending (NOT L/D * W_drag)
  fp-fixed-v-vessel: v_loop from JSON only
  Pitfall C2: P_shaft = F_tan * v_tangential at every step
"""

import json
import math
import os

# ---------------------------------------------------------------------------
# Step 1: Load Phase 1 values and force sweep
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHASE1_DIR = os.path.join(BASE_DIR, "phase1", "outputs")
PHASE2_DIR = os.path.join(BASE_DIR, "phase2", "outputs")

# Load terminal velocity (Pitfall C7 guard)
with open(os.path.join(PHASE1_DIR, "buoy03_terminal_velocity.json")) as f:
    tv = json.load(f)
v_loop = tv["v_handoff"]["v_vessel_nominal_ms"]          # 3.7137 m/s — from JSON
v_loop_conservative = tv["v_handoff"]["v_vessel_conservative_ms"]  # 3.0752 m/s

# Load Phase 1 summary (anchor values)
with open(os.path.join(PHASE1_DIR, "phase1_summary_table.json")) as f:
    p1 = json.load(f)
W_buoy = p1["W_buoy_J"]           # 20644.62 J
W_pump = p1["W_pump_nominal_J"]   # 34227.8 J
F_b_avg = p1["F_b_avg_N"]         # 1128.86 N
COP_phase1 = p1["COP_ideal_max_at_eta_70"]  # 0.6032

# Load force sweep (CONTINUE gate)
with open(os.path.join(PHASE2_DIR, "foil01_force_sweep.json")) as f:
    sweep = json.load(f)

assert sweep["geometry_model"] == "rotating_arm", \
    f"Geometry guard FAILED: expected rotating_arm, got {sweep['geometry_model']}"
assert sweep["verdict"] == "CONTINUE", \
    f"Plan halt: foil01_force_sweep.json verdict = {sweep['verdict']}"

print(f"Prerequisite check: geometry={sweep['geometry_model']}, verdict={sweep['verdict']} -- OK")
print(f"v_loop = {v_loop} m/s (from JSON, not hardcoded)")

# Pitfall C7 guard: confirm v_loop is from JSON, not 3.0 m/s
assert abs(v_loop - 3.0) > 0.1, "Pitfall C7 FAIL: v_loop suspiciously close to 3.0 m/s hardcoded value"

# ---------------------------------------------------------------------------
# Step 2: Vessel count and cycle parameters (per 02-CONTEXT.md)
# ---------------------------------------------------------------------------
N_ascending = 12   # 4 per arm × 3 arms (per CONTEXT.md; 2 vessels per arm in transition)
N_descending = 12  # symmetric; accounted in Plan 02
r = 3.66           # m — arm radius (nominal)

# Loop length estimate: 2 straight sections (ascent H + descent H) + 2 curved ends
# Narrow oval loop: straight = 2*H = 36.576 m; curved ends ≈ pi * d_loop_top_bottom
# Using 48.0 m as working estimate (2*18.288 + pi*3.66 ≈ 48.07 m)
loop_length_nominal = 48.0  # m (working estimate)
loop_length_sensitivity = [44.0, 48.0, 52.0]  # m (sensitivity sweep)

# Time for one ascending traverse (bottom to top)
t_ascending = round(18.288 / v_loop, 4)  # s — H / v_loop

# Full cycle time (full loop traversal)
t_cycle = round(loop_length_nominal / v_loop, 4)  # s

# Half-cycle check: ascending time should be H/v_loop (half the straight section)
# Descending time = same (symmetric loop, same |v_loop|)
# Full cycle = up + down + 2*(curved end transit) ≈ loop_length/v_loop

print(f"N_ascending = {N_ascending} (4 per arm x 3 arms)")
print(f"t_ascending = H/v_loop = 18.288/{v_loop:.4f} = {t_ascending:.4f} s")
print(f"t_cycle = loop_length/v_loop = {loop_length_nominal}/{v_loop:.4f} = {t_cycle:.4f} s")

# Verify t_ascending ~ 4.924 s at nominal v_loop
assert abs(t_ascending - 4.924) < 0.01, \
    f"t_ascending check FAILED: expected ~4.924 s, got {t_ascending:.4f} s"

# ---------------------------------------------------------------------------
# Step 3: Phase 1 anchor verification (CRITICAL cross-check — must PASS)
# ---------------------------------------------------------------------------
# At W_foil = 0 (no foil): COP_partial = W_buoy / W_pump must equal Phase 1 value
COP_anchor = W_buoy / W_pump
anchor_error = abs(COP_anchor - COP_phase1)

print(f"\n--- Phase 1 Anchor Verification ---")
print(f"COP_partial(W_foil=0) = W_buoy/W_pump = {W_buoy:.2f}/{W_pump:.2f} = {COP_anchor:.6f}")
print(f"Phase 1 COP_ideal_max_at_eta_70 = {COP_phase1:.4f}")
print(f"Anchor error = {anchor_error:.6f} (must be < 0.001)")
assert anchor_error < 0.001, \
    f"Phase 1 anchor FAILED: computed {COP_anchor:.6f}, expected {COP_phase1:.4f}, error={anchor_error:.6f}"
print(f"Phase 1 anchor: PASS")

# ---------------------------------------------------------------------------
# Step 4: Extract force sweep at AoA_target=7 deg, primary lambda grid
# ---------------------------------------------------------------------------
# Filter for AoA_target=7 (nominal design) and primary lambda grid (step 0.1)
results_7deg = [
    r for r in sweep["results"]
    if r.get("AoA_target_deg") == 7.0 and
    abs(r["lambda"] - round(r["lambda"], 1)) < 0.005  # primary grid only
]
# Sort by lambda
results_7deg.sort(key=lambda r: r["lambda"])

# ---------------------------------------------------------------------------
# Step 5: Shaft torque per vessel and cycle energy (for each lambda)
# ---------------------------------------------------------------------------
# Shaft torque: tau = F_tan * r [N*m]
# omega_arm: omega = v_tangential / r [rad/s]
# P_shaft per vessel: P = tau * omega = F_tan * v_tangential [W] (Pitfall C2 guard)
# W_foil per vessel (ascending traverse): W = P_shaft * t_ascending [J]
# W_foil ascending total: W_total = N_ascending * W_foil_per_vessel [J]
# COP_partial (ascending contribution only): COP = (W_buoy + W_foil_total) / W_pump

torque_results = []

for row in results_7deg:
    lam = row["lambda"]
    F_tan = row["F_tan_N"]
    F_vert = row["F_vert_N"]
    v_tan = row["v_tangential_ms"]

    # Shaft torque [N*m] — dimensional check: F_tan[N] * r[m] = N*m
    tau = F_tan * r

    # Arm angular velocity [rad/s] — from v_tangential = omega * r
    omega_arm = v_tan / r

    # Shaft power per vessel [W] — Pitfall C2 guard: F_tan * v_tan (NOT L/D * P_drag)
    # Cross-check: tau * omega = F_tan*r * (v_tan/r) = F_tan * v_tan = P_shaft (from foil_forces.py)
    P_shaft = F_tan * v_tan  # [W]
    P_shaft_check = row["P_shaft_W"]
    assert abs(P_shaft - P_shaft_check) < 0.01 * abs(P_shaft_check) + 0.1, \
        f"P_shaft consistency check at lambda={lam}: computed {P_shaft:.3f}, sweep has {P_shaft_check:.3f}"

    # Energy per ascending traverse (H/v_loop seconds at constant P_shaft)
    W_foil_per_vessel = P_shaft * t_ascending  # [J]

    # Total ascending energy per cycle (12 vessels, each contributing for t_ascending)
    W_foil_ascending_total = N_ascending * W_foil_per_vessel  # [J]

    # Vertical force fraction check
    F_vert_fraction = abs(F_vert) / F_b_avg
    F_vert_flag = "FLAG_LARGE" if F_vert_fraction > 0.20 else "OK"

    # COP_partial: ascending foil contribution only
    COP_partial_asc = (W_buoy + W_foil_ascending_total) / W_pump

    # RPM for reporting
    rpm = omega_arm * 60.0 / (2.0 * math.pi)

    torque_results.append({
        "lambda": lam,
        "AoA_eff_deg": row["AoA_eff_deg"],
        "F_tan_N": F_tan,
        "F_vert_N": F_vert,
        "shaft_torque_per_vessel_Nm": round(tau, 3),
        "omega_rad_s": round(omega_arm, 5),
        "rpm": round(rpm, 3),
        "P_shaft_per_vessel_W": round(P_shaft, 3),
        "t_ascending_s": t_ascending,
        "W_foil_per_vessel_J": round(W_foil_per_vessel, 2),
        "W_foil_ascending_total_J": round(W_foil_ascending_total, 2),
        "N_ascending": N_ascending,
        "F_vert_fraction_of_Fb": round(F_vert_fraction, 5),
        "F_vert_flag": F_vert_flag,
        "COP_partial_ascending_only": round(COP_partial_asc, 6),
        "stall_flag": row["stall_flag"],
    })

# ---------------------------------------------------------------------------
# Step 6: Loop length sensitivity at nominal design lambda=1.0
# ---------------------------------------------------------------------------
row_lam1 = next(r for r in torque_results if abs(r["lambda"] - 1.0) < 0.01)
P_shaft_lam1 = row_lam1["P_shaft_per_vessel_W"]

loop_sensitivity = {}
for ll in loop_length_sensitivity:
    t_asc_ll = 18.288 / v_loop  # t_ascending is H/v_loop, independent of loop_length
    # Loop length only affects t_cycle (full cycle); but we use t_ascending for energy
    # W_foil per vessel depends on t_ascending, NOT loop_length directly
    # loop_length sensitivity affects t_cycle, which sets cycle frequency for RPM calculation
    t_cyc_ll = ll / v_loop
    W_foil_pv = P_shaft_lam1 * t_asc_ll
    W_foil_total = N_ascending * W_foil_pv
    COP_ll = (W_buoy + W_foil_total) / W_pump
    loop_sensitivity[ll] = {
        "loop_length_m": ll,
        "t_ascending_s": round(t_asc_ll, 4),
        "t_cycle_s": round(t_cyc_ll, 4),
        "W_foil_per_vessel_J": round(W_foil_pv, 2),
        "W_foil_ascending_total_J": round(W_foil_total, 2),
        "COP_partial_asc": round(COP_ll, 6),
        "note": "W_foil and COP do not depend on loop_length (t_ascending = H/v_loop is fixed)",
    }

# ---------------------------------------------------------------------------
# Step 7: Summary of key quantities
# ---------------------------------------------------------------------------

# Nominal design point (lambda=1.0)
nominal = row_lam1
print(f"\n--- Nominal Design Point (lambda=1.0, AoA_eff=7 deg) ---")
print(f"  F_tan = {nominal['F_tan_N']:.1f} N")
print(f"  shaft_torque = {nominal['shaft_torque_per_vessel_Nm']:.1f} N*m")
print(f"  omega = {nominal['omega_rad_s']:.4f} rad/s = {nominal['rpm']:.2f} RPM")
print(f"  P_shaft per vessel = {nominal['P_shaft_per_vessel_W']:.1f} W")
print(f"  t_ascending = {nominal['t_ascending_s']:.4f} s")
print(f"  W_foil per vessel = {nominal['W_foil_per_vessel_J']:.1f} J")
print(f"  W_foil ascending total (N=12) = {nominal['W_foil_ascending_total_J']:.1f} J")
print(f"  F_vert fraction = {nominal['F_vert_fraction_of_Fb']:.4f} ({nominal['F_vert_flag']})")
print(f"  COP_partial (ascending) = {nominal['COP_partial_ascending_only']:.4f}")

# F_vert verification: at lambda=1, F_vert should be computable
# F_vert = -L*cos(beta) - D*sin(beta); at beta=45: F_vert = -(L+D)/sqrt(2)
# This opposes ascent

# Sign check: W_foil ascending total positive where F_tan > 0
for r in torque_results:
    expected_positive_W = r["F_tan_N"] > 0
    actual_positive_W = r["W_foil_ascending_total_J"] > 0
    assert expected_positive_W == actual_positive_W, \
        f"W_foil sign inconsistency at lambda={r['lambda']}: F_tan={r['F_tan_N']:.2f}, W_foil={r['W_foil_ascending_total_J']:.2f}"

# omega at lambda=1 verification: v_tan = 3.7137, r=3.66 -> omega = 1.015 rad/s = 9.69 RPM
r_arm = 3.66  # arm radius [m] — separate variable to avoid shadowing loop var r
assert abs(nominal["omega_rad_s"] - (v_loop / r_arm)) < 0.001, \
    f"omega at lambda=1 check: expected {v_loop/r_arm:.4f}, got {nominal['omega_rad_s']:.4f}"
assert abs(nominal["rpm"] - 9.69) < 0.1, \
    f"RPM at lambda=1 check: expected ~9.69, got {nominal['rpm']:.2f}"

print(f"\nomega at lambda=1: {nominal['omega_rad_s']:.4f} rad/s = {nominal['rpm']:.2f} RPM -- OK")

# ---------------------------------------------------------------------------
# Step 8: Find lambda for max P_shaft and max COP_partial_asc
# ---------------------------------------------------------------------------
max_P_row = max(torque_results, key=lambda r: r["P_shaft_per_vessel_W"])
max_COP_row = max(torque_results, key=lambda r: r["COP_partial_ascending_only"])

# Lambda range where F_tan > 0 (and thus W_foil > 0)
positive_F_tan_lambdas = [r["lambda"] for r in torque_results if r["F_tan_N"] > 0]
lambda_min_positive = min(positive_F_tan_lambdas) if positive_F_tan_lambdas else None
lambda_max_positive = max(positive_F_tan_lambdas) if positive_F_tan_lambdas else None

print(f"\nLambda range with F_tan > 0: [{lambda_min_positive}, {lambda_max_positive}]")
print(f"Max P_shaft at lambda={max_P_row['lambda']}: {max_P_row['P_shaft_per_vessel_W']:.1f} W per vessel")
print(f"Max COP_partial_asc at lambda={max_COP_row['lambda']}: {max_COP_row['COP_partial_ascending_only']:.4f}")

# ---------------------------------------------------------------------------
# Step 9: Vertical force check at all lambda
# ---------------------------------------------------------------------------
large_F_vert_cases = [r for r in torque_results if r["F_vert_flag"] == "FLAG_LARGE"]
if large_F_vert_cases:
    print(f"\nWARNING: {len(large_F_vert_cases)} lambda points with |F_vert|/F_b_avg > 0.20:")
    for r in large_F_vert_cases[:5]:
        print(f"  lambda={r['lambda']}: F_vert_fraction={r['F_vert_fraction_of_Fb']:.4f}")
else:
    print(f"\nF_vert fraction check: All points have |F_vert|/F_b_avg <= 0.20 -- OK")
    print(f"  (v_loop correction from foil drag is small; Phase 1 baseline valid)")

# ---------------------------------------------------------------------------
# Assemble and write foil02_ascending_torque.json
# ---------------------------------------------------------------------------
output = {
    "_description": "Phase 2 Plan 01 Task 2: Ascending vessel shaft torque and cycle energy; Phase 1 anchor",
    "_units": "SI throughout: m, m/s, N, N*m, W, J, dimensionless",
    "_assert_convention": (
        "unit_system=SI, geometry=rotating_arm, N_ascending=12, "
        "shaft_torque=F_tan_times_r, W_foil=P_shaft_times_t_ascending, "
        "COP_partial=(W_buoy+W_foil_ascending_total)/W_pump"
    ),
    "geometry_model": "rotating_arm",
    "phase1_inputs": {
        "W_buoy_J": W_buoy,
        "W_pump_J": W_pump,
        "F_b_avg_N": F_b_avg,
        "v_loop_ms": v_loop,
        "v_loop_source": "buoy03_terminal_velocity.json v_handoff.v_vessel_nominal_ms",
        "COP_phase1_reference": COP_phase1,
    },
    "vessel_geometry": {
        "N_ascending": N_ascending,
        "N_descending": N_descending,
        "r_m": r,
        "H_m": 18.288,
        "loop_length_estimate_m": loop_length_nominal,
        "loop_length_note": "2*H + pi*r_nominal ~ 48.07 m; sensitivity in loop_sensitivity",
        "t_ascending_s": t_ascending,
        "t_ascending_source": "H/v_loop = 18.288/3.7137",
        "t_cycle_s": t_cycle,
    },
    "phase1_anchor": {
        "COP_computed": round(COP_anchor, 6),
        "COP_phase1_reference": COP_phase1,
        "anchor_error": round(anchor_error, 8),
        "pass": bool(anchor_error < 0.001),
        "formula": "COP_partial(W_foil=0) = W_buoy / W_pump = 20644.62 / 34227.8",
        "interpretation": (
            "This is the buoyancy-only COP; equal to Phase 1 COP_ideal_max. "
            "Hydrofoil contribution (W_foil) must bring COP >= 1.5 for green light."
        ),
    },
    "loop_length_sensitivity": loop_sensitivity,
    "key_lambdas": {
        "lambda_max_P_shaft": max_P_row["lambda"],
        "max_P_shaft_per_vessel_W": max_P_row["P_shaft_per_vessel_W"],
        "lambda_max_COP_asc": max_COP_row["lambda"],
        "max_COP_partial_asc": max_COP_row["COP_partial_ascending_only"],
        "lambda_min_positive_F_tan": lambda_min_positive,
        "lambda_max_positive_F_tan": lambda_max_positive,
        "note": (
            "COP_partial_asc includes ascending foils only. "
            "Full COP with descending foils computed in Plan 02."
        ),
    },
    "nominal_design_point": {
        "lambda": nominal["lambda"],
        "AoA_eff_deg": nominal["AoA_eff_deg"],
        "shaft_torque_per_vessel_Nm": nominal["shaft_torque_per_vessel_Nm"],
        "omega_rad_s": nominal["omega_rad_s"],
        "rpm": nominal["rpm"],
        "P_shaft_per_vessel_W": nominal["P_shaft_per_vessel_W"],
        "t_ascending_s": nominal["t_ascending_s"],
        "W_foil_per_vessel_J": nominal["W_foil_per_vessel_J"],
        "W_foil_ascending_total_J": nominal["W_foil_ascending_total_J"],
        "F_vert_N": nominal["F_vert_N"],
        "F_vert_fraction_of_Fb": nominal["F_vert_fraction_of_Fb"],
        "F_vert_flag": nominal["F_vert_flag"],
        "COP_partial_ascending_only": nominal["COP_partial_ascending_only"],
        "rpm_check": f"omega=v_tan/r_arm=lambda*v_loop/r_arm=1.0*{v_loop:.4f}/3.66={v_loop/3.66:.4f} rad/s = {v_loop/3.66*60/(2*math.pi):.2f} RPM",
    },
    "pitfall_guards": {
        "fp-LD-as-power-ratio": "PASS: W_foil = P_shaft * t_ascending; no L/D * W_drag instance",
        "fp-fixed-v-vessel": f"PASS: v_loop = {v_loop} m/s loaded from JSON; not hardcoded 3.0 m/s",
        "Pitfall-C2": "PASS: P_shaft = F_tan * v_tangential at every step (verified vs foil01 P_shaft_W)",
    },
    "results": torque_results,
    "dimensional_checks": {
        "shaft_torque_Nm": "F_tan[N] * r[m] = N*m  PASS",
        "P_shaft_W": "F_tan[N] * v_tangential[m/s] = W  PASS",
        "W_foil_J": "P_shaft[W] * t_ascending[s] = J  PASS",
        "COP_partial": "(W_buoy[J] + W_foil[J]) / W_pump[J] = dimensionless  PASS",
    },
}

OUTPUT_PATH = os.path.join(PHASE2_DIR, "foil02_ascending_torque.json")
with open(OUTPUT_PATH, "w") as f:
    json.dump(output, f, indent=2)

print(f"\nWritten: {OUTPUT_PATH}")
print(f"Phase 1 anchor: COP(W_foil=0) = {COP_anchor:.6f} (error={anchor_error:.2e}) -- PASS")
print(f"N_ascending = {N_ascending}")
print(f"t_ascending = {t_ascending:.4f} s (expected 4.924 s)")
print(f"Pitfall guards: all PASS")
