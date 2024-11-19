from pix2tex.cli import LatexOCR
from PIL import Image
import re
import sympy as sp

test_image = 'equations/cubic2.png'
def get_latex(image_path) :
    model = LatexOCR()
    image = Image.open(image_path)
    return model(image)

# types = ['integral', 'de', 'polynomial', 'nonlinear', 'limit', 'derivative']
def get_type(latex_expression) :
    if latex_expression.find('int') >= 0:
        return 'integral'
    elif latex_expression.find('d x') >= 0 and latex_expression.find('d y') >= 0:
        return 'de'
    elif latex_expression.find('x') >= 0:
        return 'polynomial'
    elif latex_expression.find('sin') >= 0 or latex_expression.find('cos') >= 0 or latex_expression.find('tan') >= 0 :
        return 'nonlinear'
    elif latex_expression.find('lim') >= 0:
        return 'limit'
    elif latex_expression.find('d') >= 0:
        return 'derivative'
    else :
        return 'unknown'

def latex_to_sym(latex_expression) :
    symbolic_exp = latex_expression.replace(' ', '') # spacje out
    symbolic_exp = symbolic_exp.replace('^', '**') # zamiana potegi
    symbolic_exp = symbolic_exp.replace('{', '').replace('}', '')
    symbolic_exp = re.sub(r'(\d)(x)', r'\1*\2', symbolic_exp)
    return symbolic_exp

def get_symbolic_expression(image_path) :
    latex_expression = get_latex(image_path)
    type = get_type(latex_expression)
    if type == 'polynomial' :
        return latex_to_sym(latex_expression)
    else :
        return 'Not a polynomial'



# print(get_latex(test_image))
# print(get_type(get_latex(test_image)))
# print(latex_to_sym(get_latex(test_image)))