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
    W, H = 1200, 900
    svg = svg_header(W, H, "Crowbar Circuit — Detailed Schematic")

    # Background
    svg += '<rect width="1200" height="900" fill="#fefefe" rx="0"/>\n'

    # Title block
    svg += '<rect x="820" y="830" width="370" height="60" fill="#f5f5f5" stroke="#222" stroke-width="1.5"/>\n'
    svg += text(1005, 852, "CROWBAR OVERVOLTAGE PROTECTION", "label-lg")
    svg += text(1005, 870, "450V · 250A SCR · TL431", "label-sm")
    svg += text(1005, 885, "Rev 1.0", "label-sm")

    # Functional zone backgrounds
    svg += f'<rect x="20" y="65" width="250" height="270" class="zone-sense"/>\n'
    svg += text(145, 82, "VOLTAGE SENSING", "label-sm")
    svg += f'<rect x="290" y="65" width="250" height="430" class="zone-supply"/>\n'
    svg += text(415, 82, "LOCAL SUPPLY + TL431", "label-sm")
    svg += f'<rect x="560" y="65" width="280" height="430" class="zone-driver"/>\n'
    svg += text(700, 82, "GATE DRIVER + SCR", "label-sm")
    svg += f'<rect x="860" y="65" width="320" height="270" class="zone-power"/>\n'
    svg += text(1020, 82, "POWER STAGE", "label-sm")

    # ===== HV BUS (horizontal line at top) =====
    bus_y = 110
    svg += wire(30, bus_y, 1160, bus_y, "wire-bus")
    svg += text(50, bus_y - 8, "HV Bus (+)", "label-lg", "start")

    # ===== FUSE (top right) =====
    svg += fuse_h(950, bus_y, "F1", "300A / 500VDC")
    svg += safety_badge(950, bus_y - 18, 1)
    svg += text(1070, bus_y - 8, "→ LOAD (+)", "label-lg", "start")

    # ===== MOV (far left, from bus to GND) =====
    mov_x = 70
    svg += wire(mov_x, bus_y, mov_x, bus_y + 20)
    svg += node_dot(mov_x, bus_y)
    # MOV symbol (simplified as rectangle with ~ inside)
    svg += f'<rect x="{mov_x-15}" y="{bus_y+20}" width="30" height="45" rx="3" class="comp-body"/>\n'
    svg += text(mov_x, bus_y + 39, "~", "label-lg")
    svg += text(mov_x, bus_y + 50, "~", "label-lg")
    svg += text(mov_x + 22, bus_y + 33, "MOV1", "label-sm", "start")
    svg += text(mov_x + 22, bus_y + 48, "480V", "label-sm", "start")
    svg += safety_badge(mov_x - 18, bus_y + 18, 2)
    svg += wire(mov_x, bus_y + 65, mov_x, bus_y + 90)
    svg += ground(mov_x, bus_y + 90)

    # ===== SENSING DIVIDER (left column) =====
    sx = 170  # sensing x
    svg += wire(sx, bus_y, sx, bus_y + 30)
    svg += node_dot(sx, bus_y)

    # R1a
    svg += resistor_v(sx, bus_y + 30, "R1a", "910kΩ ½W")
    svg += wire(sx, bus_y + 90, sx, bus_y + 105)

    # R1b
    svg += resistor_v(sx, bus_y + 105, "R1b", "910kΩ ½W")
    svg += wire(sx, bus_y + 165, sx, bus_y + 180)

    # Junction node (REF)
    ref_y = bus_y + 180
    svg += node_dot(sx, ref_y)
    svg += text(sx - 5, ref_y + 16, "REF", "label-lg", "end")

    # R2 below junction
    svg += wire(sx, ref_y, sx, ref_y + 15)
    svg += resistor_v(sx, ref_y + 15, "R2", "10kΩ")
    svg += wire(sx, ref_y + 75, sx, ref_y + 85)

    # VR1 trimmer (shown as resistor with arrow)
    svg += resistor_v(sx, ref_y + 85, "VR1", "1kΩ trim")
    svg += f'<line x1="{sx-15}" y1="{ref_y+115}" x2="{sx+15}" y2="{ref_y+100}" stroke="#333" stroke-width="1.5"/>\n'
    svg += f'<polygon points="{sx+13},{ref_y+98} {sx+18},{ref_y+104} {sx+11},{ref_y+103}" fill="#333"/>\n'
    svg += safety_badge(sx + 30, ref_y + 115, 10)
    svg += wire(sx, ref_y + 145, sx, ref_y + 165)
    svg += ground(sx, ref_y + 165)

    # C3 noise filter (parallel to R2)
    c3_x = sx + 65
    svg += wire(sx, ref_y, c3_x, ref_y)
    svg += wire(c3_x, ref_y, c3_x, ref_y + 15)
    svg += cap_v(c3_x, ref_y + 15, "C3", "1nF")
    svg += safety_badge(c3_x + 15, ref_y + 12, 7)
    svg += wire(c3_x, ref_y + 45, c3_x, ref_y + 65)
    svg += ground(c3_x, ref_y + 65)

    # ===== LOCAL SUPPLY (center column) =====
    lx = 370  # local supply x
    svg += wire(lx, bus_y, lx, bus_y + 30)
    svg += node_dot(lx, bus_y)

    # R3
    svg += resistor_v(lx, bus_y + 30, "R3", "47kΩ 2W")
    svg += wire(lx, bus_y + 90, lx, bus_y + 105)
    svg += safety_badge(lx + 30, bus_y + 55, 8)

    # R4
    svg += resistor_v(lx, bus_y + 105, "R4", "47kΩ 2W")
    svg += wire(lx, bus_y + 165, lx, bus_y + 180)

    # V_local node
    vl_y = bus_y + 180
    svg += node_dot(lx, vl_y)
    svg += text(lx - 5, vl_y - 8, "V_local (15V)", "label-lg", "end")

    # ZD1 (zener to GND)
    svg += wire(lx, vl_y, lx, vl_y + 15)
    svg += zener_v(lx, vl_y + 15, "ZD1", "15V 1W")
    svg += wire(lx, vl_y + 45, lx, vl_y + 65)
    svg += ground(lx, vl_y + 65)

    # C1 (bulk cap)
    c1_x = lx + 60
    svg += wire(lx, vl_y, c1_x, vl_y)
    svg += wire(c1_x, vl_y, c1_x, vl_y + 15)
    svg += cap_v(c1_x, vl_y + 15, "C1", "1µF 25V")
    svg += safety_badge(c1_x + 15, vl_y + 12, 9)
    svg += wire(c1_x, vl_y + 45, c1_x, vl_y + 65)
    svg += ground(c1_x, vl_y + 65)

    # C4 (decoupling)
    c4_x = lx + 120
    svg += wire(c1_x, vl_y, c4_x, vl_y)
    svg += wire(c4_x, vl_y, c4_x, vl_y + 15)
    svg += cap_v(c4_x, vl_y + 15, "C4", "100nF 25V")
    svg += wire(c4_x, vl_y + 45, c4_x, vl_y + 65)
    svg += ground(c4_x, vl_y + 65)

    # ===== TL431 =====
    tl_x = 420
    tl_y = vl_y + 100

    # R5 from V_local to TL431 cathode
    r5_x = tl_x
    svg += wire(lx, vl_y, lx, vl_y - 15)  # short up
    svg += wire(lx, vl_y, r5_x - 30, vl_y)
    svg += wire(r5_x - 30, vl_y, r5_x - 30, tl_y - 40)
    svg += resistor_v(r5_x - 30, tl_y - 40, "R5", "1kΩ")
    svg += wire(r5_x - 30, tl_y + 20, r5_x - 30, tl_y + 30)

    # TL431 box
    svg += f'<rect x="{tl_x-40}" y="{tl_y+30}" width="80" height="55" rx="4" class="comp-body"/>\n'
    svg += text(tl_x, tl_y + 52, "TL431", "label-lg")
    svg += text(tl_x, tl_y + 68, "U1", "label-sm")

    # TL431 pins
    # REF (left)
    svg += wire(tl_x - 40, tl_y + 50, tl_x - 70, tl_y + 50)
    svg += text(tl_x - 55, tl_y + 44, "REF", "label-sm")
    # Connect REF to sensing divider
    svg += wire(tl_x - 70, tl_y + 50, tl_x - 70, ref_y)
    svg += wire(tl_x - 70, ref_y, sx, ref_y)

    # Cathode (top)
    svg += wire(tl_x, tl_y + 30, tl_x, tl_y + 20)
    svg += wire(tl_x, tl_y + 20, r5_x - 30, tl_y + 20)
    cath_node_y = tl_y + 20
    svg += node_dot(tl_x - 5, cath_node_y)
    svg += text(tl_x + 10, tl_y + 18, "CATHODE", "label-sm", "start")

    # Anode (bottom to GND)
    svg += wire(tl_x, tl_y + 85, tl_x, tl_y + 110)
    svg += text(tl_x + 10, tl_y + 98, "ANODE", "label-sm", "start")
    svg += ground(tl_x, tl_y + 110)

    # ===== PNP GATE DRIVER =====
    # R6 from TL431 cathode to Q1 base
    r6_x = 600
    r6_y = cath_node_y
    svg += wire(tl_x - 5, cath_node_y, r6_x, cath_node_y)
    svg += resistor_h(r6_x, cath_node_y, "R6", "1kΩ")
    svg += wire(r6_x + 60, cath_node_y, r6_x + 80, cath_node_y)

    # Q1 PNP transistor
    q1_x = r6_x + 110
    q1_y = cath_node_y
    # Base connection
    svg += wire(r6_x + 80, q1_y, q1_x - 20, q1_y)
    svg += text(q1_x - 25, q1_y - 6, "B", "label-sm")

    # Transistor symbol (PNP)
    svg += wire(q1_x - 20, q1_y, q1_x - 5, q1_y)  # base lead
    svg += f'<line x1="{q1_x-5}" y1="{q1_y-25}" x2="{q1_x-5}" y2="{q1_y+25}" stroke="#333" stroke-width="3"/>\n'  # base bar
    # Emitter (top, with arrow pointing IN for PNP)
    svg += f'<line x1="{q1_x-5}" y1="{q1_y-12}" x2="{q1_x+15}" y2="{q1_y-30}" stroke="#333" stroke-width="2"/>\n'
    svg += f'<polygon points="{q1_x+2},{q1_y-15} {q1_x-2},{q1_y-23} {q1_x+8},{q1_y-21}" fill="#333"/>\n'
    # Collector (bottom)
    svg += f'<line x1="{q1_x-5}" y1="{q1_y+12}" x2="{q1_x+15}" y2="{q1_y+30}" stroke="#333" stroke-width="2"/>\n'

    # Emitter connection to V_local
    svg += wire(q1_x + 15, q1_y - 30, q1_x + 15, q1_y - 50)
    svg += text(q1_x + 22, q1_y - 38, "E", "label-sm", "start")
    svg += text(q1_x + 22, q1_y - 52, "→ V_local", "label-sm", "start")
    # Connect to V_local bus
    svg += wire(q1_x + 15, q1_y - 50, q1_x + 15, vl_y)
    svg += wire(q1_x + 15, vl_y, c4_x, vl_y)

    svg += text(q1_x + 5, q1_y - 2, "Q1", "label-lg", "start")
    svg += text(q1_x + 5, q1_y + 12, "2N2905A", "label-sm", "start")
    svg += text(q1_x + 5, q1_y + 23, "PNP", "label-sm", "start")

    # ZD2 (V_EB clamp from base to emitter)
    zd2_x = q1_x - 40
    zd2_y = q1_y - 45
    svg += wire(r6_x + 80, q1_y, r6_x + 80, zd2_y + 30)
    svg += wire(r6_x + 80, zd2_y + 30, zd2_x, zd2_y + 30)
    svg += zener_v(zd2_x, zd2_y, "ZD2", "5.1V")
    svg += safety_badge(zd2_x - 18, zd2_y + 10, 6)
    svg += wire(zd2_x, zd2_y, zd2_x, q1_y - 50)
    svg += wire(zd2_x, q1_y - 50, q1_x + 15, q1_y - 50)

    # Collector → R7 → Gate
    coll_y = q1_y + 30
    svg += text(q1_x + 22, coll_y + 5, "C", "label-sm", "start")
    svg += wire(q1_x + 15, coll_y, q1_x + 15, coll_y + 20)
    svg += resistor_v(q1_x + 15, coll_y + 20, "R7", "47Ω ½W")
    svg += wire(q1_x + 15, coll_y + 80, q1_x + 15, coll_y + 95)

    # Gate node
    gate_y = coll_y + 95
    gate_x = q1_x + 15
    svg += node_dot(gate_x, gate_y)
    svg += text(gate_x - 5, gate_y + 16, "SCR GATE", "label-lg", "end")

    # R8 gate-cathode shunt
    r8_x = gate_x + 50
    svg += wire(gate_x, gate_y, r8_x, gate_y)
    svg += wire(r8_x, gate_y, r8_x, gate_y + 15)
    svg += resistor_v(r8_x, gate_y + 15, "R8", "100Ω")
    svg += safety_badge(r8_x + 30, gate_y + 20, 4)
    svg += wire(r8_x, gate_y + 75, r8_x, gate_y + 95)
    svg += ground(r8_x, gate_y + 95)

    # ZD3 gate overvoltage clamp
    zd3_x = gate_x + 110
    svg += wire(r8_x, gate_y, zd3_x, gate_y)
    svg += wire(zd3_x, gate_y, zd3_x, gate_y + 15)
    svg += zener_v(zd3_x, gate_y + 15, "ZD3", "15V 1W")
    svg += safety_badge(zd3_x + 15, gate_y + 12, 5)
    svg += wire(zd3_x, gate_y + 45, zd3_x, gate_y + 65)
    svg += ground(zd3_x, gate_y + 65)

    # ===== SCR =====
    scr_x = 950
    scr_top = bus_y + 40

    # SCR connection to HV bus
    svg += wire(scr_x, bus_y, scr_x, scr_top)
    svg += node_dot(scr_x, bus_y)

    # SCR symbol (triangle with gate line)
    svg += f'<polygon points="{scr_x-25},{scr_top} {scr_x+25},{scr_top} {scr_x},{scr_top+50}" fill="#fff" stroke="#333" stroke-width="2"/>\n'
    svg += f'<line x1="{scr_x-25}" y1="{scr_top+50}" x2="{scr_x+25}" y2="{scr_top+50}" stroke="#333" stroke-width="3"/>\n'
    # Gate lead
    svg += f'<line x1="{scr_x-25}" y1="{scr_top+50}" x2="{scr_x-45}" y2="{scr_top+65}" stroke="#333" stroke-width="2"/>\n'
    svg += wire(scr_x - 45, scr_top + 65, scr_x - 45, gate_y)
    svg += wire(scr_x - 45, gate_y, gate_x, gate_y)

    svg += text(scr_x + 30, scr_top + 10, "SCR1", "label-lg", "start")
    svg += text(scr_x + 30, scr_top + 25, "250A", "label-sm", "start")
    svg += text(scr_x + 30, scr_top + 38, "≥800V", "label-sm", "start")
    svg += text(scr_x - 10, scr_top - 5, "A", "label-sm")
    svg += text(scr_x - 55, scr_top + 68, "G", "label-sm")
    svg += text(scr_x - 10, scr_top + 65, "K", "label-sm")

    # SCR cathode to GND
    svg += wire(scr_x, scr_top + 50, scr_x, scr_top + 85)
    svg += ground(scr_x, scr_top + 85)
    svg += text(scr_x + 30, scr_top + 70, "→ LOAD (–) / GND", "label-sm", "start")

    # ===== SNUBBER =====
    snub_x = 1080
    svg += wire(snub_x, bus_y, snub_x, bus_y + 30)
    svg += node_dot(snub_x, bus_y)
    svg += resistor_v(snub_x, bus_y + 30, "R9", "47Ω 5W")
    svg += safety_badge(snub_x + 30, bus_y + 45, 3)
    svg += wire(snub_x, bus_y + 90, snub_x, bus_y + 105)
    svg += cap_v(snub_x, bus_y + 105, "C2", "0.47µF 630V")
    svg += wire(snub_x, bus_y + 135, snub_x, bus_y + 160)
    svg += ground(snub_x, bus_y + 160)

    # ===== LEGEND =====
    ly = 580
    svg += f'<rect x="30" y="{ly}" width="540" height="200" fill="#f9f9f9" stroke="#ccc" stroke-width="1" rx="6"/>\n'
    svg += text(50, ly + 20, "SAFETY FEATURES", "label-lg", "start")

    features = [
        ("1", "F1 — 300A Fuse: interrupts current after crowbar fires"),
        ("2", "MOV1 — 480V varistor: fast transient absorption (<1ns)"),
        ("3", "R9+C2 — RC Snubber: dv/dt protection for SCR"),
        ("4", "R8 — Gate-cathode shunt: noise immunity"),
        ("5", "ZD3 — Gate zener: overvoltage protection"),
        ("6", "ZD2 — V_EB clamp: protects PNP driver"),
        ("7", "C3 — Noise filter: rejects HF on sensing divider"),
        ("8", "R1a/R1b, R3/R4 — Split resistors: voltage derating"),
        ("9", "C1+C4 — Supply decoupling: clean gate trigger pulse"),
        ("10", "VR1 — Trimmer: precise threshold adjustment (415–457V)"),
    ]
    for i, (num, desc) in enumerate(features):
        row = i % 5
        col = i // 5
        bx = 50 + col * 270
        by = ly + 35 + row * 32
        svg += safety_badge(bx, by, num)
        svg += text(bx + 15, by + 4, desc, "label-sm", "start")

    # ===== NOTES =====
    svg += f'<rect x="600" y="{ly}" width="570" height="200" fill="#fff8e1" stroke="#f57f17" stroke-width="1" rx="6"/>\n'
    svg += text(620, ly + 20, "DESIGN PARAMETERS", "label-lg", "start")
    params = [
        "Trigger voltage: 449.9V (R1/R2 ratio 179.3:1)",
        "TL431 Vref: 2.495V (internal bandgap)",
        "SCR gate current: ~100mA from PNP driver",
        "Sensing current: 0.25mA (low power)",
        "Response time: <100µs (TL431 + PNP + SCR)",
        "Peak surge current: ~4,725A (fuse blows in <3ms)",
        "Fuse I²t (50kA²s) << SCR I²t (198kA²s) ✓",
    ]
    for i, p in enumerate(params):
        svg += text(620, ly + 42 + i * 22, p, "label-sm", "start")

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
