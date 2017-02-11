"""
Module for handling collisions.
"""

import pymunk as pm


# Collision types.
CELL = 1
FOOD = 2

def cell_cell_begin(arbiter, space, data):
    print "Begin: {}".format(arbiter.shapes)
    print "Contact points: {}".format(arbiter.contact_point_set)
    return True

def cell_cell_post_solve(arbiter, space, data):
    print "Impulse: {}".format(arbiter.total_impulse)
    print "Energy lost: {}".format(arbiter.total_ke)
    return True

def cell_cell_separate(arbiter, space, data):
    print "Separate: {}".format(arbiter.shapes)
    return True
