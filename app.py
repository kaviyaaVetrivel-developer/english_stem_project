import streamlit as st
import requests

st.title("NLP Terminology Generator")

term = st.text_input("Enter a word")

if st.button("Generate"):
    response = requests.post(
        "http://127.0.0.1:8000/generate",
        json={"word": term}   # IMPORTANT: use "word"
    )

    if response.status_code == 200:
        result = response.json()

        st.subheader(f"Results for: {result['word']}")

        for item in result["terminology"]:
            st.write("Definition:", item["definition"])
            st.write("Examples:", item["examples"])
            st.write("Synonyms:", item["synonyms"])
            st.write("Hypernyms:", item["hypernyms"])
            st.write("Hyponyms:", item["hyponyms"])
            st.write("---")
    else:
        st.error("Backend error")

