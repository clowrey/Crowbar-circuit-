#!/usr/bin/env python3
"""
Generate circuit schematics using schemdraw.

Uses the schemdraw library (https://schemdraw.readthedocs.io/) which provides
proper IEC/IEEE electronic component symbols. Much cleaner than hand-rolling SVG.

Dependencies: pip install schemdraw matplotlib
"""

import schemdraw
import schemdraw.elements as elm
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent


def draw_detailed_schematic():
    """Draw the full crowbar circuit with proper EE symbols."""

    with schemdraw.Drawing(show=False, fontsize=12) as d:
        d.config(unit=4, inches_per_unit=0.5)

        # ================================================================
        # HV BUS — horizontal rail across the top
        # ================================================================
        hv_origin = d.here
        bus = d.add(elm.Line().right(24).linewidth(3).color('#b71c1c'))
        d.add(elm.Label().at(hv_origin).label('HV Bus (+)', loc='top',
              fontsize=14).color('#b71c1c'))

        # Save key tap points along the bus
        # We'll place taps at known x-offsets from origin
        bus_y = hv_origin[1]

        def bus_tap(x_offset):
            return (hv_origin[0] + x_offset, bus_y)

        # ================================================================
        # TAP 1: MOV (x=1)
        # ================================================================
        d.here = bus_tap(1)
        d.add(elm.Dot())
        d.add(elm.Line().down(0.5))
        d.add(elm.ResistorVarIEC().down().label('MOV1\n480V', loc='right'))
        d.add(elm.Ground())

        # ================================================================
        # TAP 2: SENSING DIVIDER (x=4)
        # ================================================================
        d.here = bus_tap(4)
        d.add(elm.Dot())
        d.add(elm.Line().down(0.5))
        R1a = d.add(elm.ResistorIEC().down().label('R1a\n910kΩ', loc='right'))
        R1b = d.add(elm.ResistorIEC().down().label('R1b\n910kΩ', loc='right'))
        ref_pt = d.here
        d.add(elm.Dot())

        # R2 + VR1 continue down
        d.add(elm.ResistorIEC().down().label('R2\n10kΩ', loc='right'))
        d.add(elm.PotentiometerIEC().down().flip()
              .label('VR1\n1kΩ', loc='right'))
        d.add(elm.Ground())

        # C3 noise filter (branch right from REF node)
        d.here = ref_pt
        d.add(elm.Line().right(2))
        d.add(elm.Capacitor().down().label('C3\n1nF', loc='right'))
        d.add(elm.Ground())

        # Label REF node
        d.add(elm.Label().at(ref_pt).label('REF', loc='left', fontsize=12))

        # ================================================================
        # TAP 3: LOCAL 15V SUPPLY (x=9)
        # ================================================================
        d.here = bus_tap(9)
        d.add(elm.Dot())
        d.add(elm.Line().down(0.5))
        d.add(elm.ResistorIEC().down().label('R3\n47kΩ 2W', loc='right'))
        d.add(elm.ResistorIEC().down().label('R4\n47kΩ 2W', loc='right'))
        vlocal_pt = d.here
        d.add(elm.Dot())

        # ZD1 zener to GND
        d.add(elm.Zener().down().label('ZD1\n15V', loc='right'))
        d.add(elm.Ground())

        # Label V_local
        d.add(elm.Label().at(vlocal_pt).label('V_local', loc='left',
              fontsize=12))

        # C1 and C4 branch right from V_local
        d.here = vlocal_pt
        d.add(elm.Line().right(2))
        c1_pt = d.here
        d.add(elm.Capacitor().down().label('C1\n1µF', loc='right'))
        d.add(elm.Ground())

        d.here = c1_pt
        d.add(elm.Line().right(2))
        c4_pt = d.here
        d.add(elm.Capacitor().down().label('C4\n100nF', loc='right'))
        d.add(elm.Ground())

        # ================================================================
        # R5 + TL431 (below V_local)
        # ================================================================
        # R5 from V_local node going down
        d.here = vlocal_pt
        d.add(elm.Line().down(5))
        r5_top = d.here
        R5 = d.add(elm.ResistorIEC().down().label('R5\n1kΩ', loc='right'))
        tl431_cath_pt = d.here
        d.add(elm.Dot())

        # TL431 as a labeled box using Ic
        d.add(elm.Line().down(1))
        tl431 = d.add(elm.Ic(
            pins=[elm.IcPin(name='REF', side='left', pin='1'),
                  elm.IcPin(name='K', side='top', pin='2'),
                  elm.IcPin(name='A', side='bot', pin='3')],
            size=(2.5, 3),
            plblofst=0.15,
            botlabel='TL431 (U1)',
        ).anchor('pin2'))

        # TL431 anode → GND
        d.add(elm.Line().at(tl431.pin3).down(0.5))
        d.add(elm.Ground())

        # TL431 REF ← REF node (horizontal connection)
        ref_wire_y = tl431.pin1[1]
        d.add(elm.Line().at(tl431.pin1).left().tox(ref_pt[0]))
        d.add(elm.Line().toy(ref_pt[1]))
        d.add(elm.Dot())

        # ================================================================
        # PNP GATE DRIVER: R6 → Q1 → R7 → Gate
        # ================================================================
        # R6 from TL431 cathode going right
        d.here = tl431_cath_pt
        d.add(elm.Line().right(3))
        R6 = d.add(elm.ResistorIEC().right().label('R6\n1kΩ', loc='top'))

        # Q1 PNP transistor
        Q1 = d.add(elm.BjtPnp(circle=True).anchor('base')
                    .label('Q1\n2N2905A', loc='right', fontsize=10))

        # Q1 emitter → up to V_local rail
        d.add(elm.Line().at(Q1.emitter).up().toy(c4_pt[1]))
        d.add(elm.Line().tox(c4_pt[0]))
        d.add(elm.Dot())

        # ZD2: V_EB clamp (from Q1 base up to emitter rail)
        base_pt = Q1.base
        d.here = base_pt
        d.add(elm.Line().left(1))
        zd2_bottom = d.here
        d.add(elm.Zener().up().toy(Q1.emitter[1])
              .label('ZD2\n5.1V', loc='left'))
        d.add(elm.Line().right().tox(Q1.emitter[0]))
        d.add(elm.Dot())

        # Q1 collector → R7 → Gate node
        d.here = Q1.collector
        d.add(elm.Line().down(0.5))
        R7 = d.add(elm.ResistorIEC().down().label('R7\n47Ω', loc='right'))
        gate_pt = d.here
        d.add(elm.Dot())

        # R8 gate-cathode shunt (right from gate, then down)
        d.add(elm.Line().right(2))
        r8_top = d.here
        d.add(elm.ResistorIEC().down().label('R8\n100Ω', loc='right'))
        d.add(elm.Ground())

        # ZD3 gate clamp (further right)
        d.here = r8_top
        d.add(elm.Line().right(2))
        d.add(elm.Zener().down().label('ZD3\n15V', loc='right'))
        d.add(elm.Ground())

        # Label gate
        d.add(elm.Label().at(gate_pt).label('GATE', loc='left', fontsize=11))

        # ================================================================
        # TAP 4: SCR (x=19)
        # ================================================================
        d.here = bus_tap(19)
        d.add(elm.Dot())
        SCR1 = d.add(elm.SCR().down().label('SCR1\n250A\n≥800V', loc='right',
                      fontsize=11))
        d.add(elm.Ground())

        # SCR gate ← Gate node
        d.add(elm.Line().at(SCR1.gate).left().tox(gate_pt[0]))
        d.add(elm.Line().toy(gate_pt[1]))
        d.add(elm.Dot())

        # ================================================================
        # TAP 5: SNUBBER (x=22)
        # ================================================================
        d.here = bus_tap(22)
        d.add(elm.Dot())
        d.add(elm.Line().down(0.5))
        d.add(elm.ResistorIEC().down().label('R9\n47Ω 5W', loc='right'))
        d.add(elm.Capacitor().down().label('C2\n0.47µF\n630V', loc='right'))
        d.add(elm.Ground())

        # ================================================================
        # FUSE + LOAD (far right of bus)
        # ================================================================
        d.here = bus_tap(14)
        d.add(elm.Dot())
        d.add(elm.Line().up(1.5))
        d.add(elm.FuseIEC().right(4).label('F1  300A  500VDC', loc='top'))
        d.add(elm.Line().right(2)
              .label('→ LOAD (+)', loc='right', fontsize=13))

        # Save outputs
        svg_path = OUTPUT_DIR / 'crowbar_schematic.svg'
        png_path = OUTPUT_DIR / 'crowbar_schematic.png'
        d.save(str(svg_path))
        d.save(str(png_path), dpi=200)
        print(f"Schematic: {svg_path}")
        print(f"Schematic: {png_path}")


def draw_block_diagram():
    """Draw a high-level block diagram."""

    with schemdraw.Drawing(show=False, fontsize=12) as d:
        d.config(unit=4, inches_per_unit=0.5)

        # Row 1: HV Source → Fuse → Bus → Load
        d.add(elm.RBox(w=5, h=2).anchor('center').label('HV Source\n(≤500V)'))
        src_end = d.here
        d.add(elm.Arrow().right(2))
        d.add(elm.FuseIEC().right().label('F1\n300A', loc='top'))
        d.add(elm.Arrow().right(1.5))
        bus_pt = d.here
        d.add(elm.Dot(radius=0.2).label('HV\nBus', loc='top', fontsize=13))
        d.add(elm.Arrow().right(4))
        d.add(elm.RBox(w=5, h=2).anchor('center').label('Protected\nLoad'))

        # Column down from bus
        d.here = bus_pt
        d.add(elm.Line().down(3))
        col1 = d.here

        # MOV (left branch)
        d.here = col1
        d.add(elm.Line().left(4))
        d.add(elm.ResistorVarIEC().down().label('MOV1\n480V', loc='right'))
        d.add(elm.Ground())

        # Sensing divider (slight left)
        d.here = col1
        d.add(elm.Line().left(1))
        d.add(elm.ResistorIEC().down().label('R1a+R1b\n1.82MΩ', loc='right'))
        d.add(elm.ResistorIEC().down().label('R2+VR1\n10.15kΩ', loc='right'))
        d.add(elm.Ground())
        div_mid = d.here  # we'll come back for TL431
        # The divider midpoint is between the two resistors
        # Let me add TL431 branching from a saved point

        # Sensing → TL431 → PNP → SCR chain
        d.here = col1
        d.add(elm.Line().down(4))
        d.add(elm.Line().right(3))
        d.add(elm.RBox(w=4, h=2).anchor('center')
              .label('TL431\nVref=2.495V'))
        tl431_end = d.here
        d.add(elm.Arrow().right(3).label('cathode', loc='top', fontsize=10))
        d.add(elm.RBox(w=4, h=2).anchor('center')
              .label('PNP Driver\nQ1'))
        pnp_end = d.here
        d.add(elm.Arrow().right(3).label('gate', loc='top', fontsize=10))
        d.add(elm.RBox(w=4, h=2).anchor('center')
              .label('SCR\n250A'))
        scr_end = d.here

        # SCR up to bus
        d.add(elm.Line().up().toy(bus_pt[1]))
        d.add(elm.Line().left().tox(bus_pt[0]))
        d.add(elm.Dot())

        # Snubber (right of SCR)
        d.here = scr_end
        d.add(elm.Line().right(3))
        d.add(elm.ResistorIEC().down().label('R9', loc='right'))
        d.add(elm.Capacitor().down().label('C2', loc='right'))
        d.add(elm.Ground())

        # Local supply feeds PNP (from bus down)
        d.here = bus_pt
        d.add(elm.Line().right(4))
        d.add(elm.Dot())
        d.add(elm.Line().down(2))
        d.add(elm.ResistorIEC().down().label('R3+R4\n94kΩ', loc='right'))
        d.add(elm.Zener().down().label('ZD1\n15V', loc='right'))
        d.add(elm.Ground())

        svg_path = OUTPUT_DIR / 'block_diagram.svg'
        png_path = OUTPUT_DIR / 'block_diagram.png'
        d.save(str(svg_path))
        d.save(str(png_path), dpi=200)
        print(f"Block diagram: {svg_path}")
        print(f"Block diagram: {png_path}")


if __name__ == "__main__":
    print("Generating schematics with schemdraw...")
    draw_detailed_schematic()
    draw_block_diagram()
    print("Done.")
