import settings
import pygame as pg

class Day_Manager():
    def __init__(self, surf):
        self.surf = surf
        self.current_day = 0
        self.time = 0

    def update(self, dt):
        """
        dt = temps passé depuis la derniere fois que la fonction as étée appelée
        """
        self.time += dt
        if self.time >= settings.day_duration:
            if self.current_day >= settings.Days_max:
                return 'end'
            else:
                print('end of the day')
                return 'continue'
        else:
            self.day()

    def new_day(self):
        """
        ce que doit faire le jeu a chaques debuts de jours
        """
        self.current_day += 1
        self.time = 0
        print('start of a new_day')

    def draw_current_day(self):
        """
        Affiche le jour actuel en haut a gauche de l'écran quand le jeu est lancé
        """
        self.surf.blit(pg.font.SysFont(settings.Days_font, settings.Days_font_size).render(f'Day : {self.current_day} / {settings.Days_max}', True, (255, 255, 255)), (10, 10))

    def day(self):
        """
        tout ce qui se passe dans un jour
        """
        pass

    



