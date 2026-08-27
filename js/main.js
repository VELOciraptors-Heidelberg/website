// Small progressive enhancement — the site works fully without this file.
// Closes the mobile "Contents" disclosure after a chapter link is clicked,
// so it doesn't stay open covering the page you just jumped to.
document.querySelectorAll(".chapter-nav-mobile").forEach(function (details) {
  details.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", function () {
      details.removeAttribute("open");
    });
  });
});
