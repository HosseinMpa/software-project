document.addEventListener("DOMContentLoaded", () => {

    const settings = JSON.parse(localStorage.getItem("settings")) || {
        darkMode: false,
        notifyBookings: false,
        notifyMessages: false
    };

    document.getElementById("themeToggle").checked = settings.darkMode;
    document.getElementById("notifyBookings").checked = settings.notifyBookings;
    document.getElementById("notifyMessages").checked = settings.notifyMessages;

    if (settings.darkMode) {
        document.body.classList.add("dark");
    }

    document.getElementById("saveSettings").addEventListener("click", () => {

        const newSettings = {
            darkMode: document.getElementById("themeToggle").checked,
            notifyBookings: document.getElementById("notifyBookings").checked,
            notifyMessages: document.getElementById("notifyMessages").checked
        };

        localStorage.setItem("settings", JSON.stringify(newSettings));

        if (newSettings.darkMode) {
            document.body.classList.add("dark");
        } else {
            document.body.classList.remove("dark");
        }

        alert("تنظیمات ذخیره شد!");
    });

});
