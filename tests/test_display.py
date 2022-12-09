from src.core import Display
import pygame as pg

display = Display()
running = True

while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    # UPDATE


    # DRAW
    display.fill()
    pg.draw.rect(display.surface, (0, 0, 0), (10, 10, 200, 200))
    display.update()
