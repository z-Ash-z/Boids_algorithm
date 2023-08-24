import time
import threading

from Utils import Boids
from Utils import Stage

def main() -> None:
    stage = Stage(1000, 1000)

    boids : list[Boids] = list()

    for _ in range(100):
        boids.append(Boids(stage.WIDTH, stage.HEIGHT))

    start_time = time.time()

    for _ in range(1_000):
        for boid in boids:
            boid.flock(boids)
            boid.update()
            stage.drawBoid(boid)
        stage.show("Boids Algorithm")

    end_time = time.time()
    print(f'The time it took for 1000 iterations is: {end_time-start_time}sec')

if __name__ == '__main__':
    main()