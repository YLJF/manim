from helpers import *

from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject
from mobject.vectorized_mobject import *

from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from animation.playground import *
from topics.geometry import *
from topics.characters import *
from topics.functions import *
from topics.fractals import *
from topics.number_line import *
from topics.combinatorics import *
from topics.numerals import *
from topics.three_dimensions import *
from topics.objects import *
from scene import Scene
from scene.zoomed_scene import ZoomedScene
from scene.reconfigurable_scene import ReconfigurableScene
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *

from topics.common_scenes import OpeningQuote, PatreonThanks

from eoc.graph_scene import *

class ExpFootnoteOpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
        "Who has not been amazed to learn that the function",
        "$y = e^x$,", "like a phoenix rising again from its own",
        "ashes, is its own derivative?",
        ],
        "highlighted_quote_terms" : {
            "$y = e^x$" : MAROON_B
        },
        "author" : "Francois le Lionnais"
    }

class LastVideo(TeacherStudentsScene):
    def construct(self):
        series = VideoSeries()
        series.to_edge(UP)
        last_video = series[2]
        last_video.save_state()
        this_video = series[3]

        known_formulas = VGroup(*map(TexMobject, [
            "\\frac{d(x^n)}{dx} = nx^{n-1}",
            "\\frac{d(\\sin(x))}{dx} = \\cos(x)",
        ]))
        known_formulas.arrange_submobjects(
            DOWN, buff = MED_LARGE_BUFF,
        )
        known_formulas.scale_to_fit_height(2.5)
        exp_question = TexMobject("2^x", ", 7^x", ", e^x", " ???")

        last_video_brace = Brace(last_video)
        known_formulas.next_to(last_video_brace, DOWN)
        last_video_brace.save_state()
        last_video_brace.shift(3*LEFT)
        last_video_brace.set_fill(opacity = 0)

        self.add(series)
        self.play(
            last_video_brace.restore,
            last_video.highlight, YELLOW,
            self.get_teacher().change_mode, "raise_right_hand",
        )
        self.play(Write(known_formulas))
        self.dither()
        self.student_says(
            exp_question, student_index = -1,
            added_anims = [self.get_teacher().change_mode, "pondering"]
        )
        self.dither(2)
        self.play(known_formulas.replace, last_video)
        self.play(last_video_brace.next_to, this_video, DOWN)
        self.play(
            last_video.restore,
            this_video.highlight, YELLOW
        )
        self.play(       
            exp_question.next_to, last_video_brace, DOWN,
            FadeOut(self.get_students()[-1].bubble),
        )
        self.change_student_modes(
            *["pondering"]*3,
            look_at_arg = exp_question
        )
        self.dither()

class PopulationSizeGraphVsPopulationMassGraph(Scene):
    def construct(self):
        pass

class DoublingPopulation(PiCreatureScene):
    CONFIG = {
        "time_color" : YELLOW,
        "pi_creature_grid_dimensions" : (8, 8),
        "pi_creature_grid_height" : 6,
    }
    
    def construct(self):
        self.remove(self.get_pi_creatures())
        self.introduce_expression()
        self.introduce_pi_creatures()
        self.count_through_days()
        self.ask_about_dM_dt()
        self.growth_per_day()
        self.relate_growth_rate_to_pop_size()

    def introduce_expression(self):
        f_x = TexMobject("f(x)", "=", "2^x")
        f_t = TexMobject("f(t)", "=", "2^t")
        P_t = TexMobject("P(t)", "=", "2^t")
        M_t = TexMobject("M(t)", "=", "2^t")
        functions = VGroup(f_x, f_t, P_t, M_t)
        for function in functions:
            function.scale(1.2)
            function.to_corner(UP+LEFT)
        for function in functions[1:]:
            for i, j in (0, 2), (2, 1):
                function[i][j].highlight(self.time_color)

        t_expression = TexMobject("t", "=", "\\text{Time (in days)}")
        t_expression.to_corner(UP+RIGHT)
        t_expression[0].highlight(self.time_color)

        pop_brace, mass_brace = [
            Brace(function[0], DOWN)
            for function in P_t, M_t
        ]
        for brace, word in (pop_brace, "size"), (mass_brace, "mass"):
            text = brace.get_text("Population %s"%word)
            text.to_edge(LEFT)
            brace.text = text

        self.play(Write(f_x))
        self.dither()
        self.play(
            Transform(f_x, f_t),
            FadeIn(
                t_expression,
                run_time = 2,
                submobject_mode = "lagged_start"
            )
        )
        self.play(Transform(f_x, P_t))
        self.play(
            GrowFromCenter(pop_brace),
            Write(pop_brace.text, run_time = 2)
        )
        self.dither(2)

        self.function = f_x
        self.pop_brace = pop_brace
        self.t_expression = t_expression
        self.mass_function = M_t
        self.mass_brace = mass_brace

    def introduce_pi_creatures(self):
        creatures = self.get_pi_creatures()
        total_num_days = self.get_num_days()
        num_start_days = 4

        self.reset()
        for x in range(num_start_days):
            self.let_one_day_pass()
        self.dither()
        self.play(
            Transform(self.function, self.mass_function),
            Transform(self.pop_brace, self.mass_brace),
            Transform(self.pop_brace.text, self.mass_brace.text),
        )
        self.dither()
        for x in range(total_num_days-num_start_days):
            self.let_one_day_pass()
            self.dither()
        self.joint_blink(shuffle = False)
        self.dither()

    def count_through_days(self):
        self.reset()
        brace = self.get_population_size_descriptor()
        days_to_let_pass = 3

        self.play(GrowFromCenter(brace))
        self.dither()
        for x in range(days_to_let_pass):
            self.let_one_day_pass()
            new_brace = self.get_population_size_descriptor()
            self.play(Transform(brace, new_brace))
            self.dither()

        self.population_size_descriptor = brace

    def ask_about_dM_dt(self):
        dM_dt_question = TexMobject("{dM", "\\over dt}", "=", "???")
        dM, dt, equals, q_marks = dM_dt_question
        dM_dt_question.next_to(self.function, DOWN, buff = LARGE_BUFF)
        dM_dt_question.to_edge(LEFT)

        self.play(
            FadeOut(self.pop_brace),
            FadeOut(self.pop_brace.text),
            Write(dM_dt_question)
        )
        self.dither(3)
        for mob in dM, dt:
            self.play(Indicate(mob))
            self.dither()

        self.dM_dt_question = dM_dt_question

    def growth_per_day(self):
        day_to_day, frac = self.get_from_day_to_day_label()

        self.play(
            FadeOut(self.dM_dt_question),
            FadeOut(self.population_size_descriptor),
            FadeIn(day_to_day)
        )
        rect = self.let_day_pass_and_highlight_new_creatures(frac)

        for x in range(2):
            new_day_to_day, new_frac = self.get_from_day_to_day_label()
            self.play(*map(FadeOut, [rect, frac]))
            frac = new_frac
            self.play(Transform(day_to_day, new_day_to_day))
            rect = self.let_day_pass_and_highlight_new_creatures(frac)
        self.play(*map(FadeOut, [rect, frac, day_to_day]))

    def let_day_pass_and_highlight_new_creatures(self, frac):
        num_new_creatures = 2**self.get_curr_day()

        self.let_one_day_pass()
        new_creatures = VGroup(
            *self.get_on_screen_pi_creatures()[-num_new_creatures:]
        )
        rect = Rectangle(
            color = GREEN,
            fill_color = BLUE,
            fill_opacity = 0.3,
        )
        rect.replace(new_creatures, stretch = True)
        rect.stretch_to_fit_height(rect.get_height()+MED_SMALL_BUFF)
        rect.stretch_to_fit_width(rect.get_width()+MED_SMALL_BUFF)
        self.play(DrawBorderThenFill(rect))
        self.play(Write(frac))
        self.dither()
        return rect

    def relate_growth_rate_to_pop_size(self):
        false_deriv = TexMobject(
            "{d(2^t) ", "\\over dt}", "= 2^t"
        )
        difference_eq = TexMobject(
            "{ {2^{t+1} - 2^t} \\over", "1}", "= 2^t"
        )
        real_deriv = TexMobject(
            "{ {2^{t+dt} - 2^t} \\over", "dt}", "= \\, ???"
        )
        VGroup(
            false_deriv[0][3], 
            false_deriv[2][-1],
            difference_eq[0][1],
            difference_eq[0][-2],
            difference_eq[2][-1],
            difference_eq[2][-1],
            real_deriv[0][1],
            real_deriv[0][-2],
        ).highlight(YELLOW)
        VGroup(
            difference_eq[0][3],
            difference_eq[1][-1],
            real_deriv[0][3],
            real_deriv[0][4],
            real_deriv[1][-2],
            real_deriv[1][-1],
        ).highlight(GREEN)

        expressions = [false_deriv, difference_eq, real_deriv]
        text_arg_list = [
            ("Tempting", "...",),
            ("Rate of change", "\\\\ over one full day"),
            ("Rate of change", "\\\\ in a small time"),
        ]
        for expression, text_args in zip(expressions, text_arg_list):
            expression.next_to(
                self.function, DOWN, 
                buff = LARGE_BUFF,
                aligned_edge = LEFT,
            )
            expression.brace = Brace(expression, DOWN)
            expression.brace_text = expression.brace.get_text(*text_args)

        time = self.t_expression[-1]
        new_time = TexMobject("3")
        new_time.move_to(time, LEFT)

        fading_creatures = VGroup(*self.get_on_screen_pi_creatures()[8:])


        self.play(*map(FadeIn, [
            false_deriv, false_deriv.brace, false_deriv.brace_text
        ]))
        self.dither()
        self.play(
            Transform(time, new_time),
            FadeOut(fading_creatures)
        )
        self.dither()
        for x in range(3):
            self.let_one_day_pass(run_time = 2)
            self.dither(2)

        for expression in difference_eq, real_deriv:
            expression.brace_text[1].highlight(GREEN)
            self.play(
                Transform(false_deriv, expression),
                Transform(false_deriv.brace, expression.brace),
                Transform(false_deriv.brace_text, expression.brace_text),
            )
            self.dither(3)
        self.reset()
        for x in range(self.get_num_days()):
            self.let_one_day_pass()
        self.dither()

        rect = Rectangle(color = YELLOW)
        rect.replace(real_deriv)
        rect.stretch_to_fit_width(rect.get_width()+MED_SMALL_BUFF)
        rect.stretch_to_fit_height(rect.get_height()+MED_SMALL_BUFF)
        self.play(*map(FadeOut, [
            false_deriv.brace, false_deriv.brace_text
        ]))
        self.play(ShowCreation(rect))
        self.play(*[
            ApplyFunction(
                lambda pi : pi.change_mode("pondering").look_at(real_deriv),
                pi,
                run_time = 2,
                rate_func = squish_rate_func(smooth, a, a+0.5)
            )
            for pi in self.get_pi_creatures()
            for a in [0.5*random.random()]
        ])
        self.dither(3)

    ###########

    def create_pi_creatures(self):
        width, height = self.pi_creature_grid_dimensions
        creature_array = VGroup(*[
            VGroup(*[
                PiCreature(mode = "plain")
                for y in range(height)
            ]).arrange_submobjects(UP, buff = MED_LARGE_BUFF)
            for x in range(width)
        ]).arrange_submobjects(RIGHT, buff = MED_LARGE_BUFF)
        creatures = VGroup(*it.chain(*creature_array))
        creatures.scale_to_fit_height(self.pi_creature_grid_height)
        creatures.to_corner(DOWN+RIGHT)

        colors = color_gradient([BLUE, GREEN, GREY_BROWN], len(creatures))
        random.shuffle(colors)
        for creature, color in zip(creatures, colors):
            creature.set_color(color)

        return creatures

    def reset(self):
        time = self.t_expression[-1]
        faders = [time] + list(self.get_on_screen_pi_creatures())
        new_time = TexMobject("0")
        new_time.next_to(self.t_expression[-2], RIGHT)
        first_creature = self.get_pi_creatures()[0]

        self.play(*map(FadeOut, faders))
        self.play(*map(FadeIn, [first_creature, new_time]))
        self.t_expression.submobjects[-1] = new_time

    def let_one_day_pass(self, run_time = 2):
        all_creatures = self.get_pi_creatures()
        on_screen_creatures = self.get_on_screen_pi_creatures()
        low_i = len(on_screen_creatures)
        high_i = min(2*low_i, len(all_creatures))
        new_creatures = VGroup(*all_creatures[low_i:high_i])

        to_children_anims = []
        growing_anims = []
        for old_pi, pi in zip(on_screen_creatures, new_creatures):
            pi.save_state()
            child = pi.copy()
            child.scale(0.25, about_point = child.get_bottom())
            child.eyes.scale(1.5, about_point = child.eyes.get_bottom())
            pi.move_to(old_pi)
            pi.set_fill(opacity = 0)

            index = list(new_creatures).index(pi)
            prop = float(index)/len(new_creatures)
            alpha  = np.clip(len(new_creatures)/8.0, 0, 0.5)
            rate_func = squish_rate_func(
                smooth, alpha*prop, alpha*prop+(1-alpha)
            )

            to_child_anim = Transform(pi, child, rate_func = rate_func)
            to_child_anim.update(1)
            growing_anim = ApplyMethod(pi.restore, rate_func = rate_func)
            to_child_anim.update(0)

            to_children_anims.append(to_child_anim)
            growing_anims.append(growing_anim)

        time = self.t_expression[-1]
        total_new_creatures = len(on_screen_creatures) + len(new_creatures)
        new_time = TexMobject(str(int(np.log2(total_new_creatures))))
        new_time.move_to(time, LEFT)

        growing_anims.append(Transform(time, new_time))

        self.play(*to_children_anims, run_time = run_time/2.0)
        self.play(*growing_anims, run_time = run_time/2.0)
        
    def get_num_pi_creatures_on_screen(self):
        mobjects = self.get_mobjects()
        return sum([
            pi in mobjects for pi in self.get_pi_creatures()
        ])

    def get_population_size_descriptor(self):
        on_screen_creatures = self.get_on_screen_pi_creatures()
        brace = Brace(on_screen_creatures, LEFT)
        n = len(on_screen_creatures)
        label = brace.get_text(
            "$2^%d$"%int(np.log2(n)),
            "$=%d$"%n,
        )
        brace.add(label)
        return brace

    def get_num_days(self):
        x, y = self.pi_creature_grid_dimensions
        return int(np.log2(x*y))

    def get_curr_day(self):
        return int(np.log2(len(self.get_on_screen_pi_creatures())))

    def get_from_day_to_day_label(self):
        curr_day = self.get_curr_day()
        top_words = TextMobject(
            "From day", str(curr_day), 
            "to", str(curr_day+1), ":"
        )
        top_words.scale_to_fit_width(4)
        top_words.next_to(
            self.function, DOWN,
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT,
        )
        top_words[1].highlight(GREEN)

        bottom_words = TexMobject(
            str(2**curr_day),
            "\\text{ creatures}", "\\over {1 \\text{ day}}"
        )
        bottom_words[0].highlight(GREEN)
        bottom_words.next_to(top_words, DOWN, buff = MED_LARGE_BUFF)

        return top_words, bottom_words

class GraphOfTwoToT(GraphScene):
    CONFIG = {
        "x_axis_label" : "$t$",
        "y_axis_label" : "$M$",
        "x_labeled_nums" : range(1, 7),
        "y_labeled_nums" : range(8, 40, 8),
        "x_max" : 6,
        "y_min" : 0,
        "y_max" : 32,
        "y_tick_frequency" : 2,
        "graph_origin" : 2.5*DOWN + 5*LEFT,
    }
    def construct(self):
        self.setup_axes()
        example_t = 3
        graph = self.get_graph(lambda t : 2**t, color = BLUE_C)
        self.graph = graph
        graph_label = self.get_graph_label(
            graph, "M(t) = 2^t",
            direction = LEFT,
        )
        label_group = self.get_label_group(example_t)
        v_line, brace, height_label, ss_group, slope_label = label_group
        self.animate_secant_slope_group_change(
            ss_group,
            target_dx = 1,
            run_time = 0
        )
        self.remove(ss_group)

        #Draw graph and revert to tangent
        self.play(ShowCreation(graph))
        self.play(Write(graph_label))
        self.dither()
        self.play(Write(ss_group))
        self.dither()
        for target_dx in 0.01, 1, 0.01:
            self.animate_secant_slope_group_change(
                ss_group,
                target_dx = target_dx
            )
            self.dither()

        #Mark up with values

        self.play(ShowCreation(v_line))
        self.play(
            GrowFromCenter(brace),
            Write(height_label, run_time = 1)
        )
        self.dither()
        self.play(
            FadeIn(
                slope_label, 
                run_time = 4,
                submobject_mode = "lagged_start"
            ),
            ReplacementTransform(
                height_label.copy(),
                slope_label.get_part_by_tex("2^")
            )
        )
        self.dither()

        #Vary value
        threes = VGroup(height_label[1], slope_label[2][1])
        ts = VGroup(*[
            TexMobject("t").highlight(YELLOW).scale(0.75).move_to(three)
            for three in threes
        ])
        self.play(Transform(threes, ts))

        alt_example_t = example_t+1
        def update_label_group(group, alpha):
            t = interpolate(example_t, alt_example_t, alpha)
            new_group = self.get_label_group(t)
            Transform(group, new_group).update(1)
            for t, three in zip(ts, threes):
                t.move_to(three)
            Transform(threes, ts).update(1)
            return group

        self.play(UpdateFromAlphaFunc(
            label_group, update_label_group,
            run_time = 3,
        ))
        self.play(UpdateFromAlphaFunc(
            label_group, update_label_group,
            run_time = 3,
            rate_func = lambda t : 1 - 1.5*smooth(t)
        ))

    def get_label_group(self, t):
        graph = self.graph

        v_line = self.get_vertical_line_to_graph(
            t, graph,
            color = YELLOW,
        )
        brace = Brace(v_line, RIGHT)
        height_label = brace.get_text("$2^%d$"%t)

        ss_group = self.get_secant_slope_group(
            t, graph, dx = 0.01,
            df_label = "dM",
            dx_label = "dt",
            dx_line_color = GREEN,
            secant_line_color = RED,
        )
        slope_label = TexMobject(
            "\\text{Slope}", "=", 
            "2^%d"%t,
            "(%.7f\\dots)"%np.log(2)
        )
        slope_label.next_to(
            ss_group.secant_line.point_from_proportion(0.65),
            DOWN+RIGHT,
            buff = 0
        )
        slope_label.highlight_by_tex("Slope", RED)
        return VGroup(
            v_line, brace, height_label,
            ss_group, slope_label
        )

class SimpleGraphOfTwoToT(GraphOfTwoToT):
    CONFIG = {
        "x_axis_label" : "",
        "y_axis_label" : "",
    }
    def construct(self):
        self.setup_axes()
        func = lambda t : 2**t
        graph = self.get_graph(func)
        line_pairs = VGroup()
        for x in 1, 2, 3, 4, 5:
            point = self.coords_to_point(x, func(x))
            x_axis_point = self.coords_to_point(x, 0)
            y_axis_point = self.coords_to_point(0, func(x))
            line_pairs.add(VGroup(
                DashedLine(x_axis_point, point),
                DashedLine(y_axis_point, point),
            ))


        self.play(ShowCreation(graph, run_time = 2))
        for pair in line_pairs:
            self.play(ShowCreation(pair))
        self.dither()

class AnalyzeExponentRatio(PiCreatureScene):
    CONFIG = {
        "base" : 2,
        "base_str" : "2",
    }
    def construct(self):
        base_str = self.base_str

        func_def = TexMobject("M(", "t", ")", "= ", "%s^"%base_str, "t")
        func_def.to_corner(UP+LEFT)
        self.add(func_def)

        ratio = TexMobject(
            "{ {%s^"%base_str, "{t", "+", "dt}", "-", 
            "%s^"%base_str, "t}",
            "\\over \\,", "dt}"
        )
        ratio.shift(UP+LEFT)

        lhs = TexMobject("{dM", "\\over \\,", "dt}", "(", "t", ")", "=")
        lhs.next_to(ratio, LEFT)


        two_to_t_plus_dt = VGroup(*ratio[:4])
        two_to_t = VGroup(*ratio[5:7])
        two_to_t_two_to_dt = TexMobject(
            "%s^"%base_str, "t", 
            "%s^"%base_str, "{dt}"
        )
        two_to_t_two_to_dt.move_to(two_to_t_plus_dt, DOWN+LEFT)
        exp_prop_brace = Brace(two_to_t_two_to_dt, UP)

        one = TexMobject("1")
        one.move_to(ratio[5], DOWN)
        lp, rp = parens = TexMobject("()")
        parens.stretch(1.3, 1)
        parens.scale_to_fit_height(ratio.get_height())
        lp.next_to(ratio, LEFT, buff = 0)
        rp.next_to(ratio, RIGHT, buff = 0)

        extracted_two_to_t = TexMobject("%s^"%base_str, "t")
        extracted_two_to_t.next_to(lp, LEFT, buff = SMALL_BUFF)

        expressions = [
            ratio, two_to_t_two_to_dt, 
            extracted_two_to_t, lhs, func_def
        ]
        for expression in expressions:
            expression.highlight_by_tex("t", YELLOW)
            expression.highlight_by_tex("dt", GREEN)

        #Apply exponential property
        self.play(
            Write(ratio), Write(lhs),
            self.pi_creature.change_mode, "raise_right_hand"
        )
        self.dither(2)
        self.play(
            two_to_t_plus_dt.next_to, exp_prop_brace, UP,
            self.pi_creature.change_mode, "pondering"
        )
        self.play(
            ReplacementTransform(
                two_to_t_plus_dt.copy(), two_to_t_two_to_dt,
                run_time = 2,
                path_arc = np.pi,
            ),
            FadeIn(exp_prop_brace)
        )
        self.dither(2)

        #Talk about exponential property
        add_exp_rect, mult_rect = rects = [
            Rectangle(
                stroke_color = BLUE,
                stroke_width = 2,
            ).replace(mob).scale_in_place(1.1)
            for mob in [
                VGroup(*two_to_t_plus_dt[1:]),
                two_to_t_two_to_dt
            ]
        ]
        words = VGroup(*[
            TextMobject(s, " ideas")
            for s in "Additive", "Multiplicative"
        ])
        words[0].move_to(words[1], LEFT)
        words.highlight(BLUE)
        words.next_to(two_to_t_plus_dt, RIGHT, buff = 1.5*LARGE_BUFF)
        arrows = VGroup(*[
            Arrow(word.get_left(), rect, color = words.get_color())
            for word, rect in zip(words, rects)
        ])

        self.play(ShowCreation(add_exp_rect))
        self.dither()
        self.play(ReplacementTransform(
            add_exp_rect.copy(), mult_rect
        ))
        self.dither()
        self.change_mode("happy")
        self.play(Write(words[0], run_time = 2))
        self.play(ShowCreation(arrows[0]))
        self.dither()
        self.play(
            Transform(*words),
            Transform(*arrows),
        )
        self.dither(2)
        self.play(*map(FadeOut, [
            words[0], arrows[0], add_exp_rect, mult_rect,
            two_to_t_plus_dt, exp_prop_brace,
        ]))

        #Factor out 2^t
        self.play(*[
            FadeIn(
                mob,
                run_time = 2,
                rate_func = squish_rate_func(smooth, 0.5, 1)
            )
            for mob in one, lp, rp
        ] + [
            ReplacementTransform(
                mob, extracted_two_to_t,
                path_arc = np.pi/2,
                run_time = 2,
            )
            for mob in two_to_t, VGroup(*two_to_t_two_to_dt[:2])
        ] + [
            lhs.next_to, extracted_two_to_t, LEFT
        ])
        self.change_mode("pondering")
        shifter = VGroup(ratio[4], one, *two_to_t_two_to_dt[2:])
        stretcher = VGroup(lp, ratio[7], rp)
        self.play(
            shifter.next_to, ratio[7], UP,
            stretcher.stretch_in_place, 0.9, 0
        )
        self.dither(2)

        #Ask about dt -> 0
        brace = Brace(VGroup(extracted_two_to_t, ratio), DOWN)
        alt_brace = Brace(parens, DOWN)
        dt_to_zero = TexMobject("dt", "\\to 0")
        dt_to_zero.highlight_by_tex("dt", GREEN)
        dt_to_zero.next_to(brace, DOWN)

        self.play(GrowFromCenter(brace))
        self.play(Write(dt_to_zero))
        self.dither(2)

        #Who cares
        randy = Randolph()
        randy.scale(0.7)
        randy.to_edge(DOWN)

        self.play(
            FadeIn(randy),
            self.pi_creature.change_mode, "plain",
        )
        self.play(PiCreatureSays(
            randy, "Who cares?", 
            bubble_kwargs = {"direction" : LEFT},
            target_mode = "angry",
        ))
        self.dither(2)
        self.play(
            RemovePiCreatureBubble(randy),
            FadeOut(randy),
            self.pi_creature.change_mode, "hooray",
            self.pi_creature.look_at, parens
        )
        self.play(
            Transform(brace, alt_brace),
            dt_to_zero.next_to, alt_brace, DOWN
        )
        self.dither()

        #Highlight separation
        rects = [
            Rectangle(
                stroke_color = color,
                stroke_width = 2,
            ).replace(mob, stretch = True).scale_in_place(1.1)
            for mob, color in [
                (VGroup(parens, dt_to_zero), GREEN), 
                (extracted_two_to_t, YELLOW),
            ]
        ]
        self.play(ShowCreation(rects[0]))
        self.dither(2)
        self.play(ReplacementTransform(rects[0].copy(), rects[1]))
        self.change_mode("happy")
        self.dither()
        self.play(*map(FadeOut, rects))

        #Plug in specific values
        static_constant = self.try_specific_dt_values()
        constant = static_constant.copy()

        #Replace with actual constant
        limit_term = VGroup(
            brace, dt_to_zero, ratio[4], one, rects[0],
            *ratio[7:]+two_to_t_two_to_dt[2:]
        )
        self.play(FadeIn(rects[0]))
        self.play(limit_term.to_corner, DOWN+LEFT)
        self.play(
            lp.stretch, 0.5, 1,
            lp.stretch, 0.8, 0,
            lp.next_to, extracted_two_to_t[0], RIGHT,
            rp.stretch, 0.5, 1,
            rp.stretch, 0.8, 0,
            rp.next_to, lp, RIGHT, SMALL_BUFF,
            rp.shift, constant.get_width()*RIGHT,
            constant.next_to, extracted_two_to_t[0], RIGHT, MED_LARGE_BUFF
        )
        self.dither()
        self.change_mode("confused")
        self.dither()

        #Indicate distinction between dt group and t group again
        for mob in limit_term, extracted_two_to_t:
            self.play(FocusOn(mob))
            self.play(Indicate(mob))
        self.dither()

        #hold_final_value
        derivative = VGroup(
            lhs, extracted_two_to_t, parens, constant
        )
        func_def_rhs = VGroup(*func_def[-2:]).copy()
        func_lp, func_rp = func_parens = TexMobject("()")
        func_parens.set_fill(opacity = 0)
        func_lp.next_to(func_def_rhs[0], LEFT, buff = 0)
        func_rp.next_to(func_lp, RIGHT, buff = func_def_rhs.get_width())
        func_def_rhs.add(func_parens)
        M = lhs[0][1]

        self.play(
            FadeOut(M),
            func_def_rhs.move_to, M, LEFT,
            func_def_rhs.set_fill, None, 1,
        )
        lhs[0].submobjects[1] = func_def_rhs
        self.dither()
        self.play(
            derivative.next_to, self.pi_creature, UP,
            derivative.to_edge, RIGHT,
            self.pi_creature.change_mode, "raise_right_hand"
        )
        self.dither(2)
        for mob in extracted_two_to_t, constant:
            self.play(Indicate(mob))
            self.dither()
        self.dither(2)

    def try_specific_dt_values(self):
        expressions = []
        for num_zeros in [1, 2, 4, 7]:
            dt_str = "0." + num_zeros*"0" + "1"
            dt_num = float(dt_str)
            output_num = (self.base**dt_num - 1) / dt_num
            output_str = "%.7f\\dots"%output_num

            expression = TexMobject(
                "{%s^"%self.base_str, "{%s}"%dt_str, "-1", 
                "\\over \\,", "%s}"%dt_str, 
                "=", output_str
            )
            expression.highlight_by_tex(dt_str, GREEN)
            expression.highlight_by_tex(output_str, BLUE)
            expression.to_corner(UP+RIGHT)
            expressions.append(expression)

        curr_expression = expressions[0]
        self.play(
            Write(curr_expression),
            self.pi_creature.change_mode, "pondering"
        )
        self.dither(2)
        for expression in expressions[1:]:
            self.play(Transform(curr_expression, expression))
            self.dither(2)
        return curr_expression[-1]

class ExponentRatioWithThree(AnalyzeExponentRatio):
    CONFIG = {
        "base" : 3,
        "base_str" : "3",
    }

class ExponentRatioWithSeven(AnalyzeExponentRatio):
    CONFIG = {
        "base" : 7,
        "base_str" : "7",
    }

class ExponentRatioWithE(AnalyzeExponentRatio):
    CONFIG = {
        "base" : np.exp(1),
        "base_str" : "e",
    }

class AskAboutConstantOne(TeacherStudentsScene):
    def construct(self):
        note = TexMobject(
            "{ d(a^", "t", ")", "\\over \\,", "dt}", 
            "=", "a^", "t", "(\\text{Some constant})"
        )
        note.highlight_by_tex("t", YELLOW)
        note.highlight_by_tex("dt", GREEN)
        note.highlight_by_tex("constant", BLUE)
        note.to_corner(UP+LEFT)
        self.add(note)

        self.student_says(
            "Is there a base where\\\\",
            "that constant is 1?"
        )
        self.change_student_modes(
            "pondering", "raise_right_hand", "thinking",
            # look_at_arg = self.get_students()[1].bubble
        )
        self.dither(2)
        self.play(FadeOut(note[-1], run_time = 3))
        self.dither()

        self.teacher_says(
            "There is!\\\\",
            "$e = 2.71828\\dots$",
            target_mode = "hooray"
        )
        self.change_student_modes(*["confused"]*3)
        self.dither(3)

class NaturalLog(Scene):
    def construct(self):
        expressions = VGroup(*map(self.get_expression, [2, 3, 7]))
        expressions.arrange_submobjects(DOWN, buff = MED_SMALL_BUFF)
        expressions.to_edge(LEFT)

        self.play(FadeIn(
            expressions, 
            run_time = 3, 
            submobject_mode = "lagged_start"
        ))
        self.dither()
        self.play(
            expressions.set_fill, None, 1,
            run_time = 2,
            submobject_mode = "lagged_start"
        )
        self.dither()
        for i in 0, 2, 1:
            self.show_natural_loggedness(expressions[i])

    def show_natural_loggedness(self, expression):
        base, constant = expression[1], expression[-3]

        log_constant, exp_constant = constant.copy(), constant.copy()
        log_base, exp_base = base.copy(), base.copy()
        log_equals, exp_equals = map(TexMobject, "==")

        ln = TexMobject("\\ln(2)")
        log_base.move_to(ln[-2])        
        ln.remove(ln[-2])
        log_equals.next_to(ln, LEFT)
        log_constant.next_to(log_equals, LEFT)
        log_expression = VGroup(
            ln, log_constant, log_equals, log_base
        )

        e = TexMobject("e")
        exp_constant.scale(0.7)
        exp_constant.next_to(e, UP+RIGHT, buff = 0)
        exp_base.next_to(exp_equals, RIGHT)
        VGroup(exp_base, exp_equals).next_to(
            VGroup(e, exp_constant), RIGHT, 
            aligned_edge = DOWN
        )
        exp_expression = VGroup(
            e, exp_constant, exp_equals, exp_base
        )

        for group, vect in (log_expression, UP), (exp_expression, DOWN):
            group.to_edge(RIGHT)
            group.shift(vect)

        self.play(
            ReplacementTransform(base.copy(), log_base),
            ReplacementTransform(constant.copy(), log_constant),
            run_time = 2
        )
        self.play(Write(ln), Write(log_equals))
        self.dither()
        self.play(
            ReplacementTransform(
                log_expression.copy(),
                exp_expression,
                run_time = 2,
            )
        )
        self.dither(2)

        ln_a = expression[-1]
        self.play(
            FadeOut(expression[-2]),
            FadeOut(constant),
            ln_a.move_to, constant, LEFT,
            ln_a.highlight, BLUE
        )
        self.dither()
        self.play(*map(FadeOut, [log_expression, exp_expression]))
        self.dither()

    def get_expression(self, base):
        expression = TexMobject(
            "{d(", "%d^"%base, "t", ")", "\\over \\,", "dt}",
            "=", "%d^"%base, "t", "(%.4f\\dots)"%np.log(base),
        )
        expression.highlight_by_tex("t", YELLOW)
        expression.highlight_by_tex("dt", GREEN)
        expression.highlight_by_tex("\\dots", BLUE)

        brace = Brace(expression.get_part_by_tex("\\dots"), UP)
        brace_text = brace.get_text("$\\ln(%d)$"%base)
        for mob in brace, brace_text:
            mob.set_fill(opacity = 0)

        expression.add(brace, brace_text)
        return expression

class NextVideo(TeacherStudentsScene):
    def construct(self):
        series = VideoSeries()
        series.to_edge(UP)
        this_video = series[3]
        next_video = series[4]
        brace = Brace(this_video, DOWN)
        this_video.save_state()
        this_video.highlight(YELLOW)

        this_tex = TexMobject(
            "{d(", "a^t", ") \\over dt} = ", "a^t", "\\ln(a)"
        )
        this_tex[1][1].highlight(YELLOW)
        this_tex[3][1].highlight(YELLOW)
        this_tex.next_to(brace, DOWN)

        next_tex = VGroup(*map(TextMobject, [
            "Chain rule", "Product rule", "$\\vdots$"
        ]))
        next_tex.arrange_submobjects(DOWN)
        next_tex.next_to(brace, DOWN)
        next_tex.shift(
            next_video.get_center()[0]*RIGHT\
            -next_tex.get_center()[0]*RIGHT
        )

        self.add(series, brace, *this_tex[:3])
        self.change_student_modes(
            "confused", "pondering", "erm",
            look_at_arg = this_tex
        )
        self.play(ReplacementTransform(
            this_tex[1].copy(), this_tex[3]
        ))
        self.dither()
        self.play(
            Write(this_tex[4]),
            ReplacementTransform(
                this_tex[3][0].copy(),
                this_tex[4][3],
                path_arc = np.pi,
                remover = True
            )
        )
        self.dither(2)
        self.play(this_tex.replace, this_video)
        self.play(
            brace.next_to, next_video, DOWN,
            this_video.restore,
            Animation(this_tex),
            next_video.highlight, YELLOW,
            Write(next_tex),
            self.get_teacher().change_mode, "raise_right_hand"
        )
        self.change_student_modes(
            *["pondering"]*3,
            look_at_arg = next_tex
        )
        self.dither(3)

class ExpPatreonThanks(PatreonThanks):
    CONFIG = {
        "specific_patrons" : [
            "Ali  Yahya",
            "Meshal  Alshammari",
            "CrypticSwarm    ",
            "Kathryn Schmiedicke",
            "Nathan Pellegrin",
            "Karan Bhargava", 
            "Justin Helps",
            "Ankit   Agarwal",
            "Yu  Jun",
            "Dave    Nicponski",
            "Damion  Kistler",
            "Juan    Benet",
            "Othman  Alikhan",
            "Justin Helps",
            "Markus  Persson",
            "Dan Buchoff",
            "Derek   Dai",
            "Joseph  John Cox",
            "Luc Ritchie",
            "Mustafa Mahdi",
            "Daan Smedinga",
            "Jonathan Eppele",
            "Albert Nguyen",
            "Nils Schneider",
            "Mustafa Mahdi",
            "Mathew Bramson",
            "Guido   Gambardella",
            "Jerry   Ling",
            "Mark    Govea",
            "Vecht",
            "Shimin Kuang",
            "Rish    Kundalia",
            "Achille Brighton",
            "Kirk    Werklund",
            "Ripta   Pasay",
            "Felipe  Diniz",
        ]
    }

class Thumbnail(Scene):
    def construct(self):
        derivative = TexMobject(
            "\\frac{d(a^t)}{dt} =", "a^t \\ln(a)"
        )
        derivative[0][3].highlight(YELLOW)
        derivative[1][1].highlight(YELLOW)
        derivative[0][2].highlight(BLUE)
        derivative[1][0].highlight(BLUE)
        derivative[1][5].highlight(BLUE)
        derivative.scale(3)
        # derivative.to_edge(UP)
        derivative.shift(DOWN)

        brace = Brace(Line(LEFT, RIGHT), UP)
        brace.scale_to_fit_width(derivative[1].get_width())
        brace.next_to(derivative[1], UP)
        question = TextMobject("Why?")
        question.scale(2.5)
        question.next_to(brace, UP)

        # randy = Randolph()
        # randy.scale(1.3)
        # randy.next_to(ORIGIN, LEFT).to_edge(DOWN)
        # randy.change_mode("pondering")

        # question = TextMobject("What is $e\\,$?")
        # e = question[-2]
        # e.scale(1.2, about_point = e.get_bottom())
        # e.highlight(BLUE)
        # question.scale(1.7)
        # question.next_to(randy, RIGHT, aligned_edge = UP)
        # question.shift(DOWN)
        # randy.look_at(question)

        self.add(derivative, brace, question)




























