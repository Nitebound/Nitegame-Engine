import src.nitegame as ng
from math import radians
ng.init()
display = ng.PGDisplay()
input_manager = ng.InputManager()
input_manager.bind_defaults()

running = True

arc_rotation = 0
dt = 1
while running:
    running = input_manager.update_inputs()

    arc_rotation += .5 * dt
    display.clear()
    ng.draw.circle(display.surface, (0, 0, 0), display.surface.get_rect().center, 100)
    #ng.draw.rect(display.surface, (0, 0, 0), (0, 0, 100, 100))
    ng.draw.circle(display.surface, ng.COLORS["orange"], ng.Rect(0, 0, 100, 100).center, 45)
    ng.draw.circle(display.surface, ng.COLORS["orangered"], ng.Rect(0, 0, 100, 100).center, 15)
    ng.draw.arc(display.surface, ng.COLORS["black"], ng.Rect(0, 0, 100, 100), radians(arc_rotation), radians(90 + arc_rotation), 4)
    ng.draw.arc(display.surface, ng.COLORS["white"], ng.Rect(12, 12, 75, 75), -radians(arc_rotation), -radians(90 + arc_rotation), 3)
    ng.draw.arc(display.surface, ng.COLORS["white"], ng.Rect(25, 25, 50, 50), radians(arc_rotation), radians(180 + arc_rotation), 2)
    dt = display.update()
