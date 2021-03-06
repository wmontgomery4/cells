"""
Class for cell type.
"""

import pymunk as pm

import copy
import math
import time
import random

import collision

# Physics constants.
DENSITY = 1e-4
FRICTION = 0.3
ENERGY_FORCE_RATIO = 1e-4

# Gene definitions and ranges.
GENES = ['radius', 'color']
RADIUS_MIN = 5.
RADIUS_MAX = 30.
COLOR_ALPHA = 0.8
MUTATION_RATE = 0.1
LOG_GAIN_MIN = -5.
LOG_GAIN_MAX = -3.

class Genome():
    """ Container class for cell genomes. """
    def __init__(self):
        # Uniform for radius.
        self.radius = random.uniform(RADIUS_MIN, RADIUS_MAX)

        # Dirichlet distribution for color.
        self.r = random.gammavariate(COLOR_ALPHA, 1)
        self.g = random.gammavariate(COLOR_ALPHA, 1)
        self.b = random.gammavariate(COLOR_ALPHA, 1)
        N = self.r + self.g + self.b
        self.rgb = (self.r/N, self.g/N, self.b/N)

        # Log-Uniform for gain.
        self.log_gain = random.uniform(LOG_GAIN_MIN, LOG_GAIN_MAX)
        self.gain = math.exp(self.log_gain)

    def mutate(self, rate=MUTATION_RATE):
        """ Randomize each gene with probability 'rate'. """
        # Add gaussian noise to radius.
        self.radius += random.gauss(0,self.radius*rate)
        self.radius = min(RADIUS_MAX, max(RADIUS_MIN, self.radius))

        # Potentially draw new gammavariates.
        if random.random() < rate:
            self.r = random.gammavariate(COLOR_ALPHA, 1)
        if random.random() < rate:
            self.g = random.gammavariate(COLOR_ALPHA, 1)
        if random.random() < rate:
            self.b = random.gammavariate(COLOR_ALPHA, 1)
        N = self.r + self.g + self.b
        self.rgb = (self.r/N, self.g/N, self.b/N)

        # Add gaussian noise to gain.
        self.log_gain += random.gauss(0, rate)
        self.log_gain = min(LOG_GAIN_MAX, max(LOG_GAIN_MIN, self.radius))
        self.gain = math.exp(self.log_gain)

class Cell():
    """ Container class for cell automatons. """
    def __init__(self, world, genes=None):
        """ Initialize a Cell with 'genes', random if None given. """
        self.world = world
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
        self.shape.filter = pm.ShapeFilter(categories=collision.CELL)

        # Store reference to cell in shape for collisons.
        # TODO: This feels hacky, sign of bad design?
        self.shape.cell = self

        # Initialize life.
        self.time = time.time()
        self.alive = True
        self.force = (0, 0)
        self.energy = 0
        self.max_energy = 2*r**2
        self.update_energy(r**2)

    def update_energy(self, delta):
        """ Add or consume energy. """
        self.energy += delta
        if self.energy <= 0:
            self.die()
            return
        elif self.energy > self.max_energy:
            self.energy = self.max_energy
        # Set base color proportional to energy and genes.
        base = 0.5*self.max_energy
        mult = 255 * self.energy / base
        color = [mult*c for c in self.genes.rgb]
        # Add equally to RGB past the base energy.
        if self.energy > base:
            diff = self.energy - base
            add = 255 * diff / base
            color = [min(255, c + add) for c in color]
        self.shape.color = color

    def die(self):
        """ Remove self from space. """
        self.body.space.remove(self.body, self.shape)
        self.alive = False

    def think(self):
        """ Choose a new action. """
        # Query for closest food.
        # TODO: Add vision for nearest cells too.
        r = self.genes.radius
        pos = self.body.position
        mask = pm.ShapeFilter.ALL_MASKS ^ (collision.CELL | collision.WALL)
        info = self.world.space.point_query_nearest(pos, 12*r,
                pm.ShapeFilter(mask=mask))

        # Initialize force.
        ux = 0
        uy = 0
        self.force = ux, uy

        # No thinking without information (yet?)
        if info is None:
            return

        # Apply gains.
        K = self.genes.gain
        delta = pos - info.point
        self.force -= K*delta

    def split(self):
        """ Split into two cells. """
        # Create mutated copy of self.
        new_genes = copy.deepcopy(self.genes)
        new_genes.mutate()
        new_cell = self.world.add_cell(self.body.position, new_genes)
        # Pay penalty.
        self.update_energy(-new_cell.energy)
        return new_cell

    def loop(self):
        """ Main loop for cells. """
        # Choose new action.
        self.think()
        # Apply force.
        x, y = self.force
        self.body.apply_force_at_local_point((x,y), point=(0,0))
        # Pay penalty.
        cost = -ENERGY_FORCE_RATIO * (x**2 + y**2)
        self.update_energy(cost)
