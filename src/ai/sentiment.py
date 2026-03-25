from textblob import TextBlob

def get_sentiment(text):
    text = str(text)  # ✅ FIX

    if not text.strip():
        return "neutral"

    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0:
        return "positive"
    elif polarity == 0:
        return "neutral"
    else:
        return "negative"


def apply_sentiment(df):
    df['sentiment'] = df['clean_text'].apply(get_sentiment)
    return df