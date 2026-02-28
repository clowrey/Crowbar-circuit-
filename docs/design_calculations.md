# Design Calculations

## 1. Voltage Sensing Divider (R1, R2)

The TL431 internal reference voltage is 2.495V. The resistor divider scales the HV bus voltage to match this reference at the desired trigger point.

### Divider Equation

```
V_trigger = V_ref × (1 + R1/R2)
```

Where:
- `V_ref` = 2.495V (TL431 internal reference)
- `V_trigger` = 450V (desired trip point)

### Solving for R1/R2 Ratio

```
R1/R2 = (V_trigger / V_ref) - 1
R1/R2 = (450 / 2.495) - 1
R1/R2 = 180.36 - 1
R1/R2 = 179.36
```

### Component Selection

**R1 = 1.82MΩ** (two 910kΩ resistors in series for voltage derating):
- Each resistor sees ≤225V (well within 500V rating of standard 1206/through-hole)
- Standard E24 value: 910kΩ

**R2 = 10kΩ fixed + 1kΩ trimmer (VR1)**:
- Allows adjustment range: 415V to 457V
- Set trimmer to ~150Ω for 10.15kΩ total

### Exact Trigger Voltage

```
V_trigger = 2.495 × (1 + 1,820,000 / 10,150)
V_trigger = 2.495 × (1 + 179.31)
V_trigger = 2.495 × 180.31
V_trigger = 449.9V
```

### Power Dissipation

At 450V:
```
I_divider = 450V / (1.82MΩ + 10.15kΩ) = 0.246mA
P_R1a = (0.246mA)² × 910kΩ = 55mW  (use ¼W minimum)
P_R1b = (0.246mA)² × 910kΩ = 55mW  (use ¼W minimum)
P_R2  = (0.246mA)² × 10.15kΩ = 0.6mW  (negligible)
```

### Trimmer Adjustment Range

| R2 Total | Trigger Voltage |
|----------|----------------|
| 10.0kΩ   | 456.6V         |
| 10.15kΩ  | 449.9V (target)|
| 10.5kΩ   | 436.2V         |
| 11.0kΩ   | 415.4V         |

---

## 2. Local 15V Power Supply (R3, R4, ZD1)

### Design Requirements

- Supply voltage for gate driver: 12–15V
- Current requirement: ~5mA steady-state (TL431 bias + PNP leakage)
- Gate trigger current: ~100mA pulse (provided by C1)

### Resistor Selection

**R3 + R4 = 94kΩ** (two 47kΩ for voltage derating):

At 400V nominal bus:
```
I_supply = (400V - 15V) / 94kΩ = 4.1mA
P_R3 = (4.1mA)² × 47kΩ = 0.79W → use 2W rated
P_R4 = (4.1mA)² × 47kΩ = 0.79W → use 2W rated
```

Each resistor sees ≤225V — adequate voltage derating.

### Zener (ZD1) Selection

- ZD1: 15V, 1W (e.g., 1N4744A)
- Zener current: 4.1mA (within rated range)
- Power: 15V × 4.1mA = 62mW (well within 1W rating)

### Energy Storage Capacitor (C1)

For SCR gate trigger pulse (~100mA for ~1ms):
```
Q = I × t = 100mA × 1ms = 100µC
ΔV = Q / C = 100µC / 1µF = 100V  (far exceeds available 15V)
```

Wait — 1µF is insufficient for 100mA × 1ms at 15V. But the R3/R4 supply also provides continuous current during the trigger:
```
I_continuous = 4.1mA
I_from_cap = 100mA - 4.1mA = 95.9mA
ΔV = 95.9mA × 1ms / 1µF = 95.9V
```

The capacitor would be fully drained. However, the SCR gate trigger is very fast (<100µs for modern SCRs), so:
```
t_trigger ≈ 50µs
ΔV = 95.9mA × 50µs / 1µF = 4.8V (15V → 10.2V)
```

This is acceptable — the PNP driver can still function at 10V V_local.

**For more conservative design**, increase C1 to 10µF:
```
ΔV = 95.9mA × 50µs / 10µF = 0.48V (15V → 14.5V)
```

### Startup Time Constant

```
τ = (R3 + R4) × C1 = 94kΩ × 1µF = 94ms
```

Local supply reaches 63% (9.5V) in 94ms, and 95% (14.25V) in ~280ms. This is acceptable for a circuit that powers up over hundreds of milliseconds.

---

## 3. TL431 Operating Conditions

### Bias Current

The TL431 requires minimum cathode current of 1mA for regulation.

With R5 = 1kΩ pull-up to V_local (15V):
```
When ON:  I_cathode = (15V - 2.5V) / 1kΩ = 12.5mA  ✓ (above 1mA minimum)
When OFF: I_cathode ≈ 0mA (no conduction path)
```

### Cathode Power Dissipation

```
P_TL431 = V_cathode × I_cathode = 2.5V × 12.5mA = 31.3mW
```

Well within the TL431's 350mW power rating (SOT-23 package).

---

## 4. PNP Gate Driver (Q1 = 2N2905A)

### Operating Points

**TL431 OFF (V_bus < 450V):**
```
V(tl431_cath) ≈ V_local = 15V (pulled up by R5)
V(q1_base) ≈ 15V (through R6)
V_EB = V_local - V_base = 15V - 15V = 0V
Q1 is OFF → I_collector = 0 → V(scr_gate) = 0V  ✓
```

**TL431 ON (V_bus ≥ 450V):**
```
V(tl431_cath) ≈ 2.5V
V_EB = 15V - 2.5V = 12.5V → clamped by ZD2 to 5.1V
V(q1_base) = 15V - 5.1V = 9.9V

I_base = (9.9V - 2.5V) / R6 = 7.4V / 1kΩ = 7.4mA
  (split between Q1 base junction and ZD2)

I_collector(max) = β × I_base ≈ 120 × 4mA = 480mA (saturated)

Actual I_collector limited by R7 + R8 network:
V_CE(sat) ≈ 0.3V
I_gate = (V_local - V_CE - V_gate_drop) / R7
       ≈ (15 - 0.3 - 1.5) / 47 = 281mA
```

### SCR Gate Current

Through the R7/R8 divider network:
```
V_gate = V_local × R8 / (R7 + R8) × (1 - correction)
       ≈ (15 - 0.3) × 100 / (47 + 100) = 10.0V (with Q1 saturated)

Actual gate voltage limited by SCR gate-cathode characteristic (~1-2V):
I_gate = (V_collector - V_GK) / R7 ≈ (15 - 0.3 - 1.5) / 47 ≈ 281mA
```

This exceeds typical SCR I_GT (gate trigger current) of 50–150mA for large SCRs. ✓

---

## 5. SCR Parameters

### Key Ratings Required

| Parameter | Minimum Rating | Notes |
|-----------|---------------|-------|
| V_DRM / V_RRM | 600V | Must exceed max bus voltage with margin |
| I_T(AV) | 250A | Continuous current rating (per spec) |
| I_TSM | >5,000A | Single-cycle surge must exceed fuse I²t |
| I_GT | <200mA | Must be below available gate drive |
| dv/dt | >100V/µs | Or use snubber to reduce dv/dt |

### Recommended Part

**Vishay VS-T7201630** (or equivalent):
- V_DRM: 1600V (good margin above 450V)
- I_T(AV): 250A
- I_TSM: 6,300A (10ms, half-sine)
- Hockey-puck package

---

## 6. RC Snubber (R9, C2)

### Purpose

Limits dv/dt across the SCR to prevent false triggering from fast voltage transients.

### Design Criteria

SCR dv/dt rating: typically 200–500V/µs for high-current types.

Target dv/dt < 100V/µs (conservative):
```
dv/dt = V_peak / (R × C)
100V/µs = 450V / (R × C)
R × C = 4.5µs
```

Selected: R9 = 47Ω, C2 = 0.47µF:
```
τ = 47 × 0.47µ = 22.1µs
dv/dt(peak) = 450 / 22.1µs = 20.4V/µs  ✓ (well below SCR rating)
```

### Snubber Power Dissipation (at switching)

```
P_snubber = ½ × C × V² × f
```

In a crowbar circuit (single-shot event), continuous power dissipation is zero. The snubber only dissipates energy during the initial voltage transient and the crowbar event itself.

Peak energy: `½ × 0.47µF × 450² = 47.6mJ` (absorbed by R9).

---

## 7. Fuse Coordination

### Fuse I²t Rating

The fuse must clear before the SCR's I²t limit is exceeded.

Example fuse: **Bussmann FWH-300A** (500VDC semiconductor fuse):
- Clearing I²t: ~50,000 A²s (typical for 300A semiconductor fuse)
- Total clearing time at 4,725A: t = I²t / I² = 50,000 / 4,725² = 2.24ms

SCR I²t limit (Vishay VS-T7201630): ~200,000 A²s (half-cycle at I_TSM):
```
SCR I²t = I_TSM² × t_half / 2 = 6,300² × 0.01 / 2 = 198,450 A²s
```

**Coordination check:**
```
Fuse I²t (50,000) << SCR I²t (198,450)  ✓
```

The fuse blows well before the SCR is damaged.
