// Extra feature: όταν αλλάζεις dropdown (genre/director/sort) κάνει submit αυτόματα
document.addEventListener("DOMContentLoaded", () => {
  const genre = document.getElementById("genreSelect");
  const director = document.getElementById("directorSelect");
  const sort = document.getElementById("sortSelect");

  [genre, director, sort].forEach(el => {
    if (!el) return;
    el.addEventListener("change", () => {
      el.closest("form").submit();
    });
  });
});
