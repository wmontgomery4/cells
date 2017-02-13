"""
Module for handling collisions.
"""

import pymunk as pm

import math
import random

# Collision types.
CELL = 1
FOOD = 2

# Parameter for probability of killing another cell.
KILL_ALPHA = 1
# How much energy you get from eating other cells.
ENERGY_EFFICIENCY = 0.7

def cell_cell_begin(arbiter, space, data):
    """ Collision handler for cell/cell beginning contact. """
    strong, weak = [s.cell for s in arbiter.shapes]
    if not weak.alive:
        print "TODO: Can't attack a dead thing."
    if strong.energy < weak.energy:
        weak, strong = strong, weak
    # Compute the probability of failing.
    ratio = strong.energy / weak.energy
    prob_failure = math.exp(-KILL_ALPHA*(ratio-1))
    if random.random() > prob_failure:
        # Take energy from the other cell.
        strong.update_energy(ENERGY_EFFICIENCY*weak.energy)
        weak.die()
        return False
    return True

def cell_food_begin(arbiter, space, data):
    """ Collision handler for cell/food beginning contact. """
    # The cell eats the food and gets energy.
    cell_shape, food_shape = arbiter.shapes
    cell = cell_shape.cell
    food = food_shape.food
    cell.update_energy(food.energy)
    food.remove()
    return True
