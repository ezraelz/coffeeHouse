document.addEventListener('DOMContentLoaded', function () {
    const menuToggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('nav ul');
    const barsIcon = document.querySelector('.fa-bars');
    const timesIcon = document.querySelector('.fa-times');
    
    menuToggle.addEventListener('click', function () {
        nav.classList.toggle('active');
        const isActive = nav.classList.contains('active');
        barsIcon.style.display = isActive ? 'none' : 'block';
        timesIcon.style.display = isActive ? 'block' : 'none';
    });
});