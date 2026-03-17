# Pitfalls: Hydrowheel Buoyancy Engine

**Domain:** Fluid mechanics, thermodynamics, hydrofoil hydrodynamics, rotating bounded flow
**Prepared:** 2026-03-16
**Confidence:** HIGH for thermodynamic and force-accounting pitfalls (derivable from first principles); MEDIUM for co-rotation magnitude and low-Re hydrofoil behavior

---

## Critical Pitfalls

### PITFALL-C1: Buoyancy Work = Pumping Work in the Ideal Isothermal Case

**What goes wrong:** The buoyancy integral ∫F_b dh over the full 60 ft ascent equals the isothermal pumping work P₁V₁ ln(P₂/P₁) exactly. This is a thermodynamic identity, not a coincidence. Claiming buoyancy as net output double-counts the energy that was put in by the compressor.

**Why:** As the vessel rises and air expands isothermally from V_depth = 2.553 ft³ to V_surface = 7.069 ft³, the work done by the expanding air against the hydrostatic pressure column equals the work done by the compressor to create that pressurized air in the first place. Energy is conserved; the buoyancy work is just the compressor energy returning.

**Specific error for this system:** Using constant-volume buoyancy (F_b = ρ_w × V_vessel × g × h = 441 lb × 60 ft = 26,460 ft·lb = 35.9 kJ) instead of the correct integral overestimates buoyancy work by ~74% compared to the correct integral (20.6 kJ isothermal).

**Warning sign:** Any calculation that shows buoyancy work > pumping energy has an error in the buoyancy integral.

**Prevention:** Always compute the full integral ∫₀^H ρ_w g V_air(h) dh where V_air(h) = V_surface × P_atm / (P_atm + ρ_w g (H-h)). The result equals W_pump (isothermal) to within 1%.

**Phase:** Phase 1 — must establish this identity before Phase 4 system balance.

---

### PITFALL-C2: Hydrofoil L/D Is Force Multiplication, Not Power Multiplication

**What goes wrong:** L/D = 10 means the lift force is 10× the drag force. It does NOT mean the power extracted from lift is 10× the power lost to drag. Power = Force × velocity. The two forces act in perpendicular directions and at different velocity components.

**The velocity triangle:** For a vessel moving with vertical velocity v_v and horizontal velocity v_h:
- Power extracted by lift = F_L × v_h
- Power lost to drag = F_D × √(v_v² + v_h²) ≈ F_D × v_v (when v_v >> v_h)
- Net power gain from foil = F_L × v_h − F_D × v_v = (L/D) × (v_h/v_v) × F_D × v_v − F_D × v_v

For net gain: (L/D) × (v_h/v_v) > 1, which requires v_h to be not negligible compared to v_v.

**Critical point:** Even if the velocity triangle analysis yields apparent net gain, this power must still come from the buoyancy budget. The hydrofoil redirects buoyancy-driven energy into rotation; it does not create new energy. Total shaft power ≤ total buoyancy power.

**Warning sign:** Any analysis that only checks force magnitudes without tracking power (force × velocity) in each direction.

**Prevention:** Use the full power balance: P_shaft = ΣF_tangential × v_tangential − ΣF_drag × v for every vessel at every position around the loop.

**Phase:** Phase 2 — central analysis for hydrofoil torque.

---

### PITFALL-C3: Co-Rotation Transfers Drag to Tank Walls, Does Not Eliminate It

**What goes wrong:** A co-rotating water body reduces the relative horizontal velocity between vessel and water, reducing form drag on vessels. But the angular momentum of the co-rotating water body must be maintained against viscous dissipation at the tank walls. This wall dissipation is a real energy cost that must appear in the system balance.

**Taylor-Couette estimate:** For a 24 ft (7.32 m) diameter cylinder spinning at angular velocity ω, the viscous torque at the walls scales as T_wall ∝ μ × ω × R³ × L. For water (μ = 0.001 Pa·s), this is small but non-zero. The rotating water body also creates Ekman pumping (axial circulation) that dissipates additional energy.

**Warning sign:** Any co-rotation drag reduction claimed without a corresponding co-rotation maintenance cost in the energy balance.

**Prevention:** Compute co-rotation maintenance power P_corot = T_wall × ω and include it as an explicit cost in Phase 4. If P_corot is small relative to the drag savings, co-rotation is beneficial. If comparable, the benefit is reduced or eliminated.

**Phase:** Phase 3 — this cost must be calculated before Phase 4 can close the balance.

---

### PITFALL-C4: Tacking Does Not Add Energy Beyond the Buoyancy Budget

**What goes wrong:** Tacking the hydrofoil on descending vessels so they also contribute torque in the same rotational direction appears to double the torque output. But the descending vessel torque comes from the chain, which is driven by the ascending vessel buoyancy. The ascending vessel must provide force to:
1. Drive the ascending vessel hydrofoil drag
2. Drive the descending vessel hydrofoil drag (via chain tension)
3. Overcome friction and other losses

Adding tacking on the descending side does not add a new energy source — it adds a new energy extraction pathway from the same buoyancy source. Total output is still bounded by total buoyancy input.

**Where tacking DOES help:** Without tacking, descending vessel hydrofoil drag would oppose the descent (requiring more ascending buoyancy to overcome) while producing no useful torque. With tacking, the same drag produces useful torque instead of being pure loss. This is a real improvement — it converts waste drag into useful work — but does not exceed unity efficiency.

**Warning sign:** Calculations that treat ascending and descending vessel torque as independent additive terms without checking whether the descending-side chain tension comes from the ascending-side buoyancy.

**Prevention:** Track chain tension as the coupling variable between ascending and descending sides. Net driving torque = (buoyancy - ascending drag) × r - (descending drag) × r. Tacking reduces the net loss but does not increase the input.

**Phase:** Phase 2 — must be explicit in the tacking torque analysis.

---

### PITFALL-C5: The Heat Pump Analogy Does Not Apply

**What goes wrong:** A heat pump achieves COP > 1 because it moves heat from an external thermal reservoir (the cold source) into the hot sink, using electrical work only to drive the transport. The external reservoir provides "free" energy. This is why COP_HP = Q_hot / W_electric can be 3–5.

**Why it does not apply here:** A buoyancy engine with pumped air has no external energy reservoir. The entire energy cycle is closed:
- Compressor puts energy W_pump into the air
- Air delivers W_buoyancy = W_pump back during ascent (isothermal identity)
- Net energy available for shaft work = W_pump − all losses ≤ W_pump

There is no temperature gradient, pressure gradient, or external field being tapped. The water column's hydrostatic pressure is already fully accounted for in the buoyancy integral identity.

**What would make the analogy valid:** If there were an external driving source — for example, if a river current maintained a horizontal flow through the cylinder that could be harvested by the foils independent of the pumping cycle, or if the vessel structural weight created a net gravitational contribution over a full cycle (it does not for a symmetric loop).

**Warning sign:** Citing the heat pump analogy without identifying the specific external energy reservoir being tapped.

**Prevention:** Before claiming η > 1.0, identify explicitly: what external energy source is providing the extra energy? If none can be identified, the efficiency ceiling is 1.0 by the First Law.

**Phase:** Phase 4 — system balance closure check.

---

### PITFALL-C6: Expanding Air Jet Recovery Is Already Inside the Buoyancy Integral

**What goes wrong:** The expanding air pushes water out the open bottom nozzle during ascent, providing thrust. This is claimed as additional energy recovery on top of buoyancy. But the work done by the expanding air against the hydrostatic pressure of the exiting water IS the buoyancy integral. The "jet thrust" is not separate energy — it is the mechanism by which buoyancy work is delivered to the vessel.

**Clarification:** The shaped nozzle can improve momentum transfer efficiency (convert more of the expansion work into directed thrust vs. turbulent dissipation), but it cannot recover energy that is already accounted for in W_buoyancy.

**Warning sign:** Any energy balance that lists both "buoyancy work" and "jet recovery" as separate line items with non-trivial values for both.

**Prevention:** Choose ONE framework: either treat the vessel as a buoyancy-driven body (forces and work through hydrostatic pressure) OR as a jet-propelled body (momentum from exhaust). They are two views of the same physics. The buoyancy integral is the correct framework for the ascent energy.

**Phase:** Phase 1 — must be resolved before Phase 4 double-counting occurs.

---

### PITFALL-C7: Vessel Velocity Is Not Self-Consistent

**What goes wrong:** 3 m/s is a user estimate. Some power terms scale as v² (drag) and some as v³ (power in drag), so errors in v are not self-canceling. The actual terminal velocity of the ascending vessel depends on the balance of buoyancy, drag (hull + hydrofoil), and chain tension — a coupled system.

**Impact:** If true velocity differs by 20% from 3 m/s, drag power differs by ~44%, and any torque calculations based on velocity are proportionally wrong.

**Prevention:** Derive the self-consistent terminal velocity from the force balance in Phase 1 (BUOY-03) before using v = 3 m/s in Phase 2 hydrofoil calculations.

**Phase:** Phase 1 — calculate terminal velocity; revise Phase 2 inputs if significantly different from 3 m/s.

---

## Moderate Pitfalls

| # | Pitfall | Phase | Risk |
|---|---------|-------|------|
| M1 | Using isothermal work as pump energy without accounting for real pump efficiency (~65–80%) | Phase 1 | Underestimates input by 25–54% |
| M2 | Hydrofoil stall at low Reynolds number (Re < 5×10⁵) — C_L drops sharply, C_D increases | Phase 2 | May reduce L/D by 50%+ for small foil chords |
| M3 | Blockage effects — vessels occupy fraction of 24 ft cylinder cross-section, accelerating local flow and increasing drag | Phase 2/3 | Increases effective drag on all vessels |
| M4 | Neglecting chain/belt mechanical losses (friction, bending, bearing) | Phase 4 | Typically 5–15% of total power |
| M5 | Neglecting the energy cost of filling from ambient air at the surface (compressor inlet losses, pipe friction over 60 ft) | Phase 1 | Adds 10–20% to pump energy |

---

## Minor Pitfalls

| # | Pitfall | Phase |
|---|---------|-------|
| m1 | Sign convention errors in torque direction for tacked vs. un-tacked foil | Phase 2 |
| m2 | Confusing AoA relative to vessel axis vs. AoA relative to flow direction (they differ when vessel has both v_v and v_h) | Phase 2 |
| m3 | Air leakage at open bottom during ascent reducing effective buoyancy | Phase 1 |
| m4 | Water viscosity effects on buoyancy integral at large vessel velocities | Phase 1 |
| m5 | Ignoring the energy stored in the co-rotating water body at startup (one-time cost, not recurring) | Phase 3 |

---

## Phase-Specific Warning Matrix

| Phase | Watch For |
|-------|-----------|
| Phase 1 | Using constant V_air in buoyancy integral (C1); double-counting jet recovery (C6); not deriving self-consistent velocity (C7) |
| Phase 2 | Treating L/D as power ratio instead of force ratio (C2); not tracking power in each direction via velocity triangle (C2); sign errors on tacking torque direction (m1) |
| Phase 3 | Claiming co-rotation drag reduction without computing wall friction cost (C3) |
| Phase 4 | Accepting η > 1 without identifying external energy source (C5); any balance where ascending + descending torque exceeds buoyancy work input (C4) |

---

## Key Self-Consistency Checks

These must pass before Phase 4 closes:

1. **W_buoyancy = W_pump ± 1%** (Phase 1) — if this doesn't hold, the buoyancy integral is wrong
2. **P_shaft ≤ P_buoyancy − P_losses** at every operating point (Phase 4) — if violated, an energy term is missing
3. **Identified external energy source if η > 1.0** (Phase 4) — required by the First Law
4. **Velocity used in Phase 2 matches the self-consistent value from Phase 1** (Phase 1→2 handoff)

---

_Research prepared: 2026-03-16_
_Confidence: HIGH for thermodynamic pitfalls (C1–C6); MEDIUM for co-rotation magnitude (C3) and low-Re hydrofoil behavior (M2)_
