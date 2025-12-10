#  boucle principale -- > execution du programme complet
import pygame as pg
from Pygame.pygame import Before_Game, Settings, In_Game, Post_Game
import settings

running = True
pg.init()

Befg = Before_Game(pg.display.set_mode(settings.Display_size))
Sett = Settings(pg.display.set_mode(settings.Display_size))
Ing = In_Game(pg.display.set_mode(settings.Display_size))
Engd = Post_Game(pg.display.set_mode(settings.Display_size))


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
    pg.time.Clock().tick(60)
