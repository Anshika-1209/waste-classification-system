import streamlit as st
import tensorflow as tf
import numpy as np
import os
from PIL import Image


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="EcoSort | Smart Waste Classification",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# AI MODEL
# ============================================================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "waste_classifier_v2.keras"
)

model = tf.keras.models.load_model(MODEL_PATH)

CLASS_NAMES = [
    "cardboard",
    "glass",
    "metal",
    "paper",
    "plastic",
    "trash"
]


# ============================================================
# WASTE INFORMATION
# ============================================================

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


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: linear-gradient(
        -45deg,
        #eef4ff,
        #dbe4ff,
        #c7d2fe,
        #a5b4fc,
        #99f6e4,
        #eef4ff
    );
    background-size: 400% 400%;
    animation: gradientShift 16s ease infinite;

    color: #1a2332;
    font-family: 'Inter', sans-serif;
}

@keyframes gradientShift {
    0% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* =========================================================
   CENTER BRAND
   ========================================================= */

.brand {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #1a2332;
    letter-spacing: -1px;
    margin-bottom: 2px;
}

.brand-accent {
    color: #7c3aed;
}

.tagline {
    text-align: center;
    color: #64748b;
    font-size: 11px;
    letter-spacing: 3px;
    margin-bottom: 30px;
}


/* =========================================================
   HERO
   ========================================================= */

.hero-title {
    text-align: center;
    font-size: 50px;
    font-weight: 800;
    color: #1a2332;
    letter-spacing: -2px;
    margin-top: 10px;
}

.hero-accent {
    color: #0d9488;
}

.hero-description {
    text-align: center;
    max-width: 720px;
    margin: auto;
    color: #475569;
    font-size: 16px;
    line-height: 1.7;
}


/* =========================================================
   SECTION TITLES
   ========================================================= */

.section-title {
    font-size: 24px;
    font-weight: 750;
    color: #1a2332;
    margin-top: 38px;
    margin-bottom: 15px;
}


/* =========================================================
   STREAMLIT CONTAINERS
   ========================================================= */

[data-testid="stVerticalBlockBorderWrapper"] {
    background:
        linear-gradient(
            145deg,
            rgba(255, 255, 255, 0.92),
            rgba(238, 244, 255, 0.92)
        );

    border: 1px solid rgba(124, 58, 237, 0.16);
    border-radius: 20px;

    box-shadow:
        0 15px 40px rgba(37, 60, 130, 0.10);
}


/* =========================================================
   METRICS
   ========================================================= */

[data-testid="stMetric"] {
    background:
        rgba(255, 255, 255, 0.95);

    border: 1px solid rgba(13, 148, 136, 0.18);
    border-radius: 17px;
    padding: 18px;
}

[data-testid="stMetricLabel"] {
    color: #64748b !important;
}

[data-testid="stMetricValue"] {
    color: #0d9488 !important;
    font-weight: 800;
}


/* =========================================================
   FILE UPLOADER
   ========================================================= */

[data-testid="stFileUploader"] {
    background: rgba(240, 245, 255, 0.8);
    border-radius: 16px;
}

[data-testid="stFileUploader"] label {
    width: 100%;
    display: flex;
    justify-content: center;
    text-align: center;
}

[data-testid="stFileUploaderDropzone"] {
    background: rgba(248, 250, 255, 0.9) !important;
    border: 1px dashed rgba(124, 58, 237, 0.35) !important;
    border-radius: 15px !important;
    justify-content: center !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    text-align: center !important;
    justify-content: center !important;
    width: 100%;
}


/* =========================================================
   PROGRESS
   ========================================================= */

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #2563eb, #7c3aed, #0d9488);
}


/* =========================================================
   ALERTS
   ========================================================= */

[data-testid="stAlert"] {
    border-radius: 14px;
}


/* =========================================================
   IMAGE
   ========================================================= */

[data-testid="stImage"] img {
    border-radius: 16px;
}


/* =========================================================
   DIVIDER
   ========================================================= */

hr {
    border-color: rgba(124, 58, 237, 0.18) !important;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    padding-top: 25px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# CENTERED ECOSORT
# ============================================================

brand_col = st.columns([1, 2, 1])[1]

with brand_col:

    st.markdown(
        '<div class="brand">♻️ Eco<span class="brand-accent">Sort</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="tagline">AI • SUSTAINABILITY • SMART WASTE</div>',
        unsafe_allow_html=True
    )


# ============================================================
# HERO
# ============================================================

with st.container(border=True):

    st.markdown(
        "✦ **MACHINE LEARNING POWERED**"
    )

    st.markdown(
        '<div class="hero-title">Smart <span class="hero-accent">Waste Classification</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-description">
        Identify waste intelligently using image classification
        and turn every disposal decision into a smarter,
        more sustainable action.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">⚡ EcoSort at a Glance</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Technology", "AI / ML")

with c2:
    st.metric("Prediction", "Image")

with c3:
    st.metric("Features", "3+")

with c4:
    st.metric("Focus", "♻️ Eco")


# ============================================================
# UPLOAD
# ============================================================

st.markdown(
    '<div class="section-title">📡 Analyze Waste</div>',
    unsafe_allow_html=True
)

upload_col = st.columns([1, 2, 1])[1]

with upload_col:

    with st.container(border=True):

        st.subheader("📷 Upload Your Waste")

        st.write(
            "Upload a clear image and EcoSort will "
            "analyze the waste category."
        )

        uploaded_file = st.file_uploader(
            "Choose an image",
            type=["jpg", "jpeg", "png"]
        )


# ============================================================
# TIPS
# ============================================================

tip_cols = st.columns(5)

tips = [
    ("01", "Clear image"),
    ("02", "Object visible"),
    ("03", "Good lighting"),
    ("04", "One main object"),
    ("05", "JPG or PNG"),
]

for col, (number, text) in zip(tip_cols, tips):

    with col:

        with st.container(border=True):

            st.markdown(f"**{number}**")
            st.caption(text)


# ============================================================
# ANALYSIS
# ============================================================

if uploaded_file is not None:

    st.markdown(
        '<div class="section-title">🧠 AI Analysis</div>',
        unsafe_allow_html=True
    )

    image_col, result_col = st.columns(
        [1, 1],
        gap="large"
    )


    # --------------------------------------------------------
    # IMAGE
    # --------------------------------------------------------

    with image_col:

        with st.container(border=True):

            st.subheader("🖼️ Image Preview")

            st.image(
                uploaded_file,
                caption="Uploaded Waste",
                width="stretch"
            )


    # --------------------------------------------------------
    # REAL AI PREDICTION
    # --------------------------------------------------------

    image = Image.open(uploaded_file).convert("RGB")
    image = image.resize((224, 224))

    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(
        img_array,
        verbose=0
    )

    predicted_index = np.argmax(predictions[0])

    predicted_class = CLASS_NAMES[predicted_index]

    confidence = float(
        predictions[0][predicted_index]
    ) * 100

    waste_info = WASTE_INFO[predicted_class]

    recyclability = waste_info["score"]

    bin_info = waste_info["bin"]

    recycling_method = waste_info["method"]


    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    with result_col:

        with st.container(border=True):

            st.subheader("🎯 Classification Result")

            st.markdown(
                f"## ♻️ {predicted_class.title()}"
            )

            st.caption("Predicted Waste Category")

            st.write("**Model Confidence**")

            st.progress(
                confidence / 100
            )

            st.caption(
                f"{confidence:.2f}% confidence"
            )

            st.divider()

            r1, r2 = st.columns(2)

            with r1:

                st.metric(
                    "♻️ Recyclability",
                    f"{recyclability}%"
                )

            with r2:

                st.metric(
                    "🗂️ Category",
                    predicted_class.title()
                )


    # ========================================================
    # SMART INSIGHTS
    # ========================================================

    st.markdown(
        '<div class="section-title">🌱 Smart Waste Insights</div>',
        unsafe_allow_html=True
    )

    f1, f2, f3 = st.columns(3)


    # --------------------------------------------------------
    # COLOR INDICATOR
    # --------------------------------------------------------

    with f1:

        with st.container(border=True):

            st.subheader(f"{bin_info.split(' ')[0]} Color Indicator")

            st.write(
                "Recommended waste-bin indicator "
                "for the predicted category."
            )

            st.info(
                f"Recommended Bin: {bin_info}"
            )


    # --------------------------------------------------------
    # RECYCLING METHOD
    # --------------------------------------------------------

    with f2:

        with st.container(border=True):

            st.subheader("♻️ Recycling Method")

            st.write(
                "Suggested handling method for "
                "the identified waste."
            )

            st.success(
                recycling_method
            )


    # --------------------------------------------------------
    # RECYCLABILITY SCORE
    # --------------------------------------------------------

    with f3:

        with st.container(border=True):

            st.subheader("📊 Recyclability Score")

            st.metric(
                "Score",
                f"{recyclability}%"
            )

            st.progress(
                recyclability / 100
            )

            st.caption(
                "Estimated recycling suitability"
            )


# ============================================================
# HOW IT WORKS
# ============================================================

st.markdown(
    '<div class="section-title">🚀 How EcoSort Works</div>',
    unsafe_allow_html=True
)

s1, s2, s3, s4 = st.columns(4)


with s1:

    with st.container(border=True):

        st.subheader("01 📷")

        st.markdown("**Upload**")

        st.write(
            "Upload an image of your waste."
        )


with s2:

    with st.container(border=True):

        st.subheader("02 🧠")

        st.markdown("**Analyze**")

        st.write(
            "The ML model analyzes the image."
        )


with s3:

    with st.container(border=True):

        st.subheader("03 🎯")

        st.markdown("**Classify**")

        st.write(
            "The system predicts the waste category."
        )


with s4:

    with st.container(border=True):

        st.subheader("04 ♻️")

        st.markdown("**Guide**")

        st.write(
            "Get recycling and disposal guidance."
        )


# ============================================================
# WHY ECOSORT
# ============================================================

st.markdown(
    '<div class="section-title">🌍 Why EcoSort?</div>',
    unsafe_allow_html=True
)

problem, solution = st.columns(2)


with problem:

    with st.container(border=True):

        st.subheader("🗑️ The Challenge")

        st.write(
            """
            Improper waste segregation makes recycling
            harder and can increase the amount of waste
            going to landfills.
            """
        )


with solution:

    with st.container(border=True):

        st.subheader("💚 Our Approach")

        st.write(
            """
            EcoSort uses machine learning based image
            classification to identify waste and provide
            useful recycling information.
            """
        )


# ============================================================
# VISION
# ============================================================

st.markdown(
    '<div class="section-title">🌿 Our Vision</div>',
    unsafe_allow_html=True
)

with st.container(border=True):

    st.subheader(
        "♻️ From Waste Identification to Smart Action"
    )

    st.write(
        """
        EcoSort aims to make waste segregation easier
        by converting a simple waste image into useful
        information such as its category, recommended
        bin, recycling method and recyclability score.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        ♻️ EcoSort • AI-Powered Waste Classification
        <br><br>
        BE Machine Learning Project
    </div>
    """,
    unsafe_allow_html=True
)
