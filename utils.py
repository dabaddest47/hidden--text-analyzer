import cv2
import numpy as np
import pytesseract
import re
from PIL import Image

def extract_text(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(rgb)
    return text

def detect_blue_regions(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([140, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def guess_hidden_text(image, contours):
    guesses = []
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        crop = rgb[max(y-20,0):min(y+h+20, rgb.shape[0]), max(x-100,0):min(x+w+100, rgb.shape[1])]
        context = pytesseract.image_to_string(crop)
        matches = re.findall(r'\b\d{1}-\d{1}\b', context)
        guesses.append({
            "box": (x, y, w, h),
            "context": context.strip(),
            "guess": matches[0] if matches else "?"
        })
    return guesses
