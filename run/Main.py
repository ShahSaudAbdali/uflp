import mat2py as mp
from mat2py.core import *


def main():
    clear
    close("all")
    clc
    nP = 50
    Func_name = "F1"
    MaxIt = 100
    lb, ub, dim, fobj = BenchmarkFunctions(Func_name)
    Best_fitness, BestPositions, Convergence_curve = RUN(nP, MaxIt, lb, ub, dim, fobj)
    figure
    hold("on")
    semilogy(Convergence_curve, "Color", "r", "LineWidth", 4)
    title("Convergence curve")
    xlabel("Iteration")
    ylabel("Best fitness obtained so far")
    axis("tight")
    grid("off")
    box("on")
    legend("RUN")


if __name__ == "__main__":
    main()