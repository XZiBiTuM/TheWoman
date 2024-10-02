window.addEventListener("load", function () {
        const images = document.querySelectorAll('[src*="/media/"]');

        // Заменяем второе вхождение "media" на "/"
        images.forEach((img) => {
            img.src = img.src.replace('/media/', '/');
        });
});


// script.js


