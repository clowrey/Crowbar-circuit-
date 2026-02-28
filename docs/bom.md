# Bill of Materials (BOM)

## Crowbar Overvoltage Protection Circuit — 450V / 250A

| Ref | Qty | Description | Value | Rating | Package | Example Part Number | Notes |
|-----|-----|-------------|-------|--------|---------|-------------------|-------|
| **Power Stage** |
| SCR1 | 1 | Thyristor (SCR), 250A | — | 1600V, 250A | Hockey puck / stud | Vishay VS-T7201630 | I_TSM ≥ 5,000A; mount on heat sink |
| F1 | 1 | Semiconductor fuse, fast-acting | 300A | 500VDC | Blade / bolt-on | Bussmann FWH-300A | DC-rated; I²t < SCR I²t |
| MOV1 | 1 | Metal oxide varistor | 480V | 40kA surge | Disc, 40mm | Littelfuse V480LA40A | Clamp voltage ~800V at 100A |
| **Snubber** |
| R9 | 1 | Power resistor | 47Ω | 5W | Wirewound / TO-220 | Ohmite 45F47RE | Non-inductive preferred |
| C2 | 1 | Film capacitor | 0.47µF | 630VDC | Film, radial | WIMA MKP10 0.47µF/630V | Polypropylene, self-healing |
| **Voltage Sensing** |
| R1a | 1 | Metal film resistor | 910kΩ | ½W | Through-hole / 1206 | Vishay MRS25 910kΩ | 1% tolerance, ≤200V rated |
| R1b | 1 | Metal film resistor | 910kΩ | ½W | Through-hole / 1206 | Vishay MRS25 910kΩ | 1% tolerance, ≤200V rated |
| R2 | 1 | Metal film resistor | 10kΩ | ¼W | Through-hole / 0805 | — | 1% tolerance |
| VR1 | 1 | Trimmer potentiometer | 1kΩ | — | Multi-turn, top-adj | Bourns 3296W-1-102LF | 25-turn for fine adjustment |
| C3 | 1 | Ceramic capacitor | 1nF | 50V | 0805 / through-hole | — | C0G/NP0 dielectric preferred |
| **Local Power Supply** |
| R3 | 1 | Metal oxide resistor | 47kΩ | 2W | Through-hole | — | Voltage-rated for >250V |
| R4 | 1 | Metal oxide resistor | 47kΩ | 2W | Through-hole | — | Voltage-rated for >250V |
| ZD1 | 1 | Zener diode | 15V | 1W | DO-41 | 1N4744A | 15V ±5% |
| C1 | 1 | Electrolytic capacitor | 1µF | 25V | Radial | — | Low ESR; or use 10µF for margin |
| C4 | 1 | Ceramic capacitor | 100nF | 25V | 0805 / through-hole | — | X7R or better |
| **TL431 Voltage Reference** |
| U1 | 1 | Programmable shunt regulator | TL431A | 36V max | SOT-23 or TO-92 | TL431ACLP / TL431AILP | 2.495V ±0.5% (A grade) |
| R5 | 1 | Metal film resistor | 1kΩ | ¼W | 0805 / through-hole | — | Cathode pull-up |
| **PNP Gate Driver** |
| Q1 | 1 | PNP transistor | — | 40V, 0.6A | TO-39 / TO-92 | 2N2905A / 2N3906 | hFE ≥ 100 at I_C = 100mA |
| R6 | 1 | Metal film resistor | 1kΩ | ¼W | 0805 / through-hole | — | Base current limiter |
| ZD2 | 1 | Zener diode | 5.1V | 500mW | DO-35 | 1N4733A / BZX79-C5V1 | V_EB clamp for Q1 |
| **SCR Gate Protection** |
| R7 | 1 | Metal film resistor | 47Ω | ½W | Through-hole | — | Gate current limiter |
| R8 | 1 | Metal film resistor | 100Ω | ½W | Through-hole | — | Gate-cathode shunt |
| ZD3 | 1 | Zener diode | 15V | 1W | DO-41 | 1N4744A | Gate overvoltage clamp |

---

## Component Count Summary

| Category | Count |
|----------|-------|
| Resistors | 9 (+ 1 trimmer) |
| Capacitors | 4 |
| Diodes/Zeners | 3 |
| Transistors | 1 (PNP) |
| ICs | 1 (TL431) |
| SCR | 1 |
| Fuse | 1 |
| MOV | 1 |
| **Total** | **21 components** |

---

## Critical Sourcing Notes

1. **SCR (SCR1):** Must be sourced from major semiconductor distributors (Mouser, Digi-Key, Farnell). Verify V_DRM ≥ 600V (800V+ recommended), I_T(AV) = 250A, and I_TSM > fuse I²t. Avoid counterfeit parts — source only from authorized distributors.

2. **Fuse (F1):** Must be specifically rated for DC operation at ≥450V. Standard AC fuses cannot safely interrupt DC arcs. Use semiconductor-grade fuses (Bussmann FWH, Littelfuse KLKD, or equivalent).

3. **MOV (MOV1):** Select clamping voltage carefully. Too low → MOV absorbs energy during normal operation and degrades. Too high → inadequate transient protection. Target: V_clamp ≈ 1.4× to 1.7× of clamping voltage at rated surge current.

4. **Snubber Capacitor (C2):** Must be a film type (polypropylene preferred) rated for the full bus voltage with margin. Do not use ceramic capacitors in snubber applications — they lack self-healing capability and can fail short.

5. **High-voltage resistors (R1a, R1b, R3, R4):** Verify individual component voltage ratings. Standard 0805 ceramics are typically rated to 150V. Use through-hole metal film or metal oxide resistors rated for ≥300V, or use additional series resistors.
