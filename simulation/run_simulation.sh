#!/bin/bash
# Run crowbar circuit simulation and generate all output artifacts.
#
# Tools used:
#   ngspice  — SPICE circuit simulation (transient analysis)
#   gnuplot  — waveform plotting (reads ngspice data directly)
#
# Dependencies: apt install ngspice gnuplot
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Running ngspice transient simulation ==="
ngspice -b crowbar_circuit.cir

echo ""
echo "=== Generating waveform plots with gnuplot ==="
gnuplot plot_results.gnuplot

echo ""
echo "=== Done ==="
echo "Outputs:"
echo "  Raw data:        crowbar_results.txt"
echo "  Waveforms (PNG): crowbar_simulation_results.png"
echo "  Zoomed (PNG):    crowbar_trigger_zoomed.png"
echo "  Waveforms (SVG): crowbar_simulation_results.svg"
echo "  Zoomed (SVG):    crowbar_trigger_zoomed.svg"
