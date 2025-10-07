// Charts Module for Multi-Platform Sentiment Analytics Dashboard
// Uses Plotly.js for all visualizations with Purple/Blue theme

// Platform brand colors
const PLATFORM_COLORS = {
    doordash: '#FF4D4D',
    ubereats: '#06C167',
    grubhub: '#FF8000'
};

// Chart configuration
const CHART_CONFIG = {
    displayModeBar: false,
    responsive: true
};

const CHART_LAYOUT_BASE = {
    paper_bgcolor: '#1A1A1A',
    plot_bgcolor: '#1A1A1A',
    font: {
        family: 'Inter, sans-serif',
        color: '#F5F5F5'
    },
    margin: { t: 20, r: 20, b: 60, l: 120 }
};

// Render all charts
function renderAllCharts(data) {
    renderAspectBarChart(data);
    renderSentimentDonut(data);
    renderTreemap(data, dataProcessor.filters.parentAspects);
    renderIntensityChart(data);
    renderCorrelationHeatmap(data);

    // Render pyramid with current dropdown selections
    const platformA = document.getElementById('platformADropdown').value;
    const platformB = document.getElementById('platformBDropdown').value;
    renderPlatformPyramid(data, platformA, platformB);
}

// 1. Parent Aspects Bar Chart (Negative Reviews)
function renderAspectBarChart(data) {
    const aspectCounts = dataProcessor.getNegativeByParentAspect(data);

    const aspects = Object.keys(aspectCounts).sort();
    const counts = aspects.map(aspect => aspectCounts[aspect]);

    const trace = {
        x: counts,
        y: aspects,
        type: 'bar',
        orientation: 'h',
        marker: {
            color: '#8B5CF6',
            line: {
                color: '#6D28D9',
                width: 1
            }
        },
        text: counts.map(count => count.toString()),
        textposition: 'outside',
        hovertemplate: '<b>%{y}</b><br>Negative Reviews: %{x}<extra></extra>'
    };

    const layout = {
        ...CHART_LAYOUT_BASE,
        xaxis: {
            title: 'Number of Negative Reviews',
            gridcolor: '#2A2A2A',
            color: '#A3A3A3'
        },
        yaxis: {
            title: '',
            gridcolor: '#2A2A2A',
            color: '#A3A3A3'
        },
        height: 400
    };

    Plotly.newPlot('aspectBarChart', [trace], layout, CHART_CONFIG);
}

// 2. Sentiment Donut Chart
function renderSentimentDonut(data) {
    const distribution = dataProcessor.getSentimentDistribution(data);

    const trace = {
        values: [distribution.positive, distribution.negative, distribution.neutral],
        labels: ['Positive', 'Negative', 'Neutral'],
        type: 'pie',
        hole: 0.4,
        marker: {
            colors: ['#34D399', '#EF4444', '#9CA3AF'],
            line: {
                color: '#1A1A1A',
                width: 2
            }
        },
        textinfo: 'label+percent',
        textfont: {
            size: 14,
            color: '#F5F5F5'
        },
        hovertemplate: '<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    };

    const layout = {
        ...CHART_LAYOUT_BASE,
        showlegend: true,
        legend: {
            orientation: 'h',
            x: 0.5,
            xanchor: 'center',
            y: -0.1,
            font: {
                color: '#A3A3A3'
            }
        },
        height: 400
    };

    Plotly.newPlot('sentimentDonut', [trace], layout, CHART_CONFIG);
}

// 3. Subcategory Treemap (Negative Reviews)
function renderTreemap(data, parentFilter = ['all']) {
    const treemapData = dataProcessor.getSubcategoryTreemapData(data, parentFilter);

    if (treemapData.length === 0) {
        // Show empty state
        const layout = {
            ...CHART_LAYOUT_BASE,
            annotations: [{
                text: 'No data available for selected filters',
                xref: 'paper',
                yref: 'paper',
                x: 0.5,
                y: 0.5,
                showarrow: false,
                font: {
                    size: 16,
                    color: '#A3A3A3'
                }
            }],
            height: 400
        };
        Plotly.newPlot('treemapChart', [], layout, CHART_CONFIG);
        return;
    }

    const labels = treemapData.map(d => d.subcategory);
    const parents = treemapData.map(d => '');
    const values = treemapData.map(d => d.count);
    const avgRatings = treemapData.map(d => parseFloat(d.avgRating));

    // Color scale based on average rating (lower rating = darker red)
    const colorscale = [
        [0, '#7C2D12'],      // Dark red (low rating)
        [0.5, '#DC2626'],    // Medium red
        [1, '#FCA5A5']       // Light red (high rating)
    ];

    const trace = {
        type: 'treemap',
        labels: labels,
        parents: parents,
        values: values,
        marker: {
            colors: avgRatings,
            colorscale: colorscale,
            showscale: true,
            colorbar: {
                title: 'Avg Rating',
                titleside: 'right',
                tickmode: 'linear',
                tick0: 1,
                dtick: 1,
                len: 0.5,
                lenmode: 'fraction',
                thickness: 15,
                thicknessmode: 'pixels',
                outlinewidth: 0
            },
            line: {
                color: '#1A1A1A',
                width: 2
            }
        },
        text: labels.map((label, i) => `${label}<br>Count: ${values[i]}<br>Avg Rating: ${avgRatings[i]}`),
        textposition: 'middle center',
        hovertemplate: '<b>%{label}</b><br>Negative Reviews: %{value}<br>Avg Rating: %{color:.2f}<extra></extra>'
    };

    const layout = {
        ...CHART_LAYOUT_BASE,
        margin: { t: 10, r: 10, b: 10, l: 10 },
        height: 400
    };

    Plotly.newPlot('treemapChart', [trace], layout, CHART_CONFIG);
}

// 4. Top 3 Focus Areas by Intensity
function renderIntensityChart(data) {
    const intensityData = dataProcessor.calculateIntensity(data);
    const top3 = intensityData.slice(0, 3);

    if (top3.length === 0) {
        // Show empty state
        const layout = {
            ...CHART_LAYOUT_BASE,
            annotations: [{
                text: 'No negative reviews found',
                xref: 'paper',
                yref: 'paper',
                x: 0.5,
                y: 0.5,
                showarrow: false,
                font: {
                    size: 16,
                    color: '#A3A3A3'
                }
            }],
            height: 400
        };
        Plotly.newPlot('intensityChart', [], layout, CHART_CONFIG);
        return;
    }

    const subcategories = top3.map(d => d.subcategory);
    const intensities = top3.map(d => d.intensity);

    // Purple gradient for top 3
    const colors = ['#8B5CF6', '#7C3AED', '#6D28D9'];

    const trace = {
        x: intensities,
        y: subcategories,
        type: 'bar',
        orientation: 'h',
        marker: {
            color: colors,
            line: {
                color: '#581C87',
                width: 1
            }
        },
        text: intensities.map(i => i.toFixed(1)),
        textposition: 'outside',
        hovertemplate: '<b>%{y}</b><br>Intensity: %{x:.2f}<extra></extra>'
    };

    const layout = {
        ...CHART_LAYOUT_BASE,
        xaxis: {
            title: 'Intensity Score (6 - Rating)',
            gridcolor: '#2A2A2A',
            color: '#A3A3A3'
        },
        yaxis: {
            title: '',
            gridcolor: '#2A2A2A',
            color: '#A3A3A3',
            autorange: 'reversed'
        },
        height: 400
    };

    Plotly.newPlot('intensityChart', [trace], layout, CHART_CONFIG);
}

// 5. Correlation Heatmap (Jaccard Similarity)
function renderCorrelationHeatmap(data) {
    const { matrix, aspects } = dataProcessor.calculateCorrelationMatrix(data);

    if (aspects.length === 0) {
        // Show empty state
        const layout = {
            ...CHART_LAYOUT_BASE,
            annotations: [{
                text: 'No data available for correlation analysis',
                xref: 'paper',
                yref: 'paper',
                x: 0.5,
                y: 0.5,
                showarrow: false,
                font: {
                    size: 16,
                    color: '#A3A3A3'
                }
            }],
            height: 500
        };
        Plotly.newPlot('correlationHeatmap', [], layout, CHART_CONFIG);
        return;
    }

    // Purple/blue heatmap colorscale
    const colorscale = [
        [0, '#0F0F0F'],      // Very dark (no correlation)
        [0.3, '#3B0764'],    // Dark purple
        [0.5, '#6D28D9'],    // Purple
        [0.7, '#8B5CF6'],    // Light purple
        [1, '#C4B5FD']       // Very light purple
    ];

    const trace = {
        z: matrix,
        x: aspects,
        y: aspects,
        type: 'heatmap',
        colorscale: colorscale,
        showscale: true,
        colorbar: {
            title: 'Jaccard<br>Similarity',
            titleside: 'right',
            len: 0.7,
            lenmode: 'fraction',
            thickness: 20,
            thicknessmode: 'pixels',
            outlinewidth: 0
        },
        hovertemplate: '<b>%{y}</b> ↔ <b>%{x}</b><br>Similarity: %{z:.3f}<extra></extra>'
    };

    const layout = {
        ...CHART_LAYOUT_BASE,
        xaxis: {
            tickangle: -45,
            side: 'bottom',
            color: '#A3A3A3'
        },
        yaxis: {
            color: '#A3A3A3'
        },
        margin: { t: 20, r: 120, b: 120, l: 120 },
        height: Math.max(500, aspects.length * 25),
        width: Math.max(700, aspects.length * 25)
    };

    Plotly.newPlot('correlationHeatmap', [trace], layout, CHART_CONFIG);
}

// 6. NEW: Platform Comparison Pyramid Chart
function renderPlatformPyramid(data, platformA, platformB) {
    const comparisonData = dataProcessor.getPlatformComparisonData(data, platformA, platformB);

    if (comparisonData.subcategories.length === 0) {
        // Show empty state
        const layout = {
            ...CHART_LAYOUT_BASE,
            annotations: [{
                text: 'No negative reviews found for selected platforms',
                xref: 'paper',
                yref: 'paper',
                x: 0.5,
                y: 0.5,
                showarrow: false,
                font: {
                    size: 16,
                    color: '#A3A3A3'
                }
            }],
            height: 600
        };
        Plotly.newPlot('platformPyramid', [], layout, CHART_CONFIG);
        return;
    }

    const subcategories = comparisonData.subcategories;
    const platformAValues = subcategories.map(sub => -(comparisonData.platformA[sub] || 0));
    const platformBValues = subcategories.map(sub => comparisonData.platformB[sub] || 0);

    // Platform A (left side - negative values)
    const traceA = {
        x: platformAValues,
        y: subcategories,
        type: 'bar',
        orientation: 'h',
        name: platformA.charAt(0).toUpperCase() + platformA.slice(1),
        marker: {
            color: PLATFORM_COLORS[platformA.toLowerCase()] || '#8B5CF6',
            line: {
                color: '#1A1A1A',
                width: 1
            }
        },
        text: platformAValues.map(v => Math.abs(v)),
        textposition: 'outside',
        hovertemplate: `<b>${platformA.toUpperCase()}</b><br>%{y}<br>Count: %{text}<extra></extra>`
    };

    // Platform B (right side - positive values)
    const traceB = {
        x: platformBValues,
        y: subcategories,
        type: 'bar',
        orientation: 'h',
        name: platformB.charAt(0).toUpperCase() + platformB.slice(1),
        marker: {
            color: PLATFORM_COLORS[platformB.toLowerCase()] || '#6366F1',
            line: {
                color: '#1A1A1A',
                width: 1
            }
        },
        text: platformBValues,
        textposition: 'outside',
        hovertemplate: `<b>${platformB.toUpperCase()}</b><br>%{y}<br>Count: %{text}<extra></extra>`
    };

    const layout = {
        ...CHART_LAYOUT_BASE,
        barmode: 'overlay',
        xaxis: {
            title: 'Number of Negative Reviews',
            gridcolor: '#2A2A2A',
            color: '#A3A3A3',
            zeroline: true,
            zerolinecolor: '#4B5563',
            zerolinewidth: 2,
            tickvals: (() => {
                const maxA = Math.max(...platformAValues.map(Math.abs));
                const maxB = Math.max(...platformBValues);
                const maxVal = Math.max(maxA, maxB);
                const step = Math.ceil(maxVal / 5);
                const ticks = [];
                for (let i = -maxVal; i <= maxVal; i += step) {
                    ticks.push(i);
                }
                return ticks;
            })(),
            ticktext: (() => {
                const maxA = Math.max(...platformAValues.map(Math.abs));
                const maxB = Math.max(...platformBValues);
                const maxVal = Math.max(maxA, maxB);
                const step = Math.ceil(maxVal / 5);
                const texts = [];
                for (let i = -maxVal; i <= maxVal; i += step) {
                    texts.push(Math.abs(i).toString());
                }
                return texts;
            })()
        },
        yaxis: {
            title: '',
            gridcolor: '#2A2A2A',
            color: '#A3A3A3'
        },
        legend: {
            orientation: 'h',
            x: 0.5,
            xanchor: 'center',
            y: 1.05,
            font: {
                color: '#F5F5F5'
            }
        },
        margin: { t: 60, r: 80, b: 80, l: 200 },
        height: Math.max(600, subcategories.length * 30)
    };

    Plotly.newPlot('platformPyramid', [traceA, traceB], layout, CHART_CONFIG);
}
