"""
Utility functions for the sentiment analysis pipeline
"""

import pandas as pd
import torch
from typing import Dict, List
import json
from pathlib import Path


def print_gpu_stats():
    """Print current GPU memory statistics."""
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated() / 1e9
        reserved = torch.cuda.memory_reserved() / 1e9
        total = torch.cuda.get_device_properties(0).total_memory / 1e9

        print(f"\nGPU Memory:")
        print(f"  Allocated: {allocated:.2f} GB")
        print(f"  Reserved:  {reserved:.2f} GB")
        print(f"  Total:     {total:.2f} GB")
        print(f"  Free:      {total - allocated:.2f} GB")
    else:
        print("\nNo GPU available")


def analyze_results(df: pd.DataFrame) -> Dict:
    """
    Analyze the results and generate statistics.

    Args:
        df: DataFrame with analysis results

    Returns:
        Dictionary with statistics
    """
    stats = {}

    # Basic stats
    stats['total_reviews'] = len(df)
    stats['platforms'] = df['source'].value_counts().to_dict()
    stats['avg_rating'] = df['rating'].mean()

    # Sentiment stats
    sentiment_cols = [col for col in df.columns if 'sentiment' in col.lower()]
    for col in sentiment_cols:
        aspect = col.replace(' sentiment', '').replace('sentiment', '')
        stats[f'{aspect}_avg_sentiment'] = df[col].mean()

        # Count positive, neutral, negative
        positive = (df[col] > 0.3).sum()
        neutral = ((df[col] >= -0.3) & (df[col] <= 0.3)).sum()
        negative = (df[col] < -0.3).sum()

        stats[f'{aspect}_positive'] = positive
        stats[f'{aspect}_neutral'] = neutral
        stats[f'{aspect}_negative'] = negative

    return stats


def print_sample_results(df: pd.DataFrame, n: int = 3):
    """
    Print sample results from the analysis.

    Args:
        df: DataFrame with results
        n: Number of samples to print
    """
    print("\n" + "="*80)
    print(f"SAMPLE RESULTS (showing {n} reviews)")
    print("="*80 + "\n")

    for i in range(min(n, len(df))):
        row = df.iloc[i]

        print(f"Review #{i+1}")
        print("-" * 80)
        print(f"ID: {row['id']}")
        print(f"Source: {row['source']} | App Type: {row['app_type']}")
        print(f"Rating: {row['rating']}/5 | Date: {row['timestamp']}")
        print(f"\nComment: {row['comment'][:200]}..." if len(row['comment']) > 200 else f"\nComment: {row['comment']}")

        print(f"\nSentiment Scores:")
        for aspect in ['Food', 'Delivery', 'Service', 'Price', 'Interface', 'Overall']:
            score = row[f'{aspect} sentiment']
            sentiment_label = "Positive" if score > 0.3 else ("Negative" if score < -0.3 else "Neutral")
            print(f"  {aspect:12} : {score:+.3f} ({sentiment_label})")

        print(f"\nSubcategories:")
        for aspect in ['food', 'delivery', 'service', 'price', 'interface', 'overall']:
            subcats = row[f'{aspect} subcategories']
            print(f"  {aspect.capitalize():12} : {subcats if subcats else '(none)'}")

        print(f"\nJTBD Statement:")
        print(f"  {row['JTBD statements']}")

        print("\n")


def save_statistics(stats: Dict, output_path: str = './output/statistics.json'):
    """
    Save statistics to a JSON file.

    Args:
        stats: Statistics dictionary
        output_path: Output file path
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"✓ Statistics saved to: {output_path}")


def create_summary_report(df: pd.DataFrame, output_path: str = './output/summary_report.txt'):
    """
    Create a text summary report.

    Args:
        df: DataFrame with results
        output_path: Output file path
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write("="*80 + "\n")
        f.write("SENTIMENT ANALYSIS SUMMARY REPORT\n")
        f.write("="*80 + "\n\n")

        # Basic stats
        f.write(f"Total Reviews Analyzed: {len(df)}\n")
        f.write(f"Average Rating: {df['rating'].mean():.2f}/5\n\n")

        # Platform breakdown
        f.write("Reviews by Platform:\n")
        for platform, count in df['source'].value_counts().items():
            f.write(f"  {platform}: {count} ({count/len(df)*100:.1f}%)\n")

        f.write("\n" + "-"*80 + "\n\n")

        # Sentiment breakdown by aspect
        aspects = ['Food', 'Delivery', 'Service', 'Price', 'Interface', 'Overall']
        for aspect in aspects:
            col = f'{aspect} sentiment'
            if col in df.columns:
                avg_sentiment = df[col].mean()
                positive = (df[col] > 0.3).sum()
                neutral = ((df[col] >= -0.3) & (df[col] <= 0.3)).sum()
                negative = (df[col] < -0.3).sum()

                f.write(f"{aspect} Sentiment:\n")
                f.write(f"  Average Score: {avg_sentiment:+.3f}\n")
                f.write(f"  Positive: {positive} ({positive/len(df)*100:.1f}%)\n")
                f.write(f"  Neutral:  {neutral} ({neutral/len(df)*100:.1f}%)\n")
                f.write(f"  Negative: {negative} ({negative/len(df)*100:.1f}%)\n\n")

        f.write("="*80 + "\n")

    print(f"✓ Summary report saved to: {output_path}")


def validate_output(df: pd.DataFrame) -> bool:
    """
    Validate the output DataFrame has all required columns.

    Args:
        df: Output DataFrame

    Returns:
        True if valid, raises ValueError otherwise
    """
    required_columns = [
        'id', 'source', 'app_type', 'timestamp', 'comment', 'rating',
        'Food sentiment', 'Delivery sentiment', 'Service sentiment',
        'Price sentiment', 'Interface sentiment', 'Overall sentiment',
        'food subcategories', 'delivery subcategories', 'service subcategories',
        'price subcategories', 'interface subcategories', 'overall subcategories',
        'JTBD statements'
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    print("✓ Output validation passed")
    return True


if __name__ == "__main__":
    print("Utility functions loaded")
    print_gpu_stats()
