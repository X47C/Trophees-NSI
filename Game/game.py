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
        gere a chaque tick :
        - faire bouger les cratures
        - verifier si la nouriture est mangée
        le tout en appelant les fonctions correspondantes
        """
        # fait bouger et consomme la nouriture des creatures
        for a in settings.creatures_list:
            for c in a:
                if not c.energy == 0:
                    c.lives()
                    c.moove()

    def first_day(self):
        for pop in settings.POPULATIONS:
            a = []
            for i in range(pop['quantity']):
                a.append(Creature(pop['speed'], pop['size'], pop['view'], pop['speed_variation'],pop['size_variation'], pop['view_variation'], pop['life'], pop['color']))
            settings.creatures_list.append(a)
        for i in range(settings.Food_quantity):
            settings.food_list.append(Food(rd(280, 1000), rd(70, 650)))
        print(settings.food_list)


    def is_over(self, dt):
        """
        dt = temps passé depuis la derniere fois que la fonction as étée appelée
        """
        self.time = dt / settings.FPS
        if self.time >= settings.day_duration:
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
        for a in settings.creatures_list:
            for c in a:
                c.pos_x = 550
                c.pos_y = 440
                c.energy = 100

    def draw_current_day(self):
        """
        Affiche le jour actuel en haut a gauche de l'écran quand le jeu est lancé
        """
        self.surf.blit(pg.font.SysFont(settings.Days_font, settings.Days_font_size).render(f'Day : {self.current_day} / {settings.Days_max}', True, (255, 255, 255)), (10, 10))