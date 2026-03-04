import pygame as pg
import settings
from pygame import Rect

class Toolbox:
    """
    Menu burger en bas à gauche de l'écran.
    Permet de modifier des options en temps réel pendant la simulation.
    """

    # Dimensions du bouton burger
    BURGER_W = 50
    BURGER_H = 50

    # Dimensions du panel ouvert
    PANEL_W  = 460
    PANEL_H  = 260

    # Hauteur d'une ligne de bouton
    ROW_H = 38

    # Vitesses disponibles
    SPEED_OPTIONS = [0.5, 1, 2, 4, 8, 16]

    # --- Images des boutons (None = pas d'image, str = chemin vers l'asset) ---
    # Ordre : [btn_day, btn_crea, btn_food, btn_vision, btn_end]
    # Exemple : BUTTON_ASSETS = [None, None, None, None, 'assets/end.png']
    # Et hop un quatrieme car jamais 3 sans 4
    BUTTON_ASSETS = [None, None, None, None, None]

    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = settings.Display_size
        self.open = False

        # Polices
        self.font = pg.font.SysFont(settings.Button_font, 15)
        self.font_small = pg.font.SysFont(settings.Button_font, 13)

        # self.bg_image = pg.image.load('assets/toolbox_bg.png').convert_alpha()
        self.bg_image = None  # Remplacer None par le chemin de l'image

        # Position 
        bx = 10
        by = self.height - self.BURGER_H - 10
        self.burger_rect = Rect(bx, by, self.BURGER_W, self.BURGER_H)

        # Panel s'ouvre vers le haut depuis le burger
        px = 10
        py = by - self.PANEL_H - 8
        self.panel_rect = Rect(px, py, self.PANEL_W, self.PANEL_H)

        self._build_controls()

    def _build_controls(self):
        """
        Construit les Rect de tous les boutons du panel.
        """
        px, py = self.panel_rect.x, self.panel_rect.y
        pad = 14

        # Titre centré en haut du panel
        self.title_pos = (px + self.PANEL_W // 2, py + 10)

        # --- Ligne 1 : 3 toggles données (Jour / Créatures / Nourriture) ---
        y1 = py + 40
        btn_w = (self.PANEL_W - pad * 2 - 10) // 3
        self.btn_day  = Rect(px + pad, y1, btn_w, self.ROW_H)
        self.btn_crea = Rect(px + pad + btn_w + 5, y1, btn_w, self.ROW_H)
        self.btn_food = Rect(px + pad + (btn_w+5)*2, y1, btn_w, self.ROW_H)

        # --- Ligne 2 : toggle champ de vision ---
        y2 = y1 + self.ROW_H + 10
        self.btn_vision = Rect(px + pad, y2, self.PANEL_W - pad * 2, self.ROW_H)

        # --- Ligne 3 : vitesses de simulation ---
        y3 = y2 + self.ROW_H + 20   
        n  = len(self.SPEED_OPTIONS)
        sp_w = (self.PANEL_W - pad * 2 - (n - 1) * 5) // n
        self.speed_rects = [Rect(px + pad + i * (sp_w + 5), y3, sp_w, self.ROW_H)for i in range(n)]
        # Position du label "Vitesse :" au dessus des boutons
        self.speed_label_pos = (px + pad, y3 - 16)

        # --- Ligne 4 : fin du jeu ---
        y4 = y3 + self.ROW_H + 10
        self.btn_end = Rect(px + pad, y4, self.PANEL_W - pad * 2, self.ROW_H)


    def _draw_toggle(self, rect, label, active, asset = None, active_color = (80, 200, 120), inactive_color = (80, 80, 80)):
        """
        Dessine un bouton toggle (vert si actif, gris sinon )
        """
        if asset:
            # --- Image sur le bouton ---
            img = pg.image.load(asset).convert_alpha()
            img = pg.transform.smoothscale(img, (rect.width, rect.height))
            self.screen.blit(img, (rect.x, rect.y))
            # Overlay coloré semi-transparent pour l'état
            overlay = pg.Surface((rect.width, rect.height), pg.SRCALPHA)
            overlay.fill((*active_color, 80) if active else (0, 0, 0, 120))
            self.screen.blit(overlay, (rect.x, rect.y))
        else:
            color = active_color if active else inactive_color
            pg.draw.rect(self.screen, color, rect, border_radius=8)

        # Bordure
        border_color = (200, 230, 200) if active else (120, 120, 120)
        pg.draw.rect(self.screen, border_color, rect, 2, border_radius=8)

        # Texte centré
        txt = self.font_small.render(label, True, (255, 255, 255))
        self.screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))


    def _draw_speed_btn(self, rect, label, active):
        """
        Dessine un bouton de vitesse (bleu si sélectionné, sombre sinon).
        """
        color = (60, 140, 220) if active else (60, 60, 90)
        border = (140, 180, 240) if active else (100, 100, 130)
        pg.draw.rect(self.screen, color,  rect, border_radius=6)
        pg.draw.rect(self.screen, border, rect, 2, border_radius=6)
        txt = self.font.render(label, True, (255, 255, 255))
        self.screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))


    def draw(self):
        """
        Dessine le bouton burger et, si ouvert, le panel de la toolbox.
        """
        # --- Bouton burger (toujours visible) ---
        surf = pg.Surface((self.BURGER_W, self.BURGER_H), pg.SRCALPHA)
        pg.draw.rect(surf, (40, 40, 65, 215), (0, 0, self.BURGER_W, self.BURGER_H), border_radius = 10)
        pg.draw.rect(surf, (120, 140, 200, 180), (0, 0, self.BURGER_W, self.BURGER_H), 2, border_radius = 10)
        # Trois lignes horizontales
        for dy in [12, 21, 30]:
            pg.draw.line(surf, (220, 220, 240), (10, dy), (self.BURGER_W - 10, dy), 3)
        self.screen.blit(surf, (self.burger_rect.x, self.burger_rect.y))

        if not self.open:
            return

        # --- Fond du panel ---
        panel_surf = pg.Surface((self.PANEL_W, self.PANEL_H), pg.SRCALPHA)

        if self.bg_image:
            img = pg.transform.smoothscale(self.bg_image, (self.PANEL_W, self.PANEL_H))
            panel_surf.blit(img, (0, 0))
            # sombre pour lisibilité mais ça se change
            overlay = pg.Surface((self.PANEL_W, self.PANEL_H), pg.SRCALPHA)
            overlay.fill((0, 0, 0, 130))
            panel_surf.blit(overlay, (0, 0))
        else:
            # Fond dégradé sombre semi-transparent
            pg.draw.rect(panel_surf, (20, 20, 40, 220), (0, 0, self.PANEL_W, self.PANEL_H), border_radius=14)

        pg.draw.rect(panel_surf, (100, 120, 180, 180), (0, 0, self.PANEL_W, self.PANEL_H), 2, border_radius=14)
        self.screen.blit(panel_surf, (self.panel_rect.x, self.panel_rect.y))

        # --- Titre ---
        title = self.font.render("Toolbox", True, (200, 220, 255))
        self.screen.blit(title, (self.title_pos[0] - title.get_width()//2, self.title_pos[1]))
        pg.draw.line(self.screen, (80, 100, 160),
                     (self.panel_rect.x + 14, self.title_pos[1] + 20),
                     (self.panel_rect.right - 14, self.title_pos[1] + 20), 1)

        # --- Toggles données ---
        self._draw_toggle(self.btn_day,  "Jour",        settings.toolbox_show_day,
                          asset=self.BUTTON_ASSETS[0])
        self._draw_toggle(self.btn_crea, "Créatures",   settings.toolbox_show_creatures,
                          asset=self.BUTTON_ASSETS[1])
        self._draw_toggle(self.btn_food, "Nourriture",  settings.toolbox_show_food,
                          asset=self.BUTTON_ASSETS[2])

        # --- Toggle champ de vision ---
        self._draw_toggle(self.btn_vision, "Champ de vision des créatures",
                          settings.toolbox_show_vision,
                          asset=self.BUTTON_ASSETS[3],
                          active_color=(100, 160, 220))

        # --- Vitesses ---
        lbl = self.font_small.render("Vitesse de simulation :", True, (180, 200, 255))
        self.screen.blit(lbl, self.speed_label_pos)
        for rect, spd in zip(self.speed_rects, self.SPEED_OPTIONS):
            self._draw_speed_btn(rect, f"x{spd:g}", settings.toolbox_simulation_speed == spd)

        # --- Fin du jeu ---
        if self.BUTTON_ASSETS[4]:
            img = pg.image.load(self.BUTTON_ASSETS[4]).convert_alpha()
            img = pg.transform.smoothscale(img, (self.btn_end.width, self.btn_end.height))
            self.screen.blit(img, (self.btn_end.x, self.btn_end.y))
            pg.draw.rect(self.screen, (230, 100, 100), self.btn_end, 2, border_radius=8)
        else:
            pg.draw.rect(self.screen, (180, 50, 50),  self.btn_end, border_radius=8)
            pg.draw.rect(self.screen, (230, 100, 100), self.btn_end, 2, border_radius=8)
        end_txt = self.font.render("Fin du jeu", True, (255, 220, 220))
        self.screen.blit(end_txt, (self.btn_end.centerx - end_txt.get_width()//2,
                                   self.btn_end.centery - end_txt.get_height()//2))
        

    def handle_event(self, event):
        """
        Gère les clics sur le burger et les boutons du panel.
        Retourne 'end' si le bouton fin du jeu est cliqué, None sinon.
        Un clic en dehors du panel et du burger ferme la toolbox.
        """
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            # Ouvre / ferme le panel via le burger
            if self.burger_rect.collidepoint(mx, my):
                self.open = not self.open
                return None

            # femruture si panel est ouvert et clique en dehors
            if self.open and not self.panel_rect.collidepoint(mx, my):
                self.open = False
                return None

            if not self.open:
                return None

            # Toggles données
            if self.btn_day.collidepoint(mx, my):
                settings.toolbox_show_day = not settings.toolbox_show_day
            elif self.btn_crea.collidepoint(mx, my):
                settings.toolbox_show_creatures = not settings.toolbox_show_creatures
            elif self.btn_food.collidepoint(mx, my):
                settings.toolbox_show_food = not settings.toolbox_show_food

            # Champ de vision
            elif self.btn_vision.collidepoint(mx, my):
                settings.toolbox_show_vision = not settings.toolbox_show_vision

            # Fin du jeu
            elif self.btn_end.collidepoint(mx, my):
                return 'end'

            # Vitesses
            for rect, spd in zip(self.speed_rects, self.SPEED_OPTIONS):
                if rect.collidepoint(mx, my):
                    settings.toolbox_simulation_speed = spd

        return None