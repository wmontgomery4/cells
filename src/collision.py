"""
Module for handling collisions.
"""

import pymunk as pm

import random

# Collision types.
CELL = 1
FOOD = 2

def cell_cell_begin(arbiter, space, data):
    """ Collision handler for cell/cell beginning contact. """
    big, small = [s.cell for s in arbiter.shapes]
    if not small.alive:
        print "TODO: Can't attack a dead thing."
    if big.body.mass < small.body.mass:
        small, big = big, small
    big.attack(small)
    return True

def cell_food_begin(arbiter, space, data):
    """ Collision handler for cell/cell beginning contact. """
    cell_shape, food_shape = arbiter.shapes
    cell = cell_shape.cell
    food = food_shape.food
    cell.eat(food)
    return True
