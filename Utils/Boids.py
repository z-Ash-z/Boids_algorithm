from __future__ import annotations

import random

from .Vector import Vector


class Boids:
    
    def __init__(self, width : int, height : int) -> None:
        """
        The Boids class, initialize it with the stage's width and height.
        This class takes care of the flocking characteristic of the individual boid.

        Args:
            width: The width of the stage in pixels.
            height: The heigth of the stage in pixels.
        """
        self.position = Vector(int(random.random() * width), int(random.random() * height))
        self.WIDTH = width
        self.HEIGHT = height
        # self.position = Vector(width // 2, height // 2)
        self.velocity = Vector(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = Vector()
        self.ALIGNMENT_RADIUS = 100
        self.COHESION_RADIUS = 200
        self.SEPERATION_RADIUS = 20
        self.MAX_ALIGNMENT_FORCE = 0.01
        self.MAX_COHESION_FORCE = 0.015
        self.MAX_SEPERATION_FORCE = 0.1
        self.MAX_SPEED = 1.0

    def flock(self, boids : list[Boids]):
        """
        Uses alignment, cohesion and seperation properties of the Boids algorithm to flock all the Boids in the stage.

        Args:
            boids: The list of boids on the stage.
        """
        alignment = Vector()        # The vector that takes care of the alignment.
        cohesion = Vector()         # The vector that takes care of the cohesion. 
        seperation = Vector()       # The vector that takes care of the seperation.
        alignment_neighbour_count : int = 0
        cohesion_neighbour_count : int = 0
        seperation_neighbour_count : int = 0

        for boid in boids:
            if boid is not self:
                d = Vector.distance(self.position, boid.position)

                # Using distance for alignment force.
                if d < self.ALIGNMENT_RADIUS:
                    alignment.add(boid.velocity)
                    alignment_neighbour_count += 1

                # Using distance for cohesion force.
                if d < self.COHESION_RADIUS:
                    cohesion.add(boid.position)
                    cohesion_neighbour_count += 1

                # Using distance for seperation force.
                if d < self.SEPERATION_RADIUS:
                    diff : Vector = self.position - boid.position
                    diff.divide(d)
                    seperation.add(diff)
                    seperation_neighbour_count += 1

        # Calculating alignemnt force.
        if alignment_neighbour_count > 0:
            alignment.divide(alignment_neighbour_count)
        
        # Calculating the cohesion force.
        if cohesion_neighbour_count > 0:
            cohesion.divide(cohesion_neighbour_count)
            cohesion.sub(self.position)

        # Calculating the seperation force.
        if seperation_neighbour_count > 0:
            seperation.divide(seperation_neighbour_count)

        # Limiting the calculated forces with the set thresholds.
        alignment.limit(self.MAX_ALIGNMENT_FORCE)
        cohesion.limit(self.MAX_COHESION_FORCE)
        seperation.limit(self.MAX_SEPERATION_FORCE)

        # Calculating the acceleration 
        self.acceleration = seperation + cohesion + alignment

    def update(self):
        """
        The update method that updates the position of the boid based on the calculated acceleration.
        """
        self.position.add(self.velocity)
        self.velocity.add(self.acceleration)
        self.velocity.limit(self.MAX_SPEED)
        self.__edges()

    def __edges(self):
        """
        The method that wraps the position of the boid back to the stage, if the position crosses the stage.
        """
        if (self.position.x >= self.WIDTH):
            self.position.x = 0
        elif (self.position.x <= 0):
            self.position.x = self.WIDTH
        
        if (self.position.y >= self.HEIGHT):
            self.position.y = 0
        elif (self.position.y <= 0):
            self.position.y = self.HEIGHT

def main() -> None:
    pass

if __name__ == '__main__':
    main()