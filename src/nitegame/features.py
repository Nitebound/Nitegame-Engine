""" UI Features """
from . import core
from math import cos, sin, radians, degrees, atan2
core.pg.font.init()
DEFAULT_FONT = "Times New Roman"


class Component:
    current_cid = 0

    def __init__(self):
        # Each component will link to the parent GameObject for easy reference and access.
        self.cid = Component.current_cid
        Component.current_cid += 1
        self.type = None

    def on_init(self):
        pass

    def on_event(self, events, mouse_pos):
        pass

    def on_update(self, dt):
        pass

    def on_draw(self, dest, offset=(0, 0)):
        pass


class Transform(Component):
    def __init__(self, position=(0, 0), rotation=0):
        super().__init__()
        self.position = core.Vector2(position)
        self.local_position = core.Vector2(0, 0)
        self.rotation = rotation
        self.local_rotation = 0
        self.scale = 1
        self.local_scale = 1

        self.old_position = self.position
        self.old_rotation = self.rotation
        self.old_scale = self.scale
        self._has_changed = False

    def translate(self, translation, relative_to=None):
        pass


class GameObject:
    current_oid = 0

    def __init__(self, name, position=(0, 0), rotation=0, parent=None, surface=None):
        self.oid = GameObject.current_oid
        GameObject.current_oid += 1
        self.name = name

        self.parent = parent
        self.transform = Transform(position, rotation)

        self.components = [self.transform]

        # If the object has a parent we need to calculate the initial local offset between the parent and the new object
        if self.parent:
            self.transform.local_position = self.transform.position
            self.d = self.parent.transform.position.distance_to(self.transform.local_position)

        bound_size = (32, 32)
        self.rect = core.Rect(self.transform.position.x - bound_size[0]*2,
                         self.transform.position.y - bound_size[1]*2, bound_size[0], bound_size[1])

        if surface:
            self.surface = surface
            bound_size = self.surface.get_size()
            self.rect = core.Rect(self.transform.position.x - bound_size[0] * 2,
                             self.transform.position.y - bound_size[1] * 2, bound_size[0], bound_size[1])
        else:
            self.surface = core.pg.Surface(self.rect.size)

        self.scaled_surface = self.surface.copy()
        self.transformed_surface = self.surface.copy()

    def on_init(self):
        for component in self.components:
            component.on_init()

    def on_event(self, events, mouse_pos):
        for component in self.components:
            component.on_event(events, mouse_pos)

    def on_update(self, dt):
        for component in self.components:
            component.on_update(dt)

        if self.parent:
            if self.parent.transform.old_position != self.parent.transform.position:
                self.d = self.parent.transform.position.distance_to(self.transform.local_position)

            self.transform.rotation = self.parent.transform.rotation + self.transform.local_rotation

            # # TEMPORARY
            # # END TEMPORARY

            r = -radians(self.parent.transform.rotation)
            ox = self.d * cos(r)
            oy = self.d * sin(r)

            self.transform.position = self.parent.transform.position + (ox, oy)

        # Any time a change has been made to the transform, other than positional ones, will require both scaling
        # and rotation to be re-applied
        # Check if the transform has changed in scale, position, or rotation, and if so update the object surface.

        # Position
        if self.transform.position != self.transform.old_position:
            self.transform.old_position = self.transform.position

        # Rotation and Scale
        if (self.transform.old_scale != self.transform.scale) or (self.transform.old_rotation != self.transform.rotation):
            # Scale
            if self.transform.old_scale != self.transform.scale:
                if self.transform.scale < .1:
                    self.transform.scale = .1
                self.transform.old_scale = self.transform.scale

            self.scaled_surface = core.pg.transform.scale(self.surface, (self.surface.get_width() * self.transform.scale,
                                                                    self.surface.get_height() * self.transform.scale))

            # Rotate
            if self.transform.old_rotation != self.transform.rotation:
                self.transform.old_rotation = self.transform.rotation

            self.transformed_surface = core.pg.transform.rotate(self.scaled_surface, self.transform.rotation)
            self.transform.old_rotation = self.transform.rotation

        # Update object's rect
        self.rect = core.Rect(self.transform.position.x - self.transformed_surface.get_width() * 2,
                         self.transform.position.y - self.transformed_surface.get_height() * 2,
                         self.transformed_surface.get_width(), self.transformed_surface.get_height())

        self.rect.center = self.transform.position

    def on_draw(self, dest, offset=(0, 0)):
        for component in self.components:
            component.on_draw(dest, offset)

        # If the object has a parent, draw it relative to the parent's transform.
        # Otherwise, just draw the object at its global position.
        # Or should all objects simply be placed using global coordinates, and then we can apply the relative offset.

        dest.blit(self.transformed_surface, self.rect.center - core.Vector2(self.rect.w/2, self.rect.h/2))
        #pg.draw.rect(dest, (255, 0, 0), self.rect, 1)

        if core.DEBUG_MODE:
            if self.parent:
                pg.draw.line(dest, (0, 0, 0), self.transform.position, self.parent.transform.position)
                pg.draw.circle(dest, (0, 0, 255), self.transform.position, 3)


class UIElement:
    def __init__(self):
        self.surface = core.pg.Surface((32, 32), core.SRCALPHA)
        self.rect = core.Rect(0, 0, self.surface.get_width(), self.surface.get_height())

    def on_event(self, events, mouse_pos):
        pass

    def on_update(self, dt):
        pass

    def on_draw(self, dest, position):
        pass


class UILabel(UIElement):
    def __init__(self, text, font_size=20, font_color=(0, 0, 0), bg_color=None):
        super().__init__()
        self._font_size = font_size
        self._font_color = font_color
        self._bg_color = bg_color
        self._text = text
        self._font_path = None

        self.font = core.pg.font.SysFont(DEFAULT_FONT, font_size)
        self.surface = self.font.render(self._text, True, self._font_color, self._bg_color)
        self.rect = core.Rect(0, 0, self.surface.get_width(), self.surface.get_height())

    def set_sys_font(self, font_name=None, font_size=None):
        if not font_size:
            font_size = self._font_size
        else:
            self._font_size = font_size

        self.font = core.pg.font.SysFont(font_name, font_size)
        self.surface = self.font.render(self.text, True, self._font_color, self._bg_color)
        self.rect = core.Rect(self.rect.x, self.rect.y, self.surface.get_width(), self.surface.get_height())

    def set_ttf_font(self, font_path=None, font_size=None):
        if not font_path:
            font_path = self._font_path
        else:
            self._font_path = font_path

        if not font_size:
            font_size = self._font_size
        else:
            self._font_size = font_size

        self.font = core.pg.font.Font(font_path, font_size)
        self.surface = self.font.render(self.text, True, self._font_color, self._bg_color)
        self.rect = core.Rect(self.rect.x, self.rect.y, self.surface.get_width(), self.surface.get_height())

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
        self.rect = core.Rect(self.rect.x, self.rect.y, self.surface.get_width(), self.surface.get_height())

    @text.getter
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.surface = self.font.render(self._text, True, self._font_color, (0, 0, 0))
        self.rect = core.Rect(self.rect.x, self.rect.y, self.surface.get_width(), self.surface.get_height())

    def on_draw(self, dest, position, centerx=False):
        if centerx:
            self.rect = core.Rect(position[0]-self.surface.get_width()/2, position[1], self.surface.get_width(), self.surface.get_height())
            dest.blit(self.surface, (position[0]-self.surface.get_width()/2, position[1]))
        else:
            self.rect = core.Rect(position[0], position[1], self.surface.get_width(), self.surface.get_height())
            dest.blit(self.surface, position)

        if core.DEBUG_MODE:
            core.pg.draw.rect(dest, (255, 0, 0), self.rect, 1)


class UILink(UILabel):
    def __init__(self, text, font_size=20, font_color=(0, 0, 0), bg_color=None, command=None, cmd_args=()):
        super().__init__(text, font_size, font_color, bg_color)
        self.mouseover = False
        self.clicked = False
        self.right_clicked = False
        self.holding = False
        self.command = command
        self.args = cmd_args

    def on_event(self, events, mouse_pos):
        self.mouseover = False
        self.clicked = False
        self.right_clicked = False

        if self.rect.collidepoint(mouse_pos):
            self.mouseover = True

        for event in events:
            if event.type == core.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.mouseover:
                        self.holding = True

            if event.type == core.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.mouseover:
                        if self.holding:
                            self.clicked = True
                            if self.command:
                                self.command(self.args)

                    self.holding = False

                elif event.button == 3:
                    if self.mouseover:
                        self.right_clicked = True

        if core.pg.mouse.get_focused():
            if self.mouseover:
                self.set_underline(True)
            else:
                self.set_underline(False)

            if self.holding:
                self.font_color = (0, 0, 255)
            else:
                self.font_color = (0, 0, 0)
        else:
            self.set_underline(False)
            self.font_color = (0, 0, 0)


class UIButton(UILink):
    def __init__(self, text, font_size=20, font_color=(0, 0, 0), bg_color=(200, 200, 200), command=None, cmd_args=()):
        super().__init__(text, font_size, font_color, bg_color, command, cmd_args)

    def on_draw(self, dest, position, centerx=False):
        super().on_draw(dest, position, centerx)
        core.pg.draw.rect(dest, (0, 0, 0), self.rect, 1)