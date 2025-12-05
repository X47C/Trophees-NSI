# methodes pour gerer les creatures
from random import randint as rd

class  Creature():
    """
    Entrée : Speed, Size, View (float, compris entre 1 et 10) 
    """
    def __init__(self, Speed, Size, View, Variation_Speed, Variation_Size, Variation_View, Days_Max, Color):
        self.speed = Speed
        self.size = Size
        self.view = View
        self.color = Color
        self.ate = 0
        self.energy = 100
        self.variation_speed = Variation_Speed
        self.variation_size = Variation_Size
        self.variation_view = Variation_View
        self.days = 0
        self.days_max = Days_Max

    def Baby(self):
        """
        Se reproduit avec un pourcentage de proximité a ses parametres actuels
        """
        Creature(self.speed * rd(100 - self.variation_speed, 100 + self.variation_speed), self.view * rd(100 - self.variation_size, 100 + self.variation_size), self.speed * rd(100 - self.variation_view, 100 + self.variation_view), self.color)

    def Eat(self):
        """
        A mangé
        """
        self.ate += 1
        if self.ate == 1:
            self.energy = 100
        else:
            self.Baby()
            self.energy = 0

    def New_Day(self):
        """
        Gere un nouveau jour
        """
        if self.ate >= 1 and not self.days >= self.days_max:
            pass


    def is_alive(self):
        """
        Check si le mec est en vie renvois True ou false
        """
        pass

    def lives(self):
        """
        Tue le mec si il as plus d'energie, fait en sorte que il aille ou non a un nouveaux jour celon son age et la bouffe qu'il as mangé
        Consomme l'energie aussi ect
        """
        pass

    def get_color(self):
        """
        renvoie la couleur du machin
        """
        return self.color

