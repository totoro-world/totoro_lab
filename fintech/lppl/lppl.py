import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fmin_tnc
import random
import pandas as pd
from pandas import Series, DataFrame
import datetime
import itertools
import wind_util

sz = wind_util.get_close_price('399985.SZ',
                               datetime.datetime.strptime('20130716', '%Y%m%d'),
                               datetime.datetime.strptime('20190228', '%Y%m%d'))
date = sz.index
time = np.linspace(0, len(sz)-1, len(sz))
close = np.array(np.log(sz))
DataSeries = [time, close]

def lppl (t,x): #return fitting result using LPPL parameters 
    a = x[0]
    b = x[1]
    tc = x[2]
    m = x[3]
    c = x[4]
    w = x[5]
    phi = x[6]
    return a + (b*np.power(tc - t, m))*(1 + (c*np.cos((w *np.log(tc-t))+phi)))

def func(x):
    delta = [lppl(t,x) for t in DataSeries[0]]
    delta = np.subtract(delta, DataSeries[1])
    delta = np.power(delta, 2)
    return np.sum(delta)

class Individual:
    """base class for individuals"""

    def __init__ (self, InitValues):
        self.fit = 0
        self.cof = InitValues

    def fitness(self):
        try:
            cofs, nfeval, rc = fmin_tnc(func, self.cof, fprime=None,approx_grad=True, messages=0)
            self.fit = func(cofs)
            self.cof = cofs
        except:
            #does not converge
            return False

    def mate(self, partner):
        reply = []
        for i in range(0, len(self.cof)):
            if (random.randint(0,1) == 1):
                reply.append(self.cof[i])
            else:
                reply.append(partner.cof[i])
        return Individual(reply)

    def mutate(self):
        for i in range(0, len(self.cof)-1):
            if (random.randint(0,len(self.cof)) <= 2):
                self.cof[i] += random.choice([-1,1]) * .05 * i

    def PrintIndividual(self):
        #t, a, b, tc, m, c, w, phi
        cofs = "A: " + str(round(self.cof[0], 3))
        cofs += "B: " + str(round(self.cof[1],3))
        cofs += "Critical Time: " + str(round(self.cof[2], 3))
        cofs += "m: " + str(round(self.cof[3], 3))
        cofs += "c: " + str(round(self.cof[4], 3))
        cofs += "omega: " + str(round(self.cof[5], 3))
        cofs += "phi: " + str(round(self.cof[6], 3))
        return "fitness: " + str(self.fit) +"\n" + cofs

    def getDataSeries(self):
        return DataSeries

    def getExpData(self):
        return [lppl(t,self.cof) for t in DataSeries[0]]

    def getTradeDate(self):
        return date

def fitFunc(t, a, b, tc, m, c, w, phi):
    return a - (b*np.power(tc - t, m))*(1 + (c*np.cos((w *np.log(tc-t))+phi)))

class Population:
    """base class for a population"""

    LOOP_MAX = 1000

    def __init__ (self, limits, size, eliminate, mate, probmutate, vsize):
        'seeds the population'
        'limits is a tuple holding the lower and upper limits of the cofs'
        'size is the size of the seed population'
        self.populous = []
        self.eliminate = eliminate
        self.size = size
        self.mate = mate
        self.probmutate = probmutate
        self.fitness = []
        for i in range(size):
            SeedCofs = [random.uniform(a[0], a[1]) for a in limits]
            self.populous.append(Individual(SeedCofs))

    def PopulationPrint(self):
        for x in self.populous:
            print(x.cof)

    def SetFitness(self):
        self.fitness = [x.fit for x in self.populous]

    def FitnessStats(self):
        #returns an array with high, low, mean
        return [np.amax(self.fitness), np.amin(self.fitness), np.mean(self.fitness)]

    def Fitness(self):
        counter = 0
        false = 0
        for individual in list(self.populous):
            print('Fitness Evaluating: ' + str(counter) +  " of " + str(len(self.populous)) + "        \r"),
            state = individual.fitness()
            counter += 1
            if ((state == False)):
                false += 1
                self.populous.remove(individual)
        self.SetFitness()
        print("\n fitness out size: " + str(len(self.populous)) + " " + str(false))

    def Eliminate(self):
        a = len(self.populous)
        self.populous.sort(key=lambda ind: ind.fit)
        while (len(self.populous) > self.size * self.eliminate):
            self.populous.pop()
        print("Eliminate: " + str(a- len(self.populous)))

    def Mate(self):
        counter = 0
        while (len(self.populous) <= self.mate * self.size):
            counter += 1
            i = self.populous[random.randint(0, len(self.populous)-1)]
            j = self.populous[random.randint(0, len(self.populous)-1)]
            diff = abs(i.fit-j.fit)
            if (diff < random.uniform(np.amin(self.fitness), np.amax(self.fitness) - np.amin(self.fitness))):
                self.populous.append(i.mate(j))
            if (counter > Population.LOOP_MAX):
                print("loop broken: mate")
                while (len(self.populous) <= self.mate * self.size):
                    i = self.populous[random.randint(0, len(self.populous)-1)]
                    j = self.populous[random.randint(0, len(self.populous)-1)]
                    self.populous.append(i.mate(j))
        print("Mate Loop complete: " + str(counter))

    def Mutate(self):
        counter = 0
        for ind in self.populous:
            if (random.uniform(0, 1) < self.probmutate):
                ind.mutate()
                ind.fitness()
                counter +=1
        print("Mutate: " + str(counter))
        self.SetFitness()

    def BestSolutions(self, num):
        reply = []
        self.populous.sort(key=lambda ind: ind.fit)
        for i in range(num):
            reply.append(self.populous[i])
        return reply;

    random.seed()
