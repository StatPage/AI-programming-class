import random
import math

class Problem:
    def __init__(self, solution=None, NumEval=0, cost=0):
        self._solution = solution
        self._NumEval = NumEval
        self._cost = cost

class Numeric(Problem):
    def setSolution(self, solution):
        self._solution = solution

    def setCost(self, cost):
        self._cost = cost

    def createProblem(self):
        fileName = input("Enter the file name of a function: ")
        infile = open(fileName, 'r')
        content = [line.rstrip() for line in infile]
        infile.close()
        expression = content[0]
        varNames = []
        low = []
        up = []
        for line in content[1:]:
            line = line.split(',')
            varNames.append(line[0])
            low.append(int(line[1]))
            up.append(int(line[2]))
        domain = [varNames, low, up]
        self._expression, self._domain = expression, domain

    def randomInit(self):  ###
        up = int(self._domain[2][0])   # Variables'domains are same
        low = int(self._domain[1][0])
        init = []
        for i in range(5):
            sample = round(random.uniform(low, up), 3)
            init.append(sample)
        return init

    def evaluate(self, current):
        ## Evaluate the expression of 'p' after assigning
        ## the values of 'current' to the variables
        self._NumEval += 1
        expr = self._expression  # p[0] is function expression
        varNames = self._domain[0]  # p[1] is domain, p[1][0] is variables' names
        for i in range(len(varNames)):
            assignment = varNames[i] + '=' + str(current[i])
            exec(assignment)
        return eval(expr)

    def mutate(self, current, i, d):  ## Mutate i-th of 'current' if legal
        curCopy = current[:]
        domain = self._domain  # [VarNames, low, up]
        l = self._domain[1][i]  # Lower bound of i-th
        u = self._domain[2][i]  # Upper bound of i-th
        if l <= (curCopy[i] + d) <= u:
            curCopy[i] += d
        return curCopy

    def describeProblem(self):
        print()
        print("Objective function:")
        print(self._expression)  # Expression
        print("Search space:")
        varNames = self._domain[0]  # p[1] is domain: [VarNames, low, up]
        low = self._domain[1]
        up = self._domain[2]
        for i in range(len(low)):
            print(" " + varNames[i] + ":", (low[i], up[i]))

    def displayResult(self):
        print()
        print("Solution found:")
        print(self.coordinate())  # Convert list to tuple
        print("Minimum value: {0:,.3f}".format(self._cost))
        print()
        print("Total number of evaluations: {0:,}".format(self._NumEval))

    def coordinate(self):
        c = [round(value, 3) for value in self._solution]
        return tuple(c)  # Convert the list to a tuple


class Tsp(Problem):
    def setSolution(self, solution):
        self._solution = solution

    def setCost(self, cost):
        self._cost = cost

    def createProblem(self):
        ## Read in a TSP (# of cities, locatioins) from a file.
        ## Then, create a problem instance and return it.
        fileName = input("Enter the file name of a TSP: ")
        infile = open(fileName, 'r')
        # First line is number of cities
        numCities = int(infile.readline())
        locations = []
        line = infile.readline()  # The rest of the lines are locations
        while line != '':
            locations.append(eval(line))  # Make a tuple and append
            line = infile.readline()
        infile.close()
        table = self.calcDistanceTable(numCities, locations)
        self._numCities, self._locations, self._table = numCities, locations, table


    def calcDistanceTable(self,numCities, locations):  ###
        table = []
        for i in range(numCities):
            i_th_distanceLow = []
            for j in range(numCities):
                start = locations[i]
                end = locations[j]
                distance = math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)
                i_th_distanceLow.append(distance)
            table.append(i_th_distanceLow)
        return table  # A symmetric matrix of pairwise distances


    def randomInit(self):  # Return a random initial tour
        n = self._numCities
        init = list(range(n))
        random.shuffle(init)
        return init

    def evaluate(self, current):  ###
        ## Calculate the tour cost of 'current'
        ## 'p' is a Problem instance
        ## 'current' is a list of city ids
        self._NumEval += 1
        cost = 0
        for i in range(self._numCities - 1):
            index1, index2 = current[i], current[i + 1]
            cost += self._table[index1][index2]
        return cost


    def inversion(self, current, i, j):  ## Perform inversion
        curCopy = current[:]
        while i < j:
            curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
            i += 1
            j -= 1
        return curCopy

    def describeProblem(self):
        print()
        n = self._numCities
        print("Number of cities:", n)
        print("City locations:")
        locations = self._locations
        for i in range(n):
            print("{0:>12}".format(str(locations[i])), end='')
            if i % 5 == 4:
                print()

    def displayResult(self):
        print()
        print("Best order of visits:")
        self.tenPerRow()  # Print 10 cities per row
        print("Minimum tour cost: {0:,}".format(round(self._cost)))
        print()
        print("Total number of evaluations: {0:,}".format(self._NumEval))

    def tenPerRow(self):
        for i in range(len(self._solution)):
            print("{0:>5}".format(self._solution[i]), end='')
            if i % 10 == 9:
                print()










