# Multi-Platform Dashboard - Quick Reference

## File Paths

### Core Files
```
/Users/anudeepnarala/Projects/Sentiment/Github/dashboard-aggregator/
├── index.html                    # Main HTML (8.3 KB)
├── css/styles.css                # Purple/blue theme (8.5 KB)
├── js/data-processor.js          # Data loading & calculations (9.7 KB)
├── js/charts.js                  # 6 Plotly visualizations (13 KB)
├── js/filters.js                 # Filter logic & events (9.3 KB)
├── data/complete_analysis_20251003_234035.csv  # 13,869 reviews (4.5 MB)
├── README.md                     # User guide (4.4 KB)
└── COMPLETION_CHECKLIST.md       # Requirements checklist (5.9 KB)
```

## Quick Start

```bash
cd /Users/anudeepnarala/Projects/Sentiment/Github/dashboard-aggregator
python -m http.server 8000
# Open http://localhost:8000
```

## Key Features

### Filters
- **Platform**: Multi-select (All, DoorDash, UberEats, GrubHub)
- **Date Range**: Start/end date pickers
- **Aspect**: Multi-select (All, Service, Delivery, Price, Food, Interface, Overall)

### KPIs (3 cards)
1. Average Rating
2. Top Negative Aspect
3. Total Reviews

### Charts (6 visualizations)
1. **Parent Aspects Bar** - Negative reviews by aspect (purple bars)
2. **Sentiment Donut** - Positive/Negative/Neutral distribution
3. **Subcategory Treemap** - Negative reviews by subcategory (color by rating)
4. **Top 3 Intensity** - Focus areas by severity (purple gradient)
5. **Correlation Heatmap** - Aspect co-occurrence (CENTERED, purple scale)
6. **Platform Pyramid** - A/B comparison (brand colors)

## Theme Colors

### Primary
- Purple: `#8B5CF6`
- Blue: `#6366F1`

### Platform Brands
- DoorDash: `#FF4D4D` (red)
- UberEats: `#06C167` (green)
- GrubHub: `#FF8000` (orange)

### Background
- Page: `#0F0F0F`
- Cards: `#1A1A1A`

## HTML Element IDs

### Filters
- `platformFilterToggle` / `platformFilterMenu`
- `startDate` / `endDate`
- `aspectFilterToggle` / `aspectFilterMenu`
- `resetFilters`

### KPIs
- `avgRating`
- `topNegative`
- `totalReviews`

### Charts
- `aspectBarChart`
- `sentimentDonut`
- `treemapChart`
- `intensityChart`
- `correlationHeatmap`
- `platformPyramid`

### Pyramid Controls
- `platformADropdown` (left side)
- `platformBDropdown` (right side)

## Key Functions

### Data Processing (data-processor.js)
```javascript
loadData()                          // Load CSV with ALL platforms
applyFilters()                      // Apply platform + date filters
calculateAvgRating(data)            // Groups by review_id (FIXED)
getPlatformComparisonData(data, A, B)  // NEW for pyramid
```

### Charts (charts.js)
```javascript
renderAllCharts(data)               // Render all 6 charts
renderPlatformPyramid(data, A, B)   // NEW pyramid with brand colors
```

### Filters (filters.js)
```javascript
handlePlatformFilterChange(checkboxes)  // Platform multi-select
handlePyramidPlatformChange()          // Update pyramid
resetFilters()                         // Reset all to defaults
```

## Testing Checklist

- [ ] Platform filter (select DoorDash only)
- [ ] Platform filter (select multiple platforms)
- [ ] Date range filter (narrow date range)
- [ ] Aspect filter (select Service only)
- [ ] Pyramid dropdown A (change to UberEats)
- [ ] Pyramid dropdown B (change to GrubHub)
- [ ] Reset button (all filters reset)
- [ ] KPIs update with filters
- [ ] All charts update with filters
- [ ] Pyramid uses correct brand colors
- [ ] Heatmap is centered
- [ ] Responsive on mobile

## Deployment

### GitHub Pages
1. Push to GitHub
2. Settings → Pages
3. Source: Deploy from main branch
4. Folder: `/dashboard-aggregator`

### Other Hosts
- Netlify: Drop `dashboard-aggregator` folder
- Vercel: Import repository
- Any static host: Upload all files

## Technical Stack

- HTML5
- CSS3 (Custom properties, Flexbox, Grid)
- Vanilla JavaScript (ES6+)
- Plotly.js 2.27.0
- PapaParse 5.4.1
- Inter font (Google Fonts)

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Status

✅ **COMPLETE** - All features implemented and ready for deployment
