# Experiment Design: Phase 1 — Air, Buoyancy & Fill

> **For gpd-executor:** This file contains parameter specifications, convergence criteria, and
> statistical analysis plans for all Phase 1 computational tasks. Use these when executing
> computational work in this phase. No production run should proceed until the sanity checks
> in Section 6 pass.

**Phase goal:** Establish all energy values associated with the air/water/buoyancy subsystem
and confirm fill feasibility.

**Designed:** 2026-03-16
**Conventions source:** `.gpd/CONVENTIONS.md` (all symbols, formulas, and locked values)
**Research source:** `phases/01-air-buoyancy-and-fill/01-RESEARCH.md`
**Pitfalls source:** `research/PITFALLS.md` (C1, C6, C7, M1, M5 are directly applicable)

---

## 1. Target Quantities

| Quantity | Symbol | Dimensions | Expected Value | Required Accuracy | Validation Source |
|----------|--------|------------|----------------|-------------------|-------------------|
| Isothermal compression work | W_iso | J | 20,640 J | < 0.1% (< 21 J) | CONVENTIONS.md test value |
| Adiabatic compression work | W_adia | J | 24,040 J | < 0.1% (< 24 J) | CONVENTIONS.md test value |
| Adiabatic/isothermal ratio | W_adia / W_iso | dimensionless | 1.161 | < 0.003 absolute | Analytical: gamma=1.4, P_r=2.770 |
| Real pump work (range) | W_pump | J | 28,200–36,900 J | 1% relative per eta_c point | Derived: W_adia / eta_c |
| Buoyancy work integral (numerical) | W_buoy | J | 20,640 J | **< 1% mandatory gate** | Must equal W_iso |
| Average buoyancy force | F_b_avg | N | 1,129 N | < 0.5% | W_iso / H = 20,640 / 18.288 |
| Terminal velocity (F_chain = 0) | v_terminal | m/s | 3.4–4.2 m/s | 0.1 m/s resolution | Force balance; sweep over C_D |
| Fill window duration | t_fill | s | 1.44–2.87 s | 0.01 s | Depends on v_terminal result |
| Required volumetric flow rate | Q_required | m³/s (and CFM) | ~0.038 m³/s (80 CFM@depth) | 5% | V_depth / t_fill |
| Reynolds number at v_terminal | Re | dimensionless | ~1.4–1.9 × 10⁶ | Factor-of-2 | v * d / nu_w; confirms C_D regime |

**Derived quantities consumed by later phases:**

- v_vessel: locked value to pass to Phase 2 (from terminal velocity calculation)
- W_pump(eta_c): full table passed to Phase 4 as COP denominator
- Fill feasibility verdict: binary go/no-go on compressor spec match

---

## 2. Control Parameters

| Parameter | Symbol | Range | Sampling | N_points | Rationale |
|-----------|--------|-------|----------|----------|-----------|
| Drag coefficient | C_D | [0.8, 1.2] | Uniform | 5 | Hoerner empirical range for blunt cylinder at Re ~ 10⁶; endpoints are hard physical bounds |
| Compressor isentropic efficiency | eta_c | [0.65, 0.70, 0.75, 0.80, 0.85] | Fixed list | 5 | Industry range for single-stage rotary/piston; 0.85 is optimistic ceiling; 0.65 covers aged equipment |
| Chain tension (sensitivity only) | F_chain | {0, 200, 500} N | Fixed list | 3 | 0 = isolated-vessel upper bound; 200 N = light coupling; 500 N = moderate coupling |
| Vessel velocity (fill sweep) | v_vessel | [2.0, 2.5, 3.0, 3.5, 4.0] m/s | Fixed list | 5 | Spans plausible terminal velocity range; centered on 3 m/s user estimate |

**Fixed (locked) parameters for all computations:**

| Parameter | Value | Source |
|-----------|-------|--------|
| H | 18.288 m | CONVENTIONS.md §4 |
| P_atm | 101,325 Pa | CONVENTIONS.md §4 |
| rho_w | 998.2 kg/m³ | CONVENTIONS.md §3 |
| g | 9.807 m/s² | CONVENTIONS.md §3 |
| V_surface | 0.2002 m³ | CONVENTIONS.md §6 |
| V_depth | 0.07228 m³ | CONVENTIONS.md §6 |
| A_frontal | 0.1640 m² | CONVENTIONS.md §12 |
| d_vessel | 0.457 m | CONVENTIONS.md §12 |
| R_tank | 3.66 m | CONVENTIONS.md §4 |
| nu_w | 1.004 × 10⁻⁶ m²/s | CONVENTIONS.md §3 |
| gamma | 1.4 | CONVENTIONS.md §3 |
| P_r | 2.7669 | Derived: P_bottom / P_atm |
| C_loop | 22.996 m | Derived: 2π × R_tank |
| Fill arc | 5.749 m | Derived: C_loop / 4 |

---

## 3. Computation Structure: Four Tasks

Phase 1 consists of four distinct computations executed in strict sequence. Later tasks depend
on earlier results.

```
THRM-01  →  BUOY-02  →  BUOY-03  →  FILL-01/02/03
(thermodynamics)  (buoyancy gate)  (terminal velocity)  (fill feasibility)
```

No task should execute until all upstream gates pass. If a gate fails, stop and diagnose before
continuing.

---

## 4. Task Specifications

### Task THRM-01: Compression Work Bounds

**Purpose:** Establish W_iso and W_adia as the thermodynamic energy bounds for one compression cycle.

**Method:** Closed-form evaluation of known formulas. No numerical integration needed here.

**Formulas (use verbatim from CONVENTIONS.md §3 and §9):**

```
W_iso  = P_atm * V_surface * ln(P_r)
       = 101325 * 0.2002 * ln(P_bottom / P_atm)

W_adia = (gamma / (gamma - 1)) * P_atm * V_surface * (P_r^((gamma-1)/gamma) - 1)
       = 3.5 * 101325 * 0.2002 * (P_r^0.2857 - 1)

W_pump(eta_c) = W_adia / eta_c   for eta_c in {0.65, 0.70, 0.75, 0.80, 0.85}
```

**Required output table:**

| eta_c | W_pump (J) | W_pump (kJ) | COP_ideal_max = W_iso / W_pump |
|-------|-----------|-------------|-------------------------------|
| 0.65 | 36,861 | 36.86 | 0.560 |
| 0.70 | 34,228 | 34.23 | 0.603 |
| 0.75 | 31,946 | 31.95 | 0.646 |
| 0.80 | 29,949 | 29.95 | 0.689 |
| 0.85 | 28,188 | 28.19 | 0.732 |

Note: COP_ideal_max is the ceiling COP if ALL buoyancy work were recovered and NO losses existed.
It is below 1.0 for all eta_c values, confirming that buoyancy alone cannot achieve COP > 1.
Hydrofoil contribution is required to reach the target COP = 1.5 (Phase 4 verdict).

**Gates for THRM-01:**

| Check | Expected | Tolerance | Action if Fails |
|-------|----------|-----------|-----------------|
| W_iso == 20,640 J | 20,640 J | ± 21 J (0.1%) | Recheck P_r, V_surface, ln formula |
| W_adia == 24,040 J | 24,040 J | ± 24 J (0.1%) | Recheck gamma, exponent (gamma-1)/gamma = 0.2857 |
| W_adia / W_iso == 1.161 | 1.161 | ± 0.003 | Check both values independently |
| W_pump(0.70) in [34,000, 34,500] J | 34,228 J | ± 344 J (1%) | Recheck W_adia |
| W_pump > W_iso for all eta_c | Always | — | If W_pump < W_iso, sign of eta_c correction is wrong |

**Anti-pattern sentinel:** If W_iso > 22,000 J, a constant-volume error (PITFALL-C1) has occurred.
If W_iso < 19,000 J, the pressure profile uses gauge pressure instead of absolute.

**Mandatory note in output:** Report that W_pump in the range 28–37 kJ is the actual energy input
to use in Phase 4 COP, NOT W_iso = 20,640 J (which is the theoretical reversible minimum only).

---

### Task BUOY-02: Numerical Buoyancy Integral (Mandatory Gate)

**Purpose:** Verify the thermodynamic identity W_buoy = W_iso to < 1% using scipy.integrate.quad.
This is the single most important validation in Phase 1.

**Why this runs before BUOY-03:** The identity check validates the code's pressure profile,
volume formula, and sign conventions before those functions are used in the force-balance iteration.

**Integrand:**

```python
def F_b(z):
    P_z = P_atm + rho_w * g * (H - z)     # hydrostatic pressure at height z
    V_z = V_surface * P_atm / P_z          # Boyle's law volume (isothermal)
    return rho_w * g * V_z                  # buoyancy force at height z

W_buoy, error_estimate = scipy.integrate.quad(F_b, 0, H, limit=100, epsabs=1e-6, epsrel=1e-8)
```

**Coordinate convention:** z = 0 at tank bottom; z = H = 18.288 m at water surface. The integrand
is smooth and monotone increasing (F_b grows as the vessel rises). No singularities on [0, H].

**Expected integrand profile:**

| z (m) | P(z) (Pa) | V(z) (m³) | F_b(z) (N) |
|-------|-----------|-----------|-----------|
| 0.000 | 280,500 | 0.07228 | 707.6 |
| 4.572 | 235,594 | 0.08607 | 842.7 |
| 9.144 | 190,688 | 0.10635 | 1041.3 |
| 13.716 | 145,782 | 0.13923 | 1363.6 |
| 18.288 | 101,325 | 0.20020 | 1959.8 |

#### Convergence Study for scipy.quad

The integrand is smooth with no poles on [0, H]. Expected Gauss-Kronrod convergence is
exponential in limit; even modest settings are far more than adequate. The study below
documents that the 1% gate is satisfied at every tolerance level.

**Convergence study points:**

| atol | rtol | Expected abs error | Expected rel error | Recommended? |
|------|------|-------------------|-------------------|--------------|
| 1e-2 | 1e-2 | << 1 J | << 0.005% | No (for test only) |
| 1e-4 | 1e-4 | << 0.01 J | << 5e-5% | Adequate |
| 1e-6 | 1e-8 | << 1e-4 J | << 5e-7% | **Use this** |
| 1e-10 | 1e-12 | Machine precision | ~1e-10% | Overkill |

**Protocol:** Run at (atol=1e-6, rtol=1e-8) as production. For documentation, run once at
(atol=1e-2, rtol=1e-2) to show the 1% gate is trivially satisfied even at loose tolerance.
This demonstrates the gate is robust to algorithm settings — it is a physics check, not a
numerical precision question.

**Convergence verification table to produce:**

| Tolerance (atol, rtol) | W_buoy (J) | Error vs W_iso | Relative error | Gate pass? |
|-----------------------|-----------|----------------|---------------|------------|
| (1e-2, 1e-2) | ~20,640 | ~0 J | ~0.00% | Yes |
| (1e-6, 1e-8) | ~20,640 | ~0 J | ~0.00% | Yes |

**Mandatory gate:**

```
assert abs(W_buoy - W_iso) / W_iso < 0.01, \
    f"GATE FAIL: W_buoy={W_buoy:.1f}J vs W_iso={W_iso:.1f}J, error={abs(W_buoy-W_iso)/W_iso*100:.2f}%"
```

**Red flag sentinel:** If W_buoy > 25,000 J, the integrand uses constant volume (F_b = rho_w * g
* V_surface, not V(z)). This is PITFALL-C1. Stop immediately and fix the integrand.

**Analytical cross-check:** The integral has a known closed form obtainable by substitution
u = P(z), du = -rho_w * g * dz:

```
W_buoy = integral_0^H [rho_w * g * V_surface * P_atm / P(z)] dz
       = [P_atm * V_surface / 1] * integral_{P_bottom}^{P_atm} [-1/P] dP
       = P_atm * V_surface * ln(P_bottom / P_atm)
       = W_iso  (exactly)
```

Show this derivation in the output alongside the numerical result.

---

### Task BUOY-03: Terminal Velocity Fixed-Point Iteration

**Purpose:** Determine the self-consistent terminal velocity of a single ascending vessel,
parameterized over C_D. Result updates v_vessel from the preliminary value of 3.0 m/s.

**Force balance at terminal velocity:**

```
F_net = 0
F_b_avg - F_drag(v_t) - F_chain = 0

where:
  F_b_avg = W_iso / H = 20,640 / 18.288 = 1128.9 N
  F_drag(v) = 0.5 * rho_w * C_D * A_frontal * v^2
  F_chain: chain coupling tension (sensitivity parameter)
```

**Note on F_b_avg:** The average buoyancy force W_iso/H is used here as the driving force.
This is the energy-weighted average — it yields the correct energy balance. The actual force
varies from 707.6 N at the bottom to 1959.8 N at the surface. A single-point terminal velocity
is an approximation; the vessel actually accelerates from a lower initial speed at the bottom
to a higher speed near the surface. For Phase 1 feasibility, this average is appropriate.

**Iteration formula (rearrange force balance):**

```python
def terminal_velocity(C_D, F_chain=0.0, tol=1e-6, max_iter=20):
    F_net_drive = F_b_avg - F_chain
    if F_net_drive <= 0:
        return None  # chain tension exceeds buoyancy; no ascent
    v = 3.0  # initial guess (m/s)
    for i in range(max_iter):
        v_new = math.sqrt(2 * F_net_drive / (rho_w * C_D * A_frontal))
        if abs(v_new - v) / v < tol:
            return v_new, i+1
        v = v_new
    return v, max_iter  # flag non-convergence
```

Note: This iteration is actually not iterative in the traditional sense — F_b_avg does not
depend on v (it is the average force over the whole path, not F_b at any specific v). The
formula gives the result in one step. The "iteration" structure is retained for generality and
to match the method description in RESEARCH.md; convergence is confirmed in < 3 steps.

**Expected results table (F_chain = 0):**

| C_D | v_terminal (m/s) | Re = v*d/nu_w | C_D regime check |
|-----|-----------------|---------------|-----------------|
| 0.8 | 4.152 | 1.89 × 10⁶ | Turbulent sep.; C_D valid |
| 0.9 | 3.915 | 1.78 × 10⁶ | Turbulent sep.; C_D valid |
| 1.0 | 3.714 | 1.69 × 10⁶ | Turbulent sep.; C_D valid |
| 1.1 | 3.541 | 1.61 × 10⁶ | Turbulent sep.; C_D valid |
| 1.2 | 3.390 | 1.54 × 10⁶ | Turbulent sep.; C_D valid |

All Re values are in the range 1.5–2.0 × 10⁶, well within the 10⁵–10⁶ range for which
Hoerner C_D = 0.8–1.2 applies (blunt cylinder, turbulent separation). The C_D assumption
is self-consistent.

**Expected results table (C_D vs F_chain sensitivity):**

| C_D | F_chain = 0 N | F_chain = 200 N | F_chain = 500 N |
|-----|-------------|----------------|----------------|
| 0.8 | 4.152 m/s | 3.766 m/s | 3.099 m/s |
| 1.0 | 3.714 m/s | 3.369 m/s | 2.772 m/s |
| 1.2 | 3.390 m/s | 3.075 m/s | 2.530 m/s |

**Key finding to report:** All terminal velocity values in the C_D × F_chain parameter space
are within 17–28% of the 3.0 m/s user estimate. The 3.0 m/s assumption is conservative relative
to the F_chain = 0 upper bound (~3.4–4.2 m/s) and may be close to the true coupled-system value
(~2.5–3.4 m/s for F_chain = 200–500 N). The fill calculations should be run with the full
velocity range, not just 3.0 m/s.

**Convergence documentation requirement:** Report the number of iterations and the converged
value for each (C_D, F_chain) combination. Expected: convergence in 1–3 iterations. If
convergence requires > 10 iterations, report as anomalous.

**Gates for BUOY-03:**

| Check | Expected | Tolerance | Action if Fails |
|-------|----------|-----------|-----------------|
| All Re in [10⁵, 10⁷] | ~10⁶ | — | If Re < 10⁴, C_D regime is wrong; consult Hoerner for Stokes regime |
| v_terminal > 0 for all (C_D, F_chain) combinations | > 0 | — | If v_terminal <= 0, chain tension exceeds buoyancy; flag as design constraint |
| v_terminal in [1.0, 10.0] m/s for all table entries | 2.5–4.2 m/s | — | If > 10 m/s: A_frontal or C_D too small; if < 1 m/s: drag overestimated |
| Iteration convergence < 10 steps | 1–3 steps | — | Report if > 10 steps |

**Output for downstream phases:** The locked v_vessel value passed to Phase 2 is taken from the
row C_D = 1.0, F_chain = 0 (v_terminal = 3.714 m/s as upper bound) unless chain tension estimates
are available. Document this choice explicitly. If Phase 2 requires a conservative (slower)
estimate, use C_D = 1.2, F_chain = 200 N (v_terminal = 3.075 m/s).

---

### Task FILL-01 / FILL-02 / FILL-03: Fill Window and Flow Rate

**Purpose:** Determine whether a commercially available compressor can deliver the required
flow rate of compressed air within the fill window.

**Dependency:** These tasks use v_vessel from BUOY-03. Do not use v = 3.0 m/s directly; use
the computed terminal velocity values from the BUOY-03 table.

#### FILL-01: Fill Window Duration

**Formula:**

```
arc_length = C_loop / 4 = 2 * pi * R_tank / 4 = 5.749 m  (1/4 loop circumference)
t_fill(v_vessel) = arc_length / v_vessel
```

**Results table:**

| v_vessel (m/s) | t_fill (s) | Notes |
|---------------|-----------|-------|
| 2.0 | 2.875 | Low end: C_D=1.2, F_chain=500N |
| 2.5 | 2.300 | Moderate chain coupling |
| 3.0 | 1.916 | User baseline estimate |
| 3.5 | 1.642 | Near C_D=1.0, F_chain=0 |
| 3.714 | 1.548 | Upper bound: C_D=1.0, F_chain=0 |
| 4.0 | 1.437 | Upper bound: C_D=0.8, F_chain=0 |

#### FILL-02: Required Flow Rate

**Formula:**

```
Q_required(v_vessel) = V_depth / t_fill(v_vessel)
```

**Unit conversions (apply ALL of these; verify consistency):**

```
1 m³/s = 2118.88 CFM (cubic feet per minute) at same pressure
Q is at depth pressure P_bottom = 280,500 Pa (2.770 atm)
Q_free_air (SCFM at P_atm) = Q_CFM_depth * P_r = Q_CFM_depth * 2.770
```

**Results table:**

| v_vessel (m/s) | t_fill (s) | Q_depth (m³/s) | Q_depth (CFM) | Q_free (SCFM) |
|---------------|-----------|---------------|--------------|--------------|
| 2.0 | 2.875 | 0.02514 | 53.2 | 147 |
| 2.5 | 2.300 | 0.03143 | 66.6 | 184 |
| 3.0 | 1.916 | 0.03772 | 79.9 | 221 |
| 3.5 | 1.642 | 0.04403 | 93.3 | 258 |
| 3.714 | 1.548 | 0.04670 | 98.9 | 274 |
| 4.0 | 1.437 | 0.05030 | 106.6 | 295 |

**Critical note on units:** Q_depth (CFM) is the flow rate of compressed air at depth pressure.
This is what the compressor must deliver at the nozzle. Q_free (SCFM) is the equivalent
volume of free air at surface pressure that must be processed. Commercial compressors are
rated in SCFM or ACFM (actual CFM at intake conditions, which is surface P_atm). The
compressor rating to search for is Q_free in SCFM.

#### FILL-03: Feasibility Assessment

**Method:** Compare Q_free against commercial compressed-air specifications at the required
delivery pressure P_bottom = 280,500 Pa = 40.7 psi = 2.77 atm (gauge pressure 39.7 psig).

**Feasibility criterion:**
- The required delivery pressure is approximately 40 psig.
- Commercial single-stage reciprocating compressors rated at 40–125 psig are widely available.
- Typical flow rates at 40 psig: 10–500 SCFM for industrial compressors.
- The required range (147–295 SCFM depending on vessel velocity) is achievable with mid-to-large
  industrial rotary screw or multi-cylinder reciprocating units.

**Feasibility verdict table:**

| v_vessel (m/s) | Q_free (SCFM) | Compressor class | Feasibility |
|---------------|--------------|-----------------|-------------|
| 2.0 | 147 | Large portable / small industrial | Feasible |
| 3.0 | 221 | Medium industrial | Feasible |
| 3.714 | 274 | Medium-large industrial | Feasible |
| 4.0 | 295 | Medium-large industrial | Feasible |

**Output:** Binary verdict per velocity point, plus the specific compressor class required.
Flag that this is a feasibility assessment against commercial availability ranges, not a specific
equipment specification. Phase 4 will refine the compressor selection.

---

## 5. Parameter Sweeps: Grid Specification

### Sweep 1: C_D × v_terminal (BUOY-03 grid)

Fully factorial: 5 C_D values × 3 F_chain values = 15 combinations.
Each combination requires exactly 1–3 iterations of the fixed-point formula.

| C_D values | 0.8, 0.9, 1.0, 1.1, 1.2 |
|------------|-------------------------|
| F_chain values (N) | 0, 200, 500 |
| Total points | 15 |
| Output | v_terminal, Re, iteration count |

### Sweep 2: eta_c × W_pump (THRM-01 grid)

5 eta_c values, no interactions with other sweeps.

| eta_c values | 0.65, 0.70, 0.75, 0.80, 0.85 |
|-------------|------------------------------|
| Total points | 5 |
| Output | W_pump (J), W_pump (kJ), COP_ideal_max |

### Sweep 3: v_vessel × Fill (FILL-01/02 grid)

5 velocity values spanning the terminal velocity range from BUOY-03.

| v_vessel values (m/s) | 2.0, 2.5, 3.0, 3.5, 4.0 |
|-----------------------|--------------------------|
| Additional points | v_terminal values from each BUOY-03 C_D case |
| Total baseline points | 5 + up to 5 terminal velocity points |
| Output | t_fill, Q_depth (m³/s, CFM), Q_free (SCFM) |

---

## 6. Pre-Production Sanity Checks

Execute ALL of these before any parameter sweep. Each should take < 1 second total.

### Check 1: Pressure Profile Endpoints

Verify that P(z) formula produces correct boundary values.

```python
P_0 = P_atm + rho_w * g * (H - 0)    # should be 280,500 Pa
P_H = P_atm + rho_w * g * (H - H)    # should be 101,325 Pa
assert abs(P_0 - 280500) < 100, f"P(z=0) = {P_0}, expected 280500"
assert P_H == P_atm, f"P(z=H) = {P_H}, expected {P_atm}"
```

Expected: P(0) = 280,500 Pa ± 100 Pa; P(H) = 101,325 Pa exactly.

### Check 2: Volume Profile Endpoints

```python
V_0 = V_surface * P_atm / P_bottom    # should be 0.07228 m³
V_H = V_surface * P_atm / P_atm       # should be 0.2002 m³ (= V_surface)
assert abs(V_0 - 0.07228) < 0.0001, f"V(z=0) = {V_0}"
assert V_H == V_surface, f"V(z=H) = {V_H}"
```

Expected: V(0) = 0.07228 m³ ± 0.0001 m³; V(H) = V_surface = 0.2002 m³.

### Check 3: W_iso Closed-Form Value

```python
W_iso_calc = P_atm * V_surface * math.log(P_r)
assert abs(W_iso_calc - 20640) < 21, f"W_iso = {W_iso_calc:.1f} J"
```

Expected: 20,640 J ± 21 J (0.1%).

### Check 4: Constant-Volume Anti-Pattern Sentinel

Compute the WRONG result explicitly to confirm the error magnitude, then confirm the code does NOT use it:

```python
W_wrong = rho_w * g * V_surface * H    # constant-volume error
expected_overestimate = (W_wrong - W_iso) / W_iso
assert 0.70 < expected_overestimate < 0.80, "Sentinel: overestimate should be ~74%"
# This confirms the error magnitude; DO NOT use W_wrong anywhere else
```

Expected: W_wrong = 35,827 J; overestimate ratio = 1.736; error = 73.6%.

### Check 5: Reynolds Number Regime Confirmation

At v = 3.0 m/s (nominal):

```python
Re_nominal = rho_w * 3.0 * d_vessel / nu_w   # kinematic viscosity, not dynamic
# = 998.2 * 3.0 * 0.457 / 1.004e-6 = 1.366e6
assert 1e5 < Re_nominal < 1e7, f"Re = {Re_nominal:.2e} outside expected range"
```

Expected: Re ≈ 1.37 × 10⁶. This confirms the blunt-cylinder C_D = 0.8–1.2 regime applies.

### Check 6: Fill Geometry Cross-Check

```python
arc_length = 2 * math.pi * R_tank / 4
assert abs(arc_length - 5.749) < 0.005, f"arc = {arc_length:.3f} m"
t_fill_3ms = arc_length / 3.0
assert abs(t_fill_3ms - 1.916) < 0.005, f"t_fill at 3 m/s = {t_fill_3ms:.3f} s"
```

Expected: arc = 5.749 m; t_fill at 3 m/s = 1.916 s.

---

## 7. Error Budget and Systematic Uncertainties

All Phase 1 computations are deterministic (no stochastic elements). There is no statistical
uncertainty. All uncertainty is systematic, arising from parameter values and model approximations.

| Error Source | Affected Quantity | Magnitude | How to Handle |
|-------------|------------------|-----------|---------------|
| C_D uncertainty (±0.2) | v_terminal | ±10% on v | Full sweep over C_D ∈ [0.8, 1.2] |
| F_chain unknown | v_terminal | Up to −33% at F_chain=500N | Sensitivity table; flag for Phase 2 |
| Ideal gas assumption | W_iso, W_adia | < 0.1% at P_r = 2.77 | Acceptable; compressibility Z ≈ 1.000 |
| Isothermal ascent assumption | W_buoy | < 5% at 3 m/s | Document as model limitation |
| Loop geometry (circular approx.) | Fill arc, t_fill | ±5% | Note as geometric uncertainty |
| eta_c range (0.65–0.85) | W_pump | ±14% of W_adia | Full sweep over eta_c |
| Pipe friction (compressor delivery) | W_pump_total | +10–20% | Note as add-on factor for Phase 4 |
| rho_w temperature sensitivity | All forces, work | < 0.5% at 20°C ± 5°C | Negligible |

**Dominant uncertainties:** C_D and F_chain dominate v_terminal uncertainty (~±10% and ±33%
respectively). eta_c dominates pump work uncertainty (~±14%). These are all captured by the
parameter sweeps.

**Systematic error in final quoted values:**

- W_iso, W_adia, W_pump: quote as point values ± convergence error (< 0.1%); no free parameters
- v_terminal: quote as range [v(C_D=1.2, F_chain=500), v(C_D=0.8, F_chain=0)] = [2.53, 4.15] m/s
  with nominal at (C_D=1.0, F_chain=0) = 3.71 m/s (upper bound) or (C_D=1.0, F_chain=200) = 3.37 m/s
- Q_required: quote as range corresponding to v_terminal range

---

## 8. Computational Cost Estimate

All Phase 1 computations are extremely cheap. No HPC resources needed.

| Task | N_points | Compute per Point | Total Time | Bottleneck |
|------|----------|------------------|-----------|-----------|
| THRM-01: W_iso, W_adia (closed form) | 1 | < 0.1 ms | < 0.1 ms | None |
| THRM-01: W_pump sweep over eta_c | 5 | < 0.1 ms | < 1 ms | None |
| BUOY-02: scipy.quad buoyancy integral | 2 (tight+loose tolerance) | < 5 ms | < 10 ms | None |
| BUOY-03: terminal velocity iteration | 15 (5 C_D × 3 F_chain) | < 0.1 ms | < 2 ms | None |
| FILL-01/02: fill window sweep | 5–10 | < 0.1 ms | < 1 ms | None |
| Sanity checks (Section 6) | 6 | < 0.1 ms | < 1 ms | None |
| Plotting (P(z), V(z), F_b(z), v vs C_D) | 4 plots | < 200 ms | < 1 s | None |
| **Total** | | | **< 2 s** | **None** |

Budget: < 2 seconds of single-core CPU time. No parallelism needed. No queuing.

The entire Phase 1 computation runs as a single Python script on any laptop.

---

## 9. Execution Order and Dependencies

```
Step 1: Sanity checks (Section 6)          — Run first; halt on any failure
Step 2: THRM-01 compression work           — Closed-form; no dependencies
Step 3: BUOY-02 buoyancy integral          — Requires P(z), V(z) from Step 1 sanity checks
Step 4: BUOY-02 identity gate              — ASSERT |W_buoy - W_iso| / W_iso < 0.01
                                             IF FAILS: stop; do not proceed to Step 5
Step 5: BUOY-03 terminal velocity sweep    — Requires W_iso from Step 2
Step 6: FILL-01/02 fill window & flow rate — Requires v_terminal values from Step 5
Step 7: FILL-03 feasibility assessment     — Requires Q_free from Step 6
Step 8: Generate output tables and plots   — Requires all of Steps 2–7
Step 9: Check all gates; write summary     — Final gate: all checks passed
```

**Hard dependency:** Step 4 must pass before Step 5 runs. This is enforced by a Python
`assert` statement (or `raise ValueError`). If the buoyancy identity gate fails, the pressure
profile or volume formula has an error, and all downstream calculations that use those functions
will also be wrong.

**Soft dependency:** Steps 5–7 depend on v_terminal, which depends on W_iso through F_b_avg.
If W_iso changes significantly (it should not — it is confirmed to < 0.1% in Step 2), the
velocity and fill calculations must be rerun.

---

## 10. Expected Outcomes and Decision Criteria

### Primary Outcomes

| Result | Expected Value | Decision Rule |
|--------|---------------|---------------|
| W_iso = W_buoy identity | Difference < 1% | Pass: proceed to Phase 2. Fail: debug code, DO NOT proceed |
| v_terminal (nominal) | 3.0–3.7 m/s | Pass: within 25% of user estimate; proceed. If < 2.0 m/s: raise design concern |
| Q_free at nominal velocity | 200–280 SCFM | Pass: commercially available. Fail if > 400 SCFM: raise feasibility concern |
| W_pump range | 28–37 kJ | Pass: confirms thermodynamic framing. If W_pump < W_iso: sign error |

### Phase 1 → Phase 2 Handoff Values

The following values are locked by Phase 1 and passed to Phase 2:

| Parameter | Value | Uncertainty | Source |
|-----------|-------|-------------|--------|
| v_vessel (nominal) | 3.71 m/s | ±0.6 m/s (C_D range) | BUOY-03, C_D=1.0, F_chain=0 |
| v_vessel (conservative) | 3.07 m/s | — | BUOY-03, C_D=1.2, F_chain=200 |
| W_iso | 20,640 J | ± 21 J | THRM-01 |
| W_adia | 24,040 J | ± 24 J | THRM-01 |
| W_pump table | 28,188–36,861 J | per eta_c | THRM-01 |
| F_b(z) integrand | Verified | < 1% error | BUOY-02 |

Phase 2 must use v_vessel from this table, not the preliminary 3.0 m/s. If Phase 2's
hydrofoil analysis is sensitive to the ±10% velocity uncertainty, it must sweep over the
v_vessel range [2.5, 4.2] m/s explicitly.

---

## 11. Plots Required

| Plot | x-axis | y-axis (or curves) | Purpose |
|------|--------|-------------------|---------|
| P1-1 | z (m) | P(z) (Pa), V(z) (m³), F_b(z) (N) | Visual sanity check of all three functions; confirm monotone behavior |
| P1-2 | z (m) | F_b(z) (N) with shaded area = W_buoy | Illustrate the buoyancy integral; area should match W_iso annotation |
| P1-3 | C_D | v_terminal (m/s) for F_chain = {0, 200, 500} N | Terminal velocity sensitivity; mark 3.0 m/s reference line |
| P1-4 | eta_c | W_pump (kJ) with W_iso and W_adia reference lines | Pump energy landscape; annotate COP_ideal_max on right axis |

All plots: SI units, labeled axes with units, grid lines on. Save as PNG at 150 dpi minimum.

---

## 12. Suggested Task Breakdown (for planner)

| Task ID | Description | Type | Dependencies | Estimated Complexity |
|---------|-------------|------|-------------|---------------------|
| P1-T1 | Sanity checks + unit conversion validation | validate | none | trivial (< 10 min) |
| P1-T2 | THRM-01: W_iso, W_adia, W_pump table | calc | P1-T1 | small (< 30 min) |
| P1-T3 | BUOY-02: scipy.quad convergence study | validate | P1-T1 | small (< 30 min) |
| P1-T4 | BUOY-02: mandatory identity gate | gate | P1-T3 | trivial (< 5 min) |
| P1-T5 | BUOY-03: terminal velocity sweep | sim | P1-T4 | small (< 30 min) |
| P1-T6 | FILL-01/02/03: fill window and flow rates | calc | P1-T5 | small (< 30 min) |
| P1-T7 | Plots P1-1 through P1-4 | analysis | P1-T2, P1-T5, P1-T6 | small (< 30 min) |
| P1-T8 | Phase 1 summary: lock handoff values | analysis | all | small (< 30 min) |

Total estimated implementation time: 2–4 hours of coding and documentation.
Total estimated computation time: < 2 seconds (see Section 8).

---

## Appendix A: Anti-Pattern Cross-Reference

| Anti-Pattern | PITFALL ID | Detection Condition | Sentinel Value |
|-------------|-----------|--------------------|-|
| Constant-volume buoyancy | C1 | W_buoy > 25,000 J | W_wrong = 35,827 J |
| Gauge pressure in Boyle's law | — | V(z=0) ≠ 0.07228 m³ | V_wrong = 0.2002 * (101325/179175) = 0.1138 m³ |
| Jet recovery double-counting | C6 | Energy balance has both W_buoy and W_jet as separate nonzero terms | Remove W_jet line item |
| Using W_iso as pump energy | M1 | W_pump reported as 20,640 J without eta_c correction | Correct: W_pump ≥ W_adia/0.85 = 28,188 J |
| Unconfirmed v_vessel | C7 | Fill window uses v=3.0 without BUOY-03 result | Run BUOY-03 first |
| Pipe friction omitted | M5 | W_pump_total = W_adia/eta_c only | Add 1.10–1.20 × factor in Phase 4 |

---

## Appendix B: Convention Test Values (CONVENTIONS.md Machine-Readable Subset)

The following values are copied from CONVENTIONS.md for inline verification. Any discrepancy
between these values and CONVENTIONS.md indicates a stale copy; use CONVENTIONS.md as authority.

| Quantity | Value | Formula |
|----------|-------|---------|
| P_bottom | 280,500 Pa | 101325 + 998.2 × 9.807 × 18.288 |
| P_r | 2.7669 | 280500 / 101325 |
| W_iso | 20,640 J | 101325 × 0.2002 × ln(2.7669) |
| W_adia | 24,040 J | 3.5 × 101325 × 0.2002 × (2.7669^0.2857 − 1) |
| V_depth | 0.07228 m³ | 0.2002 / 2.7669 |
| F_b(z=H) | 1,959.8 N | 998.2 × 9.807 × 0.2002 |
| F_b(z=0) | 707.6 N | 998.2 × 9.807 × 0.07228 |
| F_b_avg | 1,128.9 N | 20,640 / 18.288 |
| C_loop | 22.996 m | 2π × 3.66 |
| Fill arc | 5.749 m | 22.996 / 4 |
| t_fill at 3 m/s | 1.916 s | 5.749 / 3.0 |
| Q at 3 m/s | 0.03772 m³/s | 0.07228 / 1.916 |
| Q at 3 m/s | 79.9 CFM@depth | 0.03772 × 2118.88 |
| Q_free at 3 m/s | 221 SCFM | 79.9 × 2.7669 |
| Re at 3 m/s | 1.37 × 10⁶ | 3.0 × 0.457 / 1.004e-6 |

---

_Experiment design prepared: 2026-03-16_
_Conventions version: Phase 0 (2026-03-16, no changes)_
_Research mode: balanced_
_Autonomy: balanced — design written without user checkpoints; no scope changes required_
