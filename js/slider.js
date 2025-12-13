let currentIndex = 0;
const slides = document.querySelectorAll(".slide");
const sliderTrack = document.getElementById("sliderTrack");
const dotsContainer = document.getElementById("dots");

let autoSlideInterval;


function updateSlider() {
    sliderTrack.style.transform = `translateX(-${currentIndex * 100}%)`;

    document.querySelectorAll(".dot").forEach((dot, i) => {
        dot.classList.toggle("active", i === currentIndex);
    });
}

function createDots() {
    slides.forEach((_, i) => {
        const dot = document.createElement("span");
        dot.classList.add("dot");
        if (i === 0) dot.classList.add("active");

        dot.addEventListener("click", () => {
            currentIndex = i;
            updateSlider();
            resetAutoSlide();
        });

        dotsContainer.appendChild(dot);
    });
}

// دکمه‌ها
document.getElementById("prevBtn").addEventListener("click", () => {
    currentIndex = (currentIndex - 1 + slides.length) % slides.length;
    updateSlider();
    resetAutoSlide();
});

document.getElementById("nextBtn").addEventListener("click", () => {
    nextSlide();
    resetAutoSlide();
});

function nextSlide() {
    currentIndex = (currentIndex + 1) % slides.length;
    updateSlider();
}

// اسلاید خودکار
function startAutoSlide() {
    autoSlideInterval = setInterval(nextSlide, 4000); // هر 4 ثانیه
}

function resetAutoSlide() {
    clearInterval(autoSlideInterval);
    startAutoSlide();
}

// توقف هنگام hover
sliderTrack.addEventListener("mouseenter", () => {
    clearInterval(autoSlideInterval);
});

sliderTrack.addEventListener("mouseleave", () => {
    startAutoSlide();
});

function goToBooking() {
    window.location.href = "booking.html";
}

// اجرا
createDots();
updateSlider();
startAutoSlide();
