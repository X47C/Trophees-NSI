import settings

class Day_Manager():
    def __init__(self):
        self.current_day = 0
        self.day_duration = settings.Day_Duration
        self.time = 0

    def uptdate(self, dt):
        """
        dt = temps passé depuis la derniere fois que la fonction as étée appelée
        """
        self.time += dt
        if self.time >= self.day_duration:
            return True

    def new_day(self):
        pass


