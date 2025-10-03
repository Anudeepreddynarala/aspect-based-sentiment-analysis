"""
Jobs-To-Be-Done (JTBD) Transformation using Advanced LLM
Converts customer reviews into actionable JTBD statements
"""

import os
from typing import List
import pandas as pd
from tqdm import tqdm
from openai import OpenAI
from anthropic import Anthropic


class JTBDTransformer:
    """
    Transforms customer reviews into Jobs-To-Be-Done statements.
    Uses advanced LLM to understand context and create actionable insights.
    """

    def __init__(self, provider: str = 'openai', model: str = None, api_key: str = None):
        """
        Initialize the JTBD transformer.

        Args:
            provider: 'openai' for GPT-4 or 'anthropic' for Claude
            model: Specific model name (defaults to best available)
            api_key: API key for the provider (or set via environment variable)
        """
        self.provider = provider

        if provider == 'openai':
            self.model = model or 'gpt-4-turbo-preview'
            api_key = api_key or os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")
            self.client = OpenAI(api_key=api_key)

        elif provider == 'anthropic':
            self.model = model or 'claude-3-sonnet-20240229'
            api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                raise ValueError("Anthropic API key required. Set ANTHROPIC_API_KEY environment variable.")
            self.client = Anthropic(api_key=api_key)

        else:
            raise ValueError(f"Unknown provider: {provider}. Use 'openai' or 'anthropic'")

        print(f"Initialized {provider} JTBD transformer with model: {self.model}")

    def create_jtbd_prompt(self, review: str, rating: int, platform: str = '') -> str:
        """
        Create a prompt for JTBD transformation.

        Args:
            review: The customer review text
            rating: Star rating (1-5)
            platform: Platform name (UberEats, DoorDash, GrubHub)

        Returns:
            Formatted prompt string
        """
        prompt = f"""You are an expert at converting customer feedback into Jobs-To-Be-Done (JTBD) statements.

A good JTBD statement captures:
1. The situation/context (When...)
2. The desired action/goal (I want to...)
3. The desired outcome (So that...)
4. Any barriers or friction points

Customer Review:
Platform: {platform or 'Food Delivery Service'}
Rating: {rating}/5 stars
Review: "{review}"

Your task:
Transform this review into a clear, actionable JTBD statement that captures what the customer is trying to accomplish, the context, desired outcome, and any obstacles they faced.

Format: "When [situation], I want to [action/goal] so that [desired outcome]. [Optional: Current barrier/issue]"

Examples:
- "When I'm hungry and need food delivered quickly, I want the app to process my order efficiently so that I can get my meal within the promised time. Currently, the app crashes during checkout causing delays."
- "When I order expensive food for delivery, I want it to arrive hot and fresh so that I get value for my money and enjoy my meal."
- "When I use a food delivery app, I want an intuitive interface with clear navigation so that I can easily find restaurants and complete my order without frustration."

Your JTBD statement:"""

        return prompt

    def transform_with_openai(self, prompt: str) -> str:
        """Call OpenAI API for JTBD transformation."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert at creating Jobs-To-Be-Done statements. Create clear, actionable JTBD statements that capture customer needs and contexts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()

    def transform_with_anthropic(self, prompt: str) -> str:
        """Call Anthropic API for JTBD transformation."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=200,
            temperature=0.3,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text.strip()

    def transform_single_review(self, review: str, rating: int = 3, platform: str = '') -> str:
        """
        Transform a single review into a JTBD statement.

        Args:
            review: The review text
            rating: Star rating
            platform: Platform name

        Returns:
            JTBD statement string
        """
        try:
            prompt = self.create_jtbd_prompt(review, rating, platform)

            if self.provider == 'openai':
                jtbd = self.transform_with_openai(prompt)
            else:
                jtbd = self.transform_with_anthropic(prompt)

            # Clean up the response
            jtbd = jtbd.strip()

            # Remove any quotes if the LLM added them
            if jtbd.startswith('"') and jtbd.endswith('"'):
                jtbd = jtbd[1:-1]

            return jtbd

        except Exception as e:
            print(f"Error transforming review: {str(e)}")
            return f"When using {platform or 'a food delivery service'}, I want a better experience."

    def transform_batch(self, reviews: List[str], ratings: List[int] = None,
                       platforms: List[str] = None) -> List[str]:
        """
        Transform multiple reviews into JTBD statements.

        Args:
            reviews: List of review texts
            ratings: List of ratings (optional)
            platforms: List of platform names (optional)

        Returns:
            List of JTBD statements
        """
        if ratings is None:
            ratings = [3] * len(reviews)
        if platforms is None:
            platforms = [''] * len(reviews)

        results = []

        print(f"Transforming {len(reviews)} reviews into JTBD statements...")

        for i, review in enumerate(tqdm(reviews)):
            try:
                jtbd = self.transform_single_review(review, ratings[i], platforms[i])
                results.append(jtbd)
            except Exception as e:
                print(f"Error processing review {i}: {str(e)}")
                results.append(f"When using a food delivery service, I want a better experience.")

        return results

    def process_dataframe(self, df: pd.DataFrame,
                         text_column: str = 'comment',
                         rating_column: str = 'rating',
                         platform_column: str = 'source') -> pd.DataFrame:
        """
        Process a DataFrame and add JTBD statements.

        Args:
            df: DataFrame with reviews
            text_column: Name of the column containing review text
            rating_column: Name of the column containing ratings
            platform_column: Name of the column containing platform info

        Returns:
            DataFrame with added JTBD statements column
        """
        print(f"\nTransforming {len(df)} reviews into JTBD statements...")

        # Extract data
        reviews = df[text_column].fillna("").astype(str).tolist()
        ratings = df[rating_column].fillna(3).astype(int).tolist() if rating_column in df.columns else None
        platforms = df[platform_column].fillna("").astype(str).tolist() if platform_column in df.columns else None

        # Transform all reviews
        jtbd_statements = self.transform_batch(reviews, ratings, platforms)

        # Add to dataframe
        df['JTBD statements'] = jtbd_statements

        print(f"✓ JTBD transformation complete!")
        print(f"  Added column: JTBD statements")

        return df


def main():
    """Test the JTBD transformer with sample data."""

    try:
        transformer = JTBDTransformer(provider='openai')

        test_review = "App keeps crashing when I try to apply promo codes. Lost my discount and had to reorder."
        test_rating = 1
        test_platform = "UberEats"

        print("\n" + "="*80)
        print("TESTING JTBD TRANSFORMER")
        print("="*80)
        print(f"\nReview: {test_review}")
        print(f"Rating: {test_rating}/5")
        print(f"Platform: {test_platform}\n")

        jtbd = transformer.transform_single_review(test_review, test_rating, test_platform)

        print("JTBD Statement:")
        print(f"  {jtbd}")

        print("\n✓ Test complete!")

    except ValueError as e:
        print(f"\nNote: {e}")
        print("Set API keys to test the transformer:")
        print("  export OPENAI_API_KEY='your-key-here'")
        print("  or")
        print("  export ANTHROPIC_API_KEY='your-key-here'")


if __name__ == "__main__":
    main()
