""" UI Features """
import pygame as pg
from .core import COLORS

pg.font.init()
DEFAULT_FONT = "Times New Roman"


class UILabel:
    def __init__(self, text, font_size=80, font_color=COLORS["black"], bg_color=None):
        self.font = pg.font.SysFont(DEFAULT_FONT, font_size)
        self._font_size = font_size
        self._font_color = font_color
        self._bg_color = bg_color
        self._text = text
        self.surface = self.font.render(self._text, True, self._font_color, self._bg_color)
        self._font_path = None

    def set_sys_font(self, font_name=None, font_size=None):
        if not font_size:
            font_size = self._font_size
        else:
            self._font_size = font_size

        self.font = pg.font.SysFont(font_name, font_size)
        self.surface = self.font.render(self.text, True, self._font_color, self._bg_color)

    def set_ttf_font(self, font_path=None, font_size=None):
        if not font_path:
            font_path = self._font_path
        else:
            self._font_path = font_path

        if not font_size:
            font_size = self._font_size
        else:
            self._font_size = font_size

        self.font = pg.font.Font(font_path, font_size)
        self.surface = self.font.render(self.text, True, self._font_color, self._bg_color)

    def set_bold(self, value=True):
        self.font.set_bold(value)
        self.surface = self.font.render(self._text, True, self._font_color, self._bg_color)

    def set_underline(self, value=True):
        self.font.set_underline(value)
        self.surface = self.font.render(self._text, True, self._font_color, self._bg_color)

    @property
    def font_color(self, color):
        self._font_color = color
        self.surface = self.font.render(self.text, True, self._font_color, self._bg_color)

    @font_color.getter
    def font_color(self):
        return self._font_color

    @font_color.setter
    def font_color(self, color):
        self._font_color = color
        self.surface = self.font.render(self.text, True, self._font_color, self._bg_color)

    @property
    def text(self, value):
        self._text = value
        self.surface = self.font.render(self._text, True, self._font_color, None)

    @text.getter
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.surface = self.font.render(self._text, True, self._font_color, COLORS["black"])
