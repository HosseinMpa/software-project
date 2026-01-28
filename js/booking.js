/* ===========================================
   BOOKING PAGE JAVASCRIPT
   =========================================== */

const movieSelect = document.getElementById("movieSelect");
const timeButtons = document.querySelectorAll(".time-btn");
const summaryMovie = document.getElementById("summaryMovie");
const summaryTime = document.getElementById("summaryTime");
const summarySeats = document.getElementById("summarySeats");
const summaryPrice = document.getElementById("summaryPrice");
const reserveBtn = document.getElementById("reserveBtn");
const seatsContainer = document.getElementById("seatsContainer");

let selectedMovie = "";
let selectedTime = "";
let selectedSeats = [];
let reservedSeats = [5, 12, 23, 41]; // صندلی‌های رزرو شده فرضی

const seatPrice = 90000;

/* ===========================================
   CREATE SEATS DYNAMICALLY
   =========================================== */
function createSeats() {
    seatsContainer.innerHTML = ""; // پاکسازی

    for (let i = 0; i < 100; i++) {
        const seat = document.createElement("div");
        seat.classList.add("seat");

        if (reservedSeats.includes(i)) {
            seat.classList.add("reserved");
        }

        seat.addEventListener("click", () => {
            if (seat.classList.contains("reserved")) return;

            seat.classList.toggle("selected");
            updateSelectedSeats();
        });

        seatsContainer.appendChild(seat);
    }
}

/* ===========================================
   MOVIE SELECT
   =========================================== */
movieSelect.addEventListener("change", () => {
    selectedMovie = movieSelect.value;
    summaryMovie.textContent = selectedMovie || "-";
});

/* ===========================================
   TIME SELECT
   =========================================== */
timeButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        timeButtons.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        selectedTime = btn.textContent.trim();
        summaryTime.textContent = selectedTime;
    });
});

/* ===========================================
   UPDATE SEAT SELECTION
   =========================================== */
function updateSelectedSeats() {
    const seats = document.querySelectorAll(".seat");
    selectedSeats = [];

    seats.forEach((seat, index) => {
        if (seat.classList.contains("selected")) {
            selectedSeats.push(index);
        }
    });

    summarySeats.textContent = selectedSeats.length
        ? selectedSeats.join(", ")
        : "-";

    summaryPrice.textContent =
        selectedSeats.length ? selectedSeats.length * seatPrice : 0;
}

/* ===========================================
   RESERVE BUTTON
   =========================================== */
   
let allBookings = JSON.parse(localStorage.getItem("allBookings")) || [];

reserveBtn.addEventListener("click", () => {
    if (!selectedMovie) return alert("لطفاً فیلم را انتخاب کنید.");
    if (!selectedTime) return alert("لطفاً سانس را انتخاب کنید.");
    if (selectedSeats.length === 0)
        return alert("حداقل یک صندلی انتخاب کنید.");

    const booking = {
        movie: selectedMovie,
        time: selectedTime,
        seats: selectedSeats,
        total: selectedSeats.length * seatPrice,
        date: new Date().toLocaleString("fa-IR")
    };

    allBookings.push(booking);

    localStorage.setItem("allBookings", JSON.stringify(allBookings));

    alert("رزرو با موفقیت ثبت شد!");
});


/* ===========================================
   INIT
   =========================================== */
createSeats();
updateSelectedSeats();
