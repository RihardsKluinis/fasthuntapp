console.log("projects.js loaded");

document.addEventListener("DOMContentLoaded", function() {
  // Function to handle click events within a project
  function handleProjectClick(event) {
    console.log("Project clicked:", event.target);
    const project = event.target.closest(".project");
    const profiles = project.querySelector(".profiles");
    console.log("Profiles element:", profiles);
    
    if (profiles) {
      if (profiles.style.display === "none" || profiles.style.display === "") {
        profiles.style.display = "block";
        const initialHeight = project.offsetHeight;
        project.style.height = 'auto';
        const expandedHeight = project.offsetHeight;
        project.style.height = initialHeight + 'px';
        setTimeout(() => {
          project.style.height = expandedHeight + 'px';
        }, 0);
      } else {
        const initialHeight = project.offsetHeight;
        profiles.style.display = "none";
        project.style.height = initialHeight + 'px';
        setTimeout(() => {
          project.style.height = '100px'; // Adjust this value to the desired collapsed height
        }, 0);
      }
    }
  }

  // Attach event delegation for project elements
    document.addEventListener("click", function(event) {
      if (event.target.closest(".project")) {
        handleProjectClick(event);
      }
    });

  // Function to handle pagination link clicks
  function handlePaginationClick(event) {
    if (event.target.classList.contains('pagination-link')) {
      console.log("Pagination link clicked");
      event.preventDefault();
      const pageLink = event.target.href;
      const scrollPosition = window.scrollY;

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

        window.scrollTo(0, scrollPosition);
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
