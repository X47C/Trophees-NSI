import settings
from .creature import Creature
import pygame as pg
from .food import Food
from random import randint as rd, shuffle

class Day_Manager():
    def __init__(self, surf):
        self.surf = surf
        self.current_day = 1
        self.time = 0

    def update(self):
        """
        """
        for a in settings.creatures_list:
            for c in a:
                if not c.energy == 0:
                    c.moove()
                    c.Eat()

    def first_day(self):
        """
        gere le premier jour de la simulation
        """
        settings.creatures_list_dico = {}
        settings.food_list = []
        settings.creatures_list = []
        for pop in settings.POPULATIONS:
            a = []
            for i in range(pop['quantity']):
                a.append(Creature(pop['speed'], pop['size'], pop['view'], pop['speed_variation'],pop['size_variation'], pop['view_variation'], pop['life'], pop['color']))
            settings.creatures_list.append(a)
        for i in range(settings.Food_quantity):
             settings.food_list.append(Food(rd(280, 1000), rd(70, 650)))
        self.distribute_on_border(settings.creatures_list, settings.Display_size)
        settings.creatures_list_dico[self.current_day] = [pop.copy() for pop in settings.creatures_list]# pas touche
        settings.food_list_dico[self.current_day] = len(settings.food_list)


    def is_over(self):
        """
        """
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
  

    def new_day(self):
        """
        ce que doit faire le jeu a chaques debuts de jours
        """
        self.current_day += 1
        self.time = 0
        for i in range(len(settings.creatures_list)):
            alive_creatures = []
            for c in settings.creatures_list[i]:
                if c.is_alive():
                    c.New_Day()
                    alive_creatures.append(c)
            settings.creatures_list[i] = alive_creatures
        settings.food_list = []
        for i in range(settings.Food_quantity):
             settings.food_list.append(Food(rd(280, 1000), rd(70, 650)))
        self.distribute_on_border(settings.creatures_list, settings.Display_size)
        settings.creatures_list_dico[self.current_day] = [pop.copy() for pop in settings.creatures_list] #allez voir le commentaire dans settings mais PAS TOUCHE !!!
        settings.food_list_dico[self.current_day] = len(settings.food_list)

        

    def draw_current_day(self):
        """
        Affiche le jour actuel en haut a gauche de l'écran quand le jeu est lancé
        """
        self.surf.blit(pg.font.SysFont(settings.Days_font, settings.Days_font_size).render(f'Day : {self.current_day} / {settings.Days_max}', True, (255, 255, 255)), (10, 10))


    def distribute_on_border(self, lists, screen_size, margin = 0):
        """
        Distribue les objets (dans lists) uniformément sur le bord de l'écran.

        - lists : liste de listes contenant des objets avec attributs pos_x et pos_y
        - screen_size : (width, height)
        - margin : marge intérieure depuis le bord (pixels)
        """
        w, h = screen_size
        eff_w = max(0, w - 2 * margin)
        eff_h = max(0, h - 2 * margin)
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
