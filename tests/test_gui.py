from src.nitegame.core import *
from src.nitegame.core import COLORS
from src.nitegame.features import *
from pathlib import Path


font_dir = Path("assets/fonts")

display = PGDisplay((1024, 768), "Nitegame Engine GUI Testing")
running = True

file_menu = UIDropMenu()
file_menu.add_option("Open")
file_menu.add_option("Exit", quit)

edit_menu = UIDropMenu()
edit_menu.add_option("Cut")
edit_menu.add_option("Copy")
edit_menu.add_option("Paste")
edit_menu.add_option("Delete")

menubar = UIMenuBar()
menubar.add_option("File", file_menu)
menubar.add_option("Edit", edit_menu)
menubar.add_option("View")
menubar.add_option("Create")


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

    menubar.on_event(events, mouse_pos)

    # UPDATE
    menubar.on_update(display.dt)

    # DRAW
    display.clear()

    menubar.on_draw(display.surface)

    display.update()
