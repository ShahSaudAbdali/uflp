import random
import math
import numpy

UB = 31
bounds = [0, UB]
arraySize = math.ceil(math.log(UB, 2))
array = numpy.random.randn(arraySize)

def transformingFunction(x):
    return 1/(1 + numpy.exp(-2 * x))

def binaryToDecimal(xValues):
    sum = 0
    for index, item in enumerate(xValues):
        sum += numpy.power(2, len(xValues) - index - 1) * item
    return sum

def objectiveFunction(x):
    return - (x*x) + 5                  #-x^2+5

def transformArray():
    for index, item in enumerate(array):
        array[index] = transformingFunction(item)

def transformToBinary():
    for index, item in enumerate(array):
        if item > random.random():
            array[index] = 1
        else: array[index] = 0

print("Array:", array)
transformArray()
print("Array After Transform:", array)
transformToBinary()
print("Array Binary Transform:", array)
decNumber = binaryToDecimal(array)
print("Decimal Number:", decNumber)
print("Optimal Solution:", objectiveFunction(decNumber))
