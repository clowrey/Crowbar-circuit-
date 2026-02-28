#!/usr/bin/env python3
"""
Plot crowbar circuit simulation results from ngspice output.

Generates a multi-panel plot showing:
  1. HV bus voltage with trigger annotation
  2. Local 15V supply and TL431 cathode state
  3. TL431 reference pin voltage vs threshold
  4. SCR gate voltage and latch state
  5. Supply/fuse current with crowbar surge
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

DATA_FILE = Path(__file__).parent / "crowbar_results.txt"
OUTPUT_DIR = Path(__file__).parent


def load_ngspice_data(filepath):
    """Load ngspice wrdata output (paired time-value columns)."""
    raw = np.loadtxt(filepath)
    return {
        'time':     raw[:, 0],
        'v_bus':    raw[:, 1],
        'v_ref':    raw[:, 3],
        'v_gate':   raw[:, 5],
        'i_supply': raw[:, 7],
        'v_local':  raw[:, 9],
        'v_tl431':  raw[:, 11],
        'v_latch':  raw[:, 13],
    }


def find_crossing(signal, threshold, direction='rising'):
    """Find the first index where signal crosses threshold."""
    for i in range(1, len(signal)):
        if direction == 'rising' and signal[i-1] < threshold <= signal[i]:
            return i
        if direction == 'falling' and signal[i-1] > threshold >= signal[i]:
            return i
    return None


def main():
    d = load_ngspice_data(DATA_FILE)
    t_ms = d['time'] * 1e3

    # Key events
    scr_fire = find_crossing(d['v_latch'], 3.0, 'rising')
    bus_collapse = find_crossing(d['v_bus'], 100, 'falling')
    tl431_trip = find_crossing(d['v_ref'], 2.49, 'rising')

    print("=" * 60)
    print("  CROWBAR CIRCUIT SIMULATION RESULTS")
    print("=" * 60)
    print(f"  HV Bus range:     {d['v_bus'].min():.1f}V – {d['v_bus'].max():.1f}V")
    print(f"  Ref node range:   {d['v_ref'].min():.4f}V – {d['v_ref'].max():.4f}V")
    print(f"  Gate peak:        {d['v_gate'].max():.3f}V")
    print(f"  Peak surge I:     {d['i_supply'].max():.0f}A")
    print(f"  Local supply:     {d['v_local'].max():.1f}V")
    if scr_fire:
        print(f"  SCR fires at:     {t_ms[scr_fire]:.2f} ms  (V_bus = {d['v_bus'][scr_fire]:.1f}V)")
    if bus_collapse:
        print(f"  Bus collapses at: {t_ms[bus_collapse]:.2f} ms")
    print("=" * 60)

    # ===== FIGURE =====
    fig, axes = plt.subplots(5, 1, figsize=(14, 17), sharex=True,
                             gridspec_kw={'height_ratios': [2.5, 1, 1.2, 1.2, 1.5]})
    fig.patch.set_facecolor('#fafafa')

    fig.suptitle(
        "Crowbar Overvoltage Protection Circuit\n"
        "450V Trigger Threshold  ·  250A SCR  ·  TL431 Precision Sensing",
        fontsize=15, fontweight='bold', y=0.995,
        color='#222222'
    )

    C = {
        'bus': '#1565C0', 'ref': '#2E7D32', 'gate': '#7B1FA2',
        'current': '#C62828', 'local': '#E65100', 'tl431': '#00838F',
        'latch': '#795548', 'thresh': '#D32F2F', 'nominal': '#9E9E9E',
        'zone_normal': '#E8F5E9', 'zone_ov': '#FFEBEE', 'zone_crowbar': '#FFF3E0',
    }

    fire_t = t_ms[scr_fire] if scr_fire else None

    for ax in axes:
        ax.set_facecolor('white')
        ax.grid(True, alpha=0.2, linewidth=0.5)
        ax.tick_params(labelsize=9)
        if fire_t:
            ax.axvline(x=fire_t, color=C['thresh'], linestyle=':', alpha=0.3, linewidth=1)

    # ---- Panel 1: HV Bus ----
    ax = axes[0]
    ax.fill_between(t_ms, 0, d['v_bus'], alpha=0.08, color=C['bus'])
    ax.plot(t_ms, d['v_bus'], color=C['bus'], linewidth=2, label='V(HV Bus)')
    ax.axhline(y=450, color=C['thresh'], linestyle='--', linewidth=1.2, alpha=0.8,
               label='450V Trigger Threshold')
    ax.axhline(y=400, color=C['nominal'], linestyle=':', linewidth=0.8, alpha=0.5,
               label='400V Nominal')
    ax.set_ylabel('Voltage (V)', fontsize=11)
    ax.set_title('HV Bus Voltage — Crowbar Activation', fontsize=12, fontweight='bold', pad=8)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.9)
    ax.set_ylim(-30, 520)

    if scr_fire:
        ax.annotate(
            f'CROWBAR FIRES\n{d["v_bus"][scr_fire]:.1f}V @ {t_ms[scr_fire]:.1f}ms',
            xy=(t_ms[scr_fire], d['v_bus'][scr_fire]),
            xytext=(t_ms[scr_fire] - 180, 280),
            arrowprops=dict(arrowstyle='->', color=C['thresh'], lw=2),
            fontsize=10, color=C['thresh'], fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF9C4', edgecolor=C['thresh'],
                      alpha=0.95, linewidth=1.5))

        # Annotate normal zone
        ax.text(250, 480, 'NORMAL\nOPERATION', fontsize=9, color='#388E3C',
                ha='center', va='center', alpha=0.6, fontweight='bold')
        ax.text(700, 480, 'BUS\nCOLLAPSED', fontsize=9, color=C['current'],
                ha='center', va='center', alpha=0.6, fontweight='bold')

    # ---- Panel 2: Local Supply & TL431 ----
    ax = axes[1]
    ax.plot(t_ms, d['v_local'], color=C['local'], linewidth=1.5, label='V(Local 15V Supply)')
    ax.plot(t_ms, d['v_tl431'], color=C['tl431'], linewidth=1.5, label='V(TL431 Cathode)')
    ax.set_ylabel('Voltage (V)', fontsize=11)
    ax.set_title('Local Power Supply & TL431 Cathode', fontsize=11, fontweight='bold', pad=6)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.9)
    ax.set_ylim(-1, 18)

    # ---- Panel 3: Reference Voltage ----
    ax = axes[2]
    ax.plot(t_ms, d['v_ref'], color=C['ref'], linewidth=1.8, label='V(REF node)')
    ax.axhline(y=2.495, color=C['thresh'], linestyle='--', linewidth=1.2, alpha=0.8,
               label='TL431 Vref = 2.495V')
    ax.set_ylabel('Voltage (V)', fontsize=11)
    ax.set_title('Sensing Divider → TL431 REF Pin', fontsize=11, fontweight='bold', pad=6)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.9)

    if tl431_trip:
        ax.annotate(f'Threshold crossed\n@ {t_ms[tl431_trip]:.1f}ms',
                    xy=(t_ms[tl431_trip], 2.495),
                    xytext=(t_ms[tl431_trip] - 150, 1.5),
                    arrowprops=dict(arrowstyle='->', color=C['ref'], lw=1.5),
                    fontsize=9, color=C['ref'])

    # ---- Panel 4: SCR Gate & Latch ----
    ax = axes[3]
    ax.plot(t_ms, d['v_gate'], color=C['gate'], linewidth=1.5, label='V(SCR Gate)')
    ax.plot(t_ms, d['v_latch'], color=C['latch'], linewidth=1.2,
            linestyle='--', alpha=0.7, label='SCR Latch State')
    ax.axhline(y=1.0, color='orange', linestyle=':', linewidth=1, alpha=0.6,
               label='Gate Trigger ≈ 1V')
    ax.set_ylabel('Voltage (V)', fontsize=11)
    ax.set_title('SCR Gate Drive & Latch', fontsize=11, fontweight='bold', pad=6)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.9)

    # ---- Panel 5: Supply Current ----
    ax = axes[4]
    ax.fill_between(t_ms, 0, d['i_supply'], alpha=0.15, color=C['current'])
    ax.plot(t_ms, d['i_supply'], color=C['current'], linewidth=1.5, label='I(Supply)')
    ax.set_ylabel('Current (A)', fontsize=11)
    ax.set_xlabel('Time (ms)', fontsize=12)
    ax.set_title('Supply / Fuse Current', fontsize=11, fontweight='bold', pad=6)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.9)

    if scr_fire:
        peak_i = d['i_supply'].max()
        peak_idx = np.argmax(d['i_supply'])
        ax.annotate(f'Peak surge: {peak_i:.0f}A',
                    xy=(t_ms[peak_idx], peak_i),
                    xytext=(t_ms[peak_idx] - 150, peak_i * 0.7),
                    arrowprops=dict(arrowstyle='->', color=C['current'], lw=1.5),
                    fontsize=9, color=C['current'], fontweight='bold')

    plt.tight_layout(rect=[0, 0, 1, 0.965])

    outpath = OUTPUT_DIR / "crowbar_simulation_results.png"
    fig.savefig(outpath, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    print(f"\nPlot saved: {outpath}")

    # Also save a zoomed-in view of the trigger event
    fig2, axes2 = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    fig2.patch.set_facecolor('#fafafa')
    fig2.suptitle('Crowbar Trigger Event — Zoomed View', fontsize=14, fontweight='bold')

    if fire_t:
        t_start = max(0, fire_t - 30)
        t_end = min(t_ms[-1], fire_t + 30)
        mask = (t_ms >= t_start) & (t_ms <= t_end)

        ax2 = axes2[0]
        ax2.plot(t_ms[mask], d['v_bus'][mask], color=C['bus'], linewidth=2)
        ax2.axhline(y=450, color=C['thresh'], linestyle='--', alpha=0.8)
        ax2.set_ylabel('V(HV Bus) (V)')
        ax2.set_title('Bus Voltage During Crowbar Event', fontweight='bold')
        ax2.grid(True, alpha=0.3)

        ax2 = axes2[1]
        ax2.plot(t_ms[mask], d['v_gate'][mask], color=C['gate'], linewidth=2)
        ax2.axhline(y=1.0, color='orange', linestyle=':', alpha=0.6)
        ax2.set_ylabel('V(SCR Gate) (V)')
        ax2.set_title('SCR Gate Voltage', fontweight='bold')
        ax2.grid(True, alpha=0.3)

        ax2 = axes2[2]
        ax2.plot(t_ms[mask], d['i_supply'][mask], color=C['current'], linewidth=2)
        ax2.set_ylabel('I(Supply) (A)')
        ax2.set_xlabel('Time (ms)')
        ax2.set_title('Surge Current', fontweight='bold')
        ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    zoom_path = OUTPUT_DIR / "crowbar_trigger_zoomed.png"
    fig2.savefig(zoom_path, dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
    print(f"Zoomed plot saved: {zoom_path}")


if __name__ == "__main__":
    main()
