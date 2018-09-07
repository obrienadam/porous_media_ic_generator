import matplotlib.pyplot as plt

from shapes import *
from solver import *

if __name__ == '__main__':
    lx = 2
    ly = 1
    n = 20

    domain = Box(np.array([0, 0]), np.array([lx, ly]))
    r = np.random.normal(0.1, 0.02, n)
    x = np.random.rand(n) * lx
    y = np.random.rand(n) * ly

    cylinders = [Cylinder(r, np.array([x, y])) for r, x, y in zip(r, x, y)]

    #cylinders = [Cylinder(0.2, np.array([0, 0])), Cylinder(0.2, np.array([0.1, 0]))]

    solver = Solver(cylinders, domain)

    print(np.array([2, 3, 41, 2]) / np.array([4, 2, 11, 3]))

    fig, ax = plt.subplots()

    for c in cylinders:
        c = plt.Circle((c.x[0], c.x[1]), c.r, color='red')
        ax.add_artist(c)

    plt.show()

    r = solver.solve()

    vx = r[:, :n]
    vy = r[:, n:2 * n]
    x = r[:, 2 * n:3 * n]
    y = r[:, 3 * n:]

    print(np.max(x), np.max(y))
    print(np.min(x), np.min(y))

    fig, ax = plt.subplots()

    for c in cylinders:
        c = plt.Circle((c.x[0], c.x[1]), c.r, color='blue')
        ax.add_artist(c)

    plt.show()

    print(r.shape)
