import src.nitegame as ng

ng.init()

display = ng.PGDisplay()
running = True

texture = ng.load_image("../assets/terrainmap1.png")
tp = ng.codekit.generate_textured_polygon([(0, 0), (100, 0), (150, 100), (150, 200), (100, 300), (0, 300)], texture)
im = ng.InputManager()

while running:
    running = im.update_inputs()
    if im.inputs["QuickExit"].released:
        running = False

    # UPDATE

    # DRAW
    display.clear()
    display.blit(tp, (100, 100))
    display.update()
