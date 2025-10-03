"""
Aspect-Based Sentiment Analysis using fabsa-roberta-sentiment model
Analyzes customer reviews across 6 aspects: food, delivery, service, price, interface, overall
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
from tqdm import tqdm
from typing import List, Dict
import os

class AspectSentimentAnalyzer:
    """
    Performs aspect-based sentiment analysis on food delivery reviews.
    Uses the Anudeep-Narala/fabsa-roberta-sentiment model for multi-aspect sentiment extraction.
    """

    def __init__(self, model_name: str = "Anudeep-Narala/fabsa-roberta-sentiment", device: str = None):
        """
        Initialize the sentiment analyzer with GPU support.

        Args:
            model_name: HuggingFace model identifier
            device: Device to use ('cuda' or 'cpu'). Auto-detects if None.
        """
        self.model_name = model_name
        self.device = device if device else ('cuda' if torch.cuda.is_available() else 'cpu')

        print(f"Loading sentiment analysis model on {self.device}...")
        print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'}")

        # Define the 6 aspects we're analyzing
        self.aspects = ['food', 'delivery', 'service', 'price', 'interface', 'overall']

        # Load model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir='./models'
        )

        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            cache_dir='./models'
        ).to(self.device)

        # Set to evaluation mode
        self.model.eval()

        # Enable mixed precision for faster inference
        self.use_fp16 = self.device == 'cuda'
        if self.use_fp16:
            self.model = self.model.half()
            print("Mixed precision (FP16) enabled for faster inference")

        print(f"Model loaded successfully!")

    def analyze_single_review(self, review_text: str) -> Dict[str, float]:
        """
        Analyze a single review and extract sentiment scores for all aspects.

        Args:
            review_text: The review text to analyze

        Returns:
            Dictionary with aspect names as keys and sentiment scores as values
        """
        results = {}

        with torch.no_grad():
            for aspect in self.aspects:
                # Create input with aspect specification
                # Format: "[CLS] review [SEP] aspect [SEP]"
                input_text = f"{review_text} [SEP] {aspect}"

                # Tokenize
                inputs = self.tokenizer(
                    input_text,
                    return_tensors='pt',
                    truncation=True,
                    max_length=512,
                    padding=True
                ).to(self.device)

                # Get predictions
                outputs = self.model(**inputs)
                logits = outputs.logits

                # Apply softmax to get probabilities
                probs = torch.nn.functional.softmax(logits, dim=-1)

                # Get sentiment score (assuming 3-class: negative=0, neutral=1, positive=2)
                # Convert to sentiment score: negative=-1, neutral=0, positive=1
                sentiment_idx = torch.argmax(probs, dim=-1).item()

                if sentiment_idx == 0:  # Negative
                    sentiment_score = -probs[0][0].item()
                elif sentiment_idx == 1:  # Neutral
                    sentiment_score = 0.0
                else:  # Positive
                    sentiment_score = probs[0][2].item()

                results[aspect] = sentiment_score

        return results

    def analyze_batch(self, reviews: List[str], batch_size: int = 16) -> List[Dict[str, float]]:
        """
        Analyze multiple reviews in batches for efficiency.

        Args:
            reviews: List of review texts
            batch_size: Number of reviews to process at once

        Returns:
            List of dictionaries with sentiment scores for each review
        """
        all_results = []

        print(f"Analyzing {len(reviews)} reviews in batches of {batch_size}...")

        for i in tqdm(range(0, len(reviews), batch_size)):
            batch = reviews[i:i + batch_size]

            for review in batch:
                try:
                    result = self.analyze_single_review(review)
                    all_results.append(result)
                except Exception as e:
                    print(f"Error processing review: {str(e)}")
                    # Return neutral scores if there's an error
                    all_results.append({aspect: 0.0 for aspect in self.aspects})

        return all_results

    def process_dataframe(self, df: pd.DataFrame, text_column: str = 'review',
                         batch_size: int = 16) -> pd.DataFrame:
        """
        Process a pandas DataFrame containing reviews.

        Args:
            df: DataFrame with reviews
            text_column: Name of the column containing review text
            batch_size: Batch size for processing

        Returns:
            DataFrame with added sentiment columns for each aspect
        """
        print(f"\nProcessing {len(df)} reviews from DataFrame...")

        # Extract reviews
        reviews = df[text_column].fillna("").astype(str).tolist()

        # Analyze all reviews
        results = self.analyze_batch(reviews, batch_size=batch_size)

        # Add results to dataframe
        for aspect in self.aspects:
            column_name = f'{aspect.capitalize()} sentiment'
            df[column_name] = [r[aspect] for r in results]

        print(f"✓ Sentiment analysis complete!")
        print(f"  Added columns: {', '.join([f'{a.capitalize()} sentiment' for a in self.aspects])}")

        return df

    def clear_cache(self):
        """Clear GPU cache to free memory."""
        if self.device == 'cuda':
            torch.cuda.empty_cache()


def main():
    """Test the sentiment analyzer with sample data."""

    # Initialize analyzer
    analyzer = AspectSentimentAnalyzer()

    # Test with a sample review
    test_review = "The food was amazing and fresh, but delivery took forever and the driver was rude. The app is easy to use though."

    print("\n" + "="*80)
    print("TESTING SENTIMENT ANALYZER")
    print("="*80)
    print(f"\nReview: {test_review}\n")

    results = analyzer.analyze_single_review(test_review)

    print("Sentiment Scores:")
    for aspect, score in results.items():
        sentiment = "Positive" if score > 0.3 else ("Negative" if score < -0.3 else "Neutral")
        print(f"  {aspect.capitalize():12} : {score:+.3f} ({sentiment})")

    # Clean up
    analyzer.clear_cache()

    print("\n✓ Test complete!")


if __name__ == "__main__":
    main()
