"""
classical.py
Classical simulation for comparison representing no wave behavior.
"""

import numpy as np

def run_classical_simulation(num_screen_qubits, shots):
    """
    Simulates a classical particle randomly going through either slit A or slit B.
    
    Parameters:
        num_screen_qubits (int): To govern the same resolution as the quantum simulation.
        shots (int): Total particles fired.
        
    Returns:
        tuple: (x_positions, classical_probabilities) Array of coordinates and matching intensity map.
    """
    num_positions = 2**num_screen_qubits
    x = np.arange(num_positions)
    mid = num_positions / 2.0
    
    # Simulating standard width and separation for two macroscopic classical slits
    shift = num_positions * 0.15
    width = num_positions * 0.1
    
    # 50/50 coin flip to pick slit A (0) or slit B (1)
    choices = np.random.choice([0, 1], size=shots)
    
    hits = np.zeros(num_positions)
    
    for choice in choices:
        # Classically the particle moves in a straight line from its slit
        center = (mid - shift) if choice == 0 else (mid + shift)
        
        # Adding some generic spread representing dispersion over the distance L
        pos = int(np.random.normal(loc=center, scale=width))
        
        # If the particle lands on the screen track it
        if 0 <= pos < num_positions:
            hits[pos] += 1
            
    # Normalize values into a probability density
    probs = hits / np.sum(hits) if np.sum(hits) > 0 else hits
    
    return x, probs
