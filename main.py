#  boucle principale -- > execution du programme complet
import pygame as pg
from Pygame.pygame import Before_Game
import settings

running = True
pg.init()
Befg = Before_Game(pg.display.set_mode(settings.Display_size))
Befg.draw()
while running: 
    for event in pg.event.get():
        if Befg.handle_event(event) == 'left':
            running = False
    pg.display.flip()
    pg.time.Clock().tick(60)
