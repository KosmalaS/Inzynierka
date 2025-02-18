import sympy as sp
from sympy import E
import numpy as np

def move_rhs_to_lhs(expression):
    lhs, rhs = expression.split('=')
    expression = f"{lhs}-({rhs})"
    return expression
def get_degree(expression) :
    expression = move_rhs_to_lhs(expression)
    poly = sp.Poly(expression)
    return poly.degree()

def solve_poly(expression):

    if get_degree(expression) <= 4:
        expression=move_rhs_to_lhs(expression)
        return sp.roots(expression, symbols='x')
    else:
        expression = move_rhs_to_lhs(expression)
        return sp.nroots(expression)

def solve_integral(expression, lower_bound, upper_bound):
    return sp.integrate(expression, ('x', lower_bound, upper_bound))

def solve_derivative(expression):
    x = sp.symbols('x')
    expr_sym = sp.sympify(expression)
    return sp.diff(expr_sym, x)

def solve_limit(expression, point):
    x = sp.symbols('x')
    expr_sym = sp.sympify(expression)
    return sp.limit(expr_sym, x, sp.sympify(point))


def solve_differential_eq(expression, x0, a):
    x = sp.Symbol('x', real=True)
    y = sp.Function('y')

    expression = sp.sympify(expression, locals={"x": x, "y": y, "Derivative": sp.Derivative})

    de = sp.Eq(expression, 0)

    solution = sp.dsolve(de, y(x))

    eq_ic = sp.Eq(solution.rhs.subs(x, x0), a)
    constants = sp.solve(eq_ic, dict=True)
    if constants:
        solution = solution.subs(constants[0])

    return solution


def solve_differential_eq_rk4(expression, x0, y0, x_end, h=0.01):
    x, y = sp.symbols('x y')

    f_expr = sp.sympify(expression.replace("y(x)", "y"))
    f_expr_no_deriv = f_expr.subs(sp.Derivative(y, x), 0)
    f_expr_final = -f_expr_no_deriv

    f = sp.lambdify((x, y), f_expr_final, 'numpy')


    n = int((x_end - x0) / h)
    xs, ys = [x0], [y0]

    for _ in range(n):
        k1 = h * f(x0, y0)
        k2 = h * f(x0 + h / 2, y0 + k1 / 2)
        k3 = h * f(x0 + h / 2, y0 + k2 / 2)
        k4 = h * f(x0 + h, y0 + k3)

        y0 += (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x0 += h

        xs.append(x0)
        ys.append(y0)

    return list(zip(xs, ys))

def solve_integral_monte_carlo(expression, lower_bound, upper_bound, num_samples=1000000):
    x = sp.symbols('x')
    expr_sym = sp.sympify(expression)
    f = sp.lambdify(x, expr_sym, 'numpy')

    x_vals = np.linspace(lower_bound, upper_bound, 1000)
    y_max = np.max(f(x_vals))

    x_samples = np.random.uniform(lower_bound, upper_bound, num_samples)
    y_samples = np.random.uniform(0, y_max, num_samples)

    under_curve = y_samples <= f(x_samples)
    points_under_curve = np.sum(under_curve)

    rectangle_area = (upper_bound - lower_bound) * y_max

    integral_value = (points_under_curve / num_samples) * rectangle_area

    return integral_value