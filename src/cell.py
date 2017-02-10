"""
Class for cell type.
"""

import pymunk as pm

import math
import random
random.seed(47)

# Physics constants.
DENSITY = 0.01
FRICTION = 0.3

# Gene definitions and ranges.
GENES = ['radius', 'color']
RADIUS_MIN = 5.
RADIUS_MAX = 50.
COLOR_ALPHA = 0.8

# Energy constants.
COST_FORCE_RATIO = 1e-5

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

        # Initialize the force and energy.
        self.force = (0, 0)
        self.energy = r**2

    def set_shape_color(self):
        """ Set self.shape based on self.genes.rgb and self.energy. """
        radius = self.genes.radius
        r, g, b = self.genes.rgb
        mult = 255 * (self.energy / radius**2)
        self.shape.color = (r*mult, g*mult, b*mult)

    def loop(self):
        """ Perform one loop. """
        # Compute new force.
        # NOTE: Using OU process for now (not sure if actually correct).
        x, y = self.force
        x += random.gauss(0, 1)
        y += random.gauss(0, 1)
        self.force = x, y

        # Apply force and update energy.
        self.body.apply_force_at_local_point(self.force, point=(0,0))
        self.energy -= COST_FORCE_RATIO * (x**2 + y**2)
        self.energy = max(0, self.energy)

        # Update color for new energy.
        self.set_shape_color()
