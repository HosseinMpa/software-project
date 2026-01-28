// === Mobile Menu Toggle ===
const menuBtn = document.querySelector('.menu-btn');
const navMenu = document.querySelector('.nav-links');

if (menuBtn) {
    menuBtn.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    });
}

// === Dark Mode Toggle ===
const darkBtn = document.getElementById("darkModeToggle");

if (darkBtn) {
    darkBtn.addEventListener("click", () => {
        document.body.classList.toggle("dark");

        // save mode
        if (document.body.classList.contains("dark")) {
            localStorage.setItem("theme", "dark");
        } else {
            localStorage.setItem("theme", "light");
        }
    });
}

// Load theme
if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark");
}
