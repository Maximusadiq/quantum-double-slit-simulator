"""
main.py
Main entry point for running the local experiment.
Draws the circuit and generates all visualizations.
"""

import config
from circuit import build_double_slit_circuit
from simulate import run_simulation, apply_macroscopic_envelope
from classical import run_classical_simulation
from visualize import (
    plot_static_comparison, 
    plot_heatmap, 
    animate_buildup, 
    animate_3d_surface, 
    animate_collapse, 
    animate_particle_buildup
)
import matplotlib.pyplot as plt

def main():
    print("Beginning Quantum Double-Slit Experiment Simulation...\n")
    
    num_positions = 2**config.NUM_QUBITS
    
    # 1. Draw and save circuit layout
    print("1. Generating quantum circuit diagram...")
    qc = build_double_slit_circuit(config.NUM_QUBITS, config.SLIT_SEP, config.SCREEN_DIST, config.WAVELENGTH, detector_on=False)
    try:
        # style="clifford" is often standard, but can sometimes crash deeply nested libraries.
        qc.draw(output='mpl', filename='circuit_diagram.png')
    except Exception as e:
        print(f"Standard MPL draw failed, fallback text print: {e}")
        # fallback if matplotlib rendering fails structurally
        with open('circuit_diagram.txt', 'w') as f:
            f.write(str(qc.draw()))
    
    # 2. Run Quantum Simulation (Detector OFF -> Interference)
    print("2. Simulating Wave Behavior (Detector OFF)...")
    x, raw_probs_off = run_simulation(config.NUM_QUBITS, config.SLIT_SEP, config.SCREEN_DIST, config.WAVELENGTH, config.SHOTS, detector_on=False)
    x, final_probs_off = apply_macroscopic_envelope(raw_probs_off, num_positions, detector_on=False)
    
    # 3. Run Quantum Simulation (Detector ON -> Particle bands)
    print("3. Simulating Particle Behavior (Detector ON)...")
    x, raw_probs_on = run_simulation(config.NUM_QUBITS, config.SLIT_SEP, config.SCREEN_DIST, config.WAVELENGTH, config.SHOTS, detector_on=True)
    x, final_probs_on = apply_macroscopic_envelope(raw_probs_on, num_positions, detector_on=True)
    
    # 4. Run Classical Comparison
    print("4. Simulating Classical reference tracking...")
    _, classical_probs = run_classical_simulation(config.NUM_QUBITS, config.SHOTS)
    
    # 5. Generate plots
    print("5. Generating Visualizations...")
    plot_static_comparison(x, final_probs_on, final_probs_off, classical_probs, "static_plot.png")
    plot_heatmap(final_probs_off, final_probs_on, num_positions, "double_slit_screen.png")
    
    print("6. Rendering standard Build-up Animation (This may take a moment)...")
    animate_buildup(config.NUM_QUBITS, config.SLIT_SEP, config.SCREEN_DIST, config.WAVELENGTH, "interference_buildup.gif")
    
    print("7. Rendering 3D Interference Surface Animation...")
    animate_3d_surface(config.NUM_QUBITS, config.SLIT_SEP, config.SCREEN_DIST, config.SHOTS, "3d_interference.gif")

    print("8. Rendering Detector Collapse Interpolation Animation...")
    animate_collapse(config.NUM_QUBITS, config.SLIT_SEP, config.SCREEN_DIST, config.WAVELENGTH, config.SHOTS, "detector_collapse.gif")

    print("9. Rendering Particle-by-Particle Scatter Animation...")
    animate_particle_buildup(config.NUM_QUBITS, config.SLIT_SEP, config.SCREEN_DIST, config.WAVELENGTH, shots=500, filepath="particle_buildup.gif")
    
    print("\nSimulation complete! Generated files:")
    print("- circuit_diagram.png")
    print("- static_plot.png")
    print("- double_slit_screen.png")
    print("- interference_buildup.gif")
    print("- 3d_interference.gif")
    print("- detector_collapse.gif")
    print("- particle_buildup.gif")

if __name__ == '__main__':
    main()
