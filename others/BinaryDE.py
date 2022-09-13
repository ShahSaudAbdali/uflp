import random

x1 = [1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1]
x2 = [0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0]
x3 = [0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0]
coeff_F = 0.7


def calculateM(x, y, a, b):
    count = 0
    for i in range(len(x1)):
        if (x[i] == a) & (y[i] == b):
            count = count + 1
    return count


def main():
    m11 = calculateM(x2, x3, 1, 1)
    m01 = calculateM(x2, x3, 0, 1)
    m10 = calculateM(x2, x3, 1, 0)
    sim_x2_x3 = m11/(m11 + m10 + m01)
    dsim_x2_x3 = 1 - sim_x2_x3
    valueA = coeff_F * dsim_x2_x3
    print("Value of A in (Xr2, Xr3):", valueA)

    n1 = n0 = 0
    # calculate 0s and 1s in the first array
    n1 = x1.count(1)
    n0 = len(x1) - n1
    print("M11 + M01 =", n1)
    print("0 <= M10 <=", n0)

    min_z = abs(dsim_x2_x3 - valueA)
    print("minZ: ", min_z)

    # populate indices of 0s and 1s array
    onesIndices = []
    zeroIndices = []
    for i in range(len(x1)):
        if x1[i]:
            onesIndices.append(i)
        else:
            zeroIndices.append(i)

    print("1 indices in x1:", onesIndices)
    print("0 indices in x1:", zeroIndices)

    # print(random.choice(onesIndices))
    totalIterations = 0
    mX = [0, 0, 0]
    diff = 1
    resX = []
    for i in range(n1 + 1):
        m11 = i
        m01 = n1 - i
        for j in range(n0 + 1):
            totalIterations += 1
            m10 = j
            # print(m11, m01, m10)
            xr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for k in range(m11):
                xr[random.choice(onesIndices)] = 1
            xr[random.choice(zeroIndices)] = 1
            # print(i+1, "Mutant Vector:", xr)

            dis_xr_x1 = 1 - calculateM(xr, x1, 1, 1)/(calculateM(xr, x1,
                                                                 1, 1) + calculateM(xr, x1, 0, 1) + calculateM(xr, x1, 1, 0))
            # print("dis:", dis_xr_x1)

            if abs(dis_xr_x1 - min_z) < diff:
                mX[0] = m11
                mX[1] = m01
                mX[2] = m10
                resX = xr
                diff = abs(dis_xr_x1 - min_z)

    print("Total Iterations: ", totalIterations)
    print("Optimal Solution: ", resX, " with diff: ",
          diff, "and m11, m01 & m10 = ", mX[0], mX[1], mX[2])


# calling the main function
main()