import time
import pygame
from Utils import Boids
from Utils.StagePygame import StagePygame
from Utils.UI import Button, Slider, InputBox

def main() -> None:
    # Initialize Stage (fullscreen=False for now to see window borders/resizing)
    stage = StagePygame(width=1000, height=800, fullscreen=False)
    
    # Game States
    STATE_MENU = 0
    STATE_SIMULATION = 1
    current_state = STATE_MENU
    
    # --- Menu UI ---
    # Center input box and button
    cx, cy = stage.WIDTH // 2, stage.HEIGHT // 2
    input_box = InputBox(cx - 100, cy - 50, 200, 50, text='500')
    
    def start_sim():
        nonlocal current_state, boids
        try:
            num = int(input_box.text)
        except ValueError:
            num = 100 # Default if invalid
        
        # Initialize Boids
        boids = Boids(num, stage.WIDTH, stage.HEIGHT)
        
        # Update Sliders with initial boid values
        slider_align.val = boids.MAX_ALIGNMENT_FORCE
        slider_coh.val = boids.MAX_COHESION_FORCE
        slider_sep.val = boids.MAX_SEPERATION_FORCE
        
        current_state = STATE_SIMULATION

    start_btn = Button(cx - 100, cy + 20, 200, 50, "Start Simulation", start_sim)
    
    # --- Simulation UI ---
    # Sliders for Alignment, Cohesion, Separation
    # Range: 0.0 to 0.1 (approx)
    slider_align = Slider(20, 20, 200, 20, 0.0, 0.05, 0.01, "Alignment")
    slider_coh = Slider(20, 60, 200, 20, 0.0, 0.05, 0.015, "Cohesion")
    slider_sep = Slider(20, 100, 200, 20, 0.0, 0.5, 0.1, "Separation")
    # FPS Slider: 10 to 120 FPS, default 60
    slider_fps = Slider(20, 140, 200, 20, 10, 120, 60, "Max FPS")
    
    def back_to_menu():
        nonlocal current_state
        current_state = STATE_MENU
        
    back_btn = Button(20, 180, 100, 40, "Back", back_to_menu, font_size=24)
    
    boids = None # Will be init in start_sim
    
    start_time = time.perf_counter()
    running = True
    
    while running:
        # Event Handling
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                stage.resize(width, height)
                if boids:
                    boids.WIDTH = width
                    boids.HEIGHT = height
                # Re-center menu items if in menu
                if current_state == STATE_MENU:
                    cx, cy = width // 2, height // 2
                    input_box.rect.topleft = (cx - 100, cy - 50)
                    start_btn.rect.topleft = (cx - 100, cy + 20)

            # Pass events to UI
            if current_state == STATE_MENU:
                input_box.handle_event(event)
                start_btn.handle_event(event)
            elif current_state == STATE_SIMULATION:
                slider_align.handle_event(event)
                slider_coh.handle_event(event)
                slider_sep.handle_event(event)
                slider_fps.handle_event(event)
                back_btn.handle_event(event)

        # Logic & Rendering
        if current_state == STATE_MENU:
            stage.screen.fill((30, 30, 30)) # Dark background
            
            # Draw Title
            font = pygame.font.Font(None, 64)
            title = font.render("Boids Simulation", True, (255, 255, 255))
            title_rect = title.get_rect(center=(stage.WIDTH//2, stage.HEIGHT//2 - 150))
            stage.screen.blit(title, title_rect)
            
            input_box.draw(stage.screen)
            start_btn.draw(stage.screen)
            
            pygame.display.flip()
            
        elif current_state == STATE_SIMULATION:
            # Update Boid Parameters from Sliders
            if boids:
                boids.MAX_ALIGNMENT_FORCE = slider_align.get_value()
                boids.MAX_COHESION_FORCE = slider_coh.get_value()
                boids.MAX_SEPERATION_FORCE = slider_sep.get_value()
            
                boids.flock()
                boids.update()
                stage.drawBoids(boids)
                
                # Draw UI on top
                slider_align.draw(stage.screen)
                slider_coh.draw(stage.screen)
                slider_sep.draw(stage.screen)
                slider_fps.draw(stage.screen)
                back_btn.draw(stage.screen)
                
                stage.show("Boids Algorithm") # This flips display
                
                # Cap FPS
                stage.clock.tick(int(slider_fps.get_value()))

    end_time = time.perf_counter()
    # print(f'The Simulation time: {end_time - start_time}sec')
    pygame.quit()

if __name__ == '__main__':
    main()