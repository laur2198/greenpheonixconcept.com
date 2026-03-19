(() => {
    document.documentElement.classList.add('js');

    // --- MENIU BURGER ---
    const setupMenu = () => {
        const burger = document.querySelector('.navbar__burger');
        const mobileMenu = document.querySelector('.navbar__mobile');
        if (!burger || !mobileMenu) return;

        burger.addEventListener('click', () => {
            mobileMenu.classList.toggle('is-open');
            burger.setAttribute('aria-expanded', mobileMenu.classList.contains('is-open'));
        });
    };

    // --- SCROLL: NAVBAR SHADOW ---
    const setupNavbarScroll = () => {
        const nav = document.querySelector('.navbar');
        if (!nav) return;
        window.addEventListener('scroll', () => {
            nav.style.boxShadow = window.scrollY > 40
                ? '0 2px 20px rgba(0,0,0,0.08)'
                : 'none';
        }, { passive: true });
    };

    // --- CURSORUL PERSONALIZAT ---
    const setupCursor = () => {
        if (!window.matchMedia('(pointer: fine)').matches) return;

        const dot = document.createElement('div');
        const outline = document.createElement('div');
        dot.className = 'cursor-dot';
        outline.className = 'cursor-outline';
        document.body.appendChild(dot);
        document.body.appendChild(outline);

        window.addEventListener('mousemove', (e) => {
            dot.style.left = `${e.clientX}px`;
            dot.style.top  = `${e.clientY}px`;
            outline.animate(
                { left: `${e.clientX}px`, top: `${e.clientY}px` },
                { duration: 500, fill: 'forwards' }
            );
        });

        document.querySelectorAll('a, button, .poster-visual, .editorial-card').forEach((el) => {
            el.addEventListener('mouseenter', () => document.body.classList.add('hovering'));
            el.addEventListener('mouseleave', () => document.body.classList.remove('hovering'));
        });
    };

    // --- ANIMAȚII REVEAL (IntersectionObserver) ---
    const setupReveal = () => {
        const els = document.querySelectorAll('.reveal');
        if (!els.length) return;

        const observer = new IntersectionObserver(
            (entries) => entries.forEach((e) => { if (e.isIntersecting) e.target.classList.add('active'); }),
            { threshold: 0.1 }
        );
        els.forEach((el) => observer.observe(el));
    };

    // --- TICKER (dacă există) ---
    const setupTicker = () => {
        const ticker = document.querySelector('.ticker-track');
        if (!ticker) return;
        if (!ticker.dataset.doubled) {
            ticker.innerHTML += ticker.innerHTML;
            ticker.dataset.doubled = '1';
        }
    };

    // --- BRAND SLOT ANIMATION (text rotativ în social proof) ---
    const setupBrandSlot = () => {
        const slots = document.querySelectorAll('.brand-slot');
        if (!slots.length) return;

        slots.forEach((slot) => {
            const words = slot.dataset.words
                ? slot.dataset.words.split('|')
                : null;
            if (!words || words.length < 2) return;

            let idx = 0;
            const text = slot.querySelector('.brand-text') || slot;

            setInterval(() => {
                slot.classList.add('brand-slot--exit');
                setTimeout(() => {
                    idx = (idx + 1) % words.length;
                    text.textContent = words[idx];
                    slot.classList.remove('brand-slot--exit');
                    slot.classList.add('brand-slot--enter');
                    setTimeout(() => slot.classList.remove('brand-slot--enter'), 400);
                }, 300);
            }, 2500);
        });
    };

    // --- STICKY CARDS PARALLAX (scroll-based offset) ---
    const setupStickyCards = () => {
        const cards = document.querySelectorAll('.sticky-card');
        if (!cards.length) return;
        // CSS `top` este deja setat inline în HTML — OK
    };

    // --- MARKETING PIXELS (cu cookie consent) ---
    const TRACKING = {
        ga4: 'G-BP0J2SJTP1',
        meta: '1250834263629342',
    };

    const loadPixels = () => {
        if (window.__pixelsLoaded) return;
        window.__pixelsLoaded = true;

        // GA4
        const ga = document.createElement('script');
        ga.async = true;
        ga.src = `https://www.googletagmanager.com/gtag/js?id=${TRACKING.ga4}`;
        document.head.appendChild(ga);
        window.dataLayer = window.dataLayer || [];
        function gtag(){ window.dataLayer.push(arguments); }
        gtag('js', new Date());
        gtag('config', TRACKING.ga4);

        // Meta Pixel
        !function(f,b,e,v,n,t,s){
            if(f.fbq)return;n=f.fbq=function(){n.callMethod?
            n.callMethod.apply(n,arguments):n.queue.push(arguments)};
            if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
            n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;
            s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)
        }(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
        window.fbq('init', TRACKING.meta);
        window.fbq('track', 'PageView');
    };

    // --- COOKIE BANNER (cu pixel management) ---
    const setupCookieBanner = () => {
        const consent = localStorage.getItem('cookieConsent');
        if (consent === 'granted') { loadPixels(); return; }
        if (consent === 'denied') return;

        const banner = document.getElementById('cookieBanner');
        if (!banner) return;

        banner.style.display = 'block';
        banner.classList.add('cookie-banner--visible');

        const accept = document.getElementById('cookieAccept');
        const refuse = document.getElementById('cookieRefuse');

        const dismiss = (val) => {
            localStorage.setItem('cookieConsent', val);
            banner.classList.remove('cookie-banner--visible');
            setTimeout(() => banner.remove(), 400);
            if (val === 'granted') loadPixels();
        };
        if (accept) accept.addEventListener('click', () => dismiss('granted'));
        if (refuse) refuse.addEventListener('click', () => dismiss('denied'));
    };

    // --- I18N (RO/EN JS-based) ---
    const setupI18n = () => {
        const translations = window.GPC_TRANSLATIONS;
        if (!translations) return;

        const saved = localStorage.getItem('gpc_lang') || 'ro';
        applyLang(saved, translations);

        document.querySelectorAll('.lang-btn-dj').forEach((btn) => {
            btn.addEventListener('click', () => {
                const lang = btn.dataset.lang;
                localStorage.setItem('gpc_lang', lang);
                applyLang(lang, translations);
                document.querySelectorAll('.lang-btn-dj').forEach((b) => {
                    b.classList.toggle('active', b.dataset.lang === lang);
                });
            });
        });

        // Set initial active state
        document.querySelectorAll('.lang-btn-dj').forEach((b) => {
            b.classList.toggle('active', b.dataset.lang === saved);
        });
    };

    const applyLang = (lang, translations) => {
        const t = translations[lang] || translations['ro'];
        document.querySelectorAll('[data-i18n]').forEach((el) => {
            const key = el.dataset.i18n;
            if (t[key] !== undefined) el.textContent = t[key];
        });
        document.documentElement.lang = lang;
    };

    document.addEventListener('DOMContentLoaded', () => {
        setupMenu();
        setupNavbarScroll();
        setupCursor();
        setupReveal();
        setupTicker();
        setupBrandSlot();
        setupStickyCards();
        setupCookieBanner();
        setupI18n();
    });
})();
