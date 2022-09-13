import math
import random
import array
from numpy.random import seed
from numpy.random import randn
import numpy as np

#Parsing the input file from ORLIB. Resource can be found @https://resources.mpi-inf.mpg.de/departments/d1/projects/benchmarks/UflLib/packages.html
fileRef = open("./ORLIB/ORLIB-cap/40/cap41.txt", "r")
file = fileRef.readlines()
populateFacilityList = False
facilityIndex = 0
for index, value in enumerate(file):
    print(index, value)
    if index == 0:
        getValue = value
        getValue = getValue.split()
        facility_count = int(getValue[0])
        location_count = int(getValue[1])
        populateFacilityList = True
    # if populateFacilityList:


print("Facility Count:", facility_count)
print("Location Count:", location_count)

#defining array of n-bits, n = location x log (facility count) - in Encoding 1
bits_for_encoding1 = [0] * int(location_count * math.log(facility_count, 2))
print(len(bits_for_encoding1))

#using transfer function
index = 0
for arr in bits_for_encoding1:
    bits_for_encoding1[index] = 1 / (1 + math.exp(-arr))
    index += 1

#using binarization
index = 0
for arr in bits_for_encoding1:
    rand = random.random()
    if(rand < 0.5):
        bits_for_encoding1[index] = 0
    else: bits_for_encoding1[index] = 1
    index += 1

#Create the data arrays for each facility
# for i in range(50):


#print matrix
print(bits_for_encoding1)
