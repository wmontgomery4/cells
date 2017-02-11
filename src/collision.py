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
    print "Begin: {}".format(arbiter.shapes)

    # Get the shapes and determine the winner.
    big, small = [s.cell for s in arbiter.shapes]
    if big.body.mass < small.body.mass:
        small, big = big, small

    # Play out a battle.
    # TODO: move this logic to cell.attack() later.
    small.die()
    big.energy += small.energy
    big.energy = min(big.energy, big.max_energy)
    big.update_shape_color()
    print "{} eats {}".format(big, small)
    return True

def cell_cell_post_solve(arbiter, space, data):
    print "Impulse: {}".format(arbiter.total_impulse)
    print "Energy lost: {}".format(arbiter.total_ke)
    return True

def cell_cell_separate(arbiter, space, data):
    print "Separate: {}".format(arbiter.shapes)
    return True
