

class Timer:
    def __init__(self, ticks, interval, callback, user_data=None):
        self.next_tick = ticks + interval
        self.user_data = user_data
        self.interval = interval
        self.callback = callback
        self.count = 0

    def update(self, ticks):
        while ticks > self.next_tick:
            self.count += 1
            self.next_tick += self.interval

        if self.count > 0:
            self.callback(self)
