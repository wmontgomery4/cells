"""
Class for cell type.
"""

import pymunk as pm

import math
import random
random.seed(47)

# Physics constants.
FRICTION = 0.3
CONTROL_LIMIT = 10000

# Gene definitions and ranges.
GENES = ['radius', 'density', 'color']
RADIUS_MIN = 5.
RADIUS_MAX = 30.
LOG_DENSITY_MIN = -1.
LOG_DENSITY_MAX = 1.


class Genome():
    """ Container class for cell genomes. """
    def __init__(self):
        self.radius = random.uniform(RADIUS_MIN, RADIUS_MAX)
        log_density = random.uniform(LOG_DENSITY_MIN, LOG_DENSITY_MAX)
        self.density = math.exp(log_density)
        self.color = (random.randint(0, 255), random.randint(0,255),
                random.randint(0,255))


class Cell():
    """ Container class for cell automatons. """
    def __init__(self, genes=None):
        """ Initialize a Cell with 'genes', random if None given. """
        if genes is None:
            genes = Genome()
        self.genes = genes

        # Create the body.
        r = self.genes.radius
        mass = r**2 * self.genes.density
        moment = pm.moment_for_circle(mass, 0, r, (0,0))
        self.body = pm.Body(mass, moment)

        # Create the shape.
        self.shape = pm.Circle(self.body, r, (0,0))
        self.shape.color = self.genes.color
        self.shape.friction = FRICTION

        # Initialize the control.
        self.force = (0, 0)

    def loop(self):
        """ Perform one loop. """
        # Implement OU process for now (not sure if actually correct).
        x, y = self.force
        x += random.gauss(0, 0.5*CONTROL_LIMIT)
        x = min(CONTROL_LIMIT, max(-CONTROL_LIMIT, x))
        y += random.gauss(0, 0.5*CONTROL_LIMIT)
        y = min(CONTROL_LIMIT, max(-CONTROL_LIMIT, x))
        self.force = x, y
        self.body.apply_force_at_local_point(self.force, point=(0,0))
