import argparse
import equation
import solvers
import warnings

# Ignore FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)


def main():
    parser = argparse.ArgumentParser(description='Recognizing and solving an equation from an image.')
    parser.add_argument('-s', '--source', required=True, help='Path to image')
    args = parser.parse_args()

    print(f'Source: {args.source}')

    expression, type = equation.get_symbolic_expression(args.source)
    if type == 'polynomial':
        result = solvers.solve_poly(expression)
    elif type == 'integral':
        lower_bound, upper_bound = equation.get_integral_bounds(equation.get_latex(args.source))
        result = solvers.solve_integral(expression, lower_bound, upper_bound)
    else:
        result = 'unknown type'

    print(result)



if __name__ == "__main__":
    main()