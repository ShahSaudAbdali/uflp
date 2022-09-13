#Transfer Functions Definitions: F1-F3 S-shaped, F4-F8 V-Shaped
import math

def F1(vector):
    for index, arr in enumerate(vector):
        vector[index] = 1 / (1 + math.exp(-arr))
    return vector

def F2(vector):
    SLOPE = 1
    for index, arr in enumerate(vector):
        vector[index] = 1 / (1 + math.exp(-arr/SLOPE))
    return vector

def F3(vector):
    SLOPE = 1
    for index, arr in enumerate(vector):
        vector[index] = 1 / (1 + math.exp(-arr * SLOPE))
    return vector

def F2(vector):
    SLOPE = 1
    for index, arr in enumerate(vector):
        vector[index] = math.tanh(-arr * SLOPE)
    return vector