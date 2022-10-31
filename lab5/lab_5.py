import math
import numpy as np
from matplotlib import pyplot as plt


def u1(t_val, u_max_val, f_val):
    return u_max_val * math.sin(2 * math.pi * f_val * t_val)


if __name__ == '__main__':
    u_max = 100
    f = 50
    r1 = 5
    r2 = 4
    r3 = 7
    c1 = 300 * pow(10,  -6)
    c2 = 150 * pow(10, -6)

    h = 0.00001
    t = 0

    Uc1_old = 0
    Uc2_old = 0
    i3_old = 0

    Uc1 = 0
    Uc2 = 0
    i3 = 0

    x_values = []
    y_values = []

    while t <= 0.2:
        Uc1 = Uc1_old + h * ((u1(t, u_max, f) - Uc1_old + i3_old * r2) / (c1 * (r1 + r2)))
        Uc2 = Uc2_old + h * (i3_old / c2)
        i3 = i3_old + h * ((((u1(t, u_max, f) - Uc1 + i3 * r2) / (r1 + r2) * r2) - Uc2) / (r2 + r3))

        u2 = (((u1(t, u_max, f) - Uc1 + i3 * r2) / (r1 + r2)) * r2 - i3 * (r2 - r3))
        x_values.append(t)
        y_values.append(u2)

        Uc1_old = Uc1
        Uc2_old = Uc2
        i3_old = i3
        t += h

    # Graph
    vals_x = np.array(x_values)
    vals_y = np.array(y_values)
    plt.title("Graph of output voltage U2", fontdict={'family': 'serif', 'color': 'darkred', 'size': 18})
    plt.xlabel("t, s")
    plt.ylabel("U, В")
    plt.axhline(y=0, color="grey")
    plt.scatter(vals_x, vals_y, s=0.1)
    plt.show()
