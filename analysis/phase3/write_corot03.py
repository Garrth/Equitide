"""Helper script to write corot03_lift_preservation.json"""
import json
import math
import os

# Load dependencies from existing JSON (no recomputation of f_stall)
corot01 = json.load(open('analysis/phase3/outputs/corot01_angular_momentum_model.json'))
p2 = json.load(open('analysis/phase2/outputs/phase2_summary_table.json'))

f_stall = corot01['f_stall']
lambda_max = corot01['lambda_max_from_foil01_interpolated']
lambda_design = p2['phase3_inputs']['lambda_design']
v_tan_design = p2['phase3_inputs']['v_tangential_design_ms']
v_loop = p2['phase1_inputs']['v_loop_nominal_ms']

# Numerical demonstration of lift preservation at key f values
demo_points = []
for f_val in [0.0, 0.1, 0.2, round(f_stall, 6)]:
    v_rel_h = v_tan_design * (1 - f_val)
    v_rel_v = v_loop  # UNCHANGED
    v_rel_total = math.sqrt(v_rel_h**2 + v_rel_v**2)
    beta_eff_deg = math.degrees(math.atan2(v_loop, v_rel_h))
    lambda_eff = lambda_design / (1 - f_val) if f_val < 1 else float('inf')
    demo_points.append({
        'f': round(f_val, 6),
        'v_rel_h_ms': round(v_rel_h, 4),
        'v_rel_v_ms': round(v_rel_v, 4),
        'v_rel_total_ms': round(v_rel_total, 4),
        'beta_eff_deg': round(beta_eff_deg, 2),
        'lambda_eff': round(lambda_eff, 4),
        'v_rel_v_unchanged': True
    })

# Build f_stall note without nested f-strings
f_stall_note = (
    "f_stall = 1 - {:.1f}/{:.4f} = {:.6f}; consistent with plan reference 0.291 "
    "(difference {:.4f} due to lambda interpolation vs 1.27)"
).format(lambda_design, lambda_max, f_stall, abs(f_stall - 0.291))

# Lift preservation argument
lift_arg = (
    "v_rel_v = v_loop = {:.4f} m/s > 0 for all f. "
    "Lift L = 0.5*rho_w*C_L*A_foil*v_rel^2 where v_rel = sqrt(v_rel_h^2 + v_rel_v^2) >= v_loop > 0. "
    "Therefore L > 0 for all f < 1 (even if v_rel_h -> 0, v_rel >= v_loop > 0). "
    "The stall constraint (AoA limit) restricts f, not the lift formula."
).format(v_loop)

lift_verdict = (
    "PRESERVED: v_rel_v = v_loop = {:.4f} m/s independent of f. "
    "Hydrofoil lift is nonzero for all f < f_stall = {:.4f}."
).format(v_loop, f_stall)

stall_impl = (
    "Stall at f_stall = {:.4f} limits useful co-rotation range. "
    "Above f_stall, lambda_eff > lambda_max = {:.4f} and ascending foil AoA exceeds stall angle (~15 deg). "
    "The stall is not a lift-going-to-zero event; it is an AoA-exceeding-stall-angle event."
).format(f_stall, lambda_max)

lambda_eff_physical = (
    "lambda_eff = v_tan / v_rel_h = v_tan / [v_tan*(1-f)] = 1/(1-f) * lambda_design. "
    "As f increases, lambda_eff increases. At f=f_stall, lambda_eff = lambda_max = {:.4f}."
).format(lambda_max)

lambda_eff_formula_str = "{:.1f} / (1-f)".format(lambda_design)

output = {
    "_description": "Phase 3 Plan 01 Task 2: Lift preservation geometric argument (COROT-03)",
    "_units": "SI throughout: m/s, dimensionless",
    "_assert_convention": "unit_system=SI, co_rotation_fraction=f in [0,1], v_water_v=0 (no vertical entrainment)",
    "_lambda_max_source": "loaded from corot01_angular_momentum_model.json (not independently recomputed)",
    "_f_stall_source": "loaded from corot01_angular_momentum_model.json (not independently recomputed)",

    "velocity_decomposition": {
        "v_vessel_horizontal_ms": "v_tan = lambda_design * v_loop = {:.1f} * {:.4f} = {:.4f} m/s (from phase2_summary_table.json)".format(lambda_design, v_loop, v_tan_design),
        "v_vessel_vertical_ms": "v_loop = {:.4f} m/s (from phase2_summary_table.json)".format(v_loop),
        "v_water_horizontal_ms": "f * v_tan  [horizontal co-rotation only; f in [0,1]]",
        "v_water_vertical_ms": 0,
        "v_water_vertical_note": "No vertical water entrainment by horizontal rotation; water recirculates in the tank horizontally only.",
        "v_rel_horizontal_ms": "v_tan * (1-f) = {:.4f} * (1-f)  [reduced by co-rotation factor (1-f)]".format(v_tan_design),
        "v_rel_vertical_ms": "v_loop = {:.4f} m/s  [UNCHANGED for all f in [0,1]]".format(v_loop),
        "v_rel_vertical_independence_proof": (
            "v_rel_v = v_vessel_v - v_water_v = v_loop - 0 = v_loop. "
            "This holds for ALL f because v_water_v = 0 identically (horizontal co-rotation "
            "has no vertical component). Therefore v_rel_v is independent of f."
        )
    },

    "v_rel_vertical_preserved": True,
    "v_rel_vertical_ms": round(v_loop, 4),
    "v_rel_horizontal_reduced_factor": "(1-f)",
    "v_rel_vertical_reduced_factor": 1.0,

    "lift_preservation_argument": lift_arg,

    "numerical_demonstration": {
        "description": "v_rel_v = v_loop at multiple f values confirms independence",
        "points": demo_points
    },

    "lambda_eff_formula": "lambda_design / (1-f)",
    "lambda_eff_formula_numeric": lambda_eff_formula_str,
    "lambda_eff_physical_meaning": lambda_eff_physical,

    "f_stall_calculation": {
        "lambda_design_from_phase2": lambda_design,
        "lambda_design_source": "phase2_summary_table.json phase3_inputs.lambda_design",
        "lambda_max_from_phase2": round(lambda_max, 4),
        "lambda_max_source": "corot01_angular_momentum_model.json (interpolated from foil01_force_sweep.json)",
        "formula": "f_stall = 1 - lambda_design / lambda_max",
        "f_stall_from_corot01": round(f_stall, 6),
        "f_stall_source": "loaded from corot01_angular_momentum_model.json (not independently recomputed)",
        "f_stall_note": f_stall_note
    },

    "lift_preservation_verdict": lift_verdict,
    "stall_implication": stall_impl,

    "consistency_checks": {
        "f_stall_vs_lambda_eff_max": {
            "f_stall": round(f_stall, 6),
            "lambda_eff_at_f_stall": round(lambda_design / (1 - f_stall), 4),
            "lambda_max": round(lambda_max, 4),
            "match": abs(lambda_design / (1 - f_stall) - lambda_max) < 1e-4,
            "note": "lambda_eff(f_stall) should equal lambda_max by definition of f_stall"
        },
        "v_rel_v_at_f_stall": {
            "f": round(f_stall, 6),
            "v_rel_v_ms": round(v_loop, 4),
            "unchanged": True
        }
    },

    "requirement": "COROT-03",
    "requirements_satisfied": ["COROT-03"],

    "references": {
        "phase2_summary_table_json": "Provides lambda_design, v_tan_design, v_loop",
        "corot01_angular_momentum_model_json": "Provides f_stall, lambda_max (loaded, not recomputed)"
    }
}

output_path = 'analysis/phase3/outputs/corot03_lift_preservation.json'
with open(output_path, 'w') as f:
    json.dump(output, f, indent=2)
print('Written:', output_path)
print('v_rel_vertical_preserved:', output['v_rel_vertical_preserved'])
print('lift_preservation_verdict:', output['lift_preservation_verdict'])
print('f_stall loaded:', output['f_stall_calculation']['f_stall_from_corot01'])
print('lambda_eff_formula:', output['lambda_eff_formula'])
print('requirements_satisfied:', output['requirements_satisfied'])

# Verify all required must_contain fields
required = [
    'velocity_decomposition', 'v_rel_vertical_preserved', 'v_rel_horizontal_reduced_factor',
    'lambda_eff_formula', 'f_stall_calculation', 'lift_preservation_verdict'
]
missing = [r for r in required if r not in output]
print('Missing required fields:', missing if missing else 'NONE - all present')

# Verify f_stall match with corot01
diff = abs(output['f_stall_calculation']['f_stall_from_corot01'] - corot01['f_stall'])
print('f_stall consistent check (diff={:.2e}): {}'.format(diff, diff < 1e-6))

# Verify f_stall value ≈ 0.29 (within expected range)
print('f_stall in expected range [0.28, 0.32]:', 0.28 <= f_stall <= 0.32)
