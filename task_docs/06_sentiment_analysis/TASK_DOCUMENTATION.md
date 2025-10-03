# Task 06: Aspect-Based Sentiment Analysis Script

## Objective
Develop a GPU-accelerated sentiment analysis script using the fabsa-roberta-sentiment model.

## Implementation Details

### File Created
- `src/sentiment_analysis.py`

### Key Features

#### 1. AspectSentimentAnalyzer Class
- Loads Anudeep-Narala/fabsa-roberta-sentiment model
- GPU-accelerated inference with CUDA support
- Mixed precision (FP16) for faster processing
- Analyzes 6 aspects: food, delivery, service, price, interface, overall

#### 2. Methods

**`__init__(model_name, device)`**
- Initializes model and tokenizer
- Auto-detects GPU availability
- Enables FP16 mixed precision on GPU
- Caches model in `./models` directory

**`analyze_single_review(review_text)`**
- Analyzes one review across all aspects
- Returns dictionary with sentiment scores per aspect
- Format: `[CLS] review [SEP] aspect [SEP]`
- Applies softmax to get probabilities
- Converts to sentiment score: -1 (negative) to +1 (positive)

**`analyze_batch(reviews, batch_size)`**
- Processes multiple reviews in batches
- Default batch size: 16 (adjustable based on GPU memory)
- Progress bar with tqdm
- Error handling for individual reviews

**`process_dataframe(df, text_column, batch_size)`**
- Processes pandas DataFrame
- Adds sentiment columns for each aspect
- Column format: `{Aspect} sentiment`
- Returns modified DataFrame

**`clear_cache()`**
- Clears GPU memory cache
- Called between major operations

### GPU Optimization

1. **Device Selection**: Auto-detects CUDA availability
2. **Mixed Precision**: FP16 for ~2x speedup
3. **Batch Processing**: Efficient memory usage
4. **Memory Management**: Cache clearing between operations

### Output Format

For each review, generates 6 sentiment scores:
- `Food sentiment`: float (-1 to +1)
- `Delivery sentiment`: float (-1 to +1)
- `Service sentiment`: float (-1 to +1)
- `Price sentiment`: float (-1 to +1)
- `Interface sentiment`: float (-1 to +1)
- `Overall sentiment`: float (-1 to +1)

### Testing

Includes `main()` function for testing with sample reviews.

## Status
✅ **COMPLETED**

## Next Steps
- Develop subcategory classification script
