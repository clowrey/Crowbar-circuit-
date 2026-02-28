#!/bin/bash
# Run the crowbar circuit simulation and generate plots
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Running ngspice simulation ==="
ngspice -b crowbar_circuit.cir

echo ""
echo "=== Generating plots ==="
python3 plot_results.py

echo ""
echo "=== Done ==="
echo "Results:"
echo "  Raw data:    simulation/crowbar_results.txt"
echo "  Full plot:   simulation/crowbar_simulation_results.png"
echo "  Zoomed plot: simulation/crowbar_trigger_zoomed.png"
