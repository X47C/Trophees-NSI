# Ensemble des methodes servant a faire marcher pygame, on a before game avec les menu et les dispositions pour créer une partie
# on a post game et in game
import Pygame as pg
from .button import Button
class Before_Game:
    """
    permet de gérer l'écran avant le lancement de la partie
    """
    def __init__(self, screen):
        """
        screen = tuple(largueur, hauteur)
        Initialise l'écran avant le lancement de la partie
        """
        self.screen = screen
        self.Button_Left = Button(pg.Rect(0, 0, 50, 50),'Left the game') 
        self.Button_Start = Button(pg.Rect(0, 0, 50, 50),'Start')
        self.bg_asset = pg.image.load('assets/bg_menu.png')
        self.Button_Left_pos = (50, screen.get_height() - 100)
        self.Button_Start_pos = (screen.get_width() - 150, screen.get_height() - 100) 

 