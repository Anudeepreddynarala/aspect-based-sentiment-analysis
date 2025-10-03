"""
Complete aspect-based sentiment analysis pipeline.
Combines aspect extraction (LLM) and sentiment analysis (RoBERTa).
"""

import pandas as pd
from typing import Dict, List
from src.aspect_extraction import AspectExtractor
from src.sentiment_analyzer import SentimentAnalyzer
import time


class ABSAPipeline:
    """Complete pipeline for aspect-based sentiment analysis."""

    def __init__(
        self,
        aspect_extractor: AspectExtractor = None,
        sentiment_analyzer: SentimentAnalyzer = None
    ):
        """Initialize pipeline with aspect extractor and sentiment analyzer."""
        self.aspect_extractor = aspect_extractor or AspectExtractor()
        self.sentiment_analyzer = sentiment_analyzer or SentimentAnalyzer()

    def process_review(self, review_text: str) -> Dict:
        """
        Process a single review through the complete pipeline.

        Args:
            review_text: The review text to analyze

        Returns:
            Dict with subcategories and their sentiments
        """
        # Step 1: Extract subcategories using LLM
        subcategories = self.aspect_extractor.extract_aspects(review_text)

        # Step 2: Get parent aspects for sentiment analysis
        parent_aspects = {}
        for subcat in subcategories:
            parent = self.aspect_extractor.get_parent_aspect(subcat)
            if parent not in parent_aspects:
                parent_aspects[parent] = []
            parent_aspects[parent].append(subcat)

        # Step 3: Analyze sentiment for each parent aspect
        results = {}
        for parent_aspect, subcats in parent_aspects.items():
            sentiment_result = self.sentiment_analyzer.analyze_sentiment(
                review_text,
                parent_aspect
            )

            # Assign same sentiment to all subcategories under this parent
            for subcat in subcats:
                results[subcat] = {
                    "sentiment": sentiment_result["sentiment"],
                    "confidence": sentiment_result["confidence"],
                    "parent_aspect": parent_aspect
                }

        return results

    def process_dataframe(
        self,
        df: pd.DataFrame,
        review_column: str = "review",
        batch_size: int = 100,
        save_checkpoints: bool = True,
        checkpoint_path: str = "/workspace/output/checkpoint.csv"
    ) -> pd.DataFrame:
        """
        Process multiple reviews from a DataFrame.

        Args:
            df: DataFrame with reviews
            review_column: Name of the column containing review text
            batch_size: Number of reviews to process before saving checkpoint
            save_checkpoints: Whether to save progress checkpoints
            checkpoint_path: Path to save checkpoints

        Returns:
            DataFrame with analysis results
        """
        results = []

        for idx, row in df.iterrows():
            start_time = time.time()

            review_text = row[review_column]
            review_id = row.get('id', idx)

            # Process review
            analysis = self.process_review(review_text)

            # Format results
            for subcategory, data in analysis.items():
                results.append({
                    "review_id": review_id,
                    "review_text": review_text,
                    "subcategory": subcategory,
                    "parent_aspect": data["parent_aspect"],
                    "sentiment": data["sentiment"],
                    "confidence": data["confidence"],
                    **{k: v for k, v in row.items() if k != review_column}
                })

            elapsed = time.time() - start_time

            if (idx + 1) % 10 == 0:
                print(f"Processed {idx + 1}/{len(df)} reviews ({elapsed:.2f}s per review)")

            # Save checkpoint
            if save_checkpoints and (idx + 1) % batch_size == 0:
                checkpoint_df = pd.DataFrame(results)
                checkpoint_df.to_csv(checkpoint_path.replace(".csv", f"_{idx+1}.csv"), index=False)
                print(f"Checkpoint saved at {idx + 1} reviews")

        return pd.DataFrame(results)


if __name__ == "__main__":
    # Test the complete pipeline
    print("Initializing pipeline...")
    pipeline = ABSAPipeline()

    test_reviews = [
        "The pizza arrived cold and the cheese was congealed. Driver was rude too.",
        "Amazing food, hot and delicious! Delivery was super fast.",
        "App is terrible, kept crashing. But the food was worth it.",
    ]

    print("\nProcessing test reviews...\n")
    for i, review in enumerate(test_reviews, 1):
        print(f"Review {i}: {review}")
        results = pipeline.process_review(review)

        for subcategory, data in results.items():
            print(f"  - {subcategory} ({data['parent_aspect']}): {data['sentiment']} ({data['confidence']:.2%})")
        print()
