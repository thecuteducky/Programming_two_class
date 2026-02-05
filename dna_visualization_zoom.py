"""
dna_visualization_zoom.py

Improved DNA double-helix viewer with zoomed segment display and striped rungs.
Run with: python dna_visualization_zoom.py
"""
import tkinter as tk
import math
import random
from typing import List, Tuple

COMPLEMENT = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

# Colors
BACKBONE_LEFT = '#5CA0D9'
BACKBONE_RIGHT = '#2A6F97'
STRIPE_COLORS = ['#ff9800', '#1976d2']  # orange, blue (alternating stripes)
BASE_COLORS = {'A': '#2ca02c', 'C': '#17becf', 'T': '#d62728', 'G': '#9467bd'}


class DNA:
    def __init__(
        self,
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
    ):
        self.canvas = canvas
        self.total_steps = total_steps
        self.amplitude = amplitude
        self.step_height = step_height
        self.twist = twist
        self.backbone_width = backbone_width
        self.circle_r = circle_r
        self.rung_thickness = rung_thickness
        self.stripe_count = stripe_count
        self.top_margin = top_margin

        self.width = int(self.canvas['width'])
        self.height = int(self.canvas['height'])
        self.center_x = center_x if center_x is not None else self.width // 2

        self.positions: List[Tuple[Tuple[float, float], Tuple[float, float]]] = []
        self.sequence: List[str] = []
        self.generate_sequence()
        self.compute_positions()

        # view window (start index and view length)
        self.view_start = 0
        self.view_length = min(20, self.total_steps)  # default visible steps

    def generate_sequence(self, seq: str = None):
        if seq:
            seq = seq.upper().strip()
            if len(seq) != self.total_steps:
                raise ValueError("Provided sequence length must equal total_steps")
            self.sequence = list(seq)
        else:
            choices = ['A', 'C', 'G', 'T']
            self.sequence = [random.choice(choices) for _ in range(self.total_steps)]

    def compute_positions(self):
        self.positions = []
        for i in range(self.total_steps):
            theta = i * self.twist
            x_off_left = self.amplitude * math.cos(theta)
            x_off_right = self.amplitude * math.cos(theta + math.pi)
            z_wobble = math.sin(theta) * (self.step_height * 0.25)
            y = self.top_margin + i * self.step_height + z_wobble
            x_left = self.center_x + x_off_left
            x_right = self.center_x + x_off_right
            self.positions.append(((x_left, y), (x_right, y)))

    def _lighten(self, hexcolor: str, amount: float) -> str:
        hexcolor = hexcolor.lstrip('#')
        r = int(hexcolor[0:2], 16)
        g = int(hexcolor[2:4], 16)
        b = int(hexcolor[4:6], 16)
        r = int(r + (255 - r) * amount)
        g = int(g + (255 - g) * amount)
        b = int(b + (255 - b) * amount)
        return f'#{r:02x}{g:02x}{b:02x}'

    def draw_backbones(self, view_positions: List[Tuple[Tuple[float, float], Tuple[float, float]]]):
        # left points and right points lists (flatten)
        left_points = []
        right_points = []
        for (l, r) in view_positions:
            left_points.extend(l)
            right_points.extend(r)

        # Draw right (darker) then left (lighter) so left appears on top
        self.canvas.create_line(
            *right_points,
            fill=BACKBONE_RIGHT,
            width=self.backbone_width,
            smooth=True,
            splinesteps=48,
            capstyle=tk.ROUND,
            joinstyle=tk.ROUND,
        )
        self.canvas.create_line(
            *left_points,
            fill=BACKBONE_LEFT,
            width=self.backbone_width,
            smooth=True,
            splinesteps=48,
            capstyle=tk.ROUND,
            joinstyle=tk.ROUND,
        )

    def draw_striped_rungs_and_bases(self, view_slice: slice):
        """Draw rungs as stacked thin horizontal stripes to give the layered look."""
        start = view_slice.start or 0
        stop = view_slice.stop or self.total_steps
        step_indices = range(start, stop)
        stripe_spacing = max(1.0, self.rung_thickness / max(1, self.stripe_count))
        for i in step_indices:
            ((xl, yl), (xr, yr)) = self.positions[i]
            left_base = self.sequence[i]
            right_base = COMPLEMENT[left_base]

            # compute stripe stack centered at y
            mid_y = (yl + yr) / 2.0
            half_span = (self.rung_thickness / 2.0)
            for s in range(self.stripe_count):
                # compute relative offset: top -> bottom
                t = s / max(1, (self.stripe_count - 1))
                offset = (t - 0.5) * self.rung_thickness
                y_line = mid_y + offset

                # alternating stripe color (two-color pattern like the sample)
                color = STRIPE_COLORS[s % len(STRIPE_COLORS)]
                # draw line (thin)
                self.canvas.create_line(
                    xl, y_line, xr, y_line,
                    fill=color,
                    width=max(1, int(stripe_spacing * 0.9)),
                    capstyle=tk.ROUND,
                )

            # draw center accent thin line (light)
            self.canvas.create_line(
                xl, mid_y, xr, mid_y,
                fill=self._lighten('#333333', 0.85),
                width=1,
                dash=(),
            )

            # draw backbone circles at the backbone points (larger for clarity)
            self.canvas.create_oval(
                xl - self.circle_r, yl - self.circle_r,
                xl + self.circle_r, yl + self.circle_r,
                fill='#FFA726', outline='#CC7600'
            )
            self.canvas.create_oval(
                xr - self.circle_r, yr - self.circle_r,
                xr + self.circle_r, yr + self.circle_r,
                fill='#FFA726', outline='#CC7600'
            )

            # draw base letters near the center (stacked vertically to be readable)
            label_offset_x = 10
            self.canvas.create_text(
                (xl + xr) / 2 - label_offset_x, mid_y,
                text=left_base, fill=BASE_COLORS[left_base],
                font=("Helvetica", 12, "bold")
            )
            self.canvas.create_text(
                (xl + xr) / 2 + label_offset_x, mid_y,
                text=right_base, fill=BASE_COLORS[right_base],
                font=("Helvetica", 12, "bold")
            )

    def draw(self):
        # compute visible slice indices
        start = max(0, min(self.total_steps - 1, int(self.view_start)))
        end = max(start + 1, min(self.total_steps, start + int(self.view_length)))
        view_positions = self.positions[start:end]

        # clear canvas and optionally resize height to match view
        self.canvas.delete("all")

        # Optionally, re-center vertically: compute vertical offset so mid of view is centered in canvas
        view_top = view_positions[0][0][1] if view_positions else self.top_margin
        view_bottom = view_positions[-1][0][1] if view_positions else (self.top_margin + self.step_height)
        view_height = view_bottom - view_top + 2 * self.circle_r

        # compute vertical translation to center the view region in canvas
        canvas_center_y = self.height / 2
        view_center_y = (view_top + view_bottom) / 2
        translate_y = canvas_center_y - view_center_y

        # Draw transformed: we will move coordinates by translate_y
        # To avoid recomputing positions array, draw everything with shifted y values by translate_y
        # Use temporary transformed positions
        transformed = []
        for (l, r) in view_positions:
            transformed.append(((l[0], l[1] + translate_y), (r[0], r[1] + translate_y)))

        # draw backbones and rungs using transformed positions
        # We temporarily replace self.positions for drawing convenience (not changing stored positions)
        saved_positions = self.positions
        try:
            # set positions to transformed for the drawing helpers
            self.positions = transformed
            self.draw_backbones(transformed)
            # draw rungs & bases using slice range mapping [start:end] -> 0..len-1
            # but we must adjust the slice to the transformed index range
            # draw_striped_rungs_and_bases expects indices in self.positions, so give 0..len-1
            self.draw_striped_rungs_and_bases(slice(0, len(transformed)))
        finally:
            self.positions = saved_positions

        # draw a central vertical guide (optional, like in your second image)
        self.canvas.create_line(self.center_x, 0, self.center_x, self.height, fill='#cfcfcf', dash=(3, 6))

    # Helper controls for paging and randomize
    def page_next(self):
        self.view_start = min(self.total_steps - self.view_length, self.view_start + int(self.view_length))
        self.draw()

    def page_prev(self):
        self.view_start = max(0, self.view_start - int(self.view_length))
        self.draw()

    def set_view(self, start: int = None, length: int = None):
        if start is not None:
            self.view_start = max(0, min(self.total_steps - 1, int(start)))
        if length is not None:
            self.view_length = max(1, min(self.total_steps, int(length)))
        self.draw()


def main():
    root = tk.Tk()
    root.title("DNA Zoomed Segment Viewer")

    canvas_w = 700
    canvas_h = 800
    canvas = tk.Canvas(root, width=canvas_w, height=canvas_h, bg='white')
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    controls = tk.Frame(root)
    controls.pack(side=tk.RIGHT, fill=tk.Y, padx=8, pady=8)

    dna = DNA(
        canvas,
        total_steps=200,
        amplitude=170,
        step_height=14,
        twist=0.36,
        backbone_width=22,
        circle_r=12,
        rung_thickness=16,
        stripe_count=12,
        center_x=canvas_w // 2,
        top_margin=20,
    )

    # initial view (you can change this)
    dna.view_start = 20
    dna.view_length = 12
    dna.draw()

    # Controls
    start_label = tk.Label(controls, text="Start index:")
    start_label.pack(anchor='w')
    start_var = tk.IntVar(value=dna.view_start)
    start_entry = tk.Entry(controls, textvariable=start_var, width=8)
    start_entry.pack(anchor='w')

    length_label = tk.Label(controls, text="View length:")
    length_label.pack(anchor='w', pady=(8, 0))
    length_var = tk.IntVar(value=dna.view_length)
    length_entry = tk.Entry(controls, textvariable=length_var, width=8)
    length_entry.pack(anchor='w')

    def apply_view():
        try:
            s = int(start_var.get())
            l = int(length_var.get())
        except Exception:
            return
        dna.set_view(start=s, length=l)

    apply_btn = tk.Button(controls, text="Apply view", command=apply_view)
    apply_btn.pack(fill=tk.X, pady=(8, 6))

    prev_btn = tk.Button(controls, text="Previous", command=lambda: [dna.page_prev()])
    prev_btn.pack(fill=tk.X, pady=2)

    next_btn = tk.Button(controls, text="Next", command=lambda: [dna.page_next()])
    next_btn.pack(fill=tk.X, pady=2)

    def randomize():
        dna.generate_sequence()
        dna.compute_positions()
        dna.view_start = 0
        dna.draw()

    rand_btn = tk.Button(controls, text="Randomize sequence", command=randomize)
    rand_btn.pack(fill=tk.X, pady=(12, 2))

    # Quick presets to mimic the look from your sample (wide stripes, spaced steps)
    def preset_sample():
        dna.amplitude = 180
        dna.step_height = 16
        dna.rung_thickness = 18
        dna.stripe_count = 14
        dna.circle_r = 13
        dna.view_length = 10
        dna.compute_positions()
        dna.view_start = 0
        start_var.set(dna.view_start)
        length_var.set(dna.view_length)
        dna.draw()

    preset_btn = tk.Button(controls, text="Preset: stacked slices", command=preset_sample)
    preset_btn.pack(fill=tk.X, pady=(12, 2))

    root.mainloop()


if __name__ == '__main__':
    main()