# Prior Work

**Project:** Hydrowheel — Buoyancy + Hydrofoil Energy System
**Physics Domain:** Fluid mechanics, thermodynamics, hydrofoil hydrodynamics
**Researched:** 2026-03-16
**Research Mode:** balanced
**Note:** WebSearch unavailable; all findings from established physics knowledge. Confidence levels set conservatively. Benchmark values marked [TRAINING-KNOWLEDGE] should be independently verified.

---

## Theoretical Framework

### Governing Theory

| Framework | Scope | Key Equations | Regime of Validity |
|-----------|-------|---------------|--------------------|
| Ideal gas law + isothermal compression | Air compression work at depth | W = P_atm V_0 ln(P_abs/P_atm) | Slow compression relative to thermal equilibration |
| Adiabatic compression | Air compression work, fast pumping | W = [γ/(γ−1)] P_i V_i [(P_f/P_i)^((γ−1)/γ) − 1] | Fast compression, no heat exchange |
| Archimedes / buoyancy | Net upward force on submerged vessel | F_b = ρ_water g V_displaced − W_vessel | Static fluid, dimensions << depth variation |
| Thermodynamic buoyancy work equivalence | Work recovered by ascending air equals isothermal compression work | W_buoyancy = W_compression (isothermal, reversible) | Closed reversible cycle only |
| Kutta-Joukowski theorem | Lift generation on hydrofoil | L = ρ U Γ per unit span | Incompressible, inviscid, steady flow |
| Thin-airfoil theory | Lift coefficient vs. angle of attack | C_L = 2π α (α in radians, thin symmetric foil) | Low AoA, attached flow, incompressible |
| Prandtl lifting-line theory | Finite-span lift and induced drag | C_D,i = C_L²/(π e AR) | Finite-span foil, attached flow, AR > 4 |

### Key System Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Water depth for injection | 60 ft = 18.288 m | Project specification |
| Hydrostatic pressure at 60 ft (fresh water) | 2.770 atm = 280,500 Pa | Confirmed in scoping |
| Fresh water density (20°C) | 998.2 kg/m³ | CRC Handbook |
| Vessel internal volume | 7.069 ft³ = 0.2002 m³ | Calculated from dimensions |
| Vessel velocity | ~3 m/s | Project specification (to be confirmed in Phase 1) |
| Isothermal compression work per vessel | ~20.6 kJ | Project scoping result |
| Adiabatic compression work per vessel | ~24.0 kJ | Project scoping result (γ = 1.4) |
| Target power ratio | 1.5 W output / 1 W pumping | Project requirement |

### Known Limiting Cases

| Limit | Expected Behavior | Reference |
|-------|-------------------|-----------|
| Reversible isothermal buoyancy cycle | W_buoyancy_out = W_compression_in; net COP = 1.0 | Thermodynamic first principles |
| Adiabatic compression, isothermal ascent | W_compression > W_buoyancy; net COP < 1 | Second law |
| Thin foil, high AR, low AoA, Re > 10⁵ | Peak L/D ≈ 60–80 (2D); 20–40 (3D, AR=3–6) | Abbott & von Doenhoff (1959) |
| Low Re < 5×10⁴ | L/D ≈ 10–20; laminar separation | Mueller & DeLaurier (2003) |

---

## Established Results

### Result 1: Thermodynamic Equivalence of Isothermal Compression and Buoyancy Work

**Statement:** For a reversible isothermal compression followed by release and isothermal expansion during ascent, W_buoyancy = W_compression exactly. Net COP = 1.0 for the buoyancy cycle alone.

**Derivation:**
- Isothermal compression work: W_in = P_atm V_0 ln(P_d / P_atm)
- Buoyancy force during ascent: F_b(z) = ρ_water g V(z) where V(z) = V_0 P_atm / P(z) (Boyle's law)
- Buoyancy work integral: W_out = ∫₀ʰ F_b(z) dz = P_atm V_0 ln(P_d / P_atm) = W_in ✓

**Status:** Exact thermodynamic result. Verified numerically in project scoping (20.6 kJ both ways).

**Reference:** Derivable from first principles. Discussed in: Pimm et al., Energy, 41(1), 2012 (underwater CAES context).

**Relevance:** Net output can only come from hydrofoil work — the buoyancy cycle is energy-neutral at best.

**Confidence:** HIGH

---

### Result 2: Adiabatic Compression Penalty at P_r = 2.770

**Statement:** Adiabatic compression work / isothermal = [(P_r^((γ−1)/γ) − 1) × γ/(γ−1)] / ln(P_r) ≈ 1.165 at P_r = 2.770, γ = 1.4.

Project scoping confirms: 24.0 kJ / 20.6 kJ ≈ 1.165. In the adiabatic case, buoyancy recovery is less than input — a 16.5% deficit before any mechanical losses.

**Confidence:** HIGH

---

### Result 3: Real Compressor Efficiency Impact

**Statement:** Single-stage reciprocating/rotary compressors at P_r = 2.770 achieve isentropic efficiency η_c ≈ 0.70–0.85. At η_c = 0.75:
- W_actual = 24.0 kJ / 0.75 ≈ 32.0 kJ per vessel cycle
- Buoyancy recovery: ~20.6 kJ
- Net deficit to break even: ~11.4 kJ per vessel (55% more energy in than out from buoyancy alone)

For 1.5× target: required output = 48.0 kJ per vessel. Hydrofoil must contribute ~27.4 kJ per vessel pass.

At 3 m/s over 18.3 m (cycle time ~6.1 s), this requires average hydrofoil force ~4.5 kN per vessel — a strong constraint on foil area.

**Reference:** Çengel & Boles, "Thermodynamics: An Engineering Approach," Ch. 9.

**Confidence:** HIGH for methodology; MEDIUM for exact η_c (equipment dependent)

---

### Result 4: NACA Hydrofoil Data at Re ~ 10⁶

**Statement:** NACA TR-824 experimental data for NACA 0012 at Re = 10⁶:
- α = 5°: C_L ≈ 0.55, C_D ≈ 0.008, L/D ≈ 69
- α = 8°: C_L ≈ 0.86, C_D ≈ 0.011, L/D ≈ 78
- α = 12°: C_L ≈ 1.20, C_D ≈ 0.016, L/D ≈ 75
- Stall: α ≈ 14–16°; C_L,max ≈ 1.4–1.6

For 3D finite-span foil (Prandtl lifting-line, elliptic loading):
- C_L,3D ≈ C_L,2D × AR/(AR + 2)
- C_D,induced = C_L²/(π e AR), e ≈ 0.85–0.95
- Practical L/D for AR = 2–4: approximately 15–35

**Reference:** Abbott, I.H. & von Doenhoff, A.E., "Theory of Wing Sections," Dover, 1959. NACA TR-824, 1945 (free via NASA NTRS). [TRAINING-KNOWLEDGE]

**Confidence:** HIGH

---

### Result 5: Reynolds Number Regime at 3 m/s in Water

Re = U c / ν = (3.0 m/s × c) / (1.004 × 10⁻⁶ m²/s) = 2.99 × 10⁶ × c

| Chord (m) | Re | Flow regime | Expected C_D (NACA 0012) |
|-----------|----|-----------|----|
| 0.10 | 3 × 10⁵ | Transitional; possible laminar separation | 0.015–0.030 |
| 0.20 | 6 × 10⁵ | Predominantly turbulent | 0.010–0.018 |
| 0.30 | 9 × 10⁵ | Turbulent; standard NACA data valid | 0.008–0.014 |
| 0.45 | 1.35 × 10⁶ | Fully turbulent; favorable regime | 0.007–0.012 |

At chord ≥ 0.30 m, NACA TR-824 data applies directly without low-Re corrections.

**Confidence:** HIGH

---

### Result 6: No Net-Energy Buoyancy Engines in Peer-Reviewed Literature

**Statement:** No peer-reviewed paper has demonstrated a closed-cycle compression-buoyancy system with COP > 1. All proposed "buoyancy wheel" over-unity claims are refuted by the thermodynamic equivalence result (Result 1).

The Hydrowheel is not a perpetual motion claim — it has explicit external energy input (compressor) and proposes net output via hydrofoil work on the water body. This is thermodynamically legitimate if a sufficient external mechanism exists.

**Reference:** Meller (2011) "Buoyancy Driven Power Generation" discusses the equivalence. Pimm et al. (2012) confirms in CAES context. [TRAINING-KNOWLEDGE]

**Confidence:** HIGH

---

### Result 7: Underwater Buoyancy Gliders — Closest Operational Analogue

**Statement:** The Slocum underwater glider uses buoyancy changes to drive vertical motion; fixed wings convert vertical velocity to forward glide. Key parameters: vertical speed ~0.3 m/s; glide angle ~20–35°; whole-vehicle L/D ~3–5.

**Reference:** Webb, D.C., Simonetti, P.J., & Jones, C.P., IEEE J. Ocean. Eng., 26(4), 2001, pp. 447–452. [TRAINING-KNOWLEDGE]

**Relevance:** Operational confirmation that buoyancy-driven vertical velocity + foil lift produces useful work. The Hydrowheel differs: compressed air source (not thermal), shaft torque extraction (not propulsion), much higher speed (3 vs 0.3 m/s).

**Confidence:** HIGH for Webb reference; MEDIUM for direct applicability

---

### Result 8: Co-Rotating Fluid Spin-Up Theory

**Statement:** Spin-up time in turbulent conditions: τ ~ R²/ν_T where ν_T ≈ 10⁻³ to 10⁻² m²/s (turbulent eddy viscosity). For R = 3.66 m: τ ~ 1,300–13,000 s. Steady-state co-rotation is achievable but requires sustained driving against Ekman dissipation at walls — an ongoing loss, not one-time cost.

**Reference:** Greenspan & Howard, J. Fluid Mech. 17(3), 1963, pp. 385–404. Greenspan, "The Theory of Rotating Fluids," Cambridge, 1968. [TRAINING-KNOWLEDGE]

**Confidence:** HIGH for theory; MEDIUM for application to Hydrowheel geometry

---

## Open Problems

1. **Net energy balance at realistic efficiencies** — Whether output/input ≥ 1.5 with real components: unresolved, this project's central question
2. **Achievable co-rotation fraction** — What fraction of solid-body co-rotation is maintained in steady state given vessel motion pattern
3. **Hydrofoil tacking mechanism efficiency** — Dead-angle zones and pitch-reversal drag

---

## Key References

| Reference | Type | Relevance |
|-----------|------|-----------|
| Abbott & von Doenhoff, "Theory of Wing Sections," Dover, 1959 | Textbook/data | Primary NACA C_L, C_D data; Phase 2 hydrofoil design |
| NACA TR-824, 1945 (NASA NTRS) | Technical report | Source foil coefficient tables; free download |
| Çengel & Boles, "Thermodynamics: An Engineering Approach," 9th ed. | Textbook | Compression work; compressor efficiency |
| Schlichting & Gersten, "Boundary Layer Theory," 9th ed., 2017 | Textbook | Viscous drag; BL transition |
| Greenspan & Howard, J. Fluid Mech. 17(3), 1963 | Journal paper | Spin-up theory for co-rotation analysis |
| Webb et al., IEEE J. Ocean. Eng. 26(4), 2001 | Journal paper | Buoyancy glider operational precedent |
| Pimm et al., Energy 41(1), 2012 | Journal paper | Underwater CAES; buoyancy-compression thermodynamics |
| Hoerner, "Fluid-Dynamic Drag," 1965 | Handbook | Practical drag data for blunt cylinders |

---

_Research prepared: 2026-03-16 | Confidence: MEDIUM (no web search; training knowledge only)_
