# ensemble des classes gérant les différents écrans du jeu
import pygame as pg
from Pygame.button import Button
from Pygame.toolbox import Toolbox
from pygame import Rect
import settings
import matplotlib as plt
plt.use("Agg")  # backend sans fenêtre
import pylab
import matplotlib.backends.backend_agg as agg
from matplotlib.ticker import MaxNLocator
import cv2


class Before_Game:
    """
    permet de gérer l'écran avant le lancement de la partie
    """
    def __init__(self, screen):
        """
        screen = tuple(largueur, hauteur)
        Initialise l'écran avant le lancement de la partie
        """
        self.width, self.height = settings.Display_size
        self.screen = screen
        
        # images des boutons
        self.button_start_img = pg.transform.scale(pg.image.load('data/home/start-button.png'), (int(self.width * 0.244), int(self.height * 0.086)))
        self.button_credits_img = pg.transform.scale(pg.image.load('data/home/credits-button.png'), (int(self.width * 0.167), int(self.height * 0.214)))
        self.button_exit_img = pg.transform.scale(pg.image.load('data/home/exit-button.png'), (int(self.width * 0.170), int(self.height * 0.094)))
        self.button_credits_exit_img = pg.transform.scale(pg.image.load('data/home/credits-exit-button.png'), (int(self.width * 0.049), int(self.height * 0.088)))

        # boutons
        self.Button_Start = Button(Rect(int(self.width * 0.378), int(self.height * 0.499), int(self.width * 0.244), int(self.height * 0.086)), '', self.screen)
        self.Button_exit = Button(Rect(int(self.width * 0.415), int(self.height * 0.646), int(self.width * 0.170), int(self.height * 0.094)), '', self.screen)
        self.Button_credits = Button(Rect(int(self.width * 0.417), int(self.height * 0.237), int(self.width * 0.167), int(self.height * 0.214)), '', self.screen)
        self.Button_credits_exit = Button(Rect(int(self.width * 0.840), int(self.height * 0.081), int(self.width * 0.049), int(self.height * 0.088)), '', self.screen)
        self.Button_tutorial_pass = Button(Rect(self.width // 2 - 65, self.height // 2 + 50, 130, 50),'Pass', self.screen)


        bg_asset = pg.image.load('data/home/background.png')
        self.bg_asset = pg.transform.scale(bg_asset, settings.Display_size)
        self.Button_font = pg.font.SysFont(settings.Button_font, settings.Button_font_size)


    def draw(self):
        """
        Dessine l'écran avant le lancement de la partie
        """
        self.screen.blit(self.bg_asset, (0, 0))
        self.Button_exit.draw(self.screen, self.Button_font, self.button_exit_img)
        self.Button_Start.draw(self.screen, self.Button_font, self.button_start_img)
        self.Button_credits.draw(self.screen, self.Button_font, self.button_credits_img)


    def handle_event(self, event):
        """
        Gère les événements de l'écran avant le lancement de la partie
        """
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                if self.Button_exit.rect.collidepoint(event.pos):  
                    return 'exit'
                if self.Button_Start.rect.collidepoint(event.pos):
                    return 'start'
                if self.Button_credits.rect.collidepoint(event.pos):
                    return 'credits'
                if self.Button_credits_exit.rect.collidepoint(event.pos):
                    return 'home'


    def tutorial(self):
        """
        Affiche le tutoriel sous forme de popup par-dessus l'écran d'accueil.
        Utilise opencv pour lire la vidéo frame par frame et l'afficher dans pygame.
        """

        # chargement de la vidéo
        cap = cv2.VideoCapture('data/tutorial.mp4')

        fps_video = cap.get(cv2.CAP_PROP_FPS) or 30
        clock_tuto = pg.time.Clock()

        # dimensions de la popup
        popup_w = int(self.width * 0.75)
        popup_h = int(self.height * 0.75)
        popup_x = (self.width - popup_w) // 2
        popup_y = (self.height - popup_h) // 2

        # hauteur réservée pour le bouton "Passer" en bas de la popup
        btn_zone_h = 60
        video_h = popup_h - btn_zone_h

        # bouton "Passer" centré en bas de la popup
        btn_w, btn_h = 130, 44
        btn_x = popup_x + (popup_w - btn_w) // 2
        btn_y = popup_y + popup_h - btn_zone_h + (btn_zone_h - btn_h) // 2
        self.Button_tutorial_pass.rect = pg.Rect(btn_x, btn_y, btn_w, btn_h)

        running_tuto = True
        while running_tuto:
            self.draw()

            # lecture d'une frame
            ret, frame = cap.read()
            if not ret:
                # fin de la vidéo : on arrete
                running_tuto = False
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgb = cv2.resize(frame_rgb, (popup_w, video_h))
            frame_surf = pg.surfarray.make_surface(frame_rgb.swapaxes(0, 1))

            # fond semi-transparent par-dessus l'écran d'accueil
            overlay = pg.Surface((self.width, self.height), pg.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, (0, 0))

            # fond de la popup
            pg.draw.rect(self.screen, (255, 255, 255), (popup_x - 15, popup_y - 15, popup_w + 30, popup_h + 15), border_radius=8)

            # affichage de la frame vidéo
            self.screen.blit(frame_surf, (popup_x, popup_y))

            # bouton "Passer"
            self.Button_tutorial_pass.draw(self.screen, self.Button_font, bg=(50, 180, 100))

            pg.display.flip()
            clock_tuto.tick(fps_video)

            # gestion des événements
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running_tuto = False
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    if self.Button_tutorial_pass.rect.collidepoint(event.pos):
                        running_tuto = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running_tuto = False

        cap.release()


    def credits(self):
        """
        Affiche les crédits du jeu
        A modifier avec une image quand on en aura une
        """
        credits_bg_asset = pg.image.load('data/home/credits-background.png')
        self.credits_bg_asset = pg.transform.scale(credits_bg_asset, settings.Display_size)
        self.screen.blit(self.credits_bg_asset, (0, 0))
        self.Button_credits_exit.draw(self.screen, self.Button_font, self.button_credits_exit_img)
        


class Settings:
    """
    permet de gérer l'écran des paramètres de la simulation
    """

    def __init__(self, screen: pg.surface):
        self.screen = screen
        self.width, self.height = settings.Display_size

        # fond
        self.bg_asset = pg.transform.scale(pg.image.load('data/settings/background.png'), settings.Display_size)

        # polices
        self.font_btn = pg.font.SysFont(settings.Button_font, settings.Button_font_size)
        self.font_lbl = pg.font.SysFont(settings.Button_label_font, settings.Button_label_font_size)

        # index de la population sélectionnée
        self.selected_pop = 0

        # préchargement et resize des images
        self.load_assets()

        # construction de l'interface
        self.build_general_controls()
        self.build_pop_management_buttons()
        self.build_pop_controls()
        self.build_bottom_buttons()


    def load_assets(self):
        """
        Précharge et redimensionne toutes les images des boutons.
        """
        def load(path, w, h):
            return pg.transform.scale(pg.image.load(path).convert_alpha(), (int(self.width * w), int(self.height * h)))

        # tailles en pourcentage de l'écran (basé sur 1280x720)
        self.img_food = load('data/settings/generals-buttons/food-button.png', 239/1280, 105/720)
        self.img_gen_minus = load('data/settings/generals-buttons/minus.png', 52/1280, 51/720)
        self.img_gen_plus = load('data/settings/generals-buttons/plus.png', 52/1280, 51/720)
        self.img_gen_btn = load('data/settings/generals-buttons/button.png', 203/1280, 51/720)
        self.img_pop_add = load('data/settings/generals-buttons/pop+.png', 99/1280, 59/720)
        self.img_pop_rem = load('data/settings/generals-buttons/pop-.png', 99/1280, 59/720)
        self.img_pop_off = load('data/settings/generals-buttons/pop-off.png', 52/1280, 51/720)
        self.img_back = load('data/settings/generals-buttons/back.png', 113/1280, 63/720)
        self.img_start = load('data/settings/generals-buttons/start.png', 70/1280, 75/720)

        self.pop_img_cache = {}


    def get_pop_imgs(self, color: str) -> dict:
        """
        Retourne les images minus/plus/button pour la couleur donnée.
        """
        # correspondance couleur RGB
        color_map = {
            (255, 0, 0): 'red',
            (0, 255, 0): 'green',
            (0, 0, 255): 'blue',
            (255, 255, 0): 'yellow',
            (255, 165, 0): 'orange',
            (128, 0, 128): 'purple'}

        # convertit le tuple en nom si nécessaire
        folder = color_map.get(color, color) if isinstance(color, tuple) else color

        if folder not in self.pop_img_cache:
            def load(name, w, h):
                path = f'data/settings/population-buttons/{folder}/{name}'
                return pg.transform.scale(pg.image.load(path).convert_alpha(), (int(self.width * w), int(self.height * h)))
            def load_general(name, w, h):
                path = f'data/settings/generals-buttons/{name}'
                return pg.transform.scale(pg.image.load(path).convert_alpha(), (int(self.width * w), int(self.height * h)))

            self.pop_img_cache[folder] = {
                'minus': load('minus.png', 52/1280, 51/720),
                'plus': load('plus.png', 52/1280, 51/720),
                'button': load('button.png', 203/1280, 51/720),
                'pop_on': load_general(f'pop-on/{folder}.png', 52/1280, 51/720)}
        return self.pop_img_cache[folder]


    def responsive(self, x, y, w, h):
        """
        Convertit des coordonnées 1280x720 en coordonnées responsives.
        """
        return Rect(int(self.width * x/1280), int(self.height * y/720), int(self.width * w/1280), int(self.height * h/720))


    def build_general_controls(self):
        """
        Construit les contrôles généraux : nourriture et nombre de jours.
        """
        settings.PostG_PADDING = 20

        settings.editable_butons['food_qtt'] = Button(self.responsive(100, 11, 239, 105), "", self.screen, description="Permet d'acceder à une fenetre permettant de gérer la quantité de nouriture de la simulation au cours du temps")
        self.general_food = {"value": settings.editable_butons['food_qtt']}

        settings.editable_butons['day_qtt'] = Button(self.responsive(914, 38, 203, 51), str(settings.Days_max), self.screen, editable=True, max_length=100, description="Permet de modifier le nombre de jours de la simulation, avec au minimum 1 jour et au maximum 100 jours.")
        self.general_days = {"minus": Button(self.responsive(851, 38, 52, 51), "", self.screen),"value": settings.editable_butons['day_qtt'],"plus":  Button(self.responsive(1128, 38, 52, 51), "", self.screen),}


    def build_pop_management_buttons(self):
        """
        Construit les boutons d'ajout, suppression et sélection de population.
        """
        self.btn_add_pop = Button(self.responsive(90, 142, 99, 59), "", self.screen, description="Permet d'augmenter le nombre de populations, maximum 6")
        self.btn_rem_pop = Button(self.responsive(194, 142, 99, 59), "", self.screen, description="Permet de diminuer le nombre de populations, minimum 1")

        # boutons numérotés pour chaque population (on/off selon existence)
        pop_positions = [(340, 146), (403, 146), (466, 146), (529, 146), (592, 146), (655, 146)]
        self.pop_number_buttons = []
        for i, (x, y) in enumerate(pop_positions):
            rect = self.responsive(x, y, 52, 51)
            self.pop_number_buttons.append((rect, i))


    def build_pop_controls(self):
        """
        Construit la grille de contrôles pour la population sélectionnée.
        """
        if len(settings.POPULATIONS) == 0:
            settings.POPULATIONS.append(settings.DEFAULT_POP.copy())

        self.selected_pop = max(0, min(self.selected_pop, len(settings.POPULATIONS) - 1))
        pop = settings.POPULATIONS[self.selected_pop]

        # positions des boutons - (x, y), + (x, y), valeur (x, y) pour chaque ligne/colonne
        # ordre : life, color, quantity, speed_variation, size_variation, view_variation, speed, size, view
        minus_positions = [(100, 247), (477, 247), (851, 247), (100, 332), (477, 332), (851, 332), (100, 416), (477, 416), (851, 416)]
        plus_positions = [(377, 247), (754, 247), (1128, 247), (377, 332), (754, 332), (1128, 332), (377, 416), (754, 416), (1128, 416)]
        btn_positions = [(163, 247), (540, 247), (914, 247), (163, 332), (540, 332), (914, 332), (163, 416), (540, 416), (914, 416)]

        keys = ['life', 'color', 'quantity', 'speed_variation', 'size_variation', 'view_variation', 'speed', 'size', 'view']
        descriptions = {
            "life": "Permet de définir au bout de combien de jours une créature meurt de vieillesse",
            "color": "Permet de choisir la couleur de chaque population",
            "quantity": "Permet de définir le nombre de créatures au début de la simulation",
            "speed_variation": "Permet de définir à quel point la vitesse varie à chaque évolution",
            "size_variation": "Permet de définir à quel point la taille varie à chaque évolution",
            "view_variation": "Permet de définir à quel point le champ de vision varie à chaque évolution",
            "speed": "Permet de définir la vitesse des créatures au début de la simulation",
            "size": "Permet de définir la taille des créatures au début de la simulation",
            "view": "Permet de définir le champ de vision des créatures au début de la simulation",
        }

        self.pop_controls = {}
        for idx, key in enumerate(keys):
            cur_val = pop.get(key, "")
            display = str(cur_val)
            desc = descriptions.get(key, "")

            minus = Button(self.responsive(*minus_positions[idx], 52, 51), "", self.screen)
            if isinstance(cur_val, int):
                value = Button(self.responsive(*btn_positions[idx], 203, 51), display, self.screen, editable=True, description=desc)
            else:
                value = Button(self.responsive(*btn_positions[idx], 203, 51), display, self.screen, description=desc)
            plus = Button(self.responsive(*plus_positions[idx], 52, 51), "", self.screen)

            self.pop_controls[key] = {"minus": minus, "value": value, "plus": plus}


    def build_bottom_buttons(self):
        """
        Construit les boutons Back et Start en bas de l'écran.
        """
        self.btn_back  = Button(self.responsive(72, 512, 113, 63), "", self.screen)
        self.btn_start = Button(self.responsive(1140, 506, 70, 75), "", self.screen)


    def update_layout(self):
        """
        Reconstruit toute l'interface en conservant la population sélectionnée.
        """
        sel = self.selected_pop
        self.build_general_controls()
        self.build_pop_management_buttons()
        self.build_pop_controls()
        self.build_bottom_buttons()
        self.selected_pop = sel
        self.editable_button_set_value()


    def draw(self):
        """
        Dessine l'écran des paramètres avec tous ses contrôles.
        """
        self.screen.blit(self.bg_asset, (0, 0))

        # bouton nourriture
        self.general_food["value"].draw(self.screen, self.font_btn, self.img_food)

        # boutons jours
        self.general_days["minus"].draw(self.screen, self.font_btn, self.img_gen_minus)
        self.general_days["value"].draw(self.screen, self.font_btn, self.img_gen_btn)
        self.general_days["plus"].draw(self.screen, self.font_btn, self.img_gen_plus)

        # boutons pop+ et pop-
        self.btn_add_pop.draw(self.screen, self.font_btn, self.img_pop_add)
        self.btn_rem_pop.draw(self.screen, self.font_btn, self.img_pop_rem)

        # boutons numérotés des populations (on si la pop existe, off sinon)
        for rect, i in self.pop_number_buttons:
            if i < len(settings.POPULATIONS):
                color = settings.POPULATIONS[i].get('color', 'default')
                img_on = self.get_pop_imgs(color)['pop_on']
                b = Button(rect, "", self.screen)
                b.draw(self.screen, self.font_btn, img_on)
            else:
                b = Button(rect, "", self.screen)
                b.draw(self.screen, self.font_btn, self.img_pop_off)

        # grille des contrôles de la population sélectionnée
        color = settings.POPULATIONS[self.selected_pop].get('color', 'default')
        pop_imgs = self.get_pop_imgs(color)

        for key, c in self.pop_controls.items():
            c["minus"].draw(self.screen, self.font_btn, pop_imgs['minus'])
            c["value"].draw(self.screen, self.font_btn, pop_imgs['button'])
            c["plus"].draw(self.screen,  self.font_btn, pop_imgs['plus'])

        # boutons du bas
        self.btn_back.draw(self.screen, self.font_btn, self.img_back)
        self.btn_start.draw(self.screen, self.font_btn, self.img_start)

        # descriptions au survol
        settings.editable_butons['food_qtt'].description()
        settings.editable_butons['day_qtt'].description()
        self.btn_add_pop.description()
        self.btn_rem_pop.description()
        for key, c in self.pop_controls.items():
            c['value'].description()
        self.btn_start.description()
        self.btn_back.description()


    def handle_event(self, event):
        """
        Gère les clics sur tous les boutons de l'écran des paramètres.
        """
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.general_food["value"].rect.collidepoint(event.pos):
                return 'edit_food_curve'
            if self.btn_start.rect.collidepoint(event.pos):
                return 'start'
            if self.btn_back.rect.collidepoint(event.pos):
                return 'back'

            mx, my = event.pos

            # contrôles généraux jours
            if self.general_days["minus"].rect.collidepoint((mx, my)):
                settings.Days_max = max(1, settings.Days_max - 1)
                settings.sync_food_quantity()
                self.editable_button_set_value()
                return None
            if self.general_days["plus"].rect.collidepoint((mx, my)):
                settings.Days_max = min(settings.Max_days_max, settings.Days_max + 1)
                settings.sync_food_quantity()
                self.editable_button_set_value()
                return None

            # ajout ou suppression d'une population
            if self.btn_add_pop.rect.collidepoint((mx, my)):
                if len(settings.POPULATIONS) < settings.POPULATION_MAX:
                    new_idx = len(settings.POPULATIONS) + 1
                    base = settings.DEFAULT_POP.copy()
                    base["name"] = f"Population {new_idx}"
                    available = settings.get_available_colors()
                    base['color'] = available[0] if available else settings.Color_options[0]
                    settings.POPULATIONS.append(base)
                    self.selected_pop = len(settings.POPULATIONS) - 1
                    self.build_pop_management_buttons()
                    self.build_pop_controls()
                    self.editable_button_set_value()
                return None

            if self.btn_rem_pop.rect.collidepoint((mx, my)):
                if len(settings.POPULATIONS) > settings.POPULATION_MIN:
                    settings.POPULATIONS.pop(self.selected_pop)
                    self.selected_pop = max(0, min(self.selected_pop, len(settings.POPULATIONS) - 1))
                    self.build_pop_management_buttons()
                    self.build_pop_controls()
                    self.editable_button_set_value()
                return None

            # sélection d'une population par son numéro
            for rect, idx in self.pop_number_buttons:
                if rect.collidepoint((mx, my)) and idx < len(settings.POPULATIONS):
                    self.selected_pop = idx
                    self.build_pop_controls()
                    self.editable_button_set_value()
                    return None

            if len(settings.POPULATIONS) == 0:
                return None

            # boutons - et + des caractéristiques de la population
            pop = settings.POPULATIONS[self.selected_pop]
            for key, c in self.pop_controls.items():
                if c["minus"].rect.collidepoint((mx, my)):
                    cur = pop.get(key)
                    if key == "color":
                        opts_all = getattr(settings, 'Color_options', [])
                        opts = settings.get_available_colors(exclude_pop_index=self.selected_pop)
                        cur_color = pop.get("color")
                        cycle = [c for c in opts_all if c in opts or c == cur_color]
                        if cycle:
                            try: i = cycle.index(cur_color)
                            except ValueError: i = 0
                            pop["color"] = cycle[(i - 1) % len(cycle)]
                    elif isinstance(cur, int):
                        if key == 'quantity' : 
                            pop[key] = max(1, cur - 1)
                        if key == 'life' : 
                            pop[key] = max(1, cur - 1)
                        else :
                            pop[key] = max(0, cur - 1)
                    self.editable_button_set_value()
                    return None

                if c["plus"].rect.collidepoint((mx, my)):
                    cur = pop.get(key)
                    match key:
                        case 'color':
                            opts_all = getattr(settings, 'Color_options', [])
                            opts = settings.get_available_colors(exclude_pop_index=self.selected_pop)
                            cur_color = pop.get("color")
                            cycle = [c for c in opts_all if c in opts or c == cur_color]
                            if cycle:
                                try: i = cycle.index(cur_color)
                                except ValueError: i = 0
                                pop["color"] = cycle[(i + 1) % len(cycle)]
                        case 'life': pop[key] = min(cur + 1, settings.Max_life)
                        case 'quantity': pop[key] = max(min(cur + 1, settings.Max_quantity), 1)
                        case 'size' | 'speed' | 'view': pop[key] = min(cur + 1, settings.Max_caracteristic)
                        case 'size_variation' | 'view_variation' | 'speed_variation': pop[key] = min(cur + 1, 100)
                    self.editable_button_set_value()
                    return None

        self.editable_button_save_value()
        return None


    def editable_button_refresh(self, event):
        """
        Propage les événements clavier aux boutons éditables.
        """
        for b in settings.editable_butons.values():
            b.handle_event(event)
        for b in self.pop_controls.values():
            b['value'].handle_event(event)


    def editable_button_set_value(self):
        """
        Met à jour l'affichage de tous les boutons éditables depuis les settings.
        """
        settings.editable_butons['day_qtt'].set_value(settings.Days_max)
        pop = settings.POPULATIONS[self.selected_pop]
        for key, c in self.pop_controls.items():
            if key != "color":
                if key == 'quantity':
                    c['value'].set_value(max(1, pop[key]))
                c['value'].set_value(pop[key])
            else:
                c["value"].text = settings.color.get(str(pop.get(key, "")), str(pop.get(key, "")))


    def editable_button_save_value(self):
        """
        Sauvegarde les valeurs saisies dans les boutons éditables vers les settings.
        """
        if isinstance( settings.editable_butons['day_qtt'].get_number(), int):
            settings.Days_max =max(1, min(settings.Max_days_max, settings.editable_butons['day_qtt'].get_number()))
            settings.sync_food_quantity()
            settings.editable_butons['day_qtt'].set_value(settings.Days_max)
        else:
            settings.Days_max = int(settings.editable_butons['day_qtt'].text)
            settings.sync_food_quantity()

        pop = settings.POPULATIONS[self.selected_pop]
        for key, c in self.pop_controls.items():
            if key != "color":
                if isinstance(c['value'].get_number(), int):
                    match key:
                        case 'life': pop[key] = max(1, min(c['value'].get_number(), settings.Max_life)); c['value'].set_value(pop[key])
                        case 'quantity': pop[key] = max(1, min(c['value'].get_number(), settings.Max_quantity)); c['value'].set_value(max(1,pop[key]))
                        case 'size' | 'speed' | 'view': pop[key] = min(c['value'].get_number(), settings.Max_caracteristic); c['value'].set_value(pop[key])
                        case 'size_variation' | 'view_variation' | 'speed_variation': pop[key] = min(c['value'].get_number(), 100); c['value'].set_value(pop[key])
                else:
                    pop[key] = int(c['value'].text)
            else:
                c["value"].text = settings.color.get(str(pop.get(key, "")), str(pop.get(key, "")))



class In_Game:
    """
    permet de gérer l'écran pendant la partie
    """
    def __init__(self, screen: pg.surface):
        """
        screen = tuple(largueur, hauteur)
        Initialise l'écran pendant la partie
        """
        self.width, self.height = settings.Display_size
        self.screen = screen

        self.bg_asset = pg.transform.scale(pg.image.load('data/game/background.png'), settings.Display_size)

        self.toolbox = Toolbox(screen)


    def draw(self, l_creatures: list, screen: pg.surface) -> None:
        """
        Dessine l'écran pendant la partie
        """
        self.screen.blit(self.bg_asset, (0, 0))

        # affiche les créatures et la nourriture
        for a in l_creatures:
            for c in a:
                c.draw(screen)
        for f in settings.food_list:
            f.draw(screen)
        self.toolbox.draw()


    def handle_event(self, event: pg.event) -> str:
        """
        Gère les événements de l'écran pendant la partie
        """
        result = self.toolbox.handle_event(event)
        if result == 'end':
            return 'end'




class Post_Game:
    """
    écran après la partie
    avec scrollbar + graphiques matplotlib intégrés
    """

    def __init__(self, screen, current_day):
        self.width, self.height = settings.Display_size
        self.screen = screen
        self.current_day = current_day

        #images de fond 
        self.bg_up = pg.transform.scale(pg.image.load('data/post-game/up.png'), (self.width, 360))
        self.bg_down = pg.transform.scale(pg.image.load('data/post-game/down.png'), (self.width, 360))
        self.bg_middle = pg.transform.scale(pg.image.load('data/post-game/middle.png'), (self.width, 540))

        #scrollbar
        self.scroll_y = 0
        self.scroll_speed = 30
        self.scrollbar_rect = Rect(self.width - 18, 20, 12, self.height - 40)
        self.scroll_thumb_height = 80
        self.scroll_thumb_y = 20
        self.dragging_scroll = False

        #construction des graphes
        self.graph_list = []
        g_nb = self.build_graphs()
        self.content_height = 540 * g_nb

        # construction du fond
        self.build_background()
        self.content_height = max(self.content_height, self.bg_total_height)

        #boutons
        btn_w, btn_h = 220, 60
        btn_gap = 20
        total_w = btn_w * 2 + btn_gap
        start_x = (self.width - total_w) // 2
        btn_y_scroll = self.content_height - btn_h - 30
        self.Button_exit = Button(Rect(start_x, btn_y_scroll, btn_w, btn_h), 'Exit to Desktop', self.screen)
        self.Button_home = Button(Rect(start_x + btn_w + btn_gap, btn_y_scroll, btn_w, btn_h), 'Return to Home', self.screen)
        self.Button_font = pg.font.SysFont(settings.Button_font, settings.Button_font_size)


    def build_background(self):
        """
        Assemble les trois images en une seule grande surface de la hauteur du contenu.
        """
        fixed_h = 360 + 360 # hauteur fixe : haut + bas
        middle_h = 540
        available = max(0, self.content_height - fixed_h)
        repeats = -(-available // middle_h)

        self.bg_total_height = fixed_h + repeats * middle_h
        self.bg_surf = pg.Surface((self.width, self.bg_total_height))

        # image du haut
        self.bg_surf.blit(self.bg_up, (0, 0))

        # répétition de l'image du milieu
        y = 360
        for _ in range(repeats):
            self.bg_surf.blit(self.bg_middle, (0, y))
            y += middle_h

        # image du bas 
        self.bg_surf.blit(self.bg_down, (0, self.bg_total_height - 360))


    def build_graphs(self):
        """
        l'endroit ou on fout les graphes
        """
        #paramètres communs
        lw = 1 # épaisseur des courbes
        jour = [i for i in range(1, self.current_day + 1)]
        figsize = [8, 5]
        dpi = 100
        g_nb = 0

        days = sorted(settings.creatures_list_dico)

        # graphe 1 : caractéristiques moyennes toutes populations
        fig1 = pylab.figure(figsize=figsize, dpi=dpi)
        ax1 = fig1.gca()

        avrage_speed = [(sum(vals) / len(vals)) if vals else 0 for vals in ([obj.speed for sub in settings.creatures_list_dico[d] for obj in sub] for d in days)]
        average_size = [(sum(vals) / len(vals)) if vals else 0 for vals in ([obj.size for sub in settings.creatures_list_dico[d] for obj in sub] for d in days)]
        average_view = [(sum(vals) / len(vals)) if vals else 0 for vals in ([obj.view for sub in settings.creatures_list_dico[d] for obj in sub] for d in days)]


        ax1.set_xlim(0.5, self.current_day + 0.5)
        ax1.xaxis.set_major_locator(MaxNLocator(nbins=12, integer=True))
        ax1.set_xticks([i for i in range(1, self.current_day + 1) if (self.current_day <= 12 or i % max(1, self.current_day // 12) == 0)])
        ax1.set_ylim(0, 10)
        ax1.set_yticks(range(0, 11))
        ax1.plot(jour, avrage_speed, label="Vitesse", lw=lw, marker='+')
        ax1.plot(jour, average_size, label="Taille", lw=lw, marker="x")
        ax1.plot(jour, average_view, label="Vue", lw=lw, marker="o")
        ax1.set_xlabel('Jours')
        ax1.set_ylabel('Moyenne')
        ax1.set_title("Évolution des caractéristiques moyennes (toutes populations)", fontsize=13, fontweight='bold', pad=12)
        ax1.legend(loc='upper left', framealpha=0.8)
        ax1.grid(True, linestyle='--', alpha=0.5)
        ax1.set_axisbelow(True)
        fig1.tight_layout()
        self.graph_list.append(self.graph_to_surf(fig1))
        pylab.close(fig1)
        g_nb += 1

        # graphe 2 : nombre de créatures et de nourriture
        fig2 = pylab.figure(figsize=figsize, dpi=dpi)
        ax2 = fig2.gca()

        c_counts = [sum(len(sub) for sub in settings.creatures_list_dico[k]) for k in range(1, len(settings.creatures_list_dico) + 1)]
        f_counts = [settings.food_list_dico[i] for i in range(1, len(settings.food_list_dico) + 1)]

        ax2.set_xlim(0.5, self.current_day + 0.5)
        ax2.xaxis.set_major_locator(MaxNLocator(nbins=10, integer=True))
        ax2.set_xticks([i for i in range(1, self.current_day + 1) if (self.current_day <= 12 or i % max(1, self.current_day // 12) == 0)])
        ax2.plot(jour, c_counts, label='Créature', lw=lw, marker="x")
        ax2.plot(jour, f_counts, label='Nouriture', lw=lw, marker="o")
        ax2.set_xlabel('Jours')
        ax2.set_ylabel('Quantitée')
        ax2.set_title("Évolution de la quantité de créatures et de la quantité de nouriture", fontsize=13, fontweight='bold', pad=12)
        ax2.legend(loc='upper left', framealpha=0.8)
        ax2.grid(True, linestyle='--', alpha=0.5)
        ax2.set_axisbelow(True)
        fig2.tight_layout()
        self.graph_list.append(self.graph_to_surf(fig2))
        pylab.close(fig2)
        g_nb += 1

        # graphe 3 : quantité par population
        fig3 = pylab.figure(figsize=figsize, dpi=dpi)
        ax3 = fig3.gca()

        for i in range(len(settings.creatures_list_dico[1])):
            c_p_conts = [len(p[i]) for p in settings.creatures_list_dico.values()]
            ax3.plot(jour, c_p_conts, lw=lw, color=settings.creatures_list_dico[1][i][0].color)
        ax3.set_xlim(0.5, self.current_day + 0.5)
        ax3.xaxis.set_major_locator(MaxNLocator(nbins=10, integer=True))
        ax3.set_xticks([i for i in range(1, self.current_day + 1) if (self.current_day <= 12 or i % max(1, self.current_day // 12) == 0)])
        ax3.set_xlabel('Jours')
        ax3.set_ylabel('Quantité')
        ax3.set_title("Évolution de la quantité de créatures par populations", fontsize=13, fontweight='bold', pad=12)
        ax3.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax3.grid(True, linestyle='--', alpha=0.5)
        ax3.set_axisbelow(True)
        fig3.tight_layout()
        self.graph_list.append(self.graph_to_surf(fig3))
        pylab.close(fig3)
        g_nb += 1

        # graphes 4+ : caractéristiques par population
        for i in range(len(settings.creatures_list)):
            color = settings.creatures_list_dico[1][i][0].color

            fig4 = pylab.figure(figsize=figsize, dpi=dpi)
            ax4 = fig4.gca()

            ax4.set_xlim(0.5, self.current_day + 0.5)
            ax4.xaxis.set_major_locator(MaxNLocator(nbins=10, integer=True))
            ax4.set_xticks([i for i in range(1, self.current_day + 1) if (self.current_day <= 12 or i % max(1, self.current_day // 12) == 0)])
            ax4.set_ylim(0, 10)
            ax4.set_yticks(range(0, 11))

            m_speed = [sum(vals) / len(vals) if len(vals) != 0 else 0 for vals in ([c.speed for c in settings.creatures_list_dico[d][i]] for d in days)]
            m_size = [sum(vals) / len(vals) if len(vals) != 0 else 0 for vals in ([c.size for c in settings.creatures_list_dico[d][i]] for d in days)]
            m_view = [sum(vals) / len(vals) if len(vals) != 0 else 0 for vals in ([c.view for c in settings.creatures_list_dico[d][i]] for d in days)]

            ax4.plot(jour, m_speed, label="Vitesse", lw=lw, marker='+', color=color)
            ax4.plot(jour, m_size, label="Taille", lw=lw, marker="x", color=color)
            ax4.plot(jour, m_view, label="Vue", lw=lw, marker="o", color=color)
            ax4.set_xlabel('Jours')
            ax4.set_ylabel('Moyenne')
            ax4.set_title(f"Évolution des caractéristiques moyennes de la population {settings.color_fe[color]}", fontsize=13, fontweight='bold', pad=12)
            ax4.legend(loc='upper left', framealpha=0.8)
            ax4.grid(True, linestyle='--', alpha=0.5)
            ax4.set_axisbelow(True)
            fig4.tight_layout()
            self.graph_list.append(self.graph_to_surf(fig4))
            pylab.close(fig4)
            g_nb += 1

        return g_nb


    def graph_to_surf(self, fig):
        """
        Transforme les graphes en surface affichables sur pygame
        """
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_argb()
        size = canvas.get_width_height()
        surf = pg.image.fromstring(raw_data, size, "ARGB")
        surf = surf.convert_alpha()
        return surf


    def draw(self):
        """
        Dessine l'écran post-partie avec les graphes et la scrollbar.
        """
        # fond
        self.screen.blit(self.bg_surf, (0, 0), area=Rect(0, self.scroll_y, self.width, self.height))

        # surface scrollable contenant les graphes
        content_surf = pg.Surface((self.width - 30, self.content_height), pg.SRCALPHA   )

        y = 160
        for g in self.graph_list:
            content_surf.blit(g, (self.width // 2 - 410, y))
            y += 530


        self.screen.blit(content_surf, (0, 0), area=Rect(0, self.scroll_y, self.width - 30, self.height))
        self.draw_scrollbar()

        # repositionne les boutons en coordonnées écran selon le scroll
        btn_y_screen = self.Button_exit.rect.y - self.scroll_y

        # dessine uniquement si visible à l'écran
        if 0 <= btn_y_screen <= self.height:
            self.Button_exit.rect.y = btn_y_screen
            self.Button_home.rect.y = btn_y_screen
            self.Button_exit.draw(self.screen, self.Button_font, bg=(200, 50, 50))
            self.Button_home.draw(self.screen, self.Button_font, bg=(50, 120, 200))
            self.Button_exit.rect.y = btn_y_screen + self.scroll_y 
            self.Button_home.rect.y = btn_y_screen + self.scroll_y


    def draw_scrollbar(self):
        """
        Dessine la scrollbar et son curseur.
        """
        pg.draw.rect(self.screen, (180, 180, 180), self.scrollbar_rect)
        pg.draw.rect(self.screen, (100, 100, 100), Rect(self.scrollbar_rect.x, self.scroll_thumb_y, self.scrollbar_rect.width, self.scroll_thumb_height))


    def handle_event(self, event):
        """
        Gère le scroll et les clics sur les boutons de navigation.
        """
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            mx, my = event.pos
            adjusted = (mx, my + self.scroll_y)

            if self.Button_exit.rect.collidepoint(adjusted):
                return 'exit'
            if self.Button_home.rect.collidepoint(adjusted):
                return 'home'
            self.dragging_scroll = False

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                thumb_rect = Rect(self.scrollbar_rect.x, self.scroll_thumb_y, self.scrollbar_rect.width, self.scroll_thumb_height)
                if thumb_rect.collidepoint(event.pos):
                    self.dragging_scroll = True
                    self.drag_offset = event.pos[1] - self.scroll_thumb_y
            if event.button == 4: # molette haut
                self.scroll_y = max(0, self.scroll_y - self.scroll_speed)
            if event.button == 5: # molette bas
                self.scroll_y = min(self.content_height - self.height, self.scroll_y + self.scroll_speed)
            self.sync_scrollbar()

        if event.type == pg.MOUSEMOTION and self.dragging_scroll:
            self.scroll_thumb_y = event.pos[1] - self.drag_offset
            self.scroll_thumb_y = max(self.scrollbar_rect.y, min(self.scrollbar_rect.bottom - self.scroll_thumb_height, self.scroll_thumb_y))
            self.sync_content_scroll()


    def sync_scrollbar(self):
        """
        Met à jour la position du curseur de la scrollbar depuis le scroll actuel.
        """
        ratio = self.scroll_y / max(1, self.content_height - self.height)
        self.scroll_thumb_y = self.scrollbar_rect.y + ratio * (self.scrollbar_rect.height - self.scroll_thumb_height)


    def sync_content_scroll(self):
        """
        Met à jour le scroll depuis la position du curseur de la scrollbar.
        """
        ratio = (self.scroll_thumb_y - self.scrollbar_rect.y) / (self.scrollbar_rect.height - self.scroll_thumb_height)
        self.scroll_y = ratio * (self.content_height - self.height)