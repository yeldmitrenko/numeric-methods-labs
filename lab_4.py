from math import sqrt, asin


def f(x_val):
    return sqrt((1 + x_val) / (1 - x_val))


def F(x_value):
    return -(sqrt(1 - pow(x_value, 2))) + asin(x_value)


if __name__ == '__main__':
    integral = 0
    n = 30
    a = 0
    b = 0.5
    h = (b - a) / n
    x = a + h

    fa = f(a)
    fb = f(b)

    for i in range(n - 1):
        integral += f(x)
        x += h

    integral = h * ((fa + fb) / 2 + integral)

    print(integral)
    print("Test:", F(b) - F(a))
