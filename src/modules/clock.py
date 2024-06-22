class Timer:
    def __init__(self, threshold: int):
        self.threshold = threshold
        self.elapsed_time = 0
        self.is_active = True  


    def update(self, dt: int):
        if self.is_active:
            self.elapsed_time += dt

    def is_triggered(self) -> bool:
        if not self.is_active: 
            return False
        return self.elapsed_time >= self.threshold

    def reset(self):
        self.elapsed_time = 0
        self.is_active = True
        
    def stop(self):  
        self.is_active = False
        self.elapsed_time = 0