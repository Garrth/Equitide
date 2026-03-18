"""
Create phase2_summary_table.json — Phase 2 complete summary for Phase 3/4 loading.
ASSERT_CONVENTION: unit_system=SI, geometry=rotating_arm, COP_label=COP_partial
"""
import json
import math
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "outputs")
P1 = os.path.join(BASE, "..", "phase1", "outputs")

with open(os.path.join(OUT, "foil04_min_ld.json")) as f:
    cop = json.load(f)
with open(os.path.join(P1, "phase1_summary_table.json")) as f:
    p1 = json.load(f)
with open(os.path.join(P1, "buoy03_terminal_velocity.json")) as f:
    tv = json.load(f)
with open(os.path.join(OUT, "foil03_descending.json")) as f:
    desc = json.load(f)

v_loop = tv["v_handoff"]["v_vessel_nominal_ms"]   # 3.7137 m/s
r_arm = 3.66
recommended_lambda = 0.9
omega_design = recommended_lambda * v_loop / r_arm
rpm_design = omega_design * 60 / (2 * math.pi)

summary = {
    "_description": "Phase 2 summary: all key results FOIL-01 through FOIL-04, formatted for Phase 3/4 loading",
    "_units": "SI throughout: m, kg, s, N, J, W, rad/s, RPM, dimensionless",
    "_assert_convention": "unit_system=SI, geometry=rotating_arm, COP_label=COP_partial",
    "phase": "02-hydrofoil-torque",
    "completion_date": "2026-03-17",
    "requirements_satisfied": ["FOIL-01", "FOIL-02", "FOIL-03", "FOIL-04"],

    # Phase 1 pass-through
    "phase1_inputs": {
        "W_buoy_J": p1["W_buoy_J"],
        "W_pump_nominal_J": p1["W_pump_nominal_J"],
        "F_b_avg_N": p1["F_b_avg_N"],
        "v_loop_nominal_ms": v_loop,
        "v_loop_conservative_ms": tv["v_handoff"]["v_vessel_conservative_ms"],
        "COP_buoy_only_at_eta70": p1["COP_ideal_max_at_eta_70"],
    },

    # Geometry
    "geometry": {
        "r_arm_m": r_arm,
        "H_m": 18.288,
        "N_arms": 3,
        "N_ascending": 12,
        "N_descending": 12,
        "N_total": 24,
        "foil_span_m": 1.0,
        "foil_chord_m": 0.25,
        "foil_AR": 4.0,
        "foil_profile": "NACA 0012",
        "mount_angle_deg": 38.0,
        "mount_angle_note": "Designed at lambda=1 for AoA_target=7 deg",
    },

    # FOIL-01/02: Ascending foils at design
    "ascending_foils": {
        "lambda_design": 1.0,
        "F_tan_N": 1135.524,
        "shaft_torque_per_vessel_Nm": 4156.018,
        "omega_rad_s": 1.01467,
        "rpm": 9.689,
        "P_shaft_per_vessel_W": 4216.995,
        "W_foil_ascending_per_vessel_J": 20766.59,
        "W_foil_ascending_total_J": cop["W_foil_ascending_total_J"],
        "F_vert_fraction_of_Fb": 1.14994,
        "F_vert_flag": "FLAG_LARGE",
        "F_vert_note": "F_vert/F_b_avg = 1.15 >> 0.20 threshold. v_loop baseline is upper bound. Phase 4 coupled solution mandatory.",
        "COP_partial_ascending_only": 1.209871,
    },

    # FOIL-03: Descending tacking
    "descending_foils": {
        "tacking_verdict": desc["tacking_verdict"],
        "tacking_geometry_summary": (
            "Explicit rotating-arm vector geometry (not assumed by symmetry). "
            "Position D (arm at 180 deg from ascending): v_vessel=(-v_tan, 0, -v_loop). "
            "After tack-flip about span axis: lift direction rotated 90 CCW in x-z plane "
            "gives -x component -> drives CCW rotation same as ascending. "
            "F_tan_D = L*sin(beta) - D*cos(beta) = F_tan_A > 0. CONFIRMED."
        ),
        "F_tan_dn_N": desc["F_tan_dn_at_lambda_1"],
        "W_foil_descending_per_vessel_J": desc["W_foil_descending_per_vessel_J"],
        "W_foil_descending_total_J": desc["W_foil_descending_total_J"],
        "N_descending": desc["N_descending"],
        "symmetry_verdict": desc["symmetry_verdict"],
        "darrieus_analogy": (
            "CONFIRMED: C_T = C_L*sin(phi) - C_D*cos(phi) > 0 on both ascending and descending passes "
            "when L/D > lambda. Reference: Paraschivoiu 2002, Wind Turbine Design, Ch. 2."
        ),
    },

    # FOIL-04: COP sweep (must_contain fields)
    "W_foil_ascending_total_J": cop["W_foil_ascending_total_J"],
    "W_foil_descending_total_J": cop["W_foil_descending_total_J"],
    "W_foil_combined_total_J": cop["W_foil_combined_total_J"],
    "COP_partial_nominal": cop["COP_partial_nominal"],
    "COP_partial_at_lambda_0p9": cop["COP_at_recommended_lambda"],
    "lambda_min_for_COP_1p5": cop["lambda_min_for_COP_1p5"],
    "lambda_min_note": (
        "lambda_min=0.7 is at stall (AoA>15 deg for both asc and desc). "
        "First reliable non-stall: lambda=0.8 (NEAR_STALL, COP=1.85). "
        "Design target: lambda=0.9 (OK, COP=2.06)."
    ),
    "lambda_min_for_COP_1p5_non_stall": cop.get("lambda_min_for_COP_1p5_no_stall"),
    "lambda_min_for_COP_1p5_OK_only": cop.get("lambda_min_for_COP_1p5_OK_only"),
    "omega_min_rad_s": cop["omega_min_rad_s"],
    "rpm_min": cop["rpm_min"],
    "v_tangential_min_ms": cop["v_tangential_min_ms"],
    "LD_min_at_lambda_min": cop["lambda_min_for_COP_1p5"],  # (L/D)_min = cot(beta) = lambda
    "LD_min_note": "(L/D)_min = cot(beta) = lambda [Plan 01 algebraic proof]; at lambda=0.7: L/D_min=0.70 << NACA achievable ~9",
    "max_COP_partial": cop["max_COP_partial"],
    "lambda_at_max_COP": cop["lambda_at_max_COP"],
    "recommended_design_lambda": recommended_lambda,
    "omega_design_rad_s": omega_design,
    "rpm_design": rpm_design,
    "v_tangential_design_ms": recommended_lambda * v_loop,
    "COP_at_recommended_design_lambda": cop.get("COP_at_recommended_lambda"),
    "green_light_verdict": cop["green_light_verdict"],

    # Stop conditions
    "stop_conditions": cop["stop_condition_checks"],

    # Critical flags
    "F_vert_flag_PROPAGATED": (
        "FLAG_LARGE: F_vert/F_b_avg = 1.15 at lambda=1.0. "
        "All Phase 2 COP_partial values are UPPER BOUNDS. "
        "Phase 4 coupled (v_loop, omega) solution mandatory before final feasibility verdict."
    ),
    "stall_note": cop.get("stall_note", ""),

    # Anchors
    "phase1_anchor_check": cop["phase1_anchor_check"],

    # Phase 3 handoff
    "phase3_inputs": {
        "lambda_design": recommended_lambda,
        "omega_design_rad_s": omega_design,
        "rpm_design": rpm_design,
        "COP_partial_at_design": cop.get("COP_at_recommended_lambda"),
        "v_tangential_design_ms": recommended_lambda * v_loop,
        "v_tangential_range_ms": [recommended_lambda * v for v in tv["v_handoff"]["v_vessel_range_ms"]],
        "note": (
            "Phase 3 models water co-rotation at omega_design. "
            "Effective v_tangential_eff = v_tangential * (1 - f_corot) where f_corot TBD. "
            "If co-rotation reduces effective lambda significantly, COP_partial will decrease."
        ),
        "warning_F_vert": "F_vert/F_b_avg=1.15: Phase 4 coupled solution will reduce v_loop and reduce COP from Phase 2 values",
    },

    # Uncertainty summary
    "uncertainty_markers": {
        "weakest_anchors": [
            "F_vert/F_b_avg=1.15 at design: v_loop baseline is NOT self-consistent with foil loading",
            "NACA 0012 data at Re~1.3e6 interpolated: ~5-10% uncertainty in C_L, C_D",
            "Prandtl LL for AR=4: ~5-15% uncertainty in C_L_3D, C_D_i",
            "Water co-rotation f_corot=0: Phase 3 may significantly reduce effective v_tangential",
            "Tack mechanism treated as lossless: actual energy cost unknown",
        ],
        "all_COP_are_upper_bounds": True,
    },
}

with open(os.path.join(OUT, "phase2_summary_table.json"), "w") as f:
    json.dump(summary, f, indent=2)

print("phase2_summary_table.json written.")

# Verify required fields
required = [
    "W_foil_ascending_total_J", "W_foil_descending_total_J",
    "W_foil_combined_total_J", "COP_partial_nominal",
    "lambda_min_for_COP_1p5", "omega_min_rad_s", "rpm_min",
    "LD_min_at_lambda_min", "green_light_verdict",
    "phase3_inputs", "requirements_satisfied"
]
with open(os.path.join(OUT, "phase2_summary_table.json")) as f:
    d = json.load(f)
for k in required:
    print(f"  {k}: {'FOUND' if k in d else 'MISSING'}")
