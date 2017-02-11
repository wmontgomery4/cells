"""
Evolutionary cell simulation.
"""

import math
import random
random.seed(47)

import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
import pymunk as pm
import pymunk.pyglet_util as util

from world import World

# App constants.
TIMESTEP = 1/250. # When running the world.
INTERVAL = 1/60. # For pyglet.clock.

WIDTH = 1200
HEIGHT = 700
OFFSET = 3

MIN_CELLS = 24
MAX_CELLS = 144


class Main(pyglet.window.Window):
    def __init__(self):
        """ Initialize pyglet app. """
        pyglet.window.Window.__init__(self, vsync=False,
                width=WIDTH, height=HEIGHT)
        self.set_caption('Cells')

        # Initialize world.
        self.world = World(MIN_CELLS, MAX_CELLS, WIDTH, HEIGHT, OFFSET)

        # Keep track of whether 'run' is scheduled.
        self.running = False
        self.toggle_run()

    def toggle_run(self):
        if self.running:
            pyglet.clock.unschedule(self.world.run)
        else:
            pyglet.clock.schedule_interval(self.world.run, INTERVAL)
        self.running = not self.running

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            pyglet.app.exit()
        elif symbol == key.SPACE:
            self.toggle_run()

    def on_draw(self):
        self.clear()
        self.world.draw()
        
if __name__ == '__main__':
    main = Main()
    pyglet.app.run()
