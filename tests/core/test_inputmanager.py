import src.nitegame as ng
from src.nitegame.locals import *

if __name__ == "__main__":
    # Initialize
    ng.init()

    display = ng.PGDisplay()
    running = True

    im = ng.InputManager()
    im.bind_defaults()
    im.create_input("Fire", JOYBUTTONDOWN, 1)

    # Main Loop
    while running:
        # Event
        running = im.update_inputs()

        if im.inputs["QuickExit"].released:
            running = False
        if im.inputs["Fire"].pressed:
            print("Fire!")
        # Update

        # Draw
        display.clear()

        display.update()
