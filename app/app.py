import streamlit as st
import tensorflow as tf
import numpy as np
import os
from PIL import Image


# --------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------

st.set_page_config(
    page_title="EcoSort | Smart Waste Classification",
    page_icon="♻️",
    layout="wide"
)


# --------------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(135deg, #f7fff9 0%, #eef8f1 100%);
    }

    .main-title {
        font-size: 52px;
        font-weight: 800;
        color: #123c2a;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 19px;
        color: #557064;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 30px;
        font-weight: 750;
        color: #173f2c;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    .metric-card {
        padding: 18px;
        border-radius: 15px;
        background: rgba(255,255,255,0.9);
        box-shadow: 0px 4px 15px rgba(0,0,0,0.07);
        text-align: center;
    }

    .prediction-value {
        font-size: 30px;
        font-weight: 800;
        color: #1b5e20;
    }

    .small-text {
        color: #66756c;
        font-size: 14px;
    }

    .feature-card {
        padding: 22px;
        border-radius: 16px;
        background: rgba(255,255,255,0.85);
        box-shadow: 0px 3px 12px rgba(0,0,0,0.06);
        min-height: 160px;
    }

    .footer {
        text-align: center;
        color: #708078;
        margin-top: 40px;
        padding: 20px;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------------
# MODEL CONFIGURATION
# --------------------------------------------------------

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "waste_classifier_v2.keras"
)


CLASS_NAMES = [
    "cardboard",
    "glass",
    "metal",
    "paper",
    "plastic",
    "trash"
]


# --------------------------------------------------------
# WASTE INFORMATION
# --------------------------------------------------------

WASTE_INFO = {

    "cardboard": {
        "bin": "🟤 Brown",
        "method": "Flatten cardboard and send it for paper/cardboard recycling.",
        "score": 85
    },

    "glass": {
        "bin": "🟢 Green",
        "method": "Separate glass carefully and send it to a suitable glass recycling facility.",
        "score": 90
    },

    "metal": {
        "bin": "⚙️ Grey",
        "method": "Separate metal items and send them to a metal recycling facility.",
        "score": 95
    },

    "paper": {
        "bin": "🔵 Blue",
        "method": "Keep paper clean and dry and send it for paper recycling.",
        "score": 85
    },

    "plastic": {
        "bin": "🟡 Yellow",
        "method": "Separate clean plastic and send it to a suitable recycling facility.",
        "score": 80
    },

    "trash": {
        "bin": "⚫ Black",
        "method": "Dispose of non-recyclable waste through the appropriate general-waste system.",
        "score": 20
    }
}


# --------------------------------------------------------
# LOAD MODEL
# --------------------------------------------------------

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)


try:
    model = load_model()
    model_loaded = True

except Exception as e:
    model = None
    model_loaded = False
    st.error(f"Unable to load model: {e}")


# --------------------------------------------------------
# HEADER / HERO SECTION
# --------------------------------------------------------

st.markdown(
    '<div class="main-title">♻️ EcoSort</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Smart Waste Classification System using AI</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------------
# OVERVIEW
# --------------------------------------------------------

st.markdown(
    '<div class="section-title">🌱 Making Waste Sorting Smarter</div>',
    unsafe_allow_html=True
)

st.write(
    """
    EcoSort uses an AI-based image classification model to identify
    different types of waste and provide useful recycling information.
    Upload a waste image and let EcoSort analyse it.
    """
)


# --------------------------------------------------------
# FILE UPLOADER
# --------------------------------------------------------

st.markdown(
    '<div class="section-title">📸 Upload Waste Image</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose a waste image",
    type=["jpg", "jpeg", "png"]
)


# --------------------------------------------------------
# ANALYSIS
# --------------------------------------------------------

if uploaded_file is not None:

    if not model_loaded:
        st.error("Model could not be loaded. Please check the model file path.")
        st.stop()

    image = Image.open(uploaded_file).convert("RGB")

    st.markdown(
        '<div class="section-title">🔍 Analysis</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 1])

    with col1:

        st.image(
            image,
            caption="Uploaded Waste Image",
            width="stretch"
        )

    # ----------------------------------------------------
    # PREPROCESS IMAGE
    # ----------------------------------------------------

    resized_image = image.resize((224, 224))

    img_array = np.array(resized_image)

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    # ----------------------------------------------------
    # PREDICTION
    # ----------------------------------------------------

    predictions = model.predict(
        img_array,
        verbose=0
    )

    predicted_index = int(
        np.argmax(predictions[0])
    )

    predicted_class = CLASS_NAMES[predicted_index]

    confidence = float(
        predictions[0][predicted_index]
    ) * 100

    waste_info = WASTE_INFO[predicted_class]

    recyclability = waste_info["score"]

    bin_info = waste_info["bin"]

    recycling_method = waste_info["method"]


    # ----------------------------------------------------
    # RESULT
    # ----------------------------------------------------

    with col2:

        st.subheader("🎯 Prediction")

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="small-text">Predicted Waste</div>
                <div class="prediction-value">
                    {predicted_class.title()}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="small-text">Confidence</div>
                <div class="prediction-value">
                    {confidence:.2f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


        st.write("")

        st.progress(
            min(confidence / 100, 1.0)
        )


    # ----------------------------------------------------
    # SMART WASTE INSIGHTS
    # ----------------------------------------------------

    st.markdown(
        '<div class="section-title">🌱 Smart Waste Insights</div>',
        unsafe_allow_html=True
    )

    f1, f2, f3 = st.columns(3)


    # ----------------------------------------------------
    # COLOR INDICATOR
    # ----------------------------------------------------

    with f1:

        with st.container(border=True):

            indicator_icon = bin_info.split(" ")[0]

            st.subheader(
                f"{indicator_icon} Color Indicator"
            )

            st.write(
                "Recommended waste-bin indicator "
                "for the predicted category."
            )

            st.info(
                f"Recommended Bin: {bin_info}"
            )


    # ----------------------------------------------------
    # RECYCLING METHOD
    # ----------------------------------------------------

    with f2:

        with st.container(border=True):

            st.subheader("♻️ Recycling Method")

            st.write(
                recycling_method
            )


    # ----------------------------------------------------
    # RECYCLABILITY SCORE
    # ----------------------------------------------------

    with f3:

        with st.container(border=True):

            st.subheader("📊 Recyclability Score")

            st.metric(
                "Score",
                f"{recyclability}/100"
            )

            st.progress(
                recyclability / 100
            )


# --------------------------------------------------------
# HOW IT WORKS
# --------------------------------------------------------

st.markdown(
    '<div class="section-title">⚙️ How EcoSort Works</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)


with c1:

    st.markdown(
        """
        <div class="feature-card">
            <h3>📸 1. Upload</h3>
            <p>
            Upload an image of the waste item you want to classify.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        """
        <div class="feature-card">
            <h3>🧠 2. Analyse</h3>
            <p>
            The trained AI model analyses the image and predicts
            the waste category.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        """
        <div class="feature-card">
            <h3>♻️ 3. Act</h3>
            <p>
            EcoSort provides recycling guidance, bin indication,
            and a recyclability score.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------------
# WHY ECOSORT
# --------------------------------------------------------

st.markdown(
    '<div class="section-title">💡 Why EcoSort?</div>',
    unsafe_allow_html=True
)

st.write(
    """
    Proper waste segregation is an important part of responsible
    waste management. EcoSort combines machine learning with a
    simple interactive interface to make waste classification
    easier and more understandable.
    """
)


# --------------------------------------------------------
# PROJECT VISION
# --------------------------------------------------------

st.markdown(
    '<div class="section-title">🌍 Project Vision</div>',
    unsafe_allow_html=True
)

st.info(
    """
    Our vision is to encourage smarter waste segregation by using
    accessible AI technology and clear recycling guidance.
    """
)


# --------------------------------------------------------
# FOOTER
# --------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        ♻️ EcoSort — Smart Waste Classification System<br>
        Built with Python, TensorFlow and Streamlit
    </div>
    """,
    unsafe_allow_html=True
)