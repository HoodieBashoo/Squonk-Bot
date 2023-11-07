import time

class Timer():
    def __init__(self, total_seconds, channel, result_func):
        self.total_seconds = total_seconds
        self.current_seconds = total_seconds
        self.channel = channel
        self.result_func = result_func
        self.is_ticking = False

    async def start_timer(self):
        self.is_ticking = True
        while self.is_ticking:
            time.sleep(1)
            print(self.current_seconds)
            self.current_seconds -= 1
            if self.current_seconds <= 0:
                self.is_ticking = False
                await self.result_func(self.channel)

    def stop_timer(self):
        self.is_ticking = False

    def set_timer(self, seconds):
        self.current_seconds = seconds

    def reset_timer(self):
        print("timer reset")
        self.current_seconds = self.total_seconds