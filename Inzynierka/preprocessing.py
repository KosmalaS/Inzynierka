import cv2
import numpy as np

test_image = 'equations/integral2.png'
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)

    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    return binary

# preprocessed_image = preprocess_image(test_image)
# cv2.imshow('preprocessed image', preprocessed_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.imwrite('equations/preprocessed_integral2.png', preprocessed_image)