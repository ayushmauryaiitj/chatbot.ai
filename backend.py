import json
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

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
    Suggest best government schemes.

    User: {user_input}

    Schemes:
    {context}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content']
