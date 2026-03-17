# Conventions Ledger

**Project:** Hydrowheel — Buoyancy + Hydrofoil Energy System
**Created:** 2026-03-16
**Last updated:** 2026-03-16 (project initialization)

> This file is append-only for convention entries. When a convention changes, add a new
> entry with the updated value and mark the old entry as superseded. Never delete entries.

---

## 1. Coordinate System

### Vertical Coordinate

| Field            | Value                                                                                     |
| ---------------- | ----------------------------------------------------------------------------------------- |
| **Convention**   | z = 0 at tank bottom; z = H at water surface; z increases upward                         |
| **Introduced**   | Phase 0 (initialization)                                                                  |
| **Rationale**    | Aligns positive z with the direction of buoyant ascent; makes F_b and v_vessel positive  |
| **Dependencies** | Pressure P(z), buoyancy force F_b(z), buoyancy work integral limits (0 to H)             |
| **Test value**   | P(0) = P_bottom = 280,500 Pa; P(H) = P_atm = 101,325 Pa; dP/dz = -rho_w * g < 0        |

### Pressure Profile

| Field            | Value                                                                                                          |
| ---------------- | -------------------------------------------------------------------------------------------------------------- |
| **Convention**   | P(z) = P_atm + rho_w * g * (H - z); absolute pressure at depth (H - z) below surface                         |
| **Introduced**   | Phase 0 (initialization)                                                                                       |
| **Rationale**    | Hydrostatic formula referenced to coordinate origin at bottom; consistent with z-up convention                 |
| **Dependencies** | V(z) via Boyle's law, F_b(z), buoyancy work integral                                                          |
| **Test value**   | P(0) = 101325 + 998.2 * 9.807 * 18.288 = 280,500 Pa = 2.770 atm; P(H) = P_atm = 101325 Pa                   |

---

## 2. Unit System

### Primary Units

| Field            | Value                                                                                                       |
| ---------------- | ----------------------------------------------------------------------------------------------------------- |
| **Convention**   | SI throughout: meters (m), kilograms (kg), seconds (s), Newtons (N), Joules (J), Watts (W), Pascals (Pa)  |
| **Introduced**   | Phase 0 (initialization)                                                                                    |
| **Rationale**    | Standard engineering units; consistent with fluid mechanics references (Cengel, Hoerner, Schlichting)       |
| **Dependencies** | All force, energy, power, and pressure expressions                                                          |
| **Test value**   | 1 atm = 101325 Pa; g = 9.807 m/s²; 1 ft = 0.3048 m; 1 ft³ = 0.02832 m³                                   |

### Imperial Cross-Checks

| Field            | Value                                                                                                                         |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Convention**   | Imperial values in parentheses for design cross-check only; SI is authoritative for all calculations                         |
| **Introduced**   | Phase 0 (initialization)                                                                                                      |
| **Rationale**    | Physical design specified in feet and inches; cross-checks prevent unit conversion errors                                     |
| **Dependencies** | Geometry inputs (H = 60 ft = 18.288 m; R = 12 ft = 3.66 m; vessel = 4 ft × 18 in)                                          |
| **Test value**   | H = 18.288 m = 60.000 ft; V_surface = 0.2002 m³ = 7.069 ft³; P_bottom = 280,500 Pa = 40.70 psi = 2.770 atm                 |

---

## 3. Fluid Properties

### Water Density

| Field            | Value                                                                               |
| ---------------- | ----------------------------------------------------------------------------------- |
| **Convention**   | rho_w = 998.2 kg/m³ (fresh water at 20 deg C, 1 atm)                               |
| **Introduced**   | Phase 0 (initialization)                                                            |
| **Rationale**    | CRC Handbook value for fresh water at 20 deg C; user specified fresh water only     |
| **Dependencies** | Hydrostatic pressure P(z), buoyancy force F_b, drag forces, Reynolds number         |
| **Test value**   | rho_w * g * H = 998.2 * 9.807 * 18.288 = 179,175 Pa; P_bottom = 101325 + 179175 = 280,500 Pa |

### Gravitational Acceleration

| Field            | Value                                                     |
| ---------------- | --------------------------------------------------------- |
| **Convention**   | g = 9.807 m/s² (standard gravity)                         |
| **Introduced**   | Phase 0 (initialization)                                  |
| **Rationale**    | Standard value; negligible variation at project location  |
| **Dependencies** | Buoyancy force F_b = rho_w * g * V, hydrostatic pressure |
| **Test value**   | F_b on fully buoyant vessel at surface: 998.2 * 9.807 * 0.2002 = 1959 N |

### Kinematic Viscosity of Water

| Field            | Value                                                                         |
| ---------------- | ----------------------------------------------------------------------------- |
| **Convention**   | nu_w = 1.004e-6 m²/s (fresh water at 20 deg C)                               |
| **Introduced**   | Phase 0 (initialization)                                                      |
| **Rationale**    | Required for Reynolds number Re = U * c / nu to determine flow regime         |
| **Dependencies** | Re calculations for hydrofoil selection and drag coefficient lookup           |
| **Test value**   | Re = v_vessel * chord / nu_w = 3.0 * 0.30 / 1.004e-6 = 8.96e5 (turbulent regime) |

### Air Thermodynamics

| Field            | Value                                                                                                           |
| ---------------- | --------------------------------------------------------------------------------------------------------------- |
| **Convention**   | Ideal gas, gamma = 1.4 (diatomic); isothermal work W_iso = P_atm * V_surface * ln(P_r); adiabatic W_adia = [gamma/(gamma-1)] * P_atm * V_surface * [(P_r)^((gamma-1)/gamma) - 1] |
| **Introduced**   | Phase 0 (initialization)                                                                                        |
| **Rationale**    | Air behaves as ideal gas at pressures up to ~3 atm; gamma = 1.4 is standard for dry air                        |
| **Dependencies** | W_pump, buoyancy work equivalence, fill volume at depth                                                         |
| **Test value**   | W_iso = 101325 * 0.2002 * ln(2.770) = 20,640 J; W_adia = 3.5 * 101325 * 0.2002 * (2.770^0.2857 - 1) = 24,040 J |

---

## 4. System Parameters (Locked)

### Water Depth

| Field            | Value                                                              |
| ---------------- | ------------------------------------------------------------------ |
| **Convention**   | H = 18.288 m (60 ft); distance from tank bottom to water surface  |
| **Introduced**   | Phase 0 (initialization)                                           |
| **Rationale**    | User specification; 60 ft fresh water column                       |
| **Dependencies** | Pressure P(z), buoyancy work integral, ascent cycle time           |
| **Test value**   | 60 ft * 0.3048 m/ft = 18.288 m exactly                            |

### Atmospheric Pressure

| Field            | Value                                                       |
| ---------------- | ----------------------------------------------------------- |
| **Convention**   | P_atm = 101,325 Pa (1.000 atm standard atmosphere)         |
| **Introduced**   | Phase 0 (initialization)                                    |
| **Rationale**    | Standard atmosphere; air at surface is at P_atm             |
| **Dependencies** | P_r, all pressure calculations, Boyle's law volume ratios   |
| **Test value**   | P_atm = 101325 Pa = 14.696 psi = 1.000 atm                 |

### Bottom Pressure

| Field            | Value                                                                          |
| ---------------- | ------------------------------------------------------------------------------ |
| **Convention**   | P_bottom = P_atm + rho_w * g * H = 280,500 Pa = 2.770 atm                     |
| **Introduced**   | Phase 0 (initialization)                                                       |
| **Rationale**    | Hydrostatic pressure at tank bottom where air injection occurs                 |
| **Dependencies** | Compression work W_pump, fill volume V_depth, pressure ratio P_r               |
| **Test value**   | 101325 + 998.2 * 9.807 * 18.288 = 280,500 Pa; ratio 280500/101325 = 2.770     |

### Pressure Ratio

| Field            | Value                                                                        |
| ---------------- | ---------------------------------------------------------------------------- |
| **Convention**   | P_r = P_bottom / P_atm = 2.770 (dimensionless)                               |
| **Introduced**   | Phase 0 (initialization)                                                      |
| **Rationale**    | Shorthand for compression ratio appearing throughout thermodynamic formulae  |
| **Dependencies** | W_iso = P_atm * V_surface * ln(P_r); V_depth = V_surface / P_r               |
| **Test value**   | ln(P_r) = ln(2.770) = 1.0188; W_iso = 101325 * 0.2002 * 1.0188 = 20,640 J  |

### Vessel Volume at Surface

| Field            | Value                                                                                          |
| ---------------- | ---------------------------------------------------------------------------------------------- |
| **Convention**   | V_surface = 0.2002 m³ (7.069 ft³); full vessel internal volume = pi * (0.2286)² * 1.219 m     |
| **Introduced**   | Phase 0 (initialization)                                                                       |
| **Rationale**    | Cylinder: diameter 18 in = 0.457 m (radius 0.2286 m), length 4 ft = 1.219 m                  |
| **Dependencies** | Fill target (air expands to exactly V_surface at z = H); compression work W_iso, W_adia       |
| **Test value**   | pi * 0.2286² * 1.219 = pi * 0.05226 * 1.219 = 0.2002 m³ = 7.069 ft³                         |

### Vessel Volume at Depth

| Field            | Value                                                                                    |
| ---------------- | ---------------------------------------------------------------------------------------- |
| **Convention**   | V_depth = V_surface / P_r = V_surface * P_atm / P_bottom = 0.07228 m³ (2.553 ft³)      |
| **Introduced**   | Phase 0 (initialization)                                                                 |
| **Rationale**    | Boyle's law: air injected at P_bottom occupies V_depth; expands to V_surface at surface |
| **Dependencies** | Required fill flow rate, fill window analysis, isothermal expansion during ascent        |
| **Test value**   | V_depth = 0.2002 / 2.770 = 0.07228 m³ = 2.553 ft³                                      |

### Number of Vessels

| Field            | Value                                                                   |
| ---------------- | ----------------------------------------------------------------------- |
| **Convention**   | N_vessels = 30 (10 vessels per vertical loop × 3 loops)                 |
| **Introduced**   | Phase 0 (initialization)                                                |
| **Rationale**    | User specification; approximately 15 ascending, 15 descending at any time |
| **Dependencies** | Total power calculations; fill rate (one vessel injected per loop per cycle) |
| **Test value**   | N_ascending ≈ 15 (half of 30); actual distribution depends on loop geometry |

### Tank Radius

| Field            | Value                                                                    |
| ---------------- | ------------------------------------------------------------------------ |
| **Convention**   | R_tank = 3.66 m (12 ft); inner radius of the cylindrical water tank      |
| **Introduced**   | Phase 0 (initialization)                                                  |
| **Rationale**    | User specification: 24 ft diameter cylinder → radius 12 ft = 3.66 m     |
| **Dependencies** | Loop circumference, co-rotation calculations (P_corot), fill window arc length |
| **Test value**   | Diameter = 2 * 3.66 = 7.32 m = 24.02 ft ≈ 24 ft                         |

### Target Efficiency (COP)

| Field            | Value                                                                                     |
| ---------------- | ----------------------------------------------------------------------------------------- |
| **Convention**   | eta_target = 1.5; system COP = W_shaft_out / W_pump_in must be >= 1.5 for go verdict     |
| **Introduced**   | Phase 0 (initialization)                                                                  |
| **Rationale**    | User-stated project requirement; 1.5 W shaft output per 1 W pumping input                |
| **Dependencies** | Go/no-go decision in Phase 4 system balance                                               |
| **Test value**   | COP = 1.0 for ideal isothermal reversible buoyancy cycle (thermodynamic baseline); must exceed 1.5 with hydrofoil contribution |

### Vessel Velocity (Preliminary)

| Field            | Value                                                                                     |
| ---------------- | ----------------------------------------------------------------------------------------- |
| **Convention**   | v_vessel = 3.0 m/s (to be confirmed in Phase 1 terminal velocity calculation)             |
| **Introduced**   | Phase 0 (initialization)                                                                  |
| **Rationale**    | User estimate from buoyancy analysis; Phase 1 will verify via force balance               |
| **Dependencies** | Fill window duration, hydrofoil lift/drag forces, Re number, cycle time                   |
| **Test value**   | Ascent time = H / v_vessel = 18.288 / 3.0 = 6.096 s (preliminary); to be updated Phase 1 |

---

## 5. Pressure Notation

| Symbol     | Definition                                                                  | Units | Notes                                        |
| ---------- | --------------------------------------------------------------------------- | ----- | -------------------------------------------- |
| P_atm      | Atmospheric pressure = 101,325 Pa                                           | Pa    | Surface air pressure; fixed                  |
| P(z)       | Absolute pressure at height z from tank bottom = P_atm + rho_w * g * (H-z) | Pa    | Hydrostatic; P(0) = P_bottom, P(H) = P_atm  |
| P_bottom   | Absolute pressure at tank bottom = P_atm + rho_w * g * H = 280,500 Pa      | Pa    | Air injection pressure                        |
| P_r        | Pressure ratio = P_bottom / P_atm = 2.770                                   | —     | Dimensionless; compression ratio for pumping |

---

## 6. Volume Notation

| Symbol     | Definition                                                                          | Units | Notes                                            |
| ---------- | ----------------------------------------------------------------------------------- | ----- | ------------------------------------------------ |
| V_surface  | Full vessel internal volume = 0.2002 m³ (7.069 ft³)                                | m³    | Volume of air at surface pressure when full      |
| V(z)       | Air volume at height z = V_surface * P_atm / P(z) (Boyle's law, isothermal)        | m³    | Varies along ascent path; V(0) = V_depth, V(H) = V_surface |
| V_depth    | Air volume injected at tank bottom = V_surface / P_r = 0.07228 m³ (2.553 ft³)      | m³    | Fill target volume at injection depth             |

### Volume Convention Notes

- **Fill target:** Air is injected at depth until V_depth of air (at P_bottom) is in the vessel. During ascent the air expands isothermally so that at the surface V_air = V_surface (vessel exactly full).
- **Open-bottom vessel:** The vessel is open at the bottom; water-air interface moves down as air expands. V(z) is the air volume at height z; the remaining vessel volume (V_surface - V(z)) is water.
- **Do not use constant-volume buoyancy:** The constant-volume approximation F_b × H overestimates buoyancy work by ~74% for this system (P_r = 2.770). Always integrate F_b(z) over z.

---

## 7. Force Notation

### Sign Convention for Forces

| Field            | Value                                                                                                         |
| ---------------- | ------------------------------------------------------------------------------------------------------------- |
| **Convention**   | Positive = in the direction of useful work. Buoyancy F_b is positive (upward = direction of ascent). Drag F_D is positive in magnitude; it enters energy balance with a negative sign (opposes motion). Lift F_L is positive (horizontal, in direction of shaft rotation). |
| **Introduced**   | Phase 0 (initialization)                                                                                      |
| **Rationale**    | Avoids sign ambiguity in multi-force energy balance; positive quantities always benefit the output             |
| **Dependencies** | Energy balance signs: W = integral F_useful * dz for useful forces; W_loss = integral F_loss * ds            |
| **Test value**   | Net work on ascending vessel: W_net = W_buoyancy - W_drag_vertical - W_lift_extraction > 0 for net ascent    |

| Symbol   | Definition                                                                   | Units | Sign                           |
| -------- | ---------------------------------------------------------------------------- | ----- | ------------------------------ |
| F_b(z)   | Buoyancy force on ascending vessel = rho_w * g * V(z) at height z           | N     | Positive (upward)              |
| F_D      | Drag force magnitude on vessel body (hull drag)                              | N     | Positive; opposes motion       |
| F_L      | Hydrofoil lift force magnitude                                               | N     | Positive; perpendicular to v_rel |
| F_net    | Net vertical force on ascending vessel = F_b - F_D,vertical - F_chain       | N     | Positive = net upward          |
| F_chain  | Chain tension coupling ascending to descending vessels                        | N     | Positive = opposes ascent      |

---

## 8. Velocity Notation

| Symbol   | Definition                                                                    | Units | Notes                                             |
| -------- | ----------------------------------------------------------------------------- | ----- | ------------------------------------------------- |
| v_vessel | Vessel speed along the loop path (scalar, preliminary 3.0 m/s)               | m/s   | Magnitude; to be confirmed Phase 1                |
| v_v      | Vertical component of vessel velocity during ascent/descent                   | m/s   | = v_vessel for purely vertical motion             |
| v_h      | Horizontal component of vessel velocity (tangential to loop)                  | m/s   | = omega * R_loop for circular motion              |
| v_rel    | Velocity of vessel relative to surrounding water                              | m/s   | Affected by co-rotation; v_rel = v_vessel if no co-rotation |
| v_rel_h  | Horizontal component of relative velocity between vessel and water            | m/s   | = v_h * (1 - f_corot) where f_corot in [0, 1]    |
| omega    | Angular velocity of vessel orbital motion around the central shaft            | rad/s | omega = v_h / R_loop                              |

### Velocity Convention Notes

- For co-rotation analysis: v_rel_h = v_h * (1 - f_corot) where f_corot = 0 means no co-rotation (full drag), f_corot = 1 means perfect co-rotation (zero horizontal drag).
- Hydrofoil lift and drag depend on v_rel, not v_vessel. In power equations, F_L * v_h and F_D * |v_rel| both use the appropriate velocity component.
- Vertical velocity is preserved under co-rotation (water co-rotates horizontally; vessel still moves vertically relative to water). This is the key physical assumption of the co-rotation benefit.

---

## 9. Energy and Work Notation

### Sign Convention for Energy

| Field            | Value                                                                                                           |
| ---------------- | --------------------------------------------------------------------------------------------------------------- |
| **Convention**   | W > 0 = energy input to system (pumping); W > 0 for work produced by the system (buoyancy, hydrofoil torque) when labeled as output. In the energy balance: COP = sum(W_out) / sum(W_in). |
| **Introduced**   | Phase 0 (initialization)                                                                                        |
| **Rationale**    | Component energy balance requires unambiguous sign for each term; each symbol is defined positive in its natural direction |
| **Dependencies** | System COP calculation, W_buoyancy = W_iso identity check                                                       |
| **Test value**   | Isothermal identity: W_buoyancy = integral_0^H [rho_w * g * V_surface * P_atm / P(z)] dz = P_atm * V_surface * ln(P_r) = W_iso |

| Symbol     | Definition                                                                                              | Units | Sign in Balance |
| ---------- | ------------------------------------------------------------------------------------------------------- | ----- | --------------- |
| W_iso      | Isothermal compression work per vessel = P_atm * V_surface * ln(P_r) = 20,640 J                        | J     | Input (cost)    |
| W_adia     | Adiabatic compression work per vessel = 3.5 * P_atm * V_surface * (P_r^0.2857 - 1) = 24,040 J         | J     | Input (cost)    |
| W_pump     | Actual pumping work per vessel = W_adia / eta_c where eta_c = compressor isentropic efficiency         | J     | Input (cost)    |
| W_buoy     | Buoyancy work extracted per ascending vessel = integral of F_b(z) dz from 0 to H = W_iso (ideal)       | J     | Output (gain)   |
| W_shaft    | Net shaft work extracted per cycle (all vessels, all mechanisms)                                        | J     | Output (net)    |
| W_drag     | Energy lost to hull drag per vessel per pass                                                            | J     | Loss (cost)     |
| W_corot    | Energy cost of maintaining co-rotation of water body                                                    | J     | Loss (cost)     |
| W_foil     | Net work extracted by hydrofoil per vessel pass = (F_L * v_h - F_D * |v_rel|) * cycle_time            | J     | Output (gain)   |
| W_jet      | Work recovered from expanding air jet during ascent (open-bottom nozzle effect)                         | J     | Output (gain)   |

---

## 10. Power Notation

| Symbol     | Definition                                                                                              | Units | Notes                                             |
| ---------- | ------------------------------------------------------------------------------------------------------- | ----- | ------------------------------------------------- |
| P_lift     | Power produced by hydrofoil lift on one vessel = F_L * v_h                                              | W     | Positive = power out                              |
| P_drag     | Power dissipated by hydrofoil profile drag on one vessel = F_D * |v_rel|                                | W     | Positive magnitude; enters balance as loss        |
| P_corot    | Power required to maintain co-rotation of water body (wall friction, Ekman dissipation)                 | W     | Continuous loss; must appear in system balance    |
| P_pump     | Total pumping power input = (W_pump per vessel) * (vessel injection rate)                               | W     | Input; vessel injection rate = N_vessels / cycle_time_total |
| P_shaft    | Net shaft power output (total output minus all losses)                                                   | W     | Target: P_shaft / P_pump >= 1.5                   |

### Power Caution Note

P_corot is an ongoing steady-state cost, not a one-time spin-up cost. It must appear in every cycle of the energy balance. The spin-up energy (Greenspan & Howard) is a separate one-time cost not included in COP.

---

## 11. Hydrofoil Notation

| Symbol   | Definition                                                                                     | Units | Notes                                               |
| -------- | ---------------------------------------------------------------------------------------------- | ----- | --------------------------------------------------- |
| C_L      | Lift coefficient = L / (0.5 * rho_w * v_rel² * A_foil)                                        | —     | 2D (per unit span) or 3D (whole foil); specify which |
| C_D      | Drag coefficient = D / (0.5 * rho_w * v_rel² * A_foil)                                        | —     | Includes profile drag and induced drag              |
| C_L_2D   | 2D section lift coefficient from NACA TR-824 or thin-airfoil theory                            | —     | Thin-airfoil: C_L_2D = 2 * pi * alpha (alpha in rad) |
| C_L_3D   | Finite-span lift coefficient = C_L_2D / (1 + 2/AR) [Prandtl elliptic approximation]           | —     | Valid for AR > 4, attached flow                     |
| C_D_i    | Induced drag coefficient = C_L_3D² / (pi * e * AR); Oswald efficiency e = 0.85-0.95           | —     | Prandtl lifting-line; finite-span penalty           |
| C_D_0    | Profile (zero-lift) drag coefficient from NACA TR-824                                          | —     | ~0.006 for NACA 0012 at Re = 10⁶, alpha = 0         |
| AR       | Aspect ratio = span² / A_foil = span / chord (rectangular foil)                                | —     | Parametric in Phase 2; typical range 2-6 for this system |
| alpha    | Angle of attack in degrees (explicitly state when using radians)                               | deg   | Range 5-10 deg for parametric study                 |
| L_over_D | Lift-to-drag ratio = C_L / C_D; key system performance parameter                               | —     | Parametric range: 5-30 for feasibility envelope     |
| A_foil   | Hydrofoil planform area = span * chord (rectangular approximation)                              | m²    | To be specified in Phase 2                          |
| Re       | Reynolds number = v_rel * chord / nu_w                                                         | —     | Must exceed 3e5 for NACA TR-824 data to apply directly |
| c_chord  | Hydrofoil chord length                                                                          | m     | To be specified in Phase 2                          |

### Hydrofoil Force Equations

Lift force (positive, perpendicular to v_rel):
  L = 0.5 * rho_w * C_L_3D * A_foil * v_rel²

Drag force (positive magnitude, parallel to v_rel, opposing motion):
  D = 0.5 * rho_w * (C_D_0 + C_D_i) * A_foil * v_rel²

Net power from one vessel's foil (positive = power extracted to shaft):
  P_net_foil = F_L * v_h - F_D * |v_rel|
             = D * |v_rel| * [(L/D) * (v_h / |v_rel|) - 1]

Condition for net positive foil extraction: L/D > |v_rel| / v_h

---

## 12. Vessel Geometry

| Symbol      | Definition                                          | Value          | Units |
| ----------- | --------------------------------------------------- | -------------- | ----- |
| d_vessel    | Vessel outer diameter                               | 0.457 m (18 in) | m    |
| L_vessel    | Vessel length                                       | 1.219 m (4 ft) | m     |
| A_frontal   | Frontal (cross-sectional) area = pi/4 * d_vessel²  | 0.1640 m²      | m²    |
| A_lateral   | Lateral (side) area = d_vessel * L_vessel           | 0.557 m²       | m²    |
| C_D_hull    | Hull drag coefficient (blunt cylinder, Re~10⁵-10⁶) | 0.8-1.2        | —     |

---

## 13. Co-Rotation Parameters

| Symbol     | Definition                                                                      | Units | Notes                                              |
| ---------- | ------------------------------------------------------------------------------- | ----- | -------------------------------------------------- |
| f_corot    | Co-rotation fraction in [0, 1]; 0 = no co-rotation, 1 = perfect solid-body     | —     | Sensitivity parameter for Phase 3                  |
| omega_w    | Angular velocity of water body (co-rotation)                                    | rad/s | Goal: omega_w / omega = f_corot                   |
| tau_w      | Wall shear stress from co-rotating water against tank wall                      | Pa    | Determines P_corot                                 |
| C_f        | Turbulent skin friction coefficient at tank wall (Schlichting correlation)      | —     | C_f ≈ 0.074 * Re_wall^(-0.2) for turbulent plate  |

---

## 14. System Energy Balance Structure

### Component Sign Table (per cycle, all vessels)

| Component         | Symbol    | Direction | Enters COP As |
| ----------------- | --------- | --------- | ------------- |
| Air pumping       | W_pump    | In        | Denominator   |
| Buoyancy work     | W_buoy    | Out       | Numerator     |
| Foil torque (asc) | W_foil_up | Out       | Numerator     |
| Foil torque (dsc) | W_foil_dn | Out       | Numerator     |
| Hull drag         | W_drag    | Loss      | Subtract from numerator |
| Foil profile drag | W_D_foil  | Loss      | Subtract from numerator |
| Co-rotation cost  | W_corot   | Loss      | Subtract from numerator |
| Chain friction    | W_friction| Loss      | Subtract from numerator |
| Jet recovery      | W_jet     | Out       | Add to numerator |

COP = (W_buoy + W_foil_up + W_foil_dn + W_jet - W_drag - W_D_foil - W_corot - W_friction) / W_pump

### Mandatory Checks (from METHODS.md)

- **Check 1:** |W_buoy - W_iso| / W_iso < 0.01 (1%). Failure = error in buoyancy integral.
- **Check 2:** Constant-volume buoyancy (F_b * H) must NOT be used. Overestimates by 74%.
- **Check 3:** COP with perfect pump (eta_c = 1), no drag, no losses must approach 1.0 (First Law check).
- **Check 4:** P_corot must appear in every cycle; it is not a one-time cost.

---

## 15. Numerical Factor Registry

Factors whose values are determined by convention choices in this project:

| Factor | Value | Source Convention | Notes |
| ------ | ----- | ----------------- | ----- |
| P_r = P_bottom / P_atm | 2.770 | H = 18.288 m, rho_w = 998.2, g = 9.807 | Compression ratio; all pumping work scales with ln(P_r) |
| V_depth / V_surface | 1 / P_r = 0.361 | Boyle's law + P_r | Fill volume fraction |
| W_adia / W_iso | 1.165 | gamma = 1.4, P_r = 2.770 | Adiabatic penalty factor |
| Constant-volume error | 74% overestimate | (P_r - 1 - ln P_r) / ln P_r | Never use F_b * H |
| 0.5 in lift/drag equations | 0.5 | Dynamic pressure q = 0.5 * rho * v² | Standard aerodynamic convention |
| A_frontal of vessel | 0.1640 m² | pi/4 * (0.457)² | Frontal area for hull drag |

---

## Convention Changes

> No convention changes have occurred. This section will record changes if conventions are updated.

| Change ID | Convention | Old Value | New Value | Changed In | Reason | Conversion |
| --------- | ---------- | --------- | --------- | ---------- | ------ | ---------- |
| (none)    | —          | —         | —         | —          | —      | —          |

---

## Cross-Convention Compatibility Notes

| Convention A | Convention B | Interaction | Factor / Sign | Example |
| ------------ | ------------ | ----------- | ------------- | ------- |
| z = 0 at bottom | P(z) = P_atm + rho_w*g*(H-z) | Pressure decreases as z increases | dP/dz = -rho_w*g < 0 | P(0) = P_bottom (max), P(H) = P_atm (min) |
| z = 0 at bottom | Buoyancy integral limits | Integral from 0 to H for full ascent | dz > 0 upward, F_b > 0 upward | W_buoy = integral_0^H F_b(z) dz > 0 |
| Boyle's law V(z) = V_surface*P_atm/P(z) | F_b(z) = rho_w*g*V(z) | Buoyancy force grows during ascent | F_b increases as P(z) decreases with z | At z=0: F_b = F_b_min; at z=H: F_b = F_b_max |
| Positive lift direction | Orbital rotation direction | Ascending vessel lift must be tangential in the direction of shaft rotation; tacking reverses for descending vessels | Tack flip ensures both up/down vessels produce positive shaft torque | Both ascending and descending vessels contribute to the same rotational sense |
| v_rel in foil equations | Co-rotation fraction f_corot | v_rel_h = v_h*(1-f_corot); v_rel_v = v_v (unchanged) | Vertical relative velocity is preserved under co-rotation | This is the key physics claim of the co-rotation benefit |
| W_buoy = W_iso identity | Thermodynamic check | Holds exactly for ideal isothermal process; any deviation is a numerical error | |W_buoy - W_iso| < 1% required | This is Phase 1 mandatory validation gate |

---

## Machine-Readable Convention Tests

```yaml
convention_tests:
  coordinate_system:
    z_origin: "bottom of tank"
    z_positive: "upward"
    z_surface: "H = 18.288 m"
    test: "P(z=0) = 280500 Pa; P(z=H) = 101325 Pa; P(z=H/2) = (280500+101325)/2 = 190913 Pa"

  pressure_profile:
    formula: "P(z) = P_atm + rho_w * g * (H - z)"
    P_atm_Pa: 101325
    rho_w_kg_m3: 998.2
    g_m_s2: 9.807
    H_m: 18.288
    P_bottom_Pa: 280500
    P_r: 2.770
    test: "101325 + 998.2*9.807*18.288 = 280500 Pa; P_r = 280500/101325 = 2.770"

  unit_system:
    primary: "SI"
    length: "meters"
    mass: "kg"
    time: "s"
    force: "N"
    energy: "J"
    power: "W"
    pressure: "Pa"
    imperial_crosscheck: "parenthetical only; SI authoritative"
    test: "1 ft = 0.3048 m; 1 ft^3 = 0.02832 m^3; 1 psi = 6894.76 Pa; 1 atm = 101325 Pa"

  water_properties:
    rho_w: 998.2
    rho_w_units: "kg/m^3"
    nu_w: 1.004e-6
    nu_w_units: "m^2/s"
    temperature: "20 deg C"
    g: 9.807
    g_units: "m/s^2"
    test: "rho_w*g*H = 998.2*9.807*18.288 = 179175 Pa; P_bottom = 101325+179175 = 280500 Pa"

  vessel_geometry:
    V_surface_m3: 0.2002
    V_surface_ft3: 7.069
    V_depth_m3: 0.07228
    V_depth_ft3: 2.553
    d_vessel_m: 0.457
    L_vessel_m: 1.219
    A_frontal_m2: 0.1640
    test: "pi*(0.2286)^2*1.219 = 0.2002 m^3; V_depth = 0.2002/2.770 = 0.07228 m^3"

  system_parameters:
    H_m: 18.288
    P_atm_Pa: 101325
    P_bottom_Pa: 280500
    P_r: 2.770
    N_vessels: 30
    R_tank_m: 3.66
    v_vessel_m_s: 3.0
    v_vessel_status: "preliminary; to be confirmed Phase 1"
    eta_target: 1.5

  thermodynamic_work:
    W_iso_J: 20640
    W_adia_J: 24040
    gamma_air: 1.4
    formula_iso: "P_atm * V_surface * ln(P_r)"
    formula_adia: "3.5 * P_atm * V_surface * (P_r^0.2857 - 1)"
    test: "101325*0.2002*ln(2.770) = 101325*0.2002*1.0188 = 20640 J"

  buoyancy_integral_identity:
    W_buoy_equals_W_iso: true
    tolerance: 0.01
    formula: "integral_0^H rho_w*g*V_surface*P_atm/P(z) dz = P_atm*V_surface*ln(P_r)"
    constant_volume_error: "74 percent overestimate; never use F_b*H"
    test: "Numerically integrate F_b(z) from 0 to H; result must equal 20640 J within 1%"

  force_sign_convention:
    F_b: "positive upward (direction of useful work)"
    F_D: "positive magnitude; opposes motion; enters energy balance as loss"
    F_L: "positive in direction of shaft rotation; perpendicular to v_rel"
    test: "Net work on ascending vessel W_net = W_buoy - W_drag - W_chain; must be positive for ascent"

  energy_sign_convention:
    W_pump: "input; denominator of COP"
    W_buoy: "output; numerator of COP"
    W_foil: "output if positive; loss if negative"
    W_drag: "loss; subtracted from numerator"
    W_corot: "ongoing loss; must appear every cycle"
    COP_formula: "(W_buoy + W_foil_up + W_foil_dn + W_jet - W_drag - W_corot - W_friction) / W_pump"
    test: "COP = 1.0 for ideal isothermal, no drag, no losses (First Law check)"

  hydrofoil_equations:
    lift: "L = 0.5 * rho_w * C_L_3D * A_foil * v_rel^2"
    drag: "D = 0.5 * rho_w * (C_D_0 + C_D_i) * A_foil * v_rel^2"
    net_power: "P_net = F_L * v_h - F_D * |v_rel|"
    net_positive_condition: "L/D > |v_rel| / v_h"
    prandtl_3d: "C_L_3D = C_L_2D / (1 + 2/AR)"
    induced_drag: "C_D_i = C_L_3D^2 / (pi * e * AR)"
    test: "NACA 0012 at Re=10^6, alpha=8 deg: C_L_2D=0.86, C_D=0.011, L/D=78 (NACA TR-824)"
```

---

_Conventions ledger created: 2026-03-16_
_Last updated: 2026-03-16 (Phase 0 — project initialization)_
