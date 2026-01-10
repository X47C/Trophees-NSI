# methodes pour gerer les creatures
from random import randint as rd, uniform
from math import radians, cos, sin, atan2, degrees, hypot
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
        self.angle_deg = rd(0, 360)
        self.ang_vel_deg_s = uniform(-120.0, 120.0)  # vitesse angulaire initiale (deg/s)
        self._move_time = 0.0                         # timer interne (s)
        self._sin_freq = uniform(0.3, 1.2)            # fréquence sinusoïde pour motif
        self._sin_phase = uniform(0, 2 * 3.14159265)
        self.ang_vel = uniform(-180, 180)  # deg/s

                

    def draw(self, screen):
        rect = self.image.get_rect(center=(int(self.pos_x), int(self.pos_y)))
        screen.blit(self.image, rect)


    def moove(self):
        dt = 1.0 / settings.FPS
        w, h = settings.Display_size
        cx, cy = w * 0.5, h * 0.5

        # --- paramètres simples ---
        speed_px_s = self.speed * 45.0     # px/s
        margin = 40 + int(self.size)

        turn_noise = 600.0                 # deg/s² → zigzag
        center_strength = 3.0              # attraction vers le centre
        max_ang_vel = 400.0                # limite de rotation

        # --- 1) bruit angulaire (zigzag) ---
        self.ang_vel += uniform(-turn_noise, turn_noise) * dt

        # --- 2) attraction vers le centre ---
        dx = cx - self.pos_x
        dy = cy - self.pos_y
        dist = hypot(dx, dy)

        if dist > 1.0:
            angle_to_center = degrees(atan2(dy, dx))
            diff = (angle_to_center - self.angle_deg + 180) % 360 - 180
            self.ang_vel += diff * center_strength * dt

        # --- 3) clamp vitesse angulaire ---
        self.ang_vel = max(-max_ang_vel, min(max_ang_vel, self.ang_vel))

        # --- 4) appliquer rotation ---
        self.angle_deg = (self.angle_deg + self.ang_vel * dt) % 360

        # --- 5) déplacement ---
        step = speed_px_s * dt
        r = radians(self.angle_deg)
        self.pos_x += cos(r) * step
        self.pos_y += sin(r) * step

        # --- 6) rebond avant mur ---
        bounced = False

        if self.pos_x < margin:
            self.pos_x = margin
            self.ang_vel = abs(self.ang_vel)
            bounced = True
        elif self.pos_x > w - margin:
            self.pos_x = w - margin
            self.ang_vel = -abs(self.ang_vel)
            bounced = True

        if self.pos_y < margin:
            self.pos_y = margin
            self.ang_vel = abs(self.ang_vel)
            bounced = True
        elif self.pos_y > h - margin:
            self.pos_y = h - margin
            self.ang_vel = -abs(self.ang_vel)
            bounced = True

        if bounced:
            self.ang_vel += uniform(-120, 120)

        # --- sécurité ---
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
        return True si la creature a de la nouritture dans son champs de vision
        False sinon. Toute la bouffe est stockée dans settings.food_list, c'est une liste d'objet ( les cooronées sont dans le init )
        Les creatures on un champs de vision qui va de 1 a 10 donc plus c'est elevé plus elles voient loin
        """
        pass

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
    
