---
name: 3b1b-manim
description: "Programmatic mathematical animation and technical explainer engine using 3Blue1Brown's Manim (manimlib/manimgl) for 2D/3D geometry, calculus, linear algebra, coordinate transformations, and headless video rendering."
---

# 3Blue1Brown Manim (manimlib)

This skill guides the construction and rendering of programmatic mathematical animations and technical explainer videos using 3Blue1Brown's original animation engine ([3b1b/manim](https://github.com/3b1b/manim)).

---

## 3b1b/manim vs. ManimCommunity

Understanding the distinction between the two primary Manim ecosystems prevents syntax and import failures:

| Feature | 3Blue1Brown Manim (`3b1b/manim`) | Manim Community (`ManimCommunity/manim`) |
|---|---|---|
| **Python Import** | `from manimlib import *` | `from manim import *` |
| **CLI Command** | `manimgl` | `manim` |
| **Rendering Engine** | Modern OpenGL + ModernGL shaders | Cairo + FFmpeg / ModernGL |
| **Interactivity** | Native interactive inspection window | Experimental via `--write_to_movie` / `-p` |
| **Camera Control** | `self.frame` (Euler angles, focal distance) | `self.camera` (CameraFrame) |
| **Creation Animation** | `ShowCreation(mobject)` | `Create(mobject)` |

---

## Command Line Interface (`manimgl`)

### Headless Rendering (Standard AGYOS Invariant)

To render animations without opening a GUI window, pass the `-w` (write) flag:

```bash
# Fast low-resolution preview (480p, 30fps)
manimgl path/to/scene.py SceneClassName -w -l

# Full HD production render (1080p, 60fps)
manimgl path/to/scene.py SceneClassName -w --hd

# 4K UHD render (2160p, 60fps)
manimgl path/to/scene.py SceneClassName -w --uhd

# Save the final frame as an image (thumbnail generation)
manimgl path/to/scene.py SceneClassName -s
```

Common flags:
- `-w` / `--write_file`: Write the scene directly to a video file.
- `-o` / `--open`: Write to file and open in default media player.
- `-s` / `--save_last_frame`: Output a single PNG image of the final frame.
- `-l` / `--low_quality`: 480p @ 30 fps (ideal for smoke tests).
- `--hd`: 1080p @ 60 fps.
- `-t` / `--transparent`: Render with alpha transparency channel.

---

## Scene Architecture

Every 3b1b/manim video script subclassing `Scene` defines a `construct` method:

```python
from manimlib import *

class LinearTransformation(Scene):
    def construct(self):
        # 1. Setup coordinate grid
        plane = NumberPlane()
        self.play(ShowCreation(plane))

        # 2. Vector definitions
        v = Vector([2, 1], color=YELLOW)
        self.play(ShowCreation(v))
        self.wait(0.5)

        # 3. Apply matrix transformation
        matrix = [[1, 2], [0, 1]]
        self.play(plane.animate.apply_matrix(matrix), run_time=2)
        self.wait(1)
```

### 3D Coordinate Spaces and Camera Manipulation

In `manimlib`, 3D scenes manipulate `self.frame`:

```python
from manimlib import *

class SurfaceExplainer(Scene):
    def construct(self):
        axes = ThreeDAxes()
        self.play(ShowCreation(axes))

        # Rotate camera to isometric 3D perspective
        self.frame.set_euler_angles(theta=-30 * DEGREES, phi=70 * DEGREES)

        surface = ParametricSurface(
            lambda u, v: np.array([u, v, np.sin(u) * np.cos(v)]),
            u_range=[-2, 2],
            v_range=[-2, 2],
            color=BLUE_D
        )
        self.play(ShowCreation(surface))
        self.wait(1)
```

---

## Core Mathematical Objects

1. **LaTeX and Typography**:
   - `Tex(r"\int_{a}^{b} f(x) dx")`: Math typesetting via LaTeX.
   - `Text("Hello World", font_size=36)`: System font text.
   - `DecimalNumber(0.0)`: Updatable animated numeric values.
2. **Coordinate Systems**:
   - `Axes(x_range=[min, max, step], y_range=[min, max, step])`
   - `NumberPlane()`: Full Cartesian 2D grid.
   - `ThreeDAxes()`: 3D coordinate system.
3. **Geometry Primitives**:
   - `Circle`, `Square`, `Rectangle`, `Polygon`, `Dot`, `Line`, `Arrow`.
4. **Calculus & Curves**:
   - `axes.get_graph(lambda x: x**2, color=RED)`: Functional graph plotting.
   - `axes.get_riemann_rectangles(graph, x_range=[0, 3], dx=0.2)`: Integral approximations.

---

## Reusable Reference Scene

Inspect [assets/example_scene.py](assets/example_scene.py) for an implementation featuring:
- 2D coordinate system setup.
- Sine to cosine curve derivation.
- Smooth object transformations (`Transform`).
- Mathematical equation rendering with LaTeX typography.

---

## Production Rules

1. **One Concept per Scene**: Structure multi-step topics across distinct scenes or chapters.
2. **Always Run Smoke Render First**: Execute `-w -l` smoke tests before running full `--hd` builds.
3. **Isolate Calculations from Animations**: Compute coordinate lists or matrix arrays before invoking `self.play`.
4. **Strict Headless Execution**: Always include the `-w` flag during automated or scripted runs to prevent headless display errors.
