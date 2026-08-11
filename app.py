import io
import streamlit as st
from PIL import Image
from image_processor import to_sketch, to_binary, array_to_png_bytes

st.set_page_config(page_title="Photo → Sketch / Binary", layout="wide")
st.title("Photo → Sketch / Binary Converter")
st.caption("Upload a photo and convert it to a pencil sketch or a binary (black & white) image.")

uploaded = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])

if uploaded:
    original = Image.open(uploaded)

    mode = st.radio(
        "Output style",
        ["Pencil Sketch", "Binary (B&W)", "Both"],
        horizontal=True,
    )

    st.divider()

    if mode == "Both":
        col_orig, col_sketch, col_binary = st.columns(3)
        sketch_arr = to_sketch(original)
        binary_arr = to_binary(original)

        with col_orig:
            st.subheader("Original")
            st.image(original, use_container_width=True)

        with col_sketch:
            st.subheader("Pencil Sketch")
            st.image(sketch_arr, use_container_width=True, clamp=True)
            st.download_button(
                "Download Sketch",
                data=array_to_png_bytes(sketch_arr),
                file_name="sketch.png",
                mime="image/png",
            )

        with col_binary:
            st.subheader("Binary (B&W)")
            st.image(binary_arr, use_container_width=True, clamp=True)
            st.download_button(
                "Download Binary",
                data=array_to_png_bytes(binary_arr),
                file_name="binary.png",
                mime="image/png",
            )

    else:
        col_orig, col_result = st.columns(2)

        with col_orig:
            st.subheader("Original")
            st.image(original, use_container_width=True)

        with col_result:
            if mode == "Pencil Sketch":
                result_arr = to_sketch(original)
                st.subheader("Pencil Sketch")
                filename = "sketch.png"
            else:
                result_arr = to_binary(original)
                st.subheader("Binary (B&W)")
                filename = "binary.png"

            st.image(result_arr, use_container_width=True, clamp=True)
            st.download_button(
                f"Download {mode}",
                data=array_to_png_bytes(result_arr),
                file_name=filename,
                mime="image/png",
            )
