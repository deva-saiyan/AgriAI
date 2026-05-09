// ================= SCROLL ANIMATION =================

const animatedCards = document.querySelectorAll('.animate-card');

function revealCards() {

    animatedCards.forEach((card) => {

        const cardTop = card.getBoundingClientRect().top;
        const triggerPoint = window.innerHeight - 100;

        if (cardTop < triggerPoint) {

            card.classList.add('show');

        }

    });

}

window.addEventListener('scroll', revealCards);

// Initial Load
revealCards();


// ================= SMOOTH SCROLL =================

const heroButtons = document.querySelectorAll('.hero-btn');

heroButtons.forEach((button) => {

    button.addEventListener('click', function (e) {

        const target = this.getAttribute('href');

        if (target.startsWith('#')) {

            e.preventDefault();

            document.querySelector(target).scrollIntoView({
                behavior: 'smooth'
            });

        }

    });

});


// ================= HERO TITLE TYPING EFFECT =================

const heroTitle = document.querySelector('.hero-title');

const originalText = heroTitle.innerText;

heroTitle.innerText = '';

let charIndex = 0;

function typeEffect() {

    if (charIndex < originalText.length) {

        heroTitle.innerText += originalText.charAt(charIndex);

        charIndex++;

        setTimeout(typeEffect, 100);

    }

}

window.addEventListener('load', typeEffect);


// ================= FLOATING ACCURACY CIRCLES =================

const accuracyCircles = document.querySelectorAll('.accuracy-circle');

accuracyCircles.forEach((circle, index) => {

    setInterval(() => {

        circle.style.transform = 'translateY(-10px) scale(1.03)';

        setTimeout(() => {

            circle.style.transform = 'translateY(0px) scale(1)';

        }, 1000);

    }, 2000 + (index * 400));

});


// ================= DATASET COUNTER ANIMATION =================

const counters = document.querySelectorAll('.dataset-box h2');

counters.forEach((counter) => {

    const updateCounter = () => {

        const text = counter.innerText;

        const target = parseInt(text.replace(/\D/g, ''));

        if (!target) return;

        let count = 0;

        const increment = target / 100;

        const interval = setInterval(() => {

            count += increment;

            if (count >= target) {

                counter.innerText = text;

                clearInterval(interval);

            } else {

                if (text.includes('K')) {

                    counter.innerText = Math.floor(count) + 'K+';

                } else {

                    counter.innerText = Math.floor(count);

                }

            }

        }, 20);

    };

    updateCounter();

});


// ================= GLOW EFFECT =================

const glowCards = document.querySelectorAll(
    '.glass-card, .algo-card, .feature-box, .journal-box, .dataset-box'
);

glowCards.forEach((card) => {

    card.addEventListener('mouseenter', () => {

        card.style.boxShadow =
            '0 20px 45px rgba(34, 197, 94, 0.35)';

    });

    card.addEventListener('mouseleave', () => {

        card.style.boxShadow =
            '0 10px 25px rgba(0,0,0,0.15)';

    });

});


// ================= PARALLAX HERO EFFECT =================

window.addEventListener('scroll', () => {

    const hero = document.querySelector('.hero-section');

    const scrollValue = window.pageYOffset;

    hero.style.backgroundPositionY = scrollValue * 0.4 + 'px';

});


// ================= RANDOM ICON ROTATION =================

const featureIcons = document.querySelectorAll('.feature-box i');

featureIcons.forEach((icon, index) => {

    setInterval(() => {

        icon.style.transform = 'rotate(10deg) scale(1.1)';

        setTimeout(() => {

            icon.style.transform = 'rotate(0deg) scale(1)';

        }, 800);

    }, 2500 + (index * 300));

});


// ================= BUTTON HOVER EFFECT =================

const buttons = document.querySelectorAll('.hero-btn');

buttons.forEach((button) => {

    button.addEventListener('mouseenter', () => {

        button.style.letterSpacing = '1px';

    });

    button.addEventListener('mouseleave', () => {

        button.style.letterSpacing = '0px';

    });

});


// ================= PAGE LOADER EFFECT =================

window.addEventListener('load', () => {

    document.body.style.opacity = '0';

    setTimeout(() => {

        document.body.style.transition = '1s ease';

        document.body.style.opacity = '1';

    }, 200);

});