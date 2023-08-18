from Utils import Boids
from Utils import Stage

def main() -> None:
    stage = Stage(1000, 1000)

    boids : list[Boids] = list()

    for _ in range(100):
        boids.append(Boids(stage.WIDTH, stage.HEIGHT))

    while True:
        for boid in boids:
            boid.flock(boids)
            boid.update()
            stage.drawBoid(boid)
        stage.show()

if __name__ == '__main__':
    main()