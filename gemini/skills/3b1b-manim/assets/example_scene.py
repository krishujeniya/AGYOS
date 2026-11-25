from manimlib import *

class MathExplainer(Scene):
    """Reference scene demonstrating 3b1b/manim (manimlib) patterns."""
    def construct(self):
        # Title card
        title = Text("3Blue1Brown Manim Engine", font_size=44)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 2D Coordinate system
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            width=8,
            height=4,
            axis_config={"include_tip": True, "stroke_width": 2}
        )
        axes.center()
        self.play(Create(axes))

        # Sine wave to cosine transformation
        sin_curve = axes.get_graph(lambda x: np.sin(x), color=BLUE)
        cos_curve = axes.get_graph(lambda x: np.cos(x), color=YELLOW)

        sin_label = Tex(r"f(x) = \sin(x)", color=BLUE).next_to(axes, UR)
        cos_label = Tex(r"f'(x) = \cos(x)", color=YELLOW).next_to(axes, UR)

        self.play(ShowCreation(sin_curve), Write(sin_label))
        self.wait(0.8)

        # Transform function and derivative label
        self.play(
            Transform(sin_curve, cos_curve),
            Transform(sin_label, cos_label),
            run_time=1.5
        )
        self.wait(1.0)

        # Derivative formula
        formula = Tex(r"\frac{d}{dx}\sin(x) = \cos(x)", font_size=40)
        formula.to_edge(DOWN)
        self.play(Write(formula))
        self.wait(1.5)
