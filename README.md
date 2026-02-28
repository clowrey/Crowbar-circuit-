# Crowbar Overvoltage Protection Circuit

**450V trigger threshold | TL431 sensing | dual-SCR module usage**

This project models a crowbar overvoltage protector for a 3-phase front end:
- 240V phase-to-phase AC input
- 6-diode rectifier
- 3A fuse on each phase
- SCR1 used as crowbar on the rectifier bus
- SCR2 (same dual-SCR module) used as a diode-connected output isolation device
- 600V / 1000uF output capacitor on the protected DC output

The key refinement is SCR2 isolation: when SCR1 crowbars the rectifier bus, the output capacitor does not discharge backward through the crowbar path.

---

## Block Diagram

![Block Diagram](schematic/block_diagram.svg)

## Detailed Schematic

![Detailed Schematic](schematic/crowbar_schematic.svg)

Note: the ASCII netlist-aligned diagram in `schematic/crowbar_schematic.txt` is the authoritative topology reference for the latest 3-phase/SCR2-isolation refinement.

See also: [schematic/crowbar_schematic.txt](schematic/crowbar_schematic.txt) for the ASCII-art version.

---

## Operating Sequence

1. **Rectification:** 3-phase 240V L-L input is rectified by a 6-diode bridge.
2. **Output charging:** SCR2 (used as a diode) conducts from rectifier bus to `dc_out`, charging the 600V/1000uF output capacitor.
3. **Monitoring:** TL431 divider monitors `dc_out` and compares against 2.495V reference.
4. **Trip:** At approximately 450V output, TL431 drives Q1, which triggers SCR1.
5. **Crowbar action:** SCR1 collapses the rectifier bus (`hv_bus`) to near its forward drop.
6. **Back-discharge prevention:** SCR2 blocks reverse current, so output capacitor energy does not dump through SCR1.

---

## Safety and Protection Features

| # | Feature | Component(s) | Purpose |
|---|---------|--------------|---------|
| 1 | Per-phase input fusing | F1A/F1B/F1C (3A each) | Protect each AC phase feeding rectifier |
| 2 | MOV clamp | MOV1 (480V behavioral model) | Limits high-voltage transients on rectifier bus |
| 3 | RC snubber | R9 + C2 | Limits SCR1 dv/dt and false triggering |
| 4 | Gate shunt | R8 | Improves SCR1 noise immunity |
| 5 | Gate clamp | ZD3 | Protects SCR1 gate from overvoltage |
| 6 | Driver clamp | ZD2 | Limits PNP base-emitter stress |
| 7 | Sensing filter | C3 | Filters high-frequency divider noise |
| 8 | Split HV resistors | R1a/R1b, R3/R4 | Voltage derating across resistor chain |
| 9 | Local supply decoupling | ZD1 + C1 + C4 | Stabilizes TL431/Q1 gate-driver rail |
| 10 | Output isolation by spare SCR | SCR2 (diode-connected model) | Blocks reverse output-capacitor discharge |
| 11 | High-energy output capacitor | C_out (1000uF, 600V) | Holds output during rectifier-bus crowbar |

For additional safety context, see [docs/safety_considerations.md](docs/safety_considerations.md).

---

## Simulation

The netlist in `simulation/crowbar_circuit.cir` now uses:
- 3-phase AC source (240V L-L nominal)
- Per-phase source impedance and 3A fuse ESR
- 6-diode bridge rectifier
- SCR1 crowbar node (`hv_bus`) and isolated output node (`dc_out`)

### Prerequisites

```bash
sudo apt-get install ngspice
pip install matplotlib numpy
```

### Run Simulation

```bash
bash simulation/run_simulation.sh
```

Or run manually:

```bash
cd simulation
ngspice -b crowbar_circuit.cir
python3 plot_results.py
```

### Plots

- `simulation/crowbar_simulation_results.png`: full waveform overview
- `simulation/crowbar_trigger_zoomed.png`: zoom around trigger event

The first panel now shows both:
- `V(Rectifier/Crowbar Bus)` collapsing when SCR1 fires
- `V(Protected Output)` holding and decaying by load, not crowbar back-discharge

---

## Bill of Materials

See [docs/bom.md](docs/bom.md) for full BOM details and sourcing notes.

---

## File Structure

```text
├── README.md
├── AGENTS.md
├── docs/
│   ├── design_calculations.md
│   ├── safety_considerations.md
│   └── bom.md
├── schematic/
│   ├── crowbar_schematic.svg
│   ├── block_diagram.svg
│   ├── crowbar_schematic.txt
│   └── generate_schematics.py
└── simulation/
    ├── crowbar_circuit.cir
    ├── plot_results.py
    ├── run_simulation.sh
    ├── crowbar_results.txt
    ├── crowbar_simulation_results.png
    └── crowbar_trigger_zoomed.png
```

---

## Warnings

> HIGH VOLTAGE CIRCUIT - This design operates at lethal voltage and energy levels. Use only as a reference and validate against applicable standards before hardware implementation.

> CROWBAR ENERGY PATH - Validate SCR surge rating, snubber energy, and per-phase fuse clearing behavior using real datasheets and lab verification.

> CAPACITOR ENERGY - The 600V/1000uF output capacitor stores significant energy even after crowbar activation. Include controlled discharge provisions in hardware.
