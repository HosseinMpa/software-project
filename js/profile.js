// profile.js

document.addEventListener("DOMContentLoaded", () => {

    const user = JSON.parse(localStorage.getItem("loggedInUser"));

    if (!user) {
        window.location.href = "login.html";
        return;
    }

    // نمایش اطلاعات در صفحه
    document.getElementById("profileFullName").textContent = user.fullName || "نام ثبت نشده";
    document.getElementById("profileUsername").textContent = "نام کاربری: " + user.username;

    document.getElementById("fullNameInput").value = user.fullName || "";
    document.getElementById("emailInput").value = user.email || "";
    document.getElementById("passwordInput").value = "";

    // ذخیره تغییرات
    document.getElementById("saveProfile").addEventListener("click", () => {

        const fullName = document.getElementById("fullNameInput").value.trim();
        const email = document.getElementById("emailInput").value.trim();
        const password = document.getElementById("passwordInput").value.trim();

        // بروزرسانی اطلاعات
        user.fullName = fullName;
        user.email = email;

        if (password.length > 0) {
            user.password = password;
        }

        localStorage.setItem("loggedInUser", JSON.stringify(user));

        alert("پروفایل با موفقیت ذخیره شد!");

        // بروزرسانی نمایش
        document.getElementById("profileFullName").textContent = user.fullName;
    });

});
