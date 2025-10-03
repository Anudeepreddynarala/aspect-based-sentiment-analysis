"""
Multi-label aspect extraction using Qwen2.5-14B-Instruct via Ollama.
Extracts all relevant subcategories from food delivery reviews.
"""

import json
import requests
from typing import List, Dict, Optional


class AspectExtractor:
    """Extract multiple subcategory aspects from reviews using LLM."""

    # Subcategory definitions with strict boundaries
    SUBCATEGORY_DEFINITIONS = {
        # FOOD ASPECTS
        "food_quality": {
            "parent": "food",
            "definition": "Physical condition and preparation of food ONLY. Temperature (hot/cold), cooking level (undercooked/overcooked/burnt), texture, consistency.",
            "keywords": "cold, hot, soggy, burnt, overcooked, undercooked, raw, stale, tough, mushy, dry, greasy"
        },
        "food_taste": {
            "parent": "food",
            "definition": "Flavor and seasoning ONLY. How food tastes, spice level, saltiness, sweetness, blandness.",
            "keywords": "delicious, tasty, bland, flavorless, too salty, too sweet, spicy, disgusting, yummy, awful taste"
        },
        "food_freshness": {
            "parent": "food",
            "definition": "Age and freshness of ingredients ONLY. Spoilage, expired items, wilted produce, old bread.",
            "keywords": "fresh, stale, rotten, expired, wilted, moldy, old, spoiled, past date"
        },
        "food_presentation": {
            "parent": "food",
            "definition": "Visual appearance and plating ONLY. How food looks, arrangement, garnish, mess.",
            "keywords": "beautiful, pretty, ugly, messy, well-plated, sloppy, appealing, unappetizing presentation"
        },

        # DELIVERY ASPECTS
        "delivery_speed": {
            "parent": "delivery",
            "definition": "Time taken for delivery ONLY. Fast, slow, late, early, on-time arrival.",
            "keywords": "fast, slow, late, early, on time, quick, took forever, arrived promptly, delayed"
        },
        "delivery_reliability": {
            "parent": "delivery",
            "definition": "Accuracy and dependability ONLY. Wrong items, missing items, wrong address, order mix-ups.",
            "keywords": "wrong order, missing items, incorrect, forgot, mixed up, reliable, accurate, complete"
        },
        "driver_behavior": {
            "parent": "delivery",
            "definition": "Driver's conduct and professionalism ONLY. Politeness, rudeness, communication, appearance.",
            "keywords": "rude driver, polite, friendly, unprofessional, nice, attitude, courteous, disrespectful"
        },
        "packaging_quality": {
            "parent": "delivery",
            "definition": "Physical packaging condition ONLY. Sealed, damaged, leaking, secure containers, bags.",
            "keywords": "leaked, spilled, damaged packaging, sealed, secure, broken, good packaging, mess"
        },

        # SERVICE ASPECTS
        "customer_support": {
            "parent": "service",
            "definition": "Help from support team ONLY. Response to complaints, refunds, issue resolution, chat/phone support.",
            "keywords": "customer service, support, refund, complaint, help, contact, resolved, unresponsive support"
        },
        "staff_attitude": {
            "parent": "service",
            "definition": "Restaurant staff behavior ONLY (not driver). Kitchen staff, order takers, management attitude.",
            "keywords": "restaurant staff, manager, kitchen, employees, workers, staff rude, helpful staff"
        },
        "responsiveness": {
            "parent": "service",
            "definition": "Speed of communication ONLY. How fast support/restaurant responds to messages or calls.",
            "keywords": "quick response, slow to respond, ignored, replied fast, no answer, responsive"
        },

        # PRICE ASPECTS
        "value_for_money": {
            "parent": "price",
            "definition": "Worth relative to cost ONLY. Portion size vs price, quality vs cost, overpriced, good deal.",
            "keywords": "overpriced, worth it, expensive, cheap, good value, small portions, bang for buck, ripoff"
        },
        "fees_charges": {
            "parent": "price",
            "definition": "Extra costs ONLY. Delivery fees, service fees, hidden charges, surcharges, tips.",
            "keywords": "delivery fee, service charge, hidden fee, surcharge, extra cost, tip, fees too high"
        },
        "discounts_promotions": {
            "parent": "price",
            "definition": "Deals and offers ONLY. Coupons, promo codes, sales, discounts, loyalty rewards.",
            "keywords": "discount, promo, coupon, deal, offer, sale, free delivery, rewards, promotion"
        },
        "pricing_fairness": {
            "parent": "price",
            "definition": "Pricing transparency and honesty ONLY. Unexpected charges, price matching menu, billing errors.",
            "keywords": "charged wrong, billing error, price mismatch, fair pricing, honest, incorrect charge"
        },

        # INTERFACE ASPECTS
        "app_usability": {
            "parent": "interface",
            "definition": "Ease of use ONLY. User-friendliness, confusing interface, smooth experience, bugs, crashes.",
            "keywords": "easy to use, confusing, crashed, buggy, smooth, glitchy, user-friendly, hard to navigate"
        },
        "navigation": {
            "parent": "interface",
            "definition": "Finding things in app ONLY. Menu organization, search function, finding restaurants/items.",
            "keywords": "hard to find, search works, menu layout, organized, can't find, browse, filter"
        },
        "app_features": {
            "parent": "interface",
            "definition": "Specific functionalities ONLY. Tracking, payment options, reorder, customization, notifications.",
            "keywords": "tracking, payment, reorder, customize, notifications, options, features, functionality"
        },

        # OVERALL
        "overall_satisfaction": {
            "parent": "overall",
            "definition": "General experience without specific details. Vague positive/negative statements, would recommend, overall impression.",
            "keywords": "great experience, terrible, recommend, never again, overall, satisfied, disappointed, happy"
        }
    }

    # Create reverse mapping for parent lookup
    SUBCATEGORIES = {k: v["parent"] for k, v in SUBCATEGORY_DEFINITIONS.items()}

    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "qwen2.5:14b-instruct"):
        """Initialize aspect extractor with Ollama endpoint."""
        self.ollama_url = ollama_url
        self.model = model
        self.api_endpoint = f"{ollama_url}/api/generate"

    def _build_prompt(self, review_text: str) -> str:
        """Build extraction prompt with strict boundaries for the LLM."""

        # Format subcategory definitions for the prompt
        definitions = []
        for subcat, info in self.SUBCATEGORY_DEFINITIONS.items():
            definitions.append(f"- {subcat}: {info['definition']}")

        definitions_text = "\n".join(definitions)

        prompt = f"""You are a precise aspect extraction system. Extract ALL subcategories mentioned in this food delivery review.

CRITICAL RULES:
1. Each subcategory has STRICT boundaries - do NOT overlap
2. ONLY select a subcategory if the review explicitly discusses that specific aspect
3. A review can have MULTIPLE subcategories
4. If nothing specific is mentioned, return ONLY ["overall_satisfaction"]

SUBCATEGORY DEFINITIONS (NO OVERLAP ALLOWED):

{definitions_text}

EXAMPLES:
- "Pizza was cold" → ["food_quality"] (NOT food_taste or food_freshness - temperature is quality)
- "Tasted bland" → ["food_taste"] (NOT food_quality - flavor is taste)
- "Driver was rude but food was great" → ["driver_behavior", "food_quality"] (multiple aspects)
- "Love this app!" → ["overall_satisfaction"] (vague, no specifics)

Review to analyze: "{review_text}"

Return ONLY a valid JSON array of subcategories, nothing else.
JSON array:"""

        return prompt

    def extract_aspects(self, review_text: str) -> List[str]:
        """
        Extract all relevant subcategories from a review.

        Args:
            review_text: The review text to analyze

        Returns:
            List of subcategory strings (e.g., ["food_quality", "driver_behavior"])
        """
        prompt = self._build_prompt(review_text)

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.1,  # Low temperature for more deterministic outputs
            "options": {
                "num_predict": 200  # Limit tokens for faster response
            }
        }

        try:
            response = requests.post(self.api_endpoint, json=payload, timeout=60)
            response.raise_for_status()

            result = response.json()
            llm_output = result.get("response", "").strip()

            # Parse JSON response
            aspects = self._parse_llm_output(llm_output)

            # Validate aspects exist in our subcategories
            valid_aspects = [a for a in aspects if a in self.SUBCATEGORIES]

            # If no valid aspects found, default to overall_satisfaction
            if not valid_aspects:
                valid_aspects = ["overall_satisfaction"]

            return valid_aspects

        except Exception as e:
            print(f"Error extracting aspects: {e}")
            # Fallback to overall_satisfaction on error
            return ["overall_satisfaction"]

    def _parse_llm_output(self, output: str) -> List[str]:
        """Parse LLM output to extract JSON array."""
        try:
            # Try direct JSON parsing
            return json.loads(output)
        except json.JSONDecodeError:
            # Try to find JSON array in output
            start_idx = output.find("[")
            end_idx = output.rfind("]")

            if start_idx != -1 and end_idx != -1:
                json_str = output[start_idx:end_idx + 1]
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    pass

            # Fallback: return empty list
            return []

    def get_parent_aspect(self, subcategory: str) -> Optional[str]:
        """Get the parent aspect for a subcategory (for sentiment analysis)."""
        return self.SUBCATEGORIES.get(subcategory)


if __name__ == "__main__":
    # Test the aspect extractor
    extractor = AspectExtractor()

    test_reviews = [
        "The pizza arrived cold and the cheese was congealed. Not happy with food quality.",
        "Driver was rude but food was hot and delicious",
        "App is easy to use and I got a great discount. Worth it!",
        "Terrible experience overall. Will never order again."
    ]

    for review in test_reviews:
        aspects = extractor.extract_aspects(review)
        print(f"\nReview: {review}")
        print(f"Aspects: {aspects}")
        print(f"Parent aspects: {[extractor.get_parent_aspect(a) for a in aspects]}")
