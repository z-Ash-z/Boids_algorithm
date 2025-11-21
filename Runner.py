import time
import pygame
from Utils import Boids
from Utils.StagePygame import StagePygame


def main() -> None:
    stage = StagePygame(fullscreen=False)

    # Initialize Boids manager with 500 boids
    boids = Boids(500, stage.WIDTH, stage.HEIGHT)
    
    start_time = time.perf_counter()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                stage.resize(width, height)
                boids.WIDTH = width
                boids.HEIGHT = height

        boids.flock()
        boids.update()
        stage.drawBoids(boids)
        stage.show("Boids Algorithm")

    end_time = time.perf_counter()
    print(f'The Simulation time: {end_time - start_time}sec')
    pygame.quit()

if __name__ == '__main__':
    main()