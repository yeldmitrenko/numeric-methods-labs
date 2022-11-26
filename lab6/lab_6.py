import copy
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import pandas as pd

C1 = 0.5 * 10 ** -3
C2 = 0.7 * 10 ** -3
C3 = 0.3 * 10 ** -3
R1 = 70
R2 = 3
R3 = 7

Umax = 10
a = 0.02
T = 2 * a
dt = T / 400


def U1(t_val):
    if 0 <= t_val <= a:
        return Umax
    elif a < t_val <= 2 * a:
        return Umax / a * t_val - 20
    else:
        return U1(t_val - T)


def U2(Uc3_val):
    return Uc3_val


def draw(vals_x, vals_y, title, xlabel, ylabel):
    vals_x = np.array(vals_x)
    vals_y = np.array(vals_y)
    plt.title(title, fontdict={'family': 'serif', 'color': 'darkred', 'size': 18})
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.axhline(y=0, color="black")
    plt.axvline(x=0, color="black")
    plt.plot(vals_x, vals_y)
    plt.show()


def main():
    def diff_equations(args):
        return [
            Uc1_old + dt * (((U1(t) - args[0] + R3 * (((args[0] + args[1]) * (R1 + R3) + R3 * (args[0] - U1(t))) /
                                                      (R3 ** 2 - (R2 + R3) * (R1 + R3)))) / (C1 * (R1 + R3)))) - args[
                0],
            Uc2_old + dt * ((((args[1] + args[2]) * (R1 + R3)) - (U1(t) * R3) + (args[0] * R3)) /
                            (C2 * (R3 ** 2 - ((R2 + R3) * (R1 + R3))))) - args[1],
            Uc3_old + dt * ((((args[1] + args[2]) * (R1 + R3)) - (U1(t) * R3) + (args[0] * R3)) /
                            (C2 * (R3 ** 2 - ((R2 + R3) * (R1 + R3))))) - args[2]
        ]

    Uc1_old = 0
    Uc2_old = 0
    Uc3_old = 0

    vals_x = []
    uc1_vals_y = []
    uc2_vals_y = []
    uc3_vals_y = []
    u1_vals_y = []
    u2_vals_y = []
    t = 0
    while t <= 5 * T:
        Uc1, Uc2, Uc3 = fsolve(diff_equations, [1, 1, 1])
        vals_x.append(t)
        uc1_vals_y.append(Uc1)
        uc2_vals_y.append(Uc2)
        uc3_vals_y.append(Uc3)
        u1_vals_y.append(U1(t))
        u2_vals_y.append(U2(Uc3))
        Uc1_old = Uc1
        Uc2_old = Uc2
        Uc3_old = Uc3
        t += dt

    df = pd.DataFrame({
        "Час": vals_x,
        "Вхідна напруга U1": u1_vals_y,
        "Вихідна напруга U2": u2_vals_y,
        "Напруга на С1": uc1_vals_y,
        "Напруга на С2": uc2_vals_y,
        "Напруга на С3": uc3_vals_y
    })
    np.savetxt("result.txt", df, fmt="%f", header="    T       U1       U2       Uc1      Uc2      Uc3", comments="")

    draw(vals_x, u1_vals_y, "Графік вхідної напруги U1", "t, сек", "U, В")
    draw(vals_x, u2_vals_y, "Графік вихідної напруги U2", "t, сек", "U, В")
    draw(vals_x, uc1_vals_y, "Графік напруги на конденсаторі С1", "t, сек", "U, В")
    draw(vals_x, uc2_vals_y, "Графік напруги на конденсаторі С2", "t, сек", "U, В")
    draw(vals_x, uc3_vals_y, "Графік напруги на конденсаторі С3", "t, сек", "U, В")


def _fsolve(funcs, args):
    n = 2
    E = [[1 if i == j else 0 for i in range(n)] for j in range(n)]
    e = 0.00001
    x = [0 for i in range(n)]
    x_older = [0 for i in range(n)]
    x_old = [0.5 for i in range(n)]
    h = [0 for i in range(n)]
    f = [0 for i in range(n)]
    _x = [0 for i in range(n)]
    _f = [0 for i in range(n)]
    J = [[0 for i in range(n)] for j in range(n)]

    def calculate_vec_f(x_vals):
        return [f1(x_vals), f2(x_vals)]

    def f1(args):
        x1_val, x2_val = args
        return x1_val ** 2 + x2_val ** 2 + 0.1 - x1_val

    def f2(args):
        x1_val, x2_val = args
        return 2 * x1_val * x2_val + 0.1 - x2_val

    condition = False
    while not condition:

        for i in range(n):
            h[i] = x_older[i] - x_old[i]

        f = calculate_vec_f(x)

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    _x[k] = x[k]
                _x[j] = x[j] + h[j]

                _f = calculate_vec_f(_x)

                J[i][j] = (_f[i] - f[i]) / h[j]

        # Метод Гауса з вибором головних елементів по рядку
        result = []
        for b in range(n):
            inx = [i for i in range(n)]
            v = copy.deepcopy(J)
            p = copy.deepcopy(E[b])
            y = [0 for i in range(len(J))]
            c = [[0 for i in range(n)] for j in range(n)]

            # Прямий хід
            for k in range(n):

                # Рядкові сортування
                m = v[k][k]
                w = k
                for l in range(k + 1, n):
                    if m < v[k][l]:
                        m = v[k][l]
                        w = l
                        inx[k], inx[w] = inx[w], inx[k]
                        for d in range(n):
                            if d < k:
                                c[d][k], c[d][w] = c[d][w], c[d][k]
                            else:
                                v[d][k], v[d][w] = v[d][w], v[d][k]

                y[k] = p[k] / v[k][k]
                for i in range(k + 1, n):
                    p[i] -= v[i][k] * y[k]
                    for j in range(k + 1, n):
                        c[k][j] = v[k][j] / v[k][k]
                        v[i][j] -= v[i][k] * c[k][j]

                # Обернений хід
                X = copy.deepcopy(y)
                for i in range(n - 1, -1, -1):
                    s = 0
                    for j in range(i + 1, n):
                        s += c[i][j] * X[j]
                    X[i] = y[i] - s

                # Впорядкування
                for i in range(n):
                    if inx[i] != i:
                        z = inx[i]
                        value = X[i]
                        X[i] = X[z]
                        X[z] = value
                        inx[i] = inx[z]
                        inx[z] = z
            result.insert(0, X)

        INVERSE = np.array(result).transpose()

        # INVERSE = np.linalg.inv(J)

        # Обчислення наступного наближення використовуючи ітераційну формулу
        for i in range(n):
            s = 0
            for j in range(n):
                s += INVERSE[i][j] * f[j]
            x[i] = x_old[i] - s

        for i in range(n):
            if abs((x[i] - x_old[i]) / x[i]) * 100 < e:
                if i == n - 1:
                    condition = True
            else:
                break

        for i in range(n):
            x_older[i] = x_old[i]
            x_old[i] = x[i]


if __name__ == '__main__':
    main()
