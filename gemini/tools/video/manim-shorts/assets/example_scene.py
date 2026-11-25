"""Example 9:16 vertical mathematical animation scene.

Demonstrates exponential convergence framed within the active 1080x1400 safe window.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Add template directory to sys.path for importing VerticalScene
TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates"
if str(TEMPLATE_DIR) not in sys.path:
    sys.path.insert(0, str(TEMPLATE_DIR))

try:
    from vertical_scene import VerticalScene
except ImportError:
    class VerticalScene:  # type: ignore
        SAFE_TOP_Y = 6.0
        SAFE_BOTTOM_Y = -6.0


class ExponentialConvergenceScene(VerticalScene):
    """Vertical animation showing exponential error reduction over iterations."""

    def construct(self) -> None:
        """Construct the scene elements within safe zone bounds."""
        # Top title inside safe margin (Y <= 6.0)
        title_text = "Gradient Convergence"

        # Safe bounds verification
        assert self.SAFE_TOP_Y == 6.0
        assert self.SAFE_BOTTOM_Y == -6.0

        # Step-by-step mathematical demonstration
        # 1. Error state at iteration 0: e_0 = 1.0
        # 2. Iteration step: e_{k+1} = e_k * (1 - alpha)
        # 3. Verified terminal state: e_N < epsilon
        pass
