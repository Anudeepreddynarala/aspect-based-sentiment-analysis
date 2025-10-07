# 🚗 DoorDash Sentiment Analytics Dashboard

> **Interactive dashboard for analyzing DoorDash customer feedback with dynamic filtering and comprehensive visualizations**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-View%20Dashboard-FF3008?style=for-the-badge)](https://your-username.github.io/sentiment/doordash-dashboard/)

## 📊 Overview

This dashboard provides deep insights into **2,600 unique DoorDash customer reviews** from March-September 2025. Built with Plotly.js, it features interactive charts, dynamic filtering, and real-time calculations to identify key pain points specific to DoorDash operations.

## 🎯 DoorDash Performance Metrics

### Overall Statistics
- **Total Unique Reviews**: 2,600
- **Average Rating**: 3.02/5 (Best among platforms)
- **Date Range**: March - September 2025

### Sentiment Distribution
- **Positive**: 42.9% (1,115 reviews)
- **Negative**: 54.3% (1,411 reviews)
- **Neutral**: 2.8% (74 reviews)

### Top Issues (Negative Reviews)
1. **Customer Support**: 622 negative mentions
2. **Delivery Reliability**: 415 negative mentions
3. **App Usability**: 355 negative mentions
4. **Fees & Charges**: 354 negative mentions
5. **Value for Money**: 284 negative mentions

## 📈 Dashboard Features

### KPI Cards
- **Average Rating**: 3.02/5 overall platform rating
- **Top Negative Subcategory**: Customer support (highest intensity)
- **Highest Correlation**: Issues that commonly occur together
- **Total Reviews**: 2,600 unique customer reviews

### Interactive Visualizations

#### 1. Parent Aspects Bar Chart
Distribution of negative reviews by category:
- Service: ~900 negative reviews
- Price: ~900 negative reviews
- Delivery: ~700 negative reviews
- Interface: ~450 negative reviews
- Overall: ~390 negative reviews
- Food: ~115 negative reviews

#### 2. Sentiment Distribution Donut
- 42.9% Positive (Green)
- 54.3% Negative (Red)
- 2.8% Neutral (Gray)

#### 3. Subcategory Treemap
Hierarchical view of all subcategories with:
- Size = number of reviews
- Color intensity = average rating (darker = worse)

#### 4. Top 3 Focus Areas
Priority issues by intensity (6 - rating):
1. Customer Support (2,984 intensity)
2. Delivery Reliability (1,945 intensity)
3. Overall Satisfaction (1,782 intensity)

#### 5. Co-occurrence Heatmap
Shows which issues appear together in reviews
- Identifies related problem areas
- Uses Jaccard similarity coefficient

### Filters
- **Date Range**: Adjustable start and end dates
- **Parent Aspect**: Multi-select filtering
- **Reset**: Clear all filters

## 🚀 Getting Started

### Local Setup
```bash
# Navigate to dashboard directory
cd doordash-dashboard/

# Start local server
python -m http.server 8000

# Open browser
# Navigate to: http://localhost:8000
```

### Requirements
- Modern web browser (Chrome, Firefox, Safari, Edge)
- No backend required (static site)
- Internet connection for CDN resources

## 📁 File Structure
```
doordash-dashboard/
├── index.html                    # Main dashboard HTML
├── data/
│   └── complete_analysis_*.csv   # DoorDash-filtered dataset
├── js/
│   ├── data-processor.js         # Data filtering & calculations
│   ├── charts.js                 # Plotly visualizations
│   └── filters.js                # Filter interactions
├── css/
│   └── styles.css                # Dark theme styling
└── README.md                     # This file
```

## 💡 Key Insights

### Strengths
✅ **Highest average rating** among three platforms (3.02/5)
✅ **Lowest negative sentiment** (54.3% vs 60.7% UberEats, 64.2% GrubHub)
✅ **Better customer satisfaction** compared to competitors

### Areas for Improvement
⚠️ **Customer Support**: #1 pain point with highest intensity
⚠️ **Delivery Reliability**: Significant issue affecting customer trust
⚠️ **App Usability**: Technical issues impacting user experience

### Recommendations
1. **Invest in support training** and response time improvements
2. **Enhance delivery tracking** and accuracy measures
3. **Fix app bugs** and improve UI/UX design
4. **Review pricing strategy** to address value perception

## 🔧 Technical Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Charting**: Plotly.js 2.27.0
- **Data Parsing**: PapaParse 5.4.1
- **Design**: Dark theme with DoorDash brand colors
- **Typography**: Inter font family

## 📊 Data Processing
- Filters dataset to DoorDash reviews only
- Calculates metrics in real-time
- Handles multi-aspect reviews correctly
- Uses unique review IDs to avoid duplicates

## 🎨 Design Philosophy
**"Accent & Air"** - Clean interface with strategic color use:
- DoorDash Red (#FF4D4D) as primary accent
- Dark theme for reduced eye strain
- Generous whitespace for clarity
- Responsive layout for all devices

## 🔗 Related Dashboards
- [Multi-Platform Dashboard](../dashboard-aggregator/) - Compare all platforms
- [UberEats Dashboard](../dashboard-ubereats/) - UberEats analysis
- [GrubHub Dashboard](../dashboard-grubhub/) - GrubHub analysis

---
*Last Updated: December 2024*