document.addEventListener("DOMContentLoaded", initialize);

function initialize() {
    assignActive();
    hideOnScroll();
}

function assignActive() {
    let nav_elements = document.querySelectorAll('nav.navbar a.nav-link[href]:not([role])');
    let dropdown_elements = document.querySelectorAll('nav.navbar a.dropdown-item[href]');
    
    for (let i=0; i<nav_elements.length; i++) {
        if (window.location.pathname.includes(nav_elements[i].getAttribute("href"))) {
            nav_elements[i].classList.add('active');
            return;
        }
    }

    for (let i=0; i<dropdown_elements.length; i++) {
        if (window.location.pathname.includes(dropdown_elements[i].getAttribute("href"))) {
            dropdown_elements[i].classList.add('active');
            return;
        }
    }
}

function hideOnScroll() {
    el_autohide = document.querySelector('.autohide');

    if(el_autohide) {
        var last_scroll_top = 0;
        el_autohide.classList.add('sticky-top');
        window.addEventListener('scroll', function() {
            let scroll_top = window.scrollY;
            if(scroll_top < last_scroll_top) {
                el_autohide.classList.remove('visually-hidden');
            } else {
                el_autohide.classList.add('visually-hidden');
            }
            last_scroll_top = scroll_top;
        });
    }
}