[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Maximusadiq/quantum-double-slit-simulator/blob/main/colab_notebook.ipynb)
# Quantum Double-Slit Experiment Simulator

A completely quantum-circuit based simulation of the famous Double-Slit Experiment. Rather than just calculating math formulas, this project physically models the experiment through logical superposition, controlled phase-shifts, and phase-kickbacks built via **Qiskit**. 

## Setup & Running 🚀

You can run this full local application or utilize the Google Colab Notebook with zero setup.

### Option A: Run Locally (Python)

1. Ensure you have Python 3.9+ installed.
2. Install the necessary physics/simulation dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the main file to build the simulations, graph outputs, and circuit diagram!
   ```bash
   python main.py
   ```

### Option B: Run on Google Colab
1. Upload the `colab_notebook.ipynb` file to [Google Colab](https://colab.research.google.com).
2. Click **Runtime** -> **Run All**.
3. Use the interactive 1-click sliders at the bottom to alter standard parameters and watch the simulation dynamically rebuild!

---

## What is the Double-Slit Experiment?
Imagine firing tennis balls randomly toward a wall that has two slits. You would expect the balls to pass through and form two distinct bands on the wall behind the slits. 

However, if you fire a beam of light—or even individual photons and electrons—they don't form two simple bands. Instead, they act like waves, overlapping and creating an alternating pattern of bright and dark lines called an **interference pattern**. The particle seems to go through both slits simultaneously! 

## Why Quantum Computing?
Why simulate this on a quantum computer? Because **quantum computers inherently operate using the exact same physics**. Rather than writing a Python function that just plots a `cosine` wave (which is visually accurate but physically hollow), we actually place a *Qubit* into a superposition so that it goes through "both paths at once." We use physical quantum phase interference to inherently derive the resulting mathematical bands.

## How the Circuit Works
We define the physical realm purely via qubits!
1. **The Slits (`q_path`)**: A single qubit represents the particle at the slits. An initial `Hadamard (H) Gate` splits it into a superposition of `|0>` (Slit A) and `|1>` (Slit B).
2. **The Screen (`q_screen`)**: Multiple qubits represent positions all across the detector screen. They are spread out via uniform superpositions.
3. **The Distance**: A series of `Controlled-Phase` gates entangles the paths with the screen, applying a shifting physical phase that depends intrinsically on the simulated wavelength, distance to screen, and slit spacing.
4. **Phase Kickback**: We apply a second `H` gate back on the path qubit. This acts exactly like the interference of physical light waves—combining the relative phases into probability bounds!


## The Observer Effect 👁️
The most fascinating element of quantum mechanics is that **looking at it changes it**. If you measure the particle at the slits to see *which* slit it travels through, the interference pattern disappears, leaving just two basic "particle-like" bands.

In our circuit, we simulate this by tracking the `detector_on` parameter. When toggled ON, we add a `Measure` operation on the Path Qubit immediately *before* it can reach the screen. This collapses the wave function, erasing the ability to kickback phase information and removing the interference pattern completely!

## Results
When running the `main.py` application, you'll receive three deep visualizations.

* **Static Comparison (`static_plot.png`)**: Comparing mathematically the interference fringes caused by the Quantum Wave State against the two tight bands of the Quantum Collapsed State and Classical setup.
* **Photographic Screen View (`double_slit_screen.png`)**: A 2D rendering using a glowing intensity map of exactly what an observer would witness exposing a photographic plate.
* **Animated Frame View (`interference_buildup.gif`)**: Watching 1 particle arrive, then 10, then 100, then 4000—revealing how random points coalesce smoothly into defined wave predictions.

## Parameters Config
Found in `config.py`.

| Parameter | Type | What Changing it Does |
| :--- | :--- | :--- |
| `NUM_QUBITS` | Setting | Increases screen resolution, yielding finer plotted bands. |
| `SHOTS` | Setting | Dictates how many 'particles' are shot. Low shots show high noise; high shots unveil the clean pattern. |
| `WAVELENGTH (λ)` | Physical | Expanding wavelength spreads the interference pattern outwards. |
| `SLIT_SEP (d)` | Physical | Compressing slits spreads the interference ripples out. |
| `SCREEN_DIST (L)`| Physical | Increasing distance enlarges and stretches the bands over larger screen gaps. |

## What I Learned

I came into this as a complete beginner to quantum computing. My only background 
was the double-slit experiment from AP Physics 2. Building this taught me that 
quantum gates aren't just abstract math; they encode real physical phenomena. 
Superposition, phase, and measurement are the same concepts in both physics class 
and a Qiskit circuit. Seeing the interference pattern appear for the first time 
was the moment it all clicked for me.

The hardest part was understanding how phase kickback converts phase differences 
into measurable probabilities, and debugging Qiskit's bitstring output format. 
