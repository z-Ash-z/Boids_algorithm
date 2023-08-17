from __future__ import annotations

import random

from .Vector import Vector


class Boids:
    
    def __init__(self, width : int, height : int) -> None:
        self.position = Vector(int(random.random() * width), int(random.random() * height))
        self.WIDTH = width
        self.HEIGHT = height
        # self.position = Vector(width // 2, height // 2)
        self.MAX_SPEED = 1
        self.velocity = Vector(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = Vector()
        self.PERCEPTION_RADIUS = 50

    def flock(self, boids : list[Boids]):
        average = Vector()
        neighbour_count : int = 0

        for boid in boids:
            if boid is not self:
                d = Vector.distance(self.position, boid.position)
                if d < self.PERCEPTION_RADIUS:
                    average.add(boid.velocity)
                    neighbour_count += 1
        
        if neighbour_count > 0:
            average.divide(neighbour_count)



    def update(self):
        self.position.add(self.velocity)
        self.velocity.add(self.acceleration)
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