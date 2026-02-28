# Bill of Materials (BOM)

## 3-Phase Crowbar Overvoltage Protection Circuit (450V trip)

| Ref | Qty | Description | Value / Type | Minimum Rating | Example Part Number | Notes |
|-----|-----|-------------|--------------|----------------|---------------------|-------|
| **3-Phase Input + Rectifier** |
| F1A, F1B, F1C | 3 | Phase fuse, fast-acting | 3A | >= 500VAC class (per system) | Bussmann FNQ-R-3 (example) | One fuse per phase feeding bridge |
| D1-D6 | 6 | Rectifier diodes | Ultrafast / bridge diodes | >= 1200V, >= 6A | STTH8R12D or equivalent | 6-pulse 3-phase bridge |
| **Crowbar + Isolation Stage** |
| SCR1 | 1 | Crowbar SCR | High-current thyristor | >= 800V, high ITSM | Module dependent | Anode on rectifier bus, cathode to return |
| SCR2 | 1 | Spare SCR used as diode | Diode-connected SCR | >= 800V, load current capable | Same dual-SCR module | Forward path rectifier bus -> output only |
| MOV1 | 1 | MOV clamp | 480V class | Surge-rated for expected transients | Littelfuse V480LA40A | Across crowbar bus |
| R9 | 1 | Snubber resistor | 47R | >= 5W pulse-capable | Ohmite 45F47RE | Non-inductive preferred |
| C2 | 1 | Snubber capacitor | 0.47uF film | >= 630VDC | WIMA MKP10 0.47uF/630V | Across SCR1 path |
| **Protected Output** |
| C_OUT | 1 | Output electrolytic capacitor | 1000uF | 600V | Vendor-specific HV capacitor | Energy storage after SCR2 isolation |
| R_LOAD | 1 | Load (for simulation) | 330R | Power per use case | Simulation element | Not a fixed hardware BOM item |
| **Voltage Sensing + Driver** |
| R1a, R1b | 2 | Divider upper resistors | 910k each | >= 0.5W, HV-rated | Vishay MRS25 910k | Split for voltage derating |
| R2 | 1 | Divider lower resistor | 10.15k | >= 0.25W | Precision metal film | Sets 450V trip with R1 chain |
| C3 | 1 | Divider noise filter | 1nF | >= 50V | C0G/NP0 preferred | Rejects HF noise |
| R3, R4 | 2 | Local supply drop resistors | 47k each | >= 2W, HV-rated | Metal oxide resistor | Feed TL431 local rail |
| ZD1 | 1 | Local supply zener | 15V | >= 1W | 1N4744A | Local rail clamp |
| C1 | 1 | Local bulk capacitor | 1uF | >= 25V | Electrolytic | Gate-drive energy support |
| C4 | 1 | Local decoupling | 100nF | >= 25V | X7R | HF bypass |
| U1 | 1 | Precision shunt reference | TL431A | Standard TL431 limits | TL431A family | Trip comparator core |
| R5 | 1 | TL431 pull-up | 1k | >= 0.25W | Metal film | Biases TL431 cathode |
| Q1 | 1 | PNP transistor | 2N2905A class | >= 40V, gate-drive current capable | 2N2905A | Drives SCR1 gate |
| R6 | 1 | Q1 base resistor | 1k | >= 0.25W | Metal film | Base current limiting |
| ZD2 | 1 | Q1 V_EB clamp | 5.1V | >= 0.5W | BZX79-C5V1 | Protects PNP base-emitter |
| R7 | 1 | SCR1 gate resistor | 47R | >= 0.5W | Metal film | Gate current limiting |
| R8 | 1 | SCR1 gate-cathode shunt | 100R | >= 0.5W | Metal film | Noise immunity |
| ZD3 | 1 | SCR1 gate clamp | 15V | >= 1W | 1N4744A | SCR gate protection |

---

## Critical Sourcing Notes

1. Use a genuine dual-SCR module so SCR1 (crowbar) and SCR2 (output isolation) share matched voltage/current class and thermal behavior.
2. Validate SCR2 operation when diode-connected in your exact module topology (gate tie method and holding behavior vary by part family).
3. Select per-phase fuses for inrush tolerance of the 1000uF output capacitor and expected line transients.
4. Choose bridge diode surge current rating for capacitor-charging pulses and fault stress during crowbar events.
5. Treat C_OUT as a high-energy component; provide hardware discharge path and service-safe bleed-down procedure.
