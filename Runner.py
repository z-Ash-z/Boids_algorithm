import time
import pygame
from Utils import Boids
from Utils.StagePygame import StagePygame


def main() -> None:
    stage = StagePygame(1000, 1000)

    # Initialize Boids manager with 1000 boids
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

        boids.flock()
        boids.update()
        stage.drawBoids(boids)
        stage.show("Boids Algorithm")

    end_time = time.perf_counter()
    print(f'The Simulation time: {end_time - start_time}sec')
    pygame.quit()

if __name__ == '__main__':
    main()