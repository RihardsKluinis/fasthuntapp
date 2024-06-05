console.log("projects.js loaded");

document.addEventListener("DOMContentLoaded", function() {
  // Function to handle image click events
  function handleImageClick(event) {
    console.log("Image clicked:", event.target);
    const profiles = event.target.parentElement.querySelector(".profiles");
    console.log("Profiles element:", profiles);
    if (profiles) {
      profiles.style.display = (profiles.style.display === "none") ? "block" : "none";
    }
  }

  // Attach event delegation for project images
  document.addEventListener("click", function(event) {
    if (event.target.matches(".project img")) {
      handleImageClick(event);
    }
  });

  // Function to handle pagination link clicks
  function handlePaginationClick(event) {
    if (event.target.classList.contains('pagination-link')) {
      console.log("Pagination link clicked");
      event.preventDefault();
      const pageLink = event.target.href;

      fetch(pageLink, {
        headers: {
          'Accept': 'text/html'
        }
      })
      .then(response => response.text())
      .then(data => {
        const parser = new DOMParser();
        const decodedHtml = parser.parseFromString(data, 'text/html');
        console.log("Decoded HTML:", decodedHtml);

        const projectsContainer = document.getElementById('projects');
        projectsContainer.innerHTML = decodedHtml.getElementById('projects').innerHTML;

        const newPagination = decodedHtml.querySelector('.pagination');
        const currentPagination = document.querySelector('.pagination');
        currentPagination.innerHTML = newPagination.innerHTML;
      })
      .catch(error => {
        console.error("Fetch error:", error);
      });
    }
  }

  // Attach event delegation for pagination links
  document.addEventListener('click', function(event) {
    if (event.target.closest('.pagination a')) {
      handlePaginationClick(event);
    }
  });
});
