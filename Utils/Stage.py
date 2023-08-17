import cv2
import numpy as np

from .Boids import Boids


class Stage:

    def __init__(self, x : int = 500, y : int = 500) -> None:
        self.createCanvas(x, y)
        self.WIDTH = x
        self.HEIGHT = y
    
    def createCanvas(self, x : int, y : int) -> None:
        self.__stage = np.zeros((y, x), dtype = np.uint8)
    
    def __resetCanvas(self) -> None:
        self.createCanvas(self.WIDTH, self.HEIGHT)

    def show(self, window_name : str = "Stage", wait_time : int = 1) -> None:
        cv2.imshow(window_name, self.__stage)
        key = cv2.waitKey(wait_time)
        
        if key == ord('q'):
            exit(0)
        
        self.__resetCanvas()

    def drawBoid(self, boid : Boids) -> None:
        cv2.circle(self.__stage, (int(boid.position.x), int(boid.position.y)), 5, (255, 255, 255), -1)


def main() -> None:
    stage = Stage(750, 750)
    stage.show(wait_time = 0)
    

if __name__ == '__main__':
    main()