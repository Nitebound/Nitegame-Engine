from src.nitegame.core import *
from src.nitegame.features import *
from pathlib import Path

font_dir = Path("assets/fonts")

display = PGDisplay()
running = True

font_label = UILabel("Hello to the GUI world!")
font_label.set_ttf_font(font_dir / "astutelight.ttf", 20)

name_label = UILabel("Zachery", 30, COLORS["red"])
name_label.set_sys_font("Times New Roman")
name_label.font_color = COLORS["blue"]

site_link = UILink("Nitebound Games")

while running:
    events = pg.event.get()
    for event in events:
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    # UPDATE

    # DRAW
    display.clear()
    font_label.draw(display.surface, (display.get_width()/2, display.get_height()/2), True)
    site_link.draw(display.surface, (display.get_width()/2, 0), True)
    name_label.draw(display.surface, (display.get_width()/2, 100), True)

    display.update()
