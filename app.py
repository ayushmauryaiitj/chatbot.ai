import streamlit as st
from backend import recommend_schemes
from utils import translate_text

# Config
st.set_page_config(page_title="SchemeSetu AI", layout="wide")

# Sidebar
st.sidebar.title("⚙️ Settings")
theme = st.sidebar.selectbox("Theme", ["Light", "Dark"])
lang = st.sidebar.selectbox("Language", ["English", "Hindi"])

# Theme
if theme == "Dark":
    st.markdown("""
        <style>
        body { background-color: #0E1117; color: white; }
        .stTextInput input { background-color: #1E1E1E; color: white; }
        </style>
    """, unsafe_allow_html=True)

# Header
st.title("🇮🇳 SchemeSetu AI")
st.caption("Your Smart Government Scheme Assistant")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
user_input = st.chat_input("Type your query...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = recommend_schemes(user_input)
            response = translate_text(response, lang)

            st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
