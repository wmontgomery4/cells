"""
Class for cell type.
"""

import pymunk as pm

import math
import random
random.seed(47)

# Physics constants.
DENSITY = 0.1
FRICTION = 0.3
CONTROL_LIMIT = 5000

# Gene definitions and ranges.
GENES = ['radius', 'color']
RADIUS_MIN = 5.
RADIUS_MAX = 50.
COLOR_ALPHA = 0.8

class Genome():
    """ Container class for cell genomes. """
    def __init__(self):
        # Uniform distribution for radius.
        self.radius = random.uniform(RADIUS_MIN, RADIUS_MAX)

        # Dirichlet distribution for color.
        r = random.gammavariate(COLOR_ALPHA, 1)
        g = random.gammavariate(COLOR_ALPHA, 1)
        b = random.gammavariate(COLOR_ALPHA, 1)
        total = r + g + b
        self.rgb = (r/total, g/total, b/total)


class Cell():
    """ Container class for cell automatons. """
    def __init__(self, genes=None):
        """ Initialize a Cell with 'genes', random if None given. """
        if genes is None:
            genes = Genome()
        self.genes = genes

        # Create the body.
        r = self.genes.radius
        mass = DENSITY * r**2
        moment = pm.moment_for_circle(mass, 0, r, (0,0))
        self.body = pm.Body(mass, moment)

        # Create the shape.
        self.shape = pm.Circle(self.body, r, (0,0))
        self.shape.friction = FRICTION
        self.set_shape_color

        # Initialize the control.
        self.force = (0, 0)

    def set_shape_color(self, color=None):
        if color is None:
            r, g, b = self.genes.rgb
            color = (r*255, g*255, b*255)
        self.shape.color = color

    def loop(self):
        """ Perform one loop. """
        # Update color based on current energy.
        self.set_shape_color()

        # Implement OU process for now (not sure if actually correct).
        x, y = self.force
        x += random.gauss(0, 0.5*CONTROL_LIMIT)
        x = min(CONTROL_LIMIT, max(-CONTROL_LIMIT, x))
        y += random.gauss(0, 0.5*CONTROL_LIMIT)
        y = min(CONTROL_LIMIT, max(-CONTROL_LIMIT, x))
        self.force = x, y
        self.body.apply_force_at_local_point(self.force, point=(0,0))
