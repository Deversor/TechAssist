// static/js/main.js
document.addEventListener("DOMContentLoaded", function() {
    console.log("Modern Minimalist Theme Engine Activated.");

    // Highlight the active navigation link based on the current window location path
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (currentPath === href || (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        }
    });
});