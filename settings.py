import pygame as pg
pg.init()

Food_quantity = 100
Simulation_duration = 1 #min 1 max 10000, en jours

Speed = 3 #min 1 max 10
Size = 3 #min 1 max 10
View = 3 #min 1 max 10

Speed_variation = 15 #min 1 max 500, pourcentage
Size_variation = 15 #min 1 max 500, pourcentage
View_variation = 15 #min 1 max 500, pourcentage

Color = 'white' #white, red, green, blue, yellow, cyan, magenta, black



Days_max = 5 #min 1 max 1000
day_duration = 5 #en secondes



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
