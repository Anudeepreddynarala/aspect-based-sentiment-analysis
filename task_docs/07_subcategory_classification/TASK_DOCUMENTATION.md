# Task 07: Subcategory Classification Script

## Objective
Develop an advanced LLM-based subcategory classifier that accurately maps reviews to relevant subcategories for each aspect.

## Implementation Details

### File Created
- `src/subcategory_classifier.py`

### Key Features

#### 1. SubcategoryClassifier Class
- Supports OpenAI (GPT-4) and Anthropic (Claude) APIs
- Precision multi-label classification
- Aspect-specific subcategory mapping
- **Important**: Each aspect's subcategories only go into their respective columns

#### 2. Subcategory Definitions

**Food**:
- quality, taste, freshness, presentation

**Delivery**:
- speed, reliability, driver_behavior, packaging

**Service**:
- customer_support, staff_attitude, responsiveness

**Price**:
- value_for_money, fees, discounts, pricing_fairness

**Interface**:
- usability, navigation, features

**Overall**:
- general_satisfaction, overall_experience

#### 3. Methods

**`__init__(provider, model, api_key)`**
- Initializes OpenAI or Anthropic client
- Default models:
  - OpenAI: gpt-4-turbo-preview
  - Anthropic: claude-3-sonnet-20240229
- Reads API keys from environment variables

**`create_classification_prompt(review, aspect)`**
- Creates aspect-specific prompts
- Lists only relevant subcategories for that aspect
- Clear instructions for precision classification
- Returns "none" if no relevant content found

**`classify_single_review(review)`**
- Classifies one review across all 6 aspects
- Returns dictionary with aspect → subcategories mapping
- Each aspect processed independently
- **Ensures subcategories only appear in their correct aspect column**

**`classify_batch(reviews, batch_size)`**
- Processes multiple reviews sequentially
- Progress tracking with tqdm
- Error handling per review

**`process_dataframe(df, text_column)`**
- Processes pandas DataFrame
- Adds 6 subcategory columns:
  - `food subcategories`
  - `delivery subcategories`
  - `service subcategories`
  - `price subcategories`
  - `interface subcategories`
  - `overall subcategories`
- Each column contains comma-separated subcategories

### API Configuration

**OpenAI**:
- Model: GPT-4 Turbo Preview
- Temperature: 0.1 (for consistency)
- Max Tokens: 100

**Anthropic**:
- Model: Claude 3 Sonnet
- Temperature: 0.1 (for consistency)
- Max Tokens: 100

### Column Mapping Guarantee

The system ensures:
- Food subcategories → `food subcategories` column ONLY
- Delivery subcategories → `delivery subcategories` column ONLY
- Service subcategories → `service subcategories` column ONLY
- Price subcategories → `price subcategories` column ONLY
- Interface subcategories → `interface subcategories` column ONLY
- Overall subcategories → `overall subcategories` column ONLY

**No cross-contamination between aspect columns.**

### Testing

Includes `main()` function for testing with sample reviews.
Requires API key to be set via environment variable.

## Status
✅ **COMPLETED**

## Next Steps
- Develop JTBD transformation script
