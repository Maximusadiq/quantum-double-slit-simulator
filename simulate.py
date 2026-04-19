"""
simulate.py
Runs the Qiskit simulation for the double-slit model and parses the counts.
"""

from qiskit_aer import AerSimulator
from qiskit import transpile
from circuit import build_double_slit_circuit
import numpy as np

def run_simulation(num_qubits, d, L, wavelength, shots, detector_on):
    """
    Executes the double slit quantum circuit.
    
    Returns:
        tuple: (x_positions, probability_distribution)
    """
    qc = build_double_slit_circuit(num_qubits, d, L, wavelength, detector_on)
    
    # Use AerSimulator
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    
    # Run the simulation
    result = simulator.run(compiled_circuit, shots=shots).result()
    counts = result.get_counts()
    
    num_positions = 2**num_qubits
    probs = np.zeros(num_positions)
    
    total_valid_shots = 0
    
    for bitstring, count in counts.items():
        # Bitstring format from qiskit: "c_screen c_path"
        parts = bitstring.split()
        if len(parts) == 2:
            c_screen_str, c_path_str = parts[0], parts[1]
        else:
            # Fallback just in case
            c_screen_str = bitstring[:-1]
            c_path_str = bitstring[-1]
            
        pos = int(c_screen_str, 2)
        
        if not detector_on:
            # For Wave Behavior (detector OFF), we post-select instances where path=0
            # to observe the interference probability distribution.
            if c_path_str == '0':
                probs[pos] += count
                total_valid_shots += count
        else:
            # For Particle Behavior (detector ON), all hits are recorded and superposition collapsed early
            probs[pos] += count
            total_valid_shots += count
            
    if total_valid_shots > 0:
        probs = probs / total_valid_shots
        
    x_positions = np.arange(num_positions)
    return x_positions, probs

def apply_macroscopic_envelope(probs, num_positions, detector_on):
    """
    While the quantum circuit simulates the pure quantum phase interference,
    a physical double slit experiment operates over a macroscopic physical area.
    This applies the macroscopic structural envelope to the quantum probability 
    results to visibly produce the 'two bright bands' particle mapping.
    """
    x = np.arange(num_positions)
    mid = num_positions / 2.0
    shift = num_positions * 0.15
    width = num_positions * 0.1
    
    # The two actual physical slits as standard Gaussian transmission functions
    g1 = np.exp(-0.5 * ((x - (mid - shift)) / width)**2)
    g2 = np.exp(-0.5 * ((x - (mid + shift)) / width)**2)
    
    # The macro envelope is the sum of transmissions through both slits
    envelope = g1 + g2
    
    # Multiply the pure quantum phase probability map against the physical boundary map
    final_probs = probs * envelope
    
    if np.sum(final_probs) > 0:
        final_probs = final_probs / np.sum(final_probs)
        
    return x, final_probs
