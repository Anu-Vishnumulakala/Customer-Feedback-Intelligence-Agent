import os
import streamlit as st
from feedback_analyzer import analyze_feedback_batch

st.set_page_config(
    page_title="Customer Feedback Intelligence Agent",
    page_icon="📊🧠",
    layout="centered"
)

st.title("📊🧠 Customer Feedback Intelligence Agent")
st.caption(
    "Transform raw customer feedback into actionable business insights using AI."
)

openai_api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    help="Used only for this session"
)

if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key

st.subheader("📥 Upload Customer Feedback")

uploaded_file = st.file_uploader(
    "Upload a CSV file with a column named `feedback`",
    type=["csv"]
)

if uploaded_file and openai_api_key:
    with st.spinner("Analyzing customer feedback..."):
        results = analyze_feedback_batch(uploaded_file)

    st.success("Analysis complete!")

    st.subheader("📌 Insights Summary")
    st.json(results["summary"])

    st.subheader("📊 Detailed Analysis")
    st.dataframe(results["detailed_results"])

st.caption(
    "This project demonstrates AI-powered customer insight extraction for marketing and product teams."
)
