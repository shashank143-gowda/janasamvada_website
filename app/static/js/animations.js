// Animation utilities for JanSamvaad Light Theme

document.addEventListener('DOMContentLoaded', function() {
    // Navbar scroll effect
    const navbar = document.querySelector('.modern-navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // Initialize AOS (Animate on Scroll)
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease',
            once: true,
            offset: 100
        });
    }

    // Card animations on scroll
    const animateCards = () => {
        const cards = document.querySelectorAll('.card-animate');
        cards.forEach(card => {
            const cardTop = card.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            if (cardTop < windowHeight - 100) {
                card.classList.add('show');
            }
        });
    };

    // Reveal elements on scroll
    const revealElements = () => {
        const elements = document.querySelectorAll('.reveal');
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            if (elementTop < windowHeight - 100) {
                element.classList.add('active');
            }
        });
    };

    // Run animations on page load
    animateCards();
    revealElements();

    // Run animations on scroll
    window.addEventListener('scroll', function() {
        animateCards();
        revealElements();
    });

    // Add hover effects to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px)';
            this.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.1)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.boxShadow = '';
        });
    });

    // Add staggered animations to lists
    const animateLists = document.querySelectorAll('.staggered-list');
    animateLists.forEach(list => {
        const items = list.querySelectorAll('li, .list-item');
        items.forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(20px)';
            item.style.animation = `fadeInUp 0.5s ease forwards ${0.1 + (index * 0.1)}s`;
        });
    });

    // Add wave animation to hero section
    const heroSection = document.querySelector('.hero-section');
    if (heroSection && !heroSection.querySelector('.wave-bottom')) {
        const wave = document.createElement('div');
        wave.className = 'wave-bottom';
        wave.innerHTML = `
            <svg data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
                <path d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z" class="shape-fill"></path>
            </svg>
        `;
        heroSection.appendChild(wave);
    }
});

// Function to add pulse animation to elements
function addPulseEffect(selector) {
    const elements = document.querySelectorAll(selector);
    elements.forEach(element => {
        element.classList.add('btn-pulse');
    });
}

// Function to add floating animation to elements
function addFloatingEffect(selector) {
    const elements = document.querySelectorAll(selector);
    elements.forEach(element => {
        element.style.animation = 'float 3s ease-in-out infinite';
    });
}