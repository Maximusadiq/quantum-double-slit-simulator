"""
circuit.py
Quantum circuit generation for modeling the double-slit experiment via Qiskit.
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import math

def build_double_slit_circuit(num_screen_qubits, d, L, wavelength, detector_on=False):
    """
    Builds the quantum circuit modeling the double slit experiment.
    
    Parameters:
        num_screen_qubits (int): Quantity of qubits encoding screen position (N qubits -> 2^N positions).
        d (float): Separation distance between slits.
        L (float): Distance from slits to the screen.
        wavelength (float): Wavelength of the simulated particle.
        detector_on (bool): If True, measures which-path qubit before interference (observer effect).
        
    Returns:
        QuantumCircuit: The compiled Qiskit circuit.
    """
    q_path = QuantumRegister(1, name="path")
    q_screen = QuantumRegister(num_screen_qubits, name="screen")
    c_path = ClassicalRegister(1, name="c_path")
    c_screen = ClassicalRegister(num_screen_qubits, name="c_screen")
    
    qc = QuantumCircuit(q_path, q_screen, c_path, c_screen)
    
    # 1. Hadamard: puts particle in superposition of both slits (acting as a wave)
    qc.h(q_path)
    
    # 2. Hadamard layer on screen: prepares screen in uniform superposition (representing all landing spots)
    qc.h(q_screen)
    
    # 3. Phase Shifts: Apply controlled phases to simulate path length differences
    # Phase difference depending on screen position x: delta(x) = (2pi / lambda) * d * x / L
    # We apply this phase cumulatively mapping the binary index across screen qubits.
    theta = (2 * math.pi * d) / (wavelength * L)
    
    for i in range(num_screen_qubits):
        angle = theta * (2**i)
        # Controlled Phase: applies phase shift proportional to screen position for slit 1
        qc.cp(angle, q_path[0], q_screen[i])
        
    # The crucial "Observer Effect" - the simulated detector
    if detector_on:
        # Measure which-path BEFORE the screen (collapses superposition, forcing particle behavior)
        qc.measure(q_path, c_path)
        
    # 4. Phase Kickback: Translates the stored phase differences into measurable probability differences.
    # This forms the interference fringes by acting as a quantum eraser.
    if not detector_on:
        # Hadamard on path completes interference
        qc.h(q_path)
        qc.measure(q_path, c_path)
        
    # 5. Measure the screen position to record where the photon/electron landed
    qc.measure(q_screen, c_screen)
    
    return qc
