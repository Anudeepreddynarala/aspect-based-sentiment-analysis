# DoorDash Sentiment Analytics Dashboard

> **Interactive dashboard for analyzing DoorDash customer feedback with dynamic filtering and comprehensive visualizations**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-View%20Dashboard-FF3008?style=for-the-badge)](https://your-username.github.io/sentiment/dashboard/)

## 📊 Overview

This dashboard provides deep insights into DoorDash customer sentiment across 13,000+ reviews from March-September 2025. Built with Plotly.js, it features interactive charts, dynamic filtering, and real-time calculations to identify key pain points and improvement opportunities.

### Key Features

✨ **5 Interactive Visualizations**
- Parent aspect negative review analysis
- Subcategory treemap with rating heatmap
- Top 3 focus areas by intensity
- Aspect co-occurrence correlation
- Sentiment distribution overview

📅 **Dynamic Filtering**
- Date range selection
- Parent aspect filtering
- One-click reset functionality

📈 **Real-time KPIs**
- Average rating across all reviews
- Top negative subcategory (by intensity)
- Highest correlation pair
- Percentage mentioning top issue

🎨 **Modern Design**
- DoorDash-branded theme
- Fully responsive (mobile/tablet/desktop)
- Smooth animations and hover effects
- Accessible and professional UI

## 🚀 Quick Start

### Option 1: View Live Dashboard (Recommended)

Visit the hosted version: **[Live Dashboard Link](https://your-username.github.io/sentiment/dashboard/)**

### Option 2: Run Locally

```bash
# Clone the repository
git clone https://github.com/your-username/sentiment.git
cd sentiment/dashboard

# Start a local server (Python 3)
python -m http.server 8000

# Or with Python 2
python -m SimpleHTTPServer 8000

# Open in browser
open http://localhost:8000
```

**Alternative servers:**
```bash
# Node.js (http-server)
npx http-server -p 8000

# PHP
php -S localhost:8000
```

## 📁 Project Structure

```
dashboard/
├── index.html                  # Main dashboard page
├── data/
│   └── complete_analysis_20251003_234035.csv  # Review dataset (13,869 rows)
├── js/
│   ├── data-processor.js       # Data loading & calculations
│   ├── charts.js               # Plotly chart rendering
│   └── filters.js              # Filter logic & event handlers
├── css/
│   └── styles.css              # DoorDash-themed styling
└── README.md                   # This file
```

## 🎯 Dashboard Components

### 1. KPI Cards (Top Section)

| Metric | Description | Calculation |
|--------|-------------|-------------|
| **Average Rating** | Mean rating across all reviews | `sum(ratings) / count(reviews)` |
| **Top Negative Subcategory** | Highest intensity subcategory | `max(sum(6 - rating) by subcategory)` |
| **Highest Correlation** | Most co-occurring aspect pair | `max(co-occurrence_matrix)` |
| **Top Aspect Mention %** | % reviews with top negative issue | `(reviews_with_aspect / total_reviews) × 100` |

### 2. Charts

#### Parent Aspects vs Negative Reviews Bar Chart
- **Purpose**: Compare negative sentiment across high-level aspects
- **Data**: Count of negative reviews per parent aspect (Service, Delivery, Price, Food, Interface, Overall)
- **Insights**: Identifies which broad category needs most attention

#### Subcategory Treemap (Negative Sentiment)
- **Purpose**: Drill down into specific subcategory issues
- **Size**: Number of negative reviews mentioning subcategory
- **Color**: Average rating (darker = lower rating)
- **Filter**: Adjustable by parent aspect dropdown
- **Insights**: Visual hierarchy of problem areas

#### Top 3 Focus Areas (Intensity Chart)
- **Purpose**: Prioritize subcategories for immediate action
- **Metric**: Intensity = `sum(6 - rating)` for negative reviews
- **Display**: Horizontal bar chart showing top 3 highest intensity scores
- **Insights**: Quantifies urgency of fixing each issue

#### Correlation Heatmap
- **Purpose**: Discover which aspects are mentioned together
- **Metric**: Co-occurrence count (how often 2 aspects appear in same review)
- **Insights**: Reveals interconnected pain points

#### Sentiment Distribution Donut Chart
- **Purpose**: Overall sentiment breakdown
- **Data**: Positive, Negative, Neutral counts
- **Center Text**: Shows % of all reviews mentioning the top negative aspect
- **Insights**: High-level sentiment health check

### 3. Filters

| Filter | Type | Effect | Default |
|--------|------|--------|---------|
| **Start Date** | Date picker | Filters all charts by date range | March 16, 2025 |
| **End Date** | Date picker | Filters all charts by date range | September 28, 2025 |
| **Parent Aspect** | Dropdown | Filters treemap only | All Aspects |
| **Reset Button** | Button | Restores all defaults | N/A |

## 📊 Data Schema

The dashboard uses `complete_analysis_20251003_234035.csv` with the following structure:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `review_id` | String | Unique review identifier | `bce430680f2cb46629e737820f40fc66` |
| `review_text` | String | Original review content | `"Door Dash keeps me sane..."` |
| `subcategory` | String | Specific aspect mentioned | `customer_support` |
| `parent_aspect` | String | High-level category | `service` |
| `sentiment` | String | Sentiment classification | `positive`, `negative`, `neutral` |
| `confidence` | Float | Model confidence score | `0.9989` |
| `rating` | Integer | Star rating (1-5) | `5` |
| `date` | Date | Review timestamp | `2025-09-27 16:48:48` |
| `platform` | String | Data source | `doordash` |

**Dataset Stats:**
- Total records: **13,869**
- Date range: **March 16 - September 28, 2025**
- Unique reviews: **~4,000**
- Platforms: DoorDash only

## 🎨 Design Specifications

### Color Palette (DoorDash Theme)

```css
Primary Red:     #FF3008
Dark Red:        #E12100
Accent Red:      #FF6347
Background:      #FFFFFF
Card Background: #F5F5F5
Text Dark:       #191919
Text Gray:       #696969
Positive:        #2ECC71
Negative:        #E74C3C
Neutral:         #95A5A6
```

### Typography
- **Font Family**: System fonts (`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto`)
- **Headings**: 700 weight, DoorDash red
- **Body Text**: 400 weight, dark gray

### Responsive Breakpoints
- **Desktop**: > 1200px (2-column grid)
- **Tablet**: 768px - 1200px (1-column grid)
- **Mobile**: < 768px (stacked layout)

## 🔧 Technical Details

### Dependencies
- **Plotly.js** v2.27.0 - Interactive charts
- **PapaParse** v5.4.1 - CSV parsing
- **Vanilla JavaScript** - No frameworks required

### Browser Compatibility
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### Performance
- **Load time**: < 2 seconds (including data)
- **Data size**: ~2MB CSV
- **Rendering**: Client-side, no backend required

## 🧮 Calculations & Algorithms

### Intensity Score
```javascript
// For negative reviews only
intensity = 6 - rating

// Example: 1-star review = 6 - 1 = 5 intensity
// Example: 2-star review = 6 - 2 = 4 intensity
```

### Co-occurrence Matrix
```javascript
// Count how many reviews mention both aspects A and B
correlation[A][B] = count(reviews where A ∈ review AND B ∈ review)
```

### Top Aspect Percentage
```javascript
percentage = (unique_reviews_with_top_aspect / total_unique_reviews) × 100
```

## 📖 User Guide

### How to Use the Dashboard

1. **Initial View**
   - Dashboard loads with all data (March-September 2025)
   - All charts render automatically
   - KPIs display summary statistics

2. **Filter by Date Range**
   - Click **Start Date** picker → Select date
   - Click **End Date** picker → Select date
   - All charts update instantly

3. **Filter Treemap by Aspect**
   - Use **Parent Aspect** dropdown
   - Select: Service, Delivery, Price, Food, Interface, or Overall
   - Only treemap updates (other charts show all data)

4. **Reset Filters**
   - Click **Reset Filters** button
   - All filters return to defaults
   - Dashboard refreshes

5. **Interact with Charts**
   - **Hover**: Show detailed tooltips
   - **Zoom**: Click-drag on charts (bar/heatmap)
   - **Pan**: Shift+drag to move view
   - **Download**: Camera icon in modebar (top-right of each chart)

### Interpreting the Data

**High Priority Issues:**
1. Check **Top 3 Focus Areas** chart (highest intensity = most urgent)
2. Look at **Parent Aspects Bar Chart** (highest bar = most complaints)
3. Drill into **Treemap** (largest + darkest boxes = worst subcategories)

**Understanding Relationships:**
- **Heatmap**: Dark cells = aspects often mentioned together
- **Correlation**: High co-occurrence suggests linked problems (fix one, may improve both)

**Sentiment Health:**
- **Donut Chart**: High negative % = serious issues
- **Center Text**: If >50%, that aspect is mentioned in majority of reviews

## 🚀 Deployment to GitHub Pages

### Step 1: Create Repository
```bash
git init
git add dashboard/
git commit -m "Add DoorDash sentiment dashboard"
git branch -M main
git remote add origin https://github.com/your-username/sentiment.git
git push -u origin main
```

### Step 2: Configure GitHub Pages
1. Go to repository **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **main** → Folder: **/ (root)**
4. Click **Save**

### Step 3: Access Dashboard
- URL format: `https://your-username.github.io/sentiment/dashboard/`
- Wait 1-2 minutes for deployment
- Verify all charts load correctly

### Troubleshooting
- **Charts not loading**: Check browser console for errors
- **Data not found**: Verify `data/complete_analysis_20251003_234035.csv` exists
- **Filters not working**: Hard refresh (`Cmd+Shift+R` / `Ctrl+Shift+R`)

## 📝 License

This project is licensed under the MIT License.

## 👤 About

**Created by**: [Your Name]
**Portfolio**: [Your Portfolio URL]
**LinkedIn**: [Your LinkedIn]
**GitHub**: [Your GitHub]

---

**Built with Plotly.js, vanilla JavaScript, and a passion for data-driven insights.**

For questions or suggestions, please open an issue or reach out via LinkedIn.
