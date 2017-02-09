"""
Evolutionary cell simulation.
"""

import random
import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
import pymunk as pm
import pymunk.pyglet_util as util
from cell import Cell

random.seed(13)

WIDTH = 1100
HEIGHT = 700
OFFSET = 5
NUM_CELLS = 24


class Main(pyglet.window.Window):
    def __init__(self):
        pyglet.window.Window.__init__(self, vsync=False,
                width=WIDTH,
                height=HEIGHT)
        self.set_caption('Cells')

        pyglet.clock.schedule_interval(self.update, 1/60.0)
        self.fps_display = pyglet.clock.ClockDisplay()

        self.draw_options = util.DrawOptions()
        self.draw_options.flags = self.draw_options.DRAW_SHAPES 

        self.init_space()
        
    def init_space(self):
        self.space = pm.Space()
        self.space.sleep_time_threshold = 0.3
        
        # Create boundaries spanning from corner to corner.
        bl = (OFFSET, OFFSET)
        tl = (OFFSET, HEIGHT-OFFSET)
        br = (WIDTH-OFFSET, OFFSET)
        tr = (WIDTH-OFFSET, HEIGHT-OFFSET)
        self.bounds = [pm.Segment(self.space.static_body, bl, br, 1),
                        pm.Segment(self.space.static_body, br, tr, 1),
                        pm.Segment(self.space.static_body, tr, tl, 1),
                        pm.Segment(self.space.static_body, tl, bl, 1)]

        for b in self.bounds:
            b.friction = 0.3
        self.space.add(self.bounds)

        # Create cells.
        self.cells = []
        for _ in range(NUM_CELLS):
            self.add_cell()

    def add_cell(self, position=None, genes=None):
        """
        Add a cell to the space at 'position' with 'genes'.
        """
        cell = Cell(genes)
        if position is None:
            r = cell.genes['radius']
            x = random.randint(OFFSET+r, WIDTH-OFFSET-r)
            y = random.randint(OFFSET+r, HEIGHT-OFFSET-r)
            position = (x,y)
        cell.body.position = position
        self.space.add(cell.body, cell.shape)
        self.cells.append(cell)

    def update(self, T):
        dt = 1/250.
        t = 0
        while t < T:
            t += dt
            for cell in self.cells:
                cell.act()
            self.space.step(dt)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            pyglet.app.exit()

    def on_draw(self):
        self.clear()
        self.fps_display.draw()  
        self.space.debug_draw(self.draw_options)
        
if __name__ == '__main__':
    main = Main()
    pyglet.app.run()
