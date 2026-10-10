import numpy as np

def validate_rgb_image(image):
    if not isinstance(image, np.ndarray):
        raise TypeError("image must be a numpy.ndarray")
    if image.ndim != 3 or image.shape[2] != 3 or image.size == 0:
        raise ValueError("Expected non-empty H x W x 3 RGB array")
    return image

def normalize_uint8(image):
    validate_rgb_image(image)
    if image.dtype != np.uint8:
        raise TypeError("Expected uint8 input")
    return image.astype(np.float32) / 255.0
