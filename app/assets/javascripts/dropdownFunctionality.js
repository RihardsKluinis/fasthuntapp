document.addEventListener('DOMContentLoaded', () => {
    const filterContainer = document.querySelector('.filter-container');
    const filterTrigger = document.querySelector('.filter-trigger');
    const filterContent = document.querySelector('.filter-content');

    // Function to open filter content
    const openFilterContent = (applyFilter) => {
        filterContainer.classList.add('is-active');
        if (applyFilter) {
            filterContent.style.transition = 'none'; // Disable transition
            filterContent.style.maxHeight = filterContent.scrollHeight + 'px';
            filterContent.style.opacity = '1';
            setTimeout(() => {
                filterContent.style.transition = ''; // Re-enable transition after setting max-height
            }, 0);
        } else {
            filterContent.style.maxHeight = filterContent.scrollHeight + 'px';
            filterContent.style.opacity = '1';
        }
    };

    // Function to close filter content
    const closeFilterContent = () => {
        filterContent.style.maxHeight = filterContent.scrollHeight + 'px';
        filterContent.offsetHeight; // force repaint
        filterContent.style.maxHeight = '0';
        filterContent.style.opacity = '0';
        filterContainer.addEventListener('transitionend', function handleTransitionEnd() {
            filterContainer.classList.remove('is-active');
            filterContainer.removeEventListener('transitionend', handleTransitionEnd);
        });
    };

    // Toggle filter content on button click
    filterTrigger.addEventListener('click', () => {
        if (filterContainer.classList.contains('is-active')) {
            closeFilterContent();
        } else {
            openFilterContent(false);
        }
    });

    // Keep filters open if any filter is applied
    const isAnyFilterApplied = () => {
        const params = new URLSearchParams(window.location.search);
        return params.has('start_date') || params.has('end_date') || params.has('checkmark_status') || params.has('social_media_list');
    };

    if (isAnyFilterApplied()) {
        openFilterContent(true);
    }

    // Ensure filters remain open after form submission
    document.querySelector('form').addEventListener('ajax:success', () => {
        openFilterContent(true);
    });

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
                if (selectedPlatforms.has(platform)) {
                    selectedPlatforms.delete(platform);
                    icon.classList.remove('is-active');
                    checkbox.checked = false;
                    console.log('Platform removed:', platform);
                } else {
                    selectedPlatforms.add(platform);
                    icon.classList.add('is-active');
                    checkbox.checked = true;
                    console.log('Platform added:', platform);
                }

                const selectedArray = Array.from(selectedPlatforms);
                console.log('Selected Platforms:', selectedArray);
                document.getElementById('social_media_list').value = selectedArray.join(',');
            });
        }
    });

    document.addEventListener('ajax:success', (event) => {
        const [data, status, xhr] = event.detail;
        const projectsContainer = document.getElementById('projects');
        projectsContainer.innerHTML = xhr.responseText;
    });

    document.addEventListener('ajax:error', () => {
        alert('An error occurred while processing your request. Please try again.');
    });
});
