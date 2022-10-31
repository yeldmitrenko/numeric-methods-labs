import copy
from sympy import *

x1, x2 = symbols('x1 x2')
F1 = x1 ** 2 + 0.8 * x2 ** 2 + 0.1 - x1
F2 = 2 * x1 * x2 - 0.1 - x2


def f1(args):
    x1_val, x2_val = args
    return x1_val ** 2 + 0.8 * x2_val ** 2 + 0.1 - x1_val


def f2(args):
    x1_val, x2_val = args
    return 2 * x1_val * x2_val - 0.1 - x2_val


def calculate_vec_f(x_vals):
    return [f1(x_vals), f2(x_vals)]


if __name__ == '__main__':
    e_value = 0.00001
    n = 2

    x = [0]*n
    x_old = [0]*n
    J = [[0 for i in range(n)] for j in range(n)]
    E = [[0 for i in range(n)] for k in range(n)]
    for k in range(0, n):
        for j in range(0, n):
            if k == j:
                E[k][j] = 1
            else:
                E[k][j] = 0

    INVERSE = []

    condition = False
    while not condition:
        vector = calculate_vec_f(x)

        J[0][0] = eval(str(diff(F1, x1)), {"x1": x_old[0], "x2": x_old[1]})
        J[0][1] = eval(str(diff(F1, x2)),
                       {"x1": x_old[0], "x2": x_old[1]})
        J[1][0] = eval(str(diff(F2, x1)),
                       {"x1": x_old[0], "x2": x_old[1]})
        J[1][1] = eval(str(diff(F2, x2)),
                       {"x1": x_old[0], "x2": x_old[1]})

        for b in range(n - 1):
            v = copy.deepcopy(J)
            c = [[0 for i in range(n)] for j in range(n)]

            for k in range(n):
                max_val = v[k][k]
                h = k
                w = k
                for l in range(k + 1, n):
                    for f in range(k, n):
                        if abs(max_val) < abs(v[l][f]):
                            max_val = abs(v[l][f])
                            h = l
                            w = f

                for d in range(n):
                    v[k][d], v[h][d] = v[h][d], v[k][d]

                for d in range(n):
                    if d < k:
                        c[d][k], c[d][w] = c[d][w], c[d][k]
                    else:
                        v[d][k], v[d][w] = v[d][w], v[d][k]

                for i in range(k + 1, n):
                    multi_var = -v[i][k] / v[k][k]
                    for j in range(k, n):
                        if k == j:
                            v[i][j] = 0
                        else:
                            v[i][j] += multi_var * v[k][j]

                X = copy.deepcopy(v)
        for i in range(n):
            INVERSE.append(X[i])

        for i in range(n):
            s = 0
            for j in range(n):
                s += INVERSE[i][j] * vector[j]
            x[i] = (x_old[i] - s)

        for i in range(n):
            if abs((x[i] - x_old[i]) / x[i]) * 100 < e_value:
                if i == n - 1:
                    condition = True
            else:
                break

        for i in range(n):
            x_old[i] = x[i]

    print("Result:", x_old)
    print("Test equation №1:", x_old[0] ** 2 + 0.8 * x_old[1] ** 2 + 0.1 - x_old[0])
    print("Test equation №2:", 2 * x_old[0] * x_old[1] - 0.1 - x_old[1])
