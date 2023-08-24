import time
import threading

from Utils import Boids
from Utils import Stage


def consolidate(boid, boids, stage) -> None:
    boid.flock(boids)
    boid.update()
    stage.drawBoid(boid)

def main() -> None:
    stage = Stage(1000, 1000)

    boids : list[Boids] = list()

    for _ in range(100):
        boids.append(Boids(stage.WIDTH, stage.HEIGHT))
    
    start_time = time.perf_counter()

    for _ in range(1_000):
        
        threads = list()

        for boid in boids:
            thread = threading.Thread(target=consolidate, args=(boid, boids, stage))   
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
        stage.show("Boids Algorithm")

    end_time = time.perf_counter()
    print(f'The time it took for 1000 iterations is: {end_time-start_time}sec')

if __name__ == '__main__':
    main()