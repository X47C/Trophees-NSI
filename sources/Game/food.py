import pygame as pg

class Food():
    """
    Entrée : position (tuple), is_eaten (bool)
    """
    def __init__(self, x: int, y: int) -> None:
        #position
        self.pos_x = x
        self.pos_y = y

        #affichage
        image = pg.image.load('../data/game/food.png')
        self.image = pg.transform.scale_by(image, (1.5, 1.5))
        self.rect = self.image.get_rect(center=(int(self.pos_x), int(self.pos_y)))


    def draw(self, screen: pg.surface) -> None:
        """
        Dessine la nouriture sur l'écran 'screen'
        """
        screen.blit(self.image, self.rect)