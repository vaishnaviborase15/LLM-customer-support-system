import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def parse_llm_output(result: str):
    sentiment = "Neutral"
    priority = "Medium"
    response = "Our support team will assist you shortly."

    try:
        lines = result.split("\n")

        for line in lines:
            line = line.strip()

            if line.lower().startswith("sentiment"):
                sentiment = line.split(":")[-1].strip()

            elif line.lower().startswith("priority"):
                priority = line.split(":")[-1].strip()

            elif line.lower().startswith("response"):
                response = line.split(":", 1)[-1].strip()

    except Exception as e:
        print("Parsing Error:", e)

    return sentiment, priority, response


def get_llm_response(user_query: str):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ latest working
            messages=[
                {"role": "system", "content": "You are a professional customer support assistant."},
                {"role": "user", "content": f"""
You are a highly professional and empathetic AI customer support assistant.

Analyze the query and respond in format:

Sentiment: <Positive/Neutral/Negative>
Priority: <Low/Medium/High/Critical>
Response: <Detailed helpful response (2-4 sentences)>

Query: {user_query}
"""}
            ],
            temperature=0.7,
            max_tokens=400
        )

        result = completion.choices[0].message.content

        print("RAW RESPONSE:\n", result)

        return parse_llm_output(result)

    except Exception as e:
        import traceback
        print("Groq Error:", str(e))
        traceback.print_exc()

        return "Neutral", "Medium", "Our support team will assist you shortly."