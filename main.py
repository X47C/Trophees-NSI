#  boucle principale 
import pygame as pg
from Pygame.pygame import Before_Game, Settings, In_Game, Post_Game
import settings
from Game.game import Day_Manager

# --- INIT ---
pg.init()
screen = pg.display.set_mode(settings.Display_size)
clock = pg.time.Clock()

Befg = Before_Game(screen)
Sett = Settings(screen)
Ing = In_Game(screen)
Engd = Post_Game(screen)

day_manager = Day_Manager(screen)

running = True
state = 'home'

# --- MAIN LOOP ---
while running:

    dt = clock.tick(settings.Fps) / 1000.0 

    # --- EVENT HANDLING ---
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        match state:
            case 'home':
                match Befg.handle_event(event):
                    case 'start':
                        state = 'settings'
                    case 'exit':
                        running = False
                    case 'credits':
                        state = 'credits'

            case 'settings':
                match Sett.handle_event(event):
                    case'start':
                        day_manager.new_day()
                        state = 'in_game'
                    case 'back':
                        state = 'home'

            case 'in_game':
                match Ing.handle_event(event):
                    case 'end':
                        state = 'post_game'   
                        day_manager.current_day = 0

            case 'post_game':
                match Engd.handle_event(event):
                    case 'exit':
                        running = False
                    case 'home':
                        state = 'home'

            case 'credits':
                match Befg.handle_event(event):
                    case 'home':
                        state = 'home'


    # --- UPDATE --- 
    if state == "in_game":

        match day_manager.update(dt):
            case "end":
                state = "post_game"
                day_manager.current_day = 0
            case "continue":
                day_manager.new_day()


    # --- DRAW ---
    screen.fill((0,0,0))

    match state:
        case 'home':
            Befg.draw()
        case 'settings':
            Sett.draw()
        case 'in_game':
            Ing.draw()
            day_manager.draw_current_day()
        case 'post_game':
            Engd.draw()
        case 'credits':
            Befg.credits()

    pg.display.flip()






# Fonctionnement theorique du jeu ( en fonctionnement ) dans la boucle main :

# toutes les creatures : listes de liste d'objets ( une liste d'objets par jours, le tout dans une liste globale utilisée pour les stats a la fin)
# la bouffe : liste d'ojets


# debut du jour :
    # - verifier les creatures en vie
    # -les afficher
    # - les mettres a des cos logiques genre pas l'une sur l'autre
    # - faire apparaitre la bouffe
    # -lancer le mouvement des cratures

# faut faire en sorte qu'un jour dure un temps donné
# pendant ce temps faut faire :
    # - a chaques tick faire avancer les creatures ( soit au hasard soit vers de la boufe si jamais y'en as pas loin)
    # -verifier si les cratures ont mangée --> utiliser la methode dans ce cas la

# le tout dans des fonctions avant la boucle principale, on fera des methodes dans une classe game pour certaines choses:
    # - def day(dt --> temps passé depuis la derniere frame, )
    # - def start_day