from Problem import Numeric

DELTA = 0.01   # Mutation step size

def main():
    p = Numeric()
    # Create an instance of numerical optimization problem
    p.createProblem()   # 'p': (expr, domain)
    # Call the search algorithm
    steepestAscent(p)
    # Show the problem and algorithm settings
    p.describeProblem()
    displaySetting()
    # Report results
    p.displayResult()


def steepestAscent(p):
    current = p.randomInit()   # 'current' is a list of values
    valueC = p.evaluate(current)
    while True:
        neighbors = mutants(current, p)
        successor, valueS = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    p.setSolution(current)
    p.setCost(valueC)


def mutants(current, p):   ###
    neighbors = []
    for i in range(len(current)):
        d = DELTA
        neighbors.append(p.mutate(current, i, d))
        d = -1 * DELTA
        neighbors.append(p.mutate(current, i, d))
    return neighbors     # Return a set of successors


def bestOf(neighbors, p): ###
    best = neighbors[0]
    bestValue = p.evaluate(best)
    for x in neighbors:
        successorValue = p.evaluate(x)
        if successorValue < bestValue:
            bestValue = successorValue
            best = x
    return best, bestValue


def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    print()
    print("Mutation step size:", DELTA)


main()