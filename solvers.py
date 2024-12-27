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

print(solve_derivative('x**2'))
