from Problem import Tsp
import random


def main():
    # Create an instance of TSP
    p = Tsp()  # 'p': (numCities, locations, table)
    p.createProblem()
    # Call the search algorithm
    steepestAscent(p)
    # Show the problem and algorithm settings
    p.describeProblem()
    displaySetting()
    # Report results
    p.displayResult()


def steepestAscent(p):
    current = p.randomInit()  # 'current' is a list of city ids
    valueC = p.evaluate(current)
    print(current)
    while True:
        neighbors = mutants(current, p)
        (successor, valueS) = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
            p.setSolution(current)
            p.setCost(valueC)


def mutants(current, p):  # Apply inversion
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


def bestOf(neighbors, p):  ###
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


main()