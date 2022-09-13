#Definitions of binarization methods

import random

def M1(vector):
    for index, arr in enumerate(vector):
        rand = random.random()
        if (arr < rand):
            vector[index] = 0
        else:
            vector[index] = 1
        index += 1