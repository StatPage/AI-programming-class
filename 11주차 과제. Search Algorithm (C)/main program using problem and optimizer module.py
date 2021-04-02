import Problem
import optimizer

def main():
    p, opt = SelectProblemAndSearchAlgorithm()
    # Create an instance of numerical optimization problem
    # Call the search algorithm
    opt.run(p)
    # Show the problem and algorithm settings
    p.describeProblem()
    opt.displaySetting()
    # Report results
    p.displayResult()

def SelectProblemAndSearchAlgorithm():
    print("Select the problem type:")
    print("  1. Numerical Optimization")
    print("  2. TSP")
    type1 = int(input("Enter the number: "))
    if type1 == 1:
        p = Problem.Numeric()
    else:
        p = Problem.Tsp()
    p.createProblem()

    print("Select the search algorithm:")
    print("  1. Steepest-Ascent")
    print("  2. First-Choice")
    print("  3. Gradient Descent")
    type2 = int(input("Enter the number: "))
    if type1 == 1:
        if type2 == 1:
            o = optimizer.steepestAscentNumeric(algorithm="Steepest-Ascent")
        elif type2 == 2:
            o = optimizer.firstChoiceNumeric(algorithm="First-Choice")
        else:
            o = optimizer.gradient(algorithm="Gradient Descent")
    else :
        if type2 == 1:
            o = optimizer.steepestAscentTsp(algorithm="Steepest-Ascent")
        else:
            o = optimizer.firstChoiceTsp(algorithm="First-Choice")

    return p, o


main()