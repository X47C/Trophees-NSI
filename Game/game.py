import settings
from .creature import Creature
import pygame as pg
from .food import Food
from random import randint as rd

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
        settings.creatures_list_dico[self.current_day] = settings.creatures_list.copy() # pas touche


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
        settings.creatures_list_dico[self.current_day] = settings.creatures_list.copy() #allez voir le commentaire dans settings mais PAS TOUCHE !!!

        

    def draw_current_day(self):
        """
        Affiche le jour actuel en haut a gauche de l'écran quand le jeu est lancé
        """
        self.surf.blit(pg.font.SysFont(settings.Days_font, settings.Days_font_size).render(f'Day : {self.current_day} / {settings.Days_max}', True, (255, 255, 255)), (10, 10))