#!/usr/bin/env python3
"""Generate SVG schematics for the crowbar overvoltage protection circuit."""

import textwrap
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent


def svg_header(width, height, title=""):
    return textwrap.dedent(f"""\
    <?xml version="1.0" encoding="UTF-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}"
         width="{width}" height="{height}" font-family="'Segoe UI', Arial, sans-serif">
    <title>{title}</title>
    <defs>
      <style>
        .wire {{ stroke: #222; stroke-width: 2; fill: none; }}
        .wire-thick {{ stroke: #222; stroke-width: 3; fill: none; }}
        .wire-bus {{ stroke: #c62828; stroke-width: 4; fill: none; }}
        .wire-sense {{ stroke: #1565c0; stroke-width: 2; fill: none; stroke-dasharray: 5,4; }}
        .comp-body {{ stroke: #333; stroke-width: 1.8; fill: #fff; }}
        .comp-fill {{ stroke: #333; stroke-width: 1.8; }}
        .label {{ font-size: 11px; fill: #333; }}
        .label-sm {{ font-size: 9.5px; fill: #555; }}
        .label-lg {{ font-size: 13px; fill: #222; font-weight: 600; }}
        .label-title {{ font-size: 18px; fill: #111; font-weight: 700; }}
        .label-subtitle {{ font-size: 12px; fill: #555; }}
        .node-dot {{ fill: #222; }}
        .gnd-symbol {{ stroke: #222; stroke-width: 2; fill: none; }}
        .highlight {{ fill: #fff3e0; stroke: #e65100; stroke-width: 1.5; rx: 6; }}
        .zone-sense {{ fill: #e3f2fd; stroke: #1565c0; stroke-width: 1; stroke-dasharray: 4,3; rx: 8; opacity: 0.5; }}
        .zone-supply {{ fill: #e8f5e9; stroke: #2e7d32; stroke-width: 1; stroke-dasharray: 4,3; rx: 8; opacity: 0.5; }}
        .zone-driver {{ fill: #fce4ec; stroke: #c62828; stroke-width: 1; stroke-dasharray: 4,3; rx: 8; opacity: 0.5; }}
        .zone-power {{ fill: #fff8e1; stroke: #f57f17; stroke-width: 1; stroke-dasharray: 4,3; rx: 8; opacity: 0.5; }}
        .safety-badge {{ fill: #c62828; }}
        .safety-text {{ font-size: 8px; fill: #fff; font-weight: 700; }}
      </style>
      <!-- Resistor (IEC zigzag) -->
      <symbol id="resistor-h" viewBox="0 0 60 20" overflow="visible">
        <polyline points="0,10 8,10 12,2 20,18 28,2 36,18 44,2 52,18 56,10 60,10"
                  stroke="#333" stroke-width="1.8" fill="none" stroke-linejoin="round"/>
      </symbol>
      <symbol id="resistor-v" viewBox="0 0 20 60" overflow="visible">
        <polyline points="10,0 10,8 2,12 18,20 2,28 18,36 2,44 18,52 10,56 10,60"
                  stroke="#333" stroke-width="1.8" fill="none" stroke-linejoin="round"/>
      </symbol>
      <!-- Capacitor -->
      <symbol id="cap-h" viewBox="0 0 30 20" overflow="visible">
        <line x1="0" y1="10" x2="12" y2="10" stroke="#333" stroke-width="2"/>
        <line x1="12" y1="0" x2="12" y2="20" stroke="#333" stroke-width="2.5"/>
        <line x1="18" y1="0" x2="18" y2="20" stroke="#333" stroke-width="2.5"/>
        <line x1="18" y1="10" x2="30" y2="10" stroke="#333" stroke-width="2"/>
      </symbol>
      <symbol id="cap-v" viewBox="0 0 20 30" overflow="visible">
        <line x1="10" y1="0" x2="10" y2="12" stroke="#333" stroke-width="2"/>
        <line x1="0" y1="12" x2="20" y2="12" stroke="#333" stroke-width="2.5"/>
        <line x1="0" y1="18" x2="20" y2="18" stroke="#333" stroke-width="2.5"/>
        <line x1="10" y1="18" x2="10" y2="30" stroke="#333" stroke-width="2"/>
      </symbol>
      <!-- Zener diode (vertical, cathode top) -->
      <symbol id="zener-v" viewBox="0 0 20 30" overflow="visible">
        <line x1="10" y1="0" x2="10" y2="10" stroke="#333" stroke-width="2"/>
        <polygon points="3,10 17,10 10,22" fill="#333" stroke="#333" stroke-width="1"/>
        <polyline points="2,22 18,22 18,19" stroke="#333" stroke-width="2" fill="none"/>
        <line x1="10" y1="22" x2="10" y2="30" stroke="#333" stroke-width="2"/>
      </symbol>
      <!-- Fuse -->
      <symbol id="fuse-h" viewBox="0 0 60 24" overflow="visible">
        <line x1="0" y1="12" x2="10" y2="12" stroke="#333" stroke-width="2"/>
        <rect x="10" y="2" width="40" height="20" rx="3" fill="#fff" stroke="#333" stroke-width="1.8"/>
        <line x1="20" y1="12" x2="40" y2="12" stroke="#333" stroke-width="1.2" stroke-dasharray="2,2"/>
        <line x1="50" y1="12" x2="60" y2="12" stroke="#333" stroke-width="2"/>
      </symbol>
      <!-- Ground symbol -->
      <symbol id="gnd" viewBox="0 0 20 16" overflow="visible">
        <line x1="10" y1="0" x2="10" y2="4" stroke="#222" stroke-width="2"/>
        <line x1="2" y1="4" x2="18" y2="4" stroke="#222" stroke-width="2"/>
        <line x1="5" y1="8" x2="15" y2="8" stroke="#222" stroke-width="2"/>
        <line x1="8" y1="12" x2="12" y2="12" stroke="#222" stroke-width="2"/>
      </symbol>
    </defs>
    """)


def svg_footer():
    return "</svg>\n"


def ground(x, y):
    return f'<use href="#gnd" x="{x-10}" y="{y}" width="20" height="16"/>\n'


def node_dot(x, y):
    return f'<circle cx="{x}" cy="{y}" r="3.5" class="node-dot"/>\n'


def wire(x1, y1, x2, y2, cls="wire"):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}"/>\n'


def polyline(points, cls="wire"):
    pts = " ".join(f"{x},{y}" for x, y in points)
    return f'<polyline points="{pts}" class="{cls}"/>\n'


def text(x, y, content, cls="label", anchor="middle"):
    safe = content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{safe}</text>\n'


def resistor_h(x, y, label, value):
    s = f'<use href="#resistor-h" x="{x}" y="{y-10}" width="60" height="20"/>\n'
    s += text(x + 30, y - 16, label, "label-sm")
    s += text(x + 30, y + 22, value, "label-sm")
    return s


def resistor_v(x, y, label, value):
    s = f'<use href="#resistor-v" x="{x-10}" y="{y}" width="20" height="60"/>\n'
    s += text(x + 18, y + 25, label, "label-sm", "start")
    s += text(x + 18, y + 38, value, "label-sm", "start")
    return s


def cap_v(x, y, label, value):
    s = f'<use href="#cap-v" x="{x-10}" y="{y}" width="20" height="30"/>\n'
    s += text(x + 18, y + 10, label, "label-sm", "start")
    s += text(x + 18, y + 22, value, "label-sm", "start")
    return s


def zener_v(x, y, label, value):
    s = f'<use href="#zener-v" x="{x-10}" y="{y}" width="20" height="30"/>\n'
    s += text(x + 18, y + 10, label, "label-sm", "start")
    s += text(x + 18, y + 22, value, "label-sm", "start")
    return s


def fuse_h(x, y, label, value):
    s = f'<use href="#fuse-h" x="{x}" y="{y-12}" width="60" height="24"/>\n'
    s += text(x + 30, y - 18, label, "label-sm")
    s += text(x + 30, y + 20, value, "label-sm")
    return s


def safety_badge(x, y, num):
    s = f'<circle cx="{x}" cy="{y}" r="7" class="safety-badge"/>\n'
    s += f'<text x="{x}" y="{y+3}" class="safety-text" text-anchor="middle">{num}</text>\n'
    return s


def generate_block_diagram():
    """Generate a high-level block diagram SVG."""
    W, H = 900, 520
    svg = svg_header(W, H, "Crowbar Circuit Block Diagram")

    # Background
    svg += '<rect width="900" height="520" fill="#fafafa" rx="0"/>\n'

    # Title
    svg += text(450, 35, "Crowbar Overvoltage Protection — Block Diagram", "label-title")
    svg += text(450, 55, "450V Trigger · 250A SCR · TL431 Sensing", "label-subtitle")

    # ---- Blocks ----
    bh = 60  # block height
    by_top = 100  # top row y

    # HV Source
    svg += f'<rect x="30" y="{by_top}" width="130" height="{bh}" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>\n'
    svg += text(95, by_top + 25, "HV Source", "label-lg")
    svg += text(95, by_top + 42, "(up to 500V)", "label-sm")

    # Fuse
    svg += f'<rect x="210" y="{by_top}" width="100" height="{bh}" rx="8" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>\n'
    svg += text(260, by_top + 25, "F1: Fuse", "label-lg")
    svg += text(260, by_top + 42, "300A / 500VDC", "label-sm")
    svg += safety_badge(210, by_top, 1)

    # HV Bus node
    svg += f'<rect x="360" y="{by_top}" width="100" height="{bh}" rx="8" fill="#ffebee" stroke="#c62828" stroke-width="2.5"/>\n'
    svg += text(410, by_top + 25, "HV Bus", "label-lg")
    svg += text(410, by_top + 42, "Node", "label-sm")

    # Load
    svg += f'<rect x="720" y="{by_top}" width="130" height="{bh}" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>\n'
    svg += text(785, by_top + 25, "Protected", "label-lg")
    svg += text(785, by_top + 42, "Load", "label-sm")

    # Arrows top row
    svg += f'<line x1="160" y1="{by_top+30}" x2="205" y2="{by_top+30}" class="wire-thick" marker-end="url(#arrowhead)"/>\n'
    svg += f'<line x1="310" y1="{by_top+30}" x2="355" y2="{by_top+30}" class="wire-thick" marker-end="url(#arrowhead)"/>\n'
    svg += f'<line x1="460" y1="{by_top+30}" x2="715" y2="{by_top+30}" class="wire-thick" marker-end="url(#arrowhead)"/>\n'

    # arrowhead marker
    svg += '<defs><marker id="arrowhead" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">'
    svg += '<polygon points="0 0, 8 3, 0 6" fill="#222"/></marker></defs>\n'

    # ---- Row 2: MOV, Sensing, Local Supply, Snubber ----
    by2 = 220

    # MOV
    svg += f'<rect x="30" y="{by2}" width="120" height="{bh}" rx="8" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>\n'
    svg += text(90, by2 + 25, "MOV1", "label-lg")
    svg += text(90, by2 + 42, "480V Clamp", "label-sm")
    svg += safety_badge(30, by2, 2)

    # Sensing Network
    svg += f'<rect x="180" y="{by2}" width="150" height="{bh}" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>\n'
    svg += text(255, by2 + 25, "Sensing Divider", "label-lg")
    svg += text(255, by2 + 42, "R1a+R1b / R2+VR1", "label-sm")

    # Local Supply
    svg += f'<rect x="360" y="{by2}" width="140" height="{bh}" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>\n'
    svg += text(430, by2 + 25, "Local 15V", "label-lg")
    svg += text(430, by2 + 42, "R3+R4, ZD1, C1", "label-sm")

    # Snubber
    svg += f'<rect x="530" y="{by2}" width="120" height="{bh}" rx="8" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>\n'
    svg += text(590, by2 + 25, "Snubber", "label-lg")
    svg += text(590, by2 + 42, "R9 + C2", "label-sm")
    svg += safety_badge(530, by2, 3)

    # Connections from HV bus down
    svg += wire(90, by_top + bh, 90, by2)  # MOV
    svg += wire(255, by_top + bh, 255, by2)  # Sensing
    svg += wire(430, by_top + bh, 430, by2)  # Local supply
    svg += wire(590, by_top + bh, 590, by2)  # Snubber

    # Vertical line from HV Bus node down
    svg += wire(410, by_top + bh, 410, by_top + bh + 15)
    svg += wire(90, by_top + bh + 15, 590, by_top + bh + 15, "wire-bus")
    for xx in [90, 255, 410, 430, 590]:
        svg += node_dot(xx, by_top + bh + 15)

    # ---- Row 3: TL431, Gate Driver, SCR ----
    by3 = 340

    # TL431
    svg += f'<rect x="180" y="{by3}" width="120" height="{bh}" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>\n'
    svg += text(240, by3 + 25, "TL431", "label-lg")
    svg += text(240, by3 + 42, "Vref = 2.495V", "label-sm")

    # Gate Driver
    svg += f'<rect x="360" y="{by3}" width="140" height="{bh}" rx="8" fill="#fce4ec" stroke="#c62828" stroke-width="2"/>\n'
    svg += text(430, by3 + 25, "PNP Driver", "label-lg")
    svg += text(430, by3 + 42, "Q1 + R6, R7, ZD2", "label-sm")

    # SCR
    svg += f'<rect x="560" y="{by3}" width="130" height="{bh}" rx="8" fill="#ffebee" stroke="#c62828" stroke-width="2.5"/>\n'
    svg += text(625, by3 + 25, "SCR 250A", "label-lg")
    svg += text(625, by3 + 42, "≥800V VDRM", "label-sm")

    # Arrows row 2→3
    svg += f'<line x1="255" y1="{by2+bh}" x2="240" y2="{by3-5}" class="wire-thick" marker-end="url(#arrowhead)"/>\n'
    svg += text(230, by2 + bh + 20, "V_ref", "label-sm")

    svg += f'<line x1="430" y1="{by2+bh}" x2="430" y2="{by3-5}" class="wire-thick" marker-end="url(#arrowhead)"/>\n'
    svg += text(448, by2 + bh + 20, "15V", "label-sm")

    # TL431 → Gate Driver
    svg += f'<line x1="300" y1="{by3+30}" x2="355" y2="{by3+30}" class="wire-thick" marker-end="url(#arrowhead)"/>\n'
    svg += text(328, by3 + 22, "Cathode", "label-sm")

    # Gate Driver → SCR
    svg += f'<line x1="500" y1="{by3+30}" x2="555" y2="{by3+30}" class="wire-thick" marker-end="url(#arrowhead)"/>\n'
    svg += text(528, by3 + 22, "Gate", "label-sm")

    # SCR → HV Bus (crowbar path)
    svg += f'<line x1="625" y1="{by3}" x2="625" y2="{by_top+bh+15}" class="wire-bus"/>\n'
    svg += node_dot(625, by_top + bh + 15)
    svg += text(638, by3 - 10, "Anode", "label-sm", "start")

    # ---- Ground bus ----
    gy = 460
    svg += wire(30, gy, 700, gy)
    svg += text(720, gy + 5, "GND", "label-lg", "start")

    # Ground connections
    for xx in [90, 255, 430, 590, 625]:
        svg += wire(xx, by3 + bh, xx, gy)
        svg += node_dot(xx, gy)

    svg += text(90, gy + 18, "MOV", "label-sm")
    svg += text(255, gy + 18, "Sense", "label-sm")
    svg += text(430, gy + 18, "Supply", "label-sm")
    svg += text(590, gy + 18, "Snubber", "label-sm")
    svg += text(625, gy + 18, "SCR-K", "label-sm")

    # ---- Signal flow annotation ----
    svg += text(450, 500, "Signal flow: HV Bus → Sensing Divider → TL431 REF → TL431 Cathode → PNP Gate Driver → SCR Gate → CROWBAR", "label-sm")

    svg += svg_footer()
    return svg


def generate_detailed_schematic():
    """Generate a detailed circuit schematic SVG with component symbols."""
    W, H = 1500, 980
    svg = svg_header(W, H, "Crowbar Circuit — Detailed Schematic (3-Phase Refined)")

    # Background
    svg += f'<rect width="{W}" height="{H}" fill="#fefefe" rx="0"/>\n'

    # Title block
    svg += '<rect x="1020" y="900" width="470" height="70" fill="#f5f5f5" stroke="#222" stroke-width="1.5"/>\n'
    svg += text(1255, 924, "CROWBAR OVERVOLTAGE PROTECTION", "label-lg")
    svg += text(1255, 942, "3-PHASE 240V L-L | SCR1 CROWBAR + SCR2 ISOLATION", "label-sm")
    svg += text(1255, 958, "Rev 2.0", "label-sm")

    # Functional zone backgrounds
    svg += f'<rect x="20" y="70" width="1460" height="360" class="zone-power"/>\n'
    svg += text(35, 88, "POWER STAGE (3-PHASE INPUT, RECTIFIER, CROWBAR, OUTPUT ISOLATION)", "label-sm", "start")
    svg += f'<rect x="20" y="450" width="1460" height="430" class="zone-sense"/>\n'
    svg += text(35, 468, "SENSING + DRIVER CONTROL CHAIN", "label-sm", "start")

    # =========================================================================
    # POWER STAGE
    # =========================================================================
    phase_y = [120, 165, 210]
    phase_lbl = ["A", "B", "C"]
    fuse_x = 90
    rect_x = 250
    rect_y = 95
    rect_w = 190
    rect_h = 170
    hv_bus_y = 165
    hv_bus_start = rect_x + rect_w
    hv_bus_end = 940
    dc_out_x = 1080
    return_y = 395

    # 3-phase source + per-phase fuses
    for idx, py in enumerate(phase_y):
        lbl = phase_lbl[idx]
        svg += text(25, py + 4, f"PH-{lbl}", "label-lg", "start")
        svg += f'<circle cx="55" cy="{py}" r="12" class="comp-body"/>\n'
        svg += text(55, py + 4, "~", "label-lg")
        svg += wire(67, py, fuse_x, py)
        svg += fuse_h(fuse_x, py, f"F1{lbl}", "3A")
        svg += wire(fuse_x + 60, py, rect_x, py)
        svg += node_dot(rect_x, py)

    svg += safety_badge(fuse_x + 8, phase_y[0] - 25, 1)
    svg += text(140, 258, "Per-phase input fusing", "label-sm", "start")

    # Bridge rectifier block with diode annotation
    svg += f'<rect x="{rect_x}" y="{rect_y}" width="{rect_w}" height="{rect_h}" rx="6" class="comp-body"/>\n'
    svg += text(rect_x + rect_w / 2, rect_y + 24, "3-PHASE BRIDGE RECTIFIER", "label-sm")
    svg += text(rect_x + rect_w / 2, rect_y + 42, "D1 D2 D3", "label-sm")
    svg += text(rect_x + rect_w / 2, rect_y + 58, "D4 D5 D6", "label-sm")
    svg += text(rect_x + rect_w / 2, rect_y + 78, "AC IN: A/B/C", "label-sm")
    svg += text(rect_x + rect_w / 2, rect_y + 96, "DC+: rect_pos", "label-sm")
    svg += text(rect_x + rect_w / 2, rect_y + 112, "DC-: return", "label-sm")

    # Rectifier outputs
    svg += wire(hv_bus_start, hv_bus_y, hv_bus_end, hv_bus_y, "wire-bus")
    svg += node_dot(hv_bus_start, hv_bus_y)
    svg += text(hv_bus_start + 8, hv_bus_y - 8, "HV_BUS", "label-lg", "start")

    rect_neg_x = rect_x + rect_w - 25
    svg += wire(rect_neg_x, rect_y + rect_h, rect_neg_x, return_y)
    svg += node_dot(rect_neg_x, return_y)

    # Return bus
    svg += wire(rect_neg_x, return_y, 1450, return_y, "wire")
    svg += text(1458, return_y + 4, "RETURN / RECTIFIER NEGATIVE", "label-sm", "start")

    # MOV at HV_BUS
    mov_x = 560
    svg += wire(mov_x, hv_bus_y, mov_x, hv_bus_y + 20)
    svg += node_dot(mov_x, hv_bus_y)
    svg += f'<rect x="{mov_x-15}" y="{hv_bus_y+20}" width="30" height="45" rx="3" class="comp-body"/>\n'
    svg += text(mov_x, hv_bus_y + 38, "~", "label-lg")
    svg += text(mov_x, hv_bus_y + 50, "~", "label-lg")
    svg += text(mov_x + 22, hv_bus_y + 34, "MOV1", "label-sm", "start")
    svg += text(mov_x + 22, hv_bus_y + 48, "480V", "label-sm", "start")
    svg += safety_badge(mov_x - 18, hv_bus_y + 16, 2)
    svg += wire(mov_x, hv_bus_y + 65, mov_x, return_y)

    # SCR1 crowbar (anode on HV_BUS, cathode on return)
    scr_x = 810
    scr_top = hv_bus_y + 30
    svg += wire(scr_x, hv_bus_y, scr_x, scr_top, "wire-bus")
    svg += node_dot(scr_x, hv_bus_y)
    svg += f'<polygon points="{scr_x-25},{scr_top} {scr_x+25},{scr_top} {scr_x},{scr_top+50}" fill="#fff" stroke="#333" stroke-width="2"/>\n'
    svg += f'<line x1="{scr_x-25}" y1="{scr_top+50}" x2="{scr_x+25}" y2="{scr_top+50}" stroke="#333" stroke-width="3"/>\n'
    svg += text(scr_x + 34, scr_top + 10, "SCR1", "label-lg", "start")
    svg += text(scr_x + 34, scr_top + 26, "Crowbar SCR", "label-sm", "start")
    svg += text(scr_x + 34, scr_top + 40, "A=HV_BUS, K=RETURN", "label-sm", "start")
    svg += text(scr_x - 12, scr_top - 5, "A", "label-sm")
    svg += text(scr_x - 12, scr_top + 66, "K", "label-sm")
    svg += wire(scr_x, scr_top + 50, scr_x, return_y)
    svg += node_dot(scr_x, return_y)

    # Snubber R9 + C2
    snub_x = 920
    svg += wire(snub_x, hv_bus_y, snub_x, hv_bus_y + 20)
    svg += node_dot(snub_x, hv_bus_y)
    svg += resistor_v(snub_x, hv_bus_y + 20, "R9", "47Ω")
    svg += safety_badge(snub_x + 28, hv_bus_y + 34, 3)
    svg += wire(snub_x, hv_bus_y + 80, snub_x, hv_bus_y + 95)
    svg += cap_v(snub_x, hv_bus_y + 95, "C2", "0.47µF")
    svg += wire(snub_x, hv_bus_y + 125, snub_x, return_y)

    # SCR2 diode-connected output isolation
    svg += wire(hv_bus_end, hv_bus_y, hv_bus_end + 15, hv_bus_y, "wire-bus")
    svg += f'<polygon points="{hv_bus_end+15},{hv_bus_y-16} {hv_bus_end+15},{hv_bus_y+16} {hv_bus_end+41},{hv_bus_y}" fill="#fff" stroke="#333" stroke-width="2"/>\n'
    svg += f'<line x1="{hv_bus_end+44}" y1="{hv_bus_y-18}" x2="{hv_bus_end+44}" y2="{hv_bus_y+18}" stroke="#333" stroke-width="2.5"/>\n'
    svg += wire(hv_bus_end + 44, hv_bus_y, dc_out_x, hv_bus_y)
    svg += node_dot(dc_out_x, hv_bus_y)
    svg += text(hv_bus_end + 32, hv_bus_y - 24, "SCR2 (used as diode)", "label-sm")
    svg += text(hv_bus_end + 32, hv_bus_y - 10, "Forward: HV_BUS → DC_OUT", "label-sm")
    svg += safety_badge(hv_bus_end + 22, hv_bus_y - 34, 10)
    svg += text(dc_out_x + 8, hv_bus_y - 8, "DC_OUT", "label-lg", "start")

    # Output capacitor and load
    svg += wire(dc_out_x, hv_bus_y, dc_out_x, hv_bus_y + 15)
    svg += cap_v(dc_out_x, hv_bus_y + 15, "C_OUT", "1000µF 600V")
    svg += wire(dc_out_x, hv_bus_y + 45, dc_out_x, return_y)

    load_x = 1160
    svg += wire(dc_out_x, hv_bus_y, load_x, hv_bus_y)
    svg += wire(load_x, hv_bus_y, load_x, hv_bus_y + 15)
    svg += resistor_v(load_x, hv_bus_y + 15, "R_LOAD", "330Ω")
    svg += wire(load_x, hv_bus_y + 75, load_x, return_y)

    # =========================================================================
    # CONTROL CHAIN (sensed from DC_OUT)
    # =========================================================================
    ctrl_tap_y = 90
    svg += wire(dc_out_x, hv_bus_y, dc_out_x, ctrl_tap_y, "wire-sense")
    svg += wire(120, ctrl_tap_y, dc_out_x, ctrl_tap_y, "wire-sense")
    svg += text(620, ctrl_tap_y - 8, "DC_OUT feed to sensing divider and local supply", "label-sm")

    bus_y = 120  # local top rail for control chain drawing
    sx = 170     # sensing x
    lx = 370     # local-supply x

    svg += wire(sx, ctrl_tap_y, sx, bus_y, "wire-sense")
    svg += wire(lx, ctrl_tap_y, lx, bus_y, "wire-sense")
    svg += node_dot(sx, bus_y)
    svg += node_dot(lx, bus_y)

    # Sensing divider R1a/R1b/R2 (from DC_OUT)
    svg += resistor_v(sx, bus_y + 30, "R1a", "910kΩ")
    svg += wire(sx, bus_y + 90, sx, bus_y + 105)
    svg += resistor_v(sx, bus_y + 105, "R1b", "910kΩ")
    svg += wire(sx, bus_y + 165, sx, bus_y + 180)
    ref_y = bus_y + 180
    svg += node_dot(sx, ref_y)
    svg += text(sx - 5, ref_y + 16, "REF_NODE", "label-lg", "end")

    svg += wire(sx, ref_y, sx, ref_y + 15)
    svg += resistor_v(sx, ref_y + 15, "R2", "10.15kΩ")
    svg += wire(sx, ref_y + 75, sx, ref_y + 95)
    svg += ground(sx, ref_y + 95)

    # C3 noise filter
    c3_x = sx + 65
    svg += wire(sx, ref_y, c3_x, ref_y)
    svg += wire(c3_x, ref_y, c3_x, ref_y + 15)
    svg += cap_v(c3_x, ref_y + 15, "C3", "1nF")
    svg += safety_badge(c3_x + 16, ref_y + 12, 7)
    svg += wire(c3_x, ref_y + 45, c3_x, ref_y + 65)
    svg += ground(c3_x, ref_y + 65)

    # Local supply from DC_OUT
    svg += resistor_v(lx, bus_y + 30, "R3", "47kΩ")
    svg += wire(lx, bus_y + 90, lx, bus_y + 105)
    svg += safety_badge(lx + 30, bus_y + 56, 8)
    svg += resistor_v(lx, bus_y + 105, "R4", "47kΩ")
    svg += wire(lx, bus_y + 165, lx, bus_y + 180)
    vl_y = bus_y + 180
    svg += node_dot(lx, vl_y)
    svg += text(lx - 5, vl_y - 8, "V_local ~15V", "label-lg", "end")

    svg += wire(lx, vl_y, lx, vl_y + 15)
    svg += zener_v(lx, vl_y + 15, "ZD1", "15V")
    svg += wire(lx, vl_y + 45, lx, vl_y + 65)
    svg += ground(lx, vl_y + 65)

    c1_x = lx + 60
    svg += wire(lx, vl_y, c1_x, vl_y)
    svg += wire(c1_x, vl_y, c1_x, vl_y + 15)
    svg += cap_v(c1_x, vl_y + 15, "C1", "1µF")
    svg += safety_badge(c1_x + 15, vl_y + 12, 9)
    svg += wire(c1_x, vl_y + 45, c1_x, vl_y + 65)
    svg += ground(c1_x, vl_y + 65)

    c4_x = lx + 120
    svg += wire(c1_x, vl_y, c4_x, vl_y)
    svg += wire(c4_x, vl_y, c4_x, vl_y + 15)
    svg += cap_v(c4_x, vl_y + 15, "C4", "100nF")
    svg += wire(c4_x, vl_y + 45, c4_x, vl_y + 65)
    svg += ground(c4_x, vl_y + 65)

    # TL431 stage
    tl_x = 440
    tl_y = vl_y + 100
    r5_x = tl_x
    svg += wire(lx, vl_y, r5_x - 30, vl_y)
    svg += wire(r5_x - 30, vl_y, r5_x - 30, tl_y - 40)
    svg += resistor_v(r5_x - 30, tl_y - 40, "R5", "1kΩ")
    svg += wire(r5_x - 30, tl_y + 20, r5_x - 30, tl_y + 30)

    svg += f'<rect x="{tl_x-40}" y="{tl_y+30}" width="85" height="55" rx="4" class="comp-body"/>\n'
    svg += text(tl_x + 2, tl_y + 52, "TL431", "label-lg")
    svg += text(tl_x + 2, tl_y + 68, "U1", "label-sm")
    svg += wire(tl_x - 40, tl_y + 50, tl_x - 75, tl_y + 50)
    svg += text(tl_x - 58, tl_y + 44, "REF", "label-sm")
    svg += wire(tl_x - 75, tl_y + 50, tl_x - 75, ref_y)
    svg += wire(tl_x - 75, ref_y, sx, ref_y)
    svg += wire(tl_x + 2, tl_y + 30, tl_x + 2, tl_y + 20)
    svg += wire(tl_x + 2, tl_y + 20, r5_x - 30, tl_y + 20)
    cath_node_y = tl_y + 20
    svg += node_dot(tl_x - 3, cath_node_y)
    svg += text(tl_x + 14, tl_y + 18, "CATHODE", "label-sm", "start")
    svg += wire(tl_x + 2, tl_y + 85, tl_x + 2, tl_y + 110)
    svg += text(tl_x + 14, tl_y + 98, "ANODE", "label-sm", "start")
    svg += ground(tl_x + 2, tl_y + 110)

    # PNP driver + gate network
    r6_x = 640
    svg += wire(tl_x - 3, cath_node_y, r6_x, cath_node_y)
    svg += resistor_h(r6_x, cath_node_y, "R6", "1kΩ")
    svg += wire(r6_x + 60, cath_node_y, r6_x + 80, cath_node_y)

    q1_x = r6_x + 110
    q1_y = cath_node_y
    svg += wire(r6_x + 80, q1_y, q1_x - 20, q1_y)
    svg += text(q1_x - 24, q1_y - 6, "B", "label-sm")
    svg += wire(q1_x - 20, q1_y, q1_x - 5, q1_y)
    svg += f'<line x1="{q1_x-5}" y1="{q1_y-25}" x2="{q1_x-5}" y2="{q1_y+25}" stroke="#333" stroke-width="3"/>\n'
    svg += f'<line x1="{q1_x-5}" y1="{q1_y-12}" x2="{q1_x+15}" y2="{q1_y-30}" stroke="#333" stroke-width="2"/>\n'
    svg += f'<polygon points="{q1_x+2},{q1_y-15} {q1_x-2},{q1_y-23} {q1_x+8},{q1_y-21}" fill="#333"/>\n'
    svg += f'<line x1="{q1_x-5}" y1="{q1_y+12}" x2="{q1_x+15}" y2="{q1_y+30}" stroke="#333" stroke-width="2"/>\n'
    svg += wire(q1_x + 15, q1_y - 30, q1_x + 15, q1_y - 50)
    svg += text(q1_x + 22, q1_y - 38, "E", "label-sm", "start")
    svg += wire(q1_x + 15, q1_y - 50, q1_x + 15, vl_y)
    svg += wire(q1_x + 15, vl_y, c4_x, vl_y)
    svg += text(q1_x + 6, q1_y - 2, "Q1", "label-lg", "start")
    svg += text(q1_x + 6, q1_y + 12, "2N2905A PNP", "label-sm", "start")

    # ZD2 clamp
    zd2_x = q1_x - 40
    zd2_y = q1_y - 45
    svg += wire(r6_x + 80, q1_y, r6_x + 80, zd2_y + 30)
    svg += wire(r6_x + 80, zd2_y + 30, zd2_x, zd2_y + 30)
    svg += zener_v(zd2_x, zd2_y, "ZD2", "5.1V")
    svg += safety_badge(zd2_x - 16, zd2_y + 10, 6)
    svg += wire(zd2_x, zd2_y, zd2_x, q1_y - 50)
    svg += wire(zd2_x, q1_y - 50, q1_x + 15, q1_y - 50)

    # Q1 collector -> gate node
    coll_y = q1_y + 30
    svg += wire(q1_x + 15, coll_y, q1_x + 15, coll_y + 20)
    svg += resistor_v(q1_x + 15, coll_y + 20, "R7", "47Ω")
    svg += wire(q1_x + 15, coll_y + 80, q1_x + 15, coll_y + 95)
    gate_y = coll_y + 95
    gate_x = q1_x + 15
    svg += node_dot(gate_x, gate_y)
    svg += text(gate_x - 4, gate_y + 16, "SCR_GATE", "label-lg", "end")

    # R8 and ZD3
    r8_x = gate_x + 50
    svg += wire(gate_x, gate_y, r8_x, gate_y)
    svg += wire(r8_x, gate_y, r8_x, gate_y + 15)
    svg += resistor_v(r8_x, gate_y + 15, "R8", "100Ω")
    svg += safety_badge(r8_x + 28, gate_y + 20, 4)
    svg += wire(r8_x, gate_y + 75, r8_x, gate_y + 95)
    svg += ground(r8_x, gate_y + 95)

    zd3_x = gate_x + 115
    svg += wire(r8_x, gate_y, zd3_x, gate_y)
    svg += wire(zd3_x, gate_y, zd3_x, gate_y + 15)
    svg += zener_v(zd3_x, gate_y + 15, "ZD3", "15V")
    svg += safety_badge(zd3_x + 15, gate_y + 12, 5)
    svg += wire(zd3_x, gate_y + 45, zd3_x, gate_y + 65)
    svg += ground(zd3_x, gate_y + 65)

    # SCR1 gate lead connection (from power section)
    svg += f'<line x1="{scr_x-25}" y1="{scr_top+50}" x2="{scr_x-45}" y2="{scr_top+65}" stroke="#333" stroke-width="2"/>\n'
    svg += text(scr_x - 58, scr_top + 72, "G", "label-sm")
    svg += wire(scr_x - 45, scr_top + 65, scr_x - 45, gate_y)
    svg += wire(scr_x - 45, gate_y, gate_x, gate_y)

    # =========================================================================
    # Legend / notes
    # =========================================================================
    ly = 760
    svg += f'<rect x="30" y="{ly}" width="700" height="180" fill="#f9f9f9" stroke="#ccc" stroke-width="1" rx="6"/>\n'
    svg += text(50, ly + 22, "SAFETY / FUNCTION KEYS", "label-lg", "start")
    features = [
        ("1", "F1A/F1B/F1C: one 3A fuse per phase"),
        ("2", "MOV1 clamps transient spikes at HV_BUS"),
        ("3", "R9+C2 snubber limits SCR1 dv/dt"),
        ("4", "R8 gate shunt improves noise immunity"),
        ("5", "ZD3 protects SCR gate from overvoltage"),
        ("6", "ZD2 protects Q1 base-emitter junction"),
        ("7", "C3 filters sensing noise"),
        ("8", "R1/R3 chains split for HV derating"),
        ("9", "C1+C4 stabilize local supply"),
        ("10", "SCR2 blocks C_OUT reverse discharge"),
    ]
    for i, (num, desc) in enumerate(features):
        row = i % 5
        col = i // 5
        bx = 50 + col * 340
        by = ly + 38 + row * 27
        svg += safety_badge(bx, by, num)
        svg += text(bx + 14, by + 4, desc, "label-sm", "start")

    svg += f'<rect x="760" y="{ly}" width="710" height="180" fill="#fff8e1" stroke="#f57f17" stroke-width="1" rx="6"/>\n'
    svg += text(780, ly + 22, "TOPOLOGY NOTES", "label-lg", "start")
    notes = [
        "Rectifier output node HV_BUS is where crowbar SCR1 is connected.",
        "SCR2 (second device in dual-SCR module) is used as a diode from HV_BUS to DC_OUT.",
        "C_OUT = 1000µF / 600V is on DC_OUT and is isolated from reverse dump into crowbar path.",
        "Sensing divider and local supply are fed from DC_OUT (protected node).",
        "This schematic matches simulation/crowbar_circuit.cir refined topology.",
    ]
    for i, p in enumerate(notes):
        svg += text(780, ly + 48 + i * 24, p, "label-sm", "start")

    svg += svg_footer()
    return svg


def main():
    block_svg = generate_block_diagram()
    block_path = OUTPUT_DIR / "block_diagram.svg"
    block_path.write_text(block_svg)
    print(f"Block diagram saved: {block_path}")

    detail_svg = generate_detailed_schematic()
    detail_path = OUTPUT_DIR / "crowbar_schematic.svg"
    detail_path.write_text(detail_svg)
    print(f"Detailed schematic saved: {detail_path}")


if __name__ == "__main__":
    main()
