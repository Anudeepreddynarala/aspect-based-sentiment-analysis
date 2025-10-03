"""
Main script to run aspect-based sentiment analysis on all review datasets.
"""

import pandas as pd
import os
from src.pipeline import ABSAPipeline
from datetime import datetime


def main():
    # Initialize pipeline
    print("=" * 80)
    print("ASPECT-BASED SENTIMENT ANALYSIS PIPELINE")
    print("=" * 80)
    print()

    pipeline = ABSAPipeline()

    # Input files
    data_dir = "/workspace/data"
    output_dir = "/workspace/output"
    os.makedirs(output_dir, exist_ok=True)

    datasets = [
        "doordash_customer_reviews.csv",
        "ubereats_customer_reviews.csv",
        "grubhub_customer_reviews.csv"
    ]

    all_results = []

    for dataset_file in datasets:
        dataset_path = os.path.join(data_dir, dataset_file)
        platform = dataset_file.replace("_customer_reviews.csv", "")

        print(f"\nProcessing {platform.upper()} reviews...")
        print("-" * 80)

        # Load data
        df = pd.read_csv(dataset_path)
        print(f"Loaded {len(df)} reviews from {dataset_file}")

        # Add platform column
        df['platform'] = platform

        # Process reviews
        results_df = pipeline.process_dataframe(
            df,
            review_column="review",
            batch_size=500,
            save_checkpoints=True,
            checkpoint_path=os.path.join(output_dir, f"{platform}_checkpoint.csv")
        )

        all_results.append(results_df)

        # Save individual platform results
        output_path = os.path.join(output_dir, f"{platform}_analysis.csv")
        results_df.to_csv(output_path, index=False)
        print(f"\nSaved {platform} results to {output_path}")

    # Combine all results
    print("\n" + "=" * 80)
    print("COMBINING ALL RESULTS")
    print("=" * 80)

    combined_df = pd.concat(all_results, ignore_index=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_output = os.path.join(output_dir, f"complete_analysis_{timestamp}.csv")
    combined_df.to_csv(final_output, index=False)

    print(f"\nFinal results saved to: {final_output}")
    print(f"Total reviews analyzed: {len(combined_df['review_id'].unique())}")
    print(f"Total aspect-sentiment pairs: {len(combined_df)}")

    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print(combined_df.groupby(['platform', 'sentiment']).size().unstack(fill_value=0))
    print()
    print("Top subcategories:")
    print(combined_df['subcategory'].value_counts().head(10))


if __name__ == "__main__":
    main()
