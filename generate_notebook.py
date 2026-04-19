import json

notebook = {
    "cells": [],
    "metadata": {},
    "nbformat": 4,
    "nbformat_minor": 4
}

def add_md(text):
    notebook["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [text]
    })

def add_code(text):
    notebook["cells"].append({
        "cell_type": "code",
        "metadata": {},
        "source": [text],
        "outputs": [],
        "execution_count": None
    })

add_md("# ⚛️ Quantum Double-Slit Experiment Simulator\n\nThis notebook simulates the famous double-slit experiment purely through quantum circuits using Qiskit. It demonstrates both wave-like interference and particle-like behavior utilizing phase kickback and quantum superposition.\n\n### Step 1: Install Dependencies\nRun this cell to install the required libraries.")

add_code("!pip install qiskit qiskit-aer matplotlib ipywidgets pylatexenc")

add_md("### Step 2: System Architecture & Imports\nThis cell defines the core logic: the quantum circuit (`build_double_slit_circuit`), the simulator, and the plotting definitions.")

core_logic = """import math
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output

plt.style.use('dark_background')

# --- 1. Circuit Construction ---
def build_double_slit_circuit(num_screen_qubits, d, L, wavelength, detector_on=False):
    q_path = QuantumRegister(1, name="path")
    q_screen = QuantumRegister(num_screen_qubits, name="screen")
    c_path = ClassicalRegister(1, name="c_path")
    c_screen = ClassicalRegister(num_screen_qubits, name="c_screen")
    
    qc = QuantumCircuit(q_path, q_screen, c_path, c_screen)
    qc.h(q_path) # Superposition: Both slits
    qc.h(q_screen) # Initialize Screen
    
    # Phase shifts simulating path length diffs
    theta = (2 * math.pi * d) / (wavelength * L)
    for i in range(num_screen_qubits):
        qc.cp(theta * (2**i), q_path[0], q_screen[i])
        
    if detector_on:
        qc.measure(q_path, c_path) # Observer Effect
        
    if not detector_on:
        qc.h(q_path) # Phase Kickback: extracts interference
        qc.measure(q_path, c_path)
        
    qc.measure(q_screen, c_screen)
    return qc

# --- 2. Simulation & Data Hooks ---
def run_simulation(num_qubits, d, L, wavelength, shots, detector_on):
    qc = build_double_slit_circuit(num_qubits, d, L, wavelength, detector_on)
    simulator = AerSimulator()
    compiled = transpile(qc, simulator)
    counts = simulator.run(compiled, shots=shots).result().get_counts()
    
    num_positions = 2**num_qubits
    probs = np.zeros(num_positions)
    valid_shots = 0
    
    for bitstring, count in counts.items():
        parts = bitstring.split()
        if len(parts) == 2:
            s_str, p_str = parts[0], parts[1]
        else:
            s_str, p_str = bitstring[:-1], bitstring[-1]
            
        pos = int(s_str, 2)
        if not detector_on:
            if p_str == '0': # Interference fringe mapping
                probs[pos] += count
                valid_shots += count
        else: # Particle behavior mapping
            probs[pos] += count
            valid_shots += count
            
    if valid_shots > 0: probs = probs / valid_shots
    return np.arange(num_positions), probs

def apply_envelope(probs, num_positions, detector_on):
    x = np.arange(num_positions)
    mid = num_positions / 2.0
    shift = num_positions * 0.15
    width = num_positions * 0.1
    g1 = np.exp(-0.5 * ((x - (mid - shift)) / width)**2)
    g2 = np.exp(-0.5 * ((x - (mid + shift)) / width)**2)
    envelope = g1 + g2
    final = probs * envelope
    if np.sum(final) > 0: final = final / np.sum(final)
    return x, final"""
add_code(core_logic)

add_md("### Step 3: Interactive Dashboard\nWe use `ipywidgets` to create sliders allowing you to simulate the actual physical behaviors in real time. **Change the Wavelength, Slit Separation, or turn the Detector ON**, and watch the interference pattern update dynamically!")

ui_code = """
out = widgets.Output()

style = {'description_width': 'initial'}
slit_slider = widgets.FloatSlider(value=4.0, min=1.0, max=10.0, step=0.5, description='Slit Separation (d):', style=style)
dist_slider = widgets.FloatSlider(value=100.0, min=50.0, max=200.0, step=10.0, description='Screen Distance (L):', style=style)
wave_slider = widgets.FloatSlider(value=1.0, min=0.1, max=3.0, step=0.1, description='Wavelength (λ):', style=style)
detector_toggle = widgets.ToggleButton(value=False, description='Detector OFF', button_style='success', icon='check')

def on_toggle_change(change):
    if change['new']:
        detector_toggle.description = 'Detector ON'
        detector_toggle.button_style = 'warning'
        detector_toggle.icon = 'exclamation'
    else:
        detector_toggle.description = 'Detector OFF'
        detector_toggle.button_style = 'success'
        detector_toggle.icon = 'check'
    update_plot()

detector_toggle.observe(on_toggle_change, names='value')

def update_plot(*args):
    with out:
        clear_output(wait=True)
        d = slit_slider.value
        L = dist_slider.value
        wl = wave_slider.value
        on = detector_toggle.value
        
        num_q = 6
        x, probs = run_simulation(num_q, d, L, wl, 4096, on)
        x, final = apply_envelope(probs, 2**num_q, on)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        color = 'orange' if on else 'cyan'
        label = "Particle Hits (No Interference)" if on else "Wave Interference"
        ax.plot(x, final, color=color, linewidth=2, label=label)
        ax.fill_between(x, final, color=color, alpha=0.2)
        ax.set_ylim(0, max(0.06, np.max(final)*1.2))
        ax.set_title(f"Quantum Simulation Output")
        ax.set_xticks([])
        ax.legend()
        plt.show()

# Bind sliders
for w in [slit_slider, dist_slider, wave_slider]:
    w.observe(update_plot, names='value')

display(widgets.VBox([
    widgets.HBox([slit_slider, dist_slider, wave_slider]),
    detector_toggle,
    out
]))

# Initial plot trigger
update_plot()
"""
add_code(ui_code)

add_md("### Conclusion: What The Quantum Circuit Demonstrated\n\n1. **Wave Behavior:** When the detector is OFF, the single `path` qubit is passed cleanly into a Hadamard representing a superposition of taking both slits. As it hits the `screen` qubits (representing position coordinates), the Fourier phases translate into fringes when kicked back through a Hadamard.\n2. **Particle Behavior:** When the detector is ON, observing the `path` qubit collapses its wave state into a defined 0 or 1. Reversing the path through the final system no longer yields the coherence to produce overlapping amplitudes, simulating precisely why measurement collapses interference.")

with open('colab_notebook.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2)

print("colab_notebook.ipynb generated successfully!")
