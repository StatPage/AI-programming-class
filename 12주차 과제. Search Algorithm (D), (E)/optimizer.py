from setup import Setup
import random
import math
import numpy as np

class Optimizer(Setup):
    def __init__(self):
        Setup.__init__(self)
        self._pType = 0       # Problem type
        self._numExp = 5

    def getAType(self):
        return self._aType

    def getNumExp(self):
        return self._numExp

    def displayNumExp(self):
        print()
        print("Number of experiments:", self._numExp)

    def setVariables(self, pType, aType, delta, alpha, dx, numExp):
        self._pType = pType
        self._aType = aType
        self._delta = delta
        self._alpha = alpha
        self._dx = dx
        self._numExp = numExp

class HillClimbing(Optimizer):
    def __init__(self):
        Optimizer.__init__(self)
        self._numRestart = 10
        self._limitStuck = 100      # Max evaluations with no improvement

    def randomRestart(self, p):
        dict1 = {}
        for _ in range(self._numRestart):
            p.setNumEval()
            self.run(p)
            dict1[p.getValue()] = p.getSolution()
        list1 = list(dict1.keys())
        list2 = sorted(list1)
        print(list2)
        value = list2[0]
        solution = dict1[value]
        p.storeResult(solution, value)

    def displaySetting(self):
        if self._pType == 1:
            print()
            print("Number of random restarts:", self._numRestart)
            print()
            print("Mutation step size:", self._delta)

    def run(self):
        pass

class SteepestAscent(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: Steepest-Ascent HIll Climbing")
        HillClimbing.displaySetting(self)   # Inherited. 상속을 선택할 수 있다.

    def run(self, p):
        current = p.randomInit()   # A current candidate solution
        valueC = p.evaluate(current)
        while True:
            neighbors = p.mutants(current)
            successor, valueS = self.bestOf(neighbors, p)
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS
        p.storeResult(current, valueC)

    def bestOf(self, neighbors, p):
        best = neighbors[0]
        bestValue = p.evaluate(best)
        for i in range(1, len(neighbors)):
            newValue = p.evaluate(neighbors[i])
            if newValue < bestValue:
                best = neighbors[i]
                bestValue = newValue
        return best, bestValue

class FirstChoice(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: First-Choice HIll Climbing")
        HillClimbing.displaySetting(self)
        print("Max evaluations with no improvement: {0:,} iterations".format(self._limitStuck))

    def run(self, p):
        current = p.randomInit()
        valueC = p.evaluate(current)
        i = 0
        while i < self._limitStuck:
            successor = p.randomMutant(current)
            valueS = p.evaluate(successor)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0
            else:
                i += 1
        p.storeResult(current, valueC)

class GradientDescent(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: Gradient Descent")
        print()
        print("Update rate:", self._alpha)
        print("Increment for calculating derivatives:", self._dx)

    def run(self, p):
        currentP = p.randomInit()
        valueC = p.evaluate(currentP)
        while True:
            nextP = p.takeStep(currentP, valueC)
            valueN = p.evaluate(nextP)
            if valueN >= valueC:
                break
            else:
                currentP = nextP
                valueC = valueN
        p.storeResult(currentP, valueC)

class Stochastic(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: Stochastic HIll Climbing")
        HillClimbing.displaySetting(self)
        print("Max evaluations with no improvement: {0:,} iterations".format(self._limitStuck))

    def run(self, p):
        current = p.randomInit()
        valueC = p.evaluate(current)
        i = 0
        while i < self._limitStuck:
            neighbors = p.mutants(current)
            successor, valueS = self.stochasticBest(neighbors, p)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0
            else:
                i += 1
        p.storeResult(current, valueC)

    def stochasticBest(self, neighbors, p):
        # Smaller valuse are better in the following list
        valuesForMin = [p.evaluate(indiv) for indiv in neighbors]
        largeValue = max(valuesForMin) + 1
        valuesForMax = [largeValue - val for val in valuesForMin]
        # Now, larger values are better
        total = sum(valuesForMax)
        randValue = random.uniform(0, total)
        s = valuesForMax[0]
        for i in range(len(valuesForMax)):
            if randValue <= s: # The one with index i is chosen
                break
            else:
                s += valuesForMax[i+1]
        return neighbors[i], valuesForMin[i]


class MetaHeuristics(Optimizer):
    def __init__(self):
        self._limitEval = 50000
        self._whenBestFound = 1
        self._numSample = 10

    def getWhenBestFound(self):
        return self._whenBestFound

    def displaySetting(self):
        if self._pType == 1:
            print()
            print("Number of evaluations with no imporvement {0:,} iterations:".format(self._limitEval))
            print()
            print("Mutation step size:", self._delta)

class Simulated(MetaHeuristics):
    """ Simulated annealing calls the following methods.
        initTemp returns an initial temperature such that the probability of
        accepting a worse neighbor is 0.5, i.e., exp(–dE/t) = 0.5.
        tSchedule returns the next temperature according to an annealing schedule."""
    def displaySetting(self):
        print()
        print("Search Algorithm: Simulated Annealing HIll Climbing")
        MetaHeuristics.displaySetting(self)

    def run(self, p):
        p.setNumEval()
        current = p.randomInit()
        valueC = p.evaluate(current)
        t = self.initTemp(p)
        while p._numEval < self._limitEval:
            neighbors = p.mutants(current)
            successor = random.choice(neighbors)
            valueS = p.evaluate(successor)
            dE = valueS - valueC
            if dE < 0:
                valueC, current = valueS, successor
            else:
                prob = np.random.binomial(1, math.exp((-1) * dE / t))
                if prob == 1:
                    valueC, current = valueS, successor
                    self._whenBestFound = p._numEval
                else:
                    pass
            if t < 1e-10:
                p.storeResult(current, valueC)
            t = self.tSchedule(t)
        p.storeResult(current, valueC)

    def initTemp(self, p): # To set initial acceptance probability to 0.5
        diffs = []
        for i in range(self._numSample):
            c0 = p.randomInit()     # A random point
            v0 = p.evaluate(c0)     # Its value
            c1 = p.randomMutant(c0) # A mutant
            v1 = p.evaluate(c1)     # Its value
            diffs.append(abs(v1 - v0))
        dE = sum(diffs) / self._numSample  # Average value difference
        t = dE / math.log(2)        # exp(–dE/t) = 0.5
        return t

    def tSchedule(self, t):
        return t * (1 - (1 / 10**4))
