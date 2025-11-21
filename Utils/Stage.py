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

    def drawBoids(self, boids : Boids) -> None:
        """
        Draws the boids on the window as triangles.

        Args:
            boids: The boids manager containing all boids.
        """
        # Clear the stage
        self.__stage.fill(0)
        
        positions = boids.get_positions()
        velocities = boids.velocities
        
        # Calculate angles
        angles = np.arctan2(velocities[:, 1], velocities[:, 0])
        c = np.cos(angles)
        s = np.sin(angles)
        
        # Define offsets for the triangle vertices (N, 2)
        # Tip: (10, 0) -> (10c, 10s)
        tip_x = 10 * c
        tip_y = 10 * s
        
        # Back Left: (-5, 5) -> (-5c - 5s, -5s + 5c)
        bl_x = -5 * c - 5 * s
        bl_y = -5 * s + 5 * c
        
        # Back Right: (-5, -5) -> (-5c + 5s, -5s - 5c)
        br_x = -5 * c + 5 * s
        br_y = -5 * s - 5 * c
        
        # Stack coordinates: (N, 3, 2)
        # We construct the x and y coordinates for all 3 vertices
        # Triangle 1: [tip_x[0], tip_y[0]], [bl_x[0], bl_y[0]], [br_x[0], br_y[0]]
        
        # Create (N, 3, 2) array of offsets
        offsets = np.zeros((len(positions), 3, 2))
        offsets[:, 0, 0] = tip_x
        offsets[:, 0, 1] = tip_y
        offsets[:, 1, 0] = bl_x
        offsets[:, 1, 1] = bl_y
        offsets[:, 2, 0] = br_x
        offsets[:, 2, 1] = br_y
        
        # Add positions to offsets
        # positions is (N, 2) -> expand to (N, 1, 2) for broadcasting
        vertices = (offsets + positions[:, np.newaxis, :]).astype(np.int32)
        
        # cv2.fillPoly expects a list of points, but we can pass the array directly
        # if it's in the right format. It expects a list of arrays.
        # We can convert the (N, 3, 2) array to a list of (3, 2) arrays?
        # Actually, fillPoly is fast but the list conversion might be slow.
        # Let's try passing the list of arrays.
        
        cv2.fillPoly(self.__stage, list(vertices), (255, 255, 255))


def main() -> None:
    stage = Stage(750, 750)
    stage.show(wait_time = 0)
    

if __name__ == '__main__':
    main()