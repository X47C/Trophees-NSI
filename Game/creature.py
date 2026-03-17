import math
from random import randint as rd, uniform, random
from math import radians, cos, sin, atan2, degrees, sqrt
import pygame as pg
import settings


class Creature():
    """
    Entrée : Speed, Size, View (int, compris entre 1 et 10)
    """

    def __init__(self, Speed:int, Size:int, View:int, Variation_Speed:int, Variation_Size:int, Variation_View:int, Days_Max:int, Color:str) -> None:
        #caracteristiques
        self.speed = Speed
        self.size = Size
        self.view = View
        self.color = Color
        self.variation_speed = Variation_Speed
        self.variation_size = Variation_Size
        self.variation_view = Variation_View
        self.days_max = Days_Max

        #position / déplacement
        self.angle_deg = rd(0, 360)
        self.radius = 10 * self.view
        self.pos_x = 0
        self.pos_y = 0

        self.days = 0
        self.ate = 0
        self.energy = 100

        self.sleep = False

        #affichage
        self.nb = 0
        self.frame = 0
        self.animations = {
            'east': self.load_animations('e'),
            'west': self.load_animations('o'),
            'north': self.load_animations('n'),
            'south': self.load_animations('s'),
            'north-east': self.load_animations('ne'),
            'south-east': self.load_animations('se'),
            'north-west': self.load_animations('no'),
            'south-west': self.load_animations('so'),
            'asleep': self.load_animations('asleep')}
        self.image = self.animations['east'][1]
        self.rect = self.image.get_rect(center=(int(self.pos_x), int(self.pos_y)))


    def draw(self, screen: pg.surface) -> None:
        """
        Dessine la créature sur l'écran 'screen'
        """
        # cercle de vision si l'option est activée
        if getattr(settings, 'toolbox_show_vision', True):
            r = 10 * self.view
            vision_surf = pg.Surface((r * 2, r * 2), pg.SRCALPHA)
            pg.draw.circle(vision_surf, (255, 255, 255, 30), (r, r), r)
            pg.draw.circle(vision_surf, (255, 255, 255, 120), (r, r), r, 2)
            screen.blit(vision_surf, (self.pos_x - r, self.pos_y - r))

        # dessin de la créature
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

        # paramètres du mouvement aléatoire
        turn_noise = 450.0
        damping = 0.96
        burst_prob = 0.5
        burst_mag = 220.0

        if not hasattr(self, "ang_vel"):
            self.ang_vel = uniform(-120.0, 120.0)

        # variation aléatoire de la direction
        self.ang_vel += uniform(-turn_noise, turn_noise) * dt

        if random() < burst_prob * dt:
            self.ang_vel += uniform(-burst_mag, burst_mag)

        # deplacement en fonction de l'environnement dans l'odre de priorité suivant : fuite d'un predateur, deplacement vers de la nouriture, deplacement vers une proie
        seen, object_id = self.see()
        # fuite d'un potientiel predateur
        if seen == 'predator':
            fx, fy = settings.creatures_list[object_id[0]][object_id[1]].pos_x, settings.creatures_list[object_id[0]][object_id[1]].pos_y
            desired = degrees(atan2(fy - self.pos_y, fx - self.pos_x) + 180) % 360.0
            self.angle_deg = desired
            self.ang_vel = 0.0

        # déplacement vers la nourriture si visible
        elif seen == 'food':
            fx, fy = settings.food_list[object_id[0]].pos_x, settings.food_list[object_id[0]].pos_y
            desired = degrees(atan2(fy - self.pos_y, fx - self.pos_x)) % 360.0
            self.angle_deg = desired
            self.ang_vel = 0.0
        
        # deplacement vers une proie si visible
        elif seen == 'prey':
            fx, fy = settings.creatures_list[object_id[0]][object_id[1]].pos_x, settings.creatures_list[object_id[0]][object_id[1]].pos_y
            desired = degrees(atan2(fy - self.pos_y, fx - self.pos_x)) % 360.0
            self.angle_deg = desired
            self.ang_vel = 0.0

        self.ang_vel *= damping

        # limite la vitesse angulaire maximale
        max_ang_vel = 550.0
        if self.ang_vel > max_ang_vel:
            self.ang_vel = max_ang_vel
        elif self.ang_vel < -max_ang_vel:
            self.ang_vel = -max_ang_vel

        # calcul de la nouvelle position
        self.angle_deg = (self.angle_deg + self.ang_vel * dt) % 360.0
        r = radians(self.angle_deg)
        step = speed_px_s * dt
        self.pos_x += cos(r) * step
        self.pos_y += sin(r) * step

        # rebond sur les bords
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

        # gestion de la collision avec une autre créature
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

            # évite la division par zéro
            if dist == 0.0:
                dx = uniform(-0.01, 0.01)
                dy = uniform(-0.01, 0.01)
                dist = sqrt(dx * dx + dy * dy)

            overlap = (r1 + r2) - dist
            if overlap > 0:
                nx = dx / dist
                ny = dy / dist

                # calcul des poids pour séparer les deux créatures
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

                # réflexion de l'angle pour self
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

                # réflexion de l'angle pour l'autre créature
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

                # applique un jitter angulaire une seule fois entre les deux
                if id(self) < id(other):
                    self.ang_vel = getattr(self, "ang_vel", 0.0) * ang_vel_damp + uniform(-jitter, jitter)
                    other.ang_vel = getattr(other, "ang_vel", 0.0) * ang_vel_damp + uniform(-jitter, jitter)

        # consommation d'énergie par frame
        base_cost = 0.07
        coeff_speed = 0.02
        coeff_size = 0.0055
        coeff_view = 0.005

        speed_cost = coeff_speed * (self.speed ** 2.8/17)
        size_cost = coeff_size * (self.size** 1.6/12)
        view_cost = coeff_view * (self.view ** 2/24)

        self.energy -= (base_cost + speed_cost + size_cost + view_cost)

        if self.energy < 0:
            self.energy = 0

        # s'assure que la créature reste dans les limites
        self.pos_x = min(max(self.pos_x, margin), w - margin)
        self.pos_y = min(max(self.pos_y, margin), h - margin)
        self.rect = self.image.get_rect(center=(int(self.pos_x), int(self.pos_y)))

        # gere l'animation de le creature
        self.animate((self.angle_deg + 90) % 360)

    def Baby(self) -> None:
        """
        Crée un bébé avec des caracteristiques identiques a self, sauf pour speed, size et view qui sont modifiés d'un certain pourcentage defini par varitaion_'caracteristique'
        """
        baby = Creature(
            max(0, min(10, self.speed * (rd(100 - self.variation_speed, 100 + self.variation_speed)/100))),
            max(0, min(10, self.size * (rd(100 - self.variation_size, 100 + self.variation_size)/100))),
            max(0, min(10, self.view * (rd(100 - self.variation_view, 100 + self.variation_view)/100))),
            self.variation_speed,
            self.variation_size,
            self.variation_view,
            self.days_max,
            self.color
        )
        baby.ate = 1

        # cherche la population de self et y ajoute le bébé
        for i in range(len(settings.POPULATIONS)):
            for crea in settings.creatures_list[i]:
                if crea == self:
                    settings.creatures_list[i].append(baby)
                    return


    def Eat(self) -> None:
        """
        Vérifie si la créature à mangée
        """
        creature_rect = self.rect

        for i, food in enumerate(settings.food_list):
            if creature_rect.colliderect(food.rect):
                self.ate += 1
                self.energy = 100
                settings.food_list.pop(i)
                return


    def New_Day(self) -> None:
        """
        Permet de verifier si la créature a survecue au jour precedent -> apppele la methode baby si besoin et reinitialise les parametres importants pour un jour
        """
        if self.is_alive():
            if self.ate >= 2:
                self.Baby()
            self.ate = 0
            self.energy = 100
            self.sleep = False
            self.image.set_alpha(255)


    def see(self) -> tuple:
        """
        return le type d'objet vu : 'predator', 'food' ou 'prey', None si rien n'est vu
        return egalement un tuple contenant la position dans la liste (i, j) de la nouriture vue. Dans le cas ou  aucune noiuriture n'est vue ce tuple est de (None, None)
        """
        # cherche un predateur 
        for i, l in enumerate(settings.creatures_list):
            for j, c in enumerate(l):
                if math.hypot(self.pos_x - c.pos_x, self.pos_y - c.pos_y) < self.radius:
                    if self.size + 4 <= c.size:
                        return 'predator', (i, j)
                    
        # cherche de le nourriture
        for i, food in enumerate(settings.food_list):
            if math.hypot(self.pos_x - food.pos_x, self.pos_y - food.pos_y) < self.radius:
                return 'food', (i, None)

        # cherche ensuite une créature plus petite à manger
        for i, l in enumerate(settings.creatures_list):
            for j, c in enumerate(l):
                if math.hypot(self.pos_x - c.pos_x, self.pos_y - c.pos_y) < self.radius:
                    if self.size - 4 >= c.size:
                        return 'prey', (i, j)

        return None, (None, None)


    def is_alive(self) -> bool:
        """
        Renvoie True si la créature est en vie, False sinon
        """
        return self.ate > 0 and self.days <= self.days_max


    def collide(self) -> tuple:
        """
        Renvoie True si une autre créature est percutée, False sinon
        Renvoie la créature percutée, False sinon 
        """
        creature_rect = self.rect

        for i, l in enumerate(settings.creatures_list):
            for j, c in enumerate(l):
                if creature_rect.colliderect(c.rect):
                    if id(c) != id(self):
                        self.canibalism(c, i, j)
                        return True, c
        return False, None


    def canibalism(self, c: object, i: int, j: int) -> None:
        """
        Entrée : 
            - c un objet de type créature
            - i est l'indice de la population de cette créature dans settings.creature_list
            - j est l'indice de la creature dans settings.creature_list[1]
        La fonction permet a la créature self de manger l'autre créature si celle si est plus petite d'au moins 4
        """
        if self.size - 4 >= c.size and c.sleep == False:
            settings.creatures_list[i].pop(j)
            return
        

    def load_animations(self, type:str) -> list:
        """
        permet de charger tout les sprites d'un animation, les renvoie dans une liste
        """
        path = f'assets/creature/{self.color}/{type}'
        frames = []
        for i in range(5):
            f = pg.image.load(f'{path}/{i}.png')
            f_size = f.get_size()
            if type == 'asleep':
                f.set_alpha(125)
            frames.append(pg.transform.smoothscale(f, (f_size[0] + self.size * 2, f_size[1] + self.size * 2)))
        return frames


    def animate(self, orientation=0) -> None:
        self.nb += 1
        if self.nb >= 15:
            self.frame += 1
            if self.frame >= 5:
                self.frame = 0
            self.nb = 0
        if self.sleep:
            self.image = self.animations['asleep'][self.frame]
        else:
            o = orientation # sécurité si jamais dépasses 360

            if o >= 337.5 or o < 22.5:
                self.image = self.animations['north'][self.frame]
            elif o < 67.5:
                self.image = self.animations['north-east'][self.frame]
            elif o < 112.5:
                self.image = self.animations['east'][self.frame]
            elif o < 157.5:
                self.image = self.animations['south-east'][self.frame]
            elif o < 202.5:
                self.image = self.animations['south'][self.frame]
            elif o < 247.5:
                self.image = self.animations['south-west'][self.frame]
            elif o < 292.5:
                self.image = self.animations['west'][self.frame]
            elif o < 337.5:
                self.image = self.animations['north-west'][self.frame]