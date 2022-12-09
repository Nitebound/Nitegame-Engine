import pygame as pg


class Display:
    def __init__(self, size=(640, 480), caption="Canvas", flags=0):
        self.surface = pg.display.set_mode(size, flags)
        pg.display.set_caption(caption)
        self.frame_clock = pg.time.Clock()
        self.frame_rate = 90
        self.pixel_size = 1
        self.show_fps = False
        self.dt = 1

    def set_caption(self, caption):
        pg.display.set_caption(caption)

    def get_caption(self):
        return pg.display.get_caption()

    def fill(self, color=(255, 255, 255), rect=None):
        self.surface.fill(color, rect)

    def update(self):
        self.dt = self.frame_clock.tick(self.frame_rate)
        pg.display.update()
