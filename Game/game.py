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
            return True

    def new_day(self):
        pass


