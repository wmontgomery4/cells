"""
Class for cell type.
"""

import random
import pymunk as pm

GENES = ['mass', 'radius', 'friction', 'color']
CONTROL_LIMIT = 10000

class Cell():
    def __init__(self, genes=None):
        """
        Initialize a Cell with 'genes'.
        """
        if genes is None:
            genes = Cell.random_genes()
        self.genes = genes

        # Create the body.
        mass = genes['mass']
        radius = genes['radius']
        moment = pm.moment_for_circle(mass, 0, radius, (0,0))
        self.body = pm.Body(mass, moment)

        # Create the shape.
        self.shape = pm.Circle(self.body, radius, (0,0))
        self.shape.color = genes['color']
        self.shape.friction = genes['friction']

        # Initialize the control.
        self.force = (0, 0)

    @staticmethod
    def random_genes():
        genes = {}
        genes['mass'] = random.randint(50, 500)
        genes['radius'] = random.randint(5, 50)
        genes['friction'] = 0.1 + 0.8*random.random()
        genes['color'] = (random.randint(0, 255),
                            random.randint(0,255),
                            random.randint(0,255),
                            random.randint(100,255))
        return genes

    def act(self, force=None):
        # Implement OU process (not sure if actually correct).
        if force is None:
            # Add new noise to old force and clip.
            x, y = self.force
            x += random.gauss(0, 0.5*CONTROL_LIMIT)
            x = min(CONTROL_LIMIT, max(-CONTROL_LIMIT, x))
            y += random.gauss(0, 0.5*CONTROL_LIMIT)
            y = min(CONTROL_LIMIT, max(-CONTROL_LIMIT, x))
            force = x, y
        self.body.apply_force_at_local_point(force, (0,0))
        # Store most recently applied force.
        self.force = force
