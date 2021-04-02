import random
from Problem import Numeric, Tsp

class HillClimbing:
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

    def displaySetting(self):
        print()
        print("Search algorithm:", self._algorithm)


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
        