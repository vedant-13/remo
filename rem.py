import streamlit as st
import requests
from rembg import remove
from streamlit_lottie import st_lottie
from PIL import Image
import io

# Add CSS styles
html_file = open('style.css', 'r')
st.markdown(f'<style>{html_file.read()}</style>', unsafe_allow_html=True)

def main():
    def load_lottie_url(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    # Load the Lottie animations from the URLs
    start_animation_url = "https://assets5.lottiefiles.com/packages/lf20_9evakyqx.json"

    start_animation_json = load_lottie_url(start_animation_url)


    # Display the start animation
    st_lottie(start_animation_json, height=400, key="lottie_start")

    st.title("Background Remover")

    inputPath = st.file_uploader("Select image file", type=["png", "jpg", "jpeg"])
    outputPath = st.text_input("Enter output file name", "output.png")

    if inputPath is not None:
        inputImage = Image.open(inputPath)

        # Display the finish animation while removing the background
        with st.spinner("Removing background..."):
           
            outputImage = remove(inputImage)

        # Convert the output image to RGBA mode if it's not already
        if outputImage.mode != "RGBA":
            outputImage = outputImage.convert("RGBA")

        st.image(outputImage, caption="Output Image", use_column_width=True)

        # Create a button to download the output image
        download_button = st.download_button(
            label="Download Output",
            data=io.BytesIO(outputImage.tobytes()),
            file_name=outputPath,
            mime="image/png"
        )
        if download_button:
            st.success(f"Output downloaded as {outputPath}")

if __name__ == "__main__":
    main()
