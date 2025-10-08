# Multi-Platform Aggregator Dashboard Color Scheme

⚠️ **IMPORTANT: DO NOT MODIFY THIS COLOR SCHEME**

This color configuration has been finalized and tested. Any changes to colors should only be made with explicit approval.

## Dashboard Theme: Blue

The aggregator dashboard uses a blue color scheme to remain neutral and not favor any specific platform.

## Sentiment Color Scheme (Monochromatic Blue)

The sentiment donut chart uses a monochromatic blue color scheme:

- **Positive**: Blue `#60A5FA`
- **Negative**: Dark Blue `#1E40AF`
- **Neutral**: Gray `#9CA3AF`

### Design Rationale
- **Neutral Theme**: Blue doesn't conflict with any platform brand colors
- **Clear Distinction**: Bright blue vs dark blue provides excellent contrast
- **Visual Harmony**: Matches the overall aggregator theme
- **Avoids Confusion**: Different from all three platforms (DoorDash red, UberEats green, GrubHub orange)

## Platform Comparison Pyramid Colors

The population pyramid (comparison chart) uses **actual platform brand colors** for clear identification:

- **DoorDash**: Red `#FF4D4D`
- **UberEats**: Green `#06C167`
- **GrubHub**: Orange `#FB923C`

This allows users to instantly recognize which platform is being displayed on each side of the comparison.

## Overall Color Palette

```css
/* Dashboard Theme */
Primary Blue:    #60A5FA  (Aggregator accent)
Background:      #0F0F0F  (Dark mode base)
Card Background: #1A1A1A  (Dark cards)
Text Primary:    #F5F5F5  (Near white)
Text Secondary:  #A3A3A3  (Light gray)

/* Sentiment Colors */
Positive:        #60A5FA  (Blue)
Negative:        #1E40AF  (Dark blue)
Neutral:         #9CA3AF  (Gray)

/* Platform Brand Colors (Comparison Chart Only) */
DoorDash:        #FF4D4D  (Red)
UberEats:        #06C167  (Green)
GrubHub:         #FB923C  (Orange)
```

## Chart-Specific Colors

### 1. Parent Aspects Bar Chart
- Primary blue bars: `#60A5FA`
- Used for all bars in the chart

### 2. Treemap (Subcategory Breakdown)
- **Blue gradient scale** based on average rating:
  ```css
  [0, '#0A2540']      // Very dark blue (low rating)
  [0.25, '#1E3A5F']   // Dark blue
  [0.5, '#1E40AF']    // Medium dark blue
  [0.75, '#3B82F6']   // Medium blue
  [1, '#93C5FD']      // Light blue (high rating)
  ```

### 3. Top 3 Focus Areas (Intensity Chart)
- Bar colors (ranked):
  1. `#60A5FA` (Primary blue - highest intensity)
  2. `#3B82F6` (Medium blue - second)
  3. `#60A5FA` (Light blue - third)

### 4. Correlation Heatmap
- **Blue gradient scale** for co-occurrence strength:
  ```css
  [0, '#0F0F0F']      // Dark background (no correlation)
  [0.2, '#0A2540']    // Very dark blue
  [0.4, '#1E3A5F']    // Dark blue
  [0.6, '#1E40AF']    // Medium dark blue
  [0.8, '#3B82F6']    // Medium blue
  [1, '#93C5FD']      // Light blue (strong correlation)
  ```

### 5. Sentiment Donut Chart
- Positive: `#93C5FD` (Light blue)
- Negative: `#1E40AF` (Dark blue)
- Neutral: `#9CA3AF` (Gray)

### 6. Platform Comparison Pyramid
- **Uses platform brand colors** (EXCEPTION to blue theme):
  - DoorDash: `#FF4D4D` (Red)
  - UberEats: `#06C167` (Green)
  - GrubHub: `#FB923C` (Orange)
- Allows direct visual association with each platform
- Makes comparisons intuitive and immediately recognizable

## Interactive Elements

### Buttons
- **Reset Button**:
  - Background: `#60A5FA` (Blue)
  - Hover: `#3B82F6` (Darker blue)

### Form Controls
- **Focus/Hover states**: Blue (`#60A5FA`)
- **Checkboxes**: Blue accent (`#60A5FA`)
- **Dropdown borders**: Blue on hover (`#60A5FA`)
