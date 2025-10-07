// Data Processor for Multi-Platform Sentiment Analytics Dashboard
// Handles data loading, filtering, and calculations

class DataProcessor {
    constructor() {
        this.rawData = [];
        this.filteredData = [];
        this.filters = {
            platforms: ['all'],
            startDate: null,
            endDate: null,
            parentAspects: ['all']
        };
    }

    // Load CSV data with PapaParse (ALL platforms - no filter)
    async loadData() {
        return new Promise((resolve, reject) => {
            Papa.parse('data/complete_analysis_20251003_234035.csv', {
                download: true,
                header: true,
                skipEmptyLines: true,
                complete: (results) => {
                    this.rawData = results.data;
                    this.filteredData = [...this.rawData];
                    this.setDefaultDateRange();
                    resolve(this.rawData);
                },
                error: (error) => {
                    reject(error);
                }
            });
        });
    }

    // Set default date range from data
    setDefaultDateRange() {
        const dates = this.rawData
            .map(row => new Date(row.date))
            .filter(date => !isNaN(date));

        if (dates.length > 0) {
            const minDate = new Date(Math.min(...dates));
            const maxDate = new Date(Math.max(...dates));

            this.filters.startDate = minDate.toISOString().split('T')[0];
            this.filters.endDate = maxDate.toISOString().split('T')[0];
        }
    }

    // Apply all filters
    applyFilters() {
        this.filteredData = this.rawData.filter(row => {
            // Platform filter
            const platformMatch = this.filters.platforms.includes('all') ||
                                 this.filters.platforms.includes(row.platform.toLowerCase());

            // Date filter
            const rowDate = new Date(row.date);
            const dateMatch = rowDate >= new Date(this.filters.startDate) &&
                            rowDate <= new Date(this.filters.endDate);

            // Parent aspect filter (only affects treemap, but we'll keep data unfiltered here)
            // Parent aspect filtering is applied in the specific chart functions

            return platformMatch && dateMatch;
        });
    }

    // Calculate average rating (fixed to group by review_id first)
    calculateAvgRating(data) {
        if (!data || data.length === 0) return 0;

        // Group by review_id to get unique reviews
        const uniqueReviews = {};
        data.forEach(row => {
            if (row.review_id && row.rating) {
                uniqueReviews[row.review_id] = parseFloat(row.rating);
            }
        });

        const ratings = Object.values(uniqueReviews);
        if (ratings.length === 0) return 0;

        const sum = ratings.reduce((acc, rating) => acc + rating, 0);
        return (sum / ratings.length).toFixed(2);
    }

    // Calculate intensity (6 - rating for negative reviews)
    calculateIntensity(data) {
        const intensityMap = {};

        data.forEach(row => {
            if (row.sentiment === 'negative' && row.rating && row.subcategory) {
                const rating = parseFloat(row.rating);
                const intensity = 6 - rating;
                const subcategory = row.subcategory;

                if (!intensityMap[subcategory]) {
                    intensityMap[subcategory] = { intensity: 0, count: 0 };
                }

                intensityMap[subcategory].intensity += intensity;
                intensityMap[subcategory].count += 1;
            }
        });

        // Convert to array and sort by total intensity
        return Object.entries(intensityMap)
            .map(([subcategory, data]) => ({
                subcategory,
                intensity: data.intensity,
                count: data.count
            }))
            .sort((a, b) => b.intensity - a.intensity);
    }

    // Get top negative subcategory
    getTopNegativeSubcategory(data) {
        const subcategoryCounts = {};

        data.forEach(row => {
            if (row.sentiment === 'negative' && row.subcategory) {
                subcategoryCounts[row.subcategory] = (subcategoryCounts[row.subcategory] || 0) + 1;
            }
        });

        if (Object.keys(subcategoryCounts).length === 0) return 'N/A';

        const topSubcategory = Object.entries(subcategoryCounts)
            .sort((a, b) => b[1] - a[1])[0];

        return `${topSubcategory[0]} (${topSubcategory[1]})`;
    }

    // Calculate correlation matrix (Jaccard similarity)
    calculateCorrelationMatrix(data) {
        // Group reviews by review_id
        const reviewAspects = {};

        data.forEach(row => {
            if (!reviewAspects[row.review_id]) {
                reviewAspects[row.review_id] = new Set();
            }
            if (row.subcategory) {
                reviewAspects[row.review_id].add(row.subcategory);
            }
        });

        // Get unique subcategories
        const subcategories = [...new Set(data.map(row => row.subcategory).filter(Boolean))].sort();

        // Calculate Jaccard similarity matrix
        const matrix = [];
        subcategories.forEach(aspect1 => {
            const row = [];
            subcategories.forEach(aspect2 => {
                let intersection = 0;
                let union = 0;

                Object.values(reviewAspects).forEach(aspects => {
                    const hasAspect1 = aspects.has(aspect1);
                    const hasAspect2 = aspects.has(aspect2);

                    if (hasAspect1 || hasAspect2) union++;
                    if (hasAspect1 && hasAspect2) intersection++;
                });

                const similarity = union > 0 ? intersection / union : 0;
                row.push(similarity);
            });
            matrix.push(row);
        });

        return { matrix, aspects: subcategories };
    }

    // Get top correlation pair
    getTopCorrelation(data) {
        const { matrix, aspects } = this.calculateCorrelationMatrix(data);

        let maxSimilarity = 0;
        let topPair = '';

        for (let i = 0; i < matrix.length; i++) {
            for (let j = i + 1; j < matrix[i].length; j++) {
                if (matrix[i][j] > maxSimilarity) {
                    maxSimilarity = matrix[i][j];
                    topPair = `${aspects[i]} ↔ ${aspects[j]}`;
                }
            }
        }

        return { pair: topPair || 'N/A', similarity: maxSimilarity.toFixed(3) };
    }

    // Get negative counts by parent aspect
    getNegativeByParentAspect(data) {
        const aspectCounts = {};

        data.forEach(row => {
            if (row.sentiment === 'negative' && row.parent_aspect) {
                aspectCounts[row.parent_aspect] = (aspectCounts[row.parent_aspect] || 0) + 1;
            }
        });

        return aspectCounts;
    }

    // Get subcategory treemap data (negative only, with parent filter)
    getSubcategoryTreemapData(data, parentFilter = ['all']) {
        const subcategoryData = {};

        data.forEach(row => {
            if (row.sentiment === 'negative' && row.subcategory && row.parent_aspect) {
                // Apply parent aspect filter
                if (!parentFilter.includes('all') && !parentFilter.includes(row.parent_aspect.toLowerCase())) {
                    return;
                }

                if (!subcategoryData[row.subcategory]) {
                    subcategoryData[row.subcategory] = {
                        count: 0,
                        totalRating: 0,
                        parent: row.parent_aspect
                    };
                }

                subcategoryData[row.subcategory].count += 1;
                subcategoryData[row.subcategory].totalRating += parseFloat(row.rating || 0);
            }
        });

        return Object.entries(subcategoryData).map(([subcategory, data]) => ({
            subcategory,
            count: data.count,
            avgRating: (data.totalRating / data.count).toFixed(2),
            parent: data.parent
        }));
    }

    // Get sentiment distribution
    getSentimentDistribution(data) {
        const distribution = { positive: 0, negative: 0, neutral: 0 };

        data.forEach(row => {
            if (row.sentiment) {
                distribution[row.sentiment] = (distribution[row.sentiment] || 0) + 1;
            }
        });

        return distribution;
    }

    // NEW: Get platform comparison data
    getPlatformComparisonData(data, platformA, platformB) {
        const platformAData = {};
        const platformBData = {};

        data.forEach(row => {
            if (row.sentiment === 'negative' && row.subcategory && row.platform) {
                const platform = row.platform.toLowerCase();

                if (platform === platformA.toLowerCase()) {
                    platformAData[row.subcategory] = (platformAData[row.subcategory] || 0) + 1;
                } else if (platform === platformB.toLowerCase()) {
                    platformBData[row.subcategory] = (platformBData[row.subcategory] || 0) + 1;
                }
            }
        });

        // Get all subcategories from both platforms
        const allSubcategories = new Set([
            ...Object.keys(platformAData),
            ...Object.keys(platformBData)
        ]);

        // Format data for pyramid chart
        return {
            subcategories: Array.from(allSubcategories).sort(),
            platformA: platformAData,
            platformB: platformBData
        };
    }

    // Get total review count
    getTotalReviews(data) {
        const uniqueReviews = new Set(data.map(row => row.review_id));
        return uniqueReviews.size;
    }
}

// Create global instance
const dataProcessor = new DataProcessor();
