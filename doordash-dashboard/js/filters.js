// Filter event listeners and interactions

// Initialize filters
function initializeFilters() {
    // Date filter listeners with validation
    document.getElementById('startDate').addEventListener('change', () => {
        if (validateDateRange()) {
            updateDashboard();
        }
    });

    document.getElementById('endDate').addEventListener('change', () => {
        if (validateDateRange()) {
            updateDashboard();
        }
    });

    // Custom dropdown toggle
    const dropdownButton = document.getElementById('aspectDropdownButton');
    const dropdownMenu = document.getElementById('aspectDropdownMenu');

    if (dropdownButton && dropdownMenu) {
        dropdownButton.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdownButton.classList.toggle('open');
            dropdownMenu.classList.toggle('show');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', () => {
            dropdownButton.classList.remove('open');
            dropdownMenu.classList.remove('show');
        });

        // Prevent dropdown from closing when clicking inside
        dropdownMenu.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }

    // Checkbox change listeners
    const checkboxes = document.querySelectorAll('.aspect-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', handleAspectCheckboxChange);
    });

    // Reset filters button
    document.getElementById('resetFilters').addEventListener('click', () => {
        resetAllFilters();
    });

    // Platform comparison selectors
    const leftPlatformSelect = document.getElementById('leftPlatform');
    const rightPlatformSelect = document.getElementById('rightPlatform');

    if (leftPlatformSelect && rightPlatformSelect) {
        leftPlatformSelect.addEventListener('change', () => {
            updateDashboard();
        });

        rightPlatformSelect.addEventListener('change', () => {
            updateDashboard();
        });
    }
}

// Handle aspect checkbox changes
function handleAspectCheckboxChange(event) {
    const allCheckbox = document.querySelector('.aspect-checkbox[value="all"]');
    const otherCheckboxes = document.querySelectorAll('.aspect-checkbox:not([value="all"])');

    if (event.target.value === 'all') {
        // If "All" is checked, uncheck others
        if (event.target.checked) {
            otherCheckboxes.forEach(cb => cb.checked = false);
        }
    } else {
        // If any other checkbox is checked, uncheck "All"
        if (event.target.checked) {
            allCheckbox.checked = false;
        }
        // If no checkboxes are checked, check "All"
        const anyChecked = Array.from(otherCheckboxes).some(cb => cb.checked);
        if (!anyChecked) {
            allCheckbox.checked = true;
        }
    }

    // Update dropdown button label
    updateDropdownLabel();

    // Update dashboard
    updateDashboard();
}

// Update dropdown button label based on selections
function updateDropdownLabel() {
    const checkedBoxes = Array.from(document.querySelectorAll('.aspect-checkbox:checked'));
    const label = document.getElementById('dropdownLabel');

    if (checkedBoxes.length === 0 || checkedBoxes[0].value === 'all') {
        label.textContent = 'All Aspects';
    } else if (checkedBoxes.length === 1) {
        label.textContent = checkedBoxes[0].dataset.label;
    } else {
        label.textContent = `${checkedBoxes.length} aspects selected`;
    }
}

// Reset all filters to default
function resetAllFilters() {
    // Reset date range to full data range
    setDefaultDateRange();

    // Reset aspect checkboxes to "all"
    const allCheckbox = document.querySelector('.aspect-checkbox[value="all"]');
    const otherCheckboxes = document.querySelectorAll('.aspect-checkbox:not([value="all"])');
    allCheckbox.checked = true;
    otherCheckboxes.forEach(cb => cb.checked = false);

    // Update dropdown label
    updateDropdownLabel();

    // Update dashboard
    updateDashboard();
}

// Validate date range
function validateDateRange() {
    const startDate = new Date(document.getElementById('startDate').value);
    const endDate = new Date(document.getElementById('endDate').value);

    if (startDate > endDate) {
        alert('Start date cannot be after end date. Please adjust your selection.');
        setDefaultDateRange();
        return false;
    }

    return true;
}

// Export functions for use in other modules
window.initializeFilters = initializeFilters;
window.resetAllFilters = resetAllFilters;
window.validateDateRange = validateDateRange;
window.handleAspectCheckboxChange = handleAspectCheckboxChange;
window.updateDropdownLabel = updateDropdownLabel;
