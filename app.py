import streamlit as st
import pandas as pd
from openai import OpenAI

st.title("📊 Excel Sales Analyzer with AI")

# Load OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Upload Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.subheader("📈 Excel Data")
        st.write(df)

        # Simple column summary
        st.subheader("🧮 Column Summary")
        st.write(df.describe(include='all'))

        # GPT prompt generation
        prompt = f"Analyze the following sales data and provide key insights:\n\n{df.head(20).to_string()}"

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        insight = response.choices[0].message.content

        st.subheader("🤖 AI-Powered Insights")
        st.text_area("Insights", insight, height=300)

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")