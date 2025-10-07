// Filters Module for Multi-Platform Sentiment Analytics Dashboard
// Handles all filter interactions and updates

// Initialize dashboard on page load
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Load data
        await dataProcessor.loadData();

        // Set up date inputs with default range
        document.getElementById('startDate').value = dataProcessor.filters.startDate;
        document.getElementById('endDate').value = dataProcessor.filters.endDate;

        // Render initial dashboard
        updateDashboard();

        // Set up event listeners
        setupFilterListeners();
        setupDropdowns();
        setupPlatformPyramidListeners();

    } catch (error) {
        console.error('Error loading dashboard:', error);
        alert('Failed to load dashboard data. Please check the console for details.');
    }
});

// Set up all filter event listeners
function setupFilterListeners() {
    // Date filters
    document.getElementById('startDate').addEventListener('change', handleDateChange);
    document.getElementById('endDate').addEventListener('change', handleDateChange);

    // Reset button
    document.getElementById('resetFilters').addEventListener('click', resetFilters);
}

// Set up custom dropdown functionality
function setupDropdowns() {
    // Platform filter dropdown
    const platformToggle = document.getElementById('platformFilterToggle');
    const platformMenu = document.getElementById('platformFilterMenu');
    const platformCheckboxes = platformMenu.querySelectorAll('input[type="checkbox"]');

    platformToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        platformMenu.classList.toggle('show');
        platformToggle.classList.toggle('active');
    });

    platformCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => handlePlatformFilterChange(platformCheckboxes));
    });

    // Aspect filter dropdown
    const aspectToggle = document.getElementById('aspectFilterToggle');
    const aspectMenu = document.getElementById('aspectFilterMenu');
    const aspectCheckboxes = aspectMenu.querySelectorAll('input[type="checkbox"]');

    aspectToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        aspectMenu.classList.toggle('show');
        aspectToggle.classList.toggle('active');
    });

    aspectCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => handleAspectFilterChange(aspectCheckboxes));
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', (e) => {
        if (!platformToggle.contains(e.target) && !platformMenu.contains(e.target)) {
            platformMenu.classList.remove('show');
            platformToggle.classList.remove('active');
        }
        if (!aspectToggle.contains(e.target) && !aspectMenu.contains(e.target)) {
            aspectMenu.classList.remove('show');
            aspectToggle.classList.remove('active');
        }
    });
}

// Set up platform pyramid dropdown listeners
function setupPlatformPyramidListeners() {
    const platformADropdown = document.getElementById('platformADropdown');
    const platformBDropdown = document.getElementById('platformBDropdown');

    platformADropdown.addEventListener('change', handlePyramidPlatformChange);
    platformBDropdown.addEventListener('change', handlePyramidPlatformChange);
}

// Handle platform filter changes
function handlePlatformFilterChange(checkboxes) {
    const allCheckbox = Array.from(checkboxes).find(cb => cb.value === 'all');
    const otherCheckboxes = Array.from(checkboxes).filter(cb => cb.value !== 'all');

    // If "All Platforms" is checked
    if (allCheckbox.checked) {
        // Uncheck all others
        otherCheckboxes.forEach(cb => cb.checked = false);
        dataProcessor.filters.platforms = ['all'];
        updatePlatformFilterLabel('All Platforms');
    } else {
        // Get selected platforms
        const selectedPlatforms = otherCheckboxes
            .filter(cb => cb.checked)
            .map(cb => cb.value);

        if (selectedPlatforms.length === 0) {
            // If nothing selected, default to "All"
            allCheckbox.checked = true;
            dataProcessor.filters.platforms = ['all'];
            updatePlatformFilterLabel('All Platforms');
        } else {
            dataProcessor.filters.platforms = selectedPlatforms;

            // Update label
            if (selectedPlatforms.length === 1) {
                const platformName = selectedPlatforms[0].charAt(0).toUpperCase() + selectedPlatforms[0].slice(1);
                updatePlatformFilterLabel(platformName);
            } else {
                updatePlatformFilterLabel(`${selectedPlatforms.length} platforms selected`);
            }
        }
    }

    // Update dashboard
    updateDashboard();
}

// Handle aspect filter changes
function handleAspectFilterChange(checkboxes) {
    const allCheckbox = Array.from(checkboxes).find(cb => cb.value === 'all');
    const otherCheckboxes = Array.from(checkboxes).filter(cb => cb.value !== 'all');

    // If "All Aspects" is checked
    if (allCheckbox.checked) {
        // Uncheck all others
        otherCheckboxes.forEach(cb => cb.checked = false);
        dataProcessor.filters.parentAspects = ['all'];
        updateAspectFilterLabel('All Aspects');
    } else {
        // Get selected aspects
        const selectedAspects = otherCheckboxes
            .filter(cb => cb.checked)
            .map(cb => cb.value);

        if (selectedAspects.length === 0) {
            // If nothing selected, default to "All"
            allCheckbox.checked = true;
            dataProcessor.filters.parentAspects = ['all'];
            updateAspectFilterLabel('All Aspects');
        } else {
            dataProcessor.filters.parentAspects = selectedAspects;

            // Update label
            if (selectedAspects.length === 1) {
                const aspectName = selectedAspects[0].charAt(0).toUpperCase() + selectedAspects[0].slice(1);
                updateAspectFilterLabel(aspectName);
            } else {
                updateAspectFilterLabel(`${selectedAspects.length} aspects selected`);
            }
        }
    }

    // Update only the treemap (aspect filter only affects treemap)
    renderTreemap(dataProcessor.filteredData, dataProcessor.filters.parentAspects);
}

// Handle date filter changes
function handleDateChange() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;

    // Validate dates
    if (startDate && endDate && new Date(startDate) > new Date(endDate)) {
        alert('Start date cannot be after end date');
        return;
    }

    dataProcessor.filters.startDate = startDate;
    dataProcessor.filters.endDate = endDate;

    updateDashboard();
}

// Handle platform pyramid dropdown changes
function handlePyramidPlatformChange() {
    const platformA = document.getElementById('platformADropdown').value;
    const platformB = document.getElementById('platformBDropdown').value;

    // Re-render pyramid chart with new platforms
    renderPlatformPyramid(dataProcessor.filteredData, platformA, platformB);
}

// Reset all filters
function resetFilters() {
    // Reset platform filter
    const platformCheckboxes = document.querySelectorAll('#platformFilterMenu input[type="checkbox"]');
    platformCheckboxes.forEach(cb => {
        cb.checked = cb.value === 'all';
    });
    dataProcessor.filters.platforms = ['all'];
    updatePlatformFilterLabel('All Platforms');

    // Reset date filters
    dataProcessor.setDefaultDateRange();
    document.getElementById('startDate').value = dataProcessor.filters.startDate;
    document.getElementById('endDate').value = dataProcessor.filters.endDate;

    // Reset aspect filter
    const aspectCheckboxes = document.querySelectorAll('#aspectFilterMenu input[type="checkbox"]');
    aspectCheckboxes.forEach(cb => {
        cb.checked = cb.value === 'all';
    });
    dataProcessor.filters.parentAspects = ['all'];
    updateAspectFilterLabel('All Aspects');

    // Reset pyramid dropdowns
    document.getElementById('platformADropdown').value = 'doordash';
    document.getElementById('platformBDropdown').value = 'ubereats';

    // Update dashboard
    updateDashboard();
}

// Update platform filter label
function updatePlatformFilterLabel(text) {
    document.getElementById('platformFilterLabel').textContent = text;
}

// Update aspect filter label
function updateAspectFilterLabel(text) {
    document.getElementById('aspectFilterLabel').textContent = text;
}

// Update entire dashboard
function updateDashboard() {
    // Apply filters to data
    dataProcessor.applyFilters();

    // Update KPIs
    updateKPIs();

    // Render all charts
    renderAllCharts(dataProcessor.filteredData);
}

// Update KPI cards
function updateKPIs() {
    const data = dataProcessor.filteredData;

    // Average Rating
    const avgRating = dataProcessor.calculateAvgRating(data);
    document.getElementById('avgRating').textContent = avgRating;

    // Top Negative Aspect
    const topNegative = dataProcessor.getTopNegativeSubcategory(data);
    document.getElementById('topNegative').textContent = topNegative;

    // Total Reviews
    const totalReviews = dataProcessor.getTotalReviews(data);
    document.getElementById('totalReviews').textContent = totalReviews.toLocaleString();
}
