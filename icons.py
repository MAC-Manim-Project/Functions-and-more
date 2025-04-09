from manim import *

def machineIcon(letter = "f" , _color=BLUE , letter_color=WHITE):
    center_rectangle = RoundedRectangle(0.25 , width=2 , height = 1.2 , stroke_width = 0 , stroke_color = _color , fill_color = _color , fill_opacity = 1)
    input_area = Polygon([-1 , 0.2 , 0] , [-1.5 , 0.5 , 0] , [-1.5 , -0.5 , 0] , [-1 , -0.2 , 0] , stroke_width = 0 , stroke_color = _color , fill_color = _color , fill_opacity = 1)
    output_area = Polygon([1 , 0.2 , 0] , [1.5 , 0.5 , 0] , [1.5 , -0.5 , 0] , [1 , -0.2 , 0] , stroke_width = 0 , stroke_color = _color , fill_color = _color , fill_opacity = 1)
    logo = MathTex(f"{letter}" , color=letter_color)

    input_area.round_corners([0.05 , 0.05 , 0 , 0])
    output_area.round_corners([0.05 , 0.05 , 0 , 0])
    
    return VGroup(center_rectangle , input_area , output_area , logo)

def screenRectanlge(opacity):
    return Rectangle(BLACK , 10 , 16 , fill_opacity = opacity)


class Scene1(Scene):
    def construct(self):
        # self.add(NumberPlane())
        self.add(machineIcon())