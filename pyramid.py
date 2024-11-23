import pygame
import math
import colorsys
import numpy as np

pygame.init()
pygame.mixer.init()
bg_music = pygame.mixer.Sound("bg_music.mp3")
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("PyBox")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
font_large = pygame.font.Font(None, 120)
font_small = pygame.font.Font(None, 40)
CUBE_SIZE = 100
ROTATION_SPEED = 0.02

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
        self.clicked = False
        
    def draw(self, surface):
        color = GRAY if self.is_hovered else BLACK
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 3, border_radius=10)
        text_surface = font_small.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                return True
        return False

class Cube:
    def __init__(self):
        self.vertices = np.array([
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
        ]) * CUBE_SIZE
        self.edges = [
            (0,1), (1,2), (2,3), (3,0),
            (4,5), (5,6), (6,7), (7,4),
            (0,4), (1,5), (2,6), (3,7)
        ]
        self.angle = 0
        
    def rotate(self):
        self.angle += ROTATION_SPEED
        rotation_x = np.array([
            [1, 0, 0],
            [0, np.cos(self.angle), -np.sin(self.angle)],
            [0, np.sin(self.angle), np.cos(self.angle)]
        ])
        rotation_y = np.array([
            [np.cos(self.angle), 0, np.sin(self.angle)],
            [0, 1, 0],
            [-np.sin(self.angle), 0, np.cos(self.angle)]
        ])
        rotated = np.dot(self.vertices, rotation_x)
        rotated = np.dot(rotated, rotation_y)
        
        projected = []
        for point in rotated:
            x = point[0] + 400
            y = point[1] + 300
            projected.append((x, y))
        return projected

    def draw(self, surface, hue):
        points = self.rotate()
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        color = tuple(int(255 * x) for x in rgb)
        for edge in self.edges:
            start = points[edge[0]]
            end = points[edge[1]]
            pygame.draw.line(surface, color, start, end, 2)

class Pyramid:
    def __init__(self):
        self.vertices = np.array([
            [-1, -1, -1],  # Base
            [1, -1, -1],   # Base
            [1, -1, 1],    # Base
            [-1, -1, 1],   # Base
            [0, 1, 0]      # Apex
        ]) * CUBE_SIZE
        
        self.edges = [
            (0,1), (1,2), (2,3), (3,0),  # Base edges
            (0,4), (1,4), (2,4), (3,4)   # Edges to apex
        ]
        self.angle = 0

    def rotate(self):
        rotation_x = np.array([
            [1, 0, 0],
            [0, np.cos(self.angle), -np.sin(self.angle)],
            [0, np.sin(self.angle), np.cos(self.angle)]
        ])
        rotation_y = np.array([
            [np.cos(self.angle), 0, np.sin(self.angle)],
            [0, 1, 0],
            [-np.sin(self.angle), 0, np.cos(self.angle)]
        ])
        rotated = np.dot(self.vertices, rotation_x)
        rotated = np.dot(rotated, rotation_y)
        
        projected = []
        for point in rotated:
            x = point[0] + 400
            y = point[1] + 300
            projected.append((x, y))
        
        self.angle += ROTATION_SPEED
        return projected

    def draw(self, surface, hue):
        points = self.rotate()
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        color = tuple(int(255 * x) for x in rgb)
        for edge in self.edges:
            start = points[edge[0]]
            end = points[edge[1]]
            pygame.draw.line(surface, color, start, end, 2)

def draw_3d_text(surface, text, x, y, hue):
    rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    main_color = tuple(int(255 * x) for x in rgb)
    depth = 10
    for i in range(depth, 0, -1):
        offset = i * 2
        shadow = font_large.render(text, True, (50, 50, 50))
        surface.blit(shadow, (x + offset, y + offset))
    text_surface = font_large.render(text, True, main_color)
    surface.blit(text_surface, (x, y))

def draw_escape_text(surface, text):
    escape_text = font_small.render(text, True, WHITE)
    text_rect = escape_text.get_rect()
    text_rect.bottomright = (780, 580)
    surface.blit(escape_text, text_rect)

def main():
    screen_width = 800
    screen_height = 600
    button_width = 200
    button_height = 50
    button_y = screen_height - 300
    

    button_spacing = 20  
    total_width = (button_width * 2) + button_spacing
    start_x = (screen_width - total_width) // 2

    
    cube_button = Button(start_x, button_y, button_width, button_height, "Cube")
    pyramid_button = Button(start_x + button_width + button_spacing, button_y, button_width, button_height, "Pyramid")

    coming_soon_text = "More Coming Soon!"
    text_surface = font_small.render(coming_soon_text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = screen_width // 2
    text_rect.top = button_y + button_height + 20

    pyramid = Pyramid()
    show_pyramid = False
    
    hue = 0
    running = True
    
    bg_music.play(-1)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if not show_pyramid:
                if pyramid_button.handle_event(event):
                    show_pyramid = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if show_pyramid:
                        show_pyramid = False
                    else:
                        running = False

        screen.fill(BLACK)
        
        if show_pyramid:
            pyramid.draw(screen, hue)
            draw_escape_text(screen, "Press ESCAPE to exit")
        else:
            draw_3d_text(screen, "PyBox", 250, 150, hue)
            pyramid_button.rect.centerx = screen_width // 2
            pyramid_button.rect.centery = screen_height // 2
            pyramid_button.draw(screen)
            screen.blit(text_surface, text_rect)
            draw_escape_text(screen, "Press ESCAPE to quit")
        
        hue = (hue + 0.01) % 1.0
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
