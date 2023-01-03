from tests.opengl.dfp_shaderlib.pygameoglw import *
from tests.opengl.dfp_shaderlib.shaderlib import Shader
from src.nitegame import InputManager, load_image, pg, init

init()

running = True
im = InputManager()
img_surf = load_image("../assets/logo.png")

while running:
    running = im.update_inputs()
