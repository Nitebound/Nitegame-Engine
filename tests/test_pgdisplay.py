from src.core import *
import pygame as pg

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
    #pg.draw.rect(display.surface, (0, 0, 0), (10, 10, 200, 200))
    display.update()
