from src.nitegame.core import *
display = PGDisplay()
running = True


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
    
    display.update()
