from manimlib import *
from manim_fonts import *


class CurvedConnector(CubicBezier):
    def __init__(self, start_obj, end_obj, **kwargs):
        start_point = start_obj.get_center() + start_obj.get_width() / 2 * RIGHT
        end_point = end_obj.get_center() + end_obj.get_width() / 2 * LEFT

        control_points = [
            start_point,
            start_point + 0.5 * RIGHT,
            end_point + 0.5 * LEFT,
            end_point,
        ]

        super().__init__(*control_points, **kwargs)


class Ghostbuster(Scene):
    def construct(self):
        brect = Rectangle(
            height=FRAME_HEIGHT,
            width=FRAME_WIDTH,
            color=WHITE,
            fill_opacity=1,
        )
        self.add(brect)

        inp_rect = Rectangle(
            height=3.75,
            width=3.0,
            fill_color="#f3f3f3",
            fill_opacity=1,
            stroke_color=BLACK,
        )
        inp_rect.move_to(5.5 * LEFT)

        model_rects = VGroup()
        for i in range(4):
            model_rects.add(
                Rectangle(
                    height=1.0,
                    width=2.0,
                    fill_opacity=1,
                    fill_color="#d9d2e9",
                    stroke_color=BLACK,
                ).move_to(1.5 * i * DOWN)
            )
        model_rects.move_to(2.5 * LEFT)

        features = [
            "max(ada / davinci + ada)",
            "var(davinci / ada - davinci)",
            "var(unigram * davinci)",
            "avg(unigram - ada > davinci)",
            None,
            "avg(unigram + trigram < davinci)",
        ]

        feature_rects = VGroup()
        for i in range(len(features)):
            if i == len(features) - 2:
                dots = Tex(r"\vdots", color=BLACK)
                dots.scale(1.5)
                feature_rects.add(dots)
            else:
                r = Rectangle(
                    width=3.75,
                    height=0.5,
                    fill_opacity=1,
                    fill_color="#d0e2f3",
                    stroke_color=BLACK,
                )
                feature_rects.add(r)

                text = Text(features[i], color=BLACK)
                text.scale(0.45)
                text.move_to(r)
                r.add(text)

            feature_rects[-1].shift(0.75 * i * DOWN)

        feature_rects.move_to(0.5 * LEFT, aligned_edge=LEFT)

        lr_rect = Rectangle(
            width=3.0,
            height=4.0,
            fill_opacity=1,
            fill_color="#fce5cd",
            stroke_color=BLACK,
        )
        lr_rect.move_to(5.5 * RIGHT)

        VGroup(
            inp_rect,
            model_rects,
            feature_rects,
            lr_rect,
        ).scale(0.95).center()

        inp_text_raw = """It was a typical\nFriday night, and I\nhad decided to\nspend it at home,\nbrowsing the\ninternet and\ncatching up on some\nof my favorite\nshows. My roommate\nhad gone...\n"""
        with RegisterFont("Ubuntu") as fonts:
            inp_text = Text(inp_text_raw, font=fonts[0], color=BLACK)
            inp_text.scale(0.55)
        inp_text.move_to(inp_rect)

        with RegisterFont("Ubuntu") as fonts:
            for i in range(len(model_rects)):
                model_rects[i].add(
                    Text(
                        ["Unigram", "Trigram", "GPT-3 Ada", "GPT-3 Davinci"][i],
                        font=fonts[0],
                        color=BLACK,
                    )
                    .scale(0.55)
                    .move_to(model_rects[i])
                )

            lr_text = Text(
                "Logistic\nRegression\nClassifier", font=fonts[0], color=BLACK
            )
            lr_text.scale(0.55)
            lr_text.move_to(lr_rect, UP)
            lr_text.shift(0.25 * DOWN)

            old_center = lr_text[0:8].get_center()
            lr_text[0:8].move_to([lr_rect.get_center()[0], old_center[1], 0])

            old_center = lr_text[9:22].get_center()
            lr_text[9:22].move_to([lr_rect.get_center()[0], old_center[1], 0])

            old_center = lr_text[22:].get_center()
            lr_text[22:].move_to([lr_rect.get_center()[0], old_center[1], 0])

        inp_model_conn = VGroup()
        for i in range(len(model_rects)):
            inp_model_conn.add(
                Line(
                    inp_rect.get_right(),
                    model_rects[i].get_left(),
                    stroke_color=GREY_D,
                    stroke_opacity=0.75,
                )
            )

        model_feature_conn, feature_lr_conn = VGroup(), VGroup()
        for i in range(len(feature_rects)):
            if not features[i]:
                model_feature_conn.add(VGroup())
                continue

            curr_lines = VGroup()
            if "unigram" in features[i]:
                curr_lines.add(
                    Line(
                        model_rects[0].get_right(),
                        feature_rects[i].get_left(),
                        color=GREY_D,
                        stroke_opacity=0.75,
                    )
                )

            if "trigram" in features[i]:
                curr_lines.add(
                    Line(
                        model_rects[1].get_right(),
                        feature_rects[i].get_left(),
                        color=GREY_D,
                        stroke_opacity=0.75,
                    )
                )

            if "ada" in features[i]:
                curr_lines.add(
                    Line(
                        model_rects[2].get_right(),
                        feature_rects[i].get_left(),
                        color=GREY_D,
                        stroke_opacity=0.75,
                    )
                )

            if "davinci" in features[i]:
                curr_lines.add(
                    Line(
                        model_rects[3].get_right(),
                        feature_rects[i].get_left(),
                        color=GREY_D,
                        stroke_opacity=0.75,
                    )
                )

            model_feature_conn.add(curr_lines)
            feature_lr_conn.add(
                Line(
                    feature_rects[i].get_right(),
                    lr_rect.get_left(),
                    color=GREY_D,
                    stroke_opacity=0.75,
                )
            )

        axes = Axes(
            x_range=(0, 5),
            y_range=(0, 5),
            height=2.25,
            width=2.25,
            axis_config={"include_tip": False, "color": BLACK, "tick_size": 0.05},
        )
        axes.move_to(lr_rect)
        axes.shift(0.5 * DOWN)

        dots = VGroup()
        np.random.seed(0)
        for _ in range(100):
            x, y = (
                np.random.uniform(0, 5),
                np.random.uniform(0, 5),
            )
            dots.add(
                Dot(
                    axes.c2p(x, y),
                    radius=0.025,
                    color=MAROON_E if x > y else GREEN_E,
                )
            )
        line = Line(axes.c2p(0, 0), axes.c2p(5, 5), color=GREY, stroke_width=2.5)

        self.play(Write(inp_rect), Write(inp_text))
        self.wait()

        for i in range(len(model_rects)):
            self.play(ShowCreation(inp_model_conn[i]), GrowFromCenter(model_rects[i]))
        self.wait()

        for i in range(len(features)):
            if not features[i]:
                self.play(GrowFromCenter(feature_rects[i]))
            else:
                self.play(
                    ShowCreation(model_feature_conn[i]),
                    GrowFromCenter(feature_rects[i]),
                )
        self.wait()

        self.play(ShowCreation(feature_lr_conn))
        self.play(Write(lr_rect), Write(lr_text))
        self.play(Write(axes), Write(dots), Write(line))
        self.wait()

        self.embed()


class GhostbusterFigure(Scene):
    def construct(self):
        brect = Rectangle(
            height=FRAME_HEIGHT,
            width=FRAME_WIDTH,
            color=WHITE,
            fill_opacity=1,
        )
        self.add(brect)

        inp_rect = Rectangle(
            height=3.75,
            width=3.0,
            fill_color="#f3f3f3",
            fill_opacity=1,
            stroke_color=BLACK,
        )
        inp_rect.move_to(5.5 * LEFT)

        model_rects = VGroup()
        for i in range(3):
            model_rects.add(
                Rectangle(
                    height=1.0,
                    width=2.0,
                    fill_opacity=1,
                    fill_color="#d9d2e9",
                    stroke_color=BLACK,
                ).move_to(2.25 * LEFT + (1.5 - i * 1.5) * UP)
            )

        vector_rect = Rectangle(
            width=1.5,
            height=4.5,
            fill_opacity=1,
            fill_color="#a0c5e8",
            stroke_color=BLACK,
        )
        vector_rect.move_to(0.25 * RIGHT)

        scalar_rect = Rectangle(
            width=1.5,
            height=4.5,
            fill_opacity=1,
            fill_color="#70a8dc",
            stroke_color=BLACK,
        )
        scalar_rect.move_to(2.5 * RIGHT)

        lr_rect = Rectangle(
            width=3.0,
            height=4.0,
            fill_opacity=1,
            fill_color="#fce5cd",
            stroke_color=BLACK,
        )
        lr_rect.move_to(5.5 * RIGHT)

        VGroup(
            inp_rect,
            model_rects,
            vector_rect,
            scalar_rect,
            lr_rect,
        ).scale(0.95).center()

        inp_text_raw = """It was a typical\nFriday night, and I\nhad decided to\nspend it at home,\nbrowsing the\ninternet and\ncatching up on some\nof my favorite\nshows. My roommate\nhad gone...\n"""
        with RegisterFont("Ubuntu") as fonts:
            inp_text = Text(inp_text_raw, font=fonts[0], color=BLACK)
            inp_text.scale(0.55)
        inp_text.move_to(inp_rect)

        model_text = VGroup()
        with RegisterFont("Ubuntu") as fonts:
            for i in range(3):
                model_text.add(
                    Text(
                        ["Unigram", "Trigram", "GPT-3"][i],
                        font=fonts[0],
                        color=BLACK,
                    )
                    .scale(0.55)
                    .move_to(model_rects[i])
                )

        with RegisterFont("Ubuntu") as fonts:
            vector_text = Text("Vector\nFunctions", font=fonts[0], color=BLACK)
            vector_text.scale(0.55)
            vector_text.move_to(vector_rect, UP)
            vector_text.shift(0.25 * DOWN)

            old_center = vector_text[0:6].get_center()
            vector_text[0:6].move_to([vector_rect.get_center()[0], old_center[1], 0])

            scalar_text = Text("Scalar\nFunctions", font=fonts[0], color=BLACK)
            scalar_text.scale(0.55)
            scalar_text.move_to(scalar_rect, UP)
            scalar_text.shift(0.25 * DOWN)

            old_center = scalar_text[0:6].get_center()
            scalar_text[0:6].move_to([scalar_rect.get_center()[0], old_center[1], 0])

            lr_text = Text(
                "Logisitic\nRegression\nClassifier", font=fonts[0], color=BLACK
            )
            lr_text.scale(0.55)
            lr_text.move_to(lr_rect, UP)
            lr_text.shift(0.25 * DOWN)

            old_center = lr_text[0:9].get_center()
            lr_text[0:9].move_to([lr_rect.get_center()[0], old_center[1], 0])

            old_center = lr_text[9:22].get_center()
            lr_text[9:22].move_to([lr_rect.get_center()[0], old_center[1], 0])

            old_center = lr_text[23:].get_center()
            lr_text[23:].move_to([lr_rect.get_center()[0], old_center[1], 0])

        inp_model_conn, model_vector_conn = VGroup(), VGroup()
        for i in range(3):
            inp_model_conn.add(CurvedConnector(inp_rect, model_rects[i], color=BLACK))
            model_vector_conn.add(
                CurvedConnector(model_rects[i], vector_rect, color=BLACK)
            )

        vector_scalar_conn = CurvedConnector(vector_rect, scalar_rect, color=BLACK)

        scalar_lr_conn = VGroup()
        for i in range(3):
            scalar_lr_conn.add(
                CurvedConnector(
                    scalar_rect.copy().shift(1.5 * (i - 1) * UP), lr_rect, color=BLACK
                )
            )

        vector_circles = VGroup()
        vector_tex = ["+", r"\cross", ">"]

        for i in range(3):
            vector_circles.add(
                Circle(
                    radius=0.45,
                    stroke_color=BLACK,
                    fill_color="#d0e2f3",
                    fill_opacity=1,
                ).shift(1.1 * i * UP)
            )

            vector_circles.add(
                Tex(vector_tex[i], color=BLACK).scale(0.75).move_to(vector_circles[-1])
            )

        vector_circles.move_to(vector_rect)
        vector_circles.shift(0.375 * DOWN)

        scalar_circles = VGroup()
        scalar_tex = [r"||x||_2", r"\max", r"\mathrm{var}"]

        for i in range(3):
            scalar_circles.add(
                Circle(
                    radius=0.45,
                    stroke_color=BLACK,
                    fill_color="#d0e2f3",
                    fill_opacity=1,
                ).shift(1.1 * i * UP)
            )

            scalar_circles.add(
                Tex(scalar_tex[i], color=BLACK).scale(0.75).move_to(scalar_circles[-1])
            )
        scalar_circles.move_to(scalar_rect)
        scalar_circles.shift(0.375 * DOWN)

        axes = Axes(
            x_range=(0, 5),
            y_range=(0, 5),
            height=2.25,
            width=2.25,
            axis_config={"include_tip": False, "color": BLACK, "tick_size": 0.05},
        )
        axes.move_to(lr_rect)
        axes.shift(0.5 * DOWN)

        dots = VGroup()
        np.random.seed(0)
        for _ in range(100):
            x, y = (
                np.random.uniform(0, 5),
                np.random.uniform(0, 5),
            )
            dots.add(
                Dot(
                    axes.c2p(x, y),
                    radius=0.025,
                    color=MAROON_E if x > y else GREEN_E,
                )
            )
        line = Line(axes.c2p(0, 0), axes.c2p(5, 5), color=GREY, stroke_width=2.5)

        self.play(Write(inp_rect), Write(inp_text), run_time=1)

        self.play(
            Write(inp_model_conn[0]),
            Write(model_rects[0]),
            Write(model_text[0]),
            run_time=1,
        )

        word_len = list(map(len, inp_text_raw.split()))

        for i in range(5):
            self.play(
                TransformFromCopy(
                    inp_text[sum(word_len[:i]) + i : sum(word_len[: i + 1]) + i],
                    inp_text[sum(word_len[:i]) + i : sum(word_len[: i + 1]) + i]
                    .copy()
                    .move_to(model_text[0])
                    .set_opacity(0),
                ),
                run_time=0.5,
            )

        self.play(
            Write(inp_model_conn[1]),
            Write(model_rects[1]),
            Write(model_text[1]),
            run_time=1,
        )

        for i in range(5):
            self.play(
                TransformFromCopy(
                    inp_text[sum(word_len[:i]) + i : sum(word_len[: i + 3]) + 3],
                    inp_text[sum(word_len[:i]) + i : sum(word_len[: i + 3]) + 3]
                    .copy()
                    .move_to(model_text[1])
                    .set_opacity(0),
                ),
                run_time=0.5,
            )

        self.play(
            Write(inp_model_conn[2]),
            Write(model_rects[2]),
            Write(model_text[2]),
            run_time=1,
        )

        self.play(
            TransformFromCopy(
                inp_text,
                inp_text.copy().move_to(model_text[2]).set_opacity(0),
            ),
            run_time=0.5,
        )

        self.play(
            Write(model_vector_conn),
            Write(vector_rect),
            Write(vector_text),
            Write(vector_circles),
            run_time=1,
        )

        self.play(
            Write(vector_scalar_conn),
            Write(scalar_rect),
            Write(scalar_text),
            Write(scalar_circles),
            run_time=1,
        )

        self.play(
            Write(scalar_lr_conn),
            Write(lr_rect),
            Write(lr_text),
            run_time=1,
        )

        self.play(
            Write(axes),
            Write(dots),
            Write(line),
            run_time=1,
        )

        with RegisterFont("Ubuntu") as fonts:
            feature_one_raw = "var(Unigram + GPT-3)"
            feature_one = Text(feature_one_raw, font=fonts[0], color=BLACK)
            feature_one.scale(1.25)
            feature_one.shift(3 * UP)

        feature_one_grp = VGroup(
            model_text[0],
            model_text[2],
            vector_circles[1],
            scalar_circles[-1],
        )

        self.play(*[Indicate(i, color=YELLOW_D) for i in feature_one_grp])
        self.wait()

        self.play(
            TransformFromCopy(
                feature_one_grp[0],
                feature_one[
                    feature_one_raw.find("Unigram") : feature_one_raw.find("Unigram")
                    + 7
                ],
            )
        )

        self.play(
            TransformFromCopy(
                feature_one_grp[1],
                feature_one[
                    feature_one_raw.find("GPT-3") : feature_one_raw.find("GPT-3") + 5
                ],
            )
        )

        self.play(
            TransformFromCopy(
                feature_one_grp[2],
                feature_one[feature_one_raw.find("+") : feature_one_raw.find("+") + 1],
            )
        )

        self.play(
            TransformFromCopy(
                feature_one_grp[3],
                feature_one[
                    feature_one_raw.find("var") : feature_one_raw.find("var") + 3
                ],
            ),
        )

        self.play(
            Write(feature_one[feature_one_raw.find("(")]),
            Write(feature_one[feature_one_raw.find(")")]),
        )

        self.wait()

        self.play(Transform(feature_one, Dot().move_to(lr_rect).set_opacity(0)))
        self.wait()

        self.embed()
