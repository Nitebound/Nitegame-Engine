from src.nitegame.core import *
from src.nitegame.core import COLORS
from src.nitegame.features import *
from pathlib import Path
from random import randint, seed


class UIPanel(UIElement):
    def __init__(self, title="Panel", rect = (0, 0, 200, 200)):
        super().__init__()
        self.rect = Rect(rect)
        self.handle_height = 18
        self.padding = 0
        self.scrollbar_width = 12

        # Define and initialize panel surfaces
        self.surface = pg.Surface(self.rect.size, SRCALPHA)
        self.surface.fill((0, 0, 0, 255))

        self.content_surface = pg.Surface((self.rect.w - self.padding*3 - self.scrollbar_width, self.rect.h-self.handle_height-self.padding*2), SRCALPHA)

        # Create the title label
        self.title = title
        self.title_label = UILabel(self.title, (3, 2), font_size=int(self.handle_height*.8), font_color=COLORS["black"])

        # Define visual properties
        self.transparency = 255

        handle_color = [200, 200, 200, self.transparency]
        self.handle_color = handle_color

        border_color = COLORS["black"].copy()
        border_color[3] = self.transparency
        self.border_color = border_color

        bgcolor = COLORS["gray"].copy()
        bgcolor[3] = self.transparency
        self.bgcolor = bgcolor

        content_bgcolor = COLORS["white"].copy()
        content_bgcolor[3] = self.transparency
        self.content_bgcolor = content_bgcolor

    def on_draw(self, dest):
        self.surface.fill(self.handle_color)

        # Render the panel's handle and handle border.
        pg.draw.rect(self.surface, self.handle_color, (0, 0, self.rect.w, self.handle_height))
        pg.draw.rect(self.surface, self.border_color, (0, 0, self.rect.w, self.handle_height), 1)

        # Render the panel border.
        pg.draw.rect(self.surface, self.border_color, (0, 0, self.rect.w, self.rect.h), 1)

        self.title_label.on_draw(self.surface, True)
        # Render content to the content surface and blit that surface to the panel's base surface.
        self.content_surface.fill((255, 255, 255, self.transparency))

        self.surface.blit(self.content_surface, (self.padding, self.handle_height + self.padding - 1))
        pg.draw.rect(self.surface, self.border_color, (self.padding, self.handle_height + self.padding - 1, self.rect.w - self.padding*3 - self.scrollbar_width, self.content_surface.get_height()+1), 1)
        dest.blit(self.surface, self.rect.topleft)

def exit_app():
    global running
    running = False

if __name__ == "__main__":
    font_dir = Path("../assets/fonts")

    display = PGDisplay((1920, 1080), "Nitegame Engine GUI Testing")
    running = True

    # First we initialize all the drop menus which we will link to buttons on the menu bar.
    # File Menu Options
    file_menu = UIDropMenu()
    file_menu.add_option("New")
    file_menu.add_option("Open")
    file_menu.add_option("Save")
    file_menu.add_option("Save As")
    file_menu.add_option("Exit", exit_app)

    # Edit Menu Options
    edit_menu = UIDropMenu()
    edit_menu.add_option("Cut")
    edit_menu.add_option("Copy")
    edit_menu.add_option("Paste")
    edit_menu.add_option("Delete")

    # View Menu Options
    view_menu = UIDropMenu()
    view_menu.add_option("Show Grid: True")
    view_menu.add_option("Focus Mode")

    # Create Menu Options
    create_menu = UIDropMenu()
    create_menu.add_option("Empty GameObject")
    create_menu.add_option("Circle")
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
    cursor_menu.add_option("Add", quit)
    cursor_menu.add_option("Print", print, "This option prints this message into the terminal.")

    mbsize = (400, 400)
    message_box = UIPanel("Test Panel", (display.get_width()/2-mbsize[0]/2, display.get_height()/2-mbsize[1]/2, mbsize[0], mbsize[1]))

    # Define inputs
    im = InputManager()
    im.bind_defaults()
    im.create_input("DebugMode", KEYDOWN, K_k)

    while running:
        running = im.update_inputs()
        events = im.events
        mouse_pos = im.mouse_pos

        if im.inputs["QuickExit"].released:
            running = False

        if im.inputs["DebugMode"].released:
            core.DEBUG_MODE = not core.DEBUG_MODE

        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 3:
                    # Show or hide the cursor menu when the user right clicks in the view area.
                    if not menubar.rect.collidepoint(mouse_pos):
                        cursor_menu.rect.topleft = core.Vector2(mouse_pos)
                        cursor_menu.show()
                    else:
                        cursor_menu.hide()

        message_box.on_event(events, mouse_pos)
        cursor_menu.on_event(events, mouse_pos)
        menubar.on_event(events, mouse_pos)

        # UPDATE
        message_box.on_update(display.dt)
        cursor_menu.on_update(display.dt)
        menubar.on_update(display.dt)

        # DRAW
        display.clear((100, 100, 100))

        message_box.on_draw(display.surface)
        cursor_menu.on_draw(display.surface)
        menubar.on_draw(display.surface)

        display.update()
