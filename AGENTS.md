# AGENTS.md

## Cursor Cloud specific instructions

This is an electronics/hardware design project — a **crowbar overvoltage protection circuit** (450V trigger, 250A SCR, TL431 sensing). There is no traditional software application to build or serve.

### Toolchain

| Tool | Purpose | Install |
|------|---------|---------|
| **ngspice** | Circuit simulation | `sudo apt install ngspice` |
| **gnuplot** | Waveform plotting | `sudo apt install gnuplot` |
| **schemdraw** | Circuit schematic generation | `pip install schemdraw matplotlib` |

### Running the simulation

```bash
bash simulation/run_simulation.sh       # ngspice → gnuplot → PNG/SVG plots
```

Or individually:
```bash
cd simulation
ngspice -b crowbar_circuit.cir          # transient analysis → crowbar_results.txt
gnuplot plot_results.gnuplot            # waveform plots → PNG + SVG
```

### Regenerating schematics

```bash
python3 schematic/generate_schematics.py   # schemdraw → SVG + PNG
```

Schematics use the **schemdraw** library which provides proper IEC/IEEE electronic component symbols (resistors, capacitors, zener diodes, SCR, PNP BJT, fuse, varistor, etc.).

### Key simulation notes

- Behavioral models are used for TL431, SCR, MOV, and zener diodes — approximate but captures essential switching/latching behavior.
- The SCR model uses a capacitor-based latch state variable (`scr_state` node). Fires when gate voltage exceeds 1V and latch charges above 3V.
- Source impedance (`R_source = 0.1Ω`) models realistic bus voltage collapse when SCR fires.
- Simulation timescale is 800ms with a 200ms startup ramp. Overvoltage event begins at 500ms.
- Large SVG waveform plots (~8MB) are in `.gitignore`; run gnuplot to regenerate.
