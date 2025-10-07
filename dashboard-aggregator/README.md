# Multi-Platform Sentiment Analytics Dashboard

A comprehensive interactive dashboard for analyzing customer sentiment across DoorDash, UberEats, and GrubHub food delivery platforms.

## Features

### Filters
- **Platform Filter**: Multi-select dropdown to filter by platform (All, DoorDash, UberEats, GrubHub)
- **Date Range Filter**: Start and end date pickers to analyze specific time periods
- **Aspect Filter**: Multi-select dropdown to filter subcategories by parent aspect (affects treemap only)
- **Reset Button**: Quickly reset all filters to defaults

### KPI Cards
1. **Average Rating**: Overall average rating across all reviews
2. **Top Negative Aspect**: Most mentioned subcategory in negative reviews
3. **Total Reviews Analyzed**: Count of unique reviews in current filter selection

### Visualizations

#### Row 1
- **Negative Reviews by Parent Aspect** (Left): Horizontal bar chart showing negative review counts by parent aspect
- **Sentiment Distribution** (Right): Donut chart showing positive/negative/neutral sentiment breakdown

#### Row 2
- **Subcategory Breakdown** (Left): Treemap showing negative reviews by subcategory with color-coded average ratings
- **Top 3 Focus Areas** (Right): Horizontal bar chart highlighting top 3 subcategories by intensity score

#### Row 3 (Full Width)
- **Aspect Co-occurrence Matrix**: Centered heatmap showing Jaccard similarity between subcategories

#### Row 4 (Full Width)
- **Platform Comparison Pyramid**: Back-to-back horizontal bar chart comparing negative reviews between two selected platforms
  - Dropdown controls to select Platform A (left) and Platform B (right)
  - Uses brand colors for each platform

## Design

### Theme
- **Color Scheme**: Purple/Blue accent theme (#8B5CF6) with dark mode foundation
- **Platform Colors**:
  - DoorDash: #FF4D4D (red)
  - UberEats: #06C167 (green)
  - GrubHub: #FF8000 (orange)
- **Typography**: Inter font family
- **Philosophy**: "Accent & Air" - clean, spacious interface with strategic use of color

### Responsive
- Desktop: 2-column grid layout
- Tablet: Single column layout
- Mobile: Fully stacked layout with optimized controls

## Usage

### Local Development
```bash
# Navigate to dashboard directory
cd dashboard-aggregator

# Start local server
python -m http.server 8000

# Open browser
open http://localhost:8000
```

### Deployment
The dashboard is a fully static site and can be deployed to:
- GitHub Pages
- Netlify
- Vercel
- Any static hosting service

## Data

### Input File
- `data/complete_analysis_20251003_234035.csv`
- Contains sentiment analysis results for all three platforms
- 13,869 rows of analyzed reviews

### Required Columns
- `review_id`: Unique review identifier
- `review_text`: Original review text
- `subcategory`: Aspect subcategory (18 total)
- `parent_aspect`: Parent aspect category (6 total)
- `sentiment`: positive/negative/neutral
- `confidence`: Model confidence score
- `platform`: doordash/ubereats/grubhub
- `rating`: 1-5 star rating
- `date`: Review date (YYYY-MM-DD HH:MM:SS)

## Technical Stack

- **HTML5**: Structure
- **CSS3**: Styling with custom properties
- **Vanilla JavaScript**: All interactions (no frameworks)
- **Plotly.js 2.27.0**: Interactive visualizations
- **PapaParse 5.4.1**: CSV parsing
- **Google Fonts**: Inter typography

## File Structure

```
dashboard-aggregator/
├── index.html              # Main HTML structure
├── README.md               # This file
├── data/
│   └── complete_analysis_20251003_234035.csv
├── css/
│   └── styles.css          # Purple/blue theme styling
└── js/
    ├── data-processor.js   # Data loading & calculations
    ├── charts.js           # Plotly visualizations
    └── filters.js          # Filter logic & events
```

## Key Metrics

### Intensity Calculation
```
intensity = 6 - rating
```
Used to weight negative reviews by severity:
- 1-star review: intensity = 5 (most urgent)
- 2-star review: intensity = 4
- 3-star review: intensity = 3
- 4-star review: intensity = 2
- 5-star review: intensity = 1 (least urgent)

### Jaccard Similarity
```
similarity = intersection / union
```
Measures how often two aspects are mentioned together in the same review.

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License

MIT License - See main repository for details

## Contact

For questions or suggestions, please contact the repository owner.
