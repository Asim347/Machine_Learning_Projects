import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import streamlit as st

# Initialize Porter Stemmer
ps = PorterStemmer()


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words("english") and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


# Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="SMS Spam Classifier | AI Security",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom Pro-Level CSS Styling
st.markdown(
    """
    <style>
        .main {
            background-color: #0e1117;
        }
        .stTextArea textarea {
            background-color: #161b22;
            color: #c9d1d9;
            border: 1px solid #30363d;
            border-radius: 10px;
            font-size: 16px;
        }
        .stButton button {
            background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
            color: white;
            font-weight: 600;
            border: none;
            padding: 0.6rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
            transition: all 0.3s ease;
            width: 100%;
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(99, 102, 241, 0.5);
        }
        .card {
            background-color: #161b22;
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid #30363d;
            box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        }
        h1 {
            color: #f0f6fc;
            font-family: 'Inter', sans-serif;
            font-weight: 800;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# Load Model and Vectorizer safely
@st.cache_resource
def load_assets():
    tfidf = pickle.load(open("vectorizer.pkl", "rb"))
    model = pickle.load(open("model.pkl", "rb"))
    return tfidf, model


tfidf, model = load_assets()

# Sidebar Design
with st.sidebar:
    st.image("https://img.icons8.com/color/96/domain-security.png", width=80)
    st.markdown("### 🛡️ AI Security Suite")
    st.info(
        "This application leverages Machine Learning & Natural Language Processing"
        " (NLP) to filter out unwanted spam messages in real-time."
    )
    st.markdown("---")
    st.markdown("**Built with:** Python, Scikit-Learn & Streamlit")
    st.markdown("**Developer:** Portfolio Project")

# Main Interface Layout
st.markdown(
    "<div style='text-align: center;'><h1>📧 Email & SMS Spam"
    " Detector</h1><p style='color: #8b949e; font-size: 1.1rem;'>Protect your"
    " inbox instantly with high-precision text"
    " classification.</p></div><br>",
    unsafe_allow_html=True,
)

# Input container card
input_sms = st.text_area(
    "**Enter your message below:**",
    placeholder="e.g., Congratulations! You have won a $1,000 Walmart gift card...",
    height=120,
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    predict_btn = st.button("🔍 Analyze Message")

# Backend Prediction Logic & Result Presentation
if predict_btn:
    if input_sms.strip() == "":
        st.warning("⚠️ Please enter a message text before analyzing.")
    else:
        with st.spinner("Analyzing text patterns..."):
            transformed_sms = transform_text(input_sms)
            vector_input = tfidf.transform([transformed_sms])
            result = model.predict(vector_input)[0]

        st.markdown("<br>", unsafe_allow_html=True)

        if result == 1:
            st.error(
                "🚨 **SPAM DETECTED!** This message exhibits characteristics of"
                " unsolicited promotional or malicious content.",
                icon="🚨",
            )
        else:
            st.success(
                "✅ **SAFE MESSAGE (NOT SPAM).** This message appears to be"
                " legitimate and clean.",
                icon="🛡️",
            )