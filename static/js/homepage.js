document.addEventListener('DOMContentLoaded', function() {
    // Dein bestehender Code
    const shortcuts = document.querySelectorAll('.unity-shortcut');
    shortcuts.forEach(shortcut => {
        shortcut.addEventListener('click', function() {
            const url = shortcut.getAttribute('data-shortcut-url');
            const newTab = shortcut.getAttribute('data-shortcut-new-tab') === 'True';

            if (url) {
                if (newTab) {
                    window.open(url, '_blank');
                } else {
                    window.location.href = url;
                }
            }
        });
    });

    const newsItems = document.querySelectorAll('.news-item-container');
    newsItems.forEach(item => {
        item.addEventListener('click', function() {
            const identifier = item.getAttribute('data-news-identifier');
            if (identifier) {
                window.location.href = `/article/${identifier}`;
            }
        });
    });

    // Karussell-Code
    let currentIndex = 0;
    let direction = 1; // 1 for right, -1 for left
    let autoSlideInterval;
    let autoSlideTimeout;

    function getItemsPerSlide() {
        return window.innerWidth >= 768 ? 4 : 1;
    }

    function updateCarousel() {
        const itemsPerRow = getItemsPerSlide();
        const totalItems = document.querySelectorAll('.news-item-container').length;
        const maxIndex = totalItems - itemsPerRow;

        if (totalItems <= itemsPerRow) {
            const wrapper = document.querySelector('.news-items-wrapper');
            if (wrapper) {
                wrapper.style.justifyContent = 'center';
            }
            const arrows = document.querySelectorAll('.carousel-arrow');
            arrows.forEach(arrow => {
                arrow.style.display = 'none';
            });
            return;
        }

        // Sicherstellen, dass currentIndex innerhalb der Grenzen bleibt
        if (currentIndex < 0) {
            currentIndex = 0;
        } else if (currentIndex > maxIndex) {
            currentIndex = maxIndex;
        }

        const itemWidthPercentage = 100 / itemsPerRow;
        const translateX = -currentIndex * itemWidthPercentage;

        const wrapper = document.querySelector('.news-items-wrapper');
        if (wrapper) {
            wrapper.style.transform = 'translateX(' + translateX + '%)';
        }
    }

    function showNext() {
        const itemsPerRow = getItemsPerSlide();
        const totalItems = document.querySelectorAll('.news-item-container').length;
        const maxIndex = totalItems - itemsPerRow;

        if (currentIndex < maxIndex) {
            currentIndex++;
        } else {
            direction = -1; // Change direction to left
            currentIndex--;
        }
        updateCarousel();
    }

    function showPrevious() {
        if (currentIndex > 0) {
            currentIndex--;
        } else {
            direction = 1; // Change direction to right
            currentIndex++;
        }
        updateCarousel();
    }

    function autoSlide() {
        if (direction === 1) {
            showNext();
        } else {
            showPrevious();
        }
    }

    function startAutoSlide() {
        const itemsPerRow = getItemsPerSlide();
        const totalItems = document.querySelectorAll('.news-item-container').length;
        if ((window.innerWidth >= 768 && totalItems > 4) || (window.innerWidth < 768 && totalItems > 1)) {
            autoSlideInterval = setInterval(autoSlide, 6000); // Slide every 6 seconds
        }
    }

    function stopAutoSlide() {
        clearInterval(autoSlideInterval);
        clearTimeout(autoSlideTimeout);
        autoSlideTimeout = setTimeout(startAutoSlide, 20000); // Restart auto-slide after 20 seconds of inactivity
    }

    window.addEventListener('resize', updateCarousel);

    // Initialisiere das Karussell nach dem Laden der Seite
    updateCarousel();
    startAutoSlide();

    // Event Listener für die Karussell-Pfeile
    const nextButton = document.querySelector('.carousel-arrow.right');
    const prevButton = document.querySelector('.carousel-arrow.left');

    if (nextButton) {
        nextButton.addEventListener('click', function() {
            showNext();
            stopAutoSlide();
        });
    }

    if (prevButton) {
        prevButton.addEventListener('click', function() {
            showPrevious();
            stopAutoSlide();
        });
    }
});