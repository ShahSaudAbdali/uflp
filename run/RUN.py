import mat2py as mp
from mat2py.core import *


def RUN(nP, MaxIt, lb, ub, dim, fobj):
    Cost = zeros(nP, 1)
    X = initialization(nP, dim, ub, lb)
    Xnew2 = zeros(1, dim)
    Convergence_curve = zeros(1, MaxIt)
    for i in M[1:nP]:
        Cost[I[i]] = fobj(X[I[i, :]])

    Best_Cost, ind = min(Cost)
    Best_X = X[I[ind, :]]
    Convergence_curve[I[1]] = copy(Best_Cost)
    it = 1
    while it < MaxIt:
        it = it + 1
        f = 20 * exp(-(12 * (mrdivide(it, MaxIt))))
        Xavg = mean(X)
        SF = (2 * (0.5 - rand(1, nP))) * f
        for i in M[1:nP]:
            _, ind_l = min(Cost)
            lBest = X[I[ind_l, :]]
            A, B, _C = RndX(nP, i)
            _, ind1 = min(Cost(M[[A, B, _C]]))
            gama = (rand * (X[I[i, :]] - (rand(1, dim) * (ub - lb)))) * exp(
                mrdivide((-4) * it, MaxIt)
            )
            Stp = rand(1, dim) * ((Best_X - (rand * Xavg)) + gama)
            DelX = (2 * rand(1, dim)) * abs(Stp)
            if Cost(i) < Cost(ind1):
                Xb = X[I[i, :]]
                Xw = X[I[ind1, :]]
            else:
                Xb = X[I[ind1, :]]
                Xw = X[I[i, :]]
            SM = RungeKutta(Xb, Xw, DelX)
            L = rand(1, dim) < 0.5
            Xc = (L * X[I[i, :]]) + ((1 - L) * X[I[A, :]])
            Xm = (L * Best_X) + ((1 - L) * lBest)
            vec = M[[1, -1]]
            flag = floor((2 * rand(1, dim)) + 1)
            r = vec(flag)
            g = 2 * rand
            mu = 0.5 + (0.1 * randn(1, dim))
            if rand < 0.5:
                Xnew = ((Xc + (((r * SF(i)) * g) * Xc)) + (SF(i) * SM)) + (
                    mu * (Xm - Xc)
                )
            else:
                Xnew = ((Xm + (((r * SF(i)) * g) * Xm)) + (SF(i) * SM)) + (
                    mu * (X[I[A, :]] - X[I[B, :]])
                )
            FU = Xnew > ub
            FL = Xnew < lb
            Xnew = ((Xnew * (_not(FU + FL))) + (ub * FU)) + (lb * FL)
            CostNew = fobj(Xnew)
            if CostNew < Cost(i):
                X[I[i, :]] = copy(Xnew)
                Cost[I[i]] = copy(CostNew)
            if rand < 0.5:
                EXP = exp(mrdivide(((-5) * rand) @ M[it], MaxIt))
                r = floor(Unifrnd(-1, 2, 1, 1))
                u = 2 * rand(1, dim)
                w = Unifrnd(0, 2, 1, dim) * EXP
                A, B, _C = RndX(nP, i)
                Xavg = ((X[I[A, :]] + X[I[B, :]]) + X[I[_C, :]]) / 3
                beta = rand(1, dim)
                Xnew1 = (beta * Best_X) + ((1 - beta) * Xavg)
                for j in M[1:dim]:
                    if w(j) < 1:
                        Xnew2[I[j]] = Xnew1(j) + (
                            (M[M[r] @ w(j)]) @ abs((Xnew1(j) - Xavg(j)) + randn)
                        )
                    else:
                        Xnew2[I[j]] = (Xnew1(j) - Xavg(j)) + (
                            (M[M[r] @ w(j)])
                            @ abs(((u(j) * Xnew1(j)) - Xavg(j)) + randn)
                        )

                FU = Xnew2 > ub
                FL = Xnew2 < lb
                Xnew2 = ((Xnew2 * (_not(FU + FL))) + (ub * FU)) + (lb * FL)
                CostNew = fobj(Xnew2)
                if CostNew < Cost(i):
                    X[I[i, :]] = copy(Xnew2)
                    Cost[I[i]] = copy(CostNew)
                else:
                    if rand < w(randi(dim)):
                        SM = RungeKutta(X[I[i, :]], Xnew2, DelX)
                        Xnew = (Xnew2 - (rand * Xnew2)) + (
                            M[SF(i)] @ (SM + (((2 * rand(1, dim)) * Best_X) - Xnew2))
                        )
                        FU = Xnew > ub
                        FL = Xnew < lb
                        Xnew = ((Xnew * (_not(FU + FL))) + (ub * FU)) + (lb * FL)
                        CostNew = fobj(Xnew)
                        if CostNew < Cost(i):
                            X[I[i, :]] = copy(Xnew)
                            Cost[I[i]] = copy(CostNew)
            if Cost(i) < Best_Cost:
                Best_X = X[I[i, :]]
                Best_Cost = Cost(i)

        Convergence_curve[I[it]] = copy(Best_Cost)
        disp(
            M[["it : ", num2str(it), ", Best Cost = ", num2str(Convergence_curve(it))]]
        )

    return Best_Cost, Best_X, Convergence_curve


def Unifrnd(a, b, c, dim):
    a2 = a / 2
    b2 = b / 2
    mu = a2 + b2
    sig = b2 - a2
    z = mu + (sig * ((2 * rand(c, dim)) - 1))
    return z