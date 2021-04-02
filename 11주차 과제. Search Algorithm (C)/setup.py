import random
import math

class SetUp:
    def __init__(self, DELTA=0.01, DELTA_X=0.0001, UPDATE_RATE=0.01):
        self._DELTA = DELTA
        self._DELTA_X = DELTA_X
        self._UPDATE_RATE = UPDATE_RATE

class HillClimbing(SetUp):
    def __init__(self, algorithm="", DELTA=0.01, LIMIT_STUCK=100, UPDATE_RATE = 0.01, DELTA_X = 0.0001, TOLERANCE = 0.000001):
        self._algorithm = algorithm
        self._DELTA = DELTA
        self._LIMIT_STUCK = LIMIT_STUCK
        self._UPDATE_RATE = UPDATE_RATE
        self._DELTA_X = DELTA_X
        self._TOLERANCE = TOLERANCE

    def run(self):
        pass

    def displaySetting(self):
        print()
        print("Search algorithm:", self._algorithm)
        print()
        print("Mutation step size:", self._DELTA)

class steepestAscentNumeric(HillClimbing):
    def run(self, p):
        current = p.randomInit()  # 'current' is a list of values
        valueC = p.evaluate(current)
        while True:
            neighbors = self.mutants(current, p)
            successor, valueS = self.bestOf(neighbors, p)
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS
        p.setSolution(current)
        p.setCost(valueC)

    def mutants(self, current, p):  ###
        neighbors = []
        for i in range(len(current)):
            d = self._DELTA
            neighbors.append(p.mutate(current, i, d))
            d = -1 * self._DELTA
            neighbors.append(p.mutate(current, i, d))
        return neighbors  # Return a set of successors

    def bestOf(self, neighbors, p):  ###
        best = neighbors[0]
        bestValue = p.evaluate(best)
        for x in neighbors:
            successorValue = p.evaluate(x)
            if successorValue < bestValue:
                bestValue = successorValue
                best = x
        return best, bestValue

class steepestAscentTsp(HillClimbing):
    def run(self, p):
        current = p.randomInit()  # 'current' is a list of city ids
        valueC = p.evaluate(current)
        print(current)
        while True:
            neighbors = self.mutants(current, p)
            (successor, valueS) = self.bestOf(neighbors, p)
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS
                p.setSolution(current)
                p.setCost(valueC)

    def mutants(self, current, p):  # Apply inversion
        n = len(current)
        neighbors = []
        count = 0
        triedPairs = []
        while count <= n:  # Pick two random loci for inversion
            i, j = sorted([random.randrange(n) for _ in range(2)])
            if i < j and [i, j] not in triedPairs:
                triedPairs.append([i, j])
                curCopy = p.inversion(current, i, j)
                count += 1
                neighbors.append(curCopy)
        return neighbors

    def bestOf(self, neighbors, p):  ###
        best = neighbors[0]
        bestValue = p.evaluate(best)
        for x in neighbors:
            successorValue = p.evaluate(x)
            if successorValue < bestValue:
                bestValue = successorValue
                best = x
        return best, bestValue


class firstChoiceNumeric(HillClimbing):
    def run(self, p):
        current = p.randomInit()  # 'current' is a list of values
        valueC = p.evaluate(current)
        i = 0
        while i < self._LIMIT_STUCK:
            successor = self.randomMutant(current, p)
            valueS = p.evaluate(successor)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0  # Reset stuck counter
            else:
                i += 1
        p.setSolution(current)
        p.setCost(valueC)

    def randomMutant(self, current, p):  ###
        i = random.randint(0, len(current) - 1)
        d = random.randint(-1, 1) * self._DELTA
        return p.mutate(current, i, d)  # Return a random successor


class firstChoiceTsp(HillClimbing):
    def run(self, p):
        current = p.randomInit()  # 'current' is a list of city ids
        valueC = p.evaluate(current)
        i = 0
        while i < self._LIMIT_STUCK:  # LIMIT_STUCK = 100
            successor = self.randomMutant(current, p)
            valueS = p.evaluate(successor)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0  # Reset stuck counter
            else:
                i += 1
        p.setSolution(current)
        p.setCost(valueC)

    def randomMutant(self, current, p):  # Apply inversion
        while True:
            i, j = sorted([random.randrange(len(current))  # random.randrange(p[0])는 0 이상 30 미만인 하나의 난수.
                           for _ in range(2)])
            if i < j:
                curCopy = p.inversion(current, i, j)
                break
        return curCopy

    def displaySetting(self):
        print()
        print("Search algorithm:", self._algorithm)


class gradient(HillClimbing):
    def partial_difference_quotient(self, p, x, i):  # 여기서도 역시 'h'만큼 움직였을때의 변화율로써 근사를 한다. 여기서 h는 1e-9와같이 매우 작은 수가 들어간다.
        f1 = p.evaluate(x)
        w = [x_j + (self._DELTA_X if j == i else 0) for j, x_j in
             enumerate(x)]  # h가 변화율인데 이것은 내가 임의로 줘야 한다. 엄청 작게. 예를 들면 h는 1e-9
        x = w[:]
        f2 = p.evaluate(x)
        return (f2 - f1) / self._DELTA_X  # 미분할 때 배운 식

    # 편미분 값들을 리스트 형태로 출력해주는 함수.
    def estimate_gradient(self, p, x):
        return [self.partial_difference_quotient(p, x, i) for i, _ in enumerate(x)]  # 여러 변수의 각각의 미분값이 나오는 리스트 반환

    # 얼마만큼의 변화를 줄 것인가.
    def step(self, x, gradient):
        return [x_i + -self._UPDATE_RATE * gradient_i
                # 왠만하면 step_size는 -0.01이 될 것이고 direction은 estimate_gradient일 것이다.
                for x_i, gradient_i in zip(x, gradient)]

    def run(self, p):  # target_fn은 원래 함수. gradient_fn은 미분으로 구하는 함수. theta_0는 넣고 싶은 값. tolerance는 근사값 수치
        current = p.randomInit()
        valueC = p.evaluate(current)
        while True:
            gradient = self.estimate_gradient(p, current)
            successor = self.step(current, gradient)
            valueS = p.evaluate(successor)
            if valueC - valueS < self._TOLERANCE:
                p.setSolution(current)
                p.setCost(valueC)
                break
            current, valueC = successor, valueS

    def displaySetting(self):
        print()
        print("Search algorithm:", self._algorithm)
        print()
        print("Update rate:", self._UPDATE_RATE)
        print("Increment for calculating derivatives:", self._DELTA_X)


class Problem(SetUp):
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