# methodes pour gerer la nouriture
import pygame as pg

class Food():
    """
    Entry : position (tupple), is_eaten (bool)
    """
    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.image = pg.image.load('assets/food.png')
        self.rect = self.image.get_rect(center=(int(self.pos_x), int(self.pos_y)))
    
    def draw(self, screen):
        """
        affiche la nourriture
        """
        screen.blit(self.image, self.rect)
