import argparse
import sympy
import equation
import solvers
import warnings
import preprocessing
import warnings
warnings.filterwarnings("ignore", category=UserWarning)



def main():
    parser = argparse.ArgumentParser(description='Recognizing and solving an equation from an image.')
    parser.add_argument('-s', '--source', required=True, help='Path to image')
    parser.add_argument('-ic', '--initial_condition', nargs=2, type=float, metavar=('x0', 'a'),
                        help='Initial condition for DE f(x0)=a')
    parser.add_argument('-xe', '--x_end', type=float, help='End value of x for numerical methods')
    parser.add_argument('-n', '--numerical', action='store_true', help='Use numerical method')

    args = parser.parse_args()

    print(f'Source: {args.source}', '\n')
    image = preprocessing.preprocess_image(args.source)

    expression, type = equation.get_symbolic_expression(image)
    print(expression, '\n')
    print(type, '\n')

    if type == 'polynomial':
        result = solvers.solve_poly(expression)
    elif type == 'integral':
        lower_bound, upper_bound = equation.get_integral_bounds(equation.get_latex(image))
        if args.numerical:
            result = solvers.solve_integral_monte_carlo(expression, float(lower_bound), float(upper_bound))
        else:
            result = solvers.solve_integral(expression, float(lower_bound), float(upper_bound))
    elif type == 'derivative':
        latex_expr = equation.get_latex(image)
        derivative_expr = equation.get_derivative_expr(latex_expr)
        derivative_expr_sym = equation.latex_to_sym(derivative_expr)
        result = solvers.solve_derivative(derivative_expr_sym)
    elif type == 'limit':
        latex_expr = equation.get_latex(image)
        limit_point = equation.get_limit_point(latex_expr)
        result = solvers.solve_limit(expression, limit_point)
    elif type == 'de':
        if not args.initial_condition:
            raise ValueError("Initial condition is required. Use -ic x0 a.")
        x0, a = args.initial_condition
        latex_expr = equation.get_latex(image)
        expression = equation.get_differential_expr(latex_expr)

        if args.numerical:
            if args.x_end is None:
                raise ValueError("For numerical method, provide -xe x_end.")
            result = solvers.solve_differential_eq_rk4(expression, x0, a, args.x_end)
        else:
            result = solvers.solve_differential_eq(expression, x0, a)
    else:
        result = 'unknown type'

    print(result)

if __name__ == "__main__":
    main()