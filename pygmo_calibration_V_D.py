import time
import os
import numpy as np
import shutil
from   datetime import datetime
import socket
import pandas as pd
import glob
import matplotlib.pyplot as plt
import pygmo as pg
import multiprocessing
from   functions import *


class UDP: # user defined problem
    def __init__(self,\
                 problem_name,\
                 x_l,\
                 x_u,\
                 x_name):
        self.problem_name = problem_name
        self.x_l = x_l
        self.x_u = x_u
        self.dim = len(self.x_u)

    # Return number of objectives
    def get_nobj(self):
        return 1

    # Return bounds of decision variables
    def get_bounds(self):
        lower = self.x_l
        upper = self.x_u
        return (lower,upper)

    # Return function name
    def get_name(self):
        return self.problem_name

    # number of dimensions
    def get_extra_info(self):
        return "\tDimensions: " + str(self.dim)

    # return the objective function
    def fitness(self, x):
        f1 = run_mizuRoute(x[0],x[1],str(os.getpid()))
        return [f1]


# serial
prob = pg.problem(UDP('mizuRoute',[0.1,500],[2,20000],['velocity','diffusivity']))
algo = pg.algorithm(pg.sga())
pop = pg.population(prob, size=200)
pop = algo.evolve(pop)
print(pop)
# extract results
fits, vectors = pop.get_f(), pop.get_x()
print(fits[0])
print(vectors[0,:])
# extract and print non-dominated fronts
ndf, dl, dc, ndr = pg.fast_non_dominated_sorting(fits)


# if __name__ == "__main__": # https://github.com/esa/pagmo2/issues/199


#     nworkers = len(os.sched_getaffinity(0))
#     print('number of network is: ',nworkers)
#     pg.mp_island.init_pool(nworkers)

#     # Problem definition
#     prob = pg.problem(UDP())

#     # algorithm
#     algo = pg.algorithm(pg.sga())
#     # algo = pg.algorithm(pg.de())
#     # algo = pg.algorithm(pg.sea())
#     # algo = pg.algorithm(pg.pso())
#     # algo = pg.algorithm(pg.pso_gen())

#     # archipelago tests
#     # test 1
#     # archi = pg.archipelago(n= 4, algo = algo, prob = prob, pop_size = 100)
#     # test 2
#     archi = pg.archipelago(n= nworkers, algo = algo, prob = prob, pop_size = 10, udi=pg.mp_island())
#     # test 3
#     # archi = pg.archipelago(n= 4, algo = algo, prob = prob, pop_size = 100, udi=pg.mp_island())
#     # archi.set_topology(pg.topology(pg.ring()))

#     # evolve the archis
#     # for i in range(5):
#     archi.evolve(200)
#     archi.wait()
#     print(archi)
#     print(archi.get_champions_f())
#     print(archi.get_champions_x())
#     print('-----------------------------------')


#     # https://stackoverflow.com/questions/52635269/get-evolution-log-from-a-pygmo-archipelago
#     for island in archi: # iterate through islands
#         print(island)

#     # get the file name with a outut pattern
#     file_names = glob.glob('./test_gmo/*/output.csv')
#     results = pd.DataFrame()
#     for file_name in file_names:
#         temp = pd.read_csv(file_name)
#         results = pd.concat([results, temp], axis=0)
#     print(results)
#     results['datetime'] = pd.to_datetime(results['time'], format='%Y-%m-%d %H:%M:%S.%f')
#     results = results.set_index('datetime')
#     results = results.sort_index()
#     results.to_csv('results.csv')
#     results['pid'].plot()
#     plt.savefig('results.png', dpi = 1000)

