"""
Common Emitter Circuit Analyzer
Interactive visualization of common emitter amplifier characteristics
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrow, Rectangle
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches

class CommonEmitterAnalyzer:
    def __init__(self):
        # Default component values - chosen to achieve VCE ≈ VCC/2
        self.RC = 2.2e3      # Collector resistor (Ohms)
        self.RB1 = 47e3      # Base voltage divider - upper resistor (Ohms)
        self.RB2 = 10e3      # Base voltage divider - lower resistor (Ohms)
        self.RE = 1e3        # Emitter resistor (Ohms)
        self.RL = 10e3       # Load resistor (Ohms)
        self.VCC = 12.0      # Supply voltage (V)
        self.beta = 100      # Current gain (hFE)
        self.Cin = 10e-6     # Input coupling capacitor (F)
        self.Cout = 10e-6    # Output coupling capacitor (F)
        self.CE = 100e-6     # Emitter bypass capacitor (F)
        
        # Constants
        self.VT = 0.026      # Thermal voltage at room temp (V)
        self.VBE = 0.7       # Base-emitter voltage (V)
        
        # Selected frequency for detailed calculations
        self.selected_freq = 1000  # Default to 1 kHz
        
        # Create figure and subplots
        self.setup_figure()
        self.create_sliders()
        self.update_plots(None)
        
    def setup_figure(self):
        """Setup the main figure with subplots"""
        self.fig = plt.figure(figsize=(20, 12))
        self.fig.suptitle('Common Emitter Amplifier Analyzer', fontsize=16, fontweight='bold')
        
        # Create grid for subplots - adjusted for formula display
        gs = self.fig.add_gridspec(3, 3, left=0.05, right=0.98, top=0.92, bottom=0.28,
                                   hspace=0.3, wspace=0.4)
        
        # Circuit schematic (left side, spans 2 rows)
        self.ax_circuit = self.fig.add_subplot(gs[0:2, 0])
        self.ax_circuit.set_title('Circuit Schematic', fontweight='bold')
        self.ax_circuit.set_xlim(0, 10)
        self.ax_circuit.set_ylim(0, 10)
        self.ax_circuit.axis('off')
        
        # Gain plots
        self.ax_voltage = self.fig.add_subplot(gs[0, 1])
        self.ax_voltage.set_title('Voltage Gain vs Frequency', fontweight='bold')
        self.ax_voltage.set_xlabel('Frequency (Hz)')
        self.ax_voltage.set_ylabel('Voltage Gain (dB)')
        self.ax_voltage.grid(True, alpha=0.3)
        
        self.ax_current = self.fig.add_subplot(gs[1, 1])
        self.ax_current.set_title('Current Gain vs Frequency', fontweight='bold')
        self.ax_current.set_xlabel('Frequency (Hz)')
        self.ax_current.set_ylabel('Current Gain (dB)')
        self.ax_current.grid(True, alpha=0.3)
        
        self.ax_power = self.fig.add_subplot(gs[2, 0:2])
        self.ax_power.set_title('Power Gain vs Frequency', fontweight='bold')
        self.ax_power.set_xlabel('Frequency (Hz)')
        self.ax_power.set_ylabel('Power Gain (dB)')
        self.ax_power.grid(True, alpha=0.3)
        
        # Formula display panel (right side, spans all rows)
        self.ax_formulas = self.fig.add_subplot(gs[0:3, 2])
        self.ax_formulas.set_title('Calculations at Selected Frequency', fontweight='bold', fontsize=11)
        self.ax_formulas.axis('off')
        
    def create_sliders(self):
        """Create interactive sliders for component values"""
        slider_color = 'lightblue'
        
        # Slider positions [left, bottom, width, height]
        slider_height = 0.02
        slider_width = 0.15
        left_col = 0.08
        right_col = 0.38
        far_right_col = 0.68
        
        # Create slider axes
        ax_RC = plt.axes([left_col, 0.20, slider_width, slider_height], facecolor=slider_color)
        ax_RB = plt.axes([left_col, 0.16, slider_width, slider_height], facecolor=slider_color)
        ax_RE = plt.axes([left_col, 0.12, slider_width, slider_height], facecolor=slider_color)
        ax_RL = plt.axes([left_col, 0.08, slider_width, slider_height], facecolor=slider_color)
        
        ax_VCC = plt.axes([right_col, 0.20, slider_width, slider_height], facecolor=slider_color)
        ax_beta = plt.axes([right_col, 0.16, slider_width, slider_height], facecolor=slider_color)
        
        ax_Cin = plt.axes([far_right_col, 0.20, slider_width, slider_height], facecolor=slider_color)
        ax_Cout = plt.axes([far_right_col, 0.16, slider_width, slider_height], facecolor=slider_color)
        ax_CE = plt.axes([far_right_col, 0.12, slider_width, slider_height], facecolor=slider_color)
        
        # Frequency slider (log scale)
        ax_freq = plt.axes([left_col, 0.04, slider_width * 2.5, slider_height], facecolor='lightcoral')
        
        # Create sliders
        self.slider_RC = Slider(ax_RC, 'RC (kΩ)', 1.0, 10.0, valinit=self.RC/1e3, valstep=0.1)
        self.slider_RB1 = Slider(ax_RB, 'RB1 (kΩ)', 10.0, 200.0, valinit=self.RB1/1e3, valstep=5.0)
        self.slider_RE = Slider(ax_RE, 'RE (kΩ)', 0.1, 5.0, valinit=self.RE/1e3, valstep=0.1)
        self.slider_RL = Slider(ax_RL, 'RL (kΩ)', 1.0, 20.0, valinit=self.RL/1e3, valstep=0.5)
        
        self.slider_VCC = Slider(ax_VCC, 'VCC (V)', 5.0, 24.0, valinit=self.VCC, valstep=0.5)
        self.slider_beta = Slider(ax_beta, 'β (hFE)', 50, 300, valinit=self.beta, valstep=10)
        
        self.slider_Cin = Slider(ax_Cin, 'Cin (μF)', 0.1, 100.0, valinit=self.Cin*1e6, valstep=0.1)
        self.slider_Cout = Slider(ax_Cout, 'Cout (μF)', 0.1, 100.0, valinit=self.Cout*1e6, valstep=0.1)
        self.slider_CE = Slider(ax_CE, 'CE (μF)', 1.0, 1000.0, valinit=self.CE*1e6, valstep=10.0)
        
        # Frequency slider (logarithmic scale from 1 Hz to 1 MHz)
        self.slider_freq = Slider(ax_freq, 'Frequency (Hz)', 0, 6, valinit=3, valstep=0.01)
        
        # Connect sliders to update function
        self.slider_RC.on_changed(self.update_plots)
        self.slider_RB1.on_changed(self.update_plots)
        self.slider_RE.on_changed(self.update_plots)
        self.slider_RL.on_changed(self.update_plots)
        self.slider_VCC.on_changed(self.update_plots)
        self.slider_beta.on_changed(self.update_plots)
        self.slider_Cin.on_changed(self.update_plots)
        self.slider_Cout.on_changed(self.update_plots)
        self.slider_CE.on_changed(self.update_plots)
        self.slider_freq.on_changed(self.update_plots)

        
    def calculate_operating_point(self):
        """Calculate DC operating point (Q-point) using voltage divider bias"""
        # Thevenin equivalent of voltage divider
        # VB = VCC * RB2 / (RB1 + RB2)
        # RTH = RB1 || RB2
        if (self.RB1 + self.RB2) > 0:
            VB = self.VCC * self.RB2 / (self.RB1 + self.RB2)
            RTH = (self.RB1 * self.RB2) / (self.RB1 + self.RB2)
        else:
            VB = 0
            RTH = 1e6
        
        # Emitter voltage
        VE = VB - self.VBE
        
        # Emitter current (assuming VE > 0)
        IE = VE / self.RE if self.RE > 0 and VE > 0 else 0
        
        # Collector and base currents
        IC = IE * self.beta / (self.beta + 1) if self.beta > 0 else 0
        IB = IE / (self.beta + 1) if self.beta > 0 else 0
        
        # Collector voltage
        VC = self.VCC - IC * self.RC
        
        # Collector-emitter voltage
        VCE = VC - VE
        
        return {
            'IB': IB, 'IC': IC, 'IE': IE,
            'VB': VB, 'VC': VC, 'VE': VE, 'VCE': VCE
        }
    
    def display_calculations(self, frequency):
        """Display detailed calculations for the selected frequency"""
        self.ax_formulas.clear()
        self.ax_formulas.axis('off')
        self.ax_formulas.set_title(f'Calculations at {frequency:.1f} Hz', fontweight='bold', fontsize=11)
        
        # Calculate all values
        q_point = self.calculate_operating_point()
        IE = q_point['IE']
        
        # AC emitter resistance
        re = self.VT / IE if IE > 0 else 1e6
        
        # Effective AC collector load
        if self.RC > 0 and self.RL > 0:
            Rc_eff = (self.RC * self.RL) / (self.RC + self.RL)
        else:
            Rc_eff = self.RC if self.RC > 0 else self.RL
        
        # Capacitor impedances
        Zc_in = 1 / (2 * np.pi * frequency * self.Cin) if frequency > 0 else 1e6
        Zc_out = 1 / (2 * np.pi * frequency * self.Cout) if frequency > 0 else 1e6
        Zc_e = 1 / (2 * np.pi * frequency * self.CE) if frequency > 0 else 1e6
        
        # Effective emitter impedance
        if self.RE > 0 and Zc_e > 0:
            Ze_eff = (self.RE * Zc_e) / np.sqrt(self.RE**2 + Zc_e**2)
        else:
            Ze_eff = 0
        
        # Input resistance
        if self.RB1 > 0 and self.RB2 > 0:
            Rb_parallel = (self.RB1 * self.RB2) / (self.RB1 + self.RB2)
            Rin_base = self.beta * (re + Ze_eff)
            Rin = (Rb_parallel * Rin_base) / (Rb_parallel + Rin_base) if (Rb_parallel + Rin_base) > 0 else Rb_parallel
        else:
            Rin = 1e6
            Rb_parallel = 1e6
            Rin_base = 1e6
        
        # Input coupling response
        if Rin > 0 and frequency > 0:
            fc_in = 1 / (2 * np.pi * Rin * self.Cin)
            Cin_response = (frequency / fc_in) / np.sqrt(1 + (frequency / fc_in)**2)
        else:
            fc_in = 0
            Cin_response = 1.0
        
        # Voltage gain
        if (re + Ze_eff) > 0:
            Av_mag_base = Rc_eff / (re + Ze_eff)
        else:
            Av_mag_base = 0
        Av_mag = Av_mag_base * Cin_response
        Av_dB = 20 * np.log10(Av_mag) if Av_mag > 1e-10 else -100
        
        # Current gain
        Rs = 50
        if self.RB1 > 0 and self.RB2 > 0:
            current_division = Rin_base / (Rb_parallel + Rin_base) if (Rb_parallel + Rin_base) > 0 else 1.0
        else:
            current_division = 1.0
        
        if self.RC > 0 and self.RL > 0:
            output_division = self.RC / (self.RC + self.RL)
        else:
            output_division = 1.0
        
        Ai_mag = self.beta * current_division * output_division * Cin_response
        Ai_dB = 20 * np.log10(Ai_mag) if Ai_mag > 1e-10 else -100
        
        # Power gain
        Ap_mag = Av_mag * Ai_mag
        Ap_dB = 10 * np.log10(Ap_mag) if Ap_mag > 1e-10 else -100
        
        # Format the text display
        text_lines = []
        text_lines.append("═══ Q-POINT (DC) ═══")
        text_lines.append(f"IC = {IE*1e3:.3f} mA")
        text_lines.append(f"VCE = {q_point['VCE']:.2f} V")
        text_lines.append(f"IB = {q_point['IB']*1e6:.2f} μA")
        text_lines.append("")
        
        text_lines.append("═══ AC PARAMETERS ═══")
        text_lines.append(f"re = VT/IE = {re:.2f} Ω")
        text_lines.append(f"Rc_eff = RC||RL = {Rc_eff:.1f} Ω")
        text_lines.append(f"Rb_par = RB1||RB2 = {Rb_parallel/1e3:.2f} kΩ")
        text_lines.append("")
        
        text_lines.append("═══ CAPACITOR IMPEDANCES ═══")
        text_lines.append(f"Zc_in = {Zc_in:.2f} Ω")
        text_lines.append(f"Zc_out = {Zc_out:.2f} Ω")
        text_lines.append(f"Zc_e = {Zc_e:.2f} Ω")
        text_lines.append(f"Ze_eff = RE||CE = {Ze_eff:.2f} Ω")
        text_lines.append("")
        
        text_lines.append("═══ INPUT CIRCUIT ═══")
        text_lines.append(f"Rin_base = β(re+Ze) = {Rin_base:.1f} Ω")
        text_lines.append(f"Rin = Rb||Rin_base = {Rin:.1f} Ω")
        text_lines.append(f"fc_in = {fc_in:.2f} Hz")
        text_lines.append(f"Cin_resp = {Cin_response:.4f}")
        text_lines.append("")
        
        text_lines.append("═══ VOLTAGE GAIN ═══")
        text_lines.append(f"Av_base = Rc_eff/(re+Ze)")
        text_lines.append(f"       = {Rc_eff:.1f}/{(re+Ze_eff):.2f}")
        text_lines.append(f"       = {Av_mag_base:.2f}")
        text_lines.append(f"Av = Av_base × Cin_resp")
        text_lines.append(f"   = {Av_mag_base:.2f} × {Cin_response:.4f}")
        text_lines.append(f"   = {Av_mag:.2f}")
        text_lines.append(f"Av_dB = 20log({Av_mag:.2f})")
        text_lines.append(f"      = {Av_dB:.2f} dB")
        text_lines.append("")
        
        text_lines.append("═══ CURRENT GAIN ═══")
        text_lines.append(f"curr_div = {current_division:.4f}")
        text_lines.append(f"out_div = {output_division:.4f}")
        text_lines.append(f"Ai = β × curr × out × Cin")
        text_lines.append(f"   = {self.beta} × {current_division:.3f}")
        text_lines.append(f"     × {output_division:.3f} × {Cin_response:.3f}")
        text_lines.append(f"   = {Ai_mag:.2f}")
        text_lines.append(f"Ai_dB = {Ai_dB:.2f} dB")
        text_lines.append("")
        
        text_lines.append("═══ POWER GAIN ═══")
        text_lines.append(f"Ap = Av × Ai")
        text_lines.append(f"   = {Av_mag:.2f} × {Ai_mag:.2f}")
        text_lines.append(f"   = {Ap_mag:.2f}")
        text_lines.append(f"Ap_dB = 10log({Ap_mag:.2f})")
        text_lines.append(f"      = {Ap_dB:.2f} dB")
        
        # Display the text
        text_str = '\n'.join(text_lines)
        self.ax_formulas.text(0.05, 0.98, text_str, 
                             transform=self.ax_formulas.transAxes,
                             fontsize=8, verticalalignment='top',
                             family='monospace',
                             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    def calculate_gains(self, frequency):
        """Calculate voltage, current, and power gains at given frequency"""
        q_point = self.calculate_operating_point()
        IE = q_point['IE']
        
        # AC emitter resistance
        re = self.VT / IE if IE > 0 else 1e6
        
        # Calculate impedances at different frequencies
        # Input coupling capacitor impedance (magnitude)
        Zc_in = 1 / (2 * np.pi * frequency * self.Cin) if frequency > 0 else 1e6
        
        # Output coupling capacitor impedance (magnitude)
        Zc_out = 1 / (2 * np.pi * frequency * self.Cout) if frequency > 0 else 1e6
        
        # Emitter bypass capacitor impedance (magnitude)
        Zc_e = 1 / (2 * np.pi * frequency * self.CE) if frequency > 0 else 1e6
        
        # Effective emitter impedance (RE in parallel with CE)
        # At low freq: Zc_e is large, so Ze_eff ≈ RE (low gain)
        # At high freq: Zc_e is small, so Ze_eff ≈ 0 (high gain)
        if self.RE > 0 and Zc_e > 0:
            Ze_eff = (self.RE * Zc_e) / np.sqrt(self.RE**2 + Zc_e**2)
        else:
            Ze_eff = 0
        
        # Effective AC collector load (RC in parallel with RL)
        if self.RC > 0 and self.RL > 0:
            Rc_eff = (self.RC * self.RL) / (self.RC + self.RL)
        else:
            Rc_eff = self.RC if self.RC > 0 else self.RL
        
        # Voltage gain magnitude (with emitter bypass and load effects)
        # Av = -Rc_eff / (re + Ze_eff)
        # We take magnitude (ignore phase inversion)
        if (re + Ze_eff) > 0:
            Av_mag = Rc_eff / (re + Ze_eff)
        else:
            Av_mag = 0
        
        # Input coupling capacitor creates high-pass filter
        # Transfer function: H(jω) = jωC_in*R_in / (1 + jωC_in*R_in)
        # Input resistance seen by source (RB1 || RB2 || β*(re + Ze_eff))
        if self.RB1 > 0 and self.RB2 > 0:
            Rb_parallel = (self.RB1 * self.RB2) / (self.RB1 + self.RB2)
            Rin_base = self.beta * (re + Ze_eff)
            Rin = (Rb_parallel * Rin_base) / (Rb_parallel + Rin_base) if (Rb_parallel + Rin_base) > 0 else Rb_parallel
        else:
            Rin = 1e6
        
        # Input coupling capacitor frequency response
        if Rin > 0 and frequency > 0:
            omega = 2 * np.pi * frequency
            fc_in = 1 / (2 * np.pi * Rin * self.Cin)
            Cin_response = (frequency / fc_in) / np.sqrt(1 + (frequency / fc_in)**2)
        else:
            Cin_response = 1.0
        
        # Apply input coupling effect to voltage gain
        Av_mag = Av_mag * Cin_response
        
        # Current gain calculation
        # Ai = (i_out / i_in) = β * (Rin / (Rin + Rs))
        # where Rs is source resistance (assume 50Ω typical)
        # Also affected by biasing resistor shunting
        Rs = 50  # Typical source resistance
        
        # Base current divider: current from source splits between Rb_parallel and base
        if self.RB1 > 0 and self.RB2 > 0:
            Rb_parallel = (self.RB1 * self.RB2) / (self.RB1 + self.RB2)
            Rin_base = self.beta * (re + Ze_eff)
            # Current division factor
            if (Rb_parallel + Rin_base) > 0:
                current_division = Rin_base / (Rb_parallel + Rin_base)
            else:
                current_division = 1.0
        else:
            current_division = 1.0
        
        # Output current divider: collector current splits between RC and RL
        if self.RC > 0 and self.RL > 0:
            output_division = self.RC / (self.RC + self.RL)
        else:
            output_division = 1.0
        
        # Overall current gain (affected by frequency through Ze_eff and Cin)
        Ai_mag = self.beta * current_division * output_division * Cin_response
        
        # Power gain (linear multiplication, then convert to dB)
        # Ap = Av × Ai (in linear domain)
        Ap_mag = Av_mag * Ai_mag
        
        # Convert to dB
        Av_dB = 20 * np.log10(Av_mag) if Av_mag > 1e-10 else -100
        Ai_dB = 20 * np.log10(Ai_mag) if Ai_mag > 1e-10 else -100
        Ap_dB = 10 * np.log10(Ap_mag) if Ap_mag > 1e-10 else -100
        
        return Av_dB, Ai_dB, Ap_dB
    
    def draw_circuit(self):
        """Draw the common emitter circuit schematic"""
        self.ax_circuit.clear()
        self.ax_circuit.set_xlim(0, 10)
        self.ax_circuit.set_ylim(0, 10)
        self.ax_circuit.axis('off')
        self.ax_circuit.set_title('Circuit Schematic', fontweight='bold')
        
        # Transistor position
        tx, ty = 5, 5
        
        # Draw transistor symbol (NPN)
        # Base line
        self.ax_circuit.plot([tx-0.3, tx-0.3], [ty-0.5, ty+0.5], 'k-', linewidth=3)
        # Collector line
        self.ax_circuit.plot([tx-0.3, tx+0.4], [ty+0.3, ty+0.7], 'k-', linewidth=2)
        # Emitter line with arrow
        self.ax_circuit.plot([tx-0.3, tx+0.4], [ty-0.3, ty-0.7], 'k-', linewidth=2)
        # Arrow on emitter
        arrow = FancyArrow(tx+0.1, ty-0.5, 0.15, -0.15, width=0.08, 
                          head_width=0.2, head_length=0.15, fc='black', ec='black')
        self.ax_circuit.add_patch(arrow)
        
        # Circle around transistor
        circle = Circle((tx, ty), 0.8, fill=False, edgecolor='black', linewidth=1.5)
        self.ax_circuit.add_patch(circle)
        
        # VCC rail
        vcc_y = 9
        self.ax_circuit.plot([2, 8], [vcc_y, vcc_y], 'r-', linewidth=2)
        self.ax_circuit.text(1.5, vcc_y, f'VCC\n{self.VCC}V', fontsize=10, 
                           color='red', fontweight='bold', ha='right', va='center')
        
        # Ground
        gnd_y = 1
        self.ax_circuit.plot([2, 8], [gnd_y, gnd_y], 'k-', linewidth=3)
        self.ax_circuit.plot([2.5, 7.5], [gnd_y-0.2, gnd_y-0.2], 'k-', linewidth=2)
        self.ax_circuit.plot([3, 7], [gnd_y-0.4, gnd_y-0.4], 'k-', linewidth=1)
        
        # RC (Collector resistor)
        rc_x = tx
        self.ax_circuit.plot([rc_x, rc_x], [ty+0.7, ty+1.5], 'k-', linewidth=1.5)
        self.draw_resistor(rc_x, ty+1.5, rc_x, vcc_y-0.5, 'v')
        self.ax_circuit.plot([rc_x, rc_x], [vcc_y-0.5, vcc_y], 'k-', linewidth=1.5)
        self.ax_circuit.text(rc_x+0.5, ty+2.5, f'RC\n{self.RC/1e3:.1f}kΩ', 
                           fontsize=9, ha='left', va='center')
        
        # RE (Emitter resistor)
        re_x = tx
        self.ax_circuit.plot([re_x, re_x], [ty-0.7, ty-1.5], 'k-', linewidth=1.5)
        self.draw_resistor(re_x, ty-1.5, re_x, gnd_y+0.5, 'v')
        self.ax_circuit.plot([re_x, re_x], [gnd_y+0.5, gnd_y], 'k-', linewidth=1.5)
        self.ax_circuit.text(re_x+0.5, ty-2, f'RE\n{self.RE/1e3:.1f}kΩ', 
                           fontsize=9, ha='left', va='center')
        
        # CE (Emitter bypass capacitor) - parallel to RE
        ce_x = re_x + 0.8
        self.ax_circuit.plot([re_x, ce_x], [ty-1.5, ty-1.5], 'k-', linewidth=1)
        self.ax_circuit.plot([re_x, ce_x], [gnd_y+0.5, gnd_y+0.5], 'k-', linewidth=1)
        self.draw_capacitor(ce_x, ty-1.5, ce_x, gnd_y+0.5, 'v')
        self.ax_circuit.text(ce_x+0.3, ty-2, f'CE\n{self.CE*1e6:.0f}μF', 
                           fontsize=8, ha='left', va='center')
        
        # RB1 (Base voltage divider - upper resistor)
        rb1_x = 3
        self.ax_circuit.plot([rb1_x, rb1_x], [vcc_y, vcc_y-0.5], 'k-', linewidth=1.5)
        self.draw_resistor(rb1_x, vcc_y-0.5, rb1_x, ty+0.5, 'v')
        self.ax_circuit.plot([rb1_x, rb1_x], [ty+0.5, ty], 'k-', linewidth=1.5)
        self.ax_circuit.text(rb1_x-0.6, ty+3, f'RB1\n{self.RB1/1e3:.0f}kΩ', 
                           fontsize=9, ha='right', va='center')
        
        # RB2 (Base voltage divider - lower resistor)
        self.ax_circuit.plot([rb1_x, rb1_x], [ty, ty-0.5], 'k-', linewidth=1.5)
        self.draw_resistor(rb1_x, ty-0.5, rb1_x, gnd_y+0.5, 'v')
        self.ax_circuit.plot([rb1_x, rb1_x], [gnd_y+0.5, gnd_y], 'k-', linewidth=1.5)
        self.ax_circuit.text(rb1_x-0.6, ty-1.5, f'RB2\n{self.RB2/1e3:.1f}kΩ', 
                           fontsize=9, ha='right', va='center')
        
        # Connection from voltage divider to base
        self.ax_circuit.plot([rb1_x, tx-0.8], [ty, ty], 'k-', linewidth=1.5)
        
        # Input coupling capacitor (Cin)
        cin_x = 1.5
        self.draw_capacitor(cin_x, ty, cin_x+0.8, ty, 'h')
        self.ax_circuit.plot([cin_x+0.8, rb1_x], [ty, ty], 'k-', linewidth=1.5)
        self.ax_circuit.text(cin_x+0.5, ty+0.5, f'Cin\n{self.Cin*1e6:.0f}μF', 
                           fontsize=8, ha='center', va='bottom')
        
        # Input signal
        self.ax_circuit.plot([cin_x-0.5, cin_x], [ty, ty], 'k-', linewidth=1.5)
        self.ax_circuit.text(cin_x-0.8, ty, 'Vin', fontsize=10, 
                           fontweight='bold', ha='right', va='center')
        
        # Output coupling capacitor (Cout)
        cout_x1 = tx + 1.5
        cout_x2 = cout_x1 + 0.8
        self.ax_circuit.plot([rc_x, cout_x1], [ty+1.8, ty+1.8], 'k-', linewidth=1.5)
        self.ax_circuit.plot([rc_x, rc_x], [ty+1.5, ty+1.8], 'k-', linewidth=1.5)
        self.draw_capacitor(cout_x1, ty+1.8, cout_x2, ty+1.8, 'h')
        self.ax_circuit.text(cout_x1+0.4, ty+2.3, f'Cout\n{self.Cout*1e6:.0f}μF', 
                           fontsize=8, ha='center', va='bottom')
        
        # Load resistor (RL)
        rl_x = cout_x2 + 0.5
        self.ax_circuit.plot([cout_x2, rl_x], [ty+1.8, ty+1.8], 'k-', linewidth=1.5)
        self.draw_resistor(rl_x, ty+1.8, rl_x, gnd_y+0.5, 'v')
        self.ax_circuit.plot([rl_x, rl_x], [gnd_y+0.5, gnd_y], 'k-', linewidth=1.5)
        self.ax_circuit.text(rl_x+0.5, ty+0.5, f'RL\n{self.RL/1e3:.1f}kΩ', 
                           fontsize=9, ha='left', va='center')
        
        # Output signal
        self.ax_circuit.plot([rl_x, rl_x+0.8], [ty+1.8, ty+1.8], 'k-', linewidth=1.5)
        self.ax_circuit.text(rl_x+1.2, ty+1.8, 'Vout', fontsize=10, 
                           fontweight='bold', ha='left', va='center')
        
        # Add operating point info
        q_point = self.calculate_operating_point()
        info_text = f"Q-Point:\n"
        info_text += f"IC = {q_point['IC']*1e3:.2f} mA\n"
        info_text += f"VCE = {q_point['VCE']:.2f} V\n"
        info_text += f"IB = {q_point['IB']*1e6:.2f} μA"
        
        self.ax_circuit.text(0.5, 8, info_text, fontsize=9, 
                           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                           verticalalignment='top', family='monospace')
        
    def draw_resistor(self, x1, y1, x2, y2, orientation='v'):
        """Draw a resistor symbol"""
        if orientation == 'v':  # Vertical
            mid_y = (y1 + y2) / 2
            height = abs(y2 - y1)
            width = 0.3
            zigzag_y = np.linspace(y1, y2, 15)
            zigzag_x = [x1 + width * ((-1)**i) * 0.5 for i in range(len(zigzag_y))]
            self.ax_circuit.plot(zigzag_x, zigzag_y, 'k-', linewidth=1.5)
        else:  # Horizontal
            mid_x = (x1 + x2) / 2
            width = abs(x2 - x1)
            height = 0.3
            zigzag_x = np.linspace(x1, x2, 15)
            zigzag_y = [y1 + height * ((-1)**i) * 0.5 for i in range(len(zigzag_x))]
            self.ax_circuit.plot(zigzag_x, zigzag_y, 'k-', linewidth=1.5)
    
    def draw_capacitor(self, x1, y1, x2, y2, orientation='v'):
        """Draw a capacitor symbol"""
        if orientation == 'v':  # Vertical
            mid_y = (y1 + y2) / 2
            plate_width = 0.4
            self.ax_circuit.plot([x1-plate_width/2, x1+plate_width/2], 
                               [mid_y+0.1, mid_y+0.1], 'k-', linewidth=2)
            self.ax_circuit.plot([x1-plate_width/2, x1+plate_width/2], 
                               [mid_y-0.1, mid_y-0.1], 'k-', linewidth=2)
            self.ax_circuit.plot([x1, x1], [y1, mid_y+0.1], 'k-', linewidth=1.5)
            self.ax_circuit.plot([x1, x1], [mid_y-0.1, y2], 'k-', linewidth=1.5)
        else:  # Horizontal
            mid_x = (x1 + x2) / 2
            plate_height = 0.4
            self.ax_circuit.plot([mid_x+0.1, mid_x+0.1], 
                               [y1-plate_height/2, y1+plate_height/2], 'k-', linewidth=2)
            self.ax_circuit.plot([mid_x-0.1, mid_x-0.1], 
                               [y1-plate_height/2, y1+plate_height/2], 'k-', linewidth=2)
            self.ax_circuit.plot([x1, mid_x-0.1], [y1, y1], 'k-', linewidth=1.5)
            self.ax_circuit.plot([mid_x+0.1, x2], [y1, y1], 'k-', linewidth=1.5)
    
    def update_plots(self, val):
        """Update all plots when slider values change"""
        # Update component values from sliders
        self.RC = self.slider_RC.val * 1e3
        self.RB1 = self.slider_RB1.val * 1e3
        # RB2 is calculated to maintain voltage divider ratio
        self.RB2 = self.RB1 / 4.7  # Maintains approximately same ratio
        self.RE = self.slider_RE.val * 1e3
        self.RL = self.slider_RL.val * 1e3
        self.VCC = self.slider_VCC.val
        self.beta = int(self.slider_beta.val)
        self.Cin = self.slider_Cin.val * 1e-6
        self.Cout = self.slider_Cout.val * 1e-6
        self.CE = self.slider_CE.val * 1e-6
        
        # Get selected frequency from slider (logarithmic scale)
        self.selected_freq = 10 ** self.slider_freq.val
        
        # Redraw circuit
        self.draw_circuit()
        
        # Display calculations for selected frequency
        self.display_calculations(self.selected_freq)
        
        # Calculate gains over frequency range
        frequencies = np.logspace(0, 6, 500)  # 1 Hz to 1 MHz
        Av_dB = []
        Ai_dB = []
        Ap_dB = []
        
        for f in frequencies:
            av, ai, ap = self.calculate_gains(f)
            Av_dB.append(av)
            Ai_dB.append(ai)
            Ap_dB.append(ap)
        
        # Calculate gain at selected frequency for marker
        av_sel, ai_sel, ap_sel = self.calculate_gains(self.selected_freq)
        
        # Update voltage gain plot
        self.ax_voltage.clear()
        self.ax_voltage.semilogx(frequencies, Av_dB, 'b-', linewidth=2, label='Voltage Gain')
        self.ax_voltage.plot(self.selected_freq, av_sel, 'ro', markersize=8, label=f'Selected: {av_sel:.1f} dB @ {self.selected_freq:.1f} Hz')
        self.ax_voltage.set_title('Voltage Gain vs Frequency', fontweight='bold')
        self.ax_voltage.set_xlabel('Frequency (Hz)')
        self.ax_voltage.set_ylabel('Voltage Gain (dB)')
        self.ax_voltage.grid(True, alpha=0.3, which='both')
        self.ax_voltage.legend(fontsize=8, loc='lower right')
        
        # Update current gain plot
        self.ax_current.clear()
        self.ax_current.semilogx(frequencies, Ai_dB, 'g-', linewidth=2, label='Current Gain')
        self.ax_current.plot(self.selected_freq, ai_sel, 'ro', markersize=8, label=f'Selected: {ai_sel:.1f} dB @ {self.selected_freq:.1f} Hz')
        self.ax_current.set_title('Current Gain vs Frequency', fontweight='bold')
        self.ax_current.set_xlabel('Frequency (Hz)')
        self.ax_current.set_ylabel('Current Gain (dB)')
        self.ax_current.grid(True, alpha=0.3, which='both')
        self.ax_current.legend(fontsize=8, loc='upper right')
        
        # Update power gain plot
        self.ax_power.clear()
        self.ax_power.semilogx(frequencies, Ap_dB, 'r-', linewidth=2, label='Power Gain')
        self.ax_power.plot(self.selected_freq, ap_sel, 'ko', markersize=8, label=f'Selected: {ap_sel:.1f} dB @ {self.selected_freq:.1f} Hz')
        self.ax_power.set_title('Power Gain vs Frequency', fontweight='bold')
        self.ax_power.set_xlabel('Frequency (Hz)')
        self.ax_power.set_ylabel('Power Gain (dB)')
        self.ax_power.grid(True, alpha=0.3, which='both')
        self.ax_power.legend(fontsize=8, loc='lower right')
        
        # Redraw canvas
        self.fig.canvas.draw_idle()
    
    def show(self):
        """Display the interactive plot"""
        plt.show()

if __name__ == '__main__':
    analyzer = CommonEmitterAnalyzer()
    analyzer.show()
