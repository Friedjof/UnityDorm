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
            updateCarousel();
        }
    }

    function showPrevious() {
        if (currentIndex > 0) {
            currentIndex--;
            updateCarousel();
        }
    }

    window.addEventListener('resize', updateCarousel);

    // Initialisiere das Karussell nach dem Laden der Seite
    updateCarousel();

    // Event Listener für die Karussell-Pfeile
    const nextButton = document.querySelector('.carousel-arrow.right');
    const prevButton = document.querySelector('.carousel-arrow.left');

    if (nextButton) {
        nextButton.addEventListener('click', showNext);
    }

    if (prevButton) {
        prevButton.addEventListener('click', showPrevious);
    }
});
