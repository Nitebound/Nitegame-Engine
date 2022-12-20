from src.nitegame.codekit import perlin_array
from src.nitegame.core import *
from src.nitegame.core import COLORS
from src.nitegame.features import *
from random import randint
import numpy as np


def generate_terrain(size):
    noise = perlin_array(size)
    pixel_data = [[(0, 0, 0) for y in range(size[1])] for x in range(size[0])]

    for y in range(size[1]):
        for x in range(size[0]):
            if noise[x][y] > .8:
                pixel_data[x][y] = (255, 255, 255)
            elif noise[x][y] > .77:
                pixel_data[x][y] = COLORS["gray"][:-1]
            elif noise[x][y] > .65:
                pixel_data[x][y] = COLORS["antiquewhite4"][:-1]
            elif noise[x][y] > .5:
                pixel_data[x][y] = (0, 100, 0)
            elif noise[x][y] > .45:
                pixel_data[x][y] = COLORS["burlywood1"][:-1]
            elif noise[x][y] > .4:
                pixel_data[x][y] = COLORS["cornflowerblue"][:-1]

            else:
                pixel_data[x][y] = COLORS["dodgerblue4"][:-1]

    pixel_data = np.array(pixel_data)
    return pg.surfarray.make_surface(pixel_data)


display = PGDisplay()
running = True

noise_size = display.get_size()
hmcolor = COLORS["white"]
img = generate_terrain(noise_size)

while running:
    events = get_events()
    mouse_pos = get_mouse_pos()

    for event in events:
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                img = generate_terrain(noise_size)

            elif event.key == K_s:
                pg.image.save(img, "assets/terrainmap1.png")

    display.clear()
    display.blit(img, (0, 0))
    display.update()
