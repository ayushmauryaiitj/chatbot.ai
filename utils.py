import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_openai_client() -> OpenAI | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        client = OpenAI(api_key=api_key)
        return client
    except Exception:
        return None


def translate_text(text: str, lang: str) -> str:
    """
    Translate text between English and Hindi.
    - If lang == "English": returns English text.
    - If lang == "Hindi": attempts translation to Hindi using OpenAI.
    - If translation fails or API not available: returns original text.
    """
    if not text:
        return ""

    if lang == "English":
        return text

    # Only Hindi is supported as second language
    if lang != "Hindi":
        return text

    client = get_openai_client()
    if client is None:
        # Fallback: return original text without failing
        return text

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a translation assistant. Translate the user message into Hindi. Keep formatting, bullet points, and structure.",
                },
                {"role": "user", "content": text},
            ],
            temperature=0.2,
            max_tokens=800,
        )
        translated = completion.choices[0].message.content
        return translated or text
    except Exception:
        # On any error, just return the original text
        return text
