# Dashboard Replication Guide

This guide explains how to replicate the DoorDash dashboard for other platforms (UberEats, GrubHub, etc.) using the same design and functionality.

## Prerequisites

- Sentiment analysis CSV data with the required columns (see Data Format section)
- Basic understanding of file paths and text editing

---

## Step 1: Copy the Dashboard Template

```bash
# Navigate to your project
cd aspect-based-sentiment-analysis

# Copy the entire doordash-dashboard folder
cp -r doordash-dashboard ubereats-dashboard

# Or for GrubHub
cp -r doordash-dashboard grubhub-dashboard
```

---

## Step 2: Update Data File

Replace the data file with your platform's data:

```bash
# Copy your new sentiment analysis results
cp /path/to/ubereats_complete_analysis.csv ubereats-dashboard/data/

# Remove old data (optional, to save space)
rm ubereats-dashboard/data/complete_analysis_20251003_234035.csv
```

---

## Step 3: Update Data Path in JavaScript

Edit `ubereats-dashboard/js/data-processor.js`:

**Find line 21** (approximately):
```javascript
Papa.parse('data/complete_analysis_20251003_234035.csv', {
```

**Change to**:
```javascript
Papa.parse('data/ubereats_complete_analysis.csv', {
```

---

## Step 4: Customize Colors (Optional)

If you want platform-specific branding, edit `ubereats-dashboard/css/styles.css`:

### Current Colors (DoorDash)
```css
:root {
    --doordash-red: #FF4D4D;
    /* ... other colors ... */
}
```

### Example: UberEats Green
```css
:root {
    --ubereats-green: #06C167;  /* UberEats primary color */
    --page-background: #0F0F0F;
    --card-background: #1A1A1A;
    --text-primary: #F5F5F5;
    --text-secondary: #A3A3A3;
    --border-color: #2A2A2A;
}
```

**Then replace all instances of `var(--doordash-red)` with `var(--ubereats-green)`**

### Example: GrubHub Orange
```css
:root {
    --grubhub-orange: #F63440;  /* GrubHub primary color */
    /* ... */
}
```

---

## Step 5: Update Title and Branding

### Update HTML Title
Edit `ubereats-dashboard/index.html` (line 6):

```html
<!-- From -->
<title>DoorDash Sentiment Analytics Dashboard</title>

<!-- To -->
<title>UberEats Sentiment Analytics Dashboard</title>
```

### Update Dashboard Header
Edit `ubereats-dashboard/index.html` (lines 18-19):

```html
<!-- From -->
<h1 class="dashboard-title">DoorDash Sentiment Analytics</h1>
<p class="dashboard-subtitle">Customer Feedback Intelligence Dashboard</p>

<!-- To -->
<h1 class="dashboard-title">UberEats Sentiment Analytics</h1>
<p class="dashboard-subtitle">Customer Feedback Intelligence Dashboard</p>
```

### Update Footer
Edit `ubereats-dashboard/index.html` (line ~123):

```html
<!-- From -->
<p>DoorDash Sentiment Analytics Dashboard | ...</p>

<!-- To -->
<p>UberEats Sentiment Analytics Dashboard | ...</p>
```

---

## Step 6: Update Chart Colors in JavaScript

Edit `ubereats-dashboard/js/charts.js` (lines 1-12):

```javascript
// Change from DoorDash red to UberEats green
const COLORS = {
    primary: '#06C167',        // UberEats Green (was #FF4D4D)
    blue: '#60A5FA',
    gold: '#FBBF24',
    gray: '#9CA3AF',
    teal: '#2DD4BF',
    positive: '#34D399',
    negative: '#06C167',       // UberEats Green (was #FF4D4D)
    neutral: '#A3A3A3',
    gradientStart: '#06C167',  // UberEats Green
    gradientEnd: '#05A357'     // Darker green
};
```

---

## Step 7: Update README (Optional)

Edit `ubereats-dashboard/README.md`:

- Replace all instances of "DoorDash" with "UberEats"
- Update the color palette documentation
- Update any platform-specific descriptions

---

## Step 8: Test Locally

```bash
cd ubereats-dashboard
python3 -m http.server 8000

# Visit http://localhost:8000 in your browser
```

**Verify**:
- ✅ Data loads correctly
- ✅ All charts display
- ✅ Filters work
- ✅ Colors match platform branding
- ✅ Title shows correct platform

---

## Step 9: Deploy to GitHub

```bash
# Add to git
git add ubereats-dashboard/

# Commit
git commit -m "Add UberEats sentiment dashboard

- Replicated DoorDash dashboard design
- Updated to UberEats green branding (#06C167)
- Uses ubereats_complete_analysis.csv data
- Same interactive features and filters
"

# Push to GitHub
git push origin main
```

---

## Step 10: Enable GitHub Pages (First Time Only)

If not already enabled:

1. Go to: https://github.com/Anudeepreddynarala/aspect-based-sentiment-analysis
2. **Settings** → **Pages**
3. Source: **Deploy from a branch**
4. Branch: **main** / Folder: **/ (root)**
5. Click **Save**

**Your dashboards will be live at**:
- DoorDash: `https://anudeepreddynarala.github.io/aspect-based-sentiment-analysis/doordash-dashboard/`
- UberEats: `https://anudeepreddynarala.github.io/aspect-based-sentiment-analysis/ubereats-dashboard/`
- GrubHub: `https://anudeepreddynarala.github.io/aspect-based-sentiment-analysis/grubhub-dashboard/`

---

## Data Format Requirements

Your CSV must have these columns (exact names):

```csv
review_id,review_text,subcategory,parent_aspect,sentiment,confidence,rating,date,platform
```

### Column Descriptions

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `review_id` | String | Unique identifier | "r12345" |
| `review_text` | String | Original review text | "Food was cold" |
| `subcategory` | String | One of 18 subcategories | "food_quality" |
| `parent_aspect` | String | One of 6 parent aspects | "food" |
| `sentiment` | String | "positive", "negative", or "neutral" | "negative" |
| `confidence` | Float | Confidence score (0-1) | 0.95 |
| `rating` | Integer | Star rating (1-5) | 2 |
| `date` | String | ISO date format | "2025-03-15" |
| `platform` | String | Platform name | "ubereats" |

### Supported Subcategories (18)

**Food (4)**:
- `food_quality`, `food_taste`, `food_freshness`, `food_presentation`

**Delivery (4)**:
- `delivery_speed`, `delivery_reliability`, `driver_behavior`, `packaging_quality`

**Service (3)**:
- `customer_support`, `staff_attitude`, `responsiveness`

**Price (4)**:
- `value_for_money`, `fees_charges`, `discounts_promotions`, `pricing_fairness`

**Interface (3)**:
- `app_usability`, `navigation`, `app_features`

**Overall (1)**:
- `overall_satisfaction`

### Parent Aspects (6)
- `food`, `delivery`, `service`, `price`, `interface`, `overall`

---

## Quick Reference: Platform Colors

| Platform | Primary Color | Hex Code |
|----------|--------------|----------|
| DoorDash | Red | `#FF4D4D` |
| UberEats | Green | `#06C167` |
| GrubHub | Orange | `#F63440` |
| Postmates | Yellow | `#FFD400` |
| Deliveroo | Teal | `#00CCBC` |

---

## Troubleshooting

### Dashboard shows "Error loading data"
- ✅ Check data file path in `data-processor.js` line 21
- ✅ Verify CSV file exists in `data/` folder
- ✅ Check CSV has all required columns
- ✅ Open browser console (F12) for detailed error

### Charts don't display
- ✅ Check browser console for JavaScript errors
- ✅ Verify Plotly CDN is loading (line 11 in `index.html`)
- ✅ Clear browser cache (Ctrl+Shift+R / Cmd+Shift+R)

### Colors don't change
- ✅ Clear browser cache after updating CSS
- ✅ Check you updated both CSS variables AND chart colors in `charts.js`
- ✅ Search for all instances of old color hex codes

### Filters don't work
- ✅ Check aspect checkbox IDs match in `filters.js`
- ✅ Verify date format in CSV is ISO format (YYYY-MM-DD)
- ✅ Clear browser cache

---

## File Checklist for New Dashboard

When creating a new platform dashboard, update these files:

- [ ] **Data file**: `data/[platform]_complete_analysis.csv`
- [ ] **Data path**: `js/data-processor.js` (line 21)
- [ ] **Color palette**: `css/styles.css` (root variables)
- [ ] **Chart colors**: `js/charts.js` (COLORS object, lines 1-12)
- [ ] **HTML title**: `index.html` (line 6)
- [ ] **Dashboard header**: `index.html` (lines 18-19)
- [ ] **Footer text**: `index.html` (line ~123)
- [ ] **README**: `README.md` (all platform references)

---

## Advanced: Automated Script (Optional)

Create `replicate_dashboard.sh` for faster replication:

```bash
#!/bin/bash
# Usage: ./replicate_dashboard.sh ubereats "#06C167" "UberEats"

PLATFORM=$1
COLOR=$2
DISPLAY_NAME=$3

# Copy template
cp -r doordash-dashboard ${PLATFORM}-dashboard

# Update data path (requires manual data file placement)
echo "⚠️  Remember to copy your ${PLATFORM} CSV to ${PLATFORM}-dashboard/data/"

# Update colors
sed -i '' "s/#FF4D4D/${COLOR}/g" ${PLATFORM}-dashboard/css/styles.css
sed -i '' "s/#FF4D4D/${COLOR}/g" ${PLATFORM}-dashboard/js/charts.js

# Update text
sed -i '' "s/DoorDash/${DISPLAY_NAME}/g" ${PLATFORM}-dashboard/index.html
sed -i '' "s/DoorDash/${DISPLAY_NAME}/g" ${PLATFORM}-dashboard/README.md

echo "✅ ${DISPLAY_NAME} dashboard created!"
echo "📝 Next steps:"
echo "   1. Copy your CSV data to ${PLATFORM}-dashboard/data/"
echo "   2. Update data path in ${PLATFORM}-dashboard/js/data-processor.js"
echo "   3. Test locally: cd ${PLATFORM}-dashboard && python3 -m http.server"
```

**Usage**:
```bash
chmod +x replicate_dashboard.sh
./replicate_dashboard.sh ubereats "#06C167" "UberEats"
./replicate_dashboard.sh grubhub "#F63440" "GrubHub"
```

---

## Support

For questions or issues:
- Check browser console (F12) for errors
- Verify all file paths are correct
- Ensure CSV data format matches requirements
- Test locally before deploying to GitHub Pages

---

**Last Updated**: October 7, 2025
**Dashboard Version**: 2.1 (Dark Mode with Accent & Air Design)
