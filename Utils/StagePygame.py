import pygame
import numpy as np
from .Boids import Boids

class StagePygame:
    def __init__(self, x: int = 500, y: int = 500) -> None:
        pygame.init()
        self.WIDTH = x
        self.HEIGHT = y
        self.screen = pygame.display.set_mode((x, y))
        self.clock = pygame.time.Clock()

    def drawBoids(self, boids: Boids) -> None:
        self.screen.fill((0, 0, 0))  # Clear screen
        positions = boids.get_positions()
        
        # Pygame drawing is often faster if we don't iterate in python, but 
        # pygame.draw.circle doesn't support vectorized inputs directly.
        # We have to iterate.
        for x, y in positions:
            pygame.draw.circle(self.screen, (255, 255, 255), (int(x), int(y)), 5)

    def show(self, window_name: str = "Stage") -> None:
        pygame.display.set_caption(window_name)
        pygame.display.flip()
        # Handle events to prevent freezing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
