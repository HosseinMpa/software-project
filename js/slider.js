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


document.addEventListener("DOMContentLoaded", () => {
    const trendingSliderTrack = document.getElementById("trendingSliderTrack");
    const prevBtn = document.getElementById("prevBtnTrending");
    const nextBtn = document.getElementById("nextBtnTrending");

    // تابع بارگذاری فیلم‌های ترند
    async function loadTrendingMovies() {
        const movies = await fetchMovies(); // همین تابع رو برای fetch کردن movies.json صدا بزن

        const trendingMovies = movies.filter(movie => movie.status === "trending");

        trendingSliderTrack.innerHTML = ""; // خالی کردن اسلایدر

        trendingMovies.forEach(movie => {
            const slide = document.createElement("div");
            slide.classList.add("trending-slide");

            slide.innerHTML = `
                <img src="${movie.poster}" alt="${movie.title}" />
                <div class="slide-title">${movie.title}</div>
            `;
            trendingSliderTrack.appendChild(slide);
        });

        // برای داینامیک شدن تعداد فیلم‌ها
        updateSlider();
    }

    // حرکت اسلایدها
    let currentIndex = 0;

    function updateSlider() {
        const slides = document.querySelectorAll(".trending-slide");
        const sliderTrack = document.getElementById("trendingSliderTrack");
        sliderTrack.style.transform = `translateX(-${currentIndex * 240}px)`; // اندازه 240px بستگی به اندازه هر اسلاید دارد
    }

    prevBtn.addEventListener("click", () => {
        currentIndex = (currentIndex - 1 + document.querySelectorAll(".trending-slide").length) % document.querySelectorAll(".trending-slide").length;
        updateSlider();
    });

    nextBtn.addEventListener("click", () => {
        currentIndex = (currentIndex + 1) % document.querySelectorAll(".trending-slide").length;
        updateSlider();
    });

    // بارگذاری فیلم‌های ترند وقتی صفحه لود میشه
    loadTrendingMovies();
});

// تابع برای خواندن اطلاعات فیلم‌ها از movies.json
async function fetchMovies() {
    const response = await fetch("movies.json");
    return await response.json();
}



// اجرا
createDots();
updateSlider();
startAutoSlide();
