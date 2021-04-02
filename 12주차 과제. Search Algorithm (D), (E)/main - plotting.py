from problem import *
from optimizer import *


def main():
    p, alg, name = readPlanAndCreate()  # Setup and create (problem, algorithm)
    conductExperiment(p, alg)     # Conduct experiment & produce results
    p.describe()                  # Describe the problem solved
    alg.displayNumExp()           # Total number of experiments
    alg.displaySetting()          # Show the algorithm settings
    p.report()
    createFile(name)

def readPlanAndCreate():
    parameters = readValidPlan()  # Read and store in 'parameters'
    p = createProblem(parameters)
    alg, name = createOptimizer(parameters)
    return p, alg, name

def readValidPlan():  # Gradient Descent cannot solve TSP
    while True:   # readPlan function만 사용하면 Gradient Descent가 TSP 문제에서 사용될 수 있는 오류가 생겨 경우의 수를 제거.
        parameters = readPlan()
        if parameters['pType'] == 2 and parameters['aType'] == 4:
            print("You cannot choose Gradient Descent")
            print("       unless your want a numerical optimization.")
        else:
            break
    return parameters

def readPlan():
    fileName = input("Enter the file name of experimental setting: ")
    infile = open(fileName, 'r')
    parameters = { 'pType':0, 'pFileName':'', 'aType':0, 'delta':0,   # exp 파일의 입력 값의 순서에 맞게 작성.
                   'limitStuck':0, 'alpha':0, 'dx':0, 'numRestart':0,
                   'limitEval':0, 'numExp':0 }
    parNames = list(parameters.keys())   # parNames는 parameters의 key값들로 이뤄진 리스트
    for i in range(len(parNames)):
        line = lineAfterComments(infile)
        if parNames[i] == 'pFileName':   # 나머지는 다 number지만 파일 이름이 string이기 때문에 구별
            parameters[parNames[i]] = line.rstrip().split(':')[-1][1:]
        else:
            parameters[parNames[i]] = eval(line.rstrip().split(':')[-1][1:])
    infile.close()
    return parameters             # Return a dictionary of parameters

def lineAfterComments(infile):    # Ignore lines beginning with '#'
    line = infile.readline()      # and then return the first line
    while line[0] == '#':         # with no '#'
        line = infile.readline()
    return line

def createProblem(parameters): ###
    # Create a problem instance (a class object) 'p' of the type as
    # specified by 'pType', set the class variables, and return 'p'.
    pType = parameters['pType']
    if pType == 1:      #
        p = Numeric()   # Create an empty problem instance
    elif pType == 2:    #
        p = Tsp()       #
    fileName = parameters["pFileName"]
    p.setVariables(fileName)
    return p

def createOptimizer(parameters): ###
    # Create an optimizer instance (a class object) 'alg' of the type
    # as specified by 'aType', set the class variables, and return 'alg'.
    pType = parameters["pType"]
    aType = parameters["aType"]
    delta = parameters["delta"]
    alpha = parameters["alpha"]
    dx = parameters["dx"]
    numExp = parameters["numExp"]
    optimizers = {1: "SteepestAscent()",
                  2: "FirstChoice()",
                  3: "Stochastic()",
                  4: "GradientDescent()",
                  5: "Simulated()"}
    name = optimizers[aType][0:-2]
    alg = eval(optimizers[aType])  # Create the target algorithm
    alg.setVariables(pType=pType, aType=aType, delta=delta, alpha=alpha, dx=dx, numExp=numExp)
    return alg, name

def conductExperiment(p, alg):
    aType = alg.getAType()
    p.setAType(aType)
    if 1 <= aType <= 4:
        alg.run(p)
    else:
        alg.run(p)
    bestSolution = p.getSolution()
    bestMinimum = p.getValue()    # First result is current best
    numEval = p.getNumEval()
    sumOfMinimum = bestMinimum    # Prepare for averaging
    sumOfNumEval = numEval        # Prepare for averaging
    sumOfWhen = 0                 # When the best solution is found
    if 5 <= aType <= 6:
        sumOfWhen = alg.getWhenBestFound()
    numExp = alg.getNumExp()
    # for i in range(1, numExp):
    #     if 1 <= aType <= 4:
    #         alg.randomRestart(p)
    #     else:
    #         alg.run(p)
    #     newSolution = p.getSolution()
    #     newMinimum = p.getValue()  # New result
    #     numEval = p.getNumEval()
    #     sumOfMinimum += newMinimum
    #     sumOfNumEval += numEval
    #     if 5 <= aType <= 6:
    #         sumOfWhen += alg.getWhenBestFound()
    #     if newMinimum < bestMinimum:
    #         bestSolution = newSolution  # Update the best-so-far
    #         bestMinimum = newMinimum
    avgMinimum = p.getValue()
    avgNumEval = round(sumOfNumEval)
    avgWhen = round(sumOfWhen / numExp)
    results = (bestSolution, bestMinimum, avgMinimum,
               avgNumEval, sumOfNumEval, avgWhen)
    p.storeExpResult(results)

def createFile(p, name):
    objectiveValue = p.getObjectiveValue()
    for i in range(len(objectiveValue)):
        objectiveValue[i] = str(objectiveValue[i]) + "\n"
    outfile = open(name + ".txt", 'w')
    outfile.writelines(objectiveValue)
    outfile.close()

main()