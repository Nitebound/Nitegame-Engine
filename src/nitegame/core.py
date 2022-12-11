import pygame as pg
from pygame import Vector2, Rect
from pygame.locals import *
from math import cos, sin, radians
from .codekit import rgb_to_hex
""" Initialize Sub-Systems """

#from pygame.constants import *

# Define some constants
DEBUG_MODE = False
DEFAULT_DISPLAY_SIZE = 1600, 900
COLORS = pg.colordict.THECOLORS


""" 
Define the methods needed to handle most lower level engine features including loading assets, and handling player
input.
"""


def init():
    pg.init()
    pg.font.init()
    pg.joystick.init()
    pg.mixer.init()


def get_events():
    return pg.event.get()


def get_mouse_pos():
    return pg.mouse.get_pos()


def get_keys_pressed():
    return pg.key.get_pressed()


def get_mouse_pressed():
    return pg.mouse.get_pressed(3)


def load_image(fpath, convert=False):
    return pg.image.load(fpath)


def surface_to_surfarray(surface):
    return pg.surfarray.pixels2d(surface.copy())


def surfarray_to_surface(surf_array):
    return pg.surfarray.make_surface(surf_array)


def load_spritesheet(fpath, scale=1, smooth_scaling=False):
    sprite_sheet = load_image(fpath)
    pixel_array = surface_to_surfarray(sprite_sheet)

    vertical_lines = []
    horizontal_lines = []
    border_color_hex = 4294902014

    # Detect horizontal and vertical lines and store their end points in their respective lists.
    # for each horizontal line, check if either end pixel matches an end pixel of a vertical line.
    # if so the length of the horizontal and vertical lines is equivalent to the width and height of that border.
    # Technically, only the top and left edges of each rect need to be detected to find the size of the border.

    # This method of detecting sprite borders may need optimization, but for now it works perfect!
    # Get horizontal border edges.
    for y in range(sprite_sheet.get_height()):
        horizontal_pixels = []
        for x in range(sprite_sheet.get_width()):
            if pixel_array[x, y] == border_color_hex:
                horizontal_pixels.append((x, y))
            else:
                if horizontal_pixels:
                    line = [horizontal_pixels[0], horizontal_pixels[-1]]
                    if not line[0] == line[1]:
                        horizontal_lines.append(line)
                    horizontal_pixels = []

    # Get vertical border edges.
    for x in range(sprite_sheet.get_width()):
        vertical_pixels = []

        for y in range(sprite_sheet.get_height()):
            if pixel_array[x, y] == border_color_hex:
                vertical_pixels.append((x, y))
            else:
                if vertical_pixels:
                    line = [vertical_pixels[0], vertical_pixels[-1]]
                    if not line[0] == line[1]:
                        vertical_lines.append(line)
                    vertical_pixels = []

    border_rects = []
    # Finally we generate the border rects, and append them to a list.
    for hindex in range(len(horizontal_lines)):
        for vindex in range(0, len(vertical_lines)):
            vline = vertical_lines[vindex]
            for point in vline:
                hline = horizontal_lines[hindex]
                if point == hline[0]:
                    rect = Rect(point[0] + 1, point[1] + 1, hline[1][0] - hline[0][0] - 1,
                                     vline[1][1] - vline[0][1] - 1)
                    border_rects.append(rect)
                break

    sprite_surfaces = []
    for rect in border_rects:
        sprite = sprite_sheet.subsurface(rect)
        if smooth_scaling:
            sprite = pg.transform.smoothscale(sprite, (sprite.get_width() * scale, sprite.get_height() * scale))

        else:
            sprite = pg.transform.scale(sprite, (sprite.get_width() * scale, sprite.get_height() * scale))
        sprite_surfaces.append(sprite)

    return sprite_surfaces


def load_sfx(fpath):
    return pg.mixer.Sound(fpath)


def load_music(fpath):
    return pg.mixer.music.load(fpath)


""" Define Core Classes """


class ColorData(Color):
    def __init__(self, r=0, g=0, b=0, a=255):
        super().__init__(r, g, b, a)

    def get_hex(self):
        return rgb_to_hex((self.r, self.g, self.b, self.a))


class Display:
    def __init__(self, size=DEFAULT_DISPLAY_SIZE, caption="Display", flags=0):
        self.surface = pg.display.set_mode(size, flags)
        self._size = size
        self._caption = caption
        self.clock = pg.time.Clock()
        self.frame_rate = 120
        self.dt = 1
        self.flags = flags
        pg.display.set_caption(caption)

    def get_driver(self):
        return pg.display.get_driver()

    def get_wm_info(self):
        return pg.display.get_wm_info()

    def get_info(self):
        return pg.display.Info()

    def get_size(self):
        return self._size

    def get_width(self):
        return self._size[0]

    def get_height(self):
        return self._size[1]

    def get_caption(self):
        return pg.display.get_caption()

    def set_caption(self, caption):
        self._caption = caption
        pg.display.set_caption(caption)

    def set_mode(self, size, flags=0):
        self._size = size
        self.surface = pg.display.set_mode(size, self.flags, vsync=True)

    def clear(self, color=(255, 255, 255, 255)):
         pass

    def blit(self, surface, position):
        pass

    def update(self):
        self.clock.tick(self.frame_rate)


class PGDisplay(Display):
    """ An easy to use Pygame display."""
    def __init__(self, size=DEFAULT_DISPLAY_SIZE, caption="Pygame Display", flags=0):
        super().__init__(size, caption, flags)

    def clear(self, color=(255, 255, 255, 255)):
        self.surface.fill(color)

    def blit(self, surface, position):
        self.surface.blit(surface, position)

    def update(self):
        pg.display.update()
        super().update()


class GLDisplay(Display):
    """ An easy to use OpenGL display."""
    def __init__(self, size=DEFAULT_DISPLAY_SIZE, caption="OpenGL Display", flags=0):
        super().__init__(size, caption, DOUBLEBUF | OPENGL | flags)
        glEnable(GL_DEPTH_TEST)

    def clear(self, color=(255, 255, 255, 255)):
        c = Color(color)
        glClearColor(c.r, c.g, c.b, c.a)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def blit(self, surface, position):
        """
            The blit method for GLDisplay is handled differently than Pygame. Surfaces will likely be treated as
            Textures possibly rendered to some mesh. Study some more OpenGL and come back here to really make progress
            developing this type of Display. I may change the naming of these basic Display methods to better suit the
            hybrid nature of the abstracted Display class, so that minimal to no code changes are necessary to switch
            between a PGDisplay and a GLDisplay.

            At first any rendering of 3D graphics and meshes will only be available on a GLDisplay, but it's possible
            to eventually implement a rudimentary 3D rendering pipeline to use in any case that OpenGL is not available
            or practical. PGDisplay is essentially a software rendering pipeline, while OpenGL implements a much
            more powerful hardware accelerated rendering pipeline. This is a common feature for many graphical
            applications, so it will likely be useful in some cases.
        """
        pass

    def draw_cube(self, position=(0, 0, 0), color=(255, 255, 255), size=1, wire=False):
        glColor3f(color[0], color[1], color[2])
        glPushMatrix()
        glTranslatef(position[0], position[1], position[2])

        if wire:
            glutWireCube(size)
        else:
            glutSolidCube(size)
        glPopMatrix()

    def draw_sphere(self, position=(0, 0, 0), color=(255, 255, 255), size=1, slices=(30, 30), wire=False):
        glColor3f(color[0], color[1], color[2])
        glPushMatrix()
        glTranslatef(position[0], position[1], position[2])
        # size is 2x the radius, so we half the given size.
        if wire:
            glutWireSphere(size * .5, slices[0], slices[1])
        else:
            glutSolidSphere(size * .5, slices[0], slices[1])
        glPopMatrix()

    def update(self):
        pg.display.flip()
        #super().update()


