import random

def bournoli(probability):
    if(probability < random.uniform(0, 1)):
        return False
    return True