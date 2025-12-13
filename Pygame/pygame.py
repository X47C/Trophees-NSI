# Ensemble des methodes servant a faire marcher pygame, on a before game avec les menu et les dispositions pour créer une partie
# on a post game et in game
import pygame as pg
from Pygame.button import Button
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

        self.Button_exit = Button(Rect(self.width // 2 - 110, self.height // 2 - 40, 220, 80),'Exit', self.screen)
        self.Button_Start = Button(Rect(self.width // 2 - 110, self.height // 2 - 130, 220, 80),'Start', self.screen)
        self.Button_credits = Button(Rect(self.width // 2 - 110, self.height // 2 + 50, 220, 80),'Credits', self.screen) 
        self.Button_credits_exit = Button(Rect(self.width // 2 - 65, self.height // 2 + 130, 130, 50),'Back', self.screen)
        
        self.bg_asset = pg.image.load('assets/before-game-background.png')

        self.Button_font = pg.font.SysFont(settings.Button_font, settings.Button_font_size)


    def draw(self):
        """
        Dessine l'écran avant le lancement de la partie
        """
        self.screen.blit(self.bg_asset, (0, 0))
        self.Button_exit.draw(self.screen, self.Button_font, 'assets/button-exit.png')
        self.Button_Start.draw(self.screen, self.Button_font, 'assets/button-start.png')
        self.Button_credits.draw(self.screen, self.Button_font, 'assets/button-credits.png')

    def handle_event(self, event):
        """
        Gère les événements de l'écran avant le lancement de la partie
        """
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
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
    """
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = settings.Display_size

        # ratio gauche / droite 
        self.left_ratio = max(0.1, 0.75)
        self.left_width = int(self.width * self.left_ratio)
        self.right_width = self.width - self.left_width
        self.left_rect = Rect(0, 0, self.left_width, self.height)
        self.right_rect = Rect(self.left_width, 0, self.right_width, self.height)

        # fond global 
        self.bg_asset = pg.Surface((self.width, self.height))
        self.bg_asset.fill((200, 200, 200))

        # fond gauche
        # self.left_bg_surface = pg.image.load('assets/left_bg.png').convert()
        # self.left_bg_surface = pg.transform.scale(self.left_bg_surface, (self.left_width, self.content_height))
        self.left_bg_surface = pg.Surface((self.left_width, self.height))
        self.left_bg_surface.fill((230, 230, 230)) 

        # fond droit
        # self.right_bg_surface = pg.image.load('assets/right_bg.png').convert()
        # self.right_bg_surface = pg.transform.scale(self.right_bg_surface, (self.right_width, self.height))
        self.right_bg_surface = pg.Surface((self.right_width, self.height))
        self.right_bg_surface.fill((200, 200, 200)) 

        # police pour textes de boutons 
        self.Button_font = pg.font.SysFont(settings.Button_font, settings.Button_font_size)

        # police pour labels au-dessus des boutons gauches 
        self.Settings_label_font = pg.font.SysFont(settings.Button_label_font, settings.Button_label_font_size)

        # boutons colonne droite 
        self.Start_Button = Button(Rect(self.left_width + (self.right_width - 220) // 2, self.height // 2 - 90, 220, 80),'Start Simulation', self.screen)
        self.Back_Button = Button(Rect(self.left_width + (self.right_width - 220) // 2, self.height // 2 + 90, 220, 80),'Back', self.screen)

        # zone gauche 
        self.left_padding = 16
        self.button_height = 72
        self.button_spacing = 500

        # position manuelle des boutons 
        y = 60
        btn_w_left = self.left_width - 2 * self.left_padding - 18  # laisse place au scrollbar

        # Boutons Gauches
        self.Left_Button_1 = Button(Rect(self.left_padding, y, btn_w_left, self.button_height),'Button Gauche 1') 
        y += self.button_height + 60 + self.button_spacing # a mettre entre chaques etages de boutons
        self.Left_Button_2 = Button(Rect(self.left_padding, y, btn_w_left, self.button_height),'Button Gauche 2')
        y += self.button_height + 60 + self.button_spacing
        self.Left_Button_3 = Button(Rect(self.left_padding, y, btn_w_left, self.button_height),'Button Gauche 2')
        y += self.button_height + 60 + self.button_spacing
        self.Left_Button_4 = Button(Rect(self.left_padding, y, btn_w_left, self.button_height),'Button Gauche 4')
        y += self.button_height + 20 #A ABSOLUMENT LAISSER A LA FIN DES BOUTONS

        # labek au dessus des boutons, garder la bonne forme : Nom_Button_label
        self.Left_Button_1_label = "bouton 1 chockbar"
        self.Left_Button_2_label = "J'aurais pas pu deviner que c'etait le deucx"
        self.Left_Button_3_label = "C'est bien centré ?"
        self.Left_Button_4_label = "c'est le bouton 4"

        # calcul hauteur du contenu et création de la surface interne
        self.content_height = max(self.height, y)
        self.content_surface = pg.Surface((self.left_width, self.content_height), flags=pg.SRCALPHA)
        self.content_surface.blit(self.left_bg_surface, (0,0))

        # scroll
        self.scroll_offset = 0
        self.max_scroll = max(0, self.content_height - self.height)
        self.wheel_step = 30

        # scrollbar visuelle
        self.scrollbar_w = 14
        self.scrollbar_track_rect = Rect(self.left_width - self.scrollbar_w - 4, 8,self.scrollbar_w, self.height - 16)
        self.dragging_thumb = False
        self.drag_mouse_y = 0
        self.thumb_rect = self._compute_thumb_rect()

    def _compute_thumb_rect(self):
        """
        scrollbar helpers ( chiant de fou je suis mort )
        """
        track = self.scrollbar_track_rect
        if self.content_height <= self.height:
            return Rect(track.x, track.y, track.w, track.h)
        view_ratio = self.height / self.content_height
        thumb_h = max(24, int(track.h * view_ratio))
        max_travel = track.h - thumb_h
        if self.max_scroll == 0:
            thumb_y = track.y
        else:
            thumb_y = track.y + int((self.scroll_offset / self.max_scroll) * max_travel)
        return Rect(track.x, thumb_y, track.w, thumb_h)

    def _clamp_scroll(self):
        self.max_scroll = max(0, self.content_height - self.height)
        self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
        self.thumb_rect = self._compute_thumb_rect()


    def draw(self):
        # fond global (fallback)
        self.screen.blit(self.bg_asset, (0, 0))

        # fond de gauche
        self.screen.blit(self.left_bg_surface, (0, 0))

        # fond de droite
        self.screen.blit(self.right_bg_surface, (self.left_width, 0))

        # redessine le contenu gauche sur la content_surface 
        self.content_surface.blit(self.left_bg_surface, (0,0))

        # Le texte au desssu des boutons, a copier coller pour chaques boutons meme si pas de texte plzzzz
        if self.Left_Button_1_label:
            label_surf = self.Settings_label_font.render(self.Left_Button_1_label, True, (0,0,0))
            label_pos = (self.Left_Button_1.rect.x, self.Left_Button_1.rect.y - label_surf.get_height() - 6)
            self.content_surface.blit(label_surf, label_pos)
        self.Left_Button_1.draw(self.content_surface, self.Button_font)
        if self.Left_Button_2_label:
            label_surf = self.Settings_label_font.render(self.Left_Button_2_label, True, (0,0,0))
            label_pos = (self.Left_Button_2.rect.x, self.Left_Button_2.rect.y - label_surf.get_height() - 6)
            self.content_surface.blit(label_surf, label_pos)
        self.Left_Button_2.draw(self.content_surface, self.Button_font)
        if self.Left_Button_3_label:
            label_surf = self.Settings_label_font.render(self.Left_Button_3_label, True, (0,0,0))
            label_pos = (self.Left_Button_3.rect.x, self.Left_Button_3.rect.y - label_surf.get_height() - 6)
            self.content_surface.blit(label_surf, label_pos)
        self.Left_Button_3.draw(self.content_surface, self.Button_font)
        if self.Left_Button_4_label:
            label_surf = self.Settings_label_font.render(self.Left_Button_4_label, True, (0,0,0))
            label_pos = (self.Left_Button_4.rect.x, self.Left_Button_4.rect.y - label_surf.get_height() - 6)
            self.content_surface.blit(label_surf, label_pos)
        self.Left_Button_4.draw(self.content_surface, self.Button_font)

        # blit de la portion visible (viewport)
        visible_src = Rect(0, self.scroll_offset, self.left_width, self.height)
        self.screen.blit(self.content_surface, (self.left_rect.x, self.left_rect.y), area=visible_src)

        # dessine scrollbar
        pg.draw.rect(self.screen, (210, 210, 210), self.scrollbar_track_rect, border_radius=6)
        self.thumb_rect = self._compute_thumb_rect()
        pg.draw.rect(self.screen, (170, 170, 170), self.thumb_rect, border_radius=6)

        # séparation colonne
        pg.draw.line(self.screen, (160, 160, 160), (self.left_width, 0), (self.left_width, self.height), 2)

        # colonne droite (fixe)
        # si tu veux un fond image pour la droite, remplace right_bg_surface comme indiqué plus haut
        self.Start_Button.draw(self.screen, self.Button_font, 'assets/button-start.png')
        self.Back_Button.draw(self.screen, self.Button_font)

    def handle_event(self, event):
        # Boutons droite
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if self.Start_Button.rect.collidepoint(event.pos):
                return 'start'
            if self.Back_Button.rect.collidepoint(event.pos):
                return 'back'

        # molette 
        if event.type == pg.MOUSEWHEEL:
            mx, my = pg.mouse.get_pos()
            if self.left_rect.collidepoint((mx, my)):
                self.scroll_offset -= event.y * self.wheel_step
                self._clamp_scroll()
                return None

        # # fallback molette (boutons 4/5)
        if event.type == pg.MOUSEBUTTONUP and event.button in (4, 5):
            if self.left_rect.collidepoint(event.pos):
                if event.button == 4:
                    self.scroll_offset -= self.wheel_step
                else:
                    self.scroll_offset += self.wheel_step
                self._clamp_scroll()
                return None

        # Boutons gauches ( galere )
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if self.left_rect.collidepoint(event.pos):
                rel_x = event.pos[0] - self.left_rect.x
                rel_y = event.pos[1] - self.left_rect.y + self.scroll_offset

                if self.Left_Button_1.rect.collidepoint((rel_x, rel_y)):
                    return "left:Button Gauche 1"
                if self.Left_Button_2.rect.collidepoint((rel_x, rel_y)):
                    return "left:Button Gauche 2"
                if self.thumb_rect.collidepoint(event.pos):
                    self.dragging_thumb = True
                    self.drag_mouse_y = event.pos[1] - self.thumb_rect.y
                    return None

        # drag thumb
        if event.type == pg.MOUSEMOTION and self.dragging_thumb:
            track = self.scrollbar_track_rect
            new_y = event.pos[1] - self.drag_mouse_y
            new_y = max(track.y, min(track.y + track.h - self.thumb_rect.h, new_y))
            self.thumb_rect.y = new_y
            max_travel = track.h - self.thumb_rect.h
            if max_travel > 0:
                ratio = (self.thumb_rect.y - track.y) / max_travel
                self.scroll_offset = int(ratio * self.max_scroll)
            else:
                self.scroll_offset = 0
            self._clamp_scroll()
            return None

        # relâchement souris -> stop drag
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if self.dragging_thumb:
                self.dragging_thumb = False
                return None

        return None

        
            

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

        self.continue_button = Button(Rect(self.width - self.width // 17, self.height // 60, 90, 40), 'End', self.screen)
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
        if event.type == pg.MOUSEBUTTONUP and event.button == 1 :        
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

        self.Button_exit = Button(Rect(self.width // 2 - 110, self.height // 2 + 40, 220, 80), 'Exit to Desktop', self.screen)
        self.Button_home = Button(Rect(self.width // 2 - 110, self.height // 2 + 130, 220, 80), 'Return to Home', self.screen)

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
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if self.Button_exit.rect.collidepoint(event.pos):
                return 'exit'
            if self.Button_home.rect.collidepoint(event.pos):
                return 'home'



