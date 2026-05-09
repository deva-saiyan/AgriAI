// ================= SCROLL REVEAL ANIMATION =================

const cards = document.querySelectorAll('.animate-card');

function revealCards() {

    cards.forEach((card) => {

        const cardTop = card.getBoundingClientRect().top;
        const triggerBottom = window.innerHeight - 100;

        if (cardTop < triggerBottom) {

            card.classList.add('show');

        }

    });

}

window.addEventListener('scroll', revealCards);

// Initial Animation
revealCards();


// ================= HERO TITLE TYPING EFFECT =================

const heroTitle = document.querySelector('.hero-title');

const titleText = heroTitle.innerText;

heroTitle.innerText = '';

let i = 0;

function typingEffect() {

    if (i < titleText.length) {

        heroTitle.innerText += titleText.charAt(i);

        i++;

        setTimeout(typingEffect, 100);

    }

}

window.addEventListener('load', typingEffect);


// ================= FLOATING PROFILE IMAGE EFFECT =================

const profileImages = document.querySelectorAll('.profile-img');

profileImages.forEach((image, index) => {

    setInterval(() => {

        image.style.transform = 'translateY(-10px) scale(1.05)';

        setTimeout(() => {

            image.style.transform = 'translateY(0px) scale(1)';

        }, 1000);

    }, 2500 + (index * 400));

});


// ================= SOCIAL ICON ANIMATION =================

const socialIcons = document.querySelectorAll('.social-icons a');

socialIcons.forEach((icon) => {

    icon.addEventListener('mouseenter', () => {

        icon.style.transform = 'translateY(-10px) rotate(8deg) scale(1.1)';

    });

    icon.addEventListener('mouseleave', () => {

        icon.style.transform = 'translateY(0px) rotate(0deg) scale(1)';

    });

});


// ================= CARD GLOW EFFECT =================

const teamCards = document.querySelectorAll('.team-card');

teamCards.forEach((card) => {

    card.addEventListener('mouseenter', () => {

        card.style.boxShadow =
            '0 20px 45px rgba(56, 189, 248, 0.35)';

    });

    card.addEventListener('mouseleave', () => {

        card.style.boxShadow =
            '0 10px 25px rgba(0,0,0,0.15)';

    });

});


// ================= HERO PARALLAX EFFECT =================

window.addEventListener('scroll', () => {

    const hero = document.querySelector('.contact-hero');

    const scrollValue = window.pageYOffset;

    hero.style.backgroundPositionY = scrollValue * 0.4 + 'px';

});


// ================= RANDOM ICON PULSE EFFECT =================

function pulseIcons() {

    socialIcons.forEach((icon, index) => {

        setTimeout(() => {

            icon.style.transform = 'scale(1.15)';

            setTimeout(() => {

                icon.style.transform = 'scale(1)';

            }, 400);

        }, index * 200);

    });

}

// Repeat every 5 seconds
setInterval(pulseIcons, 5000);


// ================= PAGE FADE LOAD EFFECT =================

window.addEventListener('load', () => {

    document.body.style.opacity = '0';

    setTimeout(() => {

        document.body.style.transition = '1s ease';

        document.body.style.opacity = '1';

    }, 200);

});


// ================= CARD TILT EFFECT =================

teamCards.forEach((card) => {

    card.addEventListener('mousemove', (e) => {

        const rect = card.getBoundingClientRect();

        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = ((y - centerY) / 20);
        const rotateY = ((centerX - x) / 20);

        card.style.transform =
            `rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;

    });

    card.addEventListener('mouseleave', () => {

        card.style.transform =
            'rotateX(0deg) rotateY(0deg) translateY(0px)';

    });

});