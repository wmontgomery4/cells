"""
Basic food class, just provides energy for cells.
"""

import pymunk as pm

import math
import random

import collision

# Physics constants.
RADIUS = 3
ENERGY = 100
DENSITY = 1e-4
FRICTION = 0.3

class Food():
    """ Container class for food bodies. """
    def __init__(self):
        """ Initialize food particle. """

        # Initialize body.
        mass = DENSITY * RADIUS**2
        moment = pm.moment_for_circle(mass, 0, RADIUS, (0,0))
        self.body = pm.Body(mass, moment)

        # Initialize shape.
        self.shape = pm.Circle(self.body, RADIUS, (0,0))
        self.shape.friction = FRICTION
        self.shape.collision_type = collision.FOOD
        self.shape.color = (255, 255, 255)

        self.eaten = False
        self.energy = ENERGY

        # Store reference to self in shape for collisons.
        # TODO: This feels hacky, sign of bad design?
        self.shape.food = self

    def remove(self):
        """ Remove self from space. """
        self.eaten = True
        self.body.space.remove(self.body, self.shape)
