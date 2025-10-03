"""
Main Pipeline for Aspect-Based Sentiment Analysis
Orchestrates all processing steps: sentiment analysis, subcategory classification, and JTBD transformation
"""

import os
import sys
import pandas as pd
import torch
from datetime import datetime
from pathlib import Path

# Import our custom modules
from sentiment_analysis import AspectSentimentAnalyzer
from subcategory_classifier import SubcategoryClassifier
from jtbd_transformer import JTBDTransformer


class SentimentAnalysisPipeline:
    """
    Complete pipeline for processing food delivery reviews.
    Includes sentiment analysis, subcategory classification, and JTBD transformation.
    """

    def __init__(self, llm_provider: str = 'openai', llm_model: str = None):
        """
        Initialize the pipeline with all components.

        Args:
            llm_provider: 'openai' or 'anthropic' for advanced LLM tasks
            llm_model: Specific model name (optional)
        """
        self.llm_provider = llm_provider
        self.llm_model = llm_model

        print("="*80)
        print("INITIALIZING SENTIMENT ANALYSIS PIPELINE")
        print("="*80)

        # Check GPU availability
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        if self.device == 'cuda':
            print(f"✓ GPU Available: {torch.cuda.get_device_name(0)}")
            print(f"  Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        else:
            print("⚠ No GPU detected, using CPU (slower)")

        # Initialize components
        print("\n1. Loading Sentiment Analysis Model...")
        self.sentiment_analyzer = AspectSentimentAnalyzer()

        print("\n2. Initializing Subcategory Classifier...")
        try:
            self.subcategory_classifier = SubcategoryClassifier(
                provider=llm_provider,
                model=llm_model
            )
        except ValueError as e:
            print(f"⚠ Warning: {e}")
            self.subcategory_classifier = None

        print("\n3. Initializing JTBD Transformer...")
        try:
            self.jtbd_transformer = JTBDTransformer(
                provider=llm_provider,
                model=llm_model
            )
        except ValueError as e:
            print(f"⚠ Warning: {e}")
            self.jtbd_transformer = None

        print("\n" + "="*80)
        print("PIPELINE READY")
        print("="*80 + "\n")

    def load_data(self, file_paths: list) -> pd.DataFrame:
        """
        Load and combine all CSV files.

        Args:
            file_paths: List of CSV file paths

        Returns:
            Combined DataFrame
        """
        print(f"Loading data from {len(file_paths)} files...")

        dfs = []
        for file_path in file_paths:
            try:
                df = pd.read_csv(file_path)
                print(f"  ✓ Loaded {file_path}: {len(df)} reviews")
                dfs.append(df)
            except Exception as e:
                print(f"  ✗ Error loading {file_path}: {str(e)}")

        if not dfs:
            raise ValueError("No data loaded successfully")

        # Combine all dataframes
        combined_df = pd.concat(dfs, ignore_index=True)
        print(f"\n✓ Total reviews loaded: {len(combined_df)}")

        return combined_df

    def prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare and clean the data.

        Args:
            df: Input DataFrame

        Returns:
            Cleaned DataFrame with standardized columns
        """
        print("\nPreparing data...")

        # Rename 'date' to 'timestamp' and 'review' to 'comment'
        df = df.rename(columns={
            'date': 'timestamp',
            'review': 'comment'
        })

        # Ensure required columns exist
        required_columns = ['id', 'source', 'app_type', 'timestamp', 'comment', 'rating']
        for col in required_columns:
            if col not in df.columns:
                print(f"  ⚠ Warning: Missing column '{col}', adding empty column")
                df[col] = ''

        # Clean comment text
        df['comment'] = df['comment'].fillna("").astype(str)

        # Ensure rating is numeric
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(3).astype(int)

        print(f"✓ Data prepared: {len(df)} reviews")

        return df

    def run_sentiment_analysis(self, df: pd.DataFrame, batch_size: int = 32) -> pd.DataFrame:
        """
        Run aspect-based sentiment analysis.

        Args:
            df: Input DataFrame
            batch_size: Batch size for processing

        Returns:
            DataFrame with sentiment scores
        """
        print("\n" + "="*80)
        print("STEP 1: ASPECT-BASED SENTIMENT ANALYSIS")
        print("="*80)

        df = self.sentiment_analyzer.process_dataframe(
            df,
            text_column='comment',
            batch_size=batch_size
        )

        # Clear GPU cache
        self.sentiment_analyzer.clear_cache()

        return df

    def run_subcategory_classification(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Run subcategory classification.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with subcategory columns
        """
        print("\n" + "="*80)
        print("STEP 2: SUBCATEGORY CLASSIFICATION")
        print("="*80)

        if self.subcategory_classifier is None:
            print("⚠ Skipping: No API key provided")
            # Add empty subcategory columns
            for aspect in ['food', 'delivery', 'service', 'price', 'interface', 'overall']:
                df[f'{aspect} subcategories'] = ''
            return df

        df = self.subcategory_classifier.process_dataframe(
            df,
            text_column='comment'
        )

        return df

    def run_jtbd_transformation(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Run JTBD transformation.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with JTBD statements
        """
        print("\n" + "="*80)
        print("STEP 3: JOBS-TO-BE-DONE TRANSFORMATION")
        print("="*80)

        if self.jtbd_transformer is None:
            print("⚠ Skipping: No API key provided")
            df['JTBD statements'] = ''
            return df

        df = self.jtbd_transformer.process_dataframe(
            df,
            text_column='comment',
            rating_column='rating',
            platform_column='source'
        )

        return df

    def reorder_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Reorder columns to match the required output format.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with reordered columns
        """
        # Define the desired column order
        column_order = [
            'id',
            'source',
            'app_type',
            'timestamp',
            'comment',
            'rating',
            'Food sentiment',
            'Delivery sentiment',
            'Service sentiment',
            'Price sentiment',
            'Interface sentiment',
            'Overall sentiment',
            'food subcategories',
            'delivery subcategories',
            'service subcategories',
            'price subcategories',
            'interface subcategories',
            'overall subcategories',
            'JTBD statements'
        ]

        # Ensure all columns exist
        for col in column_order:
            if col not in df.columns:
                df[col] = ''

        # Reorder
        df = df[column_order]

        return df

    def save_output(self, df: pd.DataFrame, output_path: str):
        """
        Save the final output.

        Args:
            df: Final DataFrame
            output_path: Path to save the CSV
        """
        print("\n" + "="*80)
        print("SAVING OUTPUT")
        print("="*80)

        # Create output directory if it doesn't exist
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Save to CSV
        df.to_csv(output_path, index=False)

        print(f"✓ Saved to: {output_path}")
        print(f"  Total rows: {len(df)}")
        print(f"  Total columns: {len(df.columns)}")
        print(f"  File size: {os.path.getsize(output_path) / 1e6:.2f} MB")

    def run(self, input_files: list, output_path: str = './output/final_analysis.csv',
            sentiment_batch_size: int = 32):
        """
        Run the complete pipeline.

        Args:
            input_files: List of input CSV file paths
            output_path: Path for output CSV
            sentiment_batch_size: Batch size for sentiment analysis
        """
        start_time = datetime.now()

        print("\n" + "="*80)
        print(f"STARTING PIPELINE - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80 + "\n")

        try:
            # Step 1: Load data
            df = self.load_data(input_files)

            # Step 2: Prepare data
            df = self.prepare_data(df)

            # Step 3: Run sentiment analysis
            df = self.run_sentiment_analysis(df, batch_size=sentiment_batch_size)

            # Step 4: Run subcategory classification
            df = self.run_subcategory_classification(df)

            # Step 5: Run JTBD transformation
            df = self.run_jtbd_transformation(df)

            # Step 6: Reorder columns
            df = self.reorder_columns(df)

            # Step 7: Save output
            self.save_output(df, output_path)

            # Calculate duration
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            print("\n" + "="*80)
            print("PIPELINE COMPLETE!")
            print("="*80)
            print(f"Duration: {duration:.2f} seconds ({duration/60:.2f} minutes)")
            print(f"Processed: {len(df)} reviews")
            print(f"Speed: {len(df)/duration:.2f} reviews/second")
            print("="*80 + "\n")

            return df

        except Exception as e:
            print(f"\n✗ Pipeline failed: {str(e)}")
            raise


def main():
    """Main entry point for the pipeline."""

    # Define input files
    data_dir = Path('./data')
    input_files = [
        data_dir / 'ubereats_customer_reviews.csv',
        data_dir / 'doordash_customer_reviews.csv',
        data_dir / 'grubhub_customer_reviews.csv'
    ]

    # Check if files exist
    for file_path in input_files:
        if not file_path.exists():
            print(f"⚠ Warning: File not found: {file_path}")

    # Output file
    output_file = './output/final_analysis.csv'

    # Initialize and run pipeline
    # Note: Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable
    pipeline = SentimentAnalysisPipeline(
        llm_provider='openai',  # or 'anthropic'
        llm_model=None  # Use default (best available)
    )

    # Run the pipeline
    result_df = pipeline.run(
        input_files=input_files,
        output_path=output_file,
        sentiment_batch_size=32  # Adjust based on GPU memory
    )

    print(f"\n✓ Results saved to: {output_file}")
    print("\nSample output (first 3 rows):")
    print(result_df.head(3).to_string())


if __name__ == "__main__":
    main()
