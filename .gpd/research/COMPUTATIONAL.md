# Computational Approaches

**Project:** Hydrowheel — Buoyancy + Hydrofoil Energy System
**Physics Domain:** Fluid mechanics, thermodynamics, hydrofoil hydrodynamics
**Researched:** 2026-03-16
**Note:** WebSearch unavailable; assessment based on established computational engineering knowledge. [TRAINING-KNOWLEDGE] markers indicate values that should be verified.

---

## Recommended Software Stack

### Primary Tools

| Tool | Purpose | Why | Confidence |
|------|---------|-----|------------|
| Python 3.10+ with numpy/scipy/matplotlib | Energy balance, numerical integration, parameter sweeps, plots | Free, desktop, standard scientific stack | HIGH |
| XFOIL 6.99 | 2D hydrofoil section polars (C_L, C_D vs. α) | Industry-standard panel + integral BL; validated Re 10⁴–10⁷; seconds on desktop; free | HIGH |
| XFLR5 (optional) | Finite-wing 3D vortex-lattice analysis | If hydrofoil AR < 5; GUI wrapper around XFOIL + VLM | MEDIUM |

### Anti-Approaches (Do Not Use)

| Anti-Approach | Why Avoid | What to Use Instead |
|---------------|-----------|---------------------|
| Full 3D CFD (OpenFOAM, Fluent) for hydrofoil | Days per run on desktop; overkill for feasibility | XFOIL 2D polars + analytical finite-span correction |
| Monte Carlo uncertainty propagation at first pass | Premature; adds complexity without changing go/no-go verdict | First-order Taylor propagation after central-value calculation |
| Direct N-S for full buoyancy loop (all 30 vessels) | Computationally prohibitive | Quasi-steady per-vessel analytical model |

---

## Algorithm Specifications

### 1. XFOIL Hydrofoil Section Polar

**Purpose:** C_L(α), C_D(α) for chosen section in water at Re ~ 4×10⁵–10⁶.

**Setup:**
```
Re = ρ_water × V × c / μ_water
At V = 3 m/s, c = 0.15 m: Re ≈ 4.5×10⁵
At V = 3 m/s, c = 0.30 m: Re ≈ 9×10⁵
Mach = 0 (M = 3/1480 ≈ 0.002 — fully incompressible)
N-factor: 7–9 for moderate turbulence
α sweep: −10° to +15° in 0.5° increments
```

**Convergence criterion:** RMSDEF < 1×10⁻⁴ (XFOIL default). Increase ITER to 100–200 for stubborn points near stall. Flag unconverged points.

**Known failure modes:**
- Laminar separation bubbles at moderate α (5–10°, thin sections): convergence failure. Fix: reduce α step to 0.25°.
- CD underestimated post-stall: do not use results beyond α_stall + 2°.
- Hysteresis near transition: sweep both increasing and decreasing α; flag bistable range.
- N-factor sensitivity: run N = 7, 9, 11; report spread as uncertainty band.

**Wall time:** < 5 s per polar (any modern desktop). [TRAINING-KNOWLEDGE]

**Validation gate:** NACA 0012 at Re=10⁶, α=0°: C_D ≈ 0.006 ± 15% (Ladson et al. 1988, NASA TM-4074). [TRAINING-KNOWLEDGE]

---

### 2. Finite-Span Correction (Python, 3 lines)

```python
CL_3D = CL_2D / (1 + 2/AR)                        # Prandtl LL, elliptic
CD_induced = CL_3D**2 / (np.pi * oswald_e * AR)    # induced drag
```

Valid for AR > 4, attached flow. No external library needed.

---

### 3. Buoyancy Work Integral (scipy)

```python
import scipy.integrate as si

def P_depth(z, H=18.288, rho=998.2, g=9.807, P_atm=101325):
    return P_atm + rho * g * (H - z)

def F_buoyancy(z, V_surface=0.2002):
    P_atm = 101325
    V_z = V_surface * P_atm / P_depth(z)
    return 998.2 * 9.807 * V_z

W_buoy, err = si.quad(F_buoyancy, 0, 18.288, limit=200)
# Must agree with: P_atm * V_surface * ln(P_bottom/P_atm) to within 0.1%
```

**Convergence:** atol=1e-6 J, rtol=1e-8.

---

### 4. Terminal Velocity (Fixed-Point Iteration)

```python
def terminal_velocity(F_buoy_avg, Cd=1.0, A_frontal=0.164, rho=998.2):
    v = 3.0  # initial guess (m/s)
    for _ in range(100):
        v_new = np.sqrt(2 * F_buoy_avg / (rho * Cd * A_frontal))
        if abs(v_new - v) / v < 1e-6:
            return v_new
        v = v_new
    raise RuntimeError("No convergence")
```

---

### 5. System COP Calculation (Python)

```python
def hydrowheel_cop(L_over_D, eta_pump, co_rot_fraction, v_vessel=3.0,
                   N_vessels=30, chord=0.25, span=0.5):
    # Energy inputs
    W_compress_ideal = P_atm * V_surface * np.log(P_ratio)   # isothermal
    W_compress_real  = W_compress_adiabatic / eta_pump        # real pump
    W_pump_in = W_compress_real * (N_vessels / 2)             # ascending only

    # Buoyancy work (thermodynamic identity)
    W_buoyancy = W_compress_ideal * (N_vessels / 2)

    # Hydrofoil torque
    C_L = lift_coefficient(alpha=7.0, Re=reynolds(v_vessel, chord))
    C_D = C_L / L_over_D
    A_foil = chord * span
    F_lift  = 0.5 * 998.2 * C_L * A_foil * v_vessel**2
    F_drag  = 0.5 * 998.2 * C_D * A_foil * v_vessel**2
    W_foil_per_vessel = (F_lift * v_horizontal - F_drag * v_vessel) * cycle_time

    # Co-rotation maintenance cost
    W_corot = corotation_maintenance_power(co_rot_fraction) * cycle_time

    # Losses
    W_chain_friction = 0.10 * W_buoyancy
    W_hull_drag = hull_drag_work(v_vessel)

    W_output = (W_buoyancy
                + W_foil_per_vessel * N_vessels
                - W_corot
                - W_chain_friction
                - W_hull_drag)

    return W_output / W_pump_in
```

**Validation gate (lossless):** Set C_D = 0, eta_pump = 1.0, co_rot = 0, chain_friction = 0 → COP must converge to W_buoyancy_iso / W_compress_iso ≈ 1.0 ± 0.01%. Assert this before any lossy run.

---

### 6. Parameter Sweep

```python
L_D_vals  = np.linspace(5, 30, 30)
eta_vals  = np.array([0.65, 0.70, 0.75, 0.80, 0.85])
corot_vals = np.linspace(0, 1, 20)

# 30 × 5 × 20 = 3,000 evaluations; < 0.1 s on desktop
results = np.zeros((len(L_D_vals), len(eta_vals), len(corot_vals)))
for i, LD in enumerate(L_D_vals):
    for j, eta in enumerate(eta_vals):
        for k, f in enumerate(corot_vals):
            results[i,j,k] = hydrowheel_cop(LD, eta, f)
```

---

## Convergence Criteria Summary

| Calculation | Criterion | Tolerance |
|-------------|-----------|-----------|
| XFOIL section polar | RMSDEF < 1×10⁻⁴; ITER ≤ 200 | Exclude unconverged α |
| Terminal velocity | Δv/v < 1×10⁻⁶ | < 10 iterations |
| Buoyancy integral | scipy.quad atol=1e-6 J; cross-check vs. ln formula | < 0.1% |
| Lossless COP | Must = W_buoy_iso / W_compress_iso | < 0.01% |
| XFOIL NACA 0012 benchmark | C_D at α=0°, Re=10⁶ within 15% of Ladson et al. | Tool confidence gate |

---

## Resource Estimates

| Calculation | Wall Time | Memory |
|-------------|-----------|--------|
| XFOIL polar (1 foil, 50α, 1 Re) | < 5 s | < 10 MB |
| XFOIL sweep (5 sections × 3 Re) | < 5 min | < 10 MB |
| Python energy balance (single point) | < 1 ms | < 1 MB |
| Parameter sweep (3,000 pts) | < 1 s | < 50 MB |
| XFLR5 3D VLM (if needed) | < 30 s | < 200 MB |

All estimates for 2020+ desktop. [TRAINING-KNOWLEDGE]

---

## Known Numerical Pitfalls

| Issue | Symptom | Fix |
|-------|---------|-----|
| XFOIL convergence failure near stall | "----------" in output | Reduce α step to 0.25°; ITER 200 |
| XFOIL CD underestimate post-stall | CD too low at high α | Use only α < α_stall − 2° |
| Division by zero in COP | NaN output | Assert all denominators > 0 before division |
| Unit mixing (ft vs m, psi vs Pa) | COP >> 10 or << 0.01 | Use SI throughout; add unit assertions |
| Constant-volume buoyancy integral | ~74% overestimate | Always use variable V_air(z) |
| Dimensional mismatch in power | Apparent L/D as efficiency multiplier | Compute P = F·v in each direction separately |

---

## Installation

```bash
# Python scientific stack
pip install numpy scipy matplotlib pandas

# XFOIL 6.99 (Windows)
# Download from: web.mit.edu/drela/Public/web/xfoil/
# Single executable (xfoil.exe); run via subprocess in Python
# No installation required

# XFLR5 (optional, free GUI)
# Download from: xflr5.tech/xflr5.htm
```

---

## Key References

| Reference | Purpose |
|-----------|---------|
| Drela, M. (1989). "XFOIL: An Analysis and Design System for Low Reynolds Number Airfoils." Springer. | XFOIL algorithm and validation scope [TRAINING-KNOWLEDGE] |
| Ladson et al. (1988). NASA TM-4074. | NACA 0012 benchmark for XFOIL validation [TRAINING-KNOWLEDGE] |
| Hoerner, "Fluid-Dynamic Drag," 1965. | Blunt cylinder C_D tables [TRAINING-KNOWLEDGE] |
| Abbott & von Doenhoff (1959). "Theory of Wing Sections." | NACA section data; lifting-line theory [TRAINING-KNOWLEDGE] |
| scipy.integrate.quad documentation | Adaptive quadrature convergence parameters |

---

_Research prepared: 2026-03-16 | Confidence: HIGH for Python/scipy methods; HIGH for XFOIL methodology; MEDIUM for empirical C_D values_
