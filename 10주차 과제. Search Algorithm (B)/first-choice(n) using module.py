from Problem import Numeric
import random

DELTA = 0.01   # Mutation step size
LIMIT_STUCK = 100 # Max number of evaluations enduring no improvement


def main():
    p = Numeric()
    # Create an instance of numerical optimization problem
    p.createProblem()   # 'p': (expr, domain)
    # Call the search algorithm
    firstChoice(p)
    # Show the problem and algorithm settings
    p.describeProblem()
    displaySetting()
    # Report results
    p.displayResult()


def firstChoice(p):
    current = p.randomInit()   # 'current' is a list of values
    valueC = p.evaluate(current)
    i = 0
    while i < LIMIT_STUCK:
        successor = randomMutant(current, p)
        valueS = p.evaluate(successor)
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0              # Reset stuck counter
        else:
            i += 1
    p.setSolution(current)
    p.setCost(valueC)


def randomMutant(current, p):   ###
    i = random.randint(0, len(current)-1)
    d = random.randint(-1, 1) * DELTA
    return p.mutate(current, i, d)   # Return a random successor


def displaySetting():
    print()
    print("Search algorithm: First-Choice Hill Climbing")
    print()
    print("Mutation step size:", DELTA)


main()