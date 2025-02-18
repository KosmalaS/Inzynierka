import cv2
import numpy as np


def preprocess_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image not found at {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    _, image = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)


    success = cv2.imwrite(f"{image_path}proccessed.png", image)
    return image