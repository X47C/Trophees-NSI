import settings
from .creature import Creature
import pygame as pg
from .food import Food
from random import randint as rd, shuffle

class Day_Manager():
    def __init__(self, surf: pg.surface) -> None:
        #écran
        self.surf = surf

        #utilitaire
        self.current_day = 1
        self.time = 0


    def update(self) -> None:
        """
        Permet de faire bouger les créature et de verifier si elles ont mangé tant qu'elles ont de l'energie
        """
        for a in settings.creatures_list:
            for c in a:
                if not c.energy == 0:
                    c.moove()
                    c.Eat()
                else:
                    c.animate()
                    if c.sleep == False:
                        c.sleep = True
                    


    def first_day(self) -> None:
        """
        Gere le premier jour de la simulation
        """
        #reinitialise les graphes
        settings.creatures_list_dico = {}
        settings.food_list_dico = {}

        #reinitialise les creatures et la nouriture
        settings.food_list = []
        settings.creatures_list = []

        #créée les créatures
        for pop in settings.POPULATIONS:
            a = []
            for i in range(pop['quantity']):
                a.append(Creature(pop['speed'], pop['size'], pop['view'], pop['speed_variation'], pop['size_variation'], pop['view_variation'], pop['life'], pop['color']))
            settings.creatures_list.append(a)

        #crée la nouriture
        for i in range(settings.Food_quantity[0]):
            settings.food_list.append(Food(rd(100, 1180), rd(50, 700)))
        self.distribute_on_border(settings.creatures_list, settings.Display_size)

        #implemente les premier jour pour les graphes
        settings.creatures_list_dico[self.current_day] = [pop.copy() for pop in settings.creatures_list] # pas touche
        settings.food_list_dico[self.current_day] = len(settings.food_list)


    def is_over(self) -> str:
        """
        Renvoie 'end' si le jour actuel est fini, 'continue' dans l'autre cas
        """
        # vérifie si toutes les créatures ont épuisé leur énergie
        a = True
        for elt in settings.creatures_list:
            for c in elt:
                if c.energy != 0:
                    a = False
                if not a:
                    break

        if len(settings.food_list) == 0 or a:
            if self.current_day >= settings.Days_max:
                return 'end'
            else:
                return 'continue'


    def new_day(self) -> None:
        """
        ce que doit faire le jeu a chaques debuts de jours
        """
        #modifications utilitaires
        self.current_day += 1
        self.time = 0

        #verifie quelles creatures doivent mourir et quelles creatures survivent
        for i in range(len(settings.creatures_list)):
            alive_creatures = []
            for c in settings.creatures_list[i]:
                if c.is_alive():
                    c.New_Day()
                    alive_creatures.append(c)
            settings.creatures_list[i] = alive_creatures

        #réinitialise et recréé la nouriture
        settings.food_list = []
        for i in range(settings.Food_quantity[self.current_day - 1]):
            settings.food_list.append(Food(rd(100, 1180), rd(50, 700)))
        self.distribute_on_border(settings.creatures_list, settings.Display_size)

        #implemente le jour actuel dans les graphes
        settings.creatures_list_dico[self.current_day] = [pop.copy() for pop in settings.creatures_list]
        settings.food_list_dico[self.current_day] = len(settings.food_list)


    def draw_current_day(self) -> None:
        """
        Affiche le jour actuel ( toujours en première position si visible ).
        """
        if not getattr(settings, 'toolbox_show_day', True):
            return
        self.surf.blit(pg.font.SysFont(settings.Days_font, settings.Days_font_size).render(f'Jour : {self.current_day} / {settings.Days_max}', True, (255, 255, 255)), (10, 10))


    def draw_creature_number(self) -> None:
        """
        Affiche le nombre de créatures.
        """
        if not getattr(settings, 'toolbox_show_creatures', True):
            return
        # compte combien d'infos sont affichées au-dessus
        offset = sum([getattr(settings, 'toolbox_show_day', True)])
        y = 10 + offset * (settings.Days_font_size + 8)
        self.surf.blit(pg.font.SysFont(settings.Days_font, settings.Days_font_size).render(f'Nombre de créatures : {sum([len(l) for l in settings.creatures_list])}', True, (255, 255, 255)), (10, y))


    def draw_food_number(self) -> None:
        """
        Affiche la quantité de nourriture.
        """
        if not getattr(settings, 'toolbox_show_food', True):
            return
        # compte combien d'infos sont affichées au-dessus
        offset = sum([getattr(settings, 'toolbox_show_day', True), getattr(settings, 'toolbox_show_creatures', True)])
        y = 10 + offset * (settings.Days_font_size + 8)
        self.surf.blit(pg.font.SysFont(settings.Days_font, settings.Days_font_size).render(f'Quantité de nouriture : {len(settings.food_list)}', True, (255, 255, 255)), (10, y))


    def distribute_on_border(self, lists: list, screen_size: tuple, margin: int = 0) -> None:
        """
        Distribue les objets (dans lists) uniformément sur le bord de l'écran.

        - lists : liste de listes contenant des objets avec attributs pos_x et pos_y
        - screen_size : (width, height)
        - margin : marge intérieure depuis le bord (pixels)
        """
        w, h = screen_size
        eff_w = max(0, w - 2 * margin)
        eff_h = max(0, h - 2 * margin)

        # aplatit toutes les sous-listes en une seule
        flat = []
        for sub in lists:
            for obj in sub:
                flat.append(obj)
        shuffle(flat)

        N = len(flat)
        if N == 0:
            return

        perimeter = 2 * (eff_w + eff_h)
        spacing = perimeter / N

        #positionnement sur le périmètre
        for i, obj in enumerate(flat):
            d = i * spacing
            if d < eff_w:
                x = margin + d
                y = margin
            elif d < eff_w + eff_h:
                x = margin + eff_w
                y = margin + (d - eff_w)
            elif d < eff_w + eff_h + eff_w:
                x = margin + (eff_w - (d - (eff_w + eff_h)))
                y = margin + eff_h
            else:
                x = margin
                y = margin + (eff_h - (d - (2 * eff_w + eff_h)))

            obj.pos_x = int(round(x))
            obj.pos_y = int(round(y))