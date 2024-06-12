
document.addEventListener('DOMContentLoaded', () => {
    const dropdown = document.querySelector('.dropdown');
    const dropdownTrigger = document.querySelector('.dropdown-trigger');

    dropdownTrigger.addEventListener('click', () => {
        dropdown.classList.toggle('is-active');
    });
});