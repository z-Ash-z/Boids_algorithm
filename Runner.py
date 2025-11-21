import time
from Utils import Boids
from Utils import Stage


def main() -> None:
    stage = Stage(1000, 1000)

    # Initialize Boids manager with 100 boids
    boids = Boids(100, stage.WIDTH, stage.HEIGHT)
    
    start_time = time.perf_counter()

    for _ in range(1000):
        boids.flock()
        boids.update()
        stage.drawBoids(boids)
        stage.show("Boids Algorithm")

    end_time = time.perf_counter()
    print(f'The time it took for 1000 iterations is: {end_time - start_time}sec')

if __name__ == '__main__':
    main()