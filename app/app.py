import streamlit as st

st.title("♻️ Waste Classification System")

st.write("Upload an image of waste to classify it.")

uploaded_file = st.file_uploader(
    "Upload Waste Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Waste Image")

    st.success("Image uploaded successfully!")