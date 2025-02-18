import cv2
import numpy as np
import os

def binarize_200(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"Nie można wczytać obrazu: {image_path}")

    if len(img.shape) == 3 and img.shape[2] == 4:
        b, g, r, a = cv2.split(img)
        bgr = cv2.merge((b, g, r))

        white = np.full(bgr.shape, 255, dtype=np.uint8)
        alpha_float = a.astype(float) / 255.0
        alpha_float_3d = cv2.merge([alpha_float, alpha_float, alpha_float])

        bgr = (bgr.astype(float) * alpha_float_3d
               + white.astype(float) * (1 - alpha_float_3d)).astype(np.uint8)
    else:
        bgr = img

    if len(bgr.shape) == 3:
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    else:
        gray = bgr

    _, th_bin = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    return th_bin


def _binarize_and_crop(img, threshold=200):

    if len(img.shape) == 3 and img.shape[2] == 4:
        b, g, r, a = cv2.split(img)
        bgr = cv2.merge((b, g, r))
        white = np.full(bgr.shape, 255, dtype=np.uint8)
        alpha_float = a.astype(float) / 255.0
        alpha_float_3d = cv2.merge([alpha_float, alpha_float, alpha_float])
        bgr = (bgr.astype(float) * alpha_float_3d + white.astype(float) * (1 - alpha_float_3d)).astype(np.uint8)
    else:
        bgr = img

    if len(bgr.shape) == 3:
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    else:
        gray = bgr


    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    black_pixels = np.where(binary == 0)
    if len(black_pixels[0]) == 0:

        return binary

    y_min = np.min(black_pixels[0])
    y_max = np.max(black_pixels[0])
    x_min = np.min(black_pixels[1])
    x_max = np.max(black_pixels[1])

    cropped = binary[y_min:y_max + 1, x_min:x_max + 1]
    return cropped


def _load_and_preprocess_template(file_path, threshold=200):
    img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"Nie można wczytać szablonu: {file_path}")

    bin_img = _binarize_and_crop(img, threshold=threshold)
    return bin_img


def _load_templates(templates_folder="templates"):
    template_files = {
        '0': "0.png",
        '1': "1.png",
        '2': "2.png",
        '3': "3.png",
        '4': "4.png",
        '5': "5.png",
        '6': "6.png",
        '7': "7.png",
        '8': "8.png",
        '9': "9.png",
        'x': "x.png",
        '+': "plus.png",
        '-': "minus.png",
        '=': "equal.png",
        '(': "open.png",
        ')': "close.png"
    }

    templates = {}
    for symbol, fname in template_files.items():
        full_path = os.path.join(templates_folder, fname)
        tpl_bin = _load_and_preprocess_template(full_path, threshold=200)
        templates[symbol] = (tpl_bin, tpl_bin.shape)
    return templates


def segment_by_vertical_whitespace(bin_img, min_black_pixels=1):

    height, width = bin_img.shape

    separators = []
    previous_was_separator = True

    for x in range(width):
        black_count = np.sum(bin_img[:, x] == 0)
        if black_count <= min_black_pixels:
            if not previous_was_separator:
                separators.append(x)
            previous_was_separator = True
        else:
            if previous_was_separator:
                separators.append(x)
            previous_was_separator = False


    if not previous_was_separator:
        separators.append(width)

    segments = []
    for i in range(0, len(separators) - 1, 2):
        x_start = separators[i]
        x_end = separators[i + 1]
        if x_end - x_start > 1:
            segments.append((x_start, x_end))

    return segments


def recognize_equation_vertical(image_path, templates_folder="Inzynierka/templates", match_threshold=0.8,
                                minus_ratio_threshold=3.0):

    bin_img = binarize_200(image_path)

    templates = _load_templates(templates_folder)

    os.makedirs("segments", exist_ok=True)

    segments = segment_by_vertical_whitespace(bin_img, min_black_pixels=0)
    # print("[DEBUG] Wykryte pionowe segmenty:", segments)


    color_img = cv2.cvtColor(bin_img, cv2.COLOR_GRAY2BGR)

    recognized_equation = ""
    segment_index = 0

    for (x_start, x_end) in segments:

        segment = bin_img[:, x_start:x_end]
        black_pixels = np.where(segment == 0)
        if len(black_pixels[0]) == 0:
            continue

        y_min = np.min(black_pixels[0])
        y_max = np.max(black_pixels[0])
        roi = bin_img[y_min: y_max + 1, x_start:x_end]

        cv2.rectangle(color_img, (x_start, y_min), (x_end, y_max + 1), (0, 0, 255), 2)

        roi_height, roi_width = roi.shape
        ratio = roi_width / roi_height

        best_symbol = None
        best_score = -1.0


        if ratio > minus_ratio_threshold:
            # print(
            #     f"    Region ma wysoki stosunek szerokości do wysokości ({ratio:.2f}). Przyjmujemy '-', pomijając matchTemplate.")
            best_symbol = '-'
            best_score = 1.0
        else:
            for symbol, (tpl_img, tpl_shape) in templates.items():

                roi_resized = cv2.resize(roi, (tpl_shape[1], tpl_shape[0]))
                roi_float = roi_resized.astype(np.float32) / 255.0
                tpl_float = tpl_img.astype(np.float32) / 255.0

                result = cv2.matchTemplate(roi_float, tpl_float, cv2.TM_CCOEFF_NORMED)
                score = result[0][0]
                # print(f"    Symbol '{symbol}': wynik dopasowania = {score:.4f}")
                if score > best_score:
                    best_score = score
                    best_symbol = symbol

            # print(f"    Najlepsze dopasowanie: symbol '{best_symbol}' z wynikiem {best_score:.4f}")


        if best_symbol is not None:
            recognized_equation += best_symbol
        else:
            recognized_equation += "?"

    recognized_equation = recognized_equation.strip()
    print(recognized_equation,'\n')
    return recognized_equation
