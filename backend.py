import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_schemes():
    with open("data/schemes.json", "r") as f:
        return json.load(f)

def recommend_schemes(user_input):
    schemes = load_schemes()

    context = "\n".join([
        f"{s['name']} - {s['eligibility']} - {s['benefit']}"
        for s in schemes
    ])

    prompt = f"""
    You are a helpful Indian government schemes assistant.

    User Input:
    {user_input}

    Available Schemes:
    {context}

    Suggest best schemes with reasons in simple language.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
