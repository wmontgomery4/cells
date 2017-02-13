"""
Handle everything related to the world.
"""

import pymunk as pm
from pymunk.pyglet_util import DrawOptions

import math
import random

from cell import Cell
from food import Food

import collision
from collision import CELL, FOOD

OFFSET = 3
MIN_CELLS = 6
MAX_CELLS = 144
FOOD_SPAWN_PROB = 0.05


class World():
    def __init__(self, width, height):
        """ Create new world and initialize. """
        self.width = width
        self.height = height

        # Initialize physics engine.
        self.space = pm.Space()
        self.space.sleep_time_threshold = 0.3
        self.draw_options = DrawOptions()

        # Collision handling.
        self.cc_handler = self.space.add_collision_handler(
                collision.CELL, collision.CELL)
        self.cc_handler.begin = collision.cell_cell_begin

        self.cf_handler = self.space.add_collision_handler(
                collision.CELL, collision.FOOD)
        self.cf_handler.begin = collision.cell_food_begin
        
        # Create walls around arena.
        bl = (OFFSET, OFFSET)
        tl = (OFFSET, height-OFFSET)
        br = (width-OFFSET, OFFSET)
        tr = (width-OFFSET, height-OFFSET)
        self.walls = [pm.Segment(self.space.static_body, bl, br, 1),
                pm.Segment(self.space.static_body, br, tr, 1),
                pm.Segment(self.space.static_body, tr, tl, 1),
                pm.Segment(self.space.static_body, tl, bl, 1)]
        for w in self.walls:
            w.friction = 0.3
        self.space.add(self.walls)

        # Use main loop to populate initial cells.
        self.cells = []
        self.main_loop()

    def main_loop(self):
        """ Loop through the cells, taking actions, adding/removing. """
        new_cells = []
        for cell in self.cells:
            # Remove cells that died between calls (to allow for GC).
            if not cell.alive:
                continue
            # Split cells that have reached the energy limit.
            if cell.energy >= cell.max_energy:
                child = cell.split()
                new_cells.append(child)
            # Take a step with the cell.
            cell.loop()
            # Filter out cells that died in their loop.
            if cell.alive:
                new_cells.append(cell)
        self.cells = new_cells

        # Add more cells if we're below the minimum.
        num = MIN_CELLS - len(self.cells)
        self.cells += [self.add_cell() for _ in range(num)]

        # Add more food.
        if random.random() < FOOD_SPAWN_PROB:
            self.add_food()

    def add_cell(self, position=None, genes=None):
        """ Add a cell to the space at 'position' with 'genes'. """
        cell = Cell(self, genes)
        if position is None:
            # Random position within arena.
            r = cell.shape.radius
            x = random.uniform(OFFSET+r, self.width-OFFSET-r)
            y = random.uniform(OFFSET+r, self.height-OFFSET-r)
            position = (x,y)
        cell.body.position = position
        self.space.add(cell.body, cell.shape)
        return cell

    def add_food(self, position=None):
        """ Add a cell to the space at 'position' with 'genes'. """
        food = Food()
        if position is None:
            # Random position within arena.
            r = food.shape.radius
            x = random.uniform(OFFSET+r, self.width-OFFSET-r)
            y = random.uniform(OFFSET+r, self.height-OFFSET-r)
            position = (x,y)
        food.body.position = position
        self.space.add(food.body, food.shape)

    def run(self, T):
        """ Run the world for 'T' time at 'dt' resolution. """
        t = 0
        dt = 1/250. # Magic number.
        while t < T:
            self.main_loop()
            self.space.step(dt)
            t += dt

    def draw(self):
        """ Draw with the current draw_options. """
        self.space.debug_draw(self.draw_options)
