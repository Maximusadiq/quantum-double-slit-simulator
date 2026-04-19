"""
visualize.py
Generates the matplotlib visualizations mapping quantum and classical outputs.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import os

from simulate import run_simulation, apply_macroscopic_envelope

# Ensure we use a dark theme suitable for quantum wave representations
plt.style.use('dark_background')

def plot_static_comparison(x, probs_on, probs_off, classical_probs, filepath="static_plot.png"):
    """Plot static wave vs particle graphs."""
    plt.figure(figsize=(10, 6))
    
    # Quantum Detector OFF
    plt.plot(x, probs_off, label="Quantum: Detector OFF (Wave Behavior)", 
             color='cyan', linewidth=2, alpha=0.9)
    
    # Quantum Detector ON
    plt.plot(x, probs_on, label="Quantum: Detector ON (Particle Behavior)", 
             color='orange', linewidth=2, linestyle='--', alpha=0.9)
             
    # Classical
    plt.plot(x, classical_probs, label="Classical Particle", 
             color='gray', linewidth=1.5, linestyle=':', alpha=0.7)
             
    plt.title("Quantum Double-Slit Experiment Simulation", fontsize=16)
    plt.xlabel("Screen Position", fontsize=12)
    plt.ylabel("Detection Probability", fontsize=12)
    plt.legend(loc="upper right", fontsize=10)
    plt.grid(alpha=0.2)
    
    plt.tight_layout()
    plt.savefig(filepath, dpi=300, facecolor='black')
    plt.close()

def plot_heatmap(probs_off, probs_on, num_positions, filepath="double_slit_screen.png"):
    """
    Plots a 2D intensity map showing exactly what an observer would
    see hitting a photographic plate at the back.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), gridspec_kw={'height_ratios': [1, 1]})
    
    # Expand 1D array to 2D
    plate_matrix_off = np.tile(probs_off, (10, 1))
    plate_matrix_on = np.tile(probs_on, (10, 1))
    
    # Plot Wave Behavior
    ax1.imshow(plate_matrix_off, cmap='inferno', aspect='auto')
    ax1.set_title("Photographic Plate: Detector OFF (Interference Fringes)", color='white')
    ax1.axis('off')
    
    # Plot Particle Behavior
    ax2.imshow(plate_matrix_on, cmap='inferno', aspect='auto')
    ax2.set_title("Photographic Plate: Detector ON (Two Bright Bands)", color='white')
    ax2.axis('off')
    
    fig.patch.set_facecolor('black')
    plt.tight_layout()
    plt.savefig(filepath, dpi=300, facecolor='black', bbox_inches='tight')
    plt.close()

def animate_buildup(num_qubits, d, L, wavelength, filepath="interference_buildup.gif"):
    """
    Animate the build-up of the interference pattern by running escalating shots.
    """
    # Escalate shots up to 4096 framing the collapse into deterministic fields
    shot_counts = [10, 20, 50, 100, 200, 500, 1000, 2048, 4096, 4096, 4096]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    line, = ax.plot([], [], color='cyan', linewidth=2)
    text_shots = ax.text(0.05, 0.9, '', transform=ax.transAxes, color='white', fontsize=14)
    
    ax.set_xlim(0, 2**num_qubits - 1)
    ax.set_ylim(0, 0.08) # Approximation
    ax.set_title("Emergence of Quantum Interference", fontsize=16, color='white')
    ax.set_xlabel("Screen Position", color='white')
    ax.set_ylabel("Probability", color='white')
    ax.grid(alpha=0.2)
    
    def update(frame):
        shots = shot_counts[frame]
        x, probs = run_simulation(num_qubits, d, L, wavelength, shots, detector_on=False)
        x, final_probs = apply_macroscopic_envelope(probs, 2**num_qubits, detector_on=False)
        
        line.set_data(x, final_probs)
        text_shots.set_text(f'Shots: {shots}')
        
        # dynamic y scaling
        max_y = np.max(final_probs) * 1.2 if np.max(final_probs) > 0 else 0.05
        ax.set_ylim(0, max(0.05, max_y))
        
        return line, text_shots

    anim = FuncAnimation(fig, update, frames=len(shot_counts), interval=500, blit=False)
    
    # Save as GIF
    anim.save(filepath, writer='pillow', fps=2, facecolor='black')
    plt.close()

def animate_3d_surface(num_qubits, d, L, shots, filepath="3d_interference.gif"):
    """
    Add a 3D surface plot using mpl_toolkits.mplot3d showing the interference probability 
    as a Z-axis height map over screen position X and wavelength Y. Animate it rotating slowly.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    # We will vary wavelength from 0.5 to 2.5
    wavelengths = np.linspace(0.5, 2.5, 20)
    x_positions = np.arange(2**num_qubits)
    
    X, Y = np.meshgrid(x_positions, wavelengths)
    Z = np.zeros_like(X, dtype=float)
    
    print("   [3D Surface] Computing contour layers (takes a few moments)...")
    for i, wl in enumerate(wavelengths):
        _, probs = run_simulation(num_qubits, d, L, wl, shots, detector_on=False)
        _, final_probs = apply_macroscopic_envelope(probs, 2**num_qubits, detector_on=False)
        Z[i, :] = final_probs
        
    surf = ax.plot_surface(X, Y, Z, cmap='inferno', edgecolor='none')
    
    ax.set_title("3D Interference Surface Map vs Wavelength", color='white', fontsize=16)
    ax.set_xlabel("Screen Position X", color='white')
    ax.set_ylabel("Wavelength Y", color='white')
    ax.set_zlabel("Detection Probability Z", color='white')
    
    # Style tweaks for dark background
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.zaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='z', colors='white')
    
    # Remove pane fill colors
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    def update(frame):
        # Rotate azimuth by frame angle
        ax.view_init(elev=30, azim=frame * 2)
        return fig,

    # 180 frames for a full rotation (at 2 degrees per frame)
    anim = FuncAnimation(fig, update, frames=180, interval=50, blit=False)
    anim.save(filepath, writer='pillow', fps=20, facecolor='black')
    plt.close()

def animate_collapse(num_qubits, d, L, wavelength, shots, filepath="detector_collapse.gif"):
    """
    Animate the transition - show the interference fringes smoothly dissolving 
    into two bands when you flip the detector on.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    _, raw_off = run_simulation(num_qubits, d, L, wavelength, shots, detector_on=False)
    x, final_off = apply_macroscopic_envelope(raw_off, 2**num_qubits, detector_on=False)
    
    _, raw_on = run_simulation(num_qubits, d, L, wavelength, shots, detector_on=True)
    _, final_on = apply_macroscopic_envelope(raw_on, 2**num_qubits, detector_on=True)
    
    line, = ax.plot([], [], color='cyan', linewidth=3)
    text_alpha = ax.text(0.05, 0.9, '', transform=ax.transAxes, color='white', fontsize=14)
    
    ax.set_xlim(0, 2**num_qubits - 1)
    max_y = max(np.max(final_off), np.max(final_on)) * 1.2
    ax.set_ylim(0, max_y)
    ax.set_title("Observer Effect: Collapse of the Wavefunction", fontsize=16, color='white')
    ax.set_xlabel("Screen Position", color='white')
    ax.set_ylabel("Probability", color='white')
    ax.grid(alpha=0.2)
    
    # We interpolate alpha from 0 to 1 over 60 frames. 
    # 0 = Wave (Detector OFF), 1 = Particle (Detector ON)
    alphas = np.concatenate([
        np.zeros(10), # hold off
        np.linspace(0, 1, 40), # fade
        np.ones(10) # hold on
    ])
    
    def update(frame):
        alpha = alphas[frame]
        current_probs = (1 - alpha) * final_off + alpha * final_on
        line.set_data(x, current_probs)
        
        # Approximate color transition
        r = int(0 + alpha * 255)
        g = int(255 - alpha * 90)
        b = int(255 - alpha * 255)
        color = f'#{r:02x}{g:02x}{b:02x}'
        line.set_color(color)
        
        state_text = "Detector OFF (Wave/Fringes)" if alpha < 0.5 else "Detector ON (Particle/Bands)"
        text_alpha.set_text(state_text)
        return line, text_alpha
        
    anim = FuncAnimation(fig, update, frames=len(alphas), interval=100, blit=False)
    anim.save(filepath, writer='pillow', fps=15, facecolor='black')
    plt.close()

def animate_particle_buildup(num_qubits, d, L, wavelength, shots=500, filepath="particle_buildup.gif"):
    """
    Show individual "particles" being fired one at a time as dots, with the interference pattern 
    emerging slowly from apparent randomness.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    # Run full sim to get analytical probability distribution
    _, raw_off = run_simulation(num_qubits, d, L, wavelength, 4096, detector_on=False)
    x, final_off = apply_macroscopic_envelope(raw_off, 2**num_qubits, detector_on=False)
    
    # Sample actual coordinates according to probability distribution
    p = final_off / np.sum(final_off)
    particle_hits = np.random.choice(x, size=shots, p=p)
    
    # Assign a random Y value for each particle so they form a dense strip
    y_randoms = np.random.uniform(0, 1, size=shots)
    
    scatter = ax.scatter([], [], c='cyan', s=15, alpha=0.8, edgecolor='none')
    text_shots = ax.text(0.05, 0.9, '', transform=ax.transAxes, color='white', fontsize=14)
    
    ax.set_xlim(0, 2**num_qubits - 1)
    ax.set_ylim(0, 1) # Distribution strip
    
    # Overlay a faint outline of the final analytical distribution mapped to 0-1
    ax.plot(x, final_off / np.max(final_off) * 0.9, color='white', alpha=0.3, linewidth=2, linestyle='--')
    
    ax.set_title("Particle-by-Particle Emergence (Dots)", fontsize=16, color='white')
    ax.set_xlabel("Screen Position", color='white')
    ax.set_yticks([]) # Hide Y ticks as they are arbitrary for a dot scatter
    ax.grid(alpha=0.2)
    
    # Animation frames: 1, 2, ... 10, then steps of 5 up to max
    frames = list(range(1, 20)) + list(range(20, shots+1, 5))
    
    def update(frame_idx):
        n = frames[frame_idx]
        current_x = particle_hits[:n]
        current_y = y_randoms[:n]
        
        # update scatter
        scatter.set_offsets(np.c_[current_x, current_y])
        text_shots.set_text(f'Particles Fired: {n}')
        return scatter, text_shots

    anim = FuncAnimation(fig, update, frames=len(frames), interval=50, blit=False)
    anim.save(filepath, writer='pillow', fps=20, facecolor='black')
    plt.close()
