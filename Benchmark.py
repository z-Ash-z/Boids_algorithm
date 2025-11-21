import time
import cv2
import pygame
from Utils import Boids
from Utils import Stage
from Utils.StagePygame import StagePygame

def run_opencv(num_boids=100, steps=500):
    print(f"Running OpenCV benchmark with {num_boids} boids for {steps} steps...")
    stage = Stage(1000, 1000)
    boids = Boids(num_boids, stage.WIDTH, stage.HEIGHT)
    
    start_time = time.perf_counter()
    for _ in range(steps):
        boids.flock()
        boids.update()
        stage.drawBoids(boids)
        stage.show("OpenCV Benchmark", wait_time=1)
    
    cv2.destroyAllWindows()
    duration = time.perf_counter() - start_time
    fps = steps / duration
    print(f"OpenCV: {duration:.4f}s ({fps:.2f} FPS)")
    return fps

def run_pygame(num_boids=100, steps=500):
    print(f"Running Pygame benchmark with {num_boids} boids for {steps} steps...")
    stage = StagePygame(1000, 1000)
    boids = Boids(num_boids, stage.WIDTH, stage.HEIGHT)
    
    start_time = time.perf_counter()
    for _ in range(steps):
        boids.flock()
        boids.update()
        stage.drawBoids(boids)
        stage.show("Pygame Benchmark")
    
    pygame.quit()
    duration = time.perf_counter() - start_time
    fps = steps / duration
    print(f"Pygame: {duration:.4f}s ({fps:.2f} FPS)")
    return fps

def main():
    steps = 500
    num_boids = 100
    
    # Run OpenCV
    fps_cv = run_opencv(num_boids, steps)
    
    # Run Pygame
    fps_pg = run_pygame(num_boids, steps)
    
    print("\n--- Results ---")
    print(f"OpenCV: {fps_cv:.2f} FPS")
    print(f"Pygame: {fps_pg:.2f} FPS")
    
    if fps_pg > fps_cv:
        print(f"Pygame is {fps_pg/fps_cv:.2f}x faster.")
    else:
        print(f"OpenCV is {fps_cv/fps_pg:.2f}x faster.")

if __name__ == "__main__":
    main()
