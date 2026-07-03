
Project: eogtouch — Mouse-movement biomarker extraction
=========================================================

Summary
-------
This repository contains the code and notebooks for a project that analyzes and extracts biomarkers from a motor signal derived from mouse movement. The original idea was to use EOG (electrooculography), but technical limitations prevented reliable EOG recordings, so the study was adapted to use mouse-movement as the primary signal.

Project goals
-------------
- Record and analyze mouse-movement signals while participants perform a visual alignment and keypress task.
- Extract biomarkers from the resulting motor signals to study motor behavior and response characteristics.

Experiment / task description
-----------------------------
- A visual stimulus appears on screen. The participant aligns the mouse cursor with the stimulus.
- The stimulus changes color. Depending on the color, a specific set of keys becomes valid.
- The participant must press the correct key corresponding to the color. If the response is incorrect, the participant has up to 3 chances before the trial moves on.
- Each trial (iteration) lasts 20 seconds.

Why mouse movement (not EOG)
----------------------------
The original plan used EOG to capture eye movement biomarkers, but technical constraints (hardware, signal quality, or setup issues) made EOG unreliable. The protocol was adjusted to capture motor output via the mouse as a robust alternative.

Repository structure (high level)
--------------------------------
- `biomarcadores/` — analysis scripts and helper modules for computing biomarkers.
- `eogtouch/` — main package and GUI application code (entry point for running the experiment).
- `notebooks/` — exploratory and analysis Jupyter notebooks used during development.
- `data/` — example input data and images used in the GUI and tests.

Dependencies
----------------------
This project was developed on Ubuntu. To reproduce the environment, use WSL on Windows or an Ubuntu machine.

How to run
----------
On the developer environment (Ubuntu / WSL) the app can be launched from the command line. The project was typically started with the `uv run eogtouch` command (run this inside WSL/Ubuntu shell with the virtualenv active):

```bash
# inside WSL/Ubuntu, with venv activated
uv run eogtouch
```

Data and analysis
-----------------
- Raw mouse movement logs and trial metadata are saved during runs (see `storage/` and `data/` folders).
- Use the notebooks in `notebooks/` (e.g., `Plotting_Biomarcadores.ipynb`) to explore signals and compute biomarkers.

Contributing
------------
- If you plan to add analyses, please add a notebook under `notebooks/` and a script under `biomarcadores/` for reproducibility.

Contact / author
----------------
For questions about the experiment or analysis, open an issue or contact the repository owner.

Acknowledgements
----------------
This project was developed as part of a final degree project focused on motor-signal biomarker extraction.
