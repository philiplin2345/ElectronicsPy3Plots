# Common Base Amplifier Analyzer

Interactive visualization tool for analyzing common base BJT amplifier circuits.

## Overview

The Common Base Amplifier is a transistor configuration known for its high voltage gain and wide bandwidth. Unlike the Common Emitter, it has a very low input impedance and a current gain slightly less than unity. This interactive analyzer helps you understand how component values affect circuit performance, including DC operating point, AC gain, and frequency response.

## File

**`cb_analyzer.py`** - Main analyzer with interactive controls

## Features

### Circuit Analysis
- **DC Operating Point (Q-Point)**: Calculates and displays collector current (IC), base current (IB), and collector-emitter voltage (VCE)
- **Voltage Divider Biasing**: Uses RB1 and RB2 for stable biasing (Base is AC grounded)
- **Visual Circuit Schematic**: Real-time circuit diagram with component values

### Frequency Response
- **Voltage Gain vs Frequency**: Shows how voltage amplification varies across the frequency spectrum. Note the non-inverting nature.
- **Current Gain vs Frequency**: Displays current amplification characteristics (typically < 0 dB).
- **Power Gain vs Frequency**: Combines voltage and current gain for total power transfer analysis.

### Interactive Controls
Adjust the following parameters in real-time:
- **RC** (1-10 kΩ): Collector resistor - affects voltage gain and Q-point
- **RB1** (10-200 kΩ): Upper bias resistor - sets base voltage
- **RE** (0.1-5 kΩ): Emitter resistor - provides DC stability and sets bias current
- **RL** (1-20 kΩ): Load resistor - affects output voltage swing and gain
- **VCC** (5-24 V): Supply voltage - determines maximum output swing
- **β (hFE)** (50-300): Transistor current gain
- **Cin** (0.1-100 μF): Input coupling capacitor - creates high-pass filter at the Emitter
- **Cout** (0.1-100 μF): Output coupling capacitor - blocks DC from load
- **CB** (1-1000 μF): Base bypass capacitor - grounds the base for AC signals

## Usage

```bash
python cb_analyzer.py
```

Once running, use the sliders at the bottom of the window to adjust component values and observe:
- How the circuit schematic updates with new values
- Changes in the Q-point (operating point)
- Frequency response curves shifting in real-time

## Key Concepts Demonstrated

### 1. Common Base Configuration
- **Input**: Applied to the Emitter.
- **Output**: Taken from the Collector.
- **Base**: Grounded for AC signals (via CB).
- This configuration eliminates the Miller effect, providing better high-frequency response than Common Emitter.

### 2. Base Bypass Capacitor (CB)
- Crucial for the Common Base operation.
- **With CB** (at sufficient frequency): The base is effectively grounded, resulting in low input impedance and high voltage gain.
- **Without CB** (or at low frequencies): The base impedance increases, altering the amplifier characteristics significantly.

### 3. Input Impedance
- The Common Base amplifier has a very low input impedance ($Z_{in} \approx r_e$).
- This makes it suitable for matching low-impedance sources (like antennas) but requires a large coupling capacitor ($C_{in}$) to avoid low-frequency attenuation.

### 4. Gain Characteristics
- **Voltage Gain**: High, non-inverting. $A_v \approx R_C / r_e$.
- **Current Gain**: Less than unity ($\alpha \approx 1$).
- **Power Gain**: Moderate (roughly equal to voltage gain since current gain is ~1).

## Gain Calculations - Detailed Explanation

The analyzer calculates three types of gain at each frequency: voltage gain, current gain, and power gain.

### Step 1: DC Operating Point (Q-Point)
Identical to the Common Emitter voltage divider bias:
```
VB = VCC × RB2 / (RB1 + RB2)
VE = VB - VBE
IE = VE / RE
IC ≈ IE
VCE = VC - VE
```

### Step 2: AC Small-Signal Parameters
```
re = VT / IE                           # AC emitter resistance
Rc_eff = RC || RL                      # Effective collector load
Z_base_eff = (RB1 || RB2) || Zc_b      # Base impedance to ground
```
Ideally, `Z_base_eff` should be close to 0 due to `CB`.

### Step 3: Input Impedance
Looking into the emitter:
```
Zin_emitter = re + Z_base_eff / (β + 1)
Rin = RE || Zin_emitter
```
Because `re` is small (e.g., 26Ω at 1mA), `Rin` is very low.

### Step 4: Voltage Gain
```
Av_base = Rc_eff / Zin_emitter
```
This assumes the signal is at the emitter node. The input coupling capacitor $C_{in}$ forms a voltage divider with $R_{in}$.

### Step 5: Current Gain
```
Ai = α × (RE / (RE + Zin_emitter)) × (RC / (RC + RL))
```
Typically slightly less than 1 (0 dB).

## Educational Applications

- **RF Amplifiers**: Understanding why CB is used in high-frequency radio applications.
- **Impedance Matching**: Demonstrating buffering for low-impedance sources.
- **Cascode Configurations**: The CB stage forms the upper half of a Cascode amplifier.
