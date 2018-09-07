import numpy as np
import scipy.integrate as ode


class Solver:
    def __init__(self, cylinders, domain, damping=0.1, dt=1e-2, eps=1e-4, s=0.01):
        self.cylinders = cylinders
        self.domain = domain
        self.damping = damping
        self.dt = dt
        self.eps = eps
        self.s = s

        self.m = np.array([c.area() for c in self.cylinders])

    def compute_forces(self, vx, vy):
        fx, fy = np.zeros(len(self.cylinders)), np.zeros(len(self.cylinders))
        for i, cp in enumerate(self.cylinders):
            f = np.zeros(2)
            for cq in self.cylinders:
                if cq is cp:
                    continue

                zeta = np.linalg.norm(cp.x - cq.x) - (cp.r + cq.r)
                f += (cp.x - cq.x) / self.eps * max(0, -(zeta - self.s)) ** 2

            fx[i], fy[i] = f[0], f[1]

        return fx - self.damping * vx, fy - self.damping * vy

    def solve(self):
        def f(y, t):
            n = y.shape[0] // 4

            vx = y[:n]
            vy = y[n:2 * n]
            x = y[2 * n:3 * n]
            y = y[3 * n:]

            for vxc, yxc, xc, yc, c in zip(vx, vy, x, y, self.cylinders):
                c.x = np.array([xc, yc])

            fx, fy = self.compute_forces(vx, vy)

            print(fx, fy, vx, vy)

            return np.concatenate((fx / self.m, fy / self.m, vx, vy))

        vx = np.zeros(len(self.cylinders))
        vy = np.zeros(len(self.cylinders))
        x = np.array([c.x[0] for c in self.cylinders])
        y = np.array([c.x[1] for c in self.cylinders])

        return ode.odeint(f, np.concatenate((vx, vy, x, y)), np.arange(0, 10, self.dt))
