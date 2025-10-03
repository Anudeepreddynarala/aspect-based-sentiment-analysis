"""
Subcategory Classification using Advanced LLM (GPT-4 or Claude)
Classifies customer reviews into specific subcategories for each aspect
"""

import os
from typing import Dict, List
import pandas as pd
from tqdm import tqdm
import json
from openai import OpenAI
from anthropic import Anthropic


class SubcategoryClassifier:
    """
    Classifies reviews into subcategories for each aspect using advanced LLM.
    Ensures subcategories are mapped only to their relevant aspect columns.
    """

    # Define subcategories for each aspect
    SUBCATEGORIES = {
        'food': ['quality', 'taste', 'freshness', 'presentation'],
        'delivery': ['speed', 'reliability', 'driver_behavior', 'packaging'],
        'service': ['customer_support', 'staff_attitude', 'responsiveness'],
        'price': ['value_for_money', 'fees', 'discounts', 'pricing_fairness'],
        'interface': ['usability', 'navigation', 'features'],
        'overall': ['general_satisfaction', 'overall_experience']
    }

    def __init__(self, provider: str = 'openai', model: str = None, api_key: str = None):
        """
        Initialize the subcategory classifier.

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

        print(f"Initialized {provider} classifier with model: {self.model}")

    def create_classification_prompt(self, review: str, aspect: str) -> str:
        """
        Create a prompt for subcategory classification.

        Args:
            review: The customer review text
            aspect: The aspect to classify (food, delivery, service, etc.)

        Returns:
            Formatted prompt string
        """
        subcats = self.SUBCATEGORIES[aspect]

        prompt = f"""You are an expert at analyzing customer reviews for food delivery services.

Your task is to classify the following review into relevant subcategories for the **{aspect.upper()}** aspect only.

Available subcategories for {aspect}:
{chr(10).join(f"- {subcat.replace('_', ' ')}" for subcat in subcats)}

Review: "{review}"

Instructions:
1. Read the review carefully
2. Identify which of the {aspect} subcategories are mentioned or implied in the review
3. Return ONLY the relevant subcategories as a comma-separated list
4. If no {aspect}-related content is found, return "none"
5. Be precise - only include subcategories that are actually discussed in the review

Return format: subcategory1, subcategory2, subcategory3
OR: none (if no relevant content)

Your response:"""

        return prompt

    def classify_with_openai(self, prompt: str) -> str:
        """Call OpenAI API for classification."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a precise classification assistant. Return only the requested subcategories, nothing else."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()

    def classify_with_anthropic(self, prompt: str) -> str:
        """Call Anthropic API for classification."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=100,
            temperature=0.1,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text.strip()

    def classify_single_review(self, review: str) -> Dict[str, str]:
        """
        Classify a single review into subcategories for all aspects.

        Args:
            review: The review text

        Returns:
            Dictionary mapping aspect names to comma-separated subcategories
        """
        results = {}

        for aspect in self.SUBCATEGORIES.keys():
            try:
                prompt = self.create_classification_prompt(review, aspect)

                if self.provider == 'openai':
                    response = self.classify_with_openai(prompt)
                else:
                    response = self.classify_with_anthropic(prompt)

                # Clean up the response
                response = response.lower().strip()
                if response in ['none', 'n/a', '']:
                    results[aspect] = ''
                else:
                    results[aspect] = response

            except Exception as e:
                print(f"Error classifying {aspect}: {str(e)}")
                results[aspect] = ''

        return results

    def classify_batch(self, reviews: List[str], batch_size: int = 1) -> List[Dict[str, str]]:
        """
        Classify multiple reviews.

        Args:
            reviews: List of review texts
            batch_size: Currently 1 (sequential processing)

        Returns:
            List of dictionaries with subcategories for each review
        """
        results = []

        print(f"Classifying {len(reviews)} reviews into subcategories...")

        for review in tqdm(reviews):
            try:
                result = self.classify_single_review(review)
                results.append(result)
            except Exception as e:
                print(f"Error processing review: {str(e)}")
                results.append({aspect: '' for aspect in self.SUBCATEGORIES.keys()})

        return results

    def process_dataframe(self, df: pd.DataFrame, text_column: str = 'comment') -> pd.DataFrame:
        """
        Process a DataFrame and add subcategory columns.

        Args:
            df: DataFrame with reviews
            text_column: Name of the column containing review text

        Returns:
            DataFrame with added subcategory columns for each aspect
        """
        print(f"\nClassifying {len(df)} reviews into subcategories...")

        # Extract reviews
        reviews = df[text_column].fillna("").astype(str).tolist()

        # Classify all reviews
        results = self.classify_batch(reviews)

        # Add results to dataframe - ensure each aspect goes to its own column
        for aspect in self.SUBCATEGORIES.keys():
            column_name = f'{aspect} subcategories'
            df[column_name] = [r[aspect] for r in results]

        print(f"✓ Subcategory classification complete!")
        print(f"  Added columns: {', '.join([f'{a} subcategories' for a in self.SUBCATEGORIES.keys()])}")

        return df


def main():
    """Test the subcategory classifier with sample data."""

    # Note: Requires API key to be set
    try:
        classifier = SubcategoryClassifier(provider='openai')

        test_review = "The food arrived cold and the packaging was damaged. The delivery driver was rude and took forever to arrive."

        print("\n" + "="*80)
        print("TESTING SUBCATEGORY CLASSIFIER")
        print("="*80)
        print(f"\nReview: {test_review}\n")

        results = classifier.classify_single_review(test_review)

        print("Subcategories by Aspect:")
        for aspect, subcats in results.items():
            print(f"  {aspect.capitalize():12} : {subcats if subcats else '(none)'}")

        print("\n✓ Test complete!")

    except ValueError as e:
        print(f"\nNote: {e}")
        print("Set API keys to test the classifier:")
        print("  export OPENAI_API_KEY='your-key-here'")
        print("  or")
        print("  export ANTHROPIC_API_KEY='your-key-here'")


if __name__ == "__main__":
    main()
