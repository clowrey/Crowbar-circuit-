#!/usr/bin/env python3
"""Generate SVG diagrams for the refined 3-phase crowbar design."""

from html import escape
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent


def svg_header(width: int, height: int, title: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" font-family="Arial, Helvetica, sans-serif">
<title>{escape(title)}</title>
<defs>
  <marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">
    <polygon points="0,0 10,4 0,8" fill="#263238"/>
  </marker>
  <style>
    .bg {{ fill: #fafafa; }}
    .box {{ fill: #ffffff; stroke: #263238; stroke-width: 2; rx: 10; }}
    .box-power {{ fill: #fff3e0; stroke: #e65100; stroke-width: 2; rx: 10; }}
    .box-control {{ fill: #e3f2fd; stroke: #1565c0; stroke-width: 2; rx: 10; }}
    .box-driver {{ fill: #fce4ec; stroke: #ad1457; stroke-width: 2; rx: 10; }}
    .box-output {{ fill: #e8f5e9; stroke: #2e7d32; stroke-width: 2; rx: 10; }}
    .zone {{ fill-opacity: 0.22; stroke-dasharray: 6,4; stroke-width: 1.5; rx: 12; }}
    .zone-power {{ fill: #ffe0b2; stroke: #ef6c00; }}
    .zone-control {{ fill: #bbdefb; stroke: #1565c0; }}
    .wire {{ stroke: #263238; stroke-width: 2.2; fill: none; }}
    .wire-bus {{ stroke: #c62828; stroke-width: 3.2; fill: none; }}
    .wire-dashed {{ stroke: #455a64; stroke-width: 2; stroke-dasharray: 8,5; fill: none; }}
    .arrow {{ marker-end: url(#arrow); }}
    .node {{ fill: #263238; }}
    .title {{ font-size: 28px; fill: #111; font-weight: 700; }}
    .subtitle {{ font-size: 14px; fill: #37474f; }}
    .h1 {{ font-size: 16px; fill: #111; font-weight: 700; }}
    .h2 {{ font-size: 13px; fill: #111; font-weight: 700; }}
    .label {{ font-size: 12px; fill: #263238; }}
    .small {{ font-size: 11px; fill: #455a64; }}
    .note {{ font-size: 12px; fill: #4e342e; }}
    .warn {{ fill: #fff8e1; stroke: #ef6c00; stroke-width: 1.7; rx: 8; }}
  </style>
</defs>
"""


def svg_footer() -> str:
    return "</svg>\n"


def t(x: float, y: float, text: str, cls: str = "label", anchor: str = "middle") -> str:
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{escape(text)}</text>\n'


def rect(x: float, y: float, w: float, h: float, cls: str = "box", rx: int = 10) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="{cls}" rx="{rx}"/>\n'


def line(x1: float, y1: float, x2: float, y2: float, cls: str = "wire", arrow: bool = False) -> str:
    arrow_cls = " arrow" if arrow else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}{arrow_cls}"/>\n'


def node(x: float, y: float, r: float = 3.8) -> str:
    return f'<circle cx="{x}" cy="{y}" r="{r}" class="node"/>\n'


def block(svg: list[str], x: float, y: float, w: float, h: float, title: str, lines: list[str], cls: str) -> None:
    svg.append(rect(x, y, w, h, cls))
    svg.append(t(x + w / 2, y + 26, title, "h2"))
    for i, item in enumerate(lines):
        svg.append(t(x + w / 2, y + 46 + i * 15, item, "small"))


def generate_block_diagram() -> str:
    """Generate high-level block diagram for the refined topology."""
    width, height = 1440, 680
    svg: list[str] = [svg_header(width, height, "3-Phase Crowbar Block Diagram")]
    svg.append(rect(0, 0, width, height, "bg", rx=0))

    svg.append(t(720, 42, "Crowbar Overvoltage Protection - Refined Front End", "title"))
    svg.append(t(720, 66, "240V L-L 3-Phase Input | F1A/F1B/F1C 3A | SCR2 Output Isolation", "subtitle"))

    y = 110
    h = 92
    blocks = [
        (40, 220, "3-Phase Input", ["240V line-to-line", "A/B/C phases"], "box-power"),
        (300, 190, "Per-Phase Fusing", ["F1A, F1B, F1C", "3A each"], "box-power"),
        (530, 200, "6-Diode Bridge", ["D1..D6 rectifier", "AC to DC"], "box-power"),
        (770, 210, "HV_BUS", ["Rectifier + crowbar node", "MOV + SCR1 + snubber"], "box-power"),
        (1020, 210, "SCR2 as Diode", ["Forward: HV_BUS -> DC_OUT", "Reverse blocked"], "box-output"),
        (1270, 130, "DC_OUT", ["C_OUT 1000uF, 600V", "Protected load bus"], "box-output"),
    ]
    for x, w, title, lines_, cls in blocks:
        block(svg, x, y, w, h, title, lines_, cls)

    # Main path arrows
    ymid = y + h / 2
    path_points = [(260, 300), (490, 530), (730, 770), (980, 1020), (1230, 1270)]
    for x1, x2 in path_points:
        svg.append(line(x1, ymid, x2, ymid, "wire", arrow=True))

    # Crowbar branch
    block(svg, 760, 250, 220, 90, "SCR1 Crowbar Path", ["SCR1 (dual module)", "HV_BUS to return"], "box-driver")
    block(svg, 1010, 250, 220, 90, "RC + MOV Protection", ["R9=47R, C2=0.47uF", "MOV1 clamp"], "box-power")
    svg.append(line(875, 202, 875, 250, "wire-bus"))
    svg.append(line(875, 295, 875, 360, "wire-bus"))
    svg.append(line(1120, 202, 1120, 250, "wire"))
    svg.append(line(720, 360, 1320, 360, "wire"))
    svg.append(t(1330, 364, "Return / GND bus", "small", "start"))

    # Control chain
    block(svg, 90, 430, 310, 100, "Voltage Sense", ["R1a + R1b + R2", "C3 filter", "Trip at ~450V"], "box-control")
    block(svg, 430, 430, 290, 100, "Local Rail", ["R3 + R4 + ZD1", "C1 + C4 decoupling"], "box-control")
    block(svg, 760, 420, 320, 120, "TL431 + Q1 Driver", ["TL431 compares REF", "Q1 drives SCR1 gate"], "box-driver")
    block(svg, 1110, 435, 270, 90, "Gate Network", ["R7, R8, ZD2, ZD3"], "box-driver")

    # Control arrows
    svg.append(line(1335, 202, 1335, 430, "wire"))
    svg.append(line(1335, 430, 245, 430, "wire"))
    svg.append(line(245, 430, 245, 429, "wire"))
    svg.append(line(400, 480, 430, 480, "wire", arrow=True))
    svg.append(line(720, 480, 760, 480, "wire", arrow=True))
    svg.append(line(1080, 480, 1110, 480, "wire", arrow=True))
    svg.append(line(1245, 435, 920, 340, "wire-dashed", arrow=True))
    svg.append(t(935, 370, "SCR1 gate drive", "small"))

    # Note callout
    svg.append(rect(80, 575, 1280, 78, "warn"))
    svg.append(t(95, 602, "Key refinement:", "h2", "start"))
    svg.append(t(95, 624, "SCR2 is used as an output diode so C_OUT cannot discharge backward through the crowbar after SCR1 fires.", "note", "start"))
    svg.append(t(95, 644, "Simulation now shows HV_BUS collapse while DC_OUT remains elevated and decays through load.", "note", "start"))

    svg.append(svg_footer())
    return "".join(svg)


def generate_detailed_schematic() -> str:
    """Generate netlist-aligned schematic SVG."""
    width, height = 1660, 980
    svg: list[str] = [svg_header(width, height, "Crowbar Circuit - Netlist Aligned Schematic")]
    svg.append(rect(0, 0, width, height, "bg", rx=0))

    svg.append(t(830, 44, "Crowbar Overvoltage Protection - Netlist Aligned Schematic", "title"))
    svg.append(t(830, 68, "3-Phase 240V L-L input | F1A/F1B/F1C 3A | SCR1 crowbar + SCR2 output isolation", "subtitle"))

    # Zones
    svg.append(rect(24, 90, 1612, 340, "zone zone-power"))
    svg.append(rect(24, 450, 1612, 300, "zone zone-control"))
    svg.append(t(42, 112, "Power path", "h2", "start"))
    svg.append(t(42, 472, "Control and trip path", "h2", "start"))

    # Main power path blocks
    block(svg, 50, 145, 210, 95, "3-Phase Source", ["A, B, C phases", "240V line-to-line"], "box-power")
    block(svg, 300, 145, 210, 95, "Phase Fuses", ["F1A, F1B, F1C", "3A each"], "box-power")
    block(svg, 550, 145, 220, 95, "Bridge Rectifier", ["D1..D6", "3-phase 6-pulse"], "box-power")
    block(svg, 820, 145, 220, 95, "HV_BUS", ["Crowbar node", "V_isense at rect_pos->hv_bus"], "box-power")
    block(svg, 1085, 145, 250, 95, "SCR2 as Diode", ["B_scr_diode", "Forward HV_BUS->DC_OUT"], "box-output")
    block(svg, 1370, 145, 240, 95, "DC_OUT", ["C_OUT 1000uF / 600V", "R_LOAD to return"], "box-output")

    # Main flow arrows
    ymid = 192
    svg.append(line(260, ymid, 300, ymid, "wire", True))
    svg.append(line(510, ymid, 550, ymid, "wire", True))
    svg.append(line(770, ymid, 820, ymid, "wire", True))
    svg.append(line(1040, ymid, 1085, ymid, "wire", True))
    svg.append(line(1335, ymid, 1370, ymid, "wire", True))

    # Node markers
    for nx in [820, 1040, 1085, 1335, 1370]:
        svg.append(node(nx, ymid))

    # Branches off HV_BUS
    block(svg, 760, 280, 200, 90, "MOV1 Clamp", ["Across HV_BUS to return", "480V class"], "box-power")
    block(svg, 980, 275, 210, 110, "SCR1 Crowbar", ["A=HV_BUS, K=return", "G=scr_gate"], "box-driver")
    block(svg, 1230, 280, 200, 90, "Snubber", ["R9 47R + C2 0.47uF", "Across SCR1 path"], "box-power")

    svg.append(line(930, 240, 930, 275, "wire-bus"))
    svg.append(line(930, 240, 860, 280, "wire"))
    svg.append(line(930, 240, 1330, 280, "wire"))
    svg.append(line(1085, 240, 1085, 275, "wire"))

    # Return bus
    return_y = 412
    svg.append(line(560, return_y, 1540, return_y, "wire-bus"))
    svg.append(t(1550, return_y + 4, "Return / rectifier negative / ground reference", "small", "start"))
    svg.append(line(860, 370, 860, return_y, "wire"))
    svg.append(line(1085, 385, 1085, return_y, "wire-bus"))
    svg.append(line(1330, 370, 1330, return_y, "wire"))
    for nx in [860, 1085, 1330]:
        svg.append(node(nx, return_y))

    # Output branch
    block(svg, 1370, 275, 240, 110, "Output Stage", ["C_OUT = 1000uF, 600V", "R_LOAD = 330R (simulation)"], "box-output")
    svg.append(line(1490, 240, 1490, 275, "wire"))
    svg.append(line(1490, 385, 1490, return_y, "wire"))

    # Isolation note
    svg.append(rect(1005, 425, 605, 62, "warn"))
    svg.append(t(1020, 450, "SCR2 isolation behavior:", "h2", "start"))
    svg.append(t(1020, 470, "When SCR1 crowbars HV_BUS, SCR2 blocks reverse current so C_OUT does not discharge into crowbar.", "note", "start"))

    # Control chain
    block(svg, 80, 520, 340, 145, "Sensing Network (from DC_OUT)", ["R1a 910k + R1b 910k", "R2 10.15k and C3 1nF", "REF node to TL431"], "box-control")
    block(svg, 460, 520, 320, 145, "Local Supply (from DC_OUT)", ["R3 47k + R4 47k", "ZD1 15V, C1 1uF, C4 100nF"], "box-control")
    block(svg, 820, 505, 400, 175, "TL431 + Driver", ["TL431 cathode via R5", "Q1 PNP via R6 + ZD2 clamp", "R7 drives SCR gate"], "box-driver")
    block(svg, 1260, 525, 320, 140, "SCR Gate Net", ["R8 gate shunt", "ZD3 gate clamp", "scr_gate -> SCR1"], "box-driver")

    # Feed control from DC_OUT
    svg.append(line(1490, 240, 1490, 505, "wire"))
    svg.append(line(1490, 505, 250, 505, "wire"))
    svg.append(line(250, 505, 250, 520, "wire"))
    svg.append(line(620, 505, 620, 520, "wire"))
    svg.append(node(250, 505))
    svg.append(node(620, 505))
    svg.append(t(1498, 500, "DC_OUT sense/supply tap", "small", "start"))

    # Control flow arrows
    svg.append(line(420, 590, 460, 590, "wire", True))
    svg.append(line(780, 590, 820, 590, "wire", True))
    svg.append(line(1220, 590, 1260, 590, "wire", True))
    svg.append(line(1370, 525, 1085, 390, "wire-dashed", True))
    svg.append(t(1215, 470, "gate drive to SCR1", "small"))

    # Design notes
    svg.append(rect(80, 785, 1540, 165, "box"))
    svg.append(t(100, 812, "Design notes", "h2", "start"))
    notes = [
        "1) Topology is aligned to simulation/crowbar_circuit.cir (3-phase bridge, dual-SCR usage).",
        "2) SCR1 performs crowbar on HV_BUS (pre-isolation); SCR2 is used as a diode from HV_BUS to DC_OUT.",
        "3) DC_OUT is the protected node with 600V/1000uF capacitor hold-up.",
        "4) Per-phase 3A fuses are explicitly shown ahead of the bridge.",
        "5) During fault trip, HV_BUS collapses while DC_OUT remains isolated from crowbar back-discharge.",
    ]
    for idx, note_text in enumerate(notes):
        svg.append(t(100, 835 + idx * 24, note_text, "label", "start"))

    svg.append(svg_footer())
    return "".join(svg)


def main() -> None:
    block_path = OUTPUT_DIR / "block_diagram.svg"
    detail_path = OUTPUT_DIR / "crowbar_schematic.svg"

    block_path.write_text(generate_block_diagram())
    print(f"Block diagram saved: {block_path}")

    detail_path.write_text(generate_detailed_schematic())
    print(f"Detailed schematic saved: {detail_path}")


if __name__ == "__main__":
    main()
