# Crowbar Overvoltage Protection Circuit

**450V trigger threshold · 250A SCR · TL431 precision voltage sensing**

A crowbar overvoltage protection circuit designed to protect high-voltage DC loads from supply overvoltage events. When the bus voltage exceeds 450V, the TL431 precision voltage reference detects the overvoltage and fires a 250A SCR, which shorts the bus and blows the protective fuse, disconnecting the load.

## Circuit Overview

```
  HV Source ──[FUSE 300A]──┬────────────────────── Load+
                            │
                       HV Bus Node
                            │
          ┌─────────────────┼─────────────────────┐
          │                 │                      │
       [MOV]          [Sensing]              [SCR 250A]
       480V           Network                  Anode
          │                │                      │
         GND          [TL431]──[PNP]──[Gate]  [Snubber]
                            │                      │
                           GND               SCR Cathode
                                                   │
                                            GND ── Load-
```

### How It Works

1. **Normal operation (V < 450V):** The resistor divider scales the bus voltage below the TL431's 2.495V reference. The TL431 remains off, the PNP driver is off, and the SCR gate is held low by the gate-cathode shunt resistor.

2. **Overvoltage detected (V ≥ 450V):** The divider output exceeds 2.495V. The TL431 activates and pulls its cathode to ~2.5V. This forward-biases the PNP transistor (Q1), which drives current into the SCR gate.

3. **Crowbar activation:** The SCR fires and latches on, creating a near-short across the bus. The massive fault current blows the fuse, permanently disconnecting the supply from the load.

## Detailed Schematic

See [schematic/crowbar_schematic.txt](schematic/crowbar_schematic.txt) for the full annotated circuit diagram.

```
  HV Bus (+)
    │
    ├──[F1: 300A Fuse]──────────────────────────────── Load (+)
    │
    ├──[MOV1: 480V]──── GND
    │
    ├──[R1a: 910kΩ]──[R1b: 910kΩ]──┬──[R2: 10kΩ + VR1: 1kΩ trim]── GND
    │                                │
    │                           TL431 REF pin
    │
    ├──[R3: 47kΩ]──[R4: 47kΩ]──┬──[ZD1: 15V Zener]── GND
    │                            │
    │                       V_local (15V)
    │                            │
    │                       [C1: 1µF 25V]── GND
    │                       [C4: 100nF 25V]── GND
    │                            │
    │                       [R5: 1kΩ]── TL431 Cathode
    │                                         │
    │                                    TL431 Anode ── GND
    │                                         │
    │                                    [R6: 1kΩ]
    │                                         │
    │                  ┌──[ZD2: 5.1V]── Q1(PNP) Emitter ── V_local
    │                  │
    │             Q1 Base
    │                  │
    │             Q1 Collector ──[R7: 47Ω]── SCR Gate
    │                                              │
    │                                         [R8: 100Ω]── GND
    │                                         [ZD3: 15V]── GND
    │
    ├──[R9: 47Ω]──[C2: 0.47µF 630V]── GND    (Snubber)
    │
    SCR Anode (250A, ≥800V)
    │
    SCR Cathode ── GND ──────────────────────────────── Load (-)
```

## Safety Features

| # | Feature | Component | Purpose |
|---|---------|-----------|---------|
| 1 | **Fuse** | F1 (300A, 500VDC) | Interrupts current after SCR fires |
| 2 | **MOV** | MOV1 (480V) | Fast transient absorption (<1ns) |
| 3 | **RC Snubber** | R9 + C2 | dv/dt protection for SCR |
| 4 | **Gate Shunt** | R8 (100Ω) | Prevents noise-triggered SCR firing |
| 5 | **Gate Clamp** | ZD3 (15V) | Overvoltage protection on SCR gate |
| 6 | **V_EB Clamp** | ZD2 (5.1V) | Protects PNP driver transistor |
| 7 | **Noise Filter** | C3 (1nF) | Rejects HF noise on sensing divider |
| 8 | **Split Resistors** | R1a/R1b, R3/R4 | Voltage derating (each <250V) |
| 9 | **Local Supply** | ZD1 + C1 + C4 | Clean, decoupled gate driver supply |
| 10 | **Trimmer** | VR1 (1kΩ) | Precise threshold adjustment (415–457V) |

See [docs/safety_considerations.md](docs/safety_considerations.md) for detailed safety analysis.

## Design Calculations

Full calculations available in [docs/design_calculations.md](docs/design_calculations.md).

**Key parameters:**
- Trigger voltage: **449.9V** (set by R1/R2 divider ratio of 179.3:1)
- TL431 reference: 2.495V (internal bandgap)
- SCR gate current: ~100mA (from PNP driver via 15V local supply)
- Sensing current: 0.25mA (low power dissipation)
- Response time: <100µs (TL431 + PNP + SCR gate delay)

## Simulation

The circuit is simulated using **ngspice** with behavioral models for the TL431, SCR, and protection devices.

### Prerequisites

```bash
sudo apt-get install ngspice
pip install matplotlib numpy
```

### Run Simulation

```bash
cd simulation
ngspice -b crowbar_circuit.cir
python3 plot_results.py
```

### Simulation Results

The simulation demonstrates the full crowbar activation sequence:

1. **0–200ms:** Power supply ramps from 0V to 400V (normal startup)
2. **200–500ms:** Steady-state operation at 400V nominal
3. **500–608ms:** Overvoltage event begins (supply ramps toward 500V)
4. **608ms:** Bus reaches ~450V — **TL431 triggers → PNP drives → SCR fires**
5. **608ms+:** Bus voltage collapses as SCR shorts the rail; peak surge current ~4,725A would blow the fuse within milliseconds

| Parameter | Value |
|-----------|-------|
| Trigger voltage | 449.7V |
| Trigger accuracy | 99.9% of 450V target |
| Response time | <1ms from threshold crossing |
| Peak surge current | 4,725A |
| Post-crowbar bus voltage | ~1.5V (SCR forward drop) |

## Bill of Materials

See [docs/bom.md](docs/bom.md) for the full BOM with part numbers and sourcing.

## File Structure

```
├── README.md                     This file
├── AGENTS.md                     Development environment notes
├── docs/
│   ├── design_calculations.md    Detailed calculations
│   ├── safety_considerations.md  Safety analysis
│   └── bom.md                    Bill of materials
├── schematic/
│   └── crowbar_schematic.txt     Full annotated schematic
└── simulation/
    ├── crowbar_circuit.cir       ngspice netlist
    ├── plot_results.py           Plotting script
    ├── crowbar_results.txt       Raw simulation data
    ├── crowbar_simulation_results.png
    └── crowbar_trigger_zoomed.png
```

## Warnings

> **HIGH VOLTAGE CIRCUIT** — This circuit operates at 450V+ DC. Voltages above 50V DC are considered lethal. This design is for **reference only**. Any physical implementation must be designed, reviewed, and tested by qualified electrical engineers. Follow all applicable safety standards (IEC 61010, UL 508, etc.).

> **SCR SURGE RATING** — When the crowbar fires, peak currents exceeding 4,000A flow through the SCR. Ensure the selected SCR's I²t surge rating exceeds the fuse's I²t clearing rating. The SCR must survive until the fuse opens.

> **FUSE COORDINATION** — The fuse must be rated for the full bus voltage (DC) and must clear before the SCR's thermal limits are exceeded. Use semiconductor-grade fuses (e.g., Bussmann FWH series) for proper coordination.

## License

This design is provided as-is for educational and reference purposes.
