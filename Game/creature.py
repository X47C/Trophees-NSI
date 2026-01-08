# methodes pour gerer les creatures
from random import randint as rd
import pygame as pg
import settings

class  Creature():
    """
    Entrée : Speed, Size, View (int, compris entre 1 et 10) 
    """
    def __init__(self, Speed, Size, View, Variation_Speed, Variation_Size, Variation_View, Days_Max, Color):
        self.speed = Speed
        self.size = Size
        self.view = View
        self.color = Color
        self.ate = 0
        self.energy = 100
        self.variation_speed = Variation_Speed
        self.variation_size = Variation_Size
        self.variation_view = Variation_View
        self.days = 0
        self.days_max = Days_Max
        self.pos_x = settings.Display_size[0] // 2
        self.pos_y = settings.Display_size[1] // 2
        self.image = pg.image.load("assets/creature.png")

    def draw(self, screen):
        screen.blit(self.image, (self.pos_x, self.pos_y))

    def moove(self):
        self.pos_x += rd(-4 * self.speed, 4 * self.speed)
        self.pos_y += rd(-4 * self.speed, 4 * self.speed)

    def Baby(self):
        """
        Se reproduit avec un pourcentage de proximité a ses parametres actuels
        """
        Creature(self.speed * rd(100 - self.variation_speed, 100 + self.variation_speed), self.view * rd(100 - self.variation_size, 100 + self.variation_size), self.speed * rd(100 - self.variation_view, 100 + self.variation_view), self.color)

    def Eat(self):
        """
        Viens de manger
        """
        self.ate += 1
        if self.ate == 1:
            self.energy = 100
        else:
            self.energy = 0

    def New_Day(self):
        """
        Gere un nouveau jour
        """
        if self.is_alive():
            if self.ate >= 2:
                self.Baby()
            self.days += 1
            if not self.is_alive():
                return
            else:
                self.energy = 100
                self.ate = 0
            

    def is_alive(self):
        """
        Check si le mec est en vie renvois True ou false
        """
        return self.energy > 0 and self.days <= self.days_max

    def lives(self):
        """
        Consomme l'energie aussi ect
        """
        if self.is_alive():
            self.energy -= 1
        

    def get_color(self):
        """
        renvoie la couleur de la creature
        """
        return self.color
    
    def get_energy(self):
        """
        renvoie l'energie de la creature
        """
        return self.energy
    
    def get_size(self):
        """
        renvoie la taille de la creature
        """
        return self.size
    
    def get_speed(self):
        """
        renvoie la vitesse de la creature
        """
        return self.speed
    
    def get_view(self):
        """
        renvoie la vue de la creature
        """
        return self.view
    
