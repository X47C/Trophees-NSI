# Ensemble des methodes servant a faire marcher pygame, on a before game avec les menu et les dispositions pour créer une partie
# on a post game et in game
import Pygame as pg
from .button import Button
class Before_Game:
    """
    permet de gérer la partie
    """
    def __init__(self, screen):
        self.screen = screen
        self.Button_Left = Button(pg.Rect(0, 0, 50, 50),'Left the game') 
        self.Button_Start = Button(pg.Rect(0, 0, 50, 50),'Start')
        
        

