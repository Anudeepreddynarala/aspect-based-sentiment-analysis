# Task 09: Pipeline Orchestration Script

## Objective
Create a comprehensive pipeline script that orchestrates all processing steps from data loading to final output generation.

## Implementation Details

### Files Created
- `src/pipeline.py` - Main pipeline orchestration
- `src/utils.py` - Utility functions
- `.env.example` - API key configuration template

### Key Features

#### 1. SentimentAnalysisPipeline Class

**Complete end-to-end processing**:
1. Load data from multiple CSV files
2. Prepare and clean data
3. Run aspect-based sentiment analysis (GPU-accelerated)
4. Run subcategory classification (LLM-based)
5. Run JTBD transformation (LLM-based)
6. Reorder columns to match requirements
7. Save final output

#### 2. Pipeline Methods

**`__init__(llm_provider, llm_model)`**
- Initializes all three components:
  - AspectSentimentAnalyzer (GPU)
  - SubcategoryClassifier (LLM)
  - JTBDTransformer (LLM)
- Checks GPU availability
- Handles missing API keys gracefully

**`load_data(file_paths)`**
- Loads multiple CSV files
- Combines into single DataFrame
- Reports loading status per file
- Error handling for each file

**`prepare_data(df)`**
- Renames columns: `date` → `timestamp`, `review` → `comment`
- Validates required columns
- Cleans text data
- Ensures proper data types

**`run_sentiment_analysis(df, batch_size)`**
- Calls sentiment analyzer
- GPU-optimized batch processing
- Clears GPU cache after completion
- Adds 6 sentiment columns

**`run_subcategory_classification(df)`**
- Calls subcategory classifier
- API-based processing
- Adds 6 subcategory columns
- Skips if no API key (with warning)

**`run_jtbd_transformation(df)`**
- Calls JTBD transformer
- API-based processing
- Adds JTBD statements column
- Skips if no API key (with warning)

**`reorder_columns(df)`**
- Ensures correct column order
- Matches required output format:
  1. id
  2. source
  3. app_type
  4. timestamp
  5. comment
  6. rating
  7. Food sentiment
  8. Delivery sentiment
  9. Service sentiment
  10. Price sentiment
  11. Interface sentiment
  12. Overall sentiment
  13. food subcategories
  14. delivery subcategories
  15. service subcategories
  16. price subcategories
  17. interface subcategories
  18. overall subcategories
  19. JTBD statements

**`save_output(df, output_path)`**
- Creates output directory if needed
- Saves to CSV
- Reports file statistics

**`run(input_files, output_path, sentiment_batch_size)`**
- Main execution method
- Runs all pipeline steps
- Tracks duration and performance
- Comprehensive error handling

#### 3. Utility Functions (utils.py)

**`print_gpu_stats()`**
- Displays GPU memory usage
- Helps monitor resource utilization

**`analyze_results(df)`**
- Generates statistics from results
- Counts positive/neutral/negative per aspect
- Platform distribution
- Average ratings and sentiments

**`print_sample_results(df, n)`**
- Pretty-prints sample results
- Shows complete analysis for N reviews
- Useful for quality checking

**`save_statistics(stats, output_path)`**
- Saves statistics to JSON file
- For further analysis

**`create_summary_report(df, output_path)`**
- Creates human-readable text report
- Summary of all analyses
- Breakdown by aspect and platform

**`validate_output(df)`**
- Validates required columns exist
- Ensures data integrity
- Returns True or raises ValueError

### Configuration

**`.env.example`**:
```
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
LLM_PROVIDER=openai
```

User must copy to `.env` and add actual API keys.

### GPU Optimization

1. **Batch Processing**: Adjustable batch size (default: 32)
2. **Memory Management**: Cache clearing between stages
3. **Mixed Precision**: FP16 for faster inference
4. **Resource Monitoring**: GPU stats tracking

### Error Handling

- Graceful degradation if API keys missing
- Per-file error handling in data loading
- Per-review error handling in processing
- Fallback values for failed analyses

### Performance Tracking

- Start/end timestamps
- Total duration calculation
- Reviews per second metric
- File size reporting

## Status
✅ **COMPLETED**

## Next Steps
- Set up API keys
- Run the pipeline on actual data
- Generate final output CSV
