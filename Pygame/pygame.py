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

        self.Button_exit = Button(Rect(self.width // 2 - 110, self.height // 2 - 40, 220, 80),'Exit') 
        self.Button_Start = Button(Rect(self.width // 2 - 110, self.height // 2 - 130, 220, 80),'Start')
        self.Button_credits = Button(Rect(self.width // 2 - 110, self.height // 2 + 50, 220, 80),'Credits') 
        self.Button_credits_exit = Button(Rect(self.width // 2 - 65, self.height // 2 + 130, 130, 50),'Back')
        
        # self.bg_asset = pg.image.load('assets/bg_menu.png')
        self.bg_asset = pg.Surface((self.width, self.height))
        self.bg_asset.fill((100, 149, 237))

        self.Button_font = pg.font.SysFont(settings.Button_font, settings.Button_font_size)


    def draw(self):
        """
        Dessine l'écran avant le lancement de la partie
        """
        self.screen.blit(self.bg_asset, (0, 0))
        self.Button_exit.draw(self.screen, self.Button_font)
        self.Button_Start.draw(self.screen, self.Button_font)
        self.Button_credits.draw(self.screen, self.Button_font)

    def handle_event(self, event):
        """
        Gère les événements de l'écran avant le lancement de la partie
        """
        match event.type:
            case pg.MOUSEBUTTONDOWN:
                if self.Button_exit.rect.collidepoint(event.pos):  
                    return 'exit'
                if self.Button_Start.rect.collidepoint(event.pos):
                    return 'start'
                if self.Button_credits.rect.collidepoint(event.pos):
                    return 'credits'
                if self.Button_credits_exit.rect.collidepoint(event.pos):
                    return 'home'
                
    def credits(self):
        """
        Affiche les crédits du jeu
        A modifier avec une image quand on en aura une
        """
        pg.draw.rect(self.screen, (255,255,255), (100,100, self.width - 200, self.height - 200))
        self.Button_credits_exit.draw(self.screen, self.Button_font)
        for i in range(len(settings.Credits_Text)):
            self.screen.blit(pg.font.SysFont(settings.Credits_font, settings.Credits_font_size).render(settings.Credits_Text[i], True, (0,0,0)), (self.width // 2 - 150, 130 + 80 * i))
        


class Settings:
    """
    permet de gérer l'écran des paramètres avant la partie
    """
    def __init__(self, screen):
        """
        screen = tuple(largueur, hauteur)
        Initialise l'écran des paramètres avant la partie
        """
        self.width, self.height = settings.Display_size
        self.screen = screen

        # self.bg_asset = pg.image.load('assets/bg_settings.png')
        self.bg_asset = pg.Surface(settings.Display_size)
        self.bg_asset.fill((200, 200, 200))

        self.Start_Button = Button(pg.Rect(300, 500, 200, 50), 'Start Simulation')
        self.Button_font = pg.font.SysFont(settings.Button_font, settings.Button_font_size)

    def draw(self):
        """
        Dessine l'écran des paramètres avant la partie
        """
        self.screen.blit(self.bg_asset, (0, 0))
        self.Start_Button.draw(self.screen, self.Button_font)

    def handle_event(self, event):
        """
        Gère les événements de l'écran des paramètres avant la partie
        """
        match event.type:
            case pg.MOUSEBUTTONDOWN:
                if self.Start_Button.rect.collidepoint(event.pos):
                    return 'start'
        
            

class In_Game:
    """
    permet de gérer l'écran pendant la partie
    """
    def __init__(self, screen):
        """
        screen = tuple(largueur, hauteur)
        Initialise l'écran pendant la partie
        """
        self.width, self.height = settings.Display_size
        self.screen = screen
        
        # self.bg_asset = pg.image.load('assets/bg_in_game.png')
        self.bg_asset = pg.Surface(settings.Display_size)
        self.bg_asset.fill((34, 139, 34))

        self.continue_button = Button(pg.Rect(700, 10, 90, 40), 'End')
        self.Button_font = pg.font.SysFont(settings.Button_font, settings.Button_font_size)

    def draw(self):
        """
        Dessine l'écran pendant la partie
        """
        self.screen.blit(self.bg_asset, (0, 0))
        self.continue_button.draw(self.screen, self.Button_font)

    def handle_event(self, event):
        """
        Gère les événements de l'écran pendant la partie
        """
        match event.type:
            case pg.MOUSEBUTTONDOWN:
                if self.continue_button.rect.collidepoint(event.pos):
                    return 'end'
                


class Post_Game:
    """
    permet de gérer l'écran après la partie
    """
    def __init__(self, screen):
        """
        screen = tuple(largueur, hauteur)
        Initialise l'écran après la partie
        """
        self.width, self.height = settings.Display_size
        self.screen = screen

        # self.bg_asset = pg.image.load('assets/bg_post_game.png')
        self.bg_asset = pg.Surface(settings.Display_size)
        self.bg_asset.fill((128, 0, 128))

        self.Button_exit = Button(Rect(self.width // 2 - 110, self.height // 2 + 40, 220, 80), 'Exit to Desktop')
        self.Button_home = Button(Rect(self.width // 2 - 110, self.height // 2 + 130, 220, 80), 'Return to Home')

        self.Button_font = pg.font.SysFont(settings.Button_font, settings.Button_font_size)


    def draw(self):
        """
        Dessine l'écran après la partie
        """
        self.screen.blit(self.bg_asset, (0, 0))
        
        self.Button_exit.draw(self.screen, self.Button_font)
        self.Button_home.draw(self.screen, self.Button_font)

    def handle_event(self, event):
        """
        Gère les événements de l'écran après la partie
        """
        match event.type:
            case pg.MOUSEBUTTONDOWN:
                if self.Button_exit.rect.collidepoint(event.pos):
                    return 'exit'
                if self.Button_home.rect.collidepoint(event.pos):
                    return 'home'
