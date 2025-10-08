# Food Delivery Sentiment Analysis: Multi-Platform Customer Intelligence

> **Product Management Portfolio Project** | Data-Driven Customer Experience Analysis

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.7-red.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Executive Summary

Analyzed **7,800 unique customer reviews** (2,600 per platform) across DoorDash, UberEats, and GrubHub to extract actionable insights on customer pain points and satisfaction drivers. Built an AI-powered pipeline that automatically identifies and categorizes customer feedback into 18 distinct aspects with sentiment classification.

**Key Findings:**
- **70.7% negative sentiment** across platforms indicates critical service gaps
- **Customer support** is the #1 complaint category (1,867 negative mentions)
- **Delivery reliability** is the #2 pain point (1,246 negative mentions)
- **GrubHub shows highest negative sentiment** (64.2%) vs DoorDash (54.3%) and UberEats (60.7%)

---

## Business Problem

This project aims to understand the pain points of customers who utilize these Food delivery platforms by:

1. **Automatically categorizing** vague feedback into specific actionable categories
2. **Quantifying sentiment** across 18 distinct customer experience dimensions
3. **Identifying platform-specific weaknesses** to prioritize product improvements
4. **Scaling qualitative insights** from thousands of reviews in minutes, not months

---

## Technical Approach

### Two-Stage AI Pipeline

#### Stage 1: Aspect & Sentiment Classification (Fine-tuned FABSA RoBERTa)
- Each customer review is first passed through a RoBERTa model custom fine-tuned by me with 93.7% accuracy for aspect-based sentiment analysis. [RoBERTa Fine-Tuned Model published at Hugging Face](https://huggingface.co/Anudeep-Narala/fabsa-roberta-sentiment)
- The model automatically identifies all relevant **parent aspects** present in the text and determines the **sentiment** (positive, neutral, negative) for each detected aspect.
- This stage provides a structured overview of which major experience areas (e.g., food, delivery, service, price, interface, overall) are discussed and how customers feel about them.
- **Example**:  
  - Input: *"The pizza was cold and soggy, but the app was easy to use."*  
  - Output: `{ 'food': 'negative', 'interface': 'positive' }`

#### Stage 2: Subcategory Extraction (Qwen 2.5 14B LLM)
- For each detected aspect in a review, a large language model (Qwen 2.5 14B) further breaks down the feedback into **fine-grained subcategories** for deeper insight.
- This step helps clarify exactly what part of an aspect (e.g., food quality vs. food taste) is being praised or criticized.
- Subcategories are extracted using strict definitions and boundary rules to ensure non-overlapping, actionable categories.
- **Example**:  
  - For "food" aspect in *"The pizza was cold and soggy"*, returns: `[food_quality, food_freshness]`  
  - For "interface" aspect in *"The app was easy to use"*, returns: `[app_usability]`

### Aspects & Subcategories

The following parent aspects and their subcategories are used (with strict definitions):

#### Food
- **food_quality**: Physical condition and preparation of food ONLY. Temperature, texture, cooking level, consistency.
- **food_taste**: Flavor and seasoning ONLY. Taste, spice, saltiness, sweetness, blandness.
- **food_freshness**: Age and freshness of ingredients ONLY. Spoilage, expired items, wilted produce.
- **food_presentation**: Visual appearance and plating ONLY. Looks, arrangement, garnish.

#### Delivery
- **delivery_speed**: Time taken for delivery ONLY. Fast, slow, late, early, on-time.
- **delivery_reliability**: Accuracy and dependability ONLY. Wrong/missing items, address issues.
- **driver_behavior**: Driver’s conduct and professionalism ONLY. Politeness, rudeness, communication.
- **packaging_quality**: Physical packaging condition ONLY. Sealed, damaged, leaking, secure containers.

#### Service
- **customer_support**: Help from support team ONLY. Response to complaints, refunds, issue resolution.
- **staff_attitude**: Restaurant staff behavior ONLY (not driver). Kitchen staff, order takers, management.
- **responsiveness**: Communication speed ONLY. Promptness from restaurant or support.

#### Price
- **value_for_money**: Perceived quality vs. cost ONLY. Portion size, worth it.
- **fees_charges**: Delivery/service fees ONLY. Extra charges, transparency.
- **discounts_promotions**: Deals, coupons, and their application.
- **pricing_fairness**: Billing accuracy ONLY. Overcharge, wrong price.

#### Interface
- **app_usability**: Ease of use, bugs ONLY. App crashes, navigation, clarity.
- **navigation**: Finding items or restaurants ONLY. Search, menu organization.
- **app_features**: Specific app features ONLY. Tracking, payment, customization.

#### Overall
- **overall_satisfaction**: Vague or general feedback not specific to any above aspect.

Each subcategory is defined with clear boundaries to ensure high-quality, non-overlapping labeling. For more detail on subcategory definitions and keywords, see the [`aspect_extraction.py`](https://github.com/Anudeepreddynarala/aspect-based-sentiment-analysis/blob/main/src/aspect_extraction.py) file.

### Architecture Diagram
```
Customer Review
      ↓
┌──────────────────────────────┐
│  FABSA RoBERTa (GPU)         │  Detect aspects + sentiment
│  "What is discussed & how?"  │  → {food: negative, interface: positive}
└──────────────────────────────┘
      ↓
┌──────────────────────────────┐
│  Qwen 2.5 14B (GPU)          │  Extract subcategories for each aspect
│  "What about this aspect?"   │  → food: [food_quality, food_freshness]
└──────────────────────────────┘
      ↓
  Highly Actionable Insights
```

---

## Key Insights & Recommendations

### Platform Comparison

| Platform | Negative % | Positive % | Top Pain Point |
|----------|-----------|-----------|----------------|
| **GrubHub** | 74.8% | 26.0% | Customer support (811 mentions) |
| **UberEats** | 67.2% | 24.8% | Customer support (659 mentions) |
| **DoorDash** | 65.4% | 32.9% | Customer support (589 mentions) |

### Top 5 Customer Pain Points (Across All Platforms)

1. **Customer Support** (2,059 mentions, 85% negative)
   - *Recommendation*: Implement live chat + faster refund automation

2. **App Usability** (1,429 mentions, 78% negative)
   - *Recommendation*: Address crashes, simplify checkout flow

3. **Delivery Reliability** (1,409 mentions, 82% negative)
   - *Recommendation*: Improve order accuracy tracking, reduce wrong/missing items

4. **Fees & Charges** (1,132 mentions, 88% negative)
   - *Recommendation*: Increase pricing transparency, bundle fees

5. **Value for Money** (992 mentions, 74% negative)
   - *Recommendation*: Right-size portions, adjust pricing tiers

### Positive Drivers

- **Delivery Speed** shows highest positive sentiment (42% positive)
- **Discounts/Promotions** drive customer satisfaction when present
- **Food Quality** receives praise when executed well (fresh, hot, properly cooked)

---

## Technical Implementation

### Subcategories (18 Total)

**Food (4)**
- `food_quality`: Temperature, texture, cooking level
- `food_taste`: Flavor, seasoning, spice
- `food_freshness`: Ingredient age, spoilage
- `food_presentation`: Visual appearance, plating

**Delivery (4)**
- `delivery_speed`: Delivery time
- `delivery_reliability`: Order accuracy
- `driver_behavior`: Professionalism, communication
- `packaging_quality`: Container condition, leaks

**Service (3)**
- `customer_support`: Issue resolution, refunds
- `staff_attitude`: Restaurant staff behavior
- `responsiveness`: Communication speed

**Price (4)**
- `value_for_money`: Quality vs. cost
- `fees_charges`: Delivery/service fees
- `discounts_promotions`: Deals, coupons
- `pricing_fairness`: Billing accuracy

**Interface (3)**
- `app_usability`: Ease of use, bugs
- `navigation`: Finding items/restaurants
- `app_features`: Tracking, payment, customization

**Overall (1)**
- `overall_satisfaction`: General vague feedback

---

## Getting Started

### Prerequisites
- Python 3.12+
- NVIDIA GPU (16GB+ VRAM recommended)
- Ollama installed

### Installation

```bash
# Clone repository
git clone <your-repo-url>
cd <repo-name>

# Install dependencies
pip install pandas transformers torch requests

# Install Ollama and download model
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull qwen2.5:14b-instruct
```

### Run Analysis

```bash
python run_analysis.py
```

**Output**:
- Individual platform results: `output/doordash_analysis.csv`
- Combined results: `output/complete_analysis_YYYYMMDD_HHMMSS.csv`
- Checkpoints saved every 500 reviews for fault tolerance

---

## Interactive Dashboards

### Live Demos

**🎯 [Multi-Platform Aggregator Dashboard](https://anudeepreddynarala.github.io/aspect-based-sentiment-analysis/dashboard-aggregator/)**

**Platform-Specific Dashboards:**
- **[DoorDash Dashboard](https://anudeepreddynarala.github.io/aspect-based-sentiment-analysis/doordash-dashboard/)** 
- **[UberEats Dashboard](https://anudeepreddynarala.github.io/aspect-based-sentiment-analysis/dashboard-ubereats/)**
- **[GrubHub Dashboard](https://anudeepreddynarala.github.io/aspect-based-sentiment-analysis/dashboard-grubhub/)**

### Features
- **Real-time KPI Tracking**: Average rating, top pain points, correlation analysis
- **Interactive Visualizations**:
  - Parent aspect distribution bar charts
  - Sentiment breakdown donut charts
  - Subcategory treemaps with intensity heatmaps
  - Co-occurrence correlation matrices
  - **NEW**: Platform comparison pyramid (side-by-side analysis)
- **Dynamic Filtering**: Date range, aspect filtering, and platform selectors
- **Platform Comparison**: Visual benchmarking with brand colors (DoorDash red, UberEats green, GrubHub orange)

### Running Dashboards Locally
```bash
# Navigate to any dashboard directory
cd dashboard-aggregator/

# Start local server
python -m http.server 8000

# Open in browser
# http://localhost:8000
```

---

## Project Structure

```
├── data/                          # Input review datasets
│   ├── doordash_customer_reviews.csv
│   ├── ubereats_customer_reviews.csv
│   └── grubhub_customer_reviews.csv
├── src/                           # Source code
│   ├── aspect_extraction.py      # LLM-based subcategory extraction
│   ├── sentiment_analyzer.py     # RoBERTa sentiment classification
│   └── pipeline.py                # End-to-end pipeline orchestration
├── output/                        # Analysis results
│   └── complete_analysis_*.csv   # Final output with all insights
├── dashboard-aggregator/          # Multi-platform analytics dashboard
├── doordash-dashboard/            # DoorDash-specific dashboard
├── dashboard-ubereats/            # UberEats-specific dashboard
├── dashboard-grubhub/             # GrubHub-specific dashboard
├── run_analysis.py                # Main execution script
└── README.md                      # This file
```

---

## Sample Output

```python
# Input Review
"The pizza arrived cold but the driver was very polite"

# Pipeline Output
{
  'food_quality': {
    'sentiment': 'negative',
    'confidence': 0.94,
    'parent_aspect': 'food'
  },
  'driver_behavior': {
    'sentiment': 'positive',
    'confidence': 0.89,
    'parent_aspect': 'delivery'
  }
}
```

**Output CSV Format:**
| review_id | subcategory | sentiment | confidence | platform |
|-----------|-------------|-----------|------------|----------|
| abc123 | food_quality | negative | 0.94 | doordash |
| abc123 | driver_behavior | positive | 0.89 | doordash |

---

## Skills Demonstrated

### Product Management
- **Data-driven decision making**: Quantified customer pain points from unstructured feedback
- **Cross-functional thinking**: Bridged business needs with ML implementation
- **Prioritization**: Ranked features by customer impact (support > app > delivery)
- **Competitive analysis**: Benchmarked 3 platforms to identify gaps

### Technical Skills
- **Machine Learning**: Multi-label classification, sentiment analysis, LLM prompting
- **Python Development**: Pipeline architecture, error handling, checkpointing
- **GPU Optimization**: CUDA acceleration, batch processing
- **Data Analysis**: Pandas, statistical summarization, insight extraction

### Domain Knowledge
- **Customer Experience**: Understanding CX metrics and pain point categorization
- **Food Delivery**: Platform-specific workflows and user journeys
- **NLP**: Aspect-based sentiment analysis, semantic classification

---

## Results Summary

- **7,800 reviews processed** (2,600 per platform)
- **13,868 aspect-sentiment pairs extracted**
- **~0.5s per review** on NVIDIA A40 GPU
- **18 distinct subcategories** identified
- **3 sentiment classes** (positive, neutral, negative)

**Sentiment Breakdown:**
- Negative: 9,801 (70.7%)
- Positive: 3,917 (28.2%)
- Neutral: 150 (1.1%)

---

## Future Enhancements

1. **Time-series analysis**: Track sentiment trends over months
2. **Root cause clustering**: Group similar complaints for deeper insights
3. **Predictive modeling**: Forecast churn based on sentiment patterns
4. **Real-time dashboard**: Live monitoring of customer feedback
5. **Recommendation engine**: Suggest specific product fixes per platform

---

## License

MIT License - See [LICENSE](LICENSE) file for details

---

## About

**Product Manager | Data Analyst**

This project demonstrates my ability to:
- Translate business problems into technical solutions
- Extract actionable insights from large-scale unstructured data
- Build production-grade ML pipelines
- Communicate findings to stakeholders

anudeepreddynarala2@gmail.com
https://www.linkedin.com/in/anudeep-narala/

---

*Built with Qwen 2.5 14B, FABSA RoBERTa, PyTorch, and passion for customer experience.*
