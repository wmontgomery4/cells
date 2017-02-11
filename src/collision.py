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
    if big.body.mass < small.body.mass:
        small, big = big, small
    big.attack(small)
    return True

def cell_cell_post_solve(arbiter, space, data):
    print "Impulse: {}".format(arbiter.total_impulse)
    print "Energy lost: {}".format(arbiter.total_ke)
    return True

def cell_cell_separate(arbiter, space, data):
    print "Separate: {}".format(arbiter.shapes)
    return True
