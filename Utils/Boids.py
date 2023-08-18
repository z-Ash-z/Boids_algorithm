from __future__ import annotations

import random

from .Vector import Vector


class Boids:
    
    def __init__(self, width : int, height : int) -> None:
        self.position = Vector(int(random.random() * width), int(random.random() * height))
        self.WIDTH = width
        self.HEIGHT = height
        # self.position = Vector(width // 2, height // 2)
        self.velocity = Vector(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = Vector()
        self.ALIGNMENT_RADIUS = 100
        self.COHESION_RADIUS = 200
        self.MAX_ALIGNMENT_FORCE = 0.02
        self.MAX_COHESION_FORCE = 0.025
        self.MAX_SPEED = 1.0

    def flock(self, boids : list[Boids]):
        alignment = Vector()
        cohesion = Vector()
        alignment_neighbour_count : int = 0
        cohesion_neighbour_count : int = 0

        for boid in boids:
            if boid is not self:
                d = Vector.distance(self.position, boid.position)
                if d < self.ALIGNMENT_RADIUS:
                    alignment.add(boid.velocity)
                    alignment_neighbour_count += 1
                if d < self.COHESION_RADIUS:
                    cohesion.add(boid.position)
                    cohesion_neighbour_count += 1

        
        if alignment_neighbour_count > 0:
            alignment.divide(alignment_neighbour_count)
        if cohesion_neighbour_count > 0:
            cohesion.divide(cohesion_neighbour_count)
            cohesion.sub(self.position)

        alignment.limit(self.MAX_ALIGNMENT_FORCE)
        cohesion.limit(self.MAX_COHESION_FORCE)
        self.acceleration = cohesion + alignment

        print()



    def update(self):
        self.position.add(self.velocity)
        self.velocity.add(self.acceleration)
        self.velocity.limit(self.MAX_SPEED)
        self.__edges()

    def __edges(self):
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