# ============================================================================
# Crowbar Circuit Simulation — Gnuplot Script
# Reads ngspice wrdata output and produces multi-panel waveform plots
# ============================================================================
#
# Usage:  gnuplot plot_results.gnuplot
# Input:  crowbar_results.txt (from ngspice wrdata)
# Output: crowbar_simulation_results.svg
#         crowbar_simulation_results.png
#         crowbar_trigger_zoomed.svg
#         crowbar_trigger_zoomed.png
#
# Data format (ngspice wrdata, 4 signals):
#   col 1,2:  time, V(hv_bus)
#   col 3,4:  time, V(ref_node)
#   col 5,6:  time, V(scr_gate)
#   col 7,8:  time, I(supply)
#   col 9,10: time, V(local_pwr)
#   col 11,12: time, V(tl431_cath)
#   col 13,14: time, V(scr_state)
# ============================================================================

datafile = "crowbar_results.txt"

# --- Color scheme ---
bus_color    = "#1565C0"
ref_color    = "#2E7D32"
gate_color   = "#7B1FA2"
current_color = "#C62828"
local_color  = "#E65100"
tl431_color  = "#00838F"
latch_color  = "#795548"
thresh_color = "#D32F2F"

# ============================================================================
# PLOT 1: Full simulation waveforms (SVG)
# ============================================================================
set terminal svg size 1200,1000 font "Arial,11" enhanced background "#fafafa"
set output "crowbar_simulation_results.svg"

set multiplot layout 5,1 title \
    "Crowbar Overvoltage Protection — Simulation Results\n" . \
    "{/*0.8 450V Trigger  ·  250A SCR  ·  TL431 Sensing}" \
    font "Arial,14"

set lmargin 12
set rmargin 3
set grid lc rgb "#cccccc" lw 0.5

# Panel 1: HV Bus Voltage
set ylabel "Voltage (V)" font "Arial,10"
set yrange [-30:520]
set title "HV Bus Voltage — Crowbar Activation" font "Arial,12"
set arrow 1 from 0,450 to 0.8,450 nohead dt 2 lc rgb thresh_color lw 1.5
set label 1 "450V Trigger" at 0.002,470 font "Arial,9" tc rgb thresh_color
plot datafile using ($1*1000):2 with lines lw 2 lc rgb bus_color title "V(HV Bus)"
unset arrow 1
unset label 1

# Panel 2: Local Supply + TL431 Cathode
set ylabel "Voltage (V)" font "Arial,10"
set yrange [-1:18]
set title "Local Power Supply & TL431 Cathode" font "Arial,12"
plot datafile using ($9*1000):10 with lines lw 1.5 lc rgb local_color title "V(Local 15V)", \
     datafile using ($11*1000):12 with lines lw 1.5 lc rgb tl431_color title "V(TL431 Cathode)"

# Panel 3: Reference Voltage
set ylabel "Voltage (V)" font "Arial,10"
set yrange [*:*]
set title "Sensing Divider → TL431 REF Pin" font "Arial,12"
set arrow 2 from 0,2.495 to 0.8,2.495 nohead dt 2 lc rgb thresh_color lw 1.5
set label 2 "Vref = 2.495V" at 0.002,2.55 font "Arial,9" tc rgb thresh_color
plot datafile using ($3*1000):4 with lines lw 1.8 lc rgb ref_color title "V(REF node)"
unset arrow 2
unset label 2

# Panel 4: SCR Gate + Latch
set ylabel "Voltage (V)" font "Arial,10"
set yrange [*:*]
set title "SCR Gate Drive & Latch State" font "Arial,12"
set arrow 3 from 0,1.0 to 0.8,1.0 nohead dt 3 lc rgb "#FF8F00" lw 1
plot datafile using ($5*1000):6 with lines lw 1.5 lc rgb gate_color title "V(SCR Gate)", \
     datafile using ($13*1000):14 with lines lw 1 dt 2 lc rgb latch_color title "SCR Latch State"
unset arrow 3

# Panel 5: Supply Current
set xlabel "Time (ms)" font "Arial,11"
set ylabel "Current (A)" font "Arial,10"
set yrange [*:*]
set title "Supply / Fuse Current" font "Arial,12"
plot datafile using ($7*1000):8 with lines lw 1.5 lc rgb current_color title "I(Supply)"

unset multiplot
set output

# ============================================================================
# PLOT 1b: Full simulation waveforms (PNG)
# ============================================================================
set terminal pngcairo size 1200,1000 font "Arial,11" enhanced background "#fafafa"
set output "crowbar_simulation_results.png"

set multiplot layout 5,1 title \
    "Crowbar Overvoltage Protection — Simulation Results\n" . \
    "{/*0.8 450V Trigger  ·  250A SCR  ·  TL431 Sensing}" \
    font "Arial,14"

set lmargin 12
set rmargin 3
set grid lc rgb "#cccccc" lw 0.5
unset xlabel

# Panel 1
set ylabel "Voltage (V)" font "Arial,10"
set yrange [-30:520]
set title "HV Bus Voltage — Crowbar Activation" font "Arial,12"
set arrow 1 from 0,450 to 800,450 nohead dt 2 lc rgb thresh_color lw 1.5
set label 1 "450V Trigger" at 10,470 font "Arial,9" tc rgb thresh_color
plot datafile using ($1*1000):2 with lines lw 2 lc rgb bus_color title "V(HV Bus)"
unset arrow 1
unset label 1

# Panel 2
set ylabel "Voltage (V)" font "Arial,10"
set yrange [-1:18]
set title "Local Power Supply & TL431 Cathode" font "Arial,12"
plot datafile using ($9*1000):10 with lines lw 1.5 lc rgb local_color title "V(Local 15V)", \
     datafile using ($11*1000):12 with lines lw 1.5 lc rgb tl431_color title "V(TL431 Cathode)"

# Panel 3
set ylabel "Voltage (V)" font "Arial,10"
set yrange [*:*]
set title "Sensing Divider → TL431 REF Pin" font "Arial,12"
set arrow 2 from 0,2.495 to 800,2.495 nohead dt 2 lc rgb thresh_color lw 1.5
set label 2 "Vref = 2.495V" at 10,2.55 font "Arial,9" tc rgb thresh_color
plot datafile using ($3*1000):4 with lines lw 1.8 lc rgb ref_color title "V(REF node)"
unset arrow 2
unset label 2

# Panel 4
set ylabel "Voltage (V)" font "Arial,10"
set yrange [*:*]
set title "SCR Gate Drive & Latch State" font "Arial,12"
set arrow 3 from 0,1.0 to 800,1.0 nohead dt 3 lc rgb "#FF8F00" lw 1
plot datafile using ($5*1000):6 with lines lw 1.5 lc rgb gate_color title "V(SCR Gate)", \
     datafile using ($13*1000):14 with lines lw 1 dt 2 lc rgb latch_color title "SCR Latch State"
unset arrow 3

# Panel 5
set xlabel "Time (ms)" font "Arial,11"
set ylabel "Current (A)" font "Arial,10"
set yrange [*:*]
set title "Supply / Fuse Current" font "Arial,12"
plot datafile using ($7*1000):8 with lines lw 1.5 lc rgb current_color title "I(Supply)"

unset multiplot
set output

# ============================================================================
# PLOT 2: Zoomed trigger event (SVG)
# ============================================================================
set terminal svg size 1000,700 font "Arial,11" enhanced background "#fafafa"
set output "crowbar_trigger_zoomed.svg"

set multiplot layout 3,1 title \
    "Crowbar Trigger Event — Zoomed View" font "Arial,14"

set lmargin 12
set rmargin 3
set grid lc rgb "#cccccc" lw 0.5
set xrange [580:640]
unset xlabel

set ylabel "V(HV Bus) (V)"
set yrange [*:*]
set title "Bus Voltage During Crowbar Event" font "Arial,12"
set arrow 1 from 580,450 to 640,450 nohead dt 2 lc rgb thresh_color lw 1.5
plot datafile using ($1*1000):2 with lines lw 2 lc rgb bus_color notitle
unset arrow 1

set ylabel "V(SCR Gate) (V)"
set yrange [*:*]
set title "SCR Gate Voltage" font "Arial,12"
set arrow 2 from 580,1.0 to 640,1.0 nohead dt 3 lc rgb "#FF8F00" lw 1
plot datafile using ($5*1000):6 with lines lw 2 lc rgb gate_color notitle
unset arrow 2

set xlabel "Time (ms)" font "Arial,11"
set ylabel "I(Supply) (A)"
set yrange [*:*]
set title "Surge Current" font "Arial,12"
plot datafile using ($7*1000):8 with lines lw 2 lc rgb current_color notitle

unset multiplot
set output

# ============================================================================
# PLOT 2b: Zoomed trigger event (PNG)
# ============================================================================
set terminal pngcairo size 1000,700 font "Arial,11" enhanced background "#fafafa"
set output "crowbar_trigger_zoomed.png"

set multiplot layout 3,1 title \
    "Crowbar Trigger Event — Zoomed View" font "Arial,14"

set lmargin 12
set rmargin 3
set grid lc rgb "#cccccc" lw 0.5
set xrange [580:640]
unset xlabel

set ylabel "V(HV Bus) (V)"
set yrange [*:*]
set title "Bus Voltage During Crowbar Event" font "Arial,12"
set arrow 1 from 580,450 to 640,450 nohead dt 2 lc rgb thresh_color lw 1.5
plot datafile using ($1*1000):2 with lines lw 2 lc rgb bus_color notitle
unset arrow 1

set ylabel "V(SCR Gate) (V)"
set yrange [*:*]
set title "SCR Gate Voltage" font "Arial,12"
set arrow 2 from 580,1.0 to 640,1.0 nohead dt 3 lc rgb "#FF8F00" lw 1
plot datafile using ($5*1000):6 with lines lw 2 lc rgb gate_color notitle
unset arrow 2

set xlabel "Time (ms)" font "Arial,11"
set ylabel "I(Supply) (A)"
set yrange [*:*]
set title "Surge Current" font "Arial,12"
plot datafile using ($7*1000):8 with lines lw 2 lc rgb current_color notitle

unset multiplot
set output
