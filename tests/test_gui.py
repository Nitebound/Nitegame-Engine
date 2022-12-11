from src.nitegame.core import *
from src.nitegame.core import COLORS
from src.nitegame.features import *
from pathlib import Path

font_dir = Path("assets/fonts")

display = PGDisplay((1024, 768), "Nitegame Engine GUI Testing")
running = True

my_button = UIButton("File", font_size=25)

# This is a test to see how fast I can go back and forth between devices while making changes to this project
while running:
    events = get_events()
    mouse_pos = get_mouse_pos()

    for event in events:
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_k:
                core.DEBUG_MODE = not core.DEBUG_MODE

    my_button.on_event(events, mouse_pos)

    # UPDATE

    # DRAW
    display.clear()

    core.pg.draw.rect(display.surface, (200, 200, 200), (0, 0, display.get_width(), 28))
    my_button.on_draw(display.surface, (0, 0))

    display.update()
