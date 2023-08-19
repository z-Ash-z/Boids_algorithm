import cv2
import numpy as np

from .Boids import Boids


class Stage:

    def __init__(self, x : int = 500, y : int = 500) -> None:
        """
        This the stage class that takes care of displaying the boids on the stage.

        Args:
            x: The size of the stage in x-axis (width). Defaults to 500.
            y: The size of the stage in y-axis (height). Defaults to 500.
        """
        self.createCanvas(x, y)
        self.WIDTH = x
        self.HEIGHT = y
    
    def createCanvas(self, x : int, y : int) -> None:
        """
        The method that creates the stage using the given dimensions.

        Args:
            x: The size of the stage in x-axis (width).
            y: The size of the stage in y-axis (height).
        """
        self.__stage = np.zeros((y, x), dtype = np.uint8)
    
    def __resetCanvas(self) -> None:
        """
        The method that resets the canvas back to zeros.
        """
        self.createCanvas(self.WIDTH, self.HEIGHT)

    def show(self, window_name : str = "Stage", wait_time : int = 1) -> None:
        """
        The method that shows the stage in a window and resets the stage back to a blank screen. Use 'q' key to close the window.

        Args:
            window_name: The name of the window that pops up. Defaults to "Stage".
            wait_time: The wait time for the window, (use 0 to wait until key press). Defaults to 1.
        """
        cv2.imshow(window_name, self.__stage)
        key = cv2.waitKey(wait_time)
        
        if key == ord('q'):
            exit(0)
        
        self.__resetCanvas()

    def drawBoid(self, boid : Boids) -> None:
        """
        Draws the boids on the window.

        Args:
            boid: The boid that needs to be drawn.
        """
        cv2.circle(self.__stage, (int(boid.position.x), int(boid.position.y)), 5, (255, 255, 255), -1)


def main() -> None:
    stage = Stage(750, 750)
    stage.show(wait_time = 0)
    

if __name__ == '__main__':
    main()