"""
Module for handling collisions.
"""

import pymunk as pm


# Collision types.
CELL = 1
FOOD = 2

def cell_cell_begin(arbiter, space, data):
    print "Arbiter has shapes {}".format(arbiter.shapes)
    return True
