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
FPS = 1/250.
INTERVAL = 1/60.

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
        self.draw_options = util.DrawOptions()

        # Initialize physics engine.
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

        # Use main loop to populate initial cells.
        self.cells = []
        self.cell_loop()

        # Keep track of whether 'step' is scheduled.
        self.running = False
        self.toggle_run()

    def run(self, T):
        """ Called by pyglet.clock when self.running. """
        t = 0
        while t < T:
            self.cell_loop()
            self.space.step(FPS)
            t += FPS

    def cell_loop(self):
        """ Loop through the cells, taking actions, adding/removing. """
        new_cells = []
        for cell in self.cells:
            cell.step()
            if cell.energy > 0:
                new_cells.append(cell)
            else:
                self.space.remove(cell.body, cell.shape)
        self.cells = new_cells

        # Add more cells if we're below the minimum.
        num = MIN_CELLS - len(self.cells)
        for _ in range(num):
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

    def toggle_run(self):
        if self.running:
            pyglet.clock.unschedule(self.run)
        else:
            pyglet.clock.schedule_interval(self.run, INTERVAL)
        self.running = not self.running

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            pyglet.app.exit()
        elif symbol == key.SPACE:
            self.toggle_run()

    def on_draw(self):
        self.clear()
        self.space.debug_draw(self.draw_options)
        
if __name__ == '__main__':
    main = Main()
    pyglet.app.run()
