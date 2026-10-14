
import streamlit as st
from transformers import pipeline

st.set_page_config(
    page_title="News Headline Generator",
    page_icon="📰"
)

st.title("📰 Automatic News Headline Generation")
st.write("Generate a headline from a news article using NLP.")

@st.cache_resource
def load_model():
    return pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6"
    )

with st.spinner("Loading NLP model..."):
    generator = load_model()

article = st.text_area(
    "Enter your news article",
    height=220,
    placeholder="Paste your full news article here..."
)

if st.button("Generate Headline"):
    if len(article.split()) < 20:
        st.warning("Please enter at least 20 words.")
    else:
        with st.spinner("Generating headline..."):
            result = generator(
                article,
                max_length=40,
                min_length=8,
                do_sample=False,
                truncation=True
            )

        st.success("Generated Headline / Summary")
        st.subheader(result[0]["summary_text"])
