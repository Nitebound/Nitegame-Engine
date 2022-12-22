from pygameoglw import *
from shaderlib import *
from src.nitegame import InputManager, load_image, pg, PGDisplay

window = PygameOpenGLWin((1024, 768))

running = True
im = InputManager()
#shader = Shader("../core/shaders/basic_fragment_shader")
img_surf = load_image("../assets/logo.png")

while running:
    running = im.update_inputs()
    window.update_clear()
