import unittest
import numpy as np
from qiaopt.optimization import GAOpt, Optimizer
from qiaopt.pre import Experiment, SystemSetup, Parameter


class TestGAOpt(unittest.TestCase):

    def _paraboloid(self, var):
        """
        A simple paraboloid function. Has one global minimum:
        f(x1,x2)=0.0; (x1,x2)=(0.0, 0.0)
        :param var: List of x and y variables
        :return: Value of the function
        """
        x_loc = var[0]
        y_loc = var[1]
        return x_loc ** 2 + y_loc ** 2

    def _sixhump(self, var):
        """
        The six-hump camel back function. Has two global minimums:
        f(x1,x2)=-1.0316; (x1,x2)=(-0.0898,0.7126), (0.0898,-0.7126)
        :param var: List of x and y variables
        :return: Value of the function
        """
        x_loc = var[0]
        y_loc = var[1]
        return (4 - 2.1 * x_loc ** 2 + (x_loc ** 4) / 3.) * x_loc**2 + x_loc * y_loc + (-4 + 4 * y_loc ** 2) * y_loc**2

    def _rosenbrock(self, var):
        """
        The Rosenbrock function. Has one global minimum:
        f(x1,x2)=0.0; (x1,x2)=(1.0, 1.0)
        :param var: List of x and y variables
        :return: Value of the function
        """
        x_loc = var[0]
        y_loc = var[1]
        return (1 - x_loc)**2 + 100 * (y_loc - x_loc**2)**2

    def _rastrigin(self, var):
        """
        The Rastrigin function. Has one global minimum:
        f(x1,x2)=0.0; (x1,x2)=(0.0, 0.0)
        :param var: List of x and y variables
        :return: Value of the function
        """
        x_loc = var[0]
        y_loc = var[1]
        return (x_loc ** 2 - 10 * np.cos(2 * np.pi * x_loc)) + \
            (y_loc ** 2 - 10 * np.cos(2 * np.pi * y_loc)) + 20

    def _setup_and_execute(self, function, var_range=[1.2, 1.2], var_step=0.01):
        self.x = list(np.arange(-var_range[0], var_range[1], var_step))
        self.y = list(np.arange(-var_range[0], var_range[1], var_step))

        ga_opt = GAOpt(function, [self.x, self.y], 100)
        opt = Optimizer(ga_opt)

        return opt.optimize()

    def test_optimize_paraboloid(self):
        solution, func_values = self._setup_and_execute(self._paraboloid)
        x_true = 0.0
        y_true = 0.0

        self.assertTrue(np.abs(solution[0] - x_true) <= 1e-12)
        self.assertTrue(np.abs(solution[1] - y_true) <= 1e-12)

    def test_optimize_sixhump(self):
        solution, func_values = self._setup_and_execute(self._sixhump, var_range=[0.8, 0.8], var_step=0.01)
        x_true = -0.0898
        y_true = 0.7126

        # Check one of the possible solutions
        if solution[0] > 0:
            x_true *= -1
            y_true *= -1

        self.assertTrue(np.abs(solution[0] - x_true) <= 1e-2)
        self.assertTrue(np.abs(solution[1] - y_true) <= 1e-2)

    def test_optimize_rosenbrock(self):
        solution, func_values = self._setup_and_execute(self._rosenbrock)
        x_true = 1.0
        y_true = 1.0

        self.assertTrue(np.abs(solution[0] - x_true) <= 1e-12)
        self.assertTrue(np.abs(solution[1] - y_true) <= 1e-12)

    def test_optimize_rastrigin(self):
        solution, func_values = self._setup_and_execute(self._rastrigin)
        x_true = 0.0
        y_true = 0.0

        self.assertTrue(np.abs(solution[0] - x_true) <= 1e-12)
        self.assertTrue(np.abs(solution[1] - y_true) <= 1e-12)


if __name__ == '__main__':
    unittest.main()
