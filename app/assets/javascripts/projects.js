// projects.js
document.addEventListener("DOMContentLoaded", function() {
  const projectImages = document.querySelectorAll(".project img");

  projectImages.forEach(projectImage => {
    projectImage.addEventListener("click", function() {
      const profiles = this.parentElement.querySelector(".profiles");

      if (profiles) {
        profiles.classList.toggle("hidden");
      }
    });
  });
});