#  boucle principale -- > execution du programme complet
from Pygame.pygame import Before_Game as BeGame 
import pygame as pg
def main():
    """
    Docstring for main
    """
    before_game = BeGame(pg.display.set_mode((400,400))) #400*400 n'est pas la taille définive
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == BeGame.Button_Left_click:

    