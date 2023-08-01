import mat2py as mp
from mat2py.core import *


def BenchmarkFunctions(F):
    D = 30
    if F == "F1":
        fobj = F1
        lb = -100
        ub = 100
        dim = copy(D)
    elif F == "F2":
        fobj = F2
        lb = -100
        ub = 100
        dim = copy(D)
    elif F == "F3":
        fobj = F3
        lb = -100
        ub = 100
        dim = copy(D)
    elif F == "F4":
        fobj = F4
        lb = -100
        ub = 100
        dim = copy(D)
    elif F == "F5":
        fobj = F5
        lb = -100
        ub = 100
        dim = copy(D)
    elif F == "F6":
        fobj = F6
        lb = -100
        ub = 100
        dim = copy(D)
    elif F == "F7":
        fobj = F7
        lb = -100
        ub = +100
        dim = copy(D)
    elif F == "F8":
        fobj = F8
        lb = -100
        ub = 100
        dim = copy(D)
    elif F == "F9":
        fobj = F9
        lb = -100
        ub = 100
        dim = copy(D)
    elif F == "F10":
        fobj = F10
        lb = -32.768
        ub = 32.768
        dim = copy(D)
    elif F == "F11":
        fobj = F11
        lb = -100
        ub = 100
        dim = copy(D)
    elif F == "F12":
        fobj = F12
        lb = -100
        ub = 100
        dim = copy(D)
    elif F == "F13":
        fobj = F13
        lb = -600
        ub = 600
        dim = copy(D)
    elif F == "F14":
        fobj = F14
        lb = -50
        ub = 50
        dim = copy(D)
    return lb, ub, dim, fobj


def F1(x):
    D = size(x, 2)
    z = (x(1) ** 2) + ((10**6) * sum(x(M[2:D]) ** 2))
    return z


def F2(x):
    D = size(x, 2)
    for i in M[1:D]:
        f[I[i]] = abs(x(i)) ** (i + 1)

    z = sum(f)
    return z


def F3(x):
    z = (sum(x**2) + (sum(0.5 * x) ** 2)) + (sum(0.5 * x) ** 4)
    return z


def F4(x):
    D = size(x, 2)
    for i in M[1 : (D - 1)]:
        ff[I[i]] = (100 * (((x(i) ** 2) - x(i + 1)) ** 2)) + ((x(i) - 1) ** 2)

    z = sum(ff)
    return z


def F5(x):
    D = size(x, 2)
    z = ((10**6) * (x(1) ** 2)) + sum(x(M[2:D]) ** 2)
    return z


def F6(x):
    D = size(x, 2)
    for i in M[1:D]:
        f[I[i]] = (mpower(10**6, mrdivide(i - 1, D - 1))) @ (M[x(i) ** 2])

    z = sum(f)
    return z


def F7(x):
    D = size(x, 2)
    for i in M[1:D]:
        if i == D:
            f[I[i]] = 0.5 + (
                mrdivide(
                    (sin(sqrt((x(i) ** 2) + (x(1) ** 2))) ** 2) - 0.5,
                    (1 + (0.001 * ((x(i) ** 2) + (x(1) ** 2)))) ** 2,
                )
            )
        else:
            f[I[i]] = 0.5 + (
                mrdivide(
                    (sin(sqrt((x(i) ** 2) + (x(i + 1) ** 2))) ** 2) - 0.5,
                    (1 + (0.001 * ((x(i) ** 2) + (x(i + 1) ** 2)))) ** 2,
                )
            )

    z = sum(f)
    return z


def F8(x):
    D = size(x, 2)
    for i in M[1 : (D - 1)]:
        w[I[i]] = 1 + ((x(i) - 1) / 4)
        f[I[i]] = (M[(w(i) - 1) ** 2]) @ (1 + (10 * (sin((M[pi] @ w(i)) + 1) ** 2)))

    w[I[D]] = 1 + ((x(D) - 1) / 4)
    z = ((sin(M[pi] @ w(1)) ** 2) + sum(f)) + (
        (M[(w(D) - 1) ** 2]) @ (1 + (sin((2 * pi) @ M[w(D)]) ** 2))
    )
    return z


def F9(x):
    D = size(x, 2)
    for i in M[1:D]:
        y = x(i) + 4.209687462275036e002
        if abs(y) < 500:
            f[I[i]] = M[y] @ sin(abs(y) ** 0.5)
        elif y > 500:
            f[I[i]] = ((M[500 - mod(y, 500)]) @ sin(sqrt(abs(500 - mod(y, 500))))) - (
                mrdivide((y - 500) ** 2, 10000 * D)
            )
        elif y < (-500):
            f[I[i]] = (
                (M[mod(abs(y), 500) - 500]) @ sin(sqrt(abs(mod(abs(y), 500) - 500)))
            ) - (mrdivide((y + 500) ** 2, 10000 * D))

    z = (418.9829 * D) - sum(f)
    return z


def F10(x):
    D = size(x, 2)
    z = (
        (
            ((-20) * exp((-0.2) * (((mrdivide(1, D)) @ M[sum(x**2)]) ** 0.5)))
            - exp((M[mrdivide(1, D)]) @ sum(cos((2 * pi) * x)))
        )
        + 20
    ) + exp(1)
    return z


def F11(x):
    D = size(x, 2)
    x = x + 0.5
    a = 0.5
    b = 3
    kmax = 20
    c1[I[1 : (kmax + 1)]] = a ** (M[0:kmax])
    c2[I[1 : (kmax + 1)]] = (M[2 * pi]) @ (b ** (M[0:kmax]))
    f = 0
    c = -w(0.5, c1, c2)
    for i in M[1:D]:
        f = f + w(x[I[:, i]].H, c1, c2)

    z = f + (M[c] @ D)
    return z


def F12(x):
    D = size(x, 2)
    z = (
        (abs(sum(x**2) - D) ** (1 / 4)) + (mrdivide((0.5 * sum(x**2)) + sum(x), D))
    ) + 0.5
    return z


def F13(x):
    dim = size(x, 2)
    z = ((sum(x**2) / 4000) - prod(cos(x / sqrt(M[M[1:dim]])))) + 1
    return z


def F14(x):
    dim = size(x, 2)
    z = (
        (M[mrdivide(pi, dim)])
        @ (
            (
                (10 * (sin(M[pi] @ (1 + ((x(1) + 1) / 4))) ** 2))
                + sum(
                    (((x(M[1 : (dim - 1)]) + 1) / 4) ** 2)
                    * (1 + (10 * (sin(pi * (1 + ((x(M[2:dim]) + 1) / 4))) ** 2)))
                )
            )
            + (((x(dim) + 1) / 4) ** 2)
        )
    ) + sum(Ufun(x, 10, 100, 4))
    return z


def Ufun(x, a, k, m):
    o = ((k * ((x - a) ** m)) * (x > a)) + ((k * (((-x) - a) ** m)) * (x < (-a)))
    return o