"""
Sentiment analysis using FABSA RoBERTa model.
Analyzes sentiment for specific aspects in food delivery reviews.
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict, List


class SentimentAnalyzer:
    """Analyze sentiment for specific aspects using FABSA RoBERTa model."""

    ASPECT_MAPPING = {
        "food": "food",
        "delivery": "delivery",
        "service": "service",
        "price": "price",
        "interface": "interface",
        "overall": "overall"
    }

    SENTIMENT_LABELS = {
        0: "negative",
        1: "neutral",
        2: "positive"
    }

    def __init__(self, model_path: str = "Anudeep-Narala/fabsa-roberta-sentiment"):
        """Initialize sentiment analyzer with RoBERTa model."""
        print(f"Loading sentiment model from {model_path}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)

        # Move to GPU if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()
        print(f"Model loaded on {self.device}")

    def analyze_sentiment(self, review_text: str, aspect: str) -> Dict[str, any]:
        """
        Analyze sentiment for a specific aspect in the review.

        Args:
            review_text: The review text
            aspect: The parent aspect (food, delivery, service, price, interface, overall)

        Returns:
            Dict with sentiment label and confidence score
        """
        # Format input as expected by the model
        input_text = f"{review_text} [SEP] {aspect}"

        # Tokenize
        inputs = self.tokenizer(
            input_text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        # Get prediction
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=-1)
            predicted_class = torch.argmax(probs, dim=-1).item()
            confidence = probs[0][predicted_class].item()

        return {
            "sentiment": self.SENTIMENT_LABELS[predicted_class],
            "confidence": round(confidence, 4)
        }

    def analyze_multiple_aspects(
        self,
        review_text: str,
        aspects: List[str]
    ) -> Dict[str, Dict[str, any]]:
        """
        Analyze sentiment for multiple aspects in a single review.

        Args:
            review_text: The review text
            aspects: List of parent aspects to analyze

        Returns:
            Dict mapping each aspect to its sentiment result
        """
        results = {}
        for aspect in aspects:
            results[aspect] = self.analyze_sentiment(review_text, aspect)

        return results


if __name__ == "__main__":
    # Test the sentiment analyzer
    analyzer = SentimentAnalyzer()

    test_cases = [
        ("The pizza was cold and soggy", "food"),
        ("Driver arrived quickly and was very polite", "delivery"),
        ("App kept crashing during checkout", "interface"),
    ]

    for review, aspect in test_cases:
        result = analyzer.analyze_sentiment(review, aspect)
        print(f"\nReview: {review}")
        print(f"Aspect: {aspect}")
        print(f"Result: {result}")
