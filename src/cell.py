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
RADIUS_MIN = 10.
RADIUS_MAX = 50.
COLOR_ALPHA = 0.8
MUTATION_RATE = 0.1

# Parameter for probability of killing another cell.
KILL_ALPHA = 5


class Genome():
    """ Container class for cell genomes. """
    def __init__(self):
        self.radius = random.uniform(RADIUS_MIN, RADIUS_MAX)
        self.r = random.gammavariate(COLOR_ALPHA, 1)
        self.g = random.gammavariate(COLOR_ALPHA, 1)
        self.b = random.gammavariate(COLOR_ALPHA, 1)
        N = self.r + self.g + self.b
        self.rgb = (self.r/N, self.g/N, self.b/N)

    def mutate(self, rate=0.1):
        """ Randomize each gene with probability 'rate'. """
        # Add gaussian noise to radius.
        self.radius += radius*rate*random.gauss()
        self.radius = min(RADIUS_MAX, max(RADIUS_MIN, self.radius))

        # Dirichlet distribution for color.
        if random.random() < rate:
            self.r = random.gammavariate(COLOR_ALPHA, 1)
        if random.random() < rate:
            self.g = random.gammavariate(COLOR_ALPHA, 1)
        if random.random() < rate:
            self.b = random.gammavariate(COLOR_ALPHA, 1)
        N = self.r + self.g + self.b
        self.rgb = (self.r/N, self.g/N, self.b/N)

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

        # Store reference to cell in shape for collisons.
        # TODO: This feels hacky, sign of bad design?
        self.shape.cell = self

        # Initialize life.
        self.alive = True
        self.force = (0, 0)
        self.energy = r**2
        self.max_energy = 2*r**2
        self.update_shape_color()
        self.time = time.time()

    def update_shape_color(self):
        """ Set self.shape based on self.genes.rgb and self.energy. """
        # Set color proportional to energy and genes.
        base = 0.5*self.max_energy
        mult = 255 * self.energy / base
        color = [mult*c for c in self.genes.rgb]
        # Add extra energy equally.
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
        # TODO: More complex thinking.
        r = self.genes.radius
        x, y = 0,0
        x += random.gauss(0, r)
        y += random.gauss(0, r)
        self.force = x, y

    def eat(self, food):
        """ Eat a food particle. """
        food.remove()
        self.energy += food.energy
        self.energy = min(self.energy, self.max_energy)
        self.update_shape_color()

    def attack(self, other):
        """ Attack another cell. """
        # Compute the probability of succeeding.
        ratio = other.body.mass / self.body.mass
        prob_success = math.exp(-KILL_ALPHA*ratio)
        if random.random() < prob_success:
            # Take energy from the other cell.
            other.die()
            self.energy += other.energy
            self.energy = min(self.energy, self.max_energy)
            self.update_shape_color()

    def split(self):
        """ Split into two cells. """
        # Create mutated copy of self.
        new_genes = copy.deepcopy(self.genes)
        new_cell = self.world.add_cell(self.body.position, new_genes)
        new_cell.energy = self.energy / 2.0
        new_cell.update_shape_color()
        # Pay penalty.
        self.energy /= 2.0
        self.update_shape_color()
        return new_cell

    def loop(self):
        """ Main loop for cells. """
        # Choose new action.
        self.think()
        # Apply force.
        x, y = self.force
        self.body.apply_force_at_local_point((x,y), point=(0,0))
        # Pay penalty.
        self.energy -= ENERGY_FORCE_RATIO * (x**2 + y**2)
        if self.energy <= 0:
            self.die()
        else:
            self.update_shape_color()
