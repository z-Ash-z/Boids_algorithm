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
        velocities = boids.velocities # Access velocities directly
        
        # Triangle geometry (relative to center, pointing right)
        # Tip at (10, 0), Back corners at (-5, 5) and (-5, -5)
        # We will rotate this based on velocity angle
        
        for i in range(len(positions)):
            x, y = positions[i]
            vx, vy = velocities[i]
            
            # Calculate angle
            angle = np.arctan2(vy, vx)
            
            # Rotation matrix components
            c = np.cos(angle)
            s = np.sin(angle)
            
            # Define vertices relative to (0,0)
            # Tip
            tip_x = 10 * c - 0 * s
            tip_y = 10 * s + 0 * c
            
            # Back Left (-5, 5)
            bl_x = -5 * c - 5 * s
            bl_y = -5 * s + 5 * c
            
            # Back Right (-5, -5)
            br_x = -5 * c - (-5) * s
            br_y = -5 * s + (-5) * c
            
            # Translate to position
            vertices = [
                (x + tip_x, y + tip_y),
                (x + bl_x, y + bl_y),
                (x + br_x, y + br_y)
            ]
            
            pygame.draw.polygon(self.screen, (255, 255, 255), vertices)

    def show(self, window_name: str = "Stage") -> None:
        pygame.display.set_caption(window_name)
        pygame.display.flip()
        # Handle events to prevent freezing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
