// Smooth active link switch
document.querySelectorAll(".nav-anim").forEach(link => {
  link.addEventListener("click", function () {
    document.querySelectorAll(".nav-anim").forEach(el => el.classList.remove("active"));
    this.classList.add("active");
  });
});

// Navbar shrink effect on scroll
window.addEventListener("scroll", function () {
  const nav = document.querySelector(".custom-navbar");
  if (window.scrollY > 50) {
    nav.style.padding = "8px 0";
  } else {
    nav.style.padding = "12px 0";
  }
});