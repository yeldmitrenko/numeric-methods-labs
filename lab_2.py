from math import exp


def f(x_val):
    return exp(-x_val) - x_val


if __name__ == '__main__':
    e = 0.00001
    older_x = -2
    old_x = -0.5
    x = -1

    while True:
        older_x = old_x
        old_x = x

        fx_older = f(older_x)
        fx = f(x)

        x -= (fx / ((fx_older - fx) / (older_x - x)))

        if abs((x - old_x) / x) * 100 < e:
            break

    print("Result:", x)
    print("Test:", f(x))
