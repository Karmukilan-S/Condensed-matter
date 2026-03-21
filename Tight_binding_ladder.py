import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons

# Constants
t = 1.0
k = np.linspace(-np.pi, np.pi, 500)

def get_bands(tp, tpp, mode):
    e_base = -2 * t * np.cos(k)
    if mode == 'Simple':
        # E = -2t cos(k) +/- tp
        return e_base + tp, e_base - tp
    elif mode == 'Parallel':
        # E = -2t cos(k) +/- sqrt(tp^2 + tpp^2 + 2*tp*tpp*cos(k))
        coupling = np.sqrt(tp**2 + tpp**2 + 2*tp*tpp*np.cos(k))
        return e_base + coupling, e_base - coupling
    else: # Crossed
        # E = -2t cos(k) +/- (tp + 2*tpp*cos(k))
        coupling = tp + 2 * tpp * np.cos(k)
        return e_base + coupling, e_base - coupling

# Setup Figure
fig, ax = plt.subplots(figsize=(8, 7))
plt.subplots_adjust(left=0.1, bottom=0.3, right=0.9)

# Initial values
init_mode = '' 
init_tp = 2.0
init_tpp = 0.3

# Initial Plots
ep, em = get_bands(init_tp, init_tpp, init_mode)
line_plus, = ax.plot(k, ep, color='blue', label='$E_+$ (Anti-bonding)')
line_minus, = ax.plot(k, em, color='red', label='$E_-$ (Bonding)')

# Aesthetics
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax.set_ylim(-6, 6)
ax.set_title(f"Ladder Variation: {init_mode}")
ax.set_ylabel('Energy (E/t)')
ax.set_xlabel('Wavevector (k)')
ax.set_xticks([-np.pi, 0, np.pi])
ax.set_xticklabels(['$-\pi$', '0', '$\pi$'])
ax.legend(loc='upper right')

# Sliders & Radio Buttons
ax_tp = plt.axes([0.25, 0.15, 0.5, 0.03])
ax_tpp = plt.axes([0.25, 0.10, 0.5, 0.03])
ax_radio = plt.axes([0.02, 0.4, 0.15, 0.15], facecolor='#f0f0f0')

s_tp = Slider(ax_tp, "$t'$ ", 0.0, 4.0, valinit=init_tp)
s_tpp = Slider(ax_tpp, "$t''$ ", 0.0, 1.0, valinit=init_tpp)
radio = RadioButtons(ax_radio, ('Simple', 'Parallel', 'Crossed'))

def update(val):
    mode = radio.set_active.get_label() # Note: logic fixed in function
    tp = s_tp.val
    tpp = s_tpp.val
    current_mode = radio.value_selected
    
    ep, em = get_bands(tp, tpp, current_mode)
    line_plus.set_ydata(ep)
    line_minus.set_ydata(em)
    ax.set_title(f"Ladder Variation: {current_mode}")
    fig.canvas.draw_idle()

s_tp.on_changed(update)
s_tpp.on_changed(update)
radio.on_clicked(update)

plt.show()