# Task 08: Jobs-To-Be-Done Transformation Script

## Objective
Develop an advanced LLM-based transformer that converts customer reviews into high-quality JTBD statements.

## Implementation Details

### File Created
- `src/jtbd_transformer.py`

### Key Features

#### 1. JTBDTransformer Class
- Supports OpenAI (GPT-4) and Anthropic (Claude) APIs
- Context-aware JTBD generation
- Domain expertise in food delivery
- High-quality, actionable statements

#### 2. JTBD Statement Format

**Structure**:
```
When [situation/context],
I want to [action/goal]
so that [desired outcome].
[Optional: Current barrier/issue]
```

**Example**:
> "When I order food for delivery during my lunch break, I want the app to process my order quickly and accurately so that I can receive my meal on time and get back to work. Currently, the app crashes during checkout causing delays."

#### 3. Methods

**`__init__(provider, model, api_key)`**
- Initializes OpenAI or Anthropic client
- Default models:
  - OpenAI: gpt-4-turbo-preview (best reasoning)
  - Anthropic: claude-3-sonnet-20240229 (excellent comprehension)
- Reads API keys from environment variables

**`create_jtbd_prompt(review, rating, platform)`**
- Creates context-rich prompts
- Includes review text, rating, and platform
- Provides JTBD format guidelines
- Includes example JTBD statements
- Emphasizes situation, goal, outcome, and barriers

**`transform_single_review(review, rating, platform)`**
- Transforms one review into a JTBD statement
- Uses contextual information (rating, platform)
- Returns clean, formatted JTBD string
- Error handling with fallback statements

**`transform_batch(reviews, ratings, platforms)`**
- Processes multiple reviews sequentially
- Progress tracking with tqdm
- Handles optional ratings and platforms
- Error handling per review

**`process_dataframe(df, text_column, rating_column, platform_column)`**
- Processes pandas DataFrame
- Extracts review, rating, and platform data
- Adds `JTBD statements` column
- Returns modified DataFrame

### API Configuration

**OpenAI**:
- Model: GPT-4 Turbo Preview (best for creative reasoning)
- Temperature: 0.3 (balance between consistency and creativity)
- Max Tokens: 200 (for complete statements)

**Anthropic**:
- Model: Claude 3 Sonnet (excellent understanding)
- Temperature: 0.3 (balance between consistency and creativity)
- Max Tokens: 200 (for complete statements)

### JTBD Quality Criteria

1. **Situation/Context**: Clear "when" statement
2. **Goal/Action**: Specific "I want to" statement
3. **Desired Outcome**: Clear "so that" statement
4. **Barriers**: Optional but important for negative reviews
5. **Actionable**: Can inform product/service improvements
6. **Domain-Specific**: Food delivery context preserved

### Example Transformations

**Review**: "App crashed when applying promo code"
**JTBD**: "When I'm ready to place my food order, I want to easily apply promotional codes without technical issues so that I can save money and complete my purchase quickly."

**Review**: "Food arrived cold and late"
**JTBD**: "When I order food for delivery, I want it to arrive hot and on time so that I can enjoy a quality meal without frustration."

**Review**: "Great service, fast delivery"
**JTBD**: "When I'm hungry and short on time, I want reliable fast delivery service so that I can get a satisfying meal quickly and get on with my day."

### Testing

Includes `main()` function for testing with sample reviews.
Requires API key to be set via environment variable.

## Status
✅ **COMPLETED**

## Next Steps
- Create main pipeline orchestration script
