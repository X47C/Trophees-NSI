# Paramètres globaux et valeurs par défaut

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

# UI colors
UI_BG_COLOR = (200, 200, 200)
UI_PANEL_COLOR = (240, 240, 240)
