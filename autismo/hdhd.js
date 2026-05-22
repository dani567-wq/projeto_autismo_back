  let index = 0;
    const images = document.querySelectorAll(".carousel img");

    function showSlide() {
        images.forEach(img => img.classList.remove("active"));
        index = (index + 1) % images.length;
        images[index].classList.add("active");
    }

    setInterval(showSlide, 3000);

    