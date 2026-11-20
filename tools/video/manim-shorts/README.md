# Manim Shorts (Vertical Mathematical Animations)

This toolkit provides vertical (9:16 portrait) scene primitives, safe-zone layouts, and headless execution commands for rendering mathematical and technical explainer animations using 3Blue1Brown's Manim (`manimlib` / `3b1b/manim`).

---

## Technical Specifications

- **Aspect Ratio**: 9:16 vertical orientation (1080x1920 pixels).
- **Safe Zone**:
  - Vertical Bounds: Between $Y = -6.0$ and $Y = 6.0$ in Manim units (leaving margin clear for platform header and bottom comments).
  - Pixel Safe Zone: Central 1080x1400 window (200px top clearance, 320px bottom clearance).
- **Execution Mode**: Strictly headless (`-w` flag) without opening GUI windows.

---

## Directory Structure

```
tools/video/manim-shorts/
├── README.md                          # Architecture and usage manual
└── templates/
    └── vertical_scene.py              # Base class with safe-zone guides & 9:16 framing
```

---

## Headless CLI Invocations

All renders run headlessly using the `manimgl` command:

```bash
# 480p preview smoke test
manimgl path/to/scene.py SceneClassName -w -l

# Full HD vertical production render (1080x1920 @ 60fps)
manimgl path/to/scene.py SceneClassName -w --hd

# Save terminal thumbnail frame
manimgl path/to/scene.py SceneClassName -s
```
