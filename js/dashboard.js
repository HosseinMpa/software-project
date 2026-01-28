/* ============================================
   LOAD BOOKINGS.JSON
============================================ */

async function fetchBookings() {
    try {
        const response = await fetch("./bookings.json");

        if (!response.ok) {
            throw new Error("bookings.json not found");
        }

        const bookings = await response.json();
        const movies = await fetchMovies();

        loadReservationsTable(bookings, movies);
        updateDashboardStats(bookings, movies);
        updateCharts(bookings, movies);

    } catch (error) {
        console.error("Error loading bookings:", error);
    }
}

/* ============================================
   LOAD MOVIES.JSON
============================================ */

async function fetchMovies() {
    try {
        const response = await fetch("./movies.json");

        if (!response.ok) {
            throw new Error("movies.json not found");
        }

        return await response.json();
    } catch (error) {
        console.error("Error loading movies:", error);
        return [];
    }
}

/* ============================================
   Fill Table with Reservations
============================================ */

function loadReservationsTable(bookings, movies) {
    const table = document.getElementById("reservationsTable");
    table.innerHTML = "";

    bookings.forEach(booking => {
        const movie = movies.find(m => m.id === booking.movieId);

        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${movie ? movie.title : "نامشخص"}</td>
            <td>${booking.time}</td>
            <td>${booking.seats.join(", ")}</td>
            <td>${booking.total.toLocaleString()} تومان</td>
            <td>${booking.date}</td>
        `;
        table.appendChild(tr);
    });
}

/* ============================================
   Dashboard Statistics
============================================ */

function updateDashboardStats(bookings, movies) {
    // مجموع رزروها
    document.getElementById("totalOrders").textContent = bookings.length;

    // مجموع درآمد
    const totalIncome = bookings.reduce((sum, b) => sum + b.total, 0);
    document.getElementById("totalIncome").textContent =
        totalIncome.toLocaleString();

    // فروش هر فیلم (برای گراف)
    const movieSales = {};
    movies.forEach(m => (movieSales[m.id] = 0));

    bookings.forEach(b => {
        movieSales[b.movieId] += b.seats.length;
    });

    // ذخیره در window
    window.chartMovieSales = {
        labels: movies.map(m => m.title),
        values: movies.map(m => movieSales[m.id])
    };
}

/* ============================================
   Charts (Chart.js)
============================================ */

function updateCharts(bookings, movies) {

    if (!window.chartMovieSales) {
        console.warn("chartMovieSales not ready");
        return;
    }

    /* === Chart 1: تعداد فروش هر فیلم === */
    const ctx1 = document.getElementById("salesChart").getContext("2d");

    new Chart(ctx1, {
        type: "bar",
        data: {
            labels: window.chartMovieSales.labels,
            datasets: [{
                label: "تعداد فروش",
                data: window.chartMovieSales.values,
                backgroundColor: "rgba(255, 82, 82, 0.7)"
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

    /* === Chart 2: درآمد روزانه === */
    const incomePerDay = {};

    bookings.forEach(b => {
        if (!incomePerDay[b.date]) incomePerDay[b.date] = 0;
        incomePerDay[b.date] += b.total;
    });

    const ctx2 = document.getElementById("incomeChart").getContext("2d");

    new Chart(ctx2, {
        type: "line",
        data: {
            labels: Object.keys(incomePerDay),
            datasets: [{
                label: "درآمد روزانه",
                data: Object.values(incomePerDay),
                borderColor: "rgba(33, 150, 243, 1)",
                borderWidth: 2,
                fill: false,
                tension: 0.4
            }]
        },
        options: { responsive: true }
    });
}

/* ============================================
   INIT
============================================ */

fetchBookings();
