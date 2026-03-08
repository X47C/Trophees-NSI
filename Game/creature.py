# methodes pour gerer les creatures
import math
from random import randint as rd, uniform, random
from math import radians, cos, sin, atan2, degrees
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
        self.rect = self.image.get_rect(center=(int(self.pos_x), int(self.pos_y)))
        self.angle_deg = rd(0, 360)
        self.radius = 10 * self.view
        
    def draw(self, screen):
        pg.draw.circle(screen, (40, 145, 40), (self.pos_x, self.pos_y), 10 * self.view)
        rect = self.image.get_rect(center=(int(self.pos_x), int(self.pos_y)))
        screen.blit(self.image, rect)
        
    def moove(self):
        """
        deplace la creature en fonction de sa vitesse et de son angle
        """
        dt = 1.0 / settings.FPS


    def draw(self, screen: pg.surface) -> None:
        """
        Dessine la créature sur l'écran 'screen'
        """
        if getattr(settings, 'toolbox_show_vision', True):
            r = 10 * self.view
            vision_surf = pg.Surface((r * 2, r * 2), pg.SRCALPHA)
            pg.draw.circle(vision_surf, (255, 255, 255, 30), (r, r), r)
            pg.draw.circle(vision_surf, (255, 255, 255, 120), (r, r), r, 2)
            screen.blit(vision_surf, (self.pos_x - r, self.pos_y - r))
        rect = self.image.get_rect(center=(int(self.pos_x), int(self.pos_y)))
        screen.blit(self.image, rect)
        return


    def moove(self) -> None:
        """
        deplace la creature en fonction de sa vitesse et de son angle
        """
        collide, other_c = self.collide()
        dt = 1.0 / 60
        w, h = settings.Display_size

        speed_px_s = float(self.speed) * 15.0
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

        seen, food_id = self.see_food()
        if seen:
            fx, fy = settings.food_list[food_id].pos_x, settings.food_list[food_id].pos_y
            desired = degrees(atan2(fy - self.pos_y, fx - self.pos_x)) % 360.0
            self.angle_deg = desired
            self.ang_vel = 0.0
            # desired = degrees(atan2(fy - self.pos_y, fx - self.pos_x))

            # diff = ((desired - self.angle_deg + 180.0) % 360.0) - 180.0  # -180..180
            # add = diff * 800
            # self.ang_vel += add * dt

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
        if self.pos_x :
            pass
        if bounced:
            self.ang_vel += uniform(-40, 40)

        self.energy -= 1
        self.pos_x = min(max(self.pos_x, margin), w - margin)
        self.pos_y = min(max(self.pos_y, margin), h - margin)
        self.rect = self.image.get_rect(center=(int(self.pos_x), int(self.pos_y)))


        


    def Baby(self):
        """
        Se reproduit avec un pourcentage de proximité a ses parametres actuels
        """
        Baby = Creature(max(0, min(10, self.speed * (rd(100 - self.variation_speed, 100 + self.variation_speed)/100))), max(0, min(10, self.size * (rd(100 - self.variation_size, 100 + self.variation_size)/100))), max(0, min(10, self.view * (rd(100 - self.variation_view, 100 + self.variation_view)/100))), self.variation_speed, self.variation_size, self.variation_view, self.days_max, self.color)
        Baby.ate = 1
        for i in range(len(settings.POPULATIONS)):
            for crea in settings.creatures_list[i]:
                if crea == self:
                    settings.creatures_list[i].append(Baby)
                    return
                    
    def Eat(self):
        """
        on verifie si il a mangé haha enfait c'est simple j'etait parti super loins pour rien mdr
        """
        creature_rect = self.rect 

        for i, food in enumerate(settings.food_list):
            if creature_rect.colliderect(food.rect):
                self.ate += 1   
                self.energy = 100
                settings.food_list.pop(i)
                return 
            

    def New_Day(self):
        """
        Gere un nouveau jour
        """
        if self.is_alive:
            if self.ate >= 2:
                self.Baby()
            self.ate = 0
            self.energy = 100
            self.pos_x = 550
            self.pos_y = 440

    def see_food(self):
        """
        return True si la creature a de la nourriture dans son champs de vision
        False sinon. Toute la bouffe est stockée dans settings.food_list, c'est une liste d'objet (les coordonées sont dans le init )
        Les creatures on un champs de vision qui va de 1 a 10 donc plus c'est elevé plus elles voient loin
        """
        for i, food in enumerate(settings.food_list):
            if math.hypot(self.pos_x - food.pos_x, self.pos_y - food.pos_y) < self.radius:
                return True, i
        return False, None

    def is_alive(self):
        """
        Check si le mec est en vie renvois True ou false
        """
        return self.ate > 0 and self.days <= self.days_max   

