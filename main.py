"""
Evolutionary cell simulation.
"""

import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse

import pymunk
from pymunk import Vec2d
import pymunk.pyglet_util

import random

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700
OFFSET = 5

CELL_RADIUS = 15

NUM_CELLS = 24

class Main(pyglet.window.Window):
    def __init__(self):
        pyglet.window.Window.__init__(self, vsync=False,
                width=WINDOW_WIDTH,
                height=WINDOW_HEIGHT)
        self.set_caption('Cells')
        self.cells = []

        pyglet.clock.schedule_interval(self.update, 1/60.0)
        self.fps_display = pyglet.clock.ClockDisplay()

        self.draw_options = pymunk.pyglet_util.DrawOptions()
        self.draw_options.flags = self.draw_options.DRAW_SHAPES 

        self.init_space()
        
    def init_space(self):
        self.space = pymunk.Space()
        self.space.sleep_time_threshold = 0.3
        
        # Create boundaries
        bl = (OFFSET, OFFSET)
        tl = (OFFSET, WINDOW_HEIGHT-OFFSET)
        br = (WINDOW_WIDTH-OFFSET, OFFSET)
        tr = (WINDOW_WIDTH-OFFSET, WINDOW_HEIGHT-OFFSET)

        self.bounds = [pymunk.Segment(self.space.static_body, bl, br, 1),
                        pymunk.Segment(self.space.static_body, br, tr, 1),
                        pymunk.Segment(self.space.static_body, tr, tl, 1),
                        pymunk.Segment(self.space.static_body, tl, bl, 1)]

        for b in self.bounds:
            b.friction = 0.3
        self.space.add(self.bounds)

        # Create cells
        for c in range(NUM_CELLS):
            self.create_cell()

    def create_cell(self):
        mass = 100
        moment = pymunk.moment_for_circle(mass, 0, CELL_RADIUS, (0,0))
        body = pymunk.Body(mass, moment)

        x = random.randint(OFFSET+15, WINDOW_WIDTH-OFFSET-15)
        y = random.randint(OFFSET+15, WINDOW_HEIGHT-OFFSET-15)
        body.position = (x, y)

        shape = pymunk.Circle(body, CELL_RADIUS, (0,0))
        shape.friction = 0.3
        shape.color = (255,150,150,255)
        self.space.add(body, shape)
        
        self.cells.append(body)

    def update(self, T):
        dt = 1/250.
        t = 0
        while t < T:
            t += dt
            for cell in self.cells:
                u = (random.randint(-3000, 3000), random.randint(-3000, 3000))
                cell.apply_force_at_local_point(u, (0,0))                
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
