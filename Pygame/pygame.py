# Ensemble des methodes servant a faire marcher pygame, on a before game avec les menu et les dispositions pour créer une partie
# on a post game et in game
import pygame as pg
from .button import Button
from pygame import Rect
import settings

class Before_Game:
    """
    permet de gérer l'écran avant le lancement de la partie
    """
    def __init__(self, screen):
        """
        screen = tuple(largueur, hauteur)
        Initialise l'écran avant le lancement de la partie
        """
        self.width, self.height = settings.Display_size
        self.screen = screen
        self.Button_Left = Button(Rect(self.width // 2 - 110, self.height // 2 - 40, 220, 80),'Left the game') 
        self.Button_Start = Button(Rect(0, 0, 50, 50),'Start')
        # self.bg_asset = pg.image.load('assets/bg_menu.png')
        self.bg_asset = pg.Surface((self.width, self.height))
        self.bg_asset.fill((100, 149, 237))
        self.Button_font = pg.font.SysFont('arial', 40, bold=True)

    def draw(self):
        """
        Dessine l'écran avant le lancement de la partie
        """
        self.screen.blit(self.bg_asset, (0, 0))
        self.Button_Left.draw(self.screen, self.Button_font)
        self.Button_Start.draw(self.screen, self.Button_font)

    def handle_event(self, event):
        """
        Gère les événements de l'écran avant le lancement de la partie
        """
        if event.type == pg.MOUSEBUTTONUP:
            if self.Button_Left.rect.collidepoint(event.pos):  
                return 'left'
            if self.Button_Start.is_clicked(event.pos, Rect(0, 0, 50, 50)):
                return 'start'
        if event.type == pg.QUIT:
            return 'left'
        

class In_Game:
    """
    permet de gérer l'écran pendant la partie
    """
    def __init__(self, screen):
        """
        screen = tuple(largueur, hauteur)
        Initialise l'écran pendant la partie
        """
        self.screen = screen
        self.bg_asset = pg.image.load('assets/bg_game.png')

    def draw(self):
        """
        Dessine l'écran pendant la partie
        """
        self.screen.blit(self.bg_asset, (0, 0))


class Post_Game:
    """
    permet de gérer l'écran après la partie
    """
    def __init__(self, screen):
        """
        screen = tuple(largueur, hauteur)
        Initialise l'écran après la partie
        """
        self.screen = screen
        self.Button_Exit = Button(pg.Rect(0, 0, 50, 50),'Exit') 
        self.bg_asset = pg.image.load('assets/bg_post_game.png')
        self.Button_Exit_pos = (screen.get_width() // 2 - 25, screen.get_height() // 2 - 25)
        self.Button_font = pg.font.SysFont('arial', 40, bold=True)

    def draw(self):
        """
        Dessine l'écran après la partie
        """
        self.screen.blit(self.bg_asset, (0, 0))
        self.Button_Exit.draw(self.screen, self.Button_font)

    def handle_event(self, event):
        """
        Gère les événements de l'écran après la partie
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.Button_Exit.is_clicked(event.pos, self.Button_Exit_pos):
                return 'exit'
        return None
