# Multi-Platform Aggregator Dashboard Color Scheme

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

### All Charts (Except Comparison Pyramid)
- Use **blue gradients** for consistency with the aggregator theme
- Includes: Bar charts, treemaps, heatmaps, focus areas

### Platform Comparison Pyramid
- Uses **platform brand colors** (red/green/orange)
- Allows direct visual association with each platform
- Makes comparisons intuitive and immediately recognizable
