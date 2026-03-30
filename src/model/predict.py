from src.llm.llm_engine import get_llm_response

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


def predict_all(text: str):
    return get_llm_response(text)
