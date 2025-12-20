document.addEventListener("DOMContentLoaded", () => {
    fetch("movies.json")
        .then(res => res.json())
        .then(movies => renderMovies(movies))
        .catch(err => console.error("خطا در بارگذاری فیلم‌ها:", err));
});

function renderMovies(movies) {
    const grid = document.getElementById("moviesGrid");

    movies.forEach(movie => {
        const card = document.createElement("div");
        card.className = "movie-card";

        card.innerHTML = `
            <div class="movie-poster">
                <img src="${movie.poster}" alt="${movie.title}">
                ${movie.status ? `<span class="movie-badge ${movie.status}">${getBadgeText(movie.status)}</span>` : ""}
            </div>

            <div class="movie-info">
                <h3>${movie.title}</h3>
                <p class="movie-genre">${movie.genre} | ${movie.duration} دقیقه</p>

                <div class="movie-footer">
                    <span class="price">${movie.price.toLocaleString()} تومان</span>
                    <a href="booking.html?movie=${movie.id}" class="btn-book">رزرو بلیط</a>
                </div>
            </div>
        `;

        grid.appendChild(card);
    });
}

function getBadgeText(status) {
    if (status === "hot") return "محبوب";
    if (status === "now") return "اکران";
    return "";
}
