// Navbar burger menu
const burger = document.getElementById('navBurger');
const mobileNav = document.getElementById('navMobile');
if (burger && mobileNav) {
    burger.addEventListener('click', () => {
        mobileNav.classList.toggle('is-open');
    });
}

// Cookie banner
const cookieBanner = document.getElementById('cookieBanner');
const cookieAccept = document.getElementById('cookieAccept');
if (cookieBanner && !localStorage.getItem('cookieAccepted')) {
    cookieBanner.style.display = 'block';
}
if (cookieAccept) {
    cookieAccept.addEventListener('click', () => {
        localStorage.setItem('cookieAccepted', '1');
        cookieBanner.style.display = 'none';
    });
}

// Ticker — duplicate items for seamless loop
const ticker = document.querySelector('.ticker');
if (ticker) {
    ticker.innerHTML += ticker.innerHTML;
}
