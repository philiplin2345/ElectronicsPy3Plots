# Thevenin Theorem Applications

Interactive demonstrations of Thevenin's theorem and related circuit analysis concepts.

## Overview

This module contains visualizations that demonstrate practical applications of Thevenin's theorem, including clamper circuits and maximum power transfer. These tools help build intuition about circuit analysis techniques and nonlinear circuit behavior.

## Files

### 1. `clamper.py` - Clamper Circuit Visualization

Simulates and visualizes positive and negative clamper circuits, showing realistic transient behavior.

#### What is a Clamper?
A clamper circuit shifts the DC level of an AC signal without changing its shape. Unlike clippers that cut off portions of the waveform, clampers add or subtract a DC offset.

#### Features
- **Positive Clamper**: Shifts waveform so positive peaks are clamped near +0.7V
- **Negative Clamper**: Shifts waveform so negative peaks are clamped near -0.7V
- **Transient Behavior**: Shows realistic charging behavior from initial uncharged state to steady-state
- **Side-by-side Comparison**: Both clamper types displayed simultaneously

#### Circuit Parameters
```python
f = 100 Hz              # Input frequency
Vin_peak = 5.0 V        # Input amplitude
Vd = 0.7 V              # Diode forward voltage drop
R = 1000 Ω              # Series resistor
C = 4.7 μF              # Clamping capacitor
```

#### How It Works
1. **Positive Clamper**: 
   - Diode conducts when input voltage exceeds capacitor voltage + diode drop
   - Capacitor charges during positive peaks
   - Output is shifted downward so positive peak ≈ +Vd

2. **Negative Clamper**:
   - Diode conducts when input voltage falls below capacitor voltage - diode drop
   - Capacitor charges during negative peaks
   - Output is shifted upward so negative peak ≈ -Vd

#### Key Observations
- **Transient Period**: Initial cycles show gradual shift as capacitor charges
- **Steady State**: After several cycles, DC level stabilizes
- **Time Constant**: τ = RC determines charging speed (4.7 ms in this example)
- **Waveform Preservation**: AC component remains unchanged, only DC level shifts

#### Usage
```bash
python clamper.py
```

#### Learning Objectives
- Understand DC level shifting without waveform distortion
- Observe capacitor charging dynamics in nonlinear circuits
- Distinguish between transient and steady-state behavior
- Learn practical applications (video signal processing, voltage level shifting)

---

### 2. `resTHMaxPower.py` - Maximum Power Transfer Theorem

Demonstrates the maximum power transfer theorem using Thevenin equivalent circuits.

#### Theorem Statement
**Maximum power is transferred from a source to a load when the load resistance equals the Thevenin equivalent resistance of the source.**

Mathematically: **P_max occurs when R_L = R_th**

#### Features
- **Power vs Load Resistance**: Plots power delivered across wide range of load values
- **Logarithmic Scale**: Shows behavior from 0.1Ω to 10kΩ for comprehensive view
- **Maximum Point Highlighted**: Clearly marks where R_L = R_th
- **Quantitative Analysis**: Calculates exact maximum power value

#### Circuit Parameters
```python
V_th = 10.0 V           # Thevenin equivalent voltage
R_th = 50.0 Ω           # Thevenin equivalent resistance
R_L = 0.1 to 10,000 Ω   # Load resistance range
```

#### Power Equation
```
P = V_th² × R_L / (R_th + R_L)²
```

#### Key Insights from the Plot

1. **R_L << R_th** (left side of curve):
   - Most voltage drops across R_th
   - Little power delivered to load
   - Current is high but voltage across load is low

2. **R_L = R_th** (peak):
   - Voltage divides equally between source and load
   - Maximum power transfer achieved
   - Efficiency is exactly 50%

3. **R_L >> R_th** (right side of curve):
   - Most voltage appears across load
   - Current is very small
   - Power decreases despite high voltage

#### Usage
```bash
python resTHMaxPower.py
```

You can modify the parameters at the top of the script:
```python
V_th = 10.0    # Change source voltage
R_th = 50.0    # Change source resistance
```

#### Learning Objectives
- Understand maximum power transfer conditions
- Visualize the tradeoff between voltage and current
- Learn why impedance matching is crucial in RF and audio systems
- Recognize that maximum power transfer ≠ maximum efficiency

#### Practical Applications
- **RF Systems**: Antenna impedance matching (typically 50Ω or 75Ω)
- **Audio Systems**: Speaker impedance matching to amplifier output
- **Power Systems**: Generator and transmission line matching
- **Battery Design**: Internal resistance considerations for maximum power delivery

---

## Thevenin's Theorem Review

### What is Thevenin's Theorem?
Any linear circuit with voltage sources and resistances can be replaced by an equivalent circuit consisting of:
- A single voltage source (V_th): Open-circuit voltage at the terminals
- A single series resistance (R_th): Equivalent resistance with all sources deactivated

### Why is it Useful?
1. **Simplifies Analysis**: Complex networks reduced to simple equivalent
2. **Load Analysis**: Easy to analyze different loads without re-solving entire circuit
3. **Maximum Power Transfer**: Directly reveals optimal load resistance
4. **Design Tool**: Helps in impedance matching and power delivery optimization

### How to Find Thevenin Equivalent
1. **V_th**: Remove load, measure/calculate open-circuit voltage
2. **R_th**: Deactivate all independent sources (short voltage sources, open current sources), calculate resistance looking into terminals

---

## General Usage Tips

1. **Modify Parameters**: Both scripts have clearly marked parameter sections - experiment with different values
2. **Observe Trends**: Change one parameter at a time to understand its effect
3. **Compare Theory**: Calculate expected results by hand and verify with simulations
4. **Real Components**: Remember real diodes and capacitors have non-ideal characteristics

## Educational Applications

- **Circuit Theory Courses**: Visualize abstract theorems with concrete examples
- **Lab Preparation**: Predict behavior before building physical circuits
- **Design Practice**: Understand tradeoffs in component selection
- **Troubleshooting**: Learn to recognize normal vs abnormal circuit behavior
