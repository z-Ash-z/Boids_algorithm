import pygame

class UIElement:
    def __init__(self, x, y, w, h, font_size=24):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = pygame.font.Font(None, font_size)
        self.active = False

    def handle_event(self, event):
        pass

    def draw(self, screen):
        pass

class Button(UIElement):
    def __init__(self, x, y, w, h, text, callback, font_size=32):
        super().__init__(x, y, w, h, font_size)
        self.text = text
        self.callback = callback
        self.bg_color = (50, 50, 50)
        self.hover_color = (70, 70, 70)
        self.text_color = (255, 255, 255)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
        elif event.type == pygame.MOUSEMOTION:
            self.active = self.rect.collidepoint(event.pos)

    def draw(self, screen):
        color = self.hover_color if self.active else self.bg_color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2, border_radius=5)
        
        txt_surf = self.font.render(self.text, True, self.text_color)
        text_rect = txt_surf.get_rect(center=self.rect.center)
        screen.blit(txt_surf, text_rect)

class Slider(UIElement):
    def __init__(self, x, y, w, h, min_val, max_val, initial_val, label):
        super().__init__(x, y, w, h, font_size=20)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.label = label
        self.dragging = False
        
        # Handle width/height: h is mostly for the track thickness? 
        # Let's make h the hit area height, but draw a thin line.
        self.handle_radius = h // 2
        
    def get_value(self):
        return self.val

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.update_value(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.update_value(event.pos[0])

    def update_value(self, mouse_x):
        # Clamp mouse_x to rect
        x = max(self.rect.left, min(mouse_x, self.rect.right))
        # Normalize to 0-1
        ratio = (x - self.rect.left) / self.rect.width
        # Map to value
        self.val = self.min_val + ratio * (self.max_val - self.min_val)

    def draw(self, screen):
        # Draw Label
        label_surf = self.font.render(f"{self.label}: {self.val:.3f}", True, (255, 255, 255))
        screen.blit(label_surf, (self.rect.x, self.rect.y - 20))
        
        # Draw Track
        track_rect = pygame.Rect(self.rect.x, self.rect.centery - 2, self.rect.width, 4)
        pygame.draw.rect(screen, (150, 150, 150), track_rect)
        
        # Draw Handle
        ratio = (self.val - self.min_val) / (self.max_val - self.min_val)
        handle_x = self.rect.x + ratio * self.rect.width
        handle_pos = (int(handle_x), self.rect.centery)
        
        color = (200, 200, 200) if self.dragging else (255, 255, 255)
        pygame.draw.circle(screen, color, handle_pos, self.handle_radius)

class InputBox(UIElement):
    def __init__(self, x, y, w, h, text=''):
        super().__init__(x, y, w, h, font_size=32)
        self.text = text
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # print(self.text)
                    pass # Callback handled externally or just read text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    # Only allow numbers
                    if event.unicode.isdigit():
                        self.text += event.unicode

    def draw(self, screen):
        # Render the current text.
        txt_surface = self.font.render(self.text, True, self.color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        self.rect.w = width
        
        # Blit the text.
        screen.blit(txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
