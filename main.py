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

    expression = equation.get_symbolic_expression(args.source)
    result = solvers.solve_poly(expression)
    print(result)



if __name__ == "__main__":
    main()