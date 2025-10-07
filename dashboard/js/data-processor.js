// Global data storage
let rawData = [];
let filteredData = [];
let dateRange = { start: null, end: null };

// Initialize dashboard
async function initializeDashboard() {
    try {
        await loadData();
        setDefaultDateRange();
        updateDashboard();
    } catch (error) {
        console.error('Error initializing dashboard:', error);
        alert('Error loading data. Please check console for details.');
    }
}

// Load CSV data
function loadData() {
    return new Promise((resolve, reject) => {
        Papa.parse('data/complete_analysis_20251003_234035.csv', {
            download: true,
            header: true,
            skipEmptyLines: true,
            complete: (results) => {
                rawData = results.data.map(row => ({
                    review_id: row.review_id,
                    review_text: row.review_text,
                    subcategory: row.subcategory,
                    parent_aspect: row.parent_aspect,
                    sentiment: row.sentiment,
                    confidence: parseFloat(row.confidence),
                    rating: parseInt(row.rating),
                    date: new Date(row.date),
                    platform: row.platform
                }));
                filteredData = [...rawData];
                console.log(`Loaded ${rawData.length} records`);
                resolve();
            },
            error: (error) => reject(error)
        });
    });
}

// Set default date range from data
function setDefaultDateRange() {
    const dates = rawData.map(d => d.date).filter(d => !isNaN(d));
    const minDate = new Date(Math.min(...dates));
    const maxDate = new Date(Math.max(...dates));

    dateRange.start = minDate;
    dateRange.end = maxDate;

    document.getElementById('startDate').value = minDate.toISOString().split('T')[0];
    document.getElementById('endDate').value = maxDate.toISOString().split('T')[0];
}

// Apply filters to data
function applyFilters() {
    const startDate = new Date(document.getElementById('startDate').value);
    const endDate = new Date(document.getElementById('endDate').value);

    // Get selected aspects from custom dropdown checkboxes
    const checkedBoxes = document.querySelectorAll('.aspect-checkbox:checked');
    const selectedAspects = checkedBoxes && checkedBoxes.length > 0
        ? Array.from(checkedBoxes).map(cb => cb.value)
        : ['all'];

    filteredData = rawData.filter(row => {
        const dateMatch = row.date >= startDate && row.date <= endDate;
        const aspectMatch = selectedAspects.includes('all') || selectedAspects.includes(row.parent_aspect);
        return dateMatch && aspectMatch;
    });

    return filteredData;
}

// Calculate average rating
function calculateAvgRating(data) {
    const ratings = data.map(d => d.rating).filter(r => !isNaN(r));
    if (ratings.length === 0) return 0;
    return (ratings.reduce((a, b) => a + b, 0) / ratings.length).toFixed(2);
}

// Calculate intensity (6 - rating) for negative reviews
function calculateIntensity(data) {
    const negativeReviews = data.filter(d => d.sentiment === 'negative');
    const intensityBySubcat = {};

    negativeReviews.forEach(row => {
        const intensity = 6 - row.rating;
        if (!intensityBySubcat[row.subcategory]) {
            intensityBySubcat[row.subcategory] = { total: 0, count: 0 };
        }
        intensityBySubcat[row.subcategory].total += intensity;
        intensityBySubcat[row.subcategory].count += 1;
    });

    return Object.entries(intensityBySubcat)
        .map(([subcat, data]) => ({
            subcategory: subcat,
            intensity: data.total,
            count: data.count
        }))
        .sort((a, b) => b.intensity - a.intensity);
}

// Get top negative subcategory by intensity
function getTopNegativeSubcategory(data) {
    const intensityData = calculateIntensity(data);
    return intensityData.length > 0 ? intensityData[0].subcategory : 'N/A';
}

// Calculate co-occurrence correlation matrix for SUBCATEGORIES
function calculateCorrelationMatrix(data) {
    const subcategories = [...new Set(data.map(d => d.subcategory))].sort();
    const reviewGroups = {};

    // Group by review_id
    data.forEach(row => {
        if (!reviewGroups[row.review_id]) {
            reviewGroups[row.review_id] = new Set();
        }
        reviewGroups[row.review_id].add(row.subcategory);
    });

    // Calculate Jaccard Similarity (co-occurrence rate)
    const matrix = {};
    subcategories.forEach(s1 => {
        matrix[s1] = {};
        subcategories.forEach(s2 => {
            if (s1 === s2) {
                matrix[s1][s2] = 1.0; // Diagonal is always 1
            } else {
                // Count intersection (both appear together)
                let intersection = 0;
                // Count union (either appears)
                let union = 0;

                Object.values(reviewGroups).forEach(subcatSet => {
                    const hasS1 = subcatSet.has(s1);
                    const hasS2 = subcatSet.has(s2);

                    if (hasS1 && hasS2) {
                        intersection++;
                    }
                    if (hasS1 || hasS2) {
                        union++;
                    }
                });

                // Jaccard Similarity = intersection / union
                matrix[s1][s2] = union > 0 ? intersection / union : 0;
            }
        });
    });

    return { matrix, subcategories };
}

// Get top correlation pair
function getTopCorrelation(data) {
    const { matrix, subcategories } = calculateCorrelationMatrix(data);
    let maxCorr = 0;
    let maxPair = '';

    subcategories.forEach(s1 => {
        subcategories.forEach(s2 => {
            if (s1 !== s2 && matrix[s1][s2] > maxCorr) {
                maxCorr = matrix[s1][s2];
                maxPair = `${s1} & ${s2}`;
            }
        });
    });

    return { pair: maxPair.replace(/_/g, ' '), count: maxCorr.toFixed(2) };
}

// Calculate percentage of reviews mentioning top aspect
function calculateTopAspectPercentage(data) {
    const topNegative = getTopNegativeSubcategory(data);
    const uniqueReviewIds = new Set(data.map(d => d.review_id));
    const reviewsWithTopAspect = new Set(
        data.filter(d => d.subcategory === topNegative).map(d => d.review_id)
    );

    const percentage = (reviewsWithTopAspect.size / uniqueReviewIds.size) * 100;
    return { percentage: percentage.toFixed(1), subcategory: topNegative };
}

// Get negative reviews by parent aspect
function getNegativeByParentAspect(data) {
    const negative = data.filter(d => d.sentiment === 'negative');
    const counts = {};

    negative.forEach(row => {
        counts[row.parent_aspect] = (counts[row.parent_aspect] || 0) + 1;
    });

    return counts;
}

// Get subcategory data for treemap (negative only)
function getSubcategoryTreemapData(data, parentFilter = 'all') {
    let filtered = data.filter(d => d.sentiment === 'negative');

    if (parentFilter !== 'all') {
        // Handle both string and array for parentFilter
        if (Array.isArray(parentFilter)) {
            filtered = filtered.filter(d => parentFilter.includes(d.parent_aspect));
        } else {
            filtered = filtered.filter(d => d.parent_aspect === parentFilter);
        }
    }

    const subcatData = {};

    filtered.forEach(row => {
        if (!subcatData[row.subcategory]) {
            subcatData[row.subcategory] = {
                count: 0,
                totalRating: 0,
                parent: row.parent_aspect
            };
        }
        subcatData[row.subcategory].count += 1;
        subcatData[row.subcategory].totalRating += row.rating;
    });

    return Object.entries(subcatData).map(([subcat, data]) => ({
        subcategory: subcat,
        count: data.count,
        avgRating: (data.totalRating / data.count).toFixed(2),
        parent: data.parent
    }));
}

// Get sentiment distribution
function getSentimentDistribution(data) {
    const counts = { positive: 0, negative: 0, neutral: 0 };

    data.forEach(row => {
        if (counts.hasOwnProperty(row.sentiment)) {
            counts[row.sentiment] += 1;
        }
    });

    return counts;
}

// Update all KPIs
function updateKPIs(data) {
    const avgRating = calculateAvgRating(data);
    const topNegative = getTopNegativeSubcategory(data);
    const topCorr = getTopCorrelation(data);
    const uniqueReviews = new Set(data.map(d => d.review_id)).size;

    document.getElementById('avgRating').textContent = avgRating;
    document.getElementById('topNegative').textContent = topNegative.replace(/_/g, ' ');
    document.getElementById('topCorrelation').textContent = `${topCorr.pair} (${topCorr.count})`;
    document.getElementById('totalReviews').textContent = uniqueReviews.toLocaleString();
}

// Main update function
function updateDashboard() {
    const data = applyFilters();
    updateKPIs(data);
    renderAllCharts(data);
}
