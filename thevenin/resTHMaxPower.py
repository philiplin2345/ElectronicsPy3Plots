import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Parameters (you can change these)
# -----------------------------
V_th = 10.0          # Thevenin equivalent voltage (Volts)
R_th = 50.0          # Thevenin equivalent resistance (Ohms)

# Generate a wide range of load resistances (log scale for better view)
R_L = np.logspace(-1, 4, 800)  # from 0.1 Ω to 10,000 Ω

# Power delivered to the load: P = V_th² * R_L / (R_th + R_L)²
P = (V_th**2 * R_L) / (R_th + R_L)**2

# Find the maximum power point
max_idx = np.argmax(P)
R_L_max = R_L[max_idx]
P_max = P[max_idx]

print(f"Maximum power delivered: {P_max:.4f} W")
print(f"Occurs at R_L = {R_L_max:.2f} Ω (≈ R_th = {R_th} Ω)")

# -----------------------------
# Plotting with nice style
# -----------------------------
sns.set_style("whitegrid")          # Clean seaborn style
sns.set_context("notebook", font_scale=1.3)

plt.figure(figsize=(10, 6))

# Main power curve
plt.plot(R_L, P, color='royalblue', linewidth=2.5,
         label=f'Power to Load (V_th = {V_th} V, R_th = {R_th} Ω)')

# Highlight the maximum point
plt.plot(R_L_max, P_max, 'ro', markersize=12, label=f'Max Power = {P_max:.3f} W')
plt.axvline(x=R_th, color='darkorange', linestyle='--', linewidth=1.8,
            label=f'R_L = R_th = {R_th} Ω (Maximum Power Point)')

# Log scale on x-axis for better visualization across orders of magnitude
plt.xscale('log')

# Labels and title
plt.xlabel('Load Resistance R_L (Ω)', fontsize=13)
plt.ylabel('Power Delivered to Load (W)', fontsize=13)
plt.title('Maximum Power Transfer Theorem\n(Power is maximized when R_L = R_th)', 
          fontsize=15, fontweight='bold')

# Legend and grid
plt.legend(loc='upper right', fontsize=11, frameon=True, shadow=True)
plt.grid(True, which="both", ls="--", alpha=0.7)

# Optional: add a text annotation at the peak
plt.text(R_L_max * 1.3, P_max * 0.92, f'Max at R_L ≈ {R_th} Ω', 
         color='darkred', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.show()