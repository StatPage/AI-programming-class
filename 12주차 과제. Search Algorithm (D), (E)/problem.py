import random
import math
from setup import Setup
# import numpy as np

class Problem(Setup):
    def __init__(self):
        Setup.__init__(self)
        self._solution = []
        self._value = 0
        self._numEval = 0

    def setAType(self, aType):
        self._aType = aType

    def setVariables(self):
        pass

    def setNumEval(self):
        self._numEval = 0

    def randomInit(self):
        pass

    def evaluate(self):
        pass

    def mutants(self):
        pass

    def randomMutant(self, current):
        pass

    def describe(self):
        pass

    def storeResult(self, solution, value):
        self._solution = solution
        self._value = value

    def getSolution(self):
        return self._solution

    def getValue(self):
        return self._value

    def getNumEval(self):
        return self._numEval

    def report(self):
        print()
        print('Total Number of evaluations: {0:,}'.format(self._sumOfNumEval))

    def storeExpResult(self, results):
        self._bestSolution = results[0]
        self._bestMinimum = results[1]
        self._avgMinimum = results[2]
        self._avgNumEval = results[3]
        self._sumOfNumEval = results[4]
        self._avgWhen = results[5]


class Numeric(Problem):
    def __init__(self):
        # 자신의 상위 클래스에 있는 init을 먼저 실행 → 두 개의 init을 모두 사용할 때
        Problem.__init__(self)
        self._expression = ''
        self._domain = []


    def setVariables(self, fileName):
        infile = open(fileName, 'r')
        self._expression = infile.readline()
        varNames = []
        low = []
        up = []
        line = infile.readline()
        while line != '':
            data = line.split(',')
            varNames.append(data[0])
            low.append(int(data[1]))
            up.append(int(data[2]))
            line = infile.readline()
        infile.close()
        self._domain = [varNames, low, up]

    def getDomain(self):
        return self._domain

    def getExpression(self):
        return self._expression

    def setDomain(self, domain):
        self._domain = domain

    def setExpression(self, expression):
        self._expression = expression

    def randomInit(self):
        domain = self._domain
        low, up = domain[1], domain[2]
        init = []
        for i in range(len(low)):
            r = random.uniform(low[i], up[i])
            init.append(r)
        return init

    def evaluate(self, current):
        self._numEval += 1
        expr = self._expression
        varNames = self._domain[0]
        for i in range(len(varNames)):
            assignment = varNames[i] + '=' + str(current[i])
            exec(assignment)
        return eval(expr)

    def bestOf(self, neighbors):
        best = neighbors[0]
        bestValue = self.evaluate(best)
        for i in range(1, len(neighbors)):
            newValue = self.evaluate(neighbors[i])
            if newValue < bestValue:
                best = neighbors[i]
                bestValue = newValue
        return best, bestValue

    def mutants(self, current):
        neighbors = []
        for i in range(len(current)):
            mutant = self.mutate(current, i, self._delta)
            neighbors.append(mutant)
            mutant = self.mutate(current, i, - self._delta)
            neighbors.append(mutant)
        return neighbors

    def mutate(self, current, i, d):
        mutant = current[:]
        domain = self._domain
        l = domain[1][i]
        u = domain[2][i]
        if l <= (mutant[i] + d) <= u:
            mutant[i] += d
        return mutant

    def randomMutant(self, current):
        i = random.randint(0, len(current)-1)
        if random.uniform(0, 1) > 0.5:
            d = self._delta
        else:
            d = -self._delta
        return self.mutate(current, i, d)

    def takeStep(self, x, v):
        grad = self.gradient(x, v)
        xCopy = x[:]
        for i in range(len(xCopy)):
            xCopy[i] = xCopy[i] - self._alpha * grad[i]
        if self.isLegal(xCopy):
            return xCopy
        else:
            return x

    def gradient(self, x, v):
        grad = []
        for i in range(len(x)):
            xCopyH = x[:]
            xCopyH[i] += self._dx
            g = (self.evaluate(xCopyH) - v) / self._dx
            grad.append(g)
        return grad

    def isLegal(self, x):
        domain = self._domain
        low = domain[1]
        up = domain[2]
        flag = True
        for i in range(len(low)):
            if x[i] < low[i] or up[i] < x[i]:
                flag = False
                break
        return flag

    def describe(self):
        print()
        print('Objective function: ')
        print(self._expression)
        print('Search space: ')
        varNames = self._domain[0]
        low = self._domain[1]
        up = self._domain[2]
        for i in range(len(low)):
            print(' ' + varNames[i] + ':', (low[i], up[i]))

    def report(self):
        print()
        print('Average objective value: {0:}'.format(round(self._avgMinimum,3)))
        if 1 <= self._aType <= 4:
            print('Average number of evaluations: {0:,}'.format(self._avgNumEval))
        else:
            print('Average number of evaluations: {0:,}'.format(self._avgWhen))
        print()
        print('Best Solution found:')
        print(self.coordinate())
        print('Best value : {0:,.3f}'.format(self._bestMinimum))
        Problem.report(self)

    def coordinate(self):
        c = [round(value, 3) for value in self._bestSolution]
        return tuple(c)


class Tsp(Problem):
    def __init__(self):
        Problem.__init__(self)
        self._numCities = 0
        self._locations = []
        self._distanceTable = []
        self._objectiveValue = []

    def setVariables(self, fileName):
        infile = open(fileName, 'r')
        self._numCities = int(infile.readline())
        cityLocs = []
        line = infile.readline()
        while line != '':
            cityLocs.append(eval(line))
            line = infile.readline()
        infile.close()
        self._locations = cityLocs
        self._distanceTable = self.calcDistanceTable()

    def getObjectieveValue(self):
        return self._objectiveValue

    def getNumCities(self):
        return self._numCities

    def getLocations(self):
        return self._locations

    def getDistanceTable(self):
        return self._distanceTable

    def setNumCities(self, numCities):
        self._numCities = numCities

    def setLocations(self, locations):
        self._locations = locations

    def setDistanceTable(self, distanceTable):
        self._distanceTable = distanceTable

    def calcDistanceTable(self):
        locations = self._locations
        table = []
        for i in range(self._numCities):
            row = []
            for j in range(self._numCities):
                dx = locations[i][0] - locations[j][0]
                dy = locations[i][1] - locations[j][1]
                d = round(math.sqrt(dx**2 + dy**2), 1)
                row.append(d)
            table.append(row)
        return table

    def randomInit(self):
        n = self._numCities
        init = list(range(n))
        random.shuffle(init)
        return init

    def evaluate(self, current):
        self._numEval += 1
        n = self._numCities
        table = self._distanceTable
        cost = 0
        for i in range(n - 1):
            locFrom = current[i]
            locTo = current[i+1]
            cost += table[locFrom][locTo]
        self._objectiveValue.append(cost)
        return cost

    def bestOf(self, neighbors):  ###
        best = neighbors[0]
        bestValue = self.evaluate(best)
        for i in range(1, len(neighbors)):
            newValue = self.evaluate(neighbors[i])
            if newValue < bestValue:
                best = neighbors[i]
                bestValue = newValue
        return best, bestValue

    def mutants(self, current):
        n = self._numCities
        neighbors = []
        count = 0
        triedPairs = []
        while count <= n:
            i, j = sorted([random.randrange(n) for _ in range(2)])
            if i < j and [i, j] not in triedPairs:
                triedPairs.append([i, j])
                mutant = self.inversion(current, i, j)
                count += 1
                neighbors.append(mutant)
        return neighbors

    def inversion(self, current, i, j):
        mutant = current[:]
        while i < j:
            mutant[i], mutant[j] = mutant[j], mutant[i]
            i += 1
            j -= 1
        return mutant

    def randomMutant(self, current):
        while True:
            i, j = sorted([random.randrange(self._numCities) for _ in range(2)])
            if i < j:
                mutant = self.inversion(current, i, j)
                break
        return mutant

    def describe(self):
        print()
        n = self._numCities
        print('Number of cities:',n)
        print('City locations:')
        locations = self._locations
        for i in range(n):
            print('{0:>12}'.format(str(locations[i])), end = '')
            if i % 5 == 4:
                print()

    def report(self):
        print()
        print('Average objective value: {0:}'.format(round(self._avgMinimum, 3)))
        if 1 <= self._aType <= 4:
            print('Average number of evaluations: {0:,}'.format(self._avgNumEval))
        else:
            print('Average number of evaluations: {0:,}'.format(self._avgWhen))
        print()
        print('Best Solution found:')
        self.tenPerRow()  # Print 10 cities per row
        print('Best value : {0:,.3f}'.format(self._bestMinimum))
        Problem.report(self)

    def tenPerRow(self):
        for i in range(len(self._solution)):
            print("{0:>5}".format(self._solution[i]), end='')
            if i % 10 == 9:
                print()
