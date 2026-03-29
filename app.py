import streamlit as st

from backend import recommend_schemes
from utils import translate_text

# ---------- Page config ----------
st.set_page_config(page_title="SchemeSetu AI", layout="wide")

# ---------- Sidebar settings ----------
st.sidebar.title("⚙️ Settings")

theme = st.sidebar.selectbox("Theme", ["Light", "Dark"], index=0)
lang = st.sidebar.selectbox("Language", ["English", "Hindi"], index=0)

# ---------- Theme handling (simple) ----------
# Streamlit theming is usually managed via .streamlit/config.toml,
# but a minimal CSS tweak is added here for the Dark option.
if theme == "Dark":
    st.markdown(
        """
        <style>
        body {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        .stTextInput > div > div > input {
            background-color: #1E1E1E;
            color: #FAFAFA;
        }
        .stChatMessage {
            color: #FAFAFA;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---------- Header ----------
st.title("🇮🇳 SchemeSetu AI")
st.caption("Your Smart Government Scheme Assistant")

# ---------- Session state for chat ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- Render existing chat history ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- Chat input ----------
user_input = st.chat_input("Type your query...")

if user_input:
    # Store and render user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                raw_response = recommend_schemes(user_input)
            except Exception:
                raw_response = (
                    "Service temporarily unavailable. "
                    "Please try again after some time."
                )

            # Translation (non-fatal)
            try:
                final_response = translate_text(raw_response, lang)
            except Exception:
                final_response = raw_response

            st.markdown(final_response)

    # Save assistant message to history
    st.session_state.messages.append(
        {"role": "assistant", "content": final_response}
    )
