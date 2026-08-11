import cv2
import numpy as np
from PIL import Image


def pil_to_bgr(pil_image: Image.Image) -> np.ndarray:
    return cv2.cvtColor(np.array(pil_image.convert("RGB")), cv2.COLOR_RGB2BGR)


def to_sketch(pil_image: Image.Image) -> np.ndarray:
    bgr = pil_to_bgr(pil_image)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(gray)
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
    inverted_blur = cv2.bitwise_not(blurred)
    sketch = cv2.divide(gray, inverted_blur, scale=256.0)
    return sketch


def to_binary(pil_image: Image.Image) -> np.ndarray:
    bgr = pil_to_bgr(pil_image)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary


def array_to_png_bytes(arr: np.ndarray) -> bytes:
    img = Image.fromarray(arr)
    import io
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
