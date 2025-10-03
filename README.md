# Aspect-Based Sentiment Analysis for Food Delivery Reviews

## Project Overview
This project performs comprehensive aspect-based sentiment analysis on customer reviews from three major food delivery platforms: UberEats, DoorDash, and GrubHub. The analysis extracts sentiment across multiple aspects, categorizes feedback into subcategories, and transforms reviews into Jobs-To-Be-Done (JTBD) statements.

## Key Features
- **Aspect-Based Sentiment Analysis**: Analyzes 6 aspects (food, delivery, service, price, interface, overall)
- **Subcategory Classification**: Maps each aspect to relevant subcategories
- **JTBD Transformation**: Converts reviews into actionable Jobs-To-Be-Done statements
- **GPU-Accelerated Processing**: Optimized for NVIDIA A40 GPU on RunPod
- **Comprehensive Documentation**: Detailed task-by-task documentation

## Models Used
- **Primary Sentiment Model**: [Anudeep-Narala/fabsa-roberta-sentiment](https://huggingface.co/Anudeep-Narala/fabsa-roberta-sentiment)
- **Subcategory & JTBD**: Advanced LLM (GPT/Llama) for higher quality analysis

## Dataset
- **Source**: Customer reviews from 3 food delivery platforms
- **Files**:
  - `ubereats_customer_reviews.csv`
  - `doordash_customer_reviews.csv`
  - `grubhub_customer_reviews.csv`
- **Input Fields**: id, source, app_type, review, rating, date

## Output Format
Final CSV with the following columns:
- `id` - Unique identifier
- `source` - Review source (google_play, app_store, etc.)
- `app_type` - Application type (customer, driver, etc.)
- `timestamp` - Review date/time
- `comment` - Original review text
- `rating` - Star rating (1-5)
- `Food sentiment` - Sentiment score for food aspect
- `Delivery sentiment` - Sentiment score for delivery aspect
- `Service sentiment` - Sentiment score for service aspect
- `Price sentiment` - Sentiment score for price aspect
- `Interface sentiment` - Sentiment score for interface aspect
- `Overall sentiment` - Overall sentiment score
- `food subcategories` - Food-related subcategories (quality, taste, freshness, presentation)
- `delivery subcategories` - Delivery-related subcategories (speed, reliability, driver behavior, packaging)
- `service subcategories` - Service-related subcategories (customer support, staff attitude, responsiveness)
- `price subcategories` - Price-related subcategories (value for money, fees, discounts, pricing fairness)
- `interface subcategories` - Interface-related subcategories (usability, navigation, features)
- `JTBD statements` - Jobs-To-Be-Done transformation of the review

## Aspect Subcategories

### Food
- Food quality
- Taste
- Freshness
- Presentation

### Delivery
- Delivery speed
- Reliability
- Driver behavior
- Packaging

### Service
- Customer support
- Staff attitude
- Responsiveness

### Price
- Value for money
- Fees
- Discounts
- Pricing fairness

### Interface
- App/website usability
- Navigation
- Features

### Overall
- General satisfaction
- Overall experience

## Project Structure
```
├── data/                   # Input CSV files
├── docs/                   # Main documentation
├── task_docs/             # Task-specific documentation
├── models/                # Model cache
├── output/                # Results and final CSV
├── src/                   # Source code
│   ├── sentiment_analysis.py
│   ├── subcategory_classifier.py
│   ├── jtbd_transformer.py
│   ├── pipeline.py
│   └── utils.py
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- CUDA-capable GPU (NVIDIA A40 recommended)
- 16GB+ GPU memory
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/Anudeepreddynarala/aspect-based-sentiment-analysis.git
cd aspect-based-sentiment-analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Pipeline
```bash
# Run the complete pipeline
python src/pipeline.py

# Output will be saved to: output/final_analysis.csv
```

## GPU Optimization
- Batch processing with optimal batch sizes
- Mixed precision (FP16) for faster inference
- DataLoader with GPU pinned memory
- CUDA kernel optimization

## Documentation
- **Main Documentation**: `/docs`
- **Task Documentation**: `/task_docs` (per-task detailed logs)
- **Code Documentation**: Inline comments and docstrings

## GitHub Repository
https://github.com/Anudeepreddynarala/aspect-based-sentiment-analysis

## Author
Anudeep Narala

## License
MIT License
