from manim import *
from math import sin , cos , asin , sqrt
from utilities import myScale

from icons import machineIcon , screenRectanlge

INPUT_COLOR = WHITE
OUTPUT_COLOR = RED
PROCESS_COLOR = BLUE
INTERSECTION_COLOR = YELLOW

def areaFunction(r):
    return PI * r * r

def LineFromAngleAndPoint(angle , point , length=1.0 , **kwargs):
    dy = (length/2) * sin(angle)
    dx = (length/2) * cos(angle)
    start = [point[0] - dx , point[1] - dy , 0]
    end = [point[0] + dx , point[1] + dy , 0]

    return Line(start , end , **kwargs)

def inverseSineGeneral(x , n_values):
    answers = []
    mainAnswer = asin(x)
    for n_value in n_values:
        answers.append( (n_value * PI) + ( ((-1)**(n_value)) * mainAnswer ) )
    
    return answers

def Checkmark(color=GREEN):
    # the checkmark is a VGroup of 2 lines
    angle_from_the_vertical = 35 * DEGREES
    line1 = Line([-0.5 * sin(angle_from_the_vertical) , 0.5 * cos(angle_from_the_vertical) , 0] , [0 , 0 , 0] , color=color , stroke_width=5)
    line2 = Line([0 , 0 , 0] , [1 * sin(angle_from_the_vertical) , 1 * cos(angle_from_the_vertical) , 0] , color=color , stroke_width=5)

    #make the lines rounded
    line1.set_cap_style(CapStyleType.ROUND)
    line2.set_cap_style(CapStyleType.ROUND)

    return VGroup(line1 , line2)


class Scene1(MovingCameraScene):
    def construct(self):
        radius = ValueTracker(1)
        initialCircle = always_redraw(lambda : Circle(radius=radius.get_value() , color=PROCESS_COLOR).shift(UP))
        radius_brace = always_redraw(lambda : BraceBetweenPoints([0,1,0] , [radius.get_value(),1,0] , DOWN , buff = 0 , sharpness = 2))
        radius_brace_text = always_redraw(lambda : MathTex(r"r").scale(0.7).next_to(radius_brace , DOWN , buff=0.1))
        area_equation = MathTex(r"A = \pi " , r"r" , r"^2" , color=OUTPUT_COLOR).scale(0.8).shift(DOWN*0.5)
        area_equation[1].set_color(INPUT_COLOR)

        area_equation_new = MathTex(r"A" , r"(" , r"r" , r") = \pi " , r"r" , r"^2" , color=OUTPUT_COLOR).scale(0.8).shift(DOWN*0.5)
        area_equation_new[2].set_color(INPUT_COLOR)
        area_equation_new[4].set_color(INPUT_COLOR)


        radius_value_equation = always_redraw(lambda : MathTex(r"\text{Radius: }" , f"{radius.get_value():.1f}" , color=INPUT_COLOR).scale(0.65).shift(UP*0+ RIGHT*5))
        area_value_equation = always_redraw(lambda : MathTex(r"\text{Area: }" , f"{(radius.get_value() * radius.get_value()):.2f}" , color=OUTPUT_COLOR).scale(0.65).shift(DOWN * 1 + RIGHT*5))


        self.play(Create(initialCircle))
        self.play(FadeIn(radius_brace), Write(radius_brace_text))
        self.play(Write(area_equation))
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.move_to([3 , 0 , 0]))

        self.play(Write(radius_value_equation), Write(area_value_equation))
        self.wait()
        self.play(radius.animate.set_value(5))
        self.wait(0.5)
        self.play(radius.animate.set_value(-10), run_time=2)
        self.wait(0.5)
        self.play(Indicate(area_equation))
        self.wait(0.5)
        self.play(radius.animate.set_value(10), run_time=1)
        self.wait(0.5)
        self.play(TransformMatchingShapes(area_equation, area_equation_new))
        self.wait()
        self.play(Indicate(area_equation_new[2]), Indicate(area_equation_new[4]))
        self.play(Indicate(area_equation_new[0]))

        self.play(*[FadeOut(mob) for mob in self.mobjects])

class Scene2(Scene):
    def construct(self):
        machine = machineIcon("f", PROCESS_COLOR, WHITE)

        inputArrow = Arrow([-2.5, 0, 0], [-1, 0, 0], color=INPUT_COLOR, max_tip_length_to_length_ratio=0.2, max_stroke_width_to_length_ratio=2.5)
        inputText = MathTex(r"\text{Input}(x)", color=INPUT_COLOR).scale(0.5).next_to(inputArrow, DOWN, buff=0.1).shift(LEFT * 0.3)

        outputArrow = Arrow([1, 0, 0], [2.5, 0, 0], color=OUTPUT_COLOR, max_tip_length_to_length_ratio=0.2, max_stroke_width_to_length_ratio=2.5)
        outputText = MathTex(r"\text{Output}(f(x))", color=OUTPUT_COLOR).scale(0.5).next_to(outputArrow, DOWN, buff=0.1).shift(RIGHT * 0.6)

        self.play(DrawBorderThenFill(machine))
        self.play(GrowArrow(inputArrow), FadeIn(inputText, shift=RIGHT))
        self.play(GrowArrow(outputArrow), FadeIn(outputText, shift=RIGHT))

        self.wait()
        self.play(*[FadeOut(mob) for mob in self.mobjects])

class Scene3(Scene):
    def construct(self):
        graph_text = Text("Graphs", color=PROCESS_COLOR).scale(0.75)
        area_equation = MathTex(r"A", r"(", r"r", r") = \pi ", r"r", r"^2", color=OUTPUT_COLOR).scale(0.8)
        area_equation[2].set_color(INPUT_COLOR)
        area_equation[4].set_color(INPUT_COLOR)

        ax = Axes(
            x_range=[-7, 7, 1],
            y_range=[-2, 5, 1],
            x_length=14,
            y_length=7,
            axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
            }
        )
        labels = ax.get_axis_labels(
            Tex("radius", stroke_color=INPUT_COLOR, color=INPUT_COLOR).scale(0.5), Text("area", stroke_color=OUTPUT_COLOR, color=OUTPUT_COLOR).scale(0.4)
        )
        curve = ax.plot(areaFunction, [-1.262, 1.262], color=OUTPUT_COLOR, stroke_width=2)

        r_value = ValueTracker(-1)
        point_on_curve = always_redraw(lambda: Dot(ax.coords_to_point(r_value.get_value(), areaFunction(r_value.get_value())), color=INTERSECTION_COLOR, radius=0.05))

        r_brace = always_redraw(lambda: BraceBetweenPoints(ax.c2p(0, 0), ax.c2p(r_value.get_value(), 0), DOWN, color=PROCESS_COLOR))
        r_brace_value = always_redraw(lambda: MathTex(r"r = ", f"{r_value.get_value():.1f}", color=PROCESS_COLOR).scale(0.5).next_to(r_brace, DOWN, buff=0.1))

        height_line = always_redraw(lambda: Line(ax.c2p(r_value.get_value(), 0), ax.c2p(r_value.get_value(), areaFunction(r_value.get_value())), stroke_width=2, color=PROCESS_COLOR))
        height_label = always_redraw(lambda:
            MathTex(r"A(", r"r", r")", color=OUTPUT_COLOR).scale(0.5 if abs(r_value.get_value()) > 0.5 else abs(r_value.get_value())).rotate(PI / 2 if r_value.get_value() < 0 else -PI / 2).next_to(height_line, LEFT if r_value.get_value() < 0 else RIGHT, buff=0.1)
        )

        next_axes = Axes(
            x_range=[-7, 7, 1],
            y_range=[-3.5, 3.5, 1],
            x_length=14,
            y_length=7,
            axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
            }
        )
        next_labels = next_axes.get_axis_labels(
            Tex("x-axis", stroke_color=INPUT_COLOR, color=INPUT_COLOR).scale(0.5), Text("y-axis", stroke_color=OUTPUT_COLOR, color=OUTPUT_COLOR).scale(0.4)
        )

        self.play(Write(graph_text))
        self.play(graph_text.animate.to_corner(UL), Write(area_equation))
        self.play(Create(ax.x_axis), area_equation.animate.scale(0.8).next_to(graph_text, DOWN))
        self.play(Write(labels[0]))

        self.play(Create(ax.y_axis))
        self.play(Write(labels[1]))

        self.play(Create(curve), rate_func=linear, run_time=1)


        # Lots of changes here ////
        initial_x = 0.5
        x_tracker = ValueTracker(initial_x)
        
        dot_at_x_axis = always_redraw(lambda : Dot(ax.c2p(x_tracker.get_value() , 0) , color=INTERSECTION_COLOR , radius = 0.05))
        plotting_dot = always_redraw(lambda : Dot(ax.c2p(x_tracker.get_value() , (PI * x_tracker.get_value() * x_tracker.get_value())) , color=OUTPUT_COLOR , radius = 0.05))
        x_text = always_redraw(lambda : MathTex(f"{x_tracker.get_value():.1f}").scale(0.5).next_to(dot_at_x_axis , DOWN , buff=0.1))

        def helper3():
            a = MathTex(r"\left( " , f"{x_tracker.get_value():.1f}" , f" , {(PI * x_tracker.get_value() * x_tracker.get_value()):.2f}" , r"\right)" , color = OUTPUT_COLOR).scale(0.6).next_to(plotting_dot , RIGHT)
            a[1].set_color(INPUT_COLOR)
            return a

        coordinate_label = always_redraw(helper3)

        def helper2():
            a = MathTex(r"A", r"(", f"{x_tracker.get_value():.1f}", r") = ", f"{(PI * x_tracker.get_value() * x_tracker.get_value()):.2f}", color=OUTPUT_COLOR).scale(0.8 * 0.6).next_to(area_equation , DOWN).align_to(area_equation , LEFT)
            a[2].set_color(WHITE)
            return a

        test_points_text = always_redraw(helper2)
        
        def helper():
            if x_tracker.get_value() > initial_x:
                a = ax.plot(areaFunction , [initial_x , x_tracker.get_value()] , color=OUTPUT_COLOR , stroke_width = 2)
            else:
                a = ax.plot(areaFunction , [x_tracker.get_value() , initial_x] , color=OUTPUT_COLOR , stroke_width = 2)
            return a


        right_part_of_the_curve = always_redraw(helper)
        right_part_of_the_curve_permanent = ax.plot(areaFunction , [initial_x , 1.262] , color=OUTPUT_COLOR , stroke_width = 2)

        # left_part_of_the_curve = always_redraw( lambda : ax.plot(areaFunction , [x_tracker.get_value() , initial_x] , color=OUTPUT_COLOR , stroke_width = 2) )
        # left_part_of_the_curve_permanent = ax.plot(areaFunction , [-1.262 , initial_x] , color=OUTPUT_COLOR , stroke_width = 2)




        self.play(Uncreate(curve))
        self.remove(curve)

        curve = ax.plot(areaFunction, [-1.262, 1.262], color=OUTPUT_COLOR, stroke_width=2)

        self.play(FadeIn(dot_at_x_axis) , FocusOn(dot_at_x_axis , run_time=1))
        self.play(Write(x_text))
        self.play(Indicate(VGroup(area_equation[:3] , area_equation[3][0])))
        self.play(Write(test_points_text))
        self.play(FadeIn(plotting_dot))
        self.play(Write(coordinate_label))
        
        self.add(right_part_of_the_curve)

        self.play(x_tracker.animate.set_value(1.262) , run_time = 2.5)
        self.add(right_part_of_the_curve_permanent)
        self.play(x_tracker.animate.set_value(-1.262) , run_time = 3.5)
        self.play(FadeIn(curve) , run_time = 0.1)
        # self.play(curve.animate.move_to(ORIGIN))
        self.play(FadeOut(plotting_dot , dot_at_x_axis , x_text , coordinate_label , test_points_text , right_part_of_the_curve_permanent , right_part_of_the_curve))

        

        # Lots of changes here ////

        self.play(FadeIn(point_on_curve))
        self.play(FadeIn(r_brace, r_brace_value))
        self.play(Create(height_line))
        self.play(Write(height_label))
        self.play(r_value.animate.set_value(-1.25))
        self.play(r_value.animate.set_value(1.25), run_time=1.5)

        self.wait()

        self.play(FadeOut(area_equation, curve, point_on_curve, height_line, r_brace, r_brace_value, height_label), Transform(ax, next_axes), Transform(labels, next_labels))
        self.wait(0.5)

class Scene4(Scene):
    def construct(self):
        # these are very finely tuned functions to make the parametric curve
        def x(t):
            if(t < - (PI/3)):
                return (3 * t) + PI
            elif(t > (PI/3)):
                return (3 * t) - PI
            else:
                return -sin(3 * t)

        def y(t):
            return (cos((0.5 * t) + 4)) + ((1 / 2) * (cos(3 * t))) + ((1 / 3) * (cos((6 * t) - 6.5)))

        def parametricFunction(t):
            return (x(t) - 1.5, y(0.5 * t) + 1)

        graph_text = Text("Graphs", color=PROCESS_COLOR).scale(0.75).to_corner(UL)

        ax = Axes(
            x_range=[-7, 7, 1],
            y_range=[-3.5, 3.5, 1],
            x_length=14,
            y_length=7,
            axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
            }
        )

        labels = ax.get_axis_labels(
            Tex("x-axis", stroke_color=INPUT_COLOR, color=INPUT_COLOR).scale(0.5), Text("y-axis", stroke_color=OUTPUT_COLOR, color=OUTPUT_COLOR).scale(0.4)
        )

        curve = ax.plot_parametric_curve(parametricFunction, t_range=(-2.9, 3.9), stroke_width=2, color=OUTPUT_COLOR)
        screen_rectangle = screenRectanlge(0.8)
        no_inputs_text = Tex("No input can have more than one output", color=YELLOW)

        point_at_4 = Dot(ax.c2p(4, 0), color=INTERSECTION_COLOR, radius=0.05)

        point_at_the_left = Dot(ax.c2p(-1.5, 0), color=INTERSECTION_COLOR, radius=0.05)
        point_at_the_left_copy_1 = Dot(ax.c2p(-1.5, 0), color=INTERSECTION_COLOR, radius=0.05)
        point_at_the_left_copy_2 = Dot(ax.c2p(-1.5, 0), color=INTERSECTION_COLOR, radius=0.05)
        output_points = VGroup(
            Dot(ax.c2p(-1.5, 1.17188), color=INTERSECTION_COLOR, radius=0.05),
            Dot(ax.c2p(-1.5, 0.23897), color=INTERSECTION_COLOR, radius=0.05),
            Dot(ax.c2p(-1.5, -0.152775), color=INTERSECTION_COLOR, radius=0.05)
        )

        parabola_axes = Axes(
            x_range=[-7, 7, 1],
            y_range=[-2, 5, 1],
            x_length=14,
            y_length=7,
            axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
            }
        )

        parabola_lables = parabola_axes.get_axis_labels(
            Tex("radius", stroke_color=INPUT_COLOR, color=INPUT_COLOR).scale(0.5), Text("area", stroke_color=OUTPUT_COLOR, color=OUTPUT_COLOR).scale(0.4)
        )

        parabola_curve = parabola_axes.plot(areaFunction, [-1.5, 1.5], color=OUTPUT_COLOR, stroke_width=2)

        self.add(graph_text, ax, labels)

        self.play(Create(curve), rate_func=linear, run_time=4)
        self.play(FadeIn(screen_rectangle, run_time=0.5), Write(no_inputs_text))
        self.play(no_inputs_text.animate.scale(0.5).to_corner(UR), FadeOut(screen_rectangle, run_time=0.5))
        self.play(FocusOn(point_at_4, run_time=1), FadeIn(point_at_4, run_time=1))
        self.play(point_at_4.animate.move_to(ax.c2p(4, 0.6368123)))  # Finely tuned number #
        self.play(ReplacementTransform(point_at_4, point_at_the_left))
        self.add(point_at_the_left_copy_1, point_at_the_left_copy_2)
        self.play(
            point_at_the_left.animate.move_to(output_points[0]),
            point_at_the_left_copy_1.animate.move_to(output_points[1]),
            point_at_the_left_copy_2.animate.move_to(output_points[2])
        )

        self.play(
            FadeOut(point_at_the_left, point_at_the_left_copy_1, point_at_the_left_copy_2),
            Transform(ax, parabola_axes),
            Transform(labels, parabola_lables),
            Transform(curve, parabola_curve)
        )

        self.wait()

class Scene5(Scene):
    def construct(self):
        parabola_axes = Axes(
            x_range=[-7, 7, 1],
            y_range=[-2, 5, 1],
            x_length=14,
            y_length=7,
            axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
            }
        )

        parabola_lables = parabola_axes.get_axis_labels(
            Tex("radius", stroke_color=INPUT_COLOR, color=INPUT_COLOR).scale(0.5), Text("area", stroke_color=OUTPUT_COLOR, color=OUTPUT_COLOR).scale(0.4)
        )

        parabola_curve = parabola_axes.plot(areaFunction, [-1.5, 1.5], color=OUTPUT_COLOR, stroke_width=2)

        no_inputs_text = Tex("No input can have more than one output", color=YELLOW).scale(0.5).to_edge(UR)
        graph_text = Text("Graphs", color=PROCESS_COLOR).scale(0.75).to_corner(UL)

        r_value = ValueTracker(0)
        point_on_curve = always_redraw(lambda: Dot(parabola_axes.coords_to_point(r_value.get_value(), areaFunction(r_value.get_value())), color=INTERSECTION_COLOR, radius=0.05))

        r_brace = always_redraw(lambda: BraceBetweenPoints(parabola_axes.c2p(0, 0), parabola_axes.c2p(r_value.get_value(), 0), DOWN, color=PROCESS_COLOR))
        r_brace_value = always_redraw(lambda: MathTex(r"r = ", f"{r_value.get_value():.1f}", color=PROCESS_COLOR).scale(0.5 if abs(r_value.get_value()) > 0.4 else abs((0.5 / 0.4) * r_value.get_value())).next_to(r_brace, DOWN, buff=0.1))

        height_line = always_redraw(lambda: Line(parabola_axes.c2p(r_value.get_value(), 0), parabola_axes.c2p(r_value.get_value(), areaFunction(r_value.get_value())), stroke_width=2, color=PROCESS_COLOR))
        height_label = always_redraw(lambda:
            MathTex(r"A(", r"r", r")", color=OUTPUT_COLOR).scale(0.5 if abs(r_value.get_value()) > 0.5 else abs(r_value.get_value())).rotate(PI / 2 if r_value.get_value() < 0 else -PI / 2).next_to(height_line, LEFT if r_value.get_value() < 0 else RIGHT, buff=0.1)
        )

        vertical_line_test_text = Tex("Vertical Line Test", color=BLUE).scale(0.67).next_to(no_inputs_text, DOWN)
        vlt_point = ValueTracker(1.25)
        vertical_line = LineFromAngleAndPoint(PI / 2, parabola_axes.c2p(vlt_point.get_value(), 0), 20, color=PROCESS_COLOR, stroke_width=2)

        # these are very finely tuned functions to make the parametric curve
        def x(t):
            if(t < - (PI/3)):
                return (3 * t) + PI
            elif(t > (PI/3)):
                return (3 * t) - PI
            else:
                return -sin(3 * t)

        def y(t):
            return (cos( (0.5 * t) + 4 )) + ( (1/2) * (cos(3* t)) ) + ( (1/3) * (cos((6*t) - 6.5)) )

        def parametricFunction(t):
            return (x(t) - 1.5, y(0.5 * t) + 1)

        ax = Axes(
            x_range=[-7, 7, 1],
            y_range=[-3.5, 3.5, 1],
            x_length=14,
            y_length=7,
            axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
            }
        )

        labels = ax.get_axis_labels(
            Tex("x-axis", stroke_color=INPUT_COLOR, color=INPUT_COLOR).scale(0.5), Text("y-axis", stroke_color=OUTPUT_COLOR, color=OUTPUT_COLOR).scale(0.4)
        )

        curve = ax.plot_parametric_curve(parametricFunction, t_range=(-2.9, 3.9), stroke_width=2, color=OUTPUT_COLOR)

        self.add(parabola_axes, parabola_lables, parabola_curve, no_inputs_text, graph_text)

        self.wait(0.5)
        self.play(FadeIn(point_on_curve, r_brace, r_brace_value, height_line, height_label))
        self.play(r_value.animate.set_value(-1.25))
        self.wait(0.3)
        self.play(r_value.animate.set_value(1.25), run_time=1.5)
        self.play(ReplacementTransform(height_line, vertical_line), FadeOut(height_label, r_brace, r_brace_value), Write(vertical_line_test_text))
        point_on_curve2 = Dot(parabola_axes.coords_to_point(r_value.get_value(), areaFunction(r_value.get_value())), color=INTERSECTION_COLOR, radius=0.05)
        self.add(point_on_curve2)
        self.remove(point_on_curve)
        self.play(Transform(parabola_axes, ax), Transform(parabola_lables, labels), Transform(parabola_curve, curve), point_on_curve2.animate.shift(DOWN * 2.85))

        self.wait()

class Scene6(MovingCameraScene):
    def construct(self):
        # these are very finely tuned functions to make the parametric curve
        def x(t):
            if(t < - (PI/3)):
                return (3 * t) + PI
            elif(t > (PI/3)):
                return (3 * t) - PI
            else:
                return -sin(3 * t)

        def y(t):
            return (cos((0.5 * t) + 4)) + ((1 / 2) * (cos(3 * t))) + ((1 / 3) * (cos((6 * t) - 6.5)))

        def parametricFunction(t):
            return (x(t) - 1.5, y(0.5 * t) + 1)

        def intersectionPoints(x_value):
            x_value = x_value + 1.5
            t_values = []
            if (x_value > 0):
                t_values.append((x_value + PI)/(3))

                if (x_value <= 1):
                    t_values.extend([ans / 3 for ans in inverseSineGeneral(-x_value, [-1, 0])])

            elif (x_value < 0):
                t_values.append((x_value - PI)/(3))

                if (x_value >= -1):
                    t_values.extend([ans / 3 for ans in inverseSineGeneral(-x_value, [0, 1])])

            else:
                t_values.extend([-PI / 3, 0, PI / 3])

            t_values = list(set(t_values))

            return ([parametricFunction(t) for t in t_values])

        def parabola_intersection_points(x_value):
            y_values = []
            if x_value >= 0:
                y_values.append(sqrt(x_value))
                y_values.append(-sqrt(x_value))

            return [[x_value, y] for y in y_values]
        
        def circle_intersection_points(x_value):
            y_values = []
            if x_value >= -2 and x_value <= 2:
                y_values.append(sqrt(4 - x_value * x_value))
                y_values.append(-sqrt(4 - x_value * x_value))

            return [[x_value, y] for y in y_values]

        ax = Axes(
            x_range=[-7, 7, 1],
            y_range=[-3.5, 3.5, 1],
            x_length=14,
            y_length=7,
            axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
            }
        )

        labels = ax.get_axis_labels(
            Tex("x-axis", stroke_color=INPUT_COLOR, color=INPUT_COLOR).scale(0.5), Text("y-axis", stroke_color=OUTPUT_COLOR, color=OUTPUT_COLOR).scale(0.4)
        )

        curve = ax.plot_parametric_curve(parametricFunction, t_range=(-2.9, 3.9), stroke_width=2, color=OUTPUT_COLOR)
        sideways_parabola = ax.plot_implicit_curve(lambda x, y: (y ** 2) - x, color=OUTPUT_COLOR, stroke_width=2)
        sine_curve = ax.plot(lambda x: sin(x), [-7, 7], color=OUTPUT_COLOR, stroke_width=2)

        circle = Circle(radius=2, color=OUTPUT_COLOR , stroke_width = 2)


        no_inputs_text = Tex("No input can have more than one output", color=YELLOW).scale(0.5).to_edge(UR)
        graph_text = Text("Graphs", color=PROCESS_COLOR).scale(0.75).to_corner(UL)
        vertical_line_test_text = Tex("Vertical Line Test", color=BLUE).scale(0.67).next_to(no_inputs_text, DOWN)

        x_value = ValueTracker(1.25)
        vertical_line = always_redraw(lambda: LineFromAngleAndPoint(PI / 2, ax.c2p(x_value.get_value(), 0), 20, color=BLUE, stroke_width=2))

        intersections = always_redraw(lambda: VGroup(
            *[Dot(ax.c2p(*point), color=INTERSECTION_COLOR, radius=0.05) for point in intersectionPoints(x_value.get_value())]
        ))

        parabola_intersections = always_redraw(lambda: VGroup(
            *[Dot(ax.c2p(*point), color=INTERSECTION_COLOR, radius=0.05) for point in parabola_intersection_points(x_value.get_value())]
        ))

        sine_intersections = always_redraw(lambda: VGroup(
            *[Dot(ax.c2p(x_value.get_value(), sin(x_value.get_value())), color=INTERSECTION_COLOR, radius=0.05)]
        ))

        circle_intersections = always_redraw(lambda: VGroup(
            *[Dot(ax.c2p(*point), color=INTERSECTION_COLOR, radius=0.05) for point in circle_intersection_points(x_value.get_value())]
        ))

        not_a_function_symbol = Cross(stroke_width=5).scale(0.25).next_to(graph_text, DOWN, buff=0.5)
        # not_a_function_symbol[0].set_cap_style(CapStyleType.ROUND)
        # not_a_function_symbol[1].set_cap_style(CapStyleType.ROUND)
        yes_a_function_symbol = Checkmark(color=GREEN).scale(0.5).move_to(not_a_function_symbol)

        self.add(ax, labels, curve, no_inputs_text, graph_text, vertical_line_test_text, vertical_line, intersections)
        self.wait(0.5)
        # slow the shifting of the vertical line
        self.play(x_value.animate.set_value(-1.5), run_time=2)
        self.play(Create(not_a_function_symbol))
        self.add(parabola_intersections)
        self.play(ReplacementTransform(curve, sideways_parabola), FadeOut(intersections))
        self.play(x_value.animate.set_value(1.25))
        self.play(Indicate(not_a_function_symbol))
        self.play(ReplacementTransform(sideways_parabola, sine_curve), ReplacementTransform(parabola_intersections, sine_intersections))
        self.play(x_value.animate.set_value(-7) , rate_func = smootherstep , run_time = 2)
        self.play(x_value.animate.set_value(7) , rate_func = smootherstep , run_time = 2.3)
        self.play(FadeTransform(not_a_function_symbol, yes_a_function_symbol))
        self.play(ReplacementTransform(sine_curve, circle), FadeOut(sine_intersections))
        self.add(circle_intersections)
        self.play(x_value.animate.set_value(1))
        self.play(FadeTransform(yes_a_function_symbol, not_a_function_symbol))

        # At last I want the camera to move to the right
        # This will have the effect of moving all of the mobjects to the left
        # At the right, there will be a text that says "Domain and Range" vertically centered



        domain_and_range_text = Text("Domain and Range", color=BLUE).scale(0.67).move_to([self.camera.frame_width , 0 , 0])
        self.add(domain_and_range_text)
        self.play(self.camera.frame.animate.move_to(domain_and_range_text))


        self.wait()


class Scene7(Scene):
    def construct(self):
        domain_and_range_text = Text("Domain and Range", color=PROCESS_COLOR).scale(0.67)
        domain_description = Tex(r"\begin{center} Domain is the set of all numbers \\ that a function is allowed to take as input.\end{center}" , color=YELLOW , stroke_color=YELLOW).scale(0.75)

        example_function = MathTex(r"f(" , r"x" , r") = 3" , r"x" , color=OUTPUT_COLOR).scale(0.75).shift(RIGHT * 0.3)
        example_function[1].set_color(INPUT_COLOR)
        example_function[3].set_color(INPUT_COLOR)

        mini_axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            x_length=10,
            y_length=10,
            axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
            }
        )
        mini_axes_labels = mini_axes.get_axis_labels(
            Tex("x", stroke_color=INPUT_COLOR, color=INPUT_COLOR).scale(0.5), Text("y", stroke_color=OUTPUT_COLOR, color=OUTPUT_COLOR).scale(0.4)
        )
        mini_axes_labels[0].shift(LEFT * 0.5)
        mini_axes_labels[1].shift(UP)

        mini_axes_curve = mini_axes.plot(lambda x: 3 * x, [-10/3, 10/3], color=OUTPUT_COLOR, stroke_width=2)
        mini_axes_curve2 = mini_axes.plot(lambda x: 3 * x, [-2, 1], color=OUTPUT_COLOR, stroke_width=2)
        mini_axes_boundary = Rectangle(width=10.5, height=10.5, color=WHITE, stroke_width=2)

        solid_dots = VGroup(
            Dot(mini_axes.coords_to_point(-2, -6), color=OUTPUT_COLOR, radius=0.05),
            Dot(mini_axes.coords_to_point(1, 3), color=OUTPUT_COLOR, radius=0.05)
        )

        domain_line1 = Line(mini_axes.coords_to_point(-10, 0), mini_axes.coords_to_point(10, 0), color=YELLOW, stroke_width=4)
        domain_line2 = Line(mini_axes.coords_to_point(-2 , 0), mini_axes.coords_to_point(1, 0), color=YELLOW, stroke_width=4)


        mini_axes_group = VGroup(mini_axes[0] , mini_axes[1] , mini_axes_labels[0] , mini_axes_labels[1] , mini_axes_curve , mini_axes_curve2 , mini_axes_boundary , solid_dots[0] , solid_dots[1] , domain_line1 , domain_line2)
        mini_axes_group = myScale(mini_axes_group, 0.5)
        mini_axes_group.to_edge(LEFT).shift(LEFT * 0.3)

        domain_answer = MathTex(r"\text{Domain: }" , r"\mathbb{R}" , color=BLUE).scale(0.65).next_to(example_function, DOWN)
        domain_answer_interval_notation = MathTex(r"\text{Domain: }" , r"(-\infty , \infty)" , color=BLUE).scale(0.65).move_to(domain_answer).align_to(domain_answer, LEFT)
        domain_answer[1].set_color(YELLOW)
        domain_answer_interval_notation[1].set_color(YELLOW)

        domain_answer_interval_notation2 = MathTex(r"\text{Domain: }" , r"\left[-2 , 1\right]" , color=BLUE).scale(0.65).move_to(domain_answer).align_to(domain_answer, LEFT)
        domain_answer_interval_notation2[1].set_color(YELLOW)

        domain_restriction = MathTex(r"\left\{-2 \leq " , r"x" , r" \leq 1\right\}" , color=BLUE).scale(0.65).next_to(example_function, RIGHT)
        domain_restriction[1].set_color(INPUT_COLOR)

        mini_axes_group.remove(mini_axes_curve2 , solid_dots[1] , solid_dots[0] , domain_line1 , domain_line2)

        


        self.add(domain_and_range_text)
        self.play(domain_and_range_text.animate.to_corner(UL))
        self.play(Write(domain_description))
        self.play(domain_description.animate.scale(0.8).to_corner(UR))
        self.play(Write(example_function))
        self.play(FadeIn(mini_axes_group))
        self.play(Circumscribe(example_function[3] , Circle , fade_out=True , stroke_width=1.5))
        self.play(Write(domain_answer))
        self.play(Indicate(domain_answer[1] , rate_func=there_and_back_with_pause))
        self.play(Transform(domain_answer[1] , domain_answer_interval_notation[1]) , Create(domain_line1))
        self.play(Write(domain_restriction))
        self.play(Transform(mini_axes_curve , mini_axes_curve2) , FadeIn(solid_dots))
        self.play(Transform(domain_answer[1] , domain_answer_interval_notation2[1]) , Transform(domain_line1 , domain_line2))

        self.play(FadeOut(example_function , domain_restriction , domain_answer , mini_axes_curve , solid_dots , domain_line1))
        self.wait()

class Scene8(Scene):
    def construct(self):
        domain_and_range_text = Text("Domain and Range", color=PROCESS_COLOR).scale(0.67).to_corner(UL)
        domain_description = Tex(r"\begin{center} Domain is the set of all numbers \\ that a function is allowed to take as input.\end{center}" , color=YELLOW , stroke_color=YELLOW).scale(0.75 * 0.8).to_corner(UR)
        
        mini_axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            x_length=10,
            y_length=10,
            axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
            }
        )

        mini_axes_labels = mini_axes.get_axis_labels(
            Tex("x", stroke_color=INPUT_COLOR, color=INPUT_COLOR).scale(0.5), Text("y", stroke_color=OUTPUT_COLOR, color=OUTPUT_COLOR).scale(0.4)
        )

        mini_axes_labels[0].shift(LEFT * 0.5)
        mini_axes_labels[1].shift(UP)

        mini_axes_boundary = Rectangle(width=10.5, height=10.5, color=WHITE, stroke_width=2)

        example_function = MathTex(r"g(" , r"x" , r") = \sqrt{" , r"{x}" , r"}" , r"a" , color=OUTPUT_COLOR).scale(0.75).shift(RIGHT * 0.3)
        example_function[1].set_color(INPUT_COLOR)
        example_function[5].set_color(INPUT_COLOR) # for some reason, this works. only took me 2 hours to figure out

        mini_axes_curve = mini_axes.plot(lambda x: sqrt(x), [0, 10], color=OUTPUT_COLOR, stroke_width=2)
        domain_line = Line(mini_axes.c2p(0 , 0) , mini_axes.c2p(10 , 0) , color=YELLOW , stroke_width=4)

        mini_axes_curve2 = mini_axes.plot(lambda x: sqrt(x), [1, 10], color=OUTPUT_COLOR, stroke_width=2)
        domain_line2 = Line(mini_axes.c2p(1 , 0) , mini_axes.c2p(10 , 0) , color=YELLOW , stroke_width=4)

        mini_axes_group = VGroup(mini_axes[0] , mini_axes[1] , mini_axes_labels[0] , mini_axes_labels[1] , mini_axes_boundary , mini_axes_curve , domain_line , mini_axes_curve2 , domain_line2)
        mini_axes_group = myScale(mini_axes_group, 0.5)
        mini_axes_group.to_edge(LEFT).shift(LEFT * 0.3)
        mini_axes_group.remove(mini_axes_curve , domain_line , mini_axes_curve2 , domain_line2)

        domain_in_x = MathTex(r"\{x \geq 0\}" , color=BLUE).scale(0.7).next_to(example_function , RIGHT , buff=0.5)
        domain_interval_notation = MathTex(r"\text{Domain: }" , r"[0 , \infty)" , color=BLUE).scale(0.65).next_to(example_function , DOWN).align_to(example_function , LEFT)
        domain_interval_notation[1].set_color(YELLOW)

        x_value = ValueTracker(-1)
        restricted_arrow = always_redraw(lambda : Arrow(mini_axes.c2p(-5 , -5) , mini_axes.c2p(x_value.get_value() , 0) , color=RED , max_stroke_width_to_length_ratio=1.5 , max_tip_length_to_length_ratio=0.1 , buff=0.1))
        x_value.set_value(-10)
        unrestricted_arrow = always_redraw(lambda : Arrow(mini_axes.c2p(5 , -5) , mini_axes.c2p(x_value.get_value() + 10 , 0) , color=GREEN , max_stroke_width_to_length_ratio=1.5 , max_tip_length_to_length_ratio=0.1 , buff=0.1))
        x_value.set_value(-1)

        

        self.add(domain_and_range_text , domain_description , mini_axes_group)
        self.play(Write(example_function))
        self.play(Create(mini_axes_curve))
        self.play(GrowArrow(restricted_arrow))
        self.play(x_value.animate.set_value(-10))
        self.play(ReplacementTransform(restricted_arrow , unrestricted_arrow))
        self.play(Write(domain_in_x) , x_value.animate.set_value(0) , Create(domain_line))
        self.play(FadeOut(unrestricted_arrow))
        self.play(Write(domain_interval_notation))

        domain_interval_notation2 = MathTex(r"\text{Domain: }" , r"\left[1 , \infty\right)" , color=BLUE).scale(0.65).next_to(example_function , DOWN).align_to(example_function , LEFT)
        domain_interval_notation2[1].set_color(YELLOW)

        self.play(Transform(domain_in_x , MathTex(r"\{x \geq 1\}" , color=BLUE).scale(0.7).next_to(example_function , RIGHT , buff=0.5)) , Transform(domain_interval_notation , domain_interval_notation2))
        self.play(Transform(mini_axes_curve , mini_axes_curve2) , Transform(domain_line , domain_line2))

        self.wait()
        self.play(FadeOut(example_function , domain_in_x , domain_interval_notation , mini_axes_curve , domain_line))
        self.wait()

class Scene9(Scene):
    def construct(self):
        domain_and_range_text = Text("Domain and Range", color=PROCESS_COLOR).scale(0.67).to_corner(UL)
        domain_description = Tex(r"\begin{center} Domain is the set of all numbers \\ that a function is allowed to take as input.\end{center}" , color=YELLOW , stroke_color=YELLOW).scale(0.75 * 0.8).to_corner(UR)
        
        mini_axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            x_length=10,
            y_length=10,
            axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
            }
        )

        mini_axes_labels = mini_axes.get_axis_labels(
            Tex("x", stroke_color=INPUT_COLOR, color=INPUT_COLOR).scale(0.5), Text("y", stroke_color=OUTPUT_COLOR, color=OUTPUT_COLOR).scale(0.4)
        )

        mini_axes_labels[0].shift(LEFT * 0.5)
        mini_axes_labels[1].shift(UP)

        mini_axes_boundary = Rectangle(width=10.5, height=10.5, color=WHITE, stroke_width=2)

        mini_axes_curve = mini_axes.plot(lambda x: sqrt(4 - x), [-10, 4], color=OUTPUT_COLOR, stroke_width=2).reverse_points()
        domain_line = Line(mini_axes.c2p(-10 , 0) , mini_axes.c2p(4 , 0) , color=YELLOW , stroke_width=4)

        mini_axes_group = VGroup(mini_axes[0] , mini_axes[1] , mini_axes_labels[0] , mini_axes_labels[1] , mini_axes_boundary , mini_axes_curve , domain_line)
        mini_axes_group = myScale(mini_axes_group, 0.5)
        mini_axes_group.to_edge(LEFT).shift(LEFT * 0.3)
        mini_axes_group.remove(mini_axes_curve , domain_line)

        example_function = MathTex(r"f(" , r"x" , r") = \sqrt{" , r"4" , r"-" , r"x" , r"}" , r"a" , color=OUTPUT_COLOR).scale(0.75).shift(RIGHT * 0.3)
        example_function[1].set_color(INPUT_COLOR)
        example_function[7].set_color(INPUT_COLOR)
        # example_function[0].set_color(RED)
        # example_function[1].set_color(BLUE)
        # example_function[2].set_color(GREEN)
        # example_function[3].set_color(YELLOW)
        # example_function[4].set_color(PURE_BLUE)
        # example_function[5].set_color(PURPLE)
        # example_function[6].set_color(PURE_RED)
        # example_function[7].set_color(WHITE)

        domain_in_x = MathTex(r"4-" , r"x" , r"\geq 0" , color=BLUE).scale(0.7).next_to(example_function , RIGHT , buff=0.8).shift(UP)
        domain_in_x[1].set_color(INPUT_COLOR)

        domain_in_x2 = MathTex(r"\Rightarrow" , r"4 \geq", r"x" , color=BLUE).scale(0.7).next_to(domain_in_x , DOWN)
        domain_in_x2[2].set_color(INPUT_COLOR)

        domain_in_x3 = MathTex(r"\Rightarrow" , r"x" ,  r"\leq 4" , color=BLUE).scale(0.7).next_to(domain_in_x2 , DOWN)
        domain_in_x3[1].set_color(INPUT_COLOR)

        domain_interval_notation = MathTex(r"\text{Domain: }" , r"\left(-\infty , 4\right]" , color=BLUE).scale(0.65).next_to(example_function , DOWN).align_to(example_function , LEFT)
        domain_interval_notation[1].set_color(YELLOW)


        self.add(domain_and_range_text , domain_description , mini_axes_group)
        self.play(Write(example_function))
        self.play(Create(mini_axes_curve))
        self.play(Indicate(example_function[4:]))
        self.play(Write(domain_in_x))
        self.play(Write(domain_in_x2))
        self.play(Write(domain_in_x3))
        self.play(Write(domain_interval_notation) , Create(domain_line))
        self.wait()
        self.play(FadeOut(example_function , domain_in_x , domain_in_x2 , domain_in_x3 , domain_interval_notation , mini_axes_curve , domain_line))
        self.wait()


class Scene10(Scene):
    def construct(self):
        domain_and_range_text = Text("Domain and Range", color=PROCESS_COLOR).scale(0.67).to_corner(UL)
        domain_description = Tex(r"\begin{center} Domain is the set of all numbers \\ that a function is allowed to take as input.\end{center}" , color=YELLOW , stroke_color=YELLOW).scale(0.75 * 0.8).to_corner(UR)
        
        mini_axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            x_length=10,
            y_length=10,
            axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
            }
        )

        mini_axes_labels = mini_axes.get_axis_labels(
            Tex("x", stroke_color=INPUT_COLOR, color=INPUT_COLOR).scale(0.5), Text("y", stroke_color=OUTPUT_COLOR, color=OUTPUT_COLOR).scale(0.4)
        )

        mini_axes_labels[0].shift(LEFT * 0.5)
        mini_axes_labels[1].shift(UP)

        mini_axes_curve = mini_axes.plot(lambda x: sqrt(16 - x ** 2), [-4, 4], color=OUTPUT_COLOR, stroke_width=2)
        domain_line = Line(mini_axes.c2p(-4 , 0) , mini_axes.c2p(4 , 0) , color=YELLOW , stroke_width=4)

        mini_axes_boundary = Rectangle(width=10.5, height=10.5, color=WHITE, stroke_width=2)

        mini_axes_group = VGroup(mini_axes[0] , mini_axes[1] , mini_axes_labels[0] , mini_axes_labels[1] , mini_axes_boundary , mini_axes_curve , domain_line)
        mini_axes_group = myScale(mini_axes_group, 0.5)
        mini_axes_group.to_edge(LEFT).shift(LEFT * 0.3)
        mini_axes_group.remove(mini_axes_curve , domain_line)


        example_function = MathTex(r"f(" , r"x" , r") = \sqrt{16-" , r"x" , r"^2}" , color=OUTPUT_COLOR).scale(0.75).shift(RIGHT * 0.3)
        example_function[1].set_color(INPUT_COLOR)
        example_function[3].set_color(INPUT_COLOR)

        domain_in_x = MathTex(r"16-" , r"x" , r"^2 \geq 0" , color=BLUE).scale(0.7).next_to(example_function , RIGHT , buff=0.8).shift(UP)
        domain_in_x[1].set_color(INPUT_COLOR)

        domain_in_x2 = MathTex(r"\Rightarrow" , r"16" , r"\geq" , r"x" , r"^2" , color=BLUE).scale(0.7).next_to(domain_in_x , DOWN)
        domain_in_x2[3].set_color(INPUT_COLOR)

        domain_in_x3 = MathTex(r"\Rightarrow" , r"x" ,  r"^2" , r"\leq" , r"16" , color=BLUE).scale(0.7).next_to(domain_in_x2 , DOWN)
        domain_in_x3[1].set_color(INPUT_COLOR)

        domain_in_x4 = MathTex(r"\Rightarrow" , r"-4 \leq" ,  r"x" , r"\leq 4" , color=BLUE).scale(0.7).next_to(domain_in_x3 , DOWN)
        domain_in_x4[2].set_color(INPUT_COLOR)

        solution_step1 = MathTex(r"x" , r"^2 = 16" , color=BLUE).scale(0.7).next_to(domain_in_x , RIGHT , buff=0.8)
        solution_step1[0].set_color(INPUT_COLOR)

        solution_step2 = MathTex(r"x" , r"= \pm 4" , color=BLUE).scale(0.7).next_to(solution_step1 , DOWN)
        solution_step2[0].set_color(INPUT_COLOR)

        screen_rectangle = screenRectanlge(0.85)
        solution_step_axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-2, 18, 1],
            x_length=7,
            y_length=7,
            axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
                "tick_size": 0.05,
            }
        )
        solution_step_axes_labels = solution_step_axes.get_axis_labels(
            Tex("x", stroke_color=INPUT_COLOR, color=INPUT_COLOR).scale(0.5), MathTex("y=x^2", stroke_color=OUTPUT_COLOR, color=OUTPUT_COLOR).scale(0.5)
        )
        solution_step_curve = solution_step_axes.plot(lambda x: x ** 2, [-sqrt(18), sqrt(18)], color=OUTPUT_COLOR, stroke_width=2)

        intersection_points = VGroup(
            Dot(solution_step_axes.coords_to_point(-4, 16), color=INTERSECTION_COLOR, radius=0.05),
            Dot(solution_step_axes.coords_to_point(4, 16), color=INTERSECTION_COLOR, radius=0.05)
        )

        intersection_curve1 = solution_step_axes.plot(lambda x: x**2, [-4, 0], color=INTERSECTION_COLOR, stroke_width=2)
        intersection_curve2 = solution_step_axes.plot(lambda x: x**2, [0, 4], color=INTERSECTION_COLOR, stroke_width=2).reverse_points()
        solution_step_domain_line1 = solution_step_axes.plot(lambda x: 0, [-4, 0], color=YELLOW, stroke_width=2)
        solution_step_domain_line2 = solution_step_axes.plot(lambda x: 0, [0, 4], color=YELLOW, stroke_width=2).reverse_points()

        domain_in_interval_notation = MathTex(r"\text{Domain: }" , r"\left[-4 , 4\right]" , color=BLUE).scale(0.65).next_to(example_function , DOWN).align_to(example_function , LEFT)
        domain_in_interval_notation[1].set_color(YELLOW)

        self.add(domain_and_range_text , domain_description , mini_axes_group)
        self.play(Write(example_function))
        self.play(Create(mini_axes_curve))
        self.play(Write(domain_in_x))
        self.play(Write(domain_in_x2))
        self.play(
            TransformFromCopy(domain_in_x2[0] , domain_in_x3[0]),
            TransformFromCopy(domain_in_x2[1] , domain_in_x3[4]),
            TransformFromCopy(domain_in_x2[2] , domain_in_x3[3]),
            TransformFromCopy(domain_in_x2[3:] , domain_in_x3[1:3])
        )

        self.play(Write(solution_step1))
        self.play(Write(solution_step2))
        self.play(Indicate(domain_in_x3))
        self.play(Write(domain_in_x4))
        self.play(AnimationGroup(
            FadeIn(screen_rectangle),
            FadeIn(solution_step_axes , solution_step_axes_labels),
            lag_ratio=0.5
        ))
        self.play(Create(solution_step_curve))
        self.play(FadeIn(intersection_points))
        self.play(Create(intersection_curve1) , Create(intersection_curve2))
        self.play(TransformFromCopy(intersection_curve1 , solution_step_domain_line1) , TransformFromCopy(intersection_curve2 , solution_step_domain_line2))
        self.play(FadeOut(screen_rectangle , solution_step_axes , solution_step_axes_labels , solution_step_curve , intersection_points , intersection_curve1 , intersection_curve2 , solution_step_domain_line1 , solution_step_domain_line2))
        self.play(Write(domain_in_interval_notation) , Create(domain_line))
        self.play(ApplyWave(domain_line , amplitude=0.1 , time_width=3.5))

        self.wait()
        self.play(FadeOut(example_function , domain_in_x , domain_in_x2 , domain_in_x3 , domain_in_x4 , domain_in_interval_notation , mini_axes_curve , domain_line , solution_step1 , solution_step2))
        self.wait()

class Scene11(Scene):
    def construct(self):
        domain_and_range_text = Text("Domain and Range", color=PROCESS_COLOR).scale(0.67).to_corner(UL)
        domain_description = Tex(r"\begin{center} Domain is the set of all numbers \\ that a function is allowed to take as input.\end{center}" , color=YELLOW , stroke_color=YELLOW).scale(0.75 * 0.8).to_corner(UR)
        
        mini_axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            x_length=10,
            y_length=10,
            axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
            }
        )

        mini_axes_labels = mini_axes.get_axis_labels(
            Tex("x", stroke_color=INPUT_COLOR, color=INPUT_COLOR).scale(0.5), Text("y", stroke_color=OUTPUT_COLOR, color=OUTPUT_COLOR).scale(0.4)
        )

        mini_axes_labels[0].shift(LEFT * 0.5)
        mini_axes_labels[1].shift(UP)

        mini_axes_boundary = Rectangle(width=10.5, height=10.5, color=WHITE, stroke_width=2)

        mini_axes_curve1 = mini_axes.plot(lambda x: 1 / sqrt((x**2) - 1), [-10, -sqrt(101/100)], color=OUTPUT_COLOR, stroke_width=2 , use_smoothing=False).reverse_points()
        mini_axes_curve2 = mini_axes.plot(lambda x: 1 / sqrt((x**2) - 1), [sqrt(101/100), 10], color=OUTPUT_COLOR, stroke_width=2 , use_smoothing=False)
        mini_axes_curve = VGroup(mini_axes_curve1 , mini_axes_curve2)

        domain_line1 = Line(mini_axes.c2p(-10 , 0) , mini_axes.c2p(-1 , 0) , color=YELLOW , stroke_width=4).reverse_points()
        domain_line2 = Line(mini_axes.c2p(1 , 0) , mini_axes.c2p(10 , 0) , color=YELLOW , stroke_width=4)
        domain_line = VGroup(domain_line1 , domain_line2)

        mini_axes_group = VGroup(mini_axes[0] , mini_axes[1] , mini_axes_labels[0] , mini_axes_labels[1] , mini_axes_boundary , mini_axes_curve , domain_line)
        mini_axes_group = myScale(mini_axes_group, 0.5)
        mini_axes_group.to_edge(LEFT).shift(LEFT * 0.3)
        mini_axes_group.remove(mini_axes_curve , domain_line)

        example_function = MathTex(r"f(" , r"x" , r") = " , r"{1 \over " , r"\sqrt{" , r"x" , r"^2" , r"-" , r"1" , r"}" , r"}", color=OUTPUT_COLOR).scale(0.75).shift(RIGHT * 0.3)
        example_function[1].set_color(INPUT_COLOR)
        example_function[5].set_color(INPUT_COLOR)

        domain_in_x1 = MathTex(r"x" , r"^2-1 > 0" , color=BLUE).scale(0.7).next_to(example_function , RIGHT , buff=0.8).shift(UP)
        domain_in_x1[0].set_color(INPUT_COLOR)

        domain_in_x2 = MathTex(r"\Rightarrow" , r"x" , r"^2 > 1" , color=BLUE).scale(0.7).next_to(domain_in_x1 , DOWN)
        domain_in_x2[1].set_color(INPUT_COLOR)

        domain_in_x3 = MathTex(r"\Rightarrow" , r"x" , r"< -1 \;\;" , r"\text{ or }" , r"\;\;x" , r"> 1" , color=BLUE).scale(0.7).next_to(domain_in_x2 , DOWN).align_to(domain_in_x2 , LEFT)
        domain_in_x3[1].set_color(INPUT_COLOR)
        domain_in_x3[3].set_color(GREEN)
        domain_in_x3[4].set_color(INPUT_COLOR)

        domain_in_interval_notation = MathTex(r"\text{Domain: }" , r"\left(-\infty , -1\right)" , r"\cup" , r"\left( 1 , \infty \right)" , color=BLUE).scale(0.65).next_to(example_function , DOWN).align_to(example_function , LEFT)
        domain_in_interval_notation[1].set_color(YELLOW)
        domain_in_interval_notation[2].set_color(GREEN)
        domain_in_interval_notation[3].set_color(YELLOW)

        screen_rectangle = screenRectanlge(0.85)
        solution_step_axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-2, 18, 1],
            x_length=7,
            y_length=7,
            axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
                "tick_size": 0.05,
            }
        )
        solution_step_axes_labels = solution_step_axes.get_axis_labels(
            Tex("x", stroke_color=INPUT_COLOR, color=INPUT_COLOR).scale(0.5), MathTex("y=x^2", stroke_color=OUTPUT_COLOR, color=OUTPUT_COLOR).scale(0.5)
        )
        solution_step_curve = solution_step_axes.plot(lambda x: x ** 2, [-sqrt(18), sqrt(18)], color=OUTPUT_COLOR, stroke_width=2)

        intersection_points = VGroup(
            Dot(solution_step_axes.coords_to_point(-1, 1), color=YELLOW , radius=0.05),
            Dot(solution_step_axes.coords_to_point(1, 1), color=YELLOW , radius=0.05)
        )

        intersection_curve1 = solution_step_axes.plot(lambda x: x**2, [-10, -1], color=INTERSECTION_COLOR, stroke_width=2).reverse_points()
        intersection_curve2 = solution_step_axes.plot(lambda x: x**2, [1, 10], color=INTERSECTION_COLOR, stroke_width=2)
        solution_step_domain_line1 = solution_step_axes.plot(lambda x: 0, [-10, -1], color=YELLOW, stroke_width=2).reverse_points()
        solution_step_domain_line2 = solution_step_axes.plot(lambda x: 0, [1, 10], color=YELLOW, stroke_width=2)



        self.add(domain_and_range_text , domain_description , mini_axes_group)
        self.play(Write(example_function) , run_time = 1.5)
        self.play(Create(mini_axes_curve[0]) , Create(mini_axes_curve[1]) , run_time = 1 , rate_func = rush_into)
        self.play(Write(domain_in_x1))
        self.play(Write(domain_in_x2))

        self.play(AnimationGroup(
            FadeIn(screen_rectangle),
            FadeIn(solution_step_axes , solution_step_axes_labels),
            lag_ratio=0.5
        ))

        self.play(Create(solution_step_curve))
        self.play(FadeIn(intersection_points))
        self.play(Indicate(domain_in_x2))
        self.play(Create(intersection_curve1) , Create(intersection_curve2))
        self.play(TransformFromCopy(intersection_curve1 , solution_step_domain_line1) , TransformFromCopy(intersection_curve2 , solution_step_domain_line2))
        self.play(FadeOut(screen_rectangle , solution_step_axes , solution_step_axes_labels , solution_step_curve , solution_step_domain_line1 , solution_step_domain_line2 , intersection_curve1 , intersection_curve2 , intersection_points))
        self.play(Write(domain_in_x3))

        self.play(Write(domain_in_interval_notation) , Create(domain_line1) , Create(domain_line2))
        self.wait()
        self.play(FadeOut(mini_axes_group , example_function , domain_in_interval_notation , domain_in_x1 , domain_in_x2 , domain_in_x3 , domain_line1 , domain_line2 , mini_axes_curve) , domain_and_range_text.animate.move_to(domain_and_range_text.copy().move_to(ORIGIN).to_edge(UP)) , domain_description.animate.scale(1.25).move_to(ORIGIN))

        self.wait()

class Scene12(Scene):
    def construct(self):
        domain_and_range_text = Text("Domain and Range", color=PROCESS_COLOR).scale(0.67).to_edge(UP)
        domain_description = Tex(r"\begin{center} Domain is the set of all numbers \\ that a function is allowed to take as input.\end{center}" , color=YELLOW , stroke_color=YELLOW).scale(0.75)
        range_description = Tex(r"\begin{center} Range is the set of all numbers \\ that a function can give as output.\end{center}" , color=YELLOW , stroke_color=YELLOW).scale(0.75)

        mini_axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            x_length=10,
            y_length=10,
            axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
            }
        )

        mini_axes_labels = mini_axes.get_axis_labels(
            Tex("x", stroke_color=INPUT_COLOR, color=INPUT_COLOR).scale(0.5), Text("y", stroke_color=OUTPUT_COLOR, color=OUTPUT_COLOR).scale(0.4)
        )

        mini_axes_labels[0].shift(LEFT * 0.5)
        mini_axes_labels[1].shift(UP)

        mini_axes_boundary = Rectangle(width=10.5, height=10.5, color=WHITE, stroke_width=2)

        mini_axes_curve = mini_axes.plot(lambda x : (2*x)-1 , [-9/2 , 11/2] , color=OUTPUT_COLOR , stroke_width = 2)

        range_line = Line(mini_axes.c2p(0 , -10) , mini_axes.c2p(0 , 10) , color=YELLOW , stroke_width=4)
        

        mini_axes_group = VGroup(mini_axes[0] , mini_axes[1] , mini_axes_labels[0] , mini_axes_labels[1] , mini_axes_boundary , mini_axes_curve , range_line)
        mini_axes_group = myScale(mini_axes_group, 0.5)
        mini_axes_group.to_edge(LEFT).shift(LEFT * 0.3)
        mini_axes_group.remove(range_line)


        example_function = MathTex(r"f(" , r"x" , r") = 2" , r"x" , r"- 1", color=OUTPUT_COLOR).scale(0.75).shift(RIGHT * 0.3)
        example_function[1].set_color(INPUT_COLOR)
        example_function[3].set_color(INPUT_COLOR)

        domain_in_interval_notation = MathTex(r"\text{Domain: }" , r"\left(-\infty , \infty\right)" , color=BLUE).scale(0.65).next_to(example_function , DOWN).align_to(example_function , LEFT)
        domain_in_interval_notation[1].set_color(YELLOW)

        range_in_interval_notation = MathTex(r"\text{Range: }" , r"\left(-\infty , \infty\right)" , color=BLUE).scale(0.65).next_to(domain_in_interval_notation , DOWN).align_to(domain_in_interval_notation , LEFT)
        range_in_interval_notation[1].set_color(YELLOW)

        screen_rectangle = screenRectanlge(0.85)
        focused_text = Text("Is that actually true?" , stroke_color=BLUE , color=BLUE).scale(0.8)

        naturals = VGroup(
            [MathTex(f"{i}" , color = WHITE).scale(0.75) for i in range(1 , 12)]
        )
        naturals.add(MathTex(r"\cdots" , color = WHITE).scale(0.75))

        naturals.arrange(RIGHT , buff=0.85)


        self.add(domain_and_range_text , domain_description)
        self.play(Unwrite(domain_description) , run_time = 1.3)
        self.wait(0.15)
        self.play(Write(range_description[0][0:5]))
        self.play(Write(range_description[0][5:]))
        self.play(domain_and_range_text.animate.to_corner(UL) , range_description.animate.scale(0.8).to_corner(UR))
        self.play(Write(example_function))

        self.play(FadeIn(mini_axes_group))
        self.play(Write(domain_in_interval_notation))
        self.play(FocusOn(example_function[3]) , run_time = 1)
        self.play(ApplyWave(mini_axes[0] , time_width=3.5 , amplitude=0.1) , run_time = 1.3)
        self.play(FadeIn(screen_rectangle) , Write(focused_text) , run_time = 1.2)
        self.wait(0.2)
        self.play(focused_text.animate.shift(UP * 1.25) , Write(naturals))
        self.play(
            AnimationGroup(
                *[Transform(naturals[i] , MathTex(f"{2 * (i+1)}" , color = WHITE).scale(0.75).move_to(naturals[i])) for i in range(len(naturals) - 1)],
                lag_ratio=0.1           
            )
        )
        self.play(FadeOut(screen_rectangle , naturals , focused_text))
        self.play(Circumscribe(example_function[4] , stroke_width=2))
        self.play(Write(range_in_interval_notation) , Create(range_line))

        self.play(FadeOut(example_function , domain_in_interval_notation , range_in_interval_notation , mini_axes_curve , range_line))

        self.wait()

class Scene13(Scene):
    def construct(self):
        domain_and_range_text = Text("Domain and Range", color=PROCESS_COLOR).scale(0.67).to_corner(UL)
        range_description = Tex(r"\begin{center} Range is the set of all numbers \\ that a function can give as output.\end{center}" , color=YELLOW , stroke_color=YELLOW).scale(0.75 * 0.8).to_corner(UR)

        mini_axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            x_length=10,
            y_length=10,
            axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
            }
        )

        mini_axes_labels = mini_axes.get_axis_labels(
            Tex("x", stroke_color=INPUT_COLOR, color=INPUT_COLOR).scale(0.5), Text("y", stroke_color=OUTPUT_COLOR, color=OUTPUT_COLOR).scale(0.4)
        )

        mini_axes_labels[0].shift(LEFT * 0.5)
        mini_axes_labels[1].shift(UP)

        mini_axes_boundary = Rectangle(width=10.5, height=10.5, color=WHITE, stroke_width=2)

        mini_axes_curve = mini_axes.plot(lambda x : (x**2)-1 , [-sqrt(11) , sqrt(11)] , color=OUTPUT_COLOR , stroke_width = 2)

        range_line1 = Line(mini_axes.c2p(0 , 0) , mini_axes.c2p(0 , 10) , color=YELLOW , stroke_width=4)
        range_line = Line(mini_axes.c2p(0 , -1) , mini_axes.c2p(0 , 10) , color=YELLOW , stroke_width=4)
        

        mini_axes_group = VGroup(mini_axes[0] , mini_axes[1] , mini_axes_labels[0] , mini_axes_labels[1] , mini_axes_boundary , mini_axes_curve , range_line , range_line1)
        mini_axes_group = myScale(mini_axes_group, 0.5)
        mini_axes_group.to_edge(LEFT).shift(LEFT * 0.3)
        mini_axes_group.remove(mini_axes_curve , range_line , range_line1)

        example_function = MathTex(r"f(" , r"x" , r") = " , r"x" , r"^2" , r"- 1", color=OUTPUT_COLOR).scale(0.75).shift(RIGHT * 0.3)
        example_function[1].set_color(INPUT_COLOR)
        example_function[3].set_color(INPUT_COLOR)

        domain_in_interval_notation = MathTex(r"\text{Domain: }" , r"\left(-\infty , \infty\right)" , color=BLUE).scale(0.65).next_to(example_function , DOWN).align_to(example_function , LEFT)
        domain_in_interval_notation[1].set_color(YELLOW)

        range_in_interval_notation = MathTex(r"\text{Range: }" , r"\left[-1 , \infty\right)" , color=BLUE).scale(0.65).next_to(domain_in_interval_notation , DOWN).align_to(domain_in_interval_notation , LEFT)
        range_in_interval_notation[1].set_color(YELLOW)

        self.add(domain_and_range_text , range_description , mini_axes_group)
        self.play(Write(example_function) , Create(mini_axes_curve))
        self.play(Write(domain_in_interval_notation))
        self.play(Create(range_line1))
        self.play(Circumscribe(example_function[5] , stroke_width=2))
        self.play(ReplacementTransform(range_line1 , range_line))
        self.play(Write(range_in_interval_notation))
        self.wait()
        self.play(FadeOut(example_function , domain_in_interval_notation , range_in_interval_notation , mini_axes_curve , range_line))
        self.wait()


class Scene14(Scene):
    def construct(self):
        domain_and_range_text = Text("Domain and Range", color=PROCESS_COLOR).scale(0.67).to_corner(UL)
        range_description = Tex(r"\begin{center} Range is the set of all numbers \\ that a function can give as output.\end{center}" , color=YELLOW , stroke_color=YELLOW).scale(0.75 * 0.8).to_corner(UR)

        mini_axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            x_length=10,
            y_length=10,
            axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
            }
        )

        mini_axes2 = Axes(
            x_range=[-18, 18, 1],
            y_range=[-18, 18, 1],
            x_length=10,
            y_length=10,
            axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
                "tick_size": 0.05,
            }

        )

        # mini_axes2[0].set_stroke(width=mini_axes2[0].stroke_width * 0.05)
        # mini_axes2[1].set_stroke(width=mini_axes2[1].stroke_width * 0.05)


        mini_axes_labels = mini_axes.get_axis_labels(
            Tex("x", stroke_color=INPUT_COLOR, color=INPUT_COLOR).scale(0.5), Text("y", stroke_color=OUTPUT_COLOR, color=OUTPUT_COLOR).scale(0.4)
        )

        mini_axes_labels[0].shift(LEFT * 0.5)
        mini_axes_labels[1].shift(UP)

        mini_axes_boundary = Rectangle(width=10.5, height=10.5, color=WHITE, stroke_width=2)

        mini_axes_curve = mini_axes.plot(lambda x : sqrt(16-(x*x)) , [-4 , 4] , color=OUTPUT_COLOR , stroke_width = 2)
        mini_axes_curve2 = mini_axes2.plot(lambda x : sqrt(16-(x*x)) , [-4 , 4] , color=OUTPUT_COLOR , stroke_width = 2)

        
        range_line1 = Line(mini_axes.c2p(0 , 0) , mini_axes.c2p(0 , 10) , color=YELLOW , stroke_width=4)
        range_line2 = Line(mini_axes.c2p(0 , 0) , mini_axes.c2p(0 , -10) , color=YELLOW , stroke_width=4)
        range_line3 = Line(mini_axes.c2p(0 , 10) , mini_axes.c2p(0 , -10) , color=YELLOW , stroke_width=4)
        range_line4 = Line(mini_axes2.c2p(0 , 16) , mini_axes2.c2p(0 , -18) , color=YELLOW , stroke_width=3)
        range_line5 = Line(mini_axes2.c2p(0 , 16) , mini_axes2.c2p(0 , 0) , color=YELLOW , stroke_width=3)
        range_line = Line(mini_axes2.c2p(0 , 4) , mini_axes2.c2p(0 , 0) , color=YELLOW , stroke_width=3)
        range_line_real = Line(mini_axes.c2p(0 , 4) , mini_axes.c2p(0 , 0) , color=YELLOW , stroke_width=4)

        mini_axes_group = VGroup(mini_axes[0] , mini_axes[1] , mini_axes_labels[0] , mini_axes_labels[1] , mini_axes_boundary , mini_axes_curve , range_line , range_line_real , range_line1 , range_line2 , range_line3 , range_line4 , range_line5 , mini_axes2[0] , mini_axes2[1] , mini_axes_curve2)
        mini_axes_group = myScale(mini_axes_group, 0.5)
        mini_axes_group.to_edge(LEFT).shift(LEFT * 0.3)
        mini_axes_group.remove(mini_axes_curve , range_line , range_line1 , range_line2 , range_line3 , range_line4 , range_line5 , mini_axes2[0] , mini_axes2[1] , mini_axes_curve2 , range_line_real)

        example_function = MathTex(r"f(" , r"x" , r") = \sqrt{16-" , r"x" , r"^2}" , color=OUTPUT_COLOR).scale(0.75).shift(RIGHT * 0.3)
        example_function[1].set_color(INPUT_COLOR)
        example_function[3].set_color(INPUT_COLOR)

        range_in_interval_notation = MathTex(r"\text{Range: }" , r"\left[0 , 4\right]" , color=BLUE).scale(0.65).next_to(example_function , DOWN).align_to(example_function , LEFT)
        range_in_interval_notation[1].set_color(YELLOW)

        range_line3.z_index = 100
        range_line4.z_index = 100
        range_line5.z_index = 100
        range_line.z_index = 100
        range_line_real.z_index = 100
        # mini_axes.z_index = 99
        # mini_axes_curve.z_index = 99

        sixteen = MathTex(r"16").scale(0.27).move_to(mini_axes2.c2p(-1 , 16))
        

        self.add(domain_and_range_text , range_description , mini_axes_group)
        self.play(Write(example_function))
        self.play(Create(mini_axes_curve))
        self.play(Circumscribe(example_function[3:] , Circle , stroke_width=2))
        self.play(Create(range_line1))
        self.play(Indicate(VGroup(example_function[2][-1] , example_function[3:])))
        self.play(ReplacementTransform(range_line1 , range_line2))
        self.play(ReplacementTransform(range_line2 , range_line3))

        self.play(ReplacementTransform(mini_axes , mini_axes2) , ReplacementTransform(mini_axes_curve , mini_axes_curve2) , ReplacementTransform(range_line3 , range_line4) , FadeIn(sixteen , shift=DOWN))


        mini_axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            x_length=10,
            y_length=10,
            axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
            }
        )
        mini_axes_curve = mini_axes.plot(lambda x : sqrt(16-(x*x)) , [-4 , 4] , color=OUTPUT_COLOR , stroke_width = 2)

        group2 = VGroup(mini_axes[0] , mini_axes[1] , mini_axes_curve)
        group2 = myScale(group2 , 0.5)
        group2.move_to(mini_axes_group)


        self.play(Wiggle(VGroup(example_function[2][-3:] , example_function[3 : ])))
        self.play(ReplacementTransform(range_line4 , range_line5))
        self.play(ReplacementTransform(range_line5 , range_line))
        self.play(Transform(mini_axes2 , mini_axes) , Transform(mini_axes_curve2 , mini_axes_curve) , ReplacementTransform(range_line , range_line_real) , FadeOut(sixteen , shift=UP))
        self.play(Write(range_in_interval_notation))

        self.wait()

