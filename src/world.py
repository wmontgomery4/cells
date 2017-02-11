"""
Handle everything related to the world.
"""

import pymunk as pm
from pymunk.pyglet_util import DrawOptions

import math
import random

import collision
from cell import *


class World():
    def __init__(self, min_cells, max_cells, width, height, offset):
        """ Create new world and initialize. """
        self.min_cells = min_cells
        self.max_cells = max_cells
        self.width = width
        self.height = height
        self.offset = offset

        # Initialize physics engine.
        self.space = pm.Space()
        self.space.sleep_time_threshold = 0.3
        self.draw_options = DrawOptions()

        # Collision handling.
        self.cell_handler = self.space.add_collision_handler(1,1)
        self.cell_handler.begin = collision.cell_cell_begin
#        self.cell_handler.post_solve = collision.cell_cell_post_solve
#        self.cell_handler.separate = collision.cell_cell_separate
        
        # Create walls around arena.
        bl = (offset, offset)
        tl = (offset, height-offset)
        br = (width-offset, offset)
        tr = (width-offset, height-offset)
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

    def cell_loop(self):
        """ Loop through the cells, taking actions, adding/removing. """
        new_cells = []
        for cell in self.cells:
            # Remove cells that died between calls (to allow for GC).
            if not cell.alive:
                continue
            # Take a step with the cell.
            cell.loop()
            # Filter out cells that died in their loop.
            if cell.alive:
                new_cells.append(cell)
        self.cells = new_cells

        # Add more cells if we're below the minimum.
        num = self.min_cells - len(self.cells)
        for _ in range(num):
            self.add_cell()

    def add_cell(self, position=None, genes=None):
        """ Add a cell to the space at 'position' with 'genes'. """
        cell = Cell(genes)
        if position is None:
            # Random position within arena.
            r = cell.genes.radius
            x = random.uniform(self.offset+r, self.width-self.offset-r)
            y = random.uniform(self.offset+r, self.height-self.offset-r)
            position = (x,y)
        cell.body.position = position
        self.space.add(cell.body, cell.shape)
        self.cells.append(cell)

    def run(self, T):
        """ Run the world for 'T' time at 'dt' resolution. """
        t = 0
        dt = 1/250. # Magic number.
        while t < T:
            self.cell_loop()
            self.space.step(dt)
            t += dt

    def draw(self):
        """ Draw with the current draw_options. """
        self.space.debug_draw(self.draw_options)
