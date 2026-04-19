"""
config.py
Configuration for the Quantum Double-Slit Experiment Simulator.
"""

# Physical and Simulation Constants
NUM_QUBITS = 6            # Number of qubits for screen representation (2^6 = 64 screen positions)
SHOTS = 4096              # Number of experimental shots for the quantum simulator

WAVELENGTH = 1.0          # Simulated wavelength (lambda) of the quantum particle
SLIT_SEP = 4.0            # Simulated distance between the two slits (d)
SCREEN_DIST = 100.0       # Simulated distance from the slits to the detector screen (L)
