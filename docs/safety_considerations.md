# Safety Considerations

## High Voltage Warning

> **DANGER: LETHAL VOLTAGES** — This circuit operates at 450V+ DC. Contact with voltages above 50V DC can cause fatal electrocution. All work on this circuit must be performed by qualified electrical engineers following appropriate safety standards and procedures.

---

## 1. Protection Layers (Defense in Depth)

The circuit implements multiple independent safety layers:

### Layer 1: MOV (Metal Oxide Varistor) — First Response
- **Response time:** <1ns (fastest element)
- **Function:** Clamps fast transients and voltage spikes above 480V
- **Limitation:** Cannot absorb sustained overvoltage (energy limited)
- **Component:** MOV1 — 480V, 40kA surge rating (e.g., Littelfuse V480LA40A)
- **Key specification:** Energy rating must exceed expected transient energy

### Layer 2: TL431 + SCR Crowbar — Primary Protection
- **Response time:** <100µs (TL431 + gate driver + SCR turn-on)
- **Function:** Detects sustained overvoltage and permanently shorts the bus
- **Coordination:** SCR latches on, forcing the fuse to blow
- **Key specification:** SCR must survive until fuse clears

### Layer 3: Fuse — Interruption
- **Response time:** 1–10ms (depends on fault current magnitude)
- **Function:** Limits and interrupts line energy feeding the rectifier/crowbar path
- **Type:** One fast-acting fuse per AC phase (F1A/F1B/F1C, 3A class)
- **Key specification:** AC voltage + interrupt rating and I^2t must match inrush/fault profile

---

## 2. Specific Safety Mechanisms

### 2.1 SCR dv/dt Protection (Snubber)

**Risk:** Fast voltage transients can cause false SCR triggering through junction capacitance displacement current.

**Mitigation:** RC snubber (R9 = 47Ω, C2 = 0.47µF, 630V) limits dv/dt to <21V/µs, well below typical SCR dv/dt ratings of 200–500V/µs.

**Component requirements:**
- C2 must be rated for full bus voltage (630V minimum for 450V bus)
- R9 must handle snubber energy dissipation: P = ½CV²f
- Use film capacitor (not ceramic) for snubber application — self-healing property

### 2.2 Gate Noise Immunity

**Risk:** Electromagnetic noise, ground bounce, or coupled transients on gate wiring can cause spurious SCR firing.

**Mitigation:**
- R8 (100Ω) gate-cathode shunt: provides a low-impedance path to hold the gate low during normal operation. Any noise-induced gate current must exceed I_GT × (1 + R8/R_gate_equiv) to trigger.
- C3 (1nF) on sensing divider: filters HF noise from the voltage sensing path, preventing false TL431 activation.
- Gate wiring should be twisted pair or shielded, kept short, and routed away from power conductors.

### 2.3 Gate Overvoltage Protection

**Risk:** During crowbar activation, transient voltage spikes could damage the SCR gate-cathode junction (typically rated 10–20V).

**Mitigation:** ZD3 (15V zener) clamps the gate voltage to a safe level. This also protects against failure of the PNP driver transistor (Q1) shorting V_local to the gate.

### 2.4 Driver Transistor Protection

**Risk:** When TL431 activates, the PNP base-emitter voltage could reach 12.5V (V_local - V_TL431_cathode), exceeding the 5V maximum V_EB rating.

**Mitigation:** ZD2 (5.1V zener) clamps the base-emitter voltage to 5.1V, protecting Q1 while still providing sufficient base drive for full saturation.

### 2.5 Voltage Derating on Resistors

**Risk:** Individual resistors have maximum voltage ratings (typically 200–500V for standard sizes). The 450V bus exceeds single-resistor ratings.

**Mitigation:**
- R1 split into R1a + R1b (910kΩ each): each sees <225V
- R3 split into R3 + R4 (47kΩ each): each sees <225V
- Adequate creepage and clearance distances on PCB (>4mm for 450V per IEC 60664-1)

### 2.6 Fuse-SCR Coordination

**Risk:** If the fuse is too slow or the SCR is too small, the SCR junction temperature could exceed maximum during the fault, causing SCR failure (open circuit) before the fuse clears — leaving the load unprotected.

**Mitigation:**
- Validate per-phase fuse clearing I^2t against SCR1 surge capability
- Include capacitor charging pulse stress from the 1000uF output capacitor
- Use line fuses with published pre-arcing/clearing curves
- Verify with measured fault waveforms on hardware

### 2.7 Output Isolation SCR (SCR2) Behavior

**Risk:** Without output isolation, the high-energy output capacitor can discharge back
through the crowbar path, increasing SCR1 stress and reducing hold-up at the load.

**Mitigation:** Use the second SCR in the dual module as a diode-connected
forward element from rectifier bus to output bus. This blocks reverse current from
the 600V/1000uF capacitor into the crowbar node after SCR1 fires.

---

## 3. Failure Mode Analysis

| Component Failure | Mode | Effect | Mitigation |
|-------------------|------|--------|------------|
| R1a/R1b open | Sensing lost | TL431 always OFF; no OV protection | Redundant monitoring / alarm circuit |
| R2 short | Ref node = 0V | TL431 always OFF; no OV protection | Use precision resistor; periodic testing |
| TL431 short (C-A) | Always conducting | SCR fires immediately (false trip) | Annoyance (load disconnected), not dangerous |
| TL431 open | Never conducts | No OV protection | Redundant monitoring |
| Q1 short (C-E) | Permanent gate drive | SCR fires immediately (false trip) | Not dangerous — protective action |
| Q1 open | No gate drive | No OV protection | Redundant monitoring |
| SCR1 short | Always crowbarred | Input fuses open / no output | Safe-fail but no service |
| SCR1 open | Cannot crowbar | No OV protection | Redundant monitor / diagnostic |
| SCR2 short | No reverse isolation | Output capacitor can dump into crowbar | Validate thermal/fuse stress, monitor |
| SCR2 open | No output charging | Load undervoltage / no output | Fault detection on output bus |
| Any phase fuse open | Reduced/failed rectification | Low DC output, high ripple | Per-phase fuse monitoring |
| MOV degraded | Clamping voltage rises | Reduced transient protection; crowbar handles it | MOV health monitoring; periodic replacement |
| ZD1 short | V_local = 0 | No gate drive; OV protection lost | Redundant monitoring |
| Snubber C2 short | Bus shorted through R9 | R9 dissipates 450²/47 = 4.3kW → fails | Use self-healing film capacitor; fuse protection |

### Critical Single Points of Failure

1. **TL431 failure (open)** — Eliminates overvoltage detection
2. **SCR failure (open)** — Eliminates crowbar action
3. **Sensing resistor chain open** — Eliminates voltage monitoring

**Recommended redundancy for critical applications:**
- Dual-redundant sensing chains with independent TL431 devices
- Parallel SCRs for firing reliability
- Independent overvoltage monitor with alarm output

---

## 4. PCB Design Guidelines

### Creepage and Clearance

Per IEC 60664-1 for 450V DC, Pollution Degree 2:

| Parameter | Minimum Distance |
|-----------|-----------------|
| Clearance (air gap) | 4.0mm |
| Creepage (surface) | 5.0mm |
| Slot width (if slotted) | 1.0mm |

### Layout Guidelines

1. **Separate HV and LV zones** — Keep the 450V power path physically separated from the sensing/control circuitry. Use board cutouts or creepage slots.

2. **Wide traces for SCR path** — The SCR anode-to-fuse trace must carry >4,000A surge current. Use heavy copper (4oz+) or bus bars.

3. **Star ground** — Single point ground for the sensing divider, TL431, gate driver, and SCR cathode to prevent ground loops.

4. **Short gate wiring** — Keep the PNP collector → R7 → SCR gate → R8 → SCR cathode path as short as possible. Long gate traces pick up noise.

5. **Thermal management** — R3/R4 (0.8W each) need adequate copper area or elevated pad. The SCR requires a properly rated heat sink for continuous operation (though in crowbar use it only conducts briefly).

---

## 5. Testing Procedures

### Pre-Commissioning Checks

1. **Visual inspection** — Verify component placement, solder joints, creepage distances
2. **Resistance checks** — Measure R1 chain (1.82MΩ), R2+VR1 (~10kΩ), R3+R4 (94kΩ)
3. **Zener voltages** — Verify ZD1 (15V), ZD2 (5.1V), ZD3 (15V) with bench supply
4. **Gate circuit** — With power off, verify SCR gate-cathode shunt (R8 = 100Ω)

### Low-Voltage Functional Test

1. Use a variable bench supply (0–30V) to test the sensing/control chain
2. Scale the trigger point: for a 30V supply, set R2 to trigger at ~30V equivalent
3. Verify TL431 activation, PNP turn-on, and gate voltage appearance

### Full-Voltage Test (QUALIFIED PERSONNEL ONLY)

1. Use a current-limited HV supply
2. Slowly ramp voltage while monitoring bus voltage and SCR gate
3. Verify trigger point matches calculated value (±2%)
4. Verify fuse clears and SCR survives

---

## 6. Applicable Standards

- **IEC 61010-1** — Safety requirements for electrical equipment
- **IEC 60664-1** — Insulation coordination (creepage/clearance)
- **UL 508** — Industrial control equipment
- **IEC 60269-4** — Fuses for semiconductor protection
- **IEC 60747-6** — Thyristor (SCR) specifications
