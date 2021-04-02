from Problem import Tsp
import random
import math


LIMIT_STUCK = 100  # Max number of evaluations enduring no improvement
NumEval = 0  # Total number of evaluations


def main():
    # Create an instance of TSP
    p = Tsp()
    p.createProblem()  # 'p': (numCities, locations, distanceTable)
    # Call the search algorithm
    firstChoice(p)
    # Show the problem and algorithm settings
    p.describeProblem()
    displaySetting()
    # Report results
    p.displayResult()



def firstChoice(p):
    current = p.randomInit()  # 'current' is a list of city ids
    valueC = p.evaluate(current)
    i = 0
    while i < LIMIT_STUCK:  # LIMIT_STUCK = 100
        successor = randomMutant(current, p)
        valueS = p.evaluate(successor)
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0  # Reset stuck counter
        else:
            i += 1
    p.setSolution(current)
    p.setCost(valueC)


def randomMutant(current, p):  # Apply inversion
    while True:
        i, j = sorted([random.randrange(len(current))  # random.randrange(p[0])는 0 이상 30 미만인 하나의 난수.
                       for _ in range(2)])
        if i < j:
            curCopy = p.inversion(current, i, j)
            break
    return curCopy


def displaySetting():
    print()
    print("Search algorithm: First-Choice Hill Climbing")


main()
