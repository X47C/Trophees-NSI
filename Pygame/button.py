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
        txt = font.render(self.text, True, (255,255,255))
        surf.blit(txt, (self.rect.x + (self.rect.w - txt.get_width()) // 2, self.rect.y + (self.rect.h - txt.get_height()) //  2))

    def collide(self, pos):
        return self.rect.collidepoint(pos)