document.addEventListener("DOMContentLoaded", () => {
    const settings = JSON.parse(localStorage.getItem("settings"));

    if (settings && settings.darkMode) {
        document.body.classList.add("dark");
    }
});
