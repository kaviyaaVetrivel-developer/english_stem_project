import streamlit as st
import requests

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="NLP Terminology Generator",
    layout="centered"
)

# -------------------------
# Professional CSS Styling
# -------------------------
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: 700;
        color: #1f4e79;
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        font-size: 16px;
        color: #555;
        margin-bottom: 30px;
    }
    .card {
        background-color: #ffffff;
        padding: 22px;
        border-radius: 12px;
        border: 1px solid #e6e6e6;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .pos-badge {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        color: white;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------
st.markdown("<div class='main-title'>📖 NLP Terminology Generator</div>", unsafe_allow_html=True)

st.markdown("<div class='subtitle'>Word definitions, part of speech, and lexical relations</div>", unsafe_allow_html=True)

# -------------------------
# Input
# -------------------------
with st.form("word_form"):
    term = st.text_input("Enter a word", placeholder="Example: language")
    submit = st.form_submit_button("Generate 🚀")

if submit:
    if term.strip() == "":
        st.warning("Please enter a word.")
    else:
        with st.spinner("Processing..."):

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/generate",
                    json={"word": term}
                )

                if response.status_code == 200:
                    result = response.json()

                    st.success(f"Results for '{result['word']}'")

                    # Pronunciation
                    st.markdown(f"**Pronunciation:** {result['pronunciation']}")
                    st.markdown("---")

                    for item in result["terminology"]:

                        pos = item["part_of_speech"]

                        color_map = {
                            "Noun": "#2e7d32",
                            "Verb": "#1565c0",
                            "Adjective": "#ef6c00",
                            "Adverb": "#6a1b9a"
                        }

                        color = color_map.get(pos, "#424242")

                        # Card Layout
                        st.markdown(
                            f"""
                            <div class="card">
                                <span class="pos-badge" style="background-color:{color};">
                                    {pos}
                                </span>
                                <div style="margin-top:12px;">
                                    <strong>Definition:</strong> {item['definition']}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        # Examples
                        if item["examples"]:
                            st.markdown("**Examples**")
                            for ex in item["examples"]:
                                st.markdown(f"- {ex}")

                        # Synonyms
                        if item["synonyms"]:
                            st.markdown("**Synonyms**")
                            st.markdown(", ".join(item["synonyms"]))

                        # Hypernyms
                        if item["hypernyms"]:
                            st.markdown("**Broader Terms**")
                            for h in item["hypernyms"]:
                                st.markdown(f"• {h}")

                        # Hyponyms
                        if item["hyponyms"]:
                            st.markdown("**Narrower Terms**")
                            for h in item["hyponyms"]:
                                st.markdown(f"• {h}")

                        st.markdown("---")

                else:
                    st.error("Backend error. Ensure the FastAPI server is running.")

            except:
                st.error("Unable to connect to backend. Start the FastAPI server.")
