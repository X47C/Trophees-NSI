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

        # police
        self.font = pg.font.SysFont(settings.Days_font, settings.Days_font_size)


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
            w, h = settings.Display_size
            s = w / 638.0
            while True:
                fx = rd(0, w)
                fy = rd(0, h)
                valide = True
                if fx <= 255 * s and fy < 148 * s * (1.0 - fx / (255 * s)) + 20:
                    valide = False
                if fx >= 375 * s and fy < (138.0 / 263.0) * (fx - 375 * s) + 20:
                    valide = False
                if valide:
                    settings.food_list.append(Food(fx, fy))
                    break
        self.distribute_on_border(settings.creatures_list, settings.Display_size)

        #implemente les premier jour pour les graphes
        settings.creatures_list_dico[self.current_day] = [pop.copy() for pop in settings.creatures_list]
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
            w, h = settings.Display_size
            s = w / 638.0
            while True:
                fx = rd(0, w)
                fy = rd(0, h)
                valide = True
                if fx <= 255 * s and fy < 148 * s * (1.0 - fx / (255 * s)) + 20:
                    valide = False
                if fx >= 375 * s and fy < (138.0 / 263.0) * (fx - 375 * s) + 20:
                    valide = False
                if valide:
                    settings.food_list.append(Food(fx, fy))
                    break
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
        self.surf.blit(self.font.render(f'Jour : {self.current_day} / {settings.Days_max}', True, (0, 0, 0)), (10, 10))


    def draw_creature_number(self) -> None:
        """
        Affiche le nombre de créatures.
        """
        if not getattr(settings, 'toolbox_show_creatures', True):
            return
        offset = sum([getattr(settings, 'toolbox_show_day', True)])
        y = 10 + offset * (settings.Days_font_size + 8)
        debut = sum(len(l) for l in settings.creatures_list_dico[self.current_day])
        actuel = sum(len(l) for l in settings.creatures_list)
        self.surf.blit(pg.font.SysFont(settings.Days_font, settings.Days_font_size).render(f'Créatures : {actuel} / {debut}', True, (0, 0, 0)), (10, y))


    def draw_food_number(self) -> None:
        """
        Affiche la quantité de nourriture.
        """
        if not getattr(settings, 'toolbox_show_food', True):
            return
        offset = sum([getattr(settings, 'toolbox_show_day', True), getattr(settings, 'toolbox_show_creatures', True)])
        y = 10 + offset * (settings.Days_font_size + 8)
        debut = settings.food_list_dico[self.current_day]
        actuel = len(settings.food_list)
        self.surf.blit(pg.font.SysFont(settings.Days_font, settings.Days_font_size).render(f'Nourriture : {actuel} / {debut}', True, (0, 0, 0)), (10, y))


    def distribute_on_border(self, lists: list, screen_size: tuple, margin: int = 0) -> None:
        """
        distribue les créatures sur le bord de la surface de jeu
        """
        w, h = screen_size
        s = w / 638.0

        # les 6 coins du polygone 
        coins = [
            (0, 148 * s),
            (0, h),
            (w, h),
            (w, 138 * s),
            (375 * s, 0),
            (255 * s, 0)]
        coins.append(coins[0])  # fermeture

        # longueur de chaque segment
        from math import hypot
        seg_lens = [hypot(coins[i+1][0]-coins[i][0], coins[i+1][1]-coins[i][1]) for i in range(6)]
        perimetre = sum(seg_lens)

        # aplatit et mélange
        flat = [obj for sub in lists for obj in sub]
        shuffle(flat)
        N = len(flat)
        if N == 0:
            return

        spacing = perimetre / N

        for i, obj in enumerate(flat):
            d = i * spacing
            cumul = 0.0
            for k, seg_len in enumerate(seg_lens):
                if d <= cumul + seg_len:
                    t = (d - cumul) / seg_len if seg_len > 0 else 0.0
                    obj.pos_x = int(round(coins[k][0] + t * (coins[k+1][0] - coins[k][0])))
                    obj.pos_y = int(round(coins[k][1] + t * (coins[k+1][1] - coins[k][1])))
                    break
                cumul += seg_len