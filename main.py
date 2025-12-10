#  boucle principale -- > execution du programme complet
import pygame as pg
from Pygame.pygame import Before_Game, Settings, In_Game, Post_Game
import settings
from Game.game import Day_Manager

running = True
pg.init()

Befg = Before_Game(pg.display.set_mode(settings.Display_size))
Sett = Settings(pg.display.set_mode(settings.Display_size))
Ing = In_Game(pg.display.set_mode(settings.Display_size))
Engd = Post_Game(pg.display.set_mode(settings.Display_size))

day_manager = Day_Manager()


state = 'home'

while running: 

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        match state:
            case 'home':
                Befg.draw()
                match Befg.handle_event(event):
                    case 'start':
                        state = 'settings'
                    case 'exit':
                        running = False
                    case 'credits':
                        state = 'credits'
            case 'settings':
                Sett.draw()
                match Sett.handle_event(event):
                    case 'start':
                        state = 'in_game'

            case 'in_game':
                Ing.draw()
                if day_manager.uptdate(100):
                    state = 'post_game'

                match Ing.handle_event(event):
                    case 'end':
                        state = 'post_game'

            case 'post_game':
                Engd.draw()
                match Engd.handle_event(event):
                    case 'exit':
                        running = False
                    case 'home':
                        state = 'home'

            case 'credits':
                Befg.credits()
                match Befg.handle_event(event):
                    case 'home':
                        state = 'home'


    

    pg.display.flip()
    pg.time.Clock().tick(settings.Fps)




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