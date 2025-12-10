import settings

class Day_Manager():
    def __init__(self):
        self.current_day = 0
        self.time = 0

    def update(self, dt):
        """
        dt = temps passé depuis la derniere fois que la fonction as étée appelée
        """
        self.time += dt
        if self.time >= settings.day_duration:
            if self.current_day >= settings.day_number:
                return 'end'
            else:
                self.new_day()

    def new_day(self):
        """
        ce que doit faire le jeu a chaques debuts de jours
        """
        self.current_day += 1


