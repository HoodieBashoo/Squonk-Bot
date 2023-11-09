import time


class Timer():
    def __init__(self, total_seconds, channel, result_func):
        self.total_seconds = total_seconds
        self.current_seconds = 0
        self.starting_time = None
        self.channel = channel
        self.result_func = result_func
        self.is_ticking = False

    async def start_timer(self):
        self.is_ticking = True
        self.starting_time = time.time()
        while self.is_ticking:
            current_time = time.time()
            print(current_time)
            self.current_seconds = current_time - self.starting_time

            if self.current_seconds >= self.total_seconds:
                self.is_ticking = False
                await self.result_func(self.channel)

    def stop_timer(self):
        self.is_ticking = False

    def reset_timer(self):
        print("timer reset")
        self.current_seconds = 0
        self.starting_time = time.time()