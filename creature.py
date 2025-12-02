# methodes pour gerer les creatures
from random import randint as rd

class  Creature():
    """
    Entrée : Speed, Size, View (float, compris entre 1 et 10) 
    """
    def __init__(self, Speed, Size, View, Color = 'red'):
        self.speed = Speed
        self.size = Size
        self.view = View
        self.color = Color
        self.ate = 0

    def __str__(self):
        """
        affiche les entitées        
        """
        pass

    def Baby(self, variation_speed,  variation_size,  variation_view ):
        """
        Se reproduit avec un pourcentage de proximité a ses parametres actuels
        """
        Creature(self.speed * rd(100 - variation_speed, 100 + variation_speed), self.view * rd(100 - variation_size, 100 + variation_size), self.speed * rd(100 - variation_view, 100 + variation_view), self.color)

    def Eat(self):
        """
        A mangé
        """
        self.ate += 1
        if True:
            pass

    def New_Day(self):
        """
        Gere un nouveau jour
        """
        self.ate = 0
