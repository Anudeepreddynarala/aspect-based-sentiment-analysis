# Task 04: Python Environment Setup

## Objective
Set up Python virtual environment and install all required dependencies for the project.

## Steps Performed

### 1. Created Virtual Environment
```bash
python3 -m venv venv
```

### 2. Installed PyTorch with CUDA 11.8
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Installed Packages**:
- torch 2.7.1+cu118
- torchvision 0.22.1+cu118
- torchaudio 2.7.1+cu118
- CUDA libraries (cublas, cudnn, cusparse, etc.)
- triton 3.3.1

### 3. Installed NLP and ML Libraries
```bash
pip install transformers accelerate datasets pandas sentencepiece protobuf tokenizers tqdm python-dotenv pyyaml openai anthropic
```

**Key Libraries**:
- transformers - HuggingFace transformers library
- accelerate - GPU optimization
- datasets - Data loading and processing
- pandas - Data manipulation
- tokenizers - Fast tokenization
- openai - GPT-4 API access
- anthropic - Claude API access

## Dependencies Overview

### Core ML Stack
- PyTorch 2.7.1 with CUDA 11.8 support
- Transformers 4.56.2
- Accelerate 1.10.1

### Data Processing
- Pandas 2.3.3
- NumPy 2.1.2

### Model APIs
- OpenAI (for GPT-4 access)
- Anthropic (for Claude access)

### Utilities
- tqdm - Progress bars
- python-dotenv - Environment variable management
- pyyaml - Configuration files

## Model Selection Strategy

### Primary Sentiment Model
- **Model**: Anudeep-Narala/fabsa-roberta-sentiment
- **Purpose**: Aspect-based sentiment analysis
- **Deployment**: Local GPU inference

### Advanced LLM for Subcategories & JTBD
- **Option 1**: GPT-4 (OpenAI API) - Highest quality, best understanding
- **Option 2**: Claude 3 Sonnet (Anthropic API) - Excellent reasoning
- **Selection Criteria**:
  - Strong understanding of customer service contexts
  - Accurate multi-label classification
  - High-quality JTBD statement generation
  - Contextual understanding of food delivery domain

## Status
✅ **COMPLETED**

## Next Steps
- Verify GPU availability
- Test CUDA functionality
- Develop sentiment analysis script
