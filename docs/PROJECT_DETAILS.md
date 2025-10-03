# Project Details: Aspect-Based Sentiment Analysis

## Executive Summary
This project implements a comprehensive aspect-based sentiment analysis pipeline for food delivery platform reviews. It processes customer feedback from UberEats, DoorDash, and GrubHub to extract multi-dimensional insights across six key aspects: food quality, delivery experience, customer service, pricing, interface usability, and overall satisfaction.

## Project Specifications

### Input Data
- **Total Files**: 3 CSV files
- **Platforms**: UberEats, DoorDash, GrubHub
- **Source**: Customer reviews from Google Play Store and other sources
- **Input Schema**:
  ```
  id: string (unique identifier)
  source: string (review source platform)
  app_type: string (customer/driver/restaurant)
  review: string (review text)
  rating: integer (1-5 stars)
  date: timestamp
  ```

### Analysis Components

#### 1. Aspect-Based Sentiment Analysis
**Model**: `Anudeep-Narala/fabsa-roberta-sentiment` (HuggingFace)
**Aspects Analyzed**:
- Food
- Delivery
- Service
- Price
- Interface
- Overall

**Output**: Sentiment scores for each aspect per review

#### 2. Subcategory Classification
**Purpose**: Granular categorization of feedback within each aspect
**Method**: Advanced LLM-based classification (GPT or Llama)

**Subcategory Mapping**:

**Food**:
- Food quality
- Taste
- Freshness
- Presentation

**Delivery**:
- Delivery speed
- Reliability
- Driver behavior
- Packaging

**Service**:
- Customer support
- Staff attitude
- Responsiveness

**Price**:
- Value for money
- Fees
- Discounts
- Pricing fairness

**Interface**:
- App/website usability
- Navigation
- Features

**Overall**:
- General satisfaction
- Overall experience

#### 3. JTBD (Jobs-To-Be-Done) Transformation
**Purpose**: Convert customer reviews into actionable JTBD statements
**Method**: Advanced LLM-based transformation with context understanding
**Output**: Structured JTBD statements that capture:
- The job the customer is trying to accomplish
- The context and circumstances
- The desired outcome
- Barriers or friction points

**Example Transformation**:
- **Review**: "The app keeps crashing when I try to apply my promo code during checkout"
- **JTBD**: "When I'm ready to place my food order, I want to easily apply promotional codes without technical issues so that I can save money and complete my purchase quickly"

### Output Specification

**Final CSV Schema**:
```
id                      : string
source                  : string
app_type                : string
timestamp               : datetime
comment                 : string (original review)
rating                  : integer
Food sentiment          : float
Delivery sentiment      : float
Service sentiment       : float
Price sentiment         : float
Interface sentiment     : float
Overall sentiment       : float
food subcategories      : string (comma-separated)
delivery subcategories  : string (comma-separated)
service subcategories   : string (comma-separated)
price subcategories     : string (comma-separated)
interface subcategories : string (comma-separated)
JTBD statements         : string
```

### Technical Infrastructure

#### Hardware Requirements
- **GPU**: NVIDIA A40 (48GB VRAM)
- **Platform**: RunPod cloud GPU instance
- **CPU**: Multi-core processor
- **RAM**: 32GB+ recommended
- **Storage**: 100GB+ for models and data

#### Software Stack
- **Python**: 3.8+
- **PyTorch**: Latest stable version with CUDA support
- **Transformers**: HuggingFace library
- **Pandas**: Data manipulation
- **Datasets**: HuggingFace datasets library
- **Accelerate**: GPU optimization

#### GPU Optimization Strategy
1. **Batch Processing**: Dynamic batching based on GPU memory
2. **Mixed Precision**: FP16 for faster inference
3. **Memory Management**: Gradient checkpointing and caching
4. **Parallel Processing**: Multi-GPU support if available
5. **Model Quantization**: Optional for larger models

### Pipeline Architecture

#### Stage 1: Data Loading & Preprocessing
- Load all 3 CSV files
- Validate data integrity
- Clean and normalize text
- Handle missing values
- Preserve original metadata (id, source, app_type, timestamp, rating)

#### Stage 2: Aspect-Based Sentiment Analysis
- Load fabsa-roberta-sentiment model onto GPU
- Process reviews in batches
- Extract sentiment scores for all 6 aspects
- Store intermediate results

#### Stage 3: Subcategory Classification
- Load advanced LLM (GPT/Llama)
- For each review and aspect:
  - Analyze review context
  - Classify into relevant subcategories
  - Generate comma-separated subcategory list
- Batch processing with GPU acceleration

#### Stage 4: JTBD Transformation
- Use advanced LLM for transformation
- Prompt engineering for JTBD format
- Context-aware statement generation
- Validate output quality

#### Stage 5: Data Consolidation
- Merge all analysis results
- Combine original metadata with new columns
- Validate final schema
- Export to CSV

### Documentation Strategy

#### Main Documentation (`/docs`)
- README.md: Project overview and quick start
- PROJECT_DETAILS.md: This file - comprehensive specifications
- API_REFERENCE.md: Code documentation
- RESULTS_ANALYSIS.md: Analysis findings and insights

#### Task-Specific Documentation (`/task_docs`)
Each task has its own folder with:
- TASK_DOCUMENTATION.md: Task objectives, steps, status
- NOTES.md: Implementation notes and decisions
- RESULTS.md: Task-specific outcomes
- ISSUES.md: Challenges and solutions

### Version Control & GitHub Integration

#### Repository
- **URL**: https://github.com/Anudeepreddynarala/aspect-based-sentiment-analysis
- **Branch Strategy**: main branch for production-ready code
- **Commit Frequency**: After each major task completion

#### Commit Guidelines
- Descriptive commit messages
- Reference task numbers
- Include documentation updates
- Tag major milestones

### Quality Assurance

#### Validation Checks
- Data integrity validation
- Schema validation
- Sentiment score range checks
- JTBD statement quality review
- Output completeness verification

#### Testing Strategy
- Sample data testing before full processing
- Intermediate result validation
- Error handling and logging
- Performance benchmarking

### Performance Targets
- **Processing Speed**: 100-200 reviews/second with GPU
- **Memory Usage**: < 40GB GPU VRAM
- **Accuracy**: > 85% sentiment classification accuracy
- **Output Quality**: Manual review of sample JTBD statements

### Project Timeline
1. Environment Setup: 30 minutes
2. Code Development: 2-3 hours
3. Data Processing: 1-2 hours (depends on dataset size)
4. Validation & Documentation: 1 hour
5. Final GitHub Push: 15 minutes

**Total Estimated Time**: 4-6 hours

### Deliverables
1. ✅ Complete source code in `/src`
2. ✅ Final CSV output with all required columns
3. ✅ Comprehensive documentation
4. ✅ Task-by-task progress documentation
5. ✅ GitHub repository with all code and docs
6. ✅ Performance benchmarks and statistics

### Future Enhancements
- Real-time sentiment analysis API
- Interactive dashboard for visualization
- Multi-language support
- Comparative analysis across platforms
- Time-series trend analysis
- Automated reporting system

## Contact
For questions or issues, please open an issue on GitHub or contact Anudeep Narala.
