import cv2
from pix2tex.cli import LatexOCR
from PIL import Image
import re
import preprocessing


def get_latex(image_array):

    model = LatexOCR()
    image_pil = Image.fromarray(image_array).convert('RGB')
    latex = model(image_pil)

    print(latex, '\n')
    return latex
# types = ['integral', 'de', 'polynomial', 'nonlinear', 'limit', 'derivative']
def get_type(latex_expression):
    if latex_expression.find('int') >= 0:
        return 'integral'
    elif (latex_expression.find('d x') >= 0 and latex_expression.find('d y') >= 0) or (latex_expression.find('\\prime') >= 0 and latex_expression.find('=') >= 0):
        return 'de'
    elif latex_expression.find('\\prime') >= 0 or latex_expression.find("'") >= 0:
        return 'derivative'
    elif latex_expression.find('sin') >= 0 or latex_expression.find('cos') >= 0 or latex_expression.find('tan') >= 0:
        return 'nonlinear'
    elif latex_expression.find('lim') >= 0:
        return 'limit'
    elif latex_expression.find('x') >= 0:
        return 'polynomial'
    else:
        return 'unknown'


def get_integral_bounds(latex_expression):
    match = re.search(r'\\int_{(.*?)}\^{(.*?)}', latex_expression)
    if match:
        lower_bound, upper_bound = match.groups()
    else:
        lower_bound, upper_bound = None, None
    print('lower_bound:', lower_bound, 'upper_bound:', upper_bound,'\n')
    return lower_bound, upper_bound

def get_derivative_expr(latex_expression):
    # d/dx
    match_frac = re.search(r'\\frac{d}{dx}\s*\((.+)\)', latex_expression)
    if match_frac:
        return match_frac.group(1)

    # ( ... )'
    match_prime = re.search(r'\((.+)\)\'', latex_expression)
    if match_prime:
        return match_prime.group(1)

    return latex_expression

def latex_to_sym(latex_expression):
    symbolic_exp = re.sub(r'\\operatorname\*{lim}_\{x\\to.*?\}', r'', latex_expression)
    symbolic_exp = re.sub(r'\\int_{.*?}\^{.*?}', '', symbolic_exp)
    symbolic_exp = re.sub(r'\\frac\{(.*?)\}\{(.*?)\}', r'(\1)/(\2)', symbolic_exp)
    symbolic_exp = symbolic_exp.replace(' ', '')
    symbolic_exp = symbolic_exp.replace('^', '**')
    symbolic_exp = symbolic_exp.replace('{', '').replace('}', '')
    symbolic_exp = symbolic_exp.replace('**\\prime', '')
    symbolic_exp = re.sub(r'(\d)(x)', r'\1*\2', symbolic_exp)
    symbolic_exp = re.sub(r'(\d)(\()', r'\1*\2', symbolic_exp)
    symbolic_exp = re.sub(r'(\d+(?:\.\d+)?)(e)', r'\1*\2', symbolic_exp)
    symbolic_exp = re.sub(r'e\*\*([0-9.]+)\*x', r'e**(\1*x)', symbolic_exp)
    symbolic_exp = re.sub(r'dx$', '', symbolic_exp)
    symbolic_exp = symbolic_exp.replace('e', 'E')
    return symbolic_exp

def get_symbolic_expression(image) :
    latex_expression = get_latex(image)
    type = get_type(latex_expression)
    if type == 'polynomial' :
        return latex_to_sym(latex_expression), type
    elif type == 'integral' :
        return latex_to_sym(latex_expression), type
    elif type == 'derivative':
        return latex_to_sym(latex_expression), type
    elif type == 'limit':
        return latex_to_sym(latex_expression), type
    elif type == 'de':
        return get_differential_expr(latex_expression), type


def get_limit_point(latex_expression):
    match = re.search(r'\\operatorname\*\{lim\}_\{.*?\\to([\d.]+)\}', latex_expression)
    return match.group(1)


def get_differential_expr(latex_expression):
    latex_expression = latex_expression.replace("\\frac{d y}{d x}", "Derivative(y(x), x)")
    latex_expression = latex_expression.replace("dy/dx", "Derivative(y(x), x)")
    latex_expression = latex_expression.replace("y'", "Derivative(y(x), x)")

    latex_expression = latex_expression.replace("{", "").replace("}", "")

    latex_expression = latex_expression.replace("^", "**")

    if '=' in latex_expression:
        lhs, rhs = latex_expression.split('=')
        latex_expression = f"{lhs} - ({rhs})"

    latex_expression = re.sub(r'\by\b(?!\()', 'y(x)', latex_expression)

    latex_expression = latex_expression.replace("y(x)**\\prime", "Derivative(y(x), x)")

    return latex_expression


# print(get_limit_point(get_latex('equations/lim1.png')))
# test_image = 'equations/preprocessed_integral2.png'
# print(get_latex(test_image))
# print(get_type(get_latex(test_image)))
# print(get_integral_bounds(get_latex(test_image)))
# print(latex_to_sym(get_latex(test_image)))