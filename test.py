"""
from manimlib.imports import *


class EMWave(VGroup):
    def __init__(
        self,
        E_COLOR=YELLOW, M_COLOR=BLUE,
        frequency=1,
        alpha=1,
        num_vects=30,
        start=-FRAME_WIDTH/2,
        end=FRAME_WIDTH/2,
        **kwargs
    ):
        VGroup.__init__(self, **kwargs)
        self.alpha = alpha
        self.frequency = frequency
        self.start = start
        self.end = end
        self.tracker = ValueTracker(0)
        e_wave = VGroup(
            *[self.get_vect(E_COLOR, t, direction=UP) for t in np.linspace(self.start, self.end, num=num_vects)]
        )
        m_wave = VGroup(
            *[self.get_vect(M_COLOR, t, direction=IN) for t in np.linspace(self.start, self.end, num=num_vects)]
        )
        self.add(e_wave)
        self.add(m_wave)

    def get_t(self, value):
        return value - self.start

    def get_vect(self, color, t, direction=IN):
        x = self.get_t(t)
        length = self.alpha * np.sin(x)
        vect = Vector(direction=direction * length,
                      color=color).shift(t * RIGHT)
        vect.add_updater(lambda obj: obj.become(
            self.get_vect_updater(self.tracker.get_value(), color, t, direction=direction)))
        return vect

    def get_vect_updater(self, t, color, phi, direction=IN):
        x = self.get_t(t)
        length = self.alpha * np.sin(self.frequency * x + self.frequency * phi)
        return Vector(length * direction, color=color).shift(phi * RIGHT)


class Wave(VGroup):
    def __init__(
        self,
        E_COLOR=YELLOW, M_COLOR=BLUE,
        frequency=1,
        alpha=1,
        num_vects=30,
        start=-FRAME_WIDTH/2,
        end=FRAME_WIDTH/2,
        direction=IN,
        **kwargs
    ):
        VGroup.__init__(self, **kwargs)
        self.alpha = alpha
        self.frequency = frequency
        self.start = start
        self.end = end
        self.tracker = ValueTracker(0)
        wave = VGroup(
            *[self.get_vect(E_COLOR, t, direction=direction) for t in np.linspace(self.start, self.end, num=num_vects)]
        )
        self.add(wave)

    def get_t(self, value):
        return value - self.start

    def get_vect(self, color, t, direction=IN):
        x = self.get_t(t)
        length = self.alpha * np.sin(x)
        vect = VGroup(
            Line(ORIGIN, direction * length, color=color).shift(t * RIGHT),
        )
        tip = ArrowTip(
            start_angle=PI/2,
            color=color).shift(direction * length).shift(t * RIGHT).rotate(axis=[1, 0, 0], angle=PI/2).rotate(axis=[1, 0, 0], angle=PI)
        # if direction * length
        vect.add(tip)
        return vect



"""

from manimlib.imports import *


class LmaoArrow(Line):
    """
    CONFIG = {
        "tip_length": 0.25,
        "tip_width_to_length_ratio": 1,
        "max_tip_length_to_length_ratio": 0.35,
        "max_stem_width_to_tip_width_ratio": 0.3,
        "buff": MED_SMALL_BUFF,
        "propagate_style_to_family": False,
        "preserve_tip_size_when_scaling": True,
        "normal_vector": OUT,
        "use_rectangular_stem": True,
        "rectangular_stem_width": 0.05,
    }

    def __init__(self, *args, **kwargs):
        points = list(map(self.pointify, args))
        if len(args) == 1:
            args = (points[0] + UP + LEFT, points[0])
        Line.__init__(self, *args, **kwargs)
        self.init_tip()
        if self.use_rectangular_stem and not hasattr(self, "rect"):
            self.add_rectangular_stem()
        self.init_colors()

    def init_tip(self):
        self.add_tip()

    def add_tip(self, add_at_end=True):
        tip = VMobject(
            close_new_points=True,
            mark_paths_closed=True,
            fill_color=self.color,
            fill_opacity=1,
            stroke_color=self.color,
            stroke_width=0,
        )
        tip.add_at_end = add_at_end
        self.set_tip_points(tip, add_at_end, preserve_normal=False)
        self.add(tip)
        if not hasattr(self, 'tip'):
            self.tip = VGroup()
            self.tip.match_style(tip)
        self.tip.add(tip)
        return tip

    def add_rectangular_stem(self):
        self.rect = Rectangle(
            stroke_width=0,
            fill_color=self.tip.get_fill_color(),
            fill_opacity=self.tip.get_fill_opacity()
        )
        self.add_to_back(self.rect)
        self.set_stroke(width=0)
        self.set_rectangular_stem_points()

    def set_rectangular_stem_points(self):
        start, end = self.get_start_and_end()
        tip_base_points = self.tip[0].get_anchors()[1:3]
        tip_base = center_of_mass(tip_base_points)
        tbp1, tbp2 = tip_base_points
        perp_vect = tbp2 - tbp1
        tip_base_width = get_norm(perp_vect)
        if tip_base_width > 0:
            perp_vect /= tip_base_width
        width = min(
            self.rectangular_stem_width,
            self.max_stem_width_to_tip_width_ratio * tip_base_width,
        )
        if hasattr(self, "second_tip"):
            start = center_of_mass(
                self.second_tip.get_anchors()[1:]
            )
        self.rect.set_points_as_corners([
            tip_base - perp_vect * width / 2,
            start - perp_vect * width / 2,
            start + perp_vect * width / 2,
            tip_base + perp_vect * width / 2,
        ])
        self.stem = self.rect  # Alternate name
        return self

    def set_tip_points(
        self, tip,
        add_at_end=True,
        tip_length=None,
        preserve_normal=True,
    ):
        if tip_length is None:
            tip_length = self.tip_length
        if preserve_normal:
            normal_vector = self.get_normal_vector()
        else:
            normal_vector = self.normal_vector
        line_length = get_norm(self.points[-1] - self.points[0])
        tip_length = min(
            tip_length, self.max_tip_length_to_length_ratio * line_length
        )

        indices = (-2, -1) if add_at_end else (1, 0)
        pre_end_point, end_point = [
            self.get_anchors()[index]
            for index in indices
        ]
        vect = end_point - pre_end_point
        perp_vect = np.cross(vect, normal_vector)
        for v in vect, perp_vect:
            if get_norm(v) == 0:
                v[0] = 1
            v *= tip_length / get_norm(v)
        ratio = self.tip_width_to_length_ratio
        tip.set_points_as_corners([
            end_point,
            end_point - vect + perp_vect * ratio / 2,
            end_point - vect - perp_vect * ratio / 2,
        ])

        return self

    def get_normal_vector(self):
        p0, p1, p2 = self.tip[0].get_anchors()[:3]
        result = np.cross(p2 - p1, p1 - p0)
        norm = get_norm(result)
        if norm == 0:
            return self.normal_vector
        else:
            return result / norm

    def reset_normal_vector(self):
        self.normal_vector = self.get_normal_vector()
        return self

    def get_end(self):
        if hasattr(self, "tip"):
            return self.tip[0].get_anchors()[0]
        else:
            return Line.get_end(self)

    def get_tip(self):
        return self.tip

    def put_start_and_end_on(self, *args, **kwargs):
        Line.put_start_and_end_on(self, *args, **kwargs)
        self.set_tip_points(self.tip[0], preserve_normal=False)
        self.set_rectangular_stem_points()
        return self

    def scale(self, scale_factor, **kwargs):
        Line.scale(self, scale_factor, **kwargs)
        if self.preserve_tip_size_when_scaling:
            for t in self.tip:
                self.set_tip_points(t, add_at_end=t.add_at_end)
        if self.use_rectangular_stem:
            self.set_rectangular_stem_points()
        return self

    def copy(self):
        return self.deepcopy()
"""

class LmaoVector(LmaoArrow):
    CONFIG = {
        "color": YELLOW,
        "buff": 0,
    }

    def __init__(self, direction, **kwargs):
        if len(direction) == 2:
            direction = np.append(np.array(direction), 0)
        LmaoArrow.__init__(self, ORIGIN, direction, **kwargs)


class EMTest(Scene):
    def construct(self):
        vect = LmaoVector(2 * UP)

        #tip = ArrowTip(start_angle=PI/2).shift([0, 0, 1])
        #vect = Wave()
        #self.move_camera(0.4 * np.pi / 2, -PI/2)
        self.add(vect)
        self.wait()
        #wave = EMWave()
        # self.add(wave)
        # self.play(wave.tracker.increment_value, 4 *
        # PI, run_time=4, rate_func=linear)


"""
class EMScene(Scene):
    CONFIG = {
        "frequency": 1,
        "num_vects": 30,
        "alpha": 1,
        "run_time": 8,
        "osc_freq": 1
    }

    def construct(self):
        self.tracker = ValueTracker(0)
        wave = VGroup(
            *[self.get_vect(YELLOW, t) for t in np.linspace(-2*PI, 2*PI, num=self.num_vects)]
        )
        self.play(Write(wave))
        self.play(
            self.tracker.increment_value,
            self.osc_freq * self.run_time * PI,
            run_time=self.run_time,
            rate_func=linear
        )
        self.wait()

    def get_vect(self, color, t):
        length = self.alpha * np.sin(t)
        vect = Vector(direction=np.array(
            [0, length, 0]), color=color).shift(t * RIGHT)
        vect.add_updater(lambda x: x.become(
            self.get_vect_updater(self.tracker.get_value(), color, t)))
        return vect

    def get_vect_updater(self, t, color, phi):
        length = self.alpha * np.sin(self.frequency * t + self.frequency * phi)
        return Vector([0, length, 0], color=color).shift(phi * RIGHT)
"""
