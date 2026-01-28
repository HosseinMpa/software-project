// movies.js — بارگذاری لیست فیلم‌ها از movies.json و رندر در movies.html
async function loadMovies() {
  try {
    const res = await fetch('movies.json');
    const movies = await res.json();

    const grid = document.querySelector('.movies-grid');
    movies.forEach(m => {
      const card = document.createElement('div');
      card.className = 'movie-card';
      card.innerHTML = `
        <img src="${m.poster}" alt="${m.title}">
        <div class="movie-info">
          <h3>${m.title}</h3>
          <p>ژانر: ${m.genre} | ${m.year}</p>
          <p style="font-size:13px;color:#666;margin-top:6px">${m.summary}</p>
        </div>
        <a href="booking.html?movie=${encodeURIComponent(m.id)}" class="btn">رزرو</a>
      `;
      grid.appendChild(card);
    });
  } catch (err) {
    console.error('failed load movies', err);
    document.querySelector('.movies-grid').innerHTML = '<p>خطا در بارگذاری فیلم‌ها.</p>';
  }
}

document.addEventListener('DOMContentLoaded', loadMovies);
