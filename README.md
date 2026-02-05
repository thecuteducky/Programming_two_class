<img width="1189" height="712" alt="image" src="https://github.com/user-attachments/assets/48e7f1bb-dd7e-4502-8e9b-b5b538cb3c48" />
# DNA Visualization (Tkinter)

A small Python project that visualizes a stylized DNA double helix using Tkinter.  
It includes two example programs:

- `dna_visualization.py` — a compact full-length helix viewer (100 steps by default).
- `dna_visualization_zoom.py` — an improved viewer with a zoomed segment display, striped rungs, paging controls and presets (recommended for clearer output and taking a part of the helix).

This README explains how the code is organized, what the `DNA` class does, the available parameters, how to run the demos, and troubleshooting notes.

---

## Features

- 2D stylized double helix using sin / cos to position left/right backbones.
- Color-coded base pairs and grouping (AC vs TG) with different rung colors.
- Circles drawn at backbone positions to represent molecules.
- Zoomed segment viewer with stacked striped rungs to mimic the illustrative sample.
- UI controls for paging, setting view start/length, randomizing sequence, and presets.

---

## Requirements

- Python 3.6+ (recommended Python 3.8+)
- Tkinter (usually included with CPython)
  - On Debian/Ubuntu you may need to install: `sudo apt install python3-tk`
  - On Fedora: `sudo dnf install python3-tkinter`
  - On Windows and macOS, the standard Python installers normally include Tkinter.

No external pip packages are required.

---

## Files

- `dna_visualization.py` — simple, full-length helix example (100 steps).
- `dna_visualization_zoom.py` — improved zoomed segment viewer with UI controls and presets.
- `README.md` — this file.

---

## How to run

Open a terminal and run either example with Python:

- Run the compact / full helix:
  ```
  python dna_visualization.py
  ```

- Run the zoomed segment viewer (recommended when you want to "take a part"):
  ```
  python dna_visualization_zoom.py
  ```

If your system's Python command is `python3`, use that instead:
```
python3 dna_visualization_zoom.py
```

---

## The DNA class — overview

Both example scripts define a `DNA` class that encapsulates geometry, sequence generation, and drawing logic. The `dna_visualization_zoom.py` script exposes more controls and is the recommended starting point.

Constructor signature (example from `dna_visualization_zoom.py`):

DNA(
  canvas: tk.Canvas,
  total_steps: int = 200,
  amplitude: float = 160.0,
  step_height: float = 14.0,
  twist: float = 0.35,
  backbone_width: int = 22,
  circle_r: int = 12,
  rung_thickness: int = 12,
  stripe_count: int = 10,
  center_x: int = None,
  top_margin: int = 20,
)

Key responsibilities:
- generate_sequence(seq=None) — generate (random) or set a specific sequence. Sequence is stored as the "left" strand; the right strand is computed with standard complement rules (A<->T, C<->G).
- compute_positions() — computes (x,y) positions for each backbone step using cos/sin for lateral offsets and a small sin wobble for a 3D feel.
- draw() — draws the current view (backbones, rungs, base circles, labels) on the canvas.
- set_view(start, length) — set which subset of steps is visible (useful to “take a part”).
- page_next(), page_prev() — page the view window forwards/backwards.
- The zoomed viewer uses stacked thin horizontal stripes per rung to produce the layered look.

---

## Important parameters to tune the visual look

- `total_steps` — total number of base-pair steps in the sequence.
- `view_start` and `view_length` — control the slice that is drawn (useful to zoom in).
- `amplitude` — how wide the helix is horizontally.
- `step_height` — vertical spacing between consecutive steps (larger = less compressed).
- `twist` — how fast the helix rotates (radians per step).
- `backbone_width` — pixel width of the backbone ribbons.
- `rung_thickness` and `stripe_count` — how thick and how many stripes to draw on each rung (gives layered look).
- `circle_r` — radius of backbone molecular circles.
- `stripe_colors` — colors used to alternate stripes on rungs (in `dna_visualization_zoom.py`).

Recommended for clarity (zoomed viewer):
- Smaller `view_length` (e.g., 8–20) and larger `step_height` (12–18) produces an uncluttered, clear image similar to the sample.

---

## UI Controls (in dna_visualization_zoom.py)

- Start index — set the first visible base index (0-based).
- View length — set how many consecutive steps are drawn.
- Apply view — apply the Start and View length values.
- Previous / Next — page by the current view length.
- Randomize sequence — generate a new random sequence and redraw.
- Preset: stacked slices — applies parameters tuned to mimic the stacked stripe look shown in the example.

---

## Example: Visualize a custom sequence

You can visualize a particular DNA sequence by modifying the script before calling `draw()`:

In `dna_visualization_zoom.py` (or `dna_visualization.py`) do:

```python
# create dna object (example)
dna = DNA(canvas, total_steps=100, ...)

# set a specific sequence of length total_steps:
dna.generate_sequence("ACGTTGCA...")  # must be exactly `total_steps` characters long

# compute positions and draw
dna.compute_positions()
dna.draw()
```

Or, in `dna.draw(sequence="...")` (in `dna_visualization.py` implementation) you can pass the sequence directly.

---

## Troubleshooting

- Window shows but is blank:
  - Ensure Tkinter is available and installed (see Requirements).
  - Check console for Python exceptions and share the traceback if needed.

- Controls not responding:
  - Ensure you are running the correct script (`dna_visualization_zoom.py`) — controls are only implemented in that script.

- Tkinter on Linux:
  - If you get an import error for `tkinter`, install the OS package:
    - Debian/Ubuntu: `sudo apt install python3-tk`
    - Fedora: `sudo dnf install python3-tkinter`

---

## Next steps / Enhancements (ideas)

- Depth sorting by a z component so overlapping parts render in correct front/back order.
- 3D shading and gradients on backbone ribbons.
- Export current canvas view to a PNG image.
- Add ability to highlight or annotate specific base positions.
- Add animation of the helix twisting.

If you'd like, I can add any of the above features — tell me which and I will update the code.

---

## License

This example code is provided under the MIT license (feel free to reuse and modify). No warranty is provided — sample/educational code.

---

Thanks — if you want, I can:
- Produce a single combined script with both viewing modes,
- Add image export (PNG),
- Or add depth-sorting + shading for a more realistic overlap effect.

Tell me which feature you'd like next and I’ll implement it.
