# Methods

**Project:** Hydrowheel — Buoyancy + Hydrofoil Energy System
**Physics Domain:** Fluid mechanics, thermodynamics, hydrofoil hydrodynamics, rotating bounded flow
**Researched:** 2026-03-16
**Research Mode:** balanced

---

## Analytical Methods

### 1. Air Compression Work

**Method:** Isothermal and adiabatic bounds from ideal gas law.

**Isothermal (theoretical minimum):**
W_iso = P₁ V₁ ln(P₂/P₁) = P_atm × V_surface × ln(P_depth / P_atm)

At P_depth = 2.770 atm, V_surface = 0.2002 m³:
W_iso = 101,325 × 0.2002 × ln(2.770) = 20,640 J ≈ 20.6 kJ

**Adiabatic (isentropic, γ = 1.4):**
W_adia = [γ/(γ−1)] P₁ V₁ [(P₂/P₁)^((γ−1)/γ) − 1]
= 3.5 × P_atm × V_surface × [(2.770)^0.2857 − 1]
= 3.5 × 20,271 × [1.338 − 1] = 24,040 J ≈ 24.0 kJ

**Real pump (with η_c = 0.70–0.85):**
W_actual = W_adia / η_c ≈ 28–34 kJ per vessel cycle

**When to use each:**
- Isothermal: theoretical floor; use for best-case analysis
- Adiabatic: upper bound for fast compression; use for conservative analysis
- Real pump: use in Phase 4 system balance; treat η_c as a sensitivity parameter

**Validation:** ln formula vs. numerical integration with scipy.integrate.quad must agree to < 0.1%.

---

### 2. Buoyancy Work Integral

**Method:** Exact integral of buoyancy force over ascent path.

F_b(z) = ρ_water × g × V_air(z) where V_air(z) = V_surface × P_atm / P(z)

P(z) = P_atm + ρ_water × g × (H − z) where z is measured upward from bottom

W_buoyancy = ∫₀ᴴ ρ_water × g × V_surface × P_atm / P(z) dz
            = P_atm × V_surface × ln(P_bottom / P_atm)
            = W_isothermal ✓ (thermodynamic identity)

**Critical:** Use this variable-volume integral, NOT the constant-volume approximation F_b × H. The constant-volume formula overestimates buoyancy work by ~74% for this system.

Constant-volume error: ΔW/W = (P_r − 1 − ln P_r) / ln P_r where P_r = 2.770 → ~74% overestimate.

**Validation gate (Phase 1 mandatory):** |W_buoyancy − W_isothermal| / W_isothermal < 1%. If this fails, the buoyancy integral has an error.

---

### 3. Terminal Velocity of Ascending Vessel

**Method:** Force balance at steady state. Solve for v_terminal such that F_net = 0.

F_buoyancy(v) = ρ_water × g × V_air(h) [varies with depth — use average or mid-depth value]
F_drag(v) = ½ × ρ_water × C_D × A_frontal × v²
F_chain(v) = chain coupling to descending vessels [initially set to 0 for solo vessel estimate]

At terminal velocity: F_buoyancy = F_drag + F_chain + W_structure_in_water

**Blunt cylinder drag coefficient:** C_D ≈ 0.8–1.2 at Re ~ 10⁵–10⁶ (empirical; Hoerner "Fluid-Dynamic Drag")
A_frontal = π/4 × (0.457)² = 0.164 m²

**Numerical method:** Fixed-point iteration v_{n+1} = sqrt(2 F_b / (ρ_water C_D A_frontal)). Convergence: |Δv/v| < 10⁻⁶ in < 10 iterations.

**Phase 1 deliverable:** Confirm 3 m/s is achievable under buoyancy force alone; flag if terminal velocity differs significantly.

---

### 4. Hydrofoil Lift and Drag (2D Section)

**Method:** Thin-airfoil theory for first-order estimates; NACA TR-824 empirical data for validation.

**Thin-airfoil theory (2D, inviscid, incompressible):**
C_L = 2π sin α ≈ 2π α (for small α in radians)
At α = 7° = 0.122 rad: C_L ≈ 0.77

**NACA TR-824 data for NACA 0012 at Re = 10⁶ (preferred):**
- α = 5°: C_L = 0.55, C_D = 0.008, L/D = 69
- α = 8°: C_L = 0.86, C_D = 0.011, L/D = 78
- α = 10°: C_L = 1.06, C_D = 0.013, L/D = 82

**Phase 2 approach:** Parametric L/D sweep from 5 to 30 to bound system performance. Do not commit to a single L/D until chord/span geometry is fixed.

**Forces on a single vessel foil:**
L = ½ × ρ_water × C_L × A_foil × v_rel² (horizontal force on ascending vessel)
D = ½ × ρ_water × C_D × A_foil × v_rel² (force opposing vessel motion)

where v_rel = vessel velocity relative to water (affected by co-rotation in Phase 3).

---

### 5. Finite-Span Correction (Prandtl Lifting Line)

**Method:** Elliptic loading approximation.

C_L,3D ≈ C_L,2D / (1 + 2/AR)
C_D,induced = C_L,3D² / (π e AR), Oswald efficiency e = 0.85–0.95

**Validity:** AR > 4, attached flow (α < α_stall). For AR < 4, use XFLR5 vortex-lattice method.

**Implementation:** 3 lines of numpy. No external library required.

---

### 6. Hydrofoil Torque Contribution

**Method:** Power balance via velocity triangle.

For a vessel at position on the loop with vertical velocity v_v and horizontal velocity v_h (= ω × r):
- Power from lift: P_lift = F_L × v_h (lift × horizontal velocity component)
- Power lost to drag: P_drag = F_D × v (drag × total velocity)

Net power from foil = F_L × v_h − F_D × |v| = (L/D) × (v_h / |v|) × F_D × |v| − F_D × |v|
                    = F_D × |v| × [(L/D)(v_h / |v|) − 1]

**Key constraint:** This must be positive for net extraction: L/D > |v| / v_h = √(v_v² + v_h²) / v_h.

**Phase 2 deliverable:** Compute torque vs. L/D curve; identify minimum L/D for net positive contribution.

**Tacking (descending vessels):** Apply same analysis with v_v reversed; confirm torque direction is unchanged (both contribute in same rotational direction).

---

### 7. Co-Rotation Drag Reduction Model

**Method:** Two bounding models.

**Model A — Zero co-rotation (conservative):** Full relative velocity v_h between vessel and water. All horizontal drag present.
F_drag,h = ½ × ρ_water × C_D,lateral × A_lateral × v_h²

**Model B — Full solid-body co-rotation (optimistic):** Water rotates at ω, vessels rotate at ω. Horizontal relative velocity → 0. Horizontal drag → 0. Vertical relative velocity unchanged.

**Model C — Parametric fraction f ∈ [0,1]:** v_rel,h = v_h × (1 − f). Use as sensitivity parameter.

**Steady-state co-rotation maintenance cost (Taylor-Couette, turbulent wall):**
P_corot = T_wall × ω where T_wall ∝ τ_w × 2πR × L × R

Estimate: τ_w = ½ × ρ_water × C_f × (ω R)² where C_f ≈ 0.074 × Re_wall^(−0.2) (turbulent flat plate)
At ω R = 1 m/s, R = 3.66 m, C_f ≈ 0.006: τ_w ≈ 3 Pa; P_corot ≈ τ_w × 2πRL × ωR ≈ 3 × 2π × 3.66 × 18.3 × 1 ≈ 1,263 W

This is an ongoing cost. Must appear explicitly in Phase 4 energy balance.

**Phase 3 deliverable:** P_corot as function of ω; show whether drag reduction savings exceed maintenance cost.

---

### 8. System Energy Balance

**Method:** Component-by-component signed energy accounting.

Per full cycle (all 30 vessels):

Energy In:
- W_pump = W_actual / η_c (per ascending vessel × N_ascending = 15)

Energy Out (shaft work):
- W_buoyancy (ascending side, partial recovery via chain)
- W_foil_torque,ascending = Σ P_lift_ascending × cycle_time
- W_foil_torque_descending = Σ P_lift_descending × cycle_time (tacking)

Energy Lost:
- W_drag_hull (vessel body drag, ascending + descending)
- W_drag_foil (hydrofoil profile drag)
- W_corotation (co-rotation maintenance)
- W_chain_friction (mechanical losses, 5–15% of total)
- W_fill_loss (pipe friction, compressor inlet losses)

**System COP = W_shaft_out / W_pump_in**

**Mandatory check:** W_buoyancy_ascending ≈ W_pump_isothermal ± 1%. If violated, re-check integral.

---

## Validation Strategy

| Check | Expected Result | Tolerance | Phase |
|-------|-----------------|-----------|-------|
| W_buoyancy integral = W_isothermal | Identity, confirmed numerically | < 1% | Phase 1 |
| Terminal velocity from force balance | Within 20% of 3 m/s (if not, revise Phase 2) | ±20% | Phase 1 |
| NACA 0012 at Re=10⁶, α=0°: C_D ≈ 0.006 | From TR-824 | ±15% | Phase 2 |
| Co-rotation benefit > maintenance cost | Determines whether co-rotation helps | Explicit sign | Phase 3 |
| COP (lossless, η_c=1, no drag): should approach 1.0 | First Law check | < 0.01% closure | Phase 4 |
| Full COP ≥ 1.5 | Project go/no-go | Against L/D, η_c range | Phase 4 |

---

## Known Failure Modes

| Method | Failure Mode | Detection | Fix |
|--------|-------------|-----------|-----|
| Buoyancy integral | Using constant volume F_b × H | Result ~74% too high | Always integrate F_b(z) |
| Thin-airfoil theory | Fails at α > 10–12° | C_L plateau or drop | Use NACA TR-824 data; stay below stall |
| Prandtl LL | Fails at AR < 4 | Induced drag underestimated | Use XFLR5 or full VLM |
| Co-rotation model | Claiming zero maintenance cost | Missing wall-friction term | Always include P_corot in balance |
| Velocity triangle | Using only force magnitude, not power | L/D appears as efficiency multiplier | Compute P = F·v in each direction |

---

## References

| Reference | Type | Relevance |
|-----------|------|-----------|
| Abbott & von Doenhoff, "Theory of Wing Sections," Dover, 1959 | Textbook | NACA 2D section data; primary Phase 2 source |
| NACA TR-824, Abbott et al., 1945 (NASA NTRS, free) | Technical report | C_L, C_D tables for NACA profiles at Re = 3×10⁵–9×10⁶ |
| Çengel & Boles, "Thermodynamics," 9th ed. | Textbook | Compression work formulas; isentropic efficiency |
| Anderson, "Fundamentals of Aerodynamics," 5th ed., McGraw-Hill | Textbook | Thin-airfoil theory; Prandtl lifting line |
| Hoerner, "Fluid-Dynamic Drag," 1965 | Handbook | C_D for blunt cylinders at Re~10⁵–10⁶ |
| Schlichting & Gersten, "Boundary Layer Theory," 9th ed. | Textbook | Turbulent skin friction; wall drag estimates |

---

_Research prepared: 2026-03-16 | Confidence: HIGH for analytical methods (first principles); MEDIUM for empirical correlations_
