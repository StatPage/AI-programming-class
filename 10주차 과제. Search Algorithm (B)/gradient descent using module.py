from Problem import Numeric


UPDATE_RATE = 0.01
DELTA_X = 0.0001
TOLERANCE = 0.000001

def main():
    p = Numeric()
    p.createProblem()
    gradientDescent(p)
    p.describeProblem()
    displaySetting()
    p.displayResult()


# 다변량일때의 gradient는 편미분을해서 구한다. 다시 말해서 그냥 미분값을 비율로 구해준 내용인 것이다.
def partial_difference_quotient(p, x, i):  # 여기서도 역시 'h'만큼 움직였을때의 변화율로써 근사를 한다. 여기서 h는 1e-9와같이 매우 작은 수가 들어간다.
    f1 = p.evaluate(x)
    w = [x_j + (DELTA_X if j == i else 0) for j, x_j in enumerate(x)]  # h가 변화율인데 이것은 내가 임의로 줘야 한다. 엄청 작게. 예를 들면 h는 1e-9
    x = w[:]
    f2 = p.evaluate(x)
    return (f2 - f1) / DELTA_X  # 미분할 때 배운 식


# 편미분 값들을 리스트 형태로 출력해주는 함수.
def estimate_gradient(p, x):
    return [partial_difference_quotient(p, x, i) for i, _ in enumerate(x)]  # 여러 변수의 각각의 미분값이 나오는 리스트 반환


# 얼마만큼의 변화를 줄 것인가.
def step(x, gradient):
    return [x_i + -UPDATE_RATE * gradient_i  # 왠만하면 step_size는 -0.01이 될 것이고 direction은 estimate_gradient일 것이다.
        for x_i, gradient_i in zip(x, gradient)]


def gradientDescent(p):  # target_fn은 원래 함수. gradient_fn은 미분으로 구하는 함수. theta_0는 넣고 싶은 값. tolerance는 근사값 수치
    current = p.randomInit()
    valueC = p.evaluate(current)
    while True:
        gradient = estimate_gradient(p, current)
        successor = step(current, gradient)
        valueS = p.evaluate(successor)
        if valueC - valueS < TOLERANCE:
            p.setSolution(current)
            p.setCost(valueC)
            break
        current, valueC = successor, valueS


def displaySetting():
    print()
    print("Search algorithm: Gradient-Descent")
    print()
    print("Update rate:", UPDATE_RATE)


main()