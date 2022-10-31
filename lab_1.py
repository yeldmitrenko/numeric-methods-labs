import copy
import numpy.linalg


if __name__ == '__main__':
    a = [
        [8.3, 2.78, 4.1, 1.9],
        [3.92, 8.45, 7.62, 2.46],
        [3.77, 7.37, 8.04, 2.28],
        [2.21, 3.5, 1.69, 6.69]
    ]
    v = copy.deepcopy(a)
    n = len(v)
    c = [[0 for i in range(n)] for j in range(n)]

    det = 1

    for k in range(n):
        max_val = v[k][k]
        h = k
        w = k
        for l in range(k, n):
            for f in range(k, n):
                if max_val < v[l][f]:
                    max_val = v[l][f]
                    h = l
                    w = f

        for d in range(n):
            v[k][d], v[h][d] = v[h][d], v[k][d]

        for d in range(n):
            if d < k:
                c[d][k], c[d][w] = c[d][w], c[d][k]
            else:
                v[d][k], v[d][w] = v[d][w], v[d][k]

        det *= pow((-1), (w + h)) * v[k][k]

        for i in range(k + 1, n):
            for j in range(k + 1, n):
                c[k][j] = v[k][j] / v[k][k]
                v[i][j] -= v[i][k] * c[k][j]

    print("Result:", det)
    print("Test:", numpy.linalg.det(a))
