document.addEventListener("DOMContentLoaded", function() {
    const bubble = document.querySelector('.bubble');
    if (bubble) {
        setTimeout(function() {
            bubble.classList.remove('show');
        }, 5000); // 5 seconds timeout
    }
});
