import streamlit as st
import cv2
import numpy as np
from PIL import Image
from rembg import remove
import io

# Custom CSS for Box-Style UI
st.markdown("""
    <style>
    body {
        background-color: #1e1e2e;
        color: white;
    }
    .box {
        background: #282a36;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    .stButton button {
        background-color: #ff6b6b !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align:center;'>🖼️ AI-Powered Image Editor</h1>", unsafe_allow_html=True)

# Upload Image Box
st.markdown("<div class='box'>", unsafe_allow_html=True)
st.subheader("📤 Upload an Image")
uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    st.image(image, caption="📌 Uploaded Image", use_column_width=True)

    # Image Processing Box
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("🔧 Editing Options")
    option = st.radio("Select an effect:", ["Remove Background", "Grayscale", "Blur Effect", "Edge Detection", "Add Background", "Adjust Brightness & Contrast", "Crop Image"], key="effect")
    st.markdown("</div>", unsafe_allow_html=True)

    # Processing
    processed_image = img_array

    if option == "Remove Background":
        processed_image = remove(img_array)

    elif option == "Grayscale":
        processed_image = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

    elif option == "Blur Effect":
        blur_value = st.slider("🔄 Blur Intensity", 1, 10, 3)
        processed_image = cv2.GaussianBlur(img_array, (2*blur_value+1, 2*blur_value+1), 0)

    elif option == "Edge Detection":
        processed_image = cv2.Canny(img_array, 100, 200)

    elif option == "Add Background":
        bg_color = st.color_picker("🎨 Choose Background Color", "#ffffff")
        bg_array = np.full_like(img_array, tuple(int(bg_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)))
        mask = remove(img_array, only_mask=True)
        processed_image = np.where(mask[..., None], bg_array, img_array)

    elif option == "Adjust Brightness & Contrast":
        brightness = st.slider("☀️ Brightness", -100, 100, 0)
        contrast = st.slider("🎛️ Contrast", -100, 100, 0)
        processed_image = cv2.convertScaleAbs(img_array, alpha=1 + contrast/100, beta=brightness)

    elif option == "Crop Image":
        h, w = img_array.shape[:2]
        x1 = st.slider("X1 (Left)", 0, w, 0)
        y1 = st.slider("Y1 (Top)", 0, h, 0)
        x2 = st.slider("X2 (Right)", x1, w, w)
        y2 = st.slider("Y2 (Bottom)", y1, h, h)
        processed_image = img_array[y1:y2, x1:x2]

    # Show Processed Image
    st.image(processed_image, caption="✨ Processed Image", use_column_width=True)

    # Download Button Box
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("📥 Download Edited Image")
    img_byte_array = io.BytesIO()

    try:
        # Ensure processed_image is in RGB mode before saving
        if len(processed_image.shape) == 2:  # Grayscale or Edge Detection
            processed_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2RGB)
        elif processed_image.shape[-1] == 4:  # RGBA to RGB (Remove Alpha)
            processed_image = cv2.cvtColor(processed_image, cv2.COLOR_RGBA2RGB)

        Image.fromarray(processed_image).save(img_byte_array, format="PNG")
        st.download_button(label="Download Image", data=img_byte_array.getvalue(), file_name="edited_image.png", mime="image/png")

    except Exception as e:
        st.error(f"⚠️ Error saving image: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

# Footer - Developed by Muhammad Anas
st.markdown("""
    <hr style="border: 1px solid #ccc; margin-top: 40px;">
    <div style="text-align: center;">
        <p style="font-size: 16px;">Developed by <b>Muhammad Anas</b></p>
        <p>
            🔗 <a href="https://www.linkedin.com/in/anas-ahmed12/" target="_blank" style="color: #0077b5; text-decoration: none;">LinkedIn</a> |  
            🖥️ <a href="https://github.com/Anas-ahmed12?tab=repositories" target="_blank" style="color: #24292e; text-decoration: none;">GitHub</a>
        </p>
    </div>
""", unsafe_allow_html=True)
