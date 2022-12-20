from src.nitegame.core import *
from src.nitegame.core import COLORS
from src.nitegame.features import *
from pathlib import Path
from random import randint, seed


class UIPanel(UIElement):
    def __init__(self, rect):
        super().__init__()
        self.rect = Rect(rect)

    def on_draw(self, dest):
        pg.draw.rect(dest, (200, 200, 200), self.rect)
        pg.draw.rect(dest, (0, 0, 0), self.rect, 1)


def exit_app():
    global running
    running = False


def create_object():
    global objects, display
    position = (randint(0, display.get_width()), randint(0, display.get_height()))
    obj = GameObject("Empty GameObject", position)
    objects.append(obj)


font_dir = Path("../assets/fonts")

display = PGDisplay((1920, 1080), "Nitegame Engine GUI Testing")
running = True

# First we initialize all the drop menus which we will link to buttons on the menu bar.
file_menu = UIDropMenu()
file_menu.add_option("New")
file_menu.add_option("Open")
file_menu.add_option("Save")
file_menu.add_option("Save As")
file_menu.add_option("Exit", exit_app)

edit_menu = UIDropMenu()
edit_menu.add_option("Cut")
edit_menu.add_option("Copy")
edit_menu.add_option("Paste")
edit_menu.add_option("Delete")

view_menu = UIDropMenu()
view_menu.add_option("Show Grid: True")
view_menu.add_option("Focus Mode")

create_menu = UIDropMenu()
create_menu.add_option("Empty GameObject")
create_menu.add_option("Circle", create_object)
create_menu.add_option("Rect")
create_menu.add_option("Polygon")
create_menu.add_option("Point Light")
create_menu.add_option("Area Light")
create_menu.add_option("Global Light")

# After initializing all the menus, we create the menu bar buttons and link them to their respective drop menus.
menubar = UIMenuBar()
menubar.add_option("File", file_menu)
menubar.add_option("Edit", edit_menu)
menubar.add_option("View", view_menu)
menubar.add_option("Create", create_menu)

# Here is a test for a drop menu that opens when the user right clicks somewhere in the view area.
cursor_menu = UIDropMenu()
cursor_menu.add_option("Add")

message_box = UIPanel((display.get_width()/2-100, display.get_height()/2-100, 200, 200))

objects = []

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

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 3:
                if not menubar.rect.collidepoint(mouse_pos):
                    cursor_menu.rect.topleft = core.Vector2(mouse_pos)
                    cursor_menu.show()
                else:
                    cursor_menu.hide()

            elif event.button == 1:
                if not cursor_menu.rect.collidepoint(mouse_pos):
                    cursor_menu.hide()

    menubar.on_event(events, mouse_pos)
    cursor_menu.on_event(events, mouse_pos)
    message_box.on_event(events, mouse_pos)

    # UPDATE
    menubar.on_update(display.dt)
    cursor_menu.on_update(display.dt)
    message_box.on_update(display.dt)

    # DRAW
    display.clear()

    for obj in objects:
        obj.on_draw(display.surface)

    menubar.on_draw(display.surface)
    cursor_menu.on_draw(display.surface)
    message_box.on_draw(display.surface)

    display.update()
