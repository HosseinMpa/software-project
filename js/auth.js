// auth.js

function getLoggedInUser() {
    return JSON.parse(localStorage.getItem("loggedInUser"));
}

function requireAuth() {
    const user = getLoggedInUser();
    if (!user) {
        window.location.href = "login.html";
    }
}

function requireAdmin() {
    const user = getLoggedInUser();
    if (!user) {
        window.location.href = "login.html";
        return;
    }

    if (user.role !== "admin") {
        alert("⛔ دسترسی غیرمجاز");
        window.location.href = "index.html";
    }
}

function logout() {
    localStorage.removeItem("loggedInUser");
    window.location.href = "login.html";
}
