// login.js

// Seed Admin (فقط اگر وجود نداشت)
const users = JSON.parse(localStorage.getItem("users")) || [];

const adminExists = users.some(u => u.role === "admin");

if (!adminExists) {
    users.push({
        username: "admin",
        password: "1234",
        role: "admin"
    });

    localStorage.setItem("users", JSON.stringify(users));
}

document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("loginForm");

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value;

        if (!username || !password) {
            alert("نام کاربری و رمز عبور را وارد کنید");
            return;
        }

        // دریافت کاربران ثبت‌نام‌شده
        const users = JSON.parse(localStorage.getItem("users")) || [];

        // پیدا کردن کاربر
        const user = users.find(
            u => u.username === username && u.password === password
        );

        if (!user) {
            alert("نام کاربری یا رمز عبور اشتباه است");
            return;
        }

        // ذخیره سشن ورود
        localStorage.setItem("loggedInUser", JSON.stringify({
            id: user.id,
            fullname: user.fullname,
            username: user.username,
            role: user.role
        }));

        alert("ورود با موفقیت انجام شد ✅");

        // هدایت بر اساس نقش
        if (user.role === "admin") {
            window.location.href = "dashboard.html";
        } else {
            window.location.href = "index.html";
        }
    });

});
