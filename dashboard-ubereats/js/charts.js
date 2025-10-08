// Accent & Air Design System - UberEats Dark Edition
const COLORS = {
    primary: '#06C167',        // UberEats Green (primary accent - brightened for dark mode)
    blue: '#60A5FA',           // Accent blue (brightened)
    gold: '#FBBF24',           // Accent gold (brightened)
    gray: '#9CA3AF',           // Accent gray (brightened)
    teal: '#2DD4BF',           // Accent teal (brightened)
    positive: '#34D399',       // Success green (brightened)
    negative: '#06C167',       // Error green (same as primary)
    neutral: '#A3A3A3',        // Neutral gray (brightened)
    gradientStart: '#06C167',  // UberEats green
    gradientEnd: '#05A858'     // Darker green
};

// Common layout settings for dark mode
const commonLayout = {
    font: {
        family: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        size: 12,
        color: '#F5F5F5'
    },
    paper_bgcolor: '#1A1A1A',
    plot_bgcolor: '#0F0F0F',
    margin: { t: 40, r: 20, b: 60, l: 80 },
    hoverlabel: {
        bgcolor: '#2A2A2A',
        font: { color: '#F5F5F5', size: 13 }
    }
};

const config = {
    responsive: true,
    displayModeBar: true,
    displaylogo: false,
    modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d', 'autoScale2d']
};

const treemapConfig = {
    ...config,
    toImageButtonOptions: {
        format: 'png',
        filename: 'treemap',
        height: 500,
        width: 700,
        scale: 1
    },
    setBackground: 'transparent'
};

// 1. Parent Aspects vs Negative Reviews Bar Chart
function renderAspectBarChart(data) {
    const negativeData = getNegativeByParentAspect(data);
    const aspects = Object.keys(negativeData).sort((a, b) => negativeData[b] - negativeData[a]);
    const counts = aspects.map(a => negativeData[a]);
    const total = counts.reduce((a, b) => a + b, 0);

    const trace = {
        x: aspects.map(a => a.charAt(0).toUpperCase() + a.slice(1)),
        y: counts,
        type: 'bar',
        marker: {
            color: COLORS.primary,
            line: { color: '#0F0F0F', width: 1 }
        },
        text: counts.map((c, i) => `${c} (${((c / total) * 100).toFixed(1)}%)`),
        textposition: 'outside',
        hovertemplate: '<b>%{x}</b><br>' +
                       'Negative Reviews: %{y}<br>' +
                       'Percentage: %{text}<br>' +
                       '<extra></extra>'
    };

    const layout = {
        ...commonLayout,
        xaxis: {
            title: 'Parent Aspect',
            tickangle: -45,
            gridcolor: '#2A2A2A',
            color: '#A3A3A3'
        },
        yaxis: {
            title: 'Number of Negative Reviews',
            gridcolor: '#2A2A2A',
            color: '#A3A3A3'
        }
    };

    Plotly.newPlot('aspectBarChart', [trace], layout, config);
}

// 2. Subcategory Treemap
function renderTreemap(data, parentFilter = 'all') {
    const treemapData = getSubcategoryTreemapData(data, parentFilter);

    if (treemapData.length === 0) {
        const layout = {
            ...commonLayout,
            annotations: [{
                text: 'No data available for selected filters',
                showarrow: false,
                font: { size: 16, color: '#696969' }
            }],
            xaxis: { visible: false },
            yaxis: { visible: false }
        };
        Plotly.newPlot('treemapChart', [], layout, config);
        return;
    }

    const labels = treemapData.map(d => d.subcategory.replace(/_/g, ' ').toUpperCase());
    const parents = treemapData.map(d => '');
    const values = treemapData.map(d => d.count);
    const avgRatings = treemapData.map(d => parseFloat(d.avgRating));

    const trace = {
        type: 'treemap',
        labels: labels,
        parents: parents,
        values: values,
        text: treemapData.map(d => `${d.count} reviews`),
        textposition: 'middle center',
        marker: {
            colors: avgRatings,
            colorscale: [
                [0, '#022C22'],      // Very dark green (low rating)
                [0.25, '#064E3B'],   // Dark green
                [0.5, '#05A858'],    // Green
                [0.75, '#06C167'],   // UberEats green (bright)
                [1, '#6EE7B7']       // Light green
            ],
            showscale: true,
            colorbar: {
                title: { text: 'Avg Rating', font: { color: '#F5F5F5' } },
                thickness: 15,
                len: 0.7,
                tickfont: { color: '#A3A3A3' },
                bgcolor: 'rgba(0,0,0,0)',
                outlinewidth: 0
            },
            line: { color: '#0F0F0F', width: 2 }
        },
        hovertemplate: '<b>%{label}</b><br>' +
                       'Reviews: %{value}<br>' +
                       'Avg Rating: %{color:.2f}<br>' +
                       '<extra></extra>'
    };

    const layout = {
        font: {
            family: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
            size: 12,
            color: '#F5F5F5'
        },
        paper_bgcolor: '#1A1A1A',
        plot_bgcolor: '#1A1A1A',
        margin: { t: 0, r: 0, b: 0, l: 0 },
        hoverlabel: {
            bgcolor: '#2A2A2A',
            font: { color: '#F5F5F5', size: 13 }
        }
    };

    Plotly.newPlot('treemapChart', [trace], layout, treemapConfig);
}

// 3. Top 3 Focus Areas (Intensity Chart)
function renderIntensityChart(data) {
    const intensityData = calculateIntensity(data).slice(0, 3);

    if (intensityData.length === 0) {
        const layout = {
            ...commonLayout,
            annotations: [{
                text: 'No negative reviews in selected period',
                showarrow: false,
                font: { size: 16, color: '#696969' }
            }],
            xaxis: { visible: false },
            yaxis: { visible: false }
        };
        Plotly.newPlot('intensityChart', [], layout, config);
        return;
    }

    const trace = {
        x: intensityData.map(d => d.intensity),
        y: intensityData.map(d => d.subcategory.replace(/_/g, ' ').toUpperCase()),
        type: 'bar',
        orientation: 'h',
        marker: {
            color: [COLORS.primary, '#10B981', '#34D399'],
            line: { color: '#0F0F0F', width: 1 }
        },
        text: intensityData.map(d => `Intensity: ${d.intensity.toFixed(0)}`),
        textposition: 'outside',
        hovertemplate: '<b>%{y}</b><br>' +
                       'Total Intensity: %{x:.0f}<br>' +
                       'Review Count: %{customdata}<br>' +
                       '<extra></extra>',
        customdata: intensityData.map(d => d.count)
    };

    const layout = {
        ...commonLayout,
        xaxis: {
            title: 'Total Intensity Score (6 - Rating)',
            gridcolor: '#2A2A2A',
            color: '#A3A3A3'
        },
        yaxis: {
            title: '',
            automargin: true,
            color: '#A3A3A3'
        }
    };

    Plotly.newPlot('intensityChart', [trace], layout, config);
}

// 4. Correlation Heatmap (Subcategories) - Matching reference PNG
function renderCorrelationHeatmap(data) {
    const { matrix, subcategories } = calculateCorrelationMatrix(data);

    const z = subcategories.map(s1 => subcategories.map(s2 => matrix[s1][s2]));
    const labels = subcategories.map(s => s.replace(/_/g, ' '));

    const trace = {
        z: z,
        x: labels,
        y: labels,
        type: 'heatmap',
        colorscale: [
            [0, '#0F0F0F'],      // Dark background (no correlation)
            [0.2, '#022C22'],    // Very dark green
            [0.4, '#064E3B'],    // Dark green
            [0.6, '#05A858'],    // Medium green
            [0.8, '#06C167'],    // UberEats green (bright)
            [1, '#6EE7B7']       // Light green (strong correlation)
        ],
        showscale: true,
        colorbar: {
            title: {
                text: 'Jaccard Similarity<br>(Co-occurrence Rate)',
                font: { size: 11, color: '#F5F5F5' }
            },
            thickness: 20,
            len: 0.8,
            x: 1.02,
            tickfont: { color: '#A3A3A3' }
        },
        hovertemplate: '<b>%{y} & %{x}</b><br>' +
                       'Co-occurrence: %{z:.4f}<br>' +
                       '<extra></extra>',
        xgap: 1,
        ygap: 1
    };

    // Get container width to make heatmap fill the card
    const container = document.getElementById('correlationHeatmap');
    const containerWidth = container.offsetWidth;
    const size = Math.min(containerWidth - 300, 1000); // Leave room for margins and colorbar

    const layout = {
        ...commonLayout,
        plot_bgcolor: '#0F0F0F',
        paper_bgcolor: '#1A1A1A',
        xaxis: {
            side: 'bottom',
            tickangle: -45,
            tickfont: { size: 10, color: '#A3A3A3' },
            gridcolor: '#2A2A2A',
            showgrid: true
        },
        yaxis: {
            tickfont: { size: 10, color: '#A3A3A3' },
            gridcolor: '#2A2A2A',
            showgrid: true,
            scaleanchor: 'x',
            scaleratio: 1
        },
        margin: { t: 40, r: 120, b: 180, l: 150 },
        width: size,
        height: size
    };

    Plotly.newPlot('correlationHeatmap', [trace], layout, config);
}

// 5. Sentiment Distribution Donut Chart
function renderSentimentDonut(data) {
    const sentimentCounts = getSentimentDistribution(data);

    const trace = {
        values: [sentimentCounts.positive, sentimentCounts.negative, sentimentCounts.neutral],
        labels: ['Positive', 'Negative', 'Neutral'],
        type: 'pie',
        hole: 0.55,
        domain: { y: [0.15, 1] },
        marker: {
            colors: ['#10B981', '#065F46', '#9CA3AF'],  // Light green (positive), Dark green (negative), Gray (neutral)
            line: { color: '#0F0F0F', width: 2 }
        },
        textinfo: 'label+percent',
        textposition: 'outside',
        hovertemplate: '<b>%{label}</b><br>' +
                       'Count: %{value}<br>' +
                       'Percentage: %{percent}<br>' +
                       '<extra></extra>'
    };

    const layout = {
        ...commonLayout,
        showlegend: true,
        legend: {
            orientation: 'h',
            yanchor: 'top',
            y: -0.05,
            xanchor: 'center',
            x: 0.5,
            font: { color: '#F5F5F5' }
        },
        margin: { t: 20, r: 20, b: 80, l: 20 }
    };

    Plotly.newPlot('sentimentDonut', [trace], layout, config);
}

// Render all charts
function renderAllCharts(data) {
    // Get checked checkboxes from custom dropdown
    const checkboxes = document.querySelectorAll('.aspect-checkbox:checked');

    // Safety check: if checkboxes don't exist yet, default to 'all'
    let aspectFilter = 'all';

    if (checkboxes && checkboxes.length > 0) {
        const checkedBoxes = Array.from(checkboxes);
        const selectedValues = checkedBoxes.map(cb => cb.value);

        // If "all" is selected or nothing is selected, pass 'all'
        aspectFilter = selectedValues.includes('all') || selectedValues.length === 0
            ? 'all'
            : selectedValues;
    }

    renderAspectBarChart(data);
    renderTreemap(data, aspectFilter);
    renderIntensityChart(data);
    renderCorrelationHeatmap(data);
    renderSentimentDonut(data);
}
