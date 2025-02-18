import time
import os
from equation import get_latex
from simpleOCR import recognize_equation_vertical
import preprocessing

def compare_recognition_times(folder_path):
    results = []

    for i in range(1, 11):
        image_path = os.path.join(folder_path, f'linear{i}.png')
        image = preprocessing.preprocess_image(image_path)
        start_time = time.time()
        latex_equation = get_latex(image)
        pix2tex_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        start_time = time.time()
        custom_equation = recognize_equation_vertical(image_path)
        custom_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        results.append({
            "Image": f'linear{i}.png',
            "Pix2Tex Time (ms)": pix2tex_time,
            "Custom OCR Time (ms)": custom_time
        })

    return results

print(compare_recognition_times(r"Inzynierka\equations"))

