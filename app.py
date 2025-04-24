import streamlit as st
from PIL import Image
import pytesseract
import io

st.set_page_config(page_title="Hidden Text Analyzer Bot", layout="centered")

st.title("Hidden Text Analyzer Bot")
st.write("Upload an image to detect and extract hidden or embedded text.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Run OCR
        st.write("Processing image for hidden text...")
        text = pytesseract.image_to_string(image)

        if text.strip():
            st.subheader("Detected Text")
            st.text_area("Text from Image", text, height=250)
        else:
            st.warning("No text was detected in the image.")
    except Exception as e:
        st.error(f"Something went wrong while processing the image: {e}")
else:
    st.info("Please upload an image to begin.")
