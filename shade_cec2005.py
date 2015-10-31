#!/bin/env python
"""
This program allow to run the SHADE algorithm using the CEC'2005 benchmark.

TODO
"""
from cec2005real.cec2005 import Function
import SHADE as shade
import argparse
import numpy
import sys
import os

def main(args):
    "Main program."
    parser = argparse.ArgumentParser(description="Running SHADE with 2005 Benchmark")
    parser.add_argument('-f', dest='fun', type=int, choices=range(1, 26),
                         required=True,
                         help="the function value [1-25]")
    
    parser.add_argument('-d', dest='dim', type=int, choices=[2, 10, 30, 50],
                        required=True,
                         help="the dimensionality [2, 10, 30, 50]")
    
    parser.add_argument('-r', dest='run', default=25, type=int,
                         help="run times")

    parser.add_argument('-s', dest='seedid', required=True, type=int,
                         help="seed", choices=range(1, 6))

    params = parser.parse_args(args)
    seeds = [12345679, 32379553, 235325, 5746435, 253563]

    if (params.run <= 0):
        parser.print_help()
        return

    # Set the seeds
    numpy.random.seed(seeds[params.seedid-1])

    dim = params.dim
    fid = params.fun
    fun = Function(fid, dim)
    info = fun.info()
    fitness_fun = fun.get_eval_function()
    output = "results/shade_cec2005_f{0}d{1}_s{2}r{3}".format(fid, dim, params.seedid, params.run)
    info['best'] = 0
    ignoreLimits = (fid != 7 and fid != 25)
    noisy = (fid == 4 or fid == 25)

    
    if os.path.exists(output):
        return

    for r in range(params.run):
        result,bestIndex = shade.improve(fitness_fun, info, dim, 10000*dim,
                                         name_output=output, replace=True, times=params.run, popsize=100, ignoreLimits=ignoreLimits)
        best_sol = result.solution
        best_fitness = result.fitness

        if not noisy:
            assert(fitness_fun(best_sol)==best_fitness)

if __name__ == '__main__':
    main(sys.argv[1:])
