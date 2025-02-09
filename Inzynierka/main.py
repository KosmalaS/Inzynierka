import argparse

import sympy

import equation
import solvers
import warnings

# Ignore FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)


def main():
    parser = argparse.ArgumentParser(description='Recognizing and solving an equation from an image.')
    parser.add_argument('-s', '--source', required=True, help='Path to image')
    parser.add_argument('-ic', '--initial_condition', nargs=2, type=float, metavar=('x0', 'a'),
                        help='Initial condition for DE f(x0)=a')
    args = parser.parse_args()

    print(f'Source: {args.source}','\n')

    expression, type = equation.get_symbolic_expression(args.source)
    print(expression,'\n')
    print(type, '\n')
    if type == 'polynomial':
        result = solvers.solve_poly(expression)
    elif type == 'integral':
        lower_bound, upper_bound = equation.get_integral_bounds(equation.get_latex(args.source))
        result = solvers.solve_integral(expression, lower_bound, upper_bound)
    elif type == 'derivative':
        latex_expr = equation.get_latex(args.source)
        derivative_expr = equation.get_derivative_expr(latex_expr)
        derivative_expr_sym = equation.latex_to_sym(derivative_expr)
        result = solvers.solve_derivative(derivative_expr_sym)
    elif type == 'limit':
        latex_expr = equation.get_latex(args.source)
        limit_point = equation.get_limit_point(latex_expr)
        result = solvers.solve_limit(expression, limit_point)
    elif type == 'de':
        if not args.initial_condition:
            raise ValueError("Initial condition is required. Use -ic x0 a.")
        x0, a = args.initial_condition
        latex_expr = equation.get_latex(args.source)
        expression = equation.get_differential_expr(latex_expr)
        result = solvers.solve_differential_eq(expression, x0, a)
    else:
        result = 'unknown type'

    print(result)



if __name__ == "__main__":
    main()