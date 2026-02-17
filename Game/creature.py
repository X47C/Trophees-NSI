# methodes pour gerer les creatures
import math
from random import randint as rd, uniform, random
from math import radians, cos, sin, atan2, degrees, sqrt
import pygame as pg
import settings


class Creature():
    """
    Entrée : Speed, Size, View (int, compris entre 1 et 10)
    """

    def __init__(self, Speed:int, Size:int, View:int, Variation_Speed:int, Variation_Size:int, Variation_View:int, Days_Max:int, Color:tuple):
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
        self.pos_x = 0
        self.pos_y = 0
        img = pg.image.load("assets/creature.png")
        img_size = img.get_size()
        self.image = pg.transform.smoothscale(img, (img_size[0] + self.size * 2, img_size[1] + self.size * 2))
        self.rect = self.image.get_rect(center=(int(self.pos_x), int(self.pos_y)))
        self.angle_deg = rd(0, 360)
        self.radius = 10 * self.view

    def draw(self, screen:pg.surface):
        pg.draw.circle(screen, (40, 145, 40), (self.pos_x, self.pos_y), 10 * self.view)
        rect = self.image.get_rect(center=(int(self.pos_x), int(self.pos_y)))
        screen.blit(self.image, rect)

    def moove(self):
        """
        deplace la creature en fonction de sa vitesse et de son angle
        """
        collide, other_c = self.collide()
        dt = 1.0 / settings.FPS
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
            if food_id[1] == None:
                fx, fy = settings.food_list[food_id[0]].pos_x, settings.food_list[food_id[0]].pos_y
                desired = degrees(atan2(fy - self.pos_y, fx - self.pos_x)) % 360.0
                self.angle_deg = desired
                self.ang_vel = 0.0
            else:
                fx, fy = settings.creatures_list[food_id[0]][food_id[1]].pos_x, settings.creatures_list[food_id[0]][food_id[1]].pos_y
                desired = degrees(atan2(fy - self.pos_y, fx - self.pos_x)) % 360.0
                self.angle_deg = desired
                self.ang_vel = 0.0


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

        if collide:
            other = other_c
            blend = 0.65        
            ang_vel_damp = 0.5
            jitter = 12.0

            r1 = max(1.0, float(self.image.get_width()) / 2.0)
            r2 = max(1.0, float(other.image.get_width()) / 2.0)

            dx = other.pos_x - self.pos_x
            dy = other.pos_y - self.pos_y
            dist = sqrt(dx * dx + dy * dy)
            if dist == 0.0:
                dx = uniform(-0.01, 0.01)
                dy = uniform(-0.01, 0.01)
                dist = sqrt(dx * dx + dy * dy)
            overlap = (r1 + r2) - dist
            if overlap > 0:
                nx = dx / dist
                ny = dy / dist

                total_r = r1 + r2
                if total_r == 0:
                    w1 = w2 = 0.5
                else:
                    w1 = r2 / total_r
                    w2 = r1 / total_r

                self.pos_x -= nx * overlap * w1
                self.pos_y -= ny * overlap * w1
                other.pos_x += nx * overlap * w2
                other.pos_y += ny * overlap * w2

                if self.speed > 0:
                    v1x = cos(radians(self.angle_deg))
                    v1y = sin(radians(self.angle_deg))
                    dot1 = v1x * nx + v1y * ny
                    refl1x = v1x - 2.0 * dot1 * nx
                    refl1y = v1y - 2.0 * dot1 * ny
                    mag_refl1 = sqrt(refl1x * refl1x + refl1y * refl1y)
                    if mag_refl1 > 1e-6:
                        refl1x /= mag_refl1
                        refl1y /= mag_refl1
                    else:
                        refl1x, refl1y = v1x, v1y

                    nx1 = (1.0 - blend) * v1x + blend * refl1x
                    ny1 = (1.0 - blend) * v1y + blend * refl1y
                    mag_n1 = sqrt(nx1 * nx1 + ny1 * ny1)
                    if mag_n1 > 1e-6:
                        nx1 /= mag_n1
                        ny1 /= mag_n1
                        self.angle_deg = degrees(atan2(ny1, nx1)) % 360.0

                if other.speed > 0:
                    v2x = cos(radians(other.angle_deg))
                    v2y = sin(radians(other.angle_deg))
                    dot2 = v2x * nx + v2y * ny
                    refl2x = v2x - 2.0 * dot2 * nx
                    refl2y = v2y - 2.0 * dot2 * ny

                    mag_refl2 = sqrt(refl2x * refl2x + refl2y * refl2y)
                    if mag_refl2 > 1e-6:
                        refl2x /= mag_refl2
                        refl2y /= mag_refl2
                    else:
                        refl2x, refl2y = v2x, v2y

                    nx2 = (1.0 - blend) * v2x + blend * refl2x
                    ny2 = (1.0 - blend) * v2y + blend * refl2y
                    mag_n2 = sqrt(nx2 * nx2 + ny2 * ny2)
                    if mag_n2 > 1e-6:
                        nx2 /= mag_n2
                        ny2 /= mag_n2
                        other.angle_deg = degrees(atan2(ny2, nx2)) % 360.0

                if id(self) < id(other):
                    self.ang_vel = getattr(self, "ang_vel", 0.0) * ang_vel_damp + uniform(-jitter, jitter)
                    other.ang_vel = getattr(other, "ang_vel", 0.0) * ang_vel_damp + uniform(-jitter, jitter)


        # ----------------------
        # Consommation d'énergie 
        # ----------------------
        # Coefficients calibrés pour durée a peu pres 10s pour une créature moyenne noramlement (speed=5,size=5,view=5)
        base_cost = 0.06
        coeff_speed = 0.008  
        coeff_size = 0.006 
        coeff_view = 0.005

        speed_cost = coeff_speed * (self.speed ** 2)
        size_cost = coeff_size * self.size
        view_cost = coeff_view * self.view

        # consommation opar frame
        self.energy -= (base_cost + speed_cost + size_cost + view_cost)

        if self.energy < 0:
            self.energy = 0

        self.pos_x = min(max(self.pos_x, margin), w - margin)
        self.pos_y = min(max(self.pos_y, margin), h - margin)
        self.rect = self.image.get_rect(center=(int(self.pos_x), int(self.pos_y)))

    def Baby(self):
        """
        Se reproduit avec un pourcentage de proximité a ses parametres actuels
        """
        Baby = Creature(
            max(0, min(10, self.speed * (rd(100 - self.variation_speed, 100 + self.variation_speed)/100))),
            max(0, min(10, self.size * (rd(100 - self.variation_size, 100 + self.variation_size)/100))),
            max(0, min(10, self.view * (rd(100 - self.variation_view, 100 + self.variation_view)/100))),
            self.variation_speed,
            self.variation_size,
            self.variation_view,
            self.days_max,
            self.color
        )
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
                self.energy  = 100
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
                return True, (i, None)
        for i, l in enumerate(settings.creatures_list):
            for j, c in enumerate(l):
                if math.hypot(self.pos_x - c.pos_x, self.pos_y - c.pos_y) < self.radius:
                    if self.size - 4 >= c.size:
                        return True, (i, j)
        return False, (None, None)

    def is_alive(self):
        """
        Check si le mec est en vie renvois True ou false
        """
        return self.ate > 0 and self.days <= self.days_max
    

    def collide(self):
        creature_rect = self.rect

        for i, l in enumerate(settings.creatures_list):
            for j, c in enumerate(l):
                if creature_rect.colliderect(c.rect):
                    if id(c) != id(self):
                        self.canibalism(c, i, j)
                        return True, c
        return False, None
    
    def canibalism(self, c:object, i:int, j:int):
        if self.size - 4 >= c.size:
            settings.creatures_list[i].pop(j)
            return