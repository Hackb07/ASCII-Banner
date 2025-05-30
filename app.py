import streamlit as st
import pyfiglet
from PIL import Image
import os

def get_fonts_list():
    try:
        return pyfiglet.get_fonts()
    except AttributeError:
        fonts_dir = os.path.join(os.path.dirname(pyfiglet.__file__), "fonts")
        fonts = [f.replace(".flf", "") for f in os.listdir(fonts_dir) if f.endswith(".flf")]
        return fonts

def text_to_ascii(text, font):
    try:
        return pyfiglet.figlet_format(text, font=font)
    except pyfiglet.FontNotFound:
        return "Font not found!"

def image_to_ascii(image, width=100):
    # Resize with aspect ratio adjustment
    w_percent = width / float(image.size[0])
    h_size = int((float(image.size[1]) * w_percent) * 0.55)
    img = image.resize((width, h_size)).convert('L')  # grayscale

    ascii_chars = "@%#*+=-:. "
    scale = (len(ascii_chars) - 1) / 255  # map pixel values 0-255 to ascii index

    pixels = list(img.getdata())
    ascii_str = "".join([ascii_chars[int(pixel * scale)] for pixel in pixels])

    ascii_lines = [ascii_str[i:i + width] for i in range(0, len(ascii_str), width)]
    return "\n".join(ascii_lines)

st.title("🎨 ASCII Banner & Image to ASCII Generator")

tab1, tab2 = st.tabs(["📝 Text to ASCII", "🖼️ Image to ASCII"])

with tab1:
    st.subheader("Convert Text to ASCII Banner")
    input_text = st.text_input("Enter your text", value="Hello World")

    fonts = get_fonts_list()
    font = st.selectbox("Choose a font", options=sorted(fonts), index=fonts.index("slant") if "slant" in fonts else 0)

    if st.button("Generate ASCII Banner"):
        ascii_banner = text_to_ascii(input_text, font)
        st.code(ascii_banner)

with tab2:
    st.subheader("Convert Image to ASCII Art")
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        width = st.slider("Set ASCII Width", min_value=40, max_value=150, value=100, step=10)
        if st.button("Generate ASCII from Image"):
            ascii_art = image_to_ascii(image, width=width)
            st.code(ascii_art)
