import random

class Rule:

    def __init__(self):
        self.factors = [.25,.50,.75]
        self.scale_factor = self.set_scale()
    
    @staticmethod
    def set_scale():
        seed = random.randint(0,len(factors) -1)
        return self.factors[seed]