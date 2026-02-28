# AGENTS.md

## Cursor Cloud specific instructions

This is an electronics/hardware design project — a **crowbar overvoltage protection circuit** (450V trigger, 250A SCR, TL431 sensing). There is no traditional software application to build or serve.

### Running the simulation

The project uses **ngspice** for circuit simulation and **matplotlib** for plotting.

```bash
# Full simulation + plotting (from repo root)
bash simulation/run_simulation.sh

# Or individually:
cd simulation
ngspice -b crowbar_circuit.cir       # runs transient analysis, writes crowbar_results.txt
python3 plot_results.py              # generates PNG plots from results
```

### Dependencies

- `ngspice` (circuit simulator, installed via apt)
- `python3` with `matplotlib` and `numpy` (plotting)

### Project structure

- `simulation/crowbar_circuit.cir` — ngspice netlist (the circuit definition and simulation commands)
- `simulation/plot_results.py` — Python script that parses ngspice output and generates annotated plots
- `docs/` — design calculations, BOM, and safety analysis
- `schematic/` — ASCII art schematic

### Key simulation notes

- The simulation uses behavioral models for the TL431, SCR, MOV, and zener diodes. These are approximate but capture the essential switching/latching behavior.
- The SCR model uses a capacitor-based latch state variable (`scr_state` node). The SCR fires when gate voltage exceeds 1V and the latch charges above 3V.
- Source impedance (`R_source = 0.1Ω`) is included to model realistic bus voltage collapse when the SCR fires. Without it, the ideal voltage source would maintain bus voltage indefinitely.
- Simulation timescale is 800ms with a 200ms startup ramp. The overvoltage event begins at 500ms.
