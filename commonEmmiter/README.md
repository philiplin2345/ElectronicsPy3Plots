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

## Circuit Equations

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
