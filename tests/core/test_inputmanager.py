import src.nitegame as ng
from src.nitegame.locals import *

if __name__ == "__main__":
    # Initialize
    ng.init()

    display = ng.PGDisplay()
    running = True

    im = ng.InputManager()
    im.bind_defaults()

    # Main Loop
    while running:
        # Event
        running = im.update_inputs()

        if im.inputs["QuickExit"].released:
            running = False

        # Update

        # Draw
        display.clear()

        display.update()
