# Setup Guide

## Prerequisites

### Hardware
- NVIDIA GPU with CUDA support (A40 recommended)
- 16GB+ GPU memory
- 32GB+ system RAM
- 100GB+ storage

### Software
- Python 3.8 or higher
- CUDA 11.8
- Git

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Anudeepreddynarala/aspect-based-sentiment-analysis.git
cd aspect-based-sentiment-analysis
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install PyTorch with CUDA

```bash
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 4. Install Dependencies

```bash
pip install transformers accelerate datasets pandas sentencepiece protobuf tokenizers tqdm python-dotenv pyyaml openai anthropic
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

### 5. Verify GPU Setup

```bash
python3 -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"
```

Expected output:
```
CUDA Available: True
GPU: NVIDIA A40
```

### 6. Configure API Keys

Choose ONE of the following LLM providers:

#### Option A: OpenAI (GPT-4)

1. Get API key from https://platform.openai.com/
2. Create `.env` file:
```bash
cp .env.example .env
```
3. Edit `.env` and add your key:
```
OPENAI_API_KEY=sk-your-api-key-here
LLM_PROVIDER=openai
```

#### Option B: Anthropic (Claude)

1. Get API key from https://console.anthropic.com/
2. Create `.env` file:
```bash
cp .env.example .env
```
3. Edit `.env` and add your key:
```
ANTHROPIC_API_KEY=your-api-key-here
LLM_PROVIDER=anthropic
```

### 7. Verify Data Files

Ensure your CSV files are in the `data/` directory:
```bash
ls -lh data/
```

Expected:
```
ubereats_customer_reviews.csv
doordash_customer_reviews.csv
grubhub_customer_reviews.csv
```

## Running the Pipeline

### Quick Start

```bash
cd /workspace
source venv/bin/activate
export OPENAI_API_KEY='your-key-here'  # or ANTHROPIC_API_KEY
python src/pipeline.py
```

### Custom Configuration

Edit `src/pipeline.py` to customize:
- `llm_provider`: 'openai' or 'anthropic'
- `llm_model`: Specific model name
- `sentiment_batch_size`: Adjust for GPU memory (16-64)

### Output

Results will be saved to:
```
output/final_analysis.csv
```

## Testing Individual Components

### Test Sentiment Analysis

```bash
python src/sentiment_analysis.py
```

### Test Subcategory Classifier

```bash
export OPENAI_API_KEY='your-key-here'
python src/subcategory_classifier.py
```

### Test JTBD Transformer

```bash
export OPENAI_API_KEY='your-key-here'
python src/jtbd_transformer.py
```

## Troubleshooting

### GPU Not Detected

```bash
# Check CUDA installation
nvidia-smi

# Verify PyTorch CUDA
python3 -c "import torch; print(torch.version.cuda)"
```

### Out of Memory Error

Reduce batch size in `pipeline.py`:
```python
sentiment_batch_size=16  # Try smaller values like 8 or 4
```

### API Rate Limits

If you hit rate limits:
1. Add delays between API calls
2. Process in smaller batches
3. Consider upgrading API tier

### Model Download Issues

Models are cached in `./models/`. If download fails:
```bash
rm -rf ./models/
python src/sentiment_analysis.py  # Retry download
```

## Performance Optimization

### GPU Optimization
- Use mixed precision (enabled by default)
- Increase batch size if GPU memory allows
- Monitor GPU usage: `watch -n 1 nvidia-smi`

### API Optimization
- Use batch processing when possible
- Cache results to avoid reprocessing
- Consider parallel API calls (with rate limit awareness)

## Cost Estimation

### API Costs (Approximate)

**OpenAI GPT-4 Turbo**:
- Input: $10 per 1M tokens
- Output: $30 per 1M tokens
- Estimated: ~$0.02-0.05 per review

**Anthropic Claude 3 Sonnet**:
- Input: $3 per 1M tokens
- Output: $15 per 1M tokens
- Estimated: ~$0.01-0.02 per review

For 1000 reviews:
- OpenAI: ~$20-50
- Anthropic: ~$10-20

## Support

For issues, please:
1. Check this guide
2. Review error messages
3. Open an issue on GitHub

## Next Steps

After setup:
1. Test with small sample (10-20 reviews)
2. Review output quality
3. Run full pipeline
4. Analyze results
