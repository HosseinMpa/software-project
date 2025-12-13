// register.js

document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("registerForm");

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const fullname = document.getElementById("fullname").value.trim();
        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        // اعتبارسنجی اولیه
        if (!fullname || !username || !password || !confirmPassword) {
            alert("لطفاً تمام فیلدها را پر کنید");
            return;
        }

        if (password.length < 4) {
            alert("رمز عبور باید حداقل 4 کاراکتر باشد");
            return;
        }

        if (password !== confirmPassword) {
            alert("رمز عبور و تکرار آن یکسان نیستند");
            return;
        }

        // دریافت کاربران قبلی
        const users = JSON.parse(localStorage.getItem("users")) || [];

        // بررسی تکراری نبودن نام کاربری
        const userExists = users.find(u => u.username === username);
        if (userExists) {
            alert("این نام کاربری قبلاً ثبت شده است");
            return;
        }

        // ساخت کاربر جدید
        const newUser = {
            id: Date.now(),
            fullname,
            username,
            password,
            role: "user",   // user | admin
            createdAt: new Date().toLocaleDateString("fa-IR")
        };

        users.push(newUser);

        // ذخیره در LocalStorage
        localStorage.setItem("users", JSON.stringify(users));

        alert("ثبت‌نام با موفقیت انجام شد ✅");

        // انتقال به صفحه ورود
        window.location.href = "login.html";
    });

});
