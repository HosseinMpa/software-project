// contact.js

document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector(".contact-form");

    if (!form) return;

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const name = form.querySelector('input[type="text"]').value.trim();
        const email = form.querySelector('input[type="email"]').value.trim();
        const message = form.querySelector("textarea").value.trim();

        // اعتبارسنجی
        if (!name || !email || !message) {
            alert("لطفاً تمام فیلدها را پر کنید");
            return;
        }

        if (!validateEmail(email)) {
            alert("ایمیل وارد شده معتبر نیست");
            return;
        }

        // دریافت پیام‌های قبلی
        const messages = JSON.parse(localStorage.getItem("contactMessages")) || [];

        // پیام جدید
        const newMessage = {
            id: Date.now(),
            name,
            email,
            message,
            date: new Date().toLocaleString("fa-IR")
        };

        messages.push(newMessage);

        // ذخیره در LocalStorage
        localStorage.setItem("contactMessages", JSON.stringify(messages));

        // پیام موفقیت
        alert("پیام شما با موفقیت ارسال شد ✅");

        // ریست فرم
        form.reset();
    });

});

// اعتبارسنجی ایمیل
function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
