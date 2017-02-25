"""
Module for handling collisions.
"""

import pymunk as pm

import time
import math
import random

# Collision types.
WALL = 0b1
CELL = 0b10
FOOD = 0b100

# Parameter for probability of killing another cell.
KILL_ALPHA = 1
# How much energy you get from eating other cells.
ENERGY_EFFICIENCY = 0.9
# Ignore newborn cells for a short delay.
NEWBORN_DELAY = 0.5

def cell_cell_begin(arbiter, space, data):
    """ Collision handler for cell/cell beginning contact. """
    strong, weak = [s.cell for s in arbiter.shapes]
    # Make sure both cells are actually alive.
    if not weak.alive or not strong.alive:
        print "TODO: This shouldn't happen really"
        return False
    # Ignore newborn cells.
    cutoff = time.time() - NEWBORN_DELAY
    if weak.time > cutoff or strong.time > cutoff:
        return True
    # Sort to get actual weak/strong.
    if strong.energy < weak.energy:
        weak, strong = strong, weak
    # Compute the probability of successful attack.
    ratio = strong.energy / weak.energy
    prob_success = 1. - math.exp(-KILL_ALPHA*(ratio-1))
    r, g, b = strong.genes.rgb
    R, G, B = weak.genes.rgb
    prob_success *= 1. - (r*R + g*G + b*B)
    if random.random() < prob_success:
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
