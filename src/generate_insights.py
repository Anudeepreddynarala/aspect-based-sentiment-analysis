"""
Generate visual insights and summary statistics from analysis results.
Creates markdown-friendly tables and statistics for portfolio presentation.
"""

import pandas as pd
import sys


def generate_insights(csv_path: str):
    """Generate business insights from analysis results."""

    print("=" * 80)
    print("BUSINESS INSIGHTS GENERATOR")
    print("=" * 80)
    print()

    # Load data
    df = pd.read_csv(csv_path)

    print(f"📊 Loaded {len(df)} aspect-sentiment pairs from {df['review_id'].nunique()} reviews\n")

    # Overall Statistics
    print("## OVERALL STATISTICS")
    print("-" * 80)
    print(f"Total Reviews Analyzed: {df['review_id'].nunique():,}")
    print(f"Total Aspect-Sentiment Pairs: {len(df):,}")
    print(f"Unique Subcategories: {df['subcategory'].nunique()}")
    print(f"Platforms: {', '.join(df['platform'].unique())}")
    print()

    # Sentiment Distribution
    print("## SENTIMENT DISTRIBUTION")
    print("-" * 80)
    sentiment_counts = df['sentiment'].value_counts()
    sentiment_pcts = df['sentiment'].value_counts(normalize=True) * 100

    print("| Sentiment | Count | Percentage |")
    print("|-----------|-------|------------|")
    for sentiment in ['negative', 'neutral', 'positive']:
        if sentiment in sentiment_counts:
            print(f"| {sentiment.capitalize():9} | {sentiment_counts[sentiment]:5,} | {sentiment_pcts[sentiment]:5.1f}% |")
    print()

    # Platform Comparison
    print("## PLATFORM COMPARISON")
    print("-" * 80)
    platform_sentiment = df.groupby(['platform', 'sentiment']).size().unstack(fill_value=0)
    platform_totals = platform_sentiment.sum(axis=1)
    platform_pcts = platform_sentiment.div(platform_totals, axis=0) * 100

    print("| Platform | Negative | Neutral | Positive | Total |")
    print("|----------|----------|---------|----------|-------|")
    for platform in ['doordash', 'ubereats', 'grubhub']:
        if platform in platform_sentiment.index:
            neg_pct = platform_pcts.loc[platform, 'negative']
            pos_pct = platform_pcts.loc[platform, 'positive']
            total = platform_totals[platform]
            print(f"| {platform.title():8} | {neg_pct:5.1f}% | {platform_pcts.loc[platform, 'neutral']:5.1f}% | {pos_pct:5.1f}% | {total:5,} |")
    print()

    # Top Subcategories by Volume
    print("## TOP 10 SUBCATEGORIES (BY VOLUME)")
    print("-" * 80)
    top_subcats = df['subcategory'].value_counts().head(10)

    print("| Rank | Subcategory | Mentions |")
    print("|------|-------------|----------|")
    for rank, (subcat, count) in enumerate(top_subcats.items(), 1):
        print(f"| {rank:4} | {subcat:30} | {count:6,} |")
    print()

    # Top Pain Points (Negative Sentiment)
    print("## TOP 10 PAIN POINTS (HIGHEST NEGATIVE SENTIMENT)")
    print("-" * 80)
    negative_df = df[df['sentiment'] == 'negative']
    pain_points = negative_df['subcategory'].value_counts().head(10)

    # Calculate negative percentage for each
    print("| Rank | Subcategory | Negative Mentions | Negative % |")
    print("|------|-------------|-------------------|------------|")
    for rank, (subcat, neg_count) in enumerate(pain_points.items(), 1):
        total_count = len(df[df['subcategory'] == subcat])
        neg_pct = (neg_count / total_count) * 100
        print(f"| {rank:4} | {subcat:30} | {neg_count:9,} | {neg_pct:7.1f}% |")
    print()

    # Positive Highlights
    print("## POSITIVE HIGHLIGHTS (HIGHEST POSITIVE SENTIMENT)")
    print("-" * 80)

    # Calculate positive percentage for each subcategory
    subcat_stats = []
    for subcat in df['subcategory'].unique():
        subcat_df = df[df['subcategory'] == subcat]
        total = len(subcat_df)
        positive = len(subcat_df[subcat_df['sentiment'] == 'positive'])

        if total >= 50:  # Only include subcategories with sufficient data
            pos_pct = (positive / total) * 100
            subcat_stats.append({
                'subcategory': subcat,
                'positive_count': positive,
                'total': total,
                'positive_pct': pos_pct
            })

    positive_df = pd.DataFrame(subcat_stats).sort_values('positive_pct', ascending=False).head(10)

    print("| Rank | Subcategory | Positive % | Positive/Total |")
    print("|------|-------------|------------|----------------|")
    for rank, row in enumerate(positive_df.itertuples(), 1):
        print(f"| {rank:4} | {row.subcategory:30} | {row.positive_pct:7.1f}% | {row.positive_count:4}/{row.total:4} |")
    print()

    # Platform-Specific Pain Points
    print("## PLATFORM-SPECIFIC TOP PAIN POINTS")
    print("-" * 80)

    for platform in ['doordash', 'ubereats', 'grubhub']:
        platform_df = df[df['platform'] == platform]
        platform_negatives = platform_df[platform_df['sentiment'] == 'negative']
        top_3 = platform_negatives['subcategory'].value_counts().head(3)

        print(f"\n### {platform.upper()}")
        print("| Rank | Pain Point | Mentions |")
        print("|------|------------|----------|")
        for rank, (subcat, count) in enumerate(top_3.items(), 1):
            print(f"| {rank:4} | {subcat:30} | {count:6,} |")

    print("\n" + "=" * 80)
    print("INSIGHTS GENERATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    csv_file = "/workspace/output/complete_analysis_20251003_234035.csv"

    if len(sys.argv) > 1:
        csv_file = sys.argv[1]

    generate_insights(csv_file)
