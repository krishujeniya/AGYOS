"""Vertical Manim Scene base class for 9:16 mathematical animations."""
from __future__ import annotations

try:
    from manimlib import *  # type: ignore
except ImportError:
    # Graceful fallback when manimlib is not installed locally
    class Scene:  # type: ignore
        pass


class VerticalScene(Scene):
    """Base scene class configured for 9:16 portrait short-form video."""

    # 9:16 Aspect ratio coordinate dimensions in Manim units
    FRAME_WIDTH: float = 9.0
    FRAME_HEIGHT: float = 16.0

    # Safe zone boundaries in Manim world units (central 1080x1400 window)
    SAFE_TOP_Y: float = 6.0       # Leaves top margin clear of username/search
    SAFE_BOTTOM_Y: float = -6.0   # Leaves bottom margin clear of captions/sound bar
    SAFE_LEFT_X: float = -4.0     # Horizontal padding
    SAFE_RIGHT_X: float = 4.0

    def setup(self) -> None:
        """Initialize frame dimensions for vertical 9:16 orientation."""
        if hasattr(super(), "setup"):
            super().setup()
        if hasattr(self, "frame"):
            self.frame.set_width(self.FRAME_WIDTH)
            self.frame.set_height(self.FRAME_HEIGHT)

    def get_safe_center(self) -> list[float]:
        """Return the center coordinates of the safe viewing zone."""
        return [0.0, 0.0, 0.0]

    def get_safe_top(self) -> list[float]:
        """Return the top coordinate vector for title cards inside the safe zone."""
        return [0.0, self.SAFE_TOP_Y, 0.0]

    def get_safe_bottom(self) -> list[float]:
        """Return the bottom coordinate vector for terminal callouts inside the safe zone."""
        return [0.0, self.SAFE_BOTTOM_Y, 0.0]

    def is_within_safe_zone(self, point: list[float] | tuple[float, ...]) -> bool:
        """Check whether a given 2D/3D coordinate resides inside the safe zone."""
        x, y = point[0], point[1]
        return (
            self.SAFE_LEFT_X <= x <= self.SAFE_RIGHT_X
            and self.SAFE_BOTTOM_Y <= y <= self.SAFE_TOP_Y
        )
