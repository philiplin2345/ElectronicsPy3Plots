# Common Emitter Amplifier Analyzer

Interactive visualization tool for analyzing common emitter BJT amplifier circuits.

## Overview

The Common Emitter Amplifier is one of the most fundamental transistor amplifier configurations. This interactive analyzer helps you understand how component values affect circuit performance, including DC operating point, AC gain, and frequency response.

## File

**`ce_analyzer.py`** - Main analyzer with interactive controls

## Features

### Circuit Analysis
- **DC Operating Point (Q-Point)**: Calculates and displays collector current (IC), base current (IB), and collector-emitter voltage (VCE)
- **Voltage Divider Biasing**: Uses RB1 and RB2 for stable biasing
- **Visual Circuit Schematic**: Real-time circuit diagram with component values

### Frequency Response
- **Voltage Gain vs Frequency**: Shows how voltage amplification varies across the frequency spectrum
- **Current Gain vs Frequency**: Displays current amplification characteristics
- **Power Gain vs Frequency**: Combines voltage and current gain for total power transfer analysis

### Interactive Controls
Adjust the following parameters in real-time:
- **RC** (1-10 kΩ): Collector resistor - affects voltage gain and Q-point
- **RB1** (10-200 kΩ): Upper bias resistor - sets base voltage
- **RE** (0.1-5 kΩ): Emitter resistor - provides DC stability and affects AC gain
- **RL** (1-20 kΩ): Load resistor - affects output voltage swing
- **VCC** (5-24 V): Supply voltage - determines maximum output swing
- **β (hFE)** (50-300): Transistor current gain
- **Cin** (0.1-100 μF): Input coupling capacitor - creates high-pass filter
- **Cout** (0.1-100 μF): Output coupling capacitor - blocks DC from load
- **CE** (1-1000 μF): Emitter bypass capacitor - increases AC gain at mid/high frequencies

## Usage

```bash
python ce_analyzer.py
```

Once running, use the sliders at the bottom of the window to adjust component values and observe:
- How the circuit schematic updates with new values
- Changes in the Q-point (operating point)
- Frequency response curves shifting in real-time

## Key Concepts Demonstrated

### 1. Biasing
The voltage divider bias network (RB1, RB2) sets the base voltage, which determines the DC operating point. Proper biasing ensures:
- The transistor operates in the active region
- Maximum output voltage swing without clipping
- Stable operation despite temperature variations

### 2. Emitter Bypass Capacitor (CE)
- **Without CE** (or at low frequencies): RE is in the AC signal path, reducing gain
- **With CE** (at high frequencies): CE shorts RE for AC signals, significantly increasing gain
- Creates a frequency-dependent gain characteristic

### 3. Coupling Capacitors (Cin, Cout)
- Block DC voltages while passing AC signals
- Create high-pass filters with cutoff frequencies determined by capacitance and circuit impedances
- Cin works with input impedance; Cout works with output impedance

### 4. Frequency Response
The amplifier gain varies with frequency due to:
- **Low frequencies**: Coupling and bypass capacitors have high impedance
- **Mid frequencies**: Capacitors act as short circuits, maximum gain achieved
- **High frequencies**: Transistor internal capacitances cause gain rolloff (not modeled in this simplified version)

### 5. Load Effects
The load resistor (RL) in parallel with the collector resistor (RC) reduces the effective AC load, which:
- Decreases voltage gain
- Increases output current capability
- Affects the overall power transfer

## Gain Calculations - Detailed Explanation

The analyzer calculates three types of gain at each frequency: voltage gain, current gain, and power gain. Here's how each is computed step-by-step.

### Step 1: DC Operating Point (Q-Point)

First, we calculate the DC bias point using voltage divider biasing:

```
VB = VCC × RB2 / (RB1 + RB2)          # Base voltage from divider
VE = VB - VBE                          # Emitter voltage (VBE ≈ 0.7V)
IE = VE / RE                           # Emitter current
IC ≈ IE                                # Collector current (for high β)
IB = IC / β                            # Base current
VC = VCC - IC × RC                     # Collector voltage
VCE = VC - VE                          # Collector-emitter voltage
```

### Step 2: AC Small-Signal Parameters

These are frequency-independent AC parameters:

```
re = VT / IE                           # AC emitter resistance (VT = 26mV)
Rc_eff = RC || RL                      # Effective collector load (parallel)
       = (RC × RL) / (RC + RL)
Rb_parallel = RB1 || RB2               # Bias network equivalent
```

### Step 3: Frequency-Dependent Impedances

At each frequency `f`, capacitors have impedance:

```
Zc_in = 1 / (2π × f × Cin)            # Input coupling capacitor
Zc_out = 1 / (2π × f × Cout)          # Output coupling capacitor  
Zc_e = 1 / (2π × f × CE)              # Emitter bypass capacitor
```

**Effective emitter impedance** (RE in parallel with CE):
```
Ze_eff = (RE × Zc_e) / √(RE² + Zc_e²)
```

At low frequencies: Zc_e is large → Ze_eff ≈ RE (low gain)
At high frequencies: Zc_e is small → Ze_eff ≈ 0 (high gain)

### Step 4: Input Circuit Analysis

```
Rin_base = β × (re + Ze_eff)          # Resistance looking into base
Rin = Rb_parallel || Rin_base         # Total input resistance
fc_in = 1 / (2π × Rin × Cin)          # Input cutoff frequency
```

**Input Coupling Capacitor Response:**
```
Cin_response = (f / fc_in) / √(1 + (f / fc_in)²)
```

This is a critical factor that affects BOTH voltage and current gain:
- At f << fc_in: Cin_response ≈ 0 (signal blocked)
- At f = fc_in: Cin_response ≈ 0.707 (-3dB point)
- At f >> fc_in: Cin_response ≈ 1 (signal passes fully)

**Why it affects both gains:** The coupling capacitor forms a high-pass filter that attenuates both the input voltage AND input current at low frequencies. Think of it as a frequency-dependent valve that restricts both "pressure" (voltage) and "flow" (current) equally.

### Step 5: Voltage Gain Calculation

```
Av_base = Rc_eff / (re + Ze_eff)      # Base voltage gain (mid-band)
Av = Av_base × Cin_response            # Apply coupling capacitor effect
Av_dB = 20 × log₁₀(Av)                # Convert to decibels
```

**Physical meaning:**
- Larger Rc_eff → higher gain (more voltage drop across collector)
- Smaller (re + Ze_eff) → higher gain (less emitter degeneration)
- Cin_response reduces gain at low frequencies

### Step 6: Current Gain Calculation

```
current_division = Rin_base / (Rb_parallel + Rin_base)
output_division = RC / (RC + RL)
Ai = β × current_division × output_division × Cin_response
Ai_dB = 20 × log₁₀(Ai)
```

**Breaking it down:**
- **β**: Transistor's intrinsic current gain
- **current_division**: Input current splits between bias resistors and base
  - More goes to base when Rin_base is large (high Ze_eff)
- **output_division**: Collector current splits between RC and RL
  - More goes to load when RL is large
- **Cin_response**: Same factor as voltage gain - reduces current at low frequencies

**Why Cin_response affects current gain:** At low frequencies, the coupling capacitor has high impedance (Zc_in = 1/(2πfC) is large), which blocks current flow just as it blocks voltage. Both the input voltage and input current are attenuated by the same factor.

### Step 7: Power Gain Calculation

```
Ap = Av × Ai                           # Power gain (linear domain)
Ap_dB = 10 × log₁₀(Ap)                # Convert to decibels
```

Note: Power gain uses 10× (not 20×) because power is proportional to voltage squared.

### Frequency Response Summary

| Frequency Range | Cin_response | Ze_eff | Voltage Gain | Current Gain |
|----------------|--------------|---------|--------------|--------------|
| Very Low (< fc_in) | ~0 | ~RE | Very Low | Moderate |
| Low (≈ fc_in) | ~0.7 | Decreasing | Increasing | Decreasing |
| Mid-band | ~1 | ~0 | Maximum | Lower |
| High | ~1 | ~0 | Maximum | Lower |

**Key insights:**
1. **Voltage gain** increases with frequency (until mid-band) due to:
   - Cin_response increasing (coupling capacitor passes signal)
   - Ze_eff decreasing (bypass capacitor shorts RE)

2. **Current gain** peaks at low-to-mid frequencies because:
   - Increases with Cin_response (coupling effect)
   - Decreases as Ze_eff drops (lower input impedance → more current shunted by bias resistors)

3. **Power gain** is the product of both, typically maximizing in the mid-band region

## Circuit Equations Reference

### DC Analysis (Q-Point)
```
VB = VCC × RB2 / (RB1 + RB2)
VE = VB - VBE (where VBE ≈ 0.7V)
IE = VE / RE
IC ≈ IE (for high β)
IB = IC / β
VC = VCC - IC × RC
VCE = VC - VE
```

### AC Analysis (Gain)
```
re = VT / IE (where VT = 26mV at room temperature)
Rc_eff = RC || RL (parallel combination)
Av ≈ -Rc_eff / (re + Ze_eff)
```

Where `Ze_eff` is the effective emitter impedance (RE bypassed by CE at high frequencies).

## Example Calculations

For detailed step-by-step calculations at specific frequencies (1 Hz, 10 Hz, 100 Hz, 1 kHz, 10 kHz) using the default circuit values, see [gain_calculations_example.md](gain_calculations_example.md).

This document shows:
- All intermediate values
- Numerical results at each step
- How gains vary across the frequency spectrum
- Why the frequency response has its characteristic shape


## Learning Objectives

After using this tool, you should understand:
1. How to bias a common emitter amplifier for linear operation
2. The role of each component in the circuit
3. Why amplifier gain varies with frequency
4. The tradeoff between gain and stability (emitter degeneration)
5. How to design for specific gain and bandwidth requirements

## Tips for Exploration

1. **Start with default values** and observe the baseline performance
2. **Vary one parameter at a time** to see its isolated effect
3. **Try extreme values** to see circuit limitations (e.g., very low RE can cause saturation)
4. **Compare CE values**: Try 1 μF vs 1000 μF to see the dramatic effect on low-frequency gain
5. **Experiment with biasing**: Adjust RB1 to see how it affects the Q-point and available headroom

## Educational Applications

- **Electronics courses**: Demonstrates BJT amplifier theory
- **Lab preparation**: Predict circuit behavior before breadboarding
- **Design exercises**: Find component values for specific gain/bandwidth targets
- **Troubleshooting practice**: Understand what happens when components are out of spec
