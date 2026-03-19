# Phase 3: Co-Rotation Results

**Phase 3 verdict: net_positive** — co-rotation saves ~46.8 kW net at maximum achievable f = f_stall = 0.294 with P_corot = 0.72 kW maintenance cost. Both optimistic (P_corot×0.5) and pessimistic (P_corot×2.0) scenarios remain strongly positive.

---

## 1. Co-Rotation Model

**What is co-rotation fraction f?**
f = v_water_horizontal / v_vessel_horizontal. At f=0, water is stationary. At f=f_stall≈0.294, the water horizontal velocity equals 0.294 × v_tan_design, and the ascending foil reaches stall angle (AoA = AoA_stall).

**f_ss upper bound:** 0.635 (smooth-cylinder model, treating vessel chain as continuous rotating inner cylinder)

**Binding constraint:** f_stall = 0.294 (hydrofoil stall at lambda_eff = lambda_max = 1.275). The smooth-cylinder f_ss = 0.635 exceeds the stall boundary; therefore **the maximum achievable co-rotation is f = f_stall = 0.294**.

**P_corot at design omega:** 22.2 kW (nominal), range [11.1, 44.4] kW (±50% C_f uncertainty)
**P_corot at f_stall = 0.294 (actual operating point):** 0.72 kW (much lower because omega_w = 0.294 × omega_design = 0.268 rad/s; P_corot ∝ omega_w³)

**Spin-up time:** τ ≈ 71 s (turbulent eddy diffusion; marginal quasi-steady — steady-state analysis is an approximation)

**Key approximation:** Taylor-Couette smooth-cylinder wall friction model (Schlichting §21.2, Prandtl 1/5-power). Factor-of-2 uncertainty in P_corot at any given f.

---

## 2. P_net(f) Table

P_net(f) = N_total × P_drag_saved_per_vessel(f) − P_corot(f)

Power saving uses the **cubic formula**: P_drag_saved = P_drag_full × [1 − (1−f)³]

*NOT the force formula (1−f)²; power scales as v³, force as v².*

Baseline drag power (all 24 vessels, no co-rotation): P_drag_full = 73.4 kW

| f    | P_drag_saved (kW) | P_corot (kW) | P_net (kW) | COP_corot |
|------|:-----------------:|:------------:|:----------:|:---------:|
| 0.00 |      0.000        |    0.000     |    0.000   |   2.057   |
| 0.05 |     10.463        |    0.005     |   10.458   |   1.886   |
| 0.10 |     19.881        |    0.035     |   19.846   |   1.695   |
| 0.15 |     28.308        |    0.110     |   28.199   |   1.480   |
| 0.20 |     35.800        |    0.245     |   35.555   |   1.228   |
| 0.25 |     42.412        |    0.458     |   41.955   |   0.922   |
| 0.29 |     47.105        |    0.693     |   46.411   |   0.634   |

*f = 0.29 ≈ f_stall = 0.294 (last achievable operating point before foil stall)*

**P_net is positive throughout** — no breakeven crossing within achievable domain. P_net peaks at f_stall (stall-limited, not P_corot-dominated).

---

## 3. Lift Preservation (COROT-03)

**Verdict: PRESERVED.** Vertical relative velocity v_rel_v = v_loop = 3.7137 m/s is independent of f.

**Proof:** Co-rotation is horizontal only. Water has no vertical velocity component (v_water_v = 0 for all f). Therefore v_rel_v = v_vessel_v − v_water_v = v_loop − 0 = v_loop, independent of f.

The stall at f_stall = 0.294 is an angle-of-attack event (AoA exceeds stall angle), not a lift-going-to-zero event. Lift remains nonzero for all f < f_stall.

---

## 4. Phase 3 Verdict

**Verdict: net_positive**

| Scenario | P_corot scale | P_net at f_stall |
|----------|:-------------:|:----------------:|
| Optimistic (P_corot × 0.5) | ×0.5 | **+47.2 kW** |
| Nominal | ×1.0 | **+46.8 kW** |
| Pessimistic (P_corot × 2.0) | ×2.0 | **+46.1 kW** |

All three scenarios are strongly positive. The factor-of-2 uncertainty in P_corot does not change the verdict because P_corot (0.72 kW at f_stall) is negligible compared to P_drag_saved (47.5 kW).

**COP_corot at f_stall = 0.603** — this is the effective partial COP at the co-rotating operating point. COP_corot decreases from 2.057 (at f=0, Phase 2 value) to 0.603 at f_stall because the foil forces diminish as lambda_eff approaches lambda_max (stall).

---

## 5. Key Caveats

1. **Smooth-cylinder approximation, factor-of-2:** The Taylor-Couette P_corot model treats the vessel chain as a continuous rotating cylinder. Discrete-vessel geometry (spacing, fill fraction ~60%) reduces drag coupling by roughly a factor of 2. f_ss is labeled an upper bound; actual f_ss in practice may be 30–50% lower.

2. **Stall constraint:** f_stall = 0.294 limits the useful co-rotation range. The smooth-cylinder f_ss = 0.635 cannot be achieved — the hydrofoil stalls at f = 0.294. The effective "design" f is therefore f_stall, not f_ss.

3. **COP_corot is partial:** Phase 3 COP_corot = 0.603 at f_stall excludes hull drag, bearing friction, and the F_vert coupling correction (Phase 4). All Phase 2 and Phase 3 COP values are upper bounds pending the Phase 4 coupled (v_loop, ω) solution.

4. **F_vert flag propagated:** Phase 2 FLAG F_vert/F_b_avg = 1.15 >> 0.20 threshold is carried forward. Phase 4 coupled solution is mandatory before final feasibility verdict.

5. **Stall-limited before P_corot dominates:** The P_net curve does not peak and decline within the achievable f range. P_corot at the stall boundary (0.72 kW) is ~65× smaller than P_drag_saved (47.5 kW). This means co-rotation is economical throughout the entire achievable domain.

---

## 6. Phase 4 Inputs

| Quantity | Value | Notes |
|----------|-------|-------|
| co_rotation_f_ss | 0.294 | f_stall (binding constraint; smooth-cylinder upper bound 0.635 not achievable) |
| P_corot_W | 720 W | At f=f_stall; range [360, 1440] W (±50% C_f) |
| P_net_at_fss_W | 46,826 W | Net benefit at f_stall |
| P_net_range_at_fss_W | [47,186, 46,105] W | [optimistic, pessimistic] — both strongly positive |
| COP_corot_at_fss | 0.603 | Partial COP at operating point (Phase 4 adds remaining losses) |
| COP_partial_Phase2 | 2.057 | Phase 2 value at f=0 (upper bound) |
| phase3_verdict | **net_positive** | Robust across ±50% P_corot uncertainty |
| F_vert_flag_propagated | true | Phase 4 coupled (v_loop, ω) solution mandatory |

**Phase 3 uncertainty note:** P_corot and f_ss have factor-of-2 uncertainty from smooth-cylinder Taylor-Couette approximation. The net_positive verdict is robust because P_corot is negligible compared to P_drag_saved at achievable f values.

---

## 7. F_vert Flag (Phase 2 → Phase 4)

**Phase 2 FLAG carried forward: F_vert/F_b_avg = 1.15; Phase 4 coupled solution mandatory.**

At the Phase 2 design point (lambda=0.9), the vertical component of foil force is 1.15× the average buoyancy force. This means v_loop (used as Phase 1 terminal velocity) is NOT self-consistent with the actual foil loading. Phase 4 must solve the coupled (v_loop, ω) system simultaneously. All Phase 2 and Phase 3 COP values should be treated as upper bounds until this correction is made.

---

*Generated by: analysis/phase3/corot02_net_benefit_sweep.py*
*Sources: corot01_angular_momentum_model.json, corot03_lift_preservation.json, corot02_net_benefit_sweep.json*
*Date: 2026-03-18*
