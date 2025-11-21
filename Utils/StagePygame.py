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
        velocities = boids.velocities
        
        # Vectorized angle calculation
        angles = np.arctan2(velocities[:, 1], velocities[:, 0])
        c = np.cos(angles)
        s = np.sin(angles)
        
        # Triangle offsets (N, 3, 2)
        # Tip (10, 0) -> (10c, 10s)
        tip_x = 10 * c
        tip_y = 10 * s
        
        # Back Left (-5, 5) -> (-5c - 5s, -5s + 5c)
        bl_x = -5 * c - 5 * s
        bl_y = -5 * s + 5 * c
        
        # Back Right (-5, -5) -> (-5c + 5s, -5s - 5c)
        br_x = -5 * c + 5 * s
        br_y = -5 * s - 5 * c
        
        # Create offsets array (N, 3, 2)
        offsets = np.empty((len(positions), 3, 2))
        offsets[:, 0, 0] = tip_x
        offsets[:, 0, 1] = tip_y
        offsets[:, 1, 0] = bl_x
        offsets[:, 1, 1] = bl_y
        offsets[:, 2, 0] = br_x
        offsets[:, 2, 1] = br_y
        
        # Add positions to offsets
        vertices = offsets + positions[:, np.newaxis, :]
        
        # Draw polygons
        # We still need to iterate because pygame.draw.polygon draws one polygon at a time
        # But the math is now done in C (NumPy)
        for v in vertices:
            pygame.draw.polygon(self.screen, (255, 255, 255), v)

    def show(self, window_name: str = "Stage") -> None:
        pygame.display.set_caption(window_name)
        pygame.display.flip()
