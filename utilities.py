from manim import *

def myScale(mobject, factor):
    """Scales both the mobject and its stroke width. Works for individual objects and groups."""
    mobject.scale(factor)  

    if isinstance(mobject, VGroup):
        for submob in mobject:
            if hasattr(submob, "set_stroke"):
                submob.set_stroke(width=submob.stroke_width * factor)

    elif hasattr(mobject, "set_stroke"):
        mobject.set_stroke(width=mobject.stroke_width * factor)
    
    return mobject
