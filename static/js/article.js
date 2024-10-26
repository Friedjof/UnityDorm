document.addEventListener('DOMContentLoaded', function () {
    const imageView = document.getElementById('article-image-viewer');
    const header = document.getElementById('article-header');

    header.addEventListener('click', function () {
        imageView.style.display = 'flex';
    });

    imageView.addEventListener('click', function () {
        imageView.style.display = 'none';
    });
});