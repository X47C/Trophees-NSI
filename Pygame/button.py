import pygame
from pygame import Rect

class Button:
    """A button UI element."""
    def __init__(self, rect:Rect, text:str):
        self.rect = rect
        self.text = text

    def draw(self, surf, font, bg = (30,144,255)):
        pygame.draw.rect(surf, bg, self.rect, border_radius=8)
        pygame.draw.rect(surf, (0,0,0), self.rect, 2, border_radius=8)
        text_surface = font.render(self.text, True, (255,255,255))
        surf.blit(text_surface, (self.rect.x + (self.rect.w - text_surface.get_width()) // 2, self.rect.y + (self.rect.h - text_surface.get_height()) //  2))

    def collide(self, pos):
        return self.rect.collidepoint(pos)
    
    def is_clicked(self, mouse_pos, button_pos):
        relative_pos = (mouse_pos[0] - button_pos[0], mouse_pos[1] - button_pos[1])
        return self.collide(relative_pos)