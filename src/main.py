"""
Evolutionary cell simulation.
"""

import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
import pymunk as pm
import pymunk.pyglet_util as util
from cell import Cell

import random
random.seed(47)

# App constants.
WIDTH = 1100
HEIGHT = 700
OFFSET = 3
NUM_CELLS = 24


class Main(pyglet.window.Window):
    def __init__(self):
        """ Initialize pyglet app. """
        pyglet.window.Window.__init__(self, vsync=False,
                width=WIDTH, height=HEIGHT)
        self.set_caption('Cells')
        self.draw_options = util.DrawOptions()

        # Initialize pymunk space and start updating app.
        self.init_space()
        pyglet.clock.schedule_interval(self.update, 1/60.0)
        
    def init_space(self):
        """ Initialize pymunk physics space. """
        self.space = pm.Space()
        self.space.sleep_time_threshold = 0.3
        
        # Create walls around arena.
        bl = (OFFSET, OFFSET)
        tl = (OFFSET, HEIGHT-OFFSET)
        br = (WIDTH-OFFSET, OFFSET)
        tr = (WIDTH-OFFSET, HEIGHT-OFFSET)
        self.walls = [pm.Segment(self.space.static_body, bl, br, 1),
                pm.Segment(self.space.static_body, br, tr, 1),
                pm.Segment(self.space.static_body, tr, tl, 1),
                pm.Segment(self.space.static_body, tl, bl, 1)]
        for w in self.walls:
            w.friction = 0.3
        self.space.add(self.walls)

        # Create initial cells.
        self.cells = []
        for _ in range(NUM_CELLS):
            self.add_cell()

    def add_cell(self, position=None, genes=None):
        """
        Add a cell to the space at 'position' with 'genes'.
        """
        cell = Cell(genes)
        if position is None:
            # Random position within arena.
            r = cell.shape.radius
            x = random.uniform(OFFSET+r, WIDTH-OFFSET-r)
            y = random.uniform(OFFSET+r, HEIGHT-OFFSET-r)
            position = (x,y)
        cell.body.position = position
        self.space.add(cell.body, cell.shape)
        self.cells.append(cell)

    def update(self, T):
        dt = 1/250.
        t = 0
        while t < T:
            t += dt
            self.space.step(dt)
            for cell in self.cells:
                cell.loop()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            pyglet.app.exit()

    def on_draw(self):
        self.clear()
        self.space.debug_draw(self.draw_options)
        
if __name__ == '__main__':
    main = Main()
    pyglet.app.run()
