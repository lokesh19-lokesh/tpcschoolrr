
document.addEventListener('DOMContentLoaded', function () {
    const sliders = document.querySelectorAll('.simple-slider-container');

    sliders.forEach(slider => {
        const slides = slider.querySelectorAll('.simple-slide');
        let currentSlide = 0;
        const slideInterval = 3000; // 3 seconds

        if (slides.length > 0) {
            // Ensure first slide is active
            slides[0].classList.add('active');

            setInterval(() => {
                slides[currentSlide].classList.remove('active');
                currentSlide = (currentSlide + 1) % slides.length;
                slides[currentSlide].classList.add('active');
            }, slideInterval);
        }
    });
});
