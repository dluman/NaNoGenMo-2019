import random

class Rule:

    def __init__(self):
        self.factors = [
            .75,
            1.0,
            1.25
        ]
        self.scale_factor = self.set_scale()
    
    def set_scale(self):
        seed = random.randint(0,len(self.factors) -1)
        return self.factors[seed]