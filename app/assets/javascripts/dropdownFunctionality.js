document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded');
    
    const filterContainer = document.querySelector('.filter-container');
    const filterTrigger = document.querySelector('.filter-trigger');
    const filterContent = document.querySelector('.filter-content');
    
    
    console.log('Filter elements selected:', filterContainer, filterTrigger, filterContent);

    // Function to open filter content
    const openFilterContent = (applyFilter) => {
        console.log('Opening filter content');
        filterContainer.classList.add('is-active');
        if (applyFilter) {
            filterContent.style.transition = 'none';
            filterContent.style.maxHeight = filterContent.scrollHeight + 'px';
            filterContent.style.opacity = '1';
            setTimeout(() => {
                filterContent.style.transition = '';
            }, 0);
        } else {
            filterContent.style.maxHeight = filterContent.scrollHeight + 'px';
            filterContent.style.opacity = '1';
        }
    };

    // Function to close filter content
    const closeFilterContent = () => {
        console.log('Closing filter content');
        filterContent.style.maxHeight = filterContent.scrollHeight + 'px';
        filterContent.offsetHeight;
        filterContent.style.maxHeight = '0';
        filterContent.style.opacity = '0';
        filterContainer.addEventListener('transitionend', function handleTransitionEnd() {
            console.log('Transition ended');
            filterContainer.classList.remove('is-active');
            filterContainer.removeEventListener('transitionend', handleTransitionEnd);
        });
    };

    // Toggle filter content on button click
    filterTrigger.addEventListener('click', () => {
        console.log('Filter trigger clicked');
        if (filterContainer.classList.contains('is-active')) {
            closeFilterContent();
        } else {
            openFilterContent(false);
        }
    });

    const isAnyFilterApplied = () => {
        console.log('Checking if any filter is applied');
        const params = new URLSearchParams(window.location.search);
        const hasFilters = params.has('start_date') || params.has('end_date') || params.has('checkmark_status') || params.has('social_media_list');
        console.log('Filters applied:', hasFilters);
        return hasFilters;
    };

    const openFilterContentIfNeeded = () => {
        const filtersApplied = localStorage.getItem('filtersApplied') === 'true';
        const anyFilterApplied = isAnyFilterApplied();

        if (filtersApplied || anyFilterApplied) {
            console.log('Opening filter content');
            openFilterContent(true);
            localStorage.setItem('filtersApplied', 'true');
        } else {
            console.log('No filters applied');
            localStorage.removeItem('filtersApplied');
        }
    };

    // Run the function on page load to check the filter state
    openFilterContentIfNeeded();

    // Ensure filters remain open after form submission
    document.querySelector('form').addEventListener('ajax:success', () => {
        console.log('Form submission successful');
        openFilterContent(true);
        localStorage.setItem('filtersApplied', 'true');
    });

    // Clear filters button click event
    const clearFilterButton = document.getElementById('clear-filter-button');
    if (clearFilterButton) {
        clearFilterButton.addEventListener('click', () => {
            console.log('Clear filters button clicked');
            localStorage.removeItem('filtersApplied');
            location.reload();
        });
    }




    const iconCheckboxes = document.querySelectorAll('.icon-checkbox .social-icon');
    const selectedPlatforms = new Set();

    iconCheckboxes.forEach(icon => {
        const checkbox = icon.previousElementSibling;
        const platform = checkbox.value;

        if (checkbox.dataset.active === "true") {
            selectedPlatforms.add(platform);
            icon.classList.add('is-active');
            checkbox.checked = true;
        }

        if (!icon.dataset.clickListenerAdded) {
            icon.dataset.clickListenerAdded = true;

            icon.addEventListener('click', () => {
                console.log('Social icon clicked');
                if (selectedPlatforms.has(platform)) {
                    selectedPlatforms.delete(platform);
                    icon.classList.remove('is-active');
                    checkbox.checked = false;
                } else {
                    selectedPlatforms.add(platform);
                    icon.classList.add('is-active');
                    checkbox.checked = true;
                }

                const selectedArray = Array.from(selectedPlatforms);
                document.getElementById('social_media_list').value = selectedArray.join(',');
            });
        }
    });

        // Attach submitFilterForm to the form with ID 'filter-form'




    const submitFilterForm = (event) => {
        event.preventDefault();
        console.log('Submitting filter form');
        const form = event.target; // Use event.target to get the form that triggered the event
        const formData = new FormData(form);
        const searchParams = new URLSearchParams(formData).toString();
        const url = `${form.action}?${searchParams}`;
    
        // Disable filter button during submission
        filterTrigger.disabled = true;
    
        Rails.ajax({
            url: url,
            type: 'GET',
            dataType: 'script',
            success: (data) => {
                console.log('Filter form submitted successfully');
                openFilterContent(true);
    
                // Update projects container with new data
                const projectsContainer = document.getElementById('projects');
                projectsContainer.innerHTML = data;

                if (data.display_pagination) {
                    const paginationContainer = document.querySelector('#basic_pagination');
                    paginationContainer.style.display = 'block';
                    paginationContainer.innerHTML = data.pagination_html;
                } else {
                    const paginationContainer = document.querySelector('#basic_pagination');
                    paginationContainer.style.display = 'none';
                }
    
                // Reset filter button state
                resetFilterButtonState();
            },
            error: () => {
                console.error('Error submitting filter form');
                alert('An error occurred while processing your request. Please try again.');
    
                // Reset filter button state on error
                resetFilterButtonState();
            }
        });
    };

    // Attach submitFilterForm to the form with ID 'filter-form'
    const filterForm = document.getElementById('filter-form');
    console.log('We have caught this formL', filterForm);
    filterForm.addEventListener('submit', submitFilterForm);

    // Handle pagination links
    document.addEventListener('click', (event) => {
        if (event.target.matches('.pagination a')) {
            event.preventDefault();
            const url = event.target.href;

            Rails.ajax({
                url: url,
                type: 'GET',
                dataType: 'script',
                success: (data) => {
                    console.log('Pagination link clicked successfully');
                    const projectsContainer = document.getElementById('projects');
                    projectsContainer.innerHTML = data;

                    // Reinitialize pagination links if needed
                    const paginationContainer = document.querySelector('.pagination');
                    paginationContainer.innerHTML = data;
                },
                error: () => {
                    console.error('Error loading pagination link');
                    alert('An error occurred while loading the page. Please try again.');
                }
            });
        }
    });







    
});
