# methodes pour gerer les creatures
from random import randint as rd, uniform, random
from math import radians, cos, sin, atan2, degrees, hypot
import pygame as pg
import settings
from Game.food import Food

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
        self.angle_deg = rd(0, 360)


    def draw(self, screen):
        rect = self.image.get_rect(center=(int(self.pos_x), int(self.pos_y)))
        screen.blit(self.image, rect)


    def moove(self):
        dt = 1.0 / settings.FPS
        w, h = settings.Display_size

        speed_px_s = float(self.speed) * 15.0   # LA vitesse
        margin = 40 + int(self.size)

        turn_noise = 450.0      
        damping = 0.96         
        burst_prob = 0.5        
        burst_mag = 220.0       

        if not hasattr(self, "ang_vel"):
            self.ang_vel = uniform(-120.0, 120.0)

        self.ang_vel += uniform(-turn_noise, turn_noise) * dt

        if random() < burst_prob * dt:
            self.ang_vel += uniform(-burst_mag, burst_mag)

        self.ang_vel *= damping

        max_ang_vel = 550.0
        if self.ang_vel > max_ang_vel:
            self.ang_vel = max_ang_vel
        elif self.ang_vel < -max_ang_vel:
            self.ang_vel = -max_ang_vel

        self.angle_deg = (self.angle_deg + self.ang_vel * dt) % 360.0
        r = radians(self.angle_deg)
        step = speed_px_s * dt
        self.pos_x += cos(r) * step
        self.pos_y += sin(r) * step

        bounced = False

        if self.pos_x < margin:
            self.pos_x = margin
            self.angle_deg = (180.0 - self.angle_deg) % 360.0
            self.ang_vel = -self.ang_vel + uniform(-90, 90)
            bounced = True
        elif self.pos_x > w - margin:
            self.pos_x = w - margin
            self.angle_deg = (180.0 - self.angle_deg) % 360.0
            self.ang_vel = -self.ang_vel + uniform(-90, 90)
            bounced = True

        if self.pos_y < margin:
            self.pos_y = margin
            self.angle_deg = (-self.angle_deg) % 360.0
            self.ang_vel = -self.ang_vel + uniform(-90, 90)
            bounced = True
        elif self.pos_y > h - margin:
            self.pos_y = h - margin
            self.angle_deg = (-self.angle_deg) % 360.0
            self.ang_vel = -self.ang_vel + uniform(-90, 90)
            bounced = True

        if bounced:
            self.ang_vel += uniform(-40, 40)

        self.pos_x = min(max(self.pos_x, margin), w - margin)
        self.pos_y = min(max(self.pos_y, margin), h - margin)



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
        for elt in settings.food_list:
            if self.collide(elt.rect):
                settings.food_list.elt.__del__()
        
    def collide(self, recte):
        """
        verifie si la creature entre en collision avec un rectangle
        """
        if pg.sprite.collide_rect(self, recte):
           return True
        return False

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

    def see_food(self):
        """
        return True si la creature a de la nourriture dans son champs de vision
        False sinon. Toute la bouffe est stockée dans settings.food_list, c'est une liste d'objet (les coordonées sont dans le init )
        Les creatures on un champs de vision qui va de 1 a 10 donc plus c'est elevé plus elles voient loin
        """

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
    
    
