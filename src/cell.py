"""
Class for cell type.
"""

import pymunk as pm

import math
import random

import collision

# Physics constants.
DENSITY = 1e-4
FRICTION = 0.3
ENERGY_FORCE_RATIO = 1e-4

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
        N = r + g + b
        self.rgb = (r/N, g/N, b/N)


class Cell():
    """ Container class for cell automatons. """
    def __init__(self, genes=None):
        """ Initialize a Cell with 'genes', random if None given. """
        if genes is None:
            genes = Genome()
        self.genes = genes

        # Initialize body.
        r = self.genes.radius
        mass = DENSITY * r**2
        moment = pm.moment_for_circle(mass, 0, r, (0,0))
        self.body = pm.Body(mass, moment)

        # Initialize shape.
        self.shape = pm.Circle(self.body, r, (0,0))
        self.shape.friction = FRICTION
        self.shape.collision_type = collision.CELL

        # Initialize life.
        self.alive = True
        self.force = (0, 0)
        self.energy = r**2
        self.max_energy = r**2
        self.set_shape_color()

    def set_shape_color(self):
        """ Set self.shape based on self.genes.rgb and self.energy. """
        r, g, b = self.genes.rgb
        mult = 255 * self.energy / self.max_energy
        self.shape.color = (r*mult, g*mult, b*mult)

    def think(self):
        """ Choose a new action. """
        # TODO: More complex thinking.
        r = self.genes.radius
        x, y = 0,0
        x += random.gauss(0, r)
        y += random.gauss(0, r)
        self.force = x, y

    def loop(self):
        """ Main loop for cells. """
        # Choose new action.
        self.think()
        # Apply force.
        x, y = self.force
        self.body.apply_force_at_local_point((x,y), point=(0,0))
        # Pay penalty.
        cost = ENERGY_FORCE_RATIO * (x**2 + y**2)
        self.energy = max(0, self.energy - cost)
        # Flip life or death coin.
        prob_of_death = math.exp(-self.energy)
        if random.random() < prob_of_death:
            self.die()
        else:
            self.set_shape_color()

    def die(self):
        """ Remove self from space. """
        self.body.space.remove(self.body, self.shape)
        self.alive = False
