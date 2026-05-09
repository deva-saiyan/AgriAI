// ================= SCROLL ANIMATION =================

const animateCards = document.querySelectorAll('.animate-card');

window.addEventListener('scroll', revealCards);

function revealCards() {

    animateCards.forEach((card) => {

        const cardTop = card.getBoundingClientRect().top;
        const triggerPoint = window.innerHeight - 100;

        if (cardTop < triggerPoint) {
            card.classList.add('show');
        }

    });

}

// Initial Load
revealCards();


// ================= HERO BUTTON SMOOTH SCROLL =================

const heroButtons = document.querySelectorAll('.hero-btn');

heroButtons.forEach((button) => {

    button.addEventListener('click', function (e) {

        const targetId = this.getAttribute('href');

        if (targetId.startsWith('#')) {

            e.preventDefault();

            const targetSection = document.querySelector(targetId);

            targetSection.scrollIntoView({
                behavior: 'smooth'
            });

        }

    });

});


// ================= BAR CHART ANIMATION =================

const bars = document.querySelectorAll('.chart-bar');

function animateBars() {

    bars.forEach((bar) => {

        const finalHeight = bar.style.height;

        bar.style.height = "0px";

        setTimeout(() => {
            bar.style.height = finalHeight;
        }, 300);

    });

}

window.addEventListener('load', animateBars);


// ================= COUNTER ANIMATION =================

const datasetNumbers = document.querySelectorAll('.dataset-box h2');

datasetNumbers.forEach((counter) => {

    const updateCounter = () => {

        const targetText = counter.innerText;

        const target = parseInt(targetText.replace(/\D/g, ''));

        if (!target) return;

        let count = 0;

        const increment = target / 100;

        const interval = setInterval(() => {

            count += increment;

            if (count >= target) {

                counter.innerText = targetText;
                clearInterval(interval);

            } else {

                if (targetText.includes('K')) {
                    counter.innerText = Math.floor(count) + "K+";
                } else {
                    counter.innerText = Math.floor(count);
                }

            }

        }, 20);

    };

    updateCounter();

});


// ================= FLOATING EFFECT =================

const circles = document.querySelectorAll('.accuracy-circle');

circles.forEach((circle, index) => {

    setInterval(() => {

        circle.style.transform = 'translateY(-10px)';

        setTimeout(() => {
            circle.style.transform = 'translateY(0px)';
        }, 1000);

    }, 2000 + (index * 500));

});


// ================= GLOW EFFECT =================

const cards = document.querySelectorAll(
    '.glass-card, .algo-card, .feature-box, .journal-box'
);

cards.forEach((card) => {

    card.addEventListener('mouseenter', () => {

        card.style.boxShadow =
            '0 20px 45px rgba(56, 189, 248, 0.35)';

    });

    card.addEventListener('mouseleave', () => {

        card.style.boxShadow =
            '0 10px 25px rgba(0,0,0,0.15)';

    });

});


// ================= TYPING EFFECT =================

const heroTitle = document.querySelector('.hero-title');

const originalText = heroTitle.innerText;

heroTitle.innerText = "";

let index = 0;

function typingEffect() {

    if (index < originalText.length) {

        heroTitle.innerText += originalText.charAt(index);

        index++;

        setTimeout(typingEffect, 120);

    }

}

window.addEventListener('load', typingEffect);


// ================= PARALLAX EFFECT =================

window.addEventListener('scroll', () => {

    const hero = document.querySelector('.hero-section');

    let scrollPosition = window.pageYOffset;

    hero.style.backgroundPositionY = scrollPosition * 0.5 + "px";

});