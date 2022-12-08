#Transfer Functions Definitions: F1-F3 S-shaped, F4-F8 V-Shaped
import math
import numpy
import random

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

def F4(vector):
    SLOPE = 1
    for index, arr in enumerate(vector):
        vector[index] = math.tanh(-arr * SLOPE)
    return vector


def S1(x):
    return 1 / (1 + numpy.exp(-(2 * x)))


def S2(x):
    return 1 / (1 + numpy.exp(-x))


def S3(x):
    return 1 / (1 + numpy.exp(-(x / 2)))


def S4(x):
    return 1 / (1 + numpy.exp(-(x / 3)))


def V1(x):
    VectorLength = len(x)
    y = [0] * VectorLength
    for i in range(VectorLength):
        y[i] = abs(math.erf(x[i]))
    return y


def V2(x):
    return abs(numpy.tanh(x))


def V3(x):
    return abs(x / numpy.sqrt(1 + x * x))


def V4(x):
    return abs((2 / math.pi) * numpy.arctan((math.pi / 2) * x))