from fractions import Fraction
import pygame as pg
from math import inf, cos, sin, atan2, radians, degrees, pi
from .features import UILabel
from random import randint
from noise import pnoise2
import numpy as np


def perlin_array(shape=(200, 200),
                 scale=100, octaves=6,
                 persistence=0.5,
                 lacunarity=2.0,
                 seed=None):

    if not seed:
        seed = np.random.randint(0, 100)

    arr = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            arr[i][j] = pnoise2(i / scale,
                                j / scale,
                                octaves=octaves,
                                persistence=persistence,
                                lacunarity=lacunarity,
                                repeatx=1024,
                                repeaty=1024,
                                base=seed)

    max_arr = np.max(arr)
    min_arr = np.min(arr)
    norm_me = lambda x: (x-min_arr)/(max_arr - min_arr)
    norm_me = np.vectorize(norm_me)
    arr = norm_me(arr)
    return arr


def generate_heightmap(size, color=(255, 255, 255)):
    noise = perlin_array(size)
    pixel_data = [[(noise[x][y] * color[0], noise[x][y] * color[1], noise[x][y] * color[2]) for y in range(size[1])] for x in range(size[0])]
    pixel_data = np.array(pixel_data)
    return pg.surfarray.make_surface(pixel_data)


# Define some methods to help with common tasks.
def flatten_list(list_of_lists, flat_list=[]):
    if flat_list == []:
        return flat_list
    else:
        for item in list_of_lists:
            if type(item) == list:
                flatten_list(item)
            else:
                flat_list.append(item)

        return flat_list


def rgb_to_hex(rgb):
    hex = ""
    for value in rgb:
        hex += "%02x" + str(value)
    return hex


def calculate_aspect_ratio(width, height):
    ratio_str = str(Fraction(width, height)).split("/")
    w = int(ratio_str[0])
    h = int(ratio_str[1])
    return w, h


def ccw(a,b,c):
    return (c.y-a.y) * (b.x-a.x) > (b.y-a.y) * (c.x-a.x)


# Return true if line segments AB and CD intersect
def intersect(a, b, c, d):
    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)


def point_in_polygon(pt, poly):
    result = False
    for i in range(len(poly)-1):
        if intersect(pg.Vector2(poly[i].x, poly[i].y), pg.Vector2(poly[i+1].x, poly[i+1].y), pg.Vector2(pt.x, pt.y), pg.Vector2(inf, pt.y)):
            result = not result
    if intersect(pg.Vector2(poly[-1].x, poly[-1].y), pg.Vector2(poly[0].x, poly[0].y), pg.Vector2(pt.x, pt.y), pg.Vector2(inf, pt.y)):
        result = not result
    return result


def closest_point_on_line(line_p1, line_p2, point):
    # Calculates the nearest point on a line from a given point.
    line_p1 = pg.Vector2(line_p1)
    line_p2 = pg.Vector2(line_p2)
    point = pg.Vector2(point)

    A1 = line_p2.y - line_p1.y
    B1 = line_p1.x - line_p2.x
    C1 = (line_p2.y - line_p1.y) * line_p1.x + (line_p1.x - line_p2.x) * line_p1.y
    C2 = -B1*point.x + A1*point.y
    det = A1*A1 - -B1*B1
    cx = 0
    cy = 0
    if det != 0:
        cx = (A1*C1 - B1*C2)/det
        cy = (A1*C2 - -B1*C1)/det
    else:
        cx = point.x
        cy = point.y
    return pg.Vector2(cx, cy)


def render_grid(dest, cols, rows, offset=(0, 0), unit_size=16, line_color=(0, 0, 0)):
    w = cols * unit_size
    h = rows * unit_size

    for y in range(rows):
        pg.draw.line(dest, line_color, (offset[0], offset[1] + y*unit_size),
                     (offset[0] + cols*unit_size, offset[1] + y*unit_size))

    for x in range(cols):
        pg.draw.line(dest, line_color, (offset[0] + x*unit_size, offset[1]),
                     (offset[0] + x*unit_size, offset[1] + rows*unit_size))

    pg.draw.rect(dest, line_color, (0, 0, w, h), 1)


class Timer:
    def __init__(self):
        self.start_time = 0
        self.elapsed_time = 0
        self.started = False

    def start(self):
        self.started = True
        self.start_time = time.get_ticks()

    def stop(self):
        self.started = False
        self.elapsed_time = 0

    def update(self):
        if self.started:
            self.elapsed_time = pg.time.get_ticks() - self.start_time


def draw_tooltip(dest, text, position):
    tooltip_label = UILabel(text)
    tooltip_label.font_size = 12
    border_rect = tooltip_label.surface.get_rect()
    border_rect.x = position[0]
    border_rect.y = position[1]
    pg.draw.rect(dest, (110, 110, 110), border_rect)
    tooltip_label.draw(dest, position)


def render_outline(dest, surface, position, angle=0, color=(255, 255, 255, 255), border_size=1):
    surf_mask = pg.mask.from_surface(surface)
    mask_outline = surf_mask.outline()

    surf = pg.Surface(surface.get_size(), pg.SRCALPHA)
    for point in mask_outline:
        pg.draw.rect(surf, color, (point[0], point[1], border_size, border_size))

    surf = pg.transform.rotate(surf, angle)
    px = position[0]
    py = position[1]
    dest.blit(surf, (px, py))


def smooth_turn(goal_angle, current_angle, turn_speed, dt):
    diff = (goal_angle-current_angle+pi) % (2*pi) - pi
    return current_angle + (diff*turn_speed) * dt


def get_distance(point1, point2):
    point1 = pg.Vector2(point1)
    return point1.distance_to(point2)


def wrap_string(text, max_chars):
    lines = []
    while len(text) > 0:
        count = 0
        text_len = len(text)

        if text_len >= max_chars+1:
            cindex = max_chars - count
            char = text[cindex]

            while char != " ":
                cindex = max_chars - count
                char = text[cindex]
                count += 1

            lines.append(text[0:cindex + 1])
            text = text[(cindex + 1):]
        else:
            lines.append(text)
            text = ""

    return lines


def clamp(value, min_val, max_val):
    if value < min_val: value = min_val
    elif value > max_val: value = max_val
    return value


def lerp(a, b, t):
    return a + (b-a) * t


def randompoint(x_limits, y_limits):
    return randint(x_limits[0], x_limits[1]), randint(y_limits[0], y_limits[1])


def pad_rect(rect, h_pad, v_pad):
    rect = pg.Rect(rect)
    rect.x -= h_pad
    rect.y -= v_pad
    rect.w += h_pad*2
    rect.h += v_pad*2
    return rect


class DataGrid:
    """A grid of data for any purpose."""
    def __init__(self, size):
        self.size = size
        self.data = [0 for x in range(self.size[0]*self.size[1])]
        self.rect = pg.Rect(0, 0, size[0], size[1])

    def load_data(self, map_data):
        # Load in map data using a 2D list of values
        self.size = (len(map_data[0]), len(map_data))

        self.data = [0 for x in range(self.size[0]*self.size[1])]

        for y in range(self.size[1]):
            for x in range(self.size[0]):
                self.set_at((x, y), map_data[y][x])

    def get_area(self, rect, filled=True):
        self.rect = pg.Rect(rect)
        area = [[0 for _ in range(self.rect.h)] for _ in range(self.rect.w)]

        for y in range(0, self.rect.h):
            for x in range(0, self.rect.w):
                area[x][y] = self.get_at((self.rect.x + x, self.rect.y + y))
        return area

    def get_2D_data(self):
        data = []
        for x in range(self.size[0]):
            data.append([])
            for y in range(self.size[1]):
                data[-1].append(self.get_at((x, y)))
        return data

    def get_at(self, coord):
        return self.data[self.size[0] * coord[1] + coord[0]]

    def set_at(self, coord, value):
        i = self.size[0] * coord[1] + coord[0]
        self.data[i] = value

    def print_data(self):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                print(self.get_at((x, y)), end=' ')
            print()


# Line Intersection
# Calc the gradient 'm' of a line between p1 and p2
def calculate_gradient(p1, p2):
    # Ensure that the line is not vertical
    if (p1[0] != p2[0]):
        m = (p1[1] - p2[1]) / (p1[0] - p2[0])
        return m
    else:
        return None


# Calc the point 'b' where line crosses the Y axis
def calculate_yaxis_intersect(p, m):
    return p[1] - (m * p[0])


# Calc the point where two infinitely long lines (p1 to p2 and p3 to p4) intersect.
# Handle parallel lines and vertical lines (the later has infinate 'm').
# Returns a point tuple of points like this ((x,y),...)  or None
# In non parallel cases the tuple will contain just one point.
# For parallel lines that lay on top of one another the tuple will contain
# all four points of the two lines
def get_intersect_point(p1, p2, p3, p4):
    m1 = calculate_gradient(p1, p2)
    m2 = calculate_gradient(p3, p4)

    # See if the the lines are parallel
    if (m1 != m2):
        # Not parallel

        # See if either line is vertical
        if (m1 is not None and m2 is not None):
            # Neither line vertical
            b1 = calculate_yaxis_intersect(p1, m1)
            b2 = calculate_yaxis_intersect(p3, m2)
            x = (b2 - b1) / (m1 - m2)
            y = (m1 * x) + b1
        else:
            # Line 1 is vertical so use line 2's values
            if (m1 is None):
                b2 = calculate_yaxis_intersect(p3, m2)
                x = p1[0]
                y = (m2 * x) + b2
            # Line 2 is vertical so use line 1's values
            elif (m2 is None):
                b1 = calculate_yaxis_intersect(p1, m1)
                x = p3[0]
                y = (m1 * x) + b1
            else:
                assert False

        return ((x, y),)
    else:
        # Parallel lines with same 'b' value must be the same line so they intersect
        # everywhere in this case we return the start and end points of both lines
        # the calculate_intersect_point method will sort out which of these points
        # lays on both line segments
        b1, b2 = None, None  # vertical lines have no b value
        if m1 is not None:
            b1 = calculate_yaxis_intersect(p1, m1)

        if m2 is not None:
            b2 = calculate_yaxis_intersect(p3, m2)

        # If these parallel lines lay on one another
        if b1 == b2:
            return p1, p2, p3, p4
        else:
            return None


def get_tween_values(start, end, frame_count):
    d = end - start
    dx = d/frame_count
    cval = start
    values = []

    for val in range(frame_count):
        cval += dx
        values.append(cval)
    return values


# For line segments (ie not infinitely long lines) the intersect point
# may not lay on both lines.
#
# If the point where two lines intersect is inside both line's bounding
# rectangles then the lines intersect. Returns intersect point if the line
# intesect o None if not
def calculate_intersect_point(p1, p2, p3, p4):
    p = get_intersect_point(p1, p2, p3, p4)

    if p is not None:
        width = p2[0] - p1[0]
        height = p2[1] - p1[1]
        r1 = pg.Rect(p1, (width, height))
        r1.normalize()

        width = p4[0] - p3[0]
        height = p4[1] - p3[1]
        r2 = pg.Rect(p3, (width, height))
        r2.normalize()

        # Ensure both rects have a width and height of at least 'tolerance' else the
        # collidepoint check of the pg.Rect class will fail as it doesn't include the bottom
        # and right hand side 'pixels' of the rectangle
        tolerance = 1
        if r1.width < tolerance:
            r1.width = tolerance

        if r1.height < tolerance:
            r1.height = tolerance

        if r2.width < tolerance:
            r2.width = tolerance

        if r2.height < tolerance:
            r2.height = tolerance

        for point in p:
            try:
                res1 = r1.collidepoint(point)
                res2 = r2.collidepoint(point)
                if res1 and res2:
                    point = [int(pp) for pp in point]
                    return pg.Vector2(point)

            except ValueError:
                # sometimes the value in a point are too large for PyGame's pg.Rect class
                s = "point was invalid  ", point
                print(s)

        # This is the case where the infinitely long lines crossed but
        # the line segments didn't
        return None

    else:
        return None


def line_box_intersect(p1, p2, rect):
    p1, p2 = pg.Vector2(p1), pg.Vector2(p2)
    rect = pg.Rect(rect)
    tl = pg.Vector2(rect.topleft)

    tr = pg.Vector2(rect.topright)

    bl = pg.Vector2(rect.bottomleft)
    br = pg.Vector2(rect.bottomright)
    points_intersected = []

    if p1.x - rect.left < 0:
        # Left
        left = calculate_intersect_point(p1, p2, tl, bl)
        if left:
            points_intersected.append(left)

    elif p1.x - rect.right > 0:
        # Right
        right = calculate_intersect_point(p1, p2, tr, br)
        if right:
            points_intersected.append(right)

    if p1.y - rect.top < 0:
        # Top
        top = calculate_intersect_point(p1, p2, tl, tr)
        if top:
            points_intersected.append(top)

    elif p1.y - rect.bottom > 0:
        # Bottom
        bottom = calculate_intersect_point(p1, p2, bl, br)
        if bottom:
            points_intersected.append(bottom)

    least_id = 0
    least_d = 100000

    for i, point in enumerate(points_intersected):
        d = pg.Vector2(point).distance_to(p1)
        if d < least_d:
            least_d = d
            least_id = i

    if points_intersected:
        return points_intersected[least_id]


def render_gradient_circle(radius, color1=(255, 217, 58, 150), color2=(255, 255, 255, 100)):
    sw, sh = radius*2, radius*2
    surf = pg.Surface((sw, sh), pg.SRCALPHA)

    for r in range(radius):
        rd = r*1.5
        c = [color1[0]+rd, color1[1]+rd, color1[2]+rd, color1[3]-r*1]
        if c[0] <= 0: c[0] = 0
        if c[1] <= 0: c[1] = 0
        if c[2] <= 0: c[2] = 0
        if c[3] <= 0: c[3] = 0

        if c[0] >= 255: c[0] = 255
        if c[1] >= 255: c[1] = 255
        if c[2] >= 255: c[2] = 255
        if c[3] >= 255: c[3] = 255

        pg.draw.circle(surf, c, (sw/2, sh/2), r, 2)
    return surf


def get_radial_point(center, angle, radius):  # angle is in degrees and converted to radians below.
    p2x = center.x + radius * cos(radians(angle))
    p2y = center.y + radius * sin(radians(angle))
    return pg.Vector2(p2x, p2y)


def angle_to(p1, p2):
    return atan2(p2[1] - p1[1], p2[0] - p1[0])


def draw_arrow(dest, start, end, color=(0, 0, 0)):
    pg.draw.line(dest, color, start, end, 2)
    pg.draw.circle(dest, color, end, 3)


def render_tiled_surface(dest, texture_surface):
    for x in range(int(dest.get_width()/32)):
        for y in range(int(dest.get_height()/32)):
            dest.blit(texture_surface, (x * texture_surface.get_width(), y * texture_surface.get_height()))


def get_poly_bounds(points):
    min_x, max_x = (inf, -inf)
    min_y, max_y = (inf, -inf)
    for point in points:
        if point[0] < min_x:
            min_x = point[0]

        elif point[0] > max_x:
            max_x = point[0]

        if point[1] < min_y:
            min_y = point[1]
        elif point[1] > max_y:
            max_y = point[1]

    min_point = pg.Vector2(min_x, min_y)
    max_point = pg.Vector2(max_x, max_y)
    return min_point, max_point


def get_poly_size(points):
    poly_bounds = get_poly_bounds(points)
    pw = poly_bounds[1][0] - poly_bounds[0][0]
    ph = poly_bounds[1][1] - poly_bounds[0][1]
    return abs(pw), abs(ph)


def generate_textured_polygon(points, texture_surface):
    pw, ph = get_poly_size(points)
    poly_surf = pg.Surface((pw+20, ph+20), pg.SRCALPHA)
    poly_surf.fill((255, 255, 255, 255))
    pg.draw.polygon(poly_surf, (255, 0, 0, 0), points)

    textured_surf = pg.Surface(poly_surf.get_size(), pg.SRCALPHA)
    textured_surf.blit(texture_surface, (0, 0))
    textured_surf.blit(poly_surf, (0, 0))
    textured_surf.set_colorkey((255, 255, 255, 255))
    #pg.draw.polygon(textured_surf, (0, 0, 0), points, 3)
    return textured_surf
