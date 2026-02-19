import pygame as pg

class Food():
    """
    Entry : position (tupple), is_eaten (bool)
    """
    def __init__(self, x: int, y: int) -> None:
        #position
        self.pos_x = x
        self.pos_y = y

        #affichage
        self.image = pg.image.load('assets/food.png')
        self.rect = self.image.get_rect(center=(int(self.pos_x), int(self.pos_y)))
    

    def draw(self, screen: pg.surface) -> None:
        """
        Dessine la nouriture sur l'écran 'screen'
        """
        screen.blit(self.image, self.rect)
