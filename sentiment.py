from transformers import pipeline

# Load sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_sentiments(all_reviews_text):
    """Split reviews and analyze each one."""
    reviews = all_reviews_text.strip().split('\n\n')  # split numbered reviews
    results = []

    for review in reviews:
        review_clean = review.strip()
        if review_clean:
            result = sentiment_pipeline(review_clean[:512])[0]  # limit to 512 tokens
            label = result["label"]
            score = result["score"]

            # Style output
            if label == "POSITIVE":
                sentiment = f"✅ **Positive** ({score:.2f})"
            elif label == "NEGATIVE":
                sentiment = f"❌ **Negative** ({score:.2f})"
            else:
                sentiment = f"⚪️ **Neutral** ({score:.2f})"

            formatted = f"> {review_clean}\n\n**Sentiment:** {sentiment}"
            results.append(formatted)

    return "\n\n---\n\n".join(results)
