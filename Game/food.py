# methodes pour gerer la nouriture
import pygame as pg
import settings

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

    def __del__(self):
        """
        detruit la nourriture
        """
        pass

    def new_position(self, position):
        """
        modifie la position de la nouriture
        """
        self.position = position


    def is_alive(self):
        """
        affiche si la nourriture à était manger true pour oui false pour non
        """
        return self.is_eaten