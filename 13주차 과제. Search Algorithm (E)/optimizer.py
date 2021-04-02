from setup import Setup
import random
import math
import numpy as np

class Optimizer(Setup):
    def __init__(self):
        Setup.__init__(self)
        self._pType = 0       # Problem type
        self._numExp = 0      # Total number of experiments

    def setVariables(self, parameters):
        Setup.setVariables(self, parameters)
        self._pType = parameters["pType"]
        self._numExp = parameters['numExp']

    def getNumExp(self):
        return self._numExp

    def displayNumExp(self):
        print()
        print("Number of experiments:", self._numExp)

    def displaySetting(self):
        if self._pType == 1 and self._aType !=4 and self._aType != 6:
            print("Mutation step size:", self._delta)


class HillClimbing(Optimizer):
    def __init__(self):
        Optimizer.__init__(self)
        self._numRestart = 0      # number of restart
        self._limitStuck = 0      # Max evaluations with no improvement

    def setVariables(self, parameters):
        Optimizer.setVariables(self, parameters)
        self._limitStuck = parameters['limitStuck']
        self._numRestart = parameters['numRestart']

    # def randomRestart(self, p):
    #     dict1 = {}
    #     for _ in range(self._numRestart):
    #         p.setNumEval()
    #         self.run(p)
    #         dict1[p.getValue()] = p.getSolution()
    #     list1 = list(dict1.keys())
    #     list2 = sorted(list1)
    #     print(list2)
    #     value = list2[0]
    #     solution = dict1[value]
    #     p.storeResult(solution, value)

    def displaySetting(self):
        if self._numRestart > 1:    # restart를 1번 넘게 할 때만 출력하도록.
            print("Number of random restarts:", self._numRestart)
            print()
        Optimizer.displaySetting(self)
        if 2 <= self._aType <= 3:   # first-choice랑 stochastic에서 필요하기에 사용.
            print("Max evaluations with no improvement: {0:,} iterations".format(self._limitStuck))

    def run(self):
        pass

    def randomRestart(self, p):              # 'alg' is the chosen hill climber
        """내가 짠 코드와는 다르게 그냥 loop를 통해 최고 값을 갱신해줬다."""
        i = 1
        self.run(p)
        bestSolution = p.getSolution()
        bestMinimum = p.getValue()           # First solution is current best
        numEval = p.getNumEval()
        while i < self._numRestart:
            self.run(p)
            newSolution = p.getSolution()
            newMinimum = p.getValue()        # New solution
            numEval += p.getNumEval()
            if newMinimum < bestMinimum:
                bestSolution = newSolution   # Update best-so-far
                bestMinimum = newMinimum
            i += 1
        p.storeResult(bestSolution, bestMinimum)

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
        print()
        HillClimbing.displaySetting(self)

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
        print()
        HillClimbing.displaySetting(self)

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
        # neighbors의 value를 리스트로 출력. 값이 작을수록 좋은 것.
        largeValue = max(valuesForMin) + 1
        # 그러나 stochastic은 값이 좋을수록 뽑힐 확률이 높아야 되는데 이대로 사용되면 좋은 값의 확률이
        # 낮기 때문에 큰 값에서 빼줘 확률로 변환해주려고 한다. +1은 가장 큰 값이 뽑힐 확률이 0이 될 수
        # 있어서 그것을 고려해준 것.
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
        Optimizer.__init__(self)
        self._limitEval = 0       # Total # evaluations until termination
        self._whenBestFound = 0   # This is actually a reslut of experiment

    def setVariables(self, parameters):
        Optimizer.setVariables(self, parameters)
        self._limitEval = parameters['limitEval']

    def getWhenBestFound(self):
        return self._whenBestFound

    def displaySetting(self):
        Optimizer.displaySetting(self)
        print("Number of evaluations until termination: {0:,}".format(self._limitEval))

    def run(self):
        pass

class Simulated(MetaHeuristics):
    """ Simulated annealing calls the following methods.
        initTemp returns an initial temperature such that the probability of
        accepting a worse neighbor is 0.5, i.e., exp(–dE/t) = 0.5.
        tSchedule returns the next temperature according to an annealing schedule."""

    def __init__(self):
        MetaHeuristics.__init__(self)
        self._numSample = 100   # Number of samples used to determine
                                # initial temperature

    def displaySetting(self):
        print()
        print("Search Algorithm: Simulated Annealing")
        print()
        MetaHeuristics.displaySetting(self)

    def run(self, p):
        current = p.randomInit()
        valueC = p.evaluate(current)
        best, valueBest = current, valueC
        whenBestFound = i = 1   # To remember when best was found
        t = self.initTemp(p)    # An initial temperature is chosen
        while True:
            t = self.tSchedule(t)   # Follow annealing schedule
            if t == 0 or i == self._limitEval:
                break
            neighbor = p.randomMutant(current)
            valueN = p.evaluate(neighbor)
            i += 1
            dE = valueN - valueC
            if dE < 0:
                valueC, current = valueN, neighbor
            elif random.uniform(0, 1) < math.exp(-dE/t):
                valueC, current = valueN, neighbor
            if valueC < valueBest:   # A new best solution found
                (best, valueBest) = (current, valueC)
                whenBestFound = i    # Record when best was found
        self._whenBestFound = whenBestFound
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
        t = dE / math.log(2)        # exp(–dE/t) = 0.5 이 식을 t에 대해서 풀면 공식이 나온다.
        return t

    def tSchedule(self, t):
        return t * (1 - (1 / 10**4))   # 보통 이렇게 사용한다. 문제마다 달라질 수 있음.


class GA(MetaHeuristics):
    def __init__(self):
        MetaHeuristics.__init__(self)
        self._popSize = 0     # Population size
        self._uXp = 0   # Probability of swappping a locus for Xover
        self._mrF = 0   # Multiplication factor to 1/n for bit-flip mutation
        self._XR = 0    # Crossover rate for permutation code
        self._mR = 0    # Mutation rate for permutation code
        self._pC = 0    # Probability parameter for Xover
        self._pM = 0    # Probability parameter for mutation

    def setVariables(self, parameters):
        MetaHeuristics.setVariables(self, parameters)
        self._popSize = parameters['popSize']
        self._uXp = parameters['uXp']
        self._mrF = parameters['mrF']
        self._XR = parameters['XR']
        self._mR = parameters['mR']
        if self._pType == 1:
            self._pC = self._uXp
            self._pM = self._mrF
        if self._pType == 2:
            self._pC = self._XR
            self._pM = self._mR

    def displaySetting(self):
        print()
        print("Search Algorithm: Genetic Algorithm")
        print()
        MetaHeuristics.displaySetting(self)
        print()
        print("Population size:", self._popSize)
        if self._pType == 1:   # Numerical optimization
            print("Number of bits for binary encoding:", self._resolution)
            print("Swap probability for uniform crossover:", self._uXp)
            print("Multiplication factor to 1/L for bit-flip mutation:",
                  self._mrF)
        elif self._pType == 2: # TSP
            print("Crossover rate:", self._XR)
            print("Mutation rate:", self._mR)

    def run(self, p):
        p.setNumEval()
        numEval = p.getNumEval()
        pop = p.initializePop(self._popSize)
        best = self.findBest(pop, p)
        while numEval < self._limitEval:
            newPop = []
            i = 0
            while i < self._popSize:
                par1, par2 = self.getGoodParent(pop)
                ch1, ch2 = p.crossover(par1, par2, self._pC)
                ch1_ = p.mutation(ch1, self._pM)
                ch2_ = p.mutation(ch2, self._pM)
                newPop.extend([ch1_, ch2_])
                i += 2
            pop = newPop
            bestNew = self.findBest(pop, p)
            numEval = p.getNumEval()
            if bestNew[0] < best[0]:
                best = bestNew
                whenBestFound = numEval
        bestSolution = p.indToSol(best)
        self._whenBestFound = whenBestFound
        p.storeResult(bestSolution, best[0])   # best 자체가 fitness function과 solution으로 이뤄져 있기에 그러하다.

    def findBest(self, pop, p):
        best = pop[0]
        p.evalInd(best)
        best_value = best[0]
        for i in range(1, len(pop)):
            p.evalInd(pop[i])
            new_value = pop[i][0]
            if new_value < best_value:
                best = pop[i]
                best_value = new_value
        return best

    def getGoodParent(self, pop):
        ind1, ind2 = self.selectTwo(pop)
        par1 = self.tournament(ind1, ind2)
        ind1, ind2 = self.selectTwo(pop)
        par2 = self.tournament(ind1, ind2)
        return par1, par2

    def tournament(self, ind1, ind2):
        if ind1[0] < ind2[0]:
            return ind1
        else:
            return ind2

    def selectTwo(self, pop):
        pop_ = pop[:]
        random.shuffle(pop_)
        return pop_[0], pop_[1]