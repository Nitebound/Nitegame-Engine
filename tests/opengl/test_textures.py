# from __future__ import division
import pygame
import numpy as np
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLU import *
from OpenGL.arrays import vbo
from src.nitegame.core import load_image, InputManager
from pathlib import Path

# Define useful paths
asset_path = Path("../assets")

pygame.init()
pygame.display.set_mode((600, 400), DOUBLEBUF | OPENGL)

# Generate shaders
vertex_shader = shaders.compileShader(open("../core/shaders/basic_vertex_shader.glsl").read(), GL_VERTEX_SHADER)
fragment_shader = shaders.compileShader(open("../core/shaders/basic_fragment_shader.glsl"), GL_FRAGMENT_SHADER)
shader = shaders.compileProgram(vertex_shader, fragment_shader)

glDeleteShader(vertex_shader)
glDeleteShader(fragment_shader)

# Define Mesh Vertices
# Initialize the vertex buffer object
vertices =     np.array( [
        [  0, 1, 0 ],
        [ -1,-1, 0 ],
        [  1,-1, 0 ],
        [  2,-1, 0 ],
        [  4,-1, 0 ],
        [  4, 1, 0 ],
        [  2,-1, 0 ],
        [  4, 1, 0 ],
        [  2, 1, 0 ],
    ], dtype='float32')

vbuff = vbo.VBO(vertices)
shaders.glUseProgram(shader)
im = InputManager()
im.bind_defaults()

running = True
clock = pygame.time.Clock()
dt = 1
glTranslate(-.5, 0, 0)

glClearColor(0.1, 0.1, 0.1, 1)

while running:
    # Events
    running = im.update_inputs()

    # Render
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


    glLoadIdentity()
    shaders.glUseProgram(shader)
    vbuff.bind()
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointerf(vbuff)
    glDrawArrays(GL_TRIANGLES, 0, 9)
    vbuff.unbind()
    glDisableClientState(GL_VERTEX_ARRAY)
    shaders.glUseProgram(0)
    pygame.display.flip()
    dt = clock.tick(60)
