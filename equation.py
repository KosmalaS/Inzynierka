from pix2tex.cli import LatexOCR
from PIL import Image

ocr = LatexOCR()
print(ocr.ocr(Image.open('test2.png')))