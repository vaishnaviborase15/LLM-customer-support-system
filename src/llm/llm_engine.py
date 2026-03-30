import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_llm_response(user_query: str):
    try:
        prompt = f"""
You are a professional AI customer support assistant.

Your tasks:
- Detect sentiment (Positive / Neutral / Negative)
- Assign priority (Low / Medium / High / Critical)
- Generate a polite, helpful, human-like response

Guidelines:
- If user is angry → Apologize
- If issue is serious → Mark High/Critical
- Always give clear next steps

User Query:
{user_query}

Output STRICTLY in this format:
Sentiment: <value>
Priority: <value>
Response: <your response>
"""

        completion = client.chat.completions.create(
            model="llama3-8b-8192",  
            messages=[
                {"role": "system", "content": "You are a helpful customer support assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=120
        )

        result = completion.choices[0].message.content

        return parse_llm_output(result)

    except Exception as e:
        print("Groq Error:", e)
        return "Neutral", "Medium", "Our support team will assist you shortly."