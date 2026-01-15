import numpy as np
import matplotlib.pyplot as plt

# ───────────────────────────────────────────────
# Parameters
# ───────────────────────────────────────────────
fs = 200000             # High sampling for smooth transients
T = 0.8                # Simulate 80 ms → many cycles to see stabilization
t = np.linspace(0, T, int(fs * T))

f = 100                 # Input frequency (Hz)
Vin_peak = 5.0          # Peak amplitude
Vin = Vin_peak * np.sin(2 * np.pi * f * t)

Vd = 0.7                # Diode drop
R = 1000                # Series resistor (Ω)
C = 4.7e-6              # Capacitor (4.7 μF) → τ ≈ 4.7 ms (about half cycle at 100 Hz)
# Smaller C = faster charging/stabilization

# ───────────────────────────────────────────────
# Simulation function for clamper
# ───────────────────────────────────────────────
def simulate_clamper(Vin, t, Vd, R, C, clamp_positive=True):
    Vout = np.zeros_like(t)
    Vc = np.zeros_like(t)      # Capacitor voltage (initially 0)
    
    for i in range(1, len(t)):
        dt = t[i] - t[i-1]
        vin_now = Vin[i]
        
        # Voltage trying to go across diode
        if clamp_positive:
            # Positive clamper: diode conducts when vin > Vc + Vd
            if vin_now > (Vc[i-1] + Vd):
                ic = (vin_now - Vc[i-1] - Vd) / R
                dVc = ic * dt / C
                Vc[i] = Vc[i-1] + dVc
                Vout[i] = vin_now - Vd          # Output clamped
            else:
                Vc[i] = Vc[i-1]
                Vout[i] = vin_now + Vc[i]       # Follow input + stored voltage
        else:
            # Negative clamper: diode conducts when vin < Vc - Vd
            if vin_now < (Vc[i-1] - Vd):
                ic = (vin_now - Vc[i-1] + Vd) / R   # Note sign change
                dVc = ic * dt / C
                Vc[i] = Vc[i-1] + dVc
                Vout[i] = vin_now + Vd
            else:
                Vc[i] = Vc[i-1]
                Vout[i] = vin_now + Vc[i]
    
    return Vout, Vc

# Run simulations
Vout_pos, Vc_pos = simulate_clamper(Vin, t, Vd, R, C, clamp_positive=True)
Vout_neg, Vc_neg = simulate_clamper(Vin, t, Vd, R, C, clamp_positive=False)

# ───────────────────────────────────────────────
# Plotting with explicit axes
# ───────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 9), sharex=True)

for ax in (ax1, ax2):
    ax.grid(True, alpha=0.3, ls='--')
    ax.axhline(0, color='gray', lw=0.8, alpha=0.6)
    ax.tick_params(labelsize=10)

# Positive Clamper
ax1.plot(t*1000, Vin, 'dodgerblue', lw=1.8, alpha=0.7, label='Input')
ax1.plot(t*1000, Vout_pos, 'crimson', lw=2.4, label='Output (Positive Clamper)')
ax1.set_title('Positive Clamper – Initial Uncharged Capacitor\n'
              '(Gradual shift downward → positive peak clamps near +0.7 V)', fontsize=13)
ax1.set_ylabel('Voltage (V)')
ax1.legend(loc='upper right', fontsize=10)
ax1.set_ylim(-7.5, 7.5)

# Negative Clamper
ax2.plot(t*1000, Vin, 'dodgerblue', lw=1.8, alpha=0.7, label='Input')
ax2.plot(t*1000, Vout_neg, 'forestgreen', lw=2.4, label='Output (Negative Clamper)')
ax2.set_title('Negative Clamper – Initial Uncharged Capacitor\n'
              '(Gradual shift upward → negative peak clamps near –0.7 V)', fontsize=13)
ax2.set_ylabel('Voltage (V)')
ax2.set_xlabel('Time (ms)')
ax2.legend(loc='lower right', fontsize=10)
ax2.set_ylim(-7.5, 7.5)

# Annotations showing transient → steady state
ax1.annotate('Charging transient\n(peaks slowly shift down)', 
             xy=(20, 3), xytext=(30, 5.5), fontsize=10,
             arrowprops=dict(arrowstyle='->', color='darkred'))
ax2.annotate('Charging transient\n(troughs slowly shift up)', 
             xy=(20, -3), xytext=(30, -5.5), fontsize=10,
             arrowprops=dict(arrowstyle='->', color='darkgreen'))

fig.suptitle('Clamper Circuits – Realistic Transient Behavior\n'
             '(Capacitor starts at 0 V, gradually reaches steady-state clamp)',
             fontsize=15, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()