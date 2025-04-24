import streamlit as st
import cv2
import numpy as np
from PIL import Image
from utils import extract_text, detect_blue_regions, guess_hidden_text

st.title("Hidden Text Analyzer Bot")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    pil_img = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(pil_img)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # OCR
    st.subheader("Extracted Text")
    text = extract_text(image_cv)
    st.text_area("Visible OCR Text", text, height=200)

    # Detect Blue
    st.subheader("Detected Hidden Areas (Blue)")
    contours = detect_blue_regions(image_cv)
    image_highlighted = image_np.copy()
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(image_highlighted, (x, y), (x+w, y+h), (255, 0, 0), 2)
    st.image(image_highlighted, caption="Highlighted Blue Regions")

    # Guessing
    st.subheader("Guessed Hidden Content")
    guesses = guess_hidden_text(image_cv, contours)
    for g in guesses:
        st.markdown(f"**Guess:** {g['guess']}")
        st.code(g['context'])
