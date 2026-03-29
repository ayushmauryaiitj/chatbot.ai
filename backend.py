import json
import os
from typing import List, Dict

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # Load OPENAI_API_KEY if present

# Initialize OpenAI client safely
def get_openai_client() -> OpenAI | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        client = OpenAI(api_key=api_key)
        return client
    except Exception:
        return None


def load_schemes() -> List[Dict]:
    """
    Load schemes from data/schemes.json with safe error handling.
    Returns an empty list if file is missing or invalid.
    """
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_dir, "data", "schemes.json")

        if not os.path.exists(data_path):
            return []

        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception:
        return []


def build_prompt(user_input: str, schemes: List[Dict]) -> str:
    """
    Build a concise prompt for the model using the schemes database.
    """
    if not schemes:
        context = "No structured scheme data is currently available."
    else:
        lines = []
        for s in schemes:
            name = s.get("name", "Unknown scheme")
            eligibility = s.get("eligibility", "Eligibility not specified")
            benefit = s.get("benefit", "Benefit not specified")
            category = s.get("category", "General")
            lines.append(
                f"Name: {name}; Category: {category}; Eligibility: {eligibility}; Benefit: {benefit}"
            )
        context = "\n".join(lines)

    prompt = f"""
You are SchemeSetu AI, an assistant that recommends Indian government schemes.

User query:
{user_input}

Available schemes:
{context}

Instructions:
- Recommend 1–3 most relevant schemes.
- Briefly explain why each scheme is suitable.
- Use clear bullet points.
- If no scheme clearly matches, say so and give a generic, helpful suggestion.
"""
    return prompt.strip()


def recommend_schemes(user_input: str) -> str:
    """
    Recommend schemes for a user query.
    - Uses OpenAI if available.
    - Falls back to a simple rule-based response if API is unavailable or fails.
    """
    schemes = load_schemes()
    prompt = build_prompt(user_input, schemes)

    client = get_openai_client()
    if client is None:
        # Fallback when API key missing or client not initialized
        return fallback_recommendation(user_input, schemes)

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=600,
        )
        content = completion.choices[0].message.content
        return content or fallback_recommendation(user_input, schemes)
    except Exception:
        # Any API error → fallback
        return fallback_recommendation(user_input, schemes)


def fallback_recommendation(user_input: str, schemes: List[Dict]) -> str:
    """
    Simple deterministic fallback if the OpenAI API is not available.
    Uses keyword matching over categories and names.
    """
    if not schemes:
        return (
            "Service temporarily unavailable. "
            "Scheme database is not accessible right now. "
            "Please try again later."
        )

    text = user_input.lower()
    matches = []

    for s in schemes:
        name = s.get("name", "").lower()
        category = s.get("category", "").lower()
        eligibility = s.get("eligibility", "").lower()

        score = 0
        # Very naive keyword scoring
        keywords = [
            "farmer",
            "kisan",
            "agriculture",
            "health",
            "hospital",
            "insurance",
            "house",
            "housing",
            "ghar",
            "awas",
            "poor",
            "low income",
            "hospitalization",
        ]

        for kw in keywords:
            if kw in text and kw in (name + " " + category + " " + eligibility):
                score += 1

        if score > 0:
            matches.append((score, s))

    matches.sort(key=lambda x: x[0], reverse=True)
    top = [m[1] for m in matches[:3]]

    if not top:
        # Generic response if nothing matched
        return (
            "Service temporarily unavailable, showing basic suggestions.\n\n"
            "Based on your query, you may be eligible for central or state government schemes. "
            "Please visit your nearest CSC center or official government portal (such as pmindia.gov.in or "
            "the relevant ministry website) for detailed, up-to-date information."
        )

    lines = ["Service temporarily unavailable, showing basic suggestions.\n"]
    lines.append("Here are some schemes that may be relevant:")

    for s in top:
        lines.append(
            f"- **{s.get('name', 'Unknown')}**: {s.get('benefit', '')} "
            f"(Eligibility: {s.get('eligibility', 'Not specified')})"
        )

    return "\n".join(lines)
