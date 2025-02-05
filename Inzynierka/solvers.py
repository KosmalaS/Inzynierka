import sympy as sp
from sympy import E

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
    Y = sp.Function('y')

    expression = sp.sympify(expression, {"x": x, "y": Y, "diff": sp.diff})

    de = sp.Eq(expression.subs(Y, Y(x)), 0)

    solution = sp.dsolve(de, Y(x))
    eq_ic = sp.Eq(solution.rhs.subs(x, x0), a)

    constants = sp.solve(eq_ic, dict=True)
    solution = solution.subs(constants[0])
    return solution

