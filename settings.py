<<<<<<< HEAD
# Paramètres globaux et valeurs par défaut
=======
import pygame as pg
pg.init()

Food_quantity = 100
Simulation_duration = 1 #min 1 max 10000, en jours
>>>>>>> d40f72c75e5bd1e4161f926052f7eb947a913428

# Affichage
Display_size = (1280, 720)  # largeur, hauteur
FPS = 60

# Police 
Days_font = "arial"
Days_font_size = 18
Button_font = "arial" 
Button_font_size = 18
Button_label_font = "arial"
Button_label_font_size = 14

#  Boutons généraux 
Food_quantity = 100         # Quantité de nourriture initiale
Days_max = 1                # Nombre de jours de la simulation (min 1)
day_duration = 5

# limites populations 
POPULATION_MIN = 1
POPULATION_MAX = 6

Color_options = ["white", "red", "green", "blue", "yellow", "purple", "black"]

# Valeurs par défaut pour une population
DEFAULT_POP = {
    "name": "Population 1",
    "life": 50,
    "color": "white",
    "quantity": 10,
    "speed_variation": 15,
    "size_variation": 15,
    "view_variation": 15,
    "view": 15,
    "speed": 3,
    "size": 3
}

# Liste des populations ( au moins 1 )
POPULATIONS = [
    DEFAULT_POP.copy()
]

<<<<<<< HEAD
# UI colors
UI_BG_COLOR = (200, 200, 200)
UI_PANEL_COLOR = (240, 240, 240)
=======

Button_font = 'arial' #nom de la police d'écriture des boutons
Button_font_size = 40 #taille de la police d'écriture des boutons*
Credits_font = 'arial' #nom de la police d'écriture des crédits
Credits_font_size = 30 #taille de la police d'écriture des crédits
Days_font = 'arial'
Days_font_size = 40 #taille de la police d'écriture des jours
Button_label_font = 'arial'
Button_label_font_size = 40



Display_size = (pg.display.Info().current_w, pg.display.Info().current_h) #taille de la fenêtre d'affichage (largeur, hauteur)

Credits_Text = ["Game developed by:",'Graffan Jules', 'Cros Cyprien', 'Quota Feminin']

Fps = 60
>>>>>>> d40f72c75e5bd1e4161f926052f7eb947a913428
