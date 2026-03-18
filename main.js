(() => {
    document.documentElement.classList.add('js');

    // CONFIGURARE ID-URI (Înlocuiește cu ID-urile tale reale)
    const TRACKING_CONFIG = {
        ga4_id: 'G-BP0J2SJTP1',
        meta_pixel_id: '1250834263629342',
        tiktok_pixel_id: 'D64F6T3C77U69UNGKT30'
    };

    const translations = {
        ro: {
            about_cta: "Hai să discutăm ->",
            ads_budget_cta: "SOLICITĂ O STRATEGIE",
            ads_budget_desc: "Pentru rezultate optime și date statistice relevante, recomandăm un buget media de minim <strong>1000€ / lună</strong>.",
            ads_budget_title: "BUGET RECOMANDAT",
            ads_deliverable_1: "Audit conturi Ads",
            ads_deliverable_2: "Setup Tracking (GA4 + GTM)",
            ads_deliverable_3: "Design Creatives & Copy",
            ads_deliverable_4: "Raportare lunară (Looker)",
            ads_deliverables_title: "LIVRABILE:",
            ads_faq_a1: "Tu. Întotdeauna lucrăm pe contul clientului. Ai proprietate 100% asupra datelor.",
            ads_faq_a2: "Nu. Bugetul de reclame se plătește direct către Facebook/Google. Fee-ul nostru este separat pentru management.",
            ads_faq_q1: "Cine deține contul de reclame?",
            ads_faq_q2: "Includeți și bugetul de media în preț?",
            ads_faq_title: "ÎNTREBĂRI FRECVENTE",
            ads_google_desc: "Captăm clienții care caută deja activ serviciile tale. Cea mai mare rată de conversie, dar necesită o structură impecabilă a cuvintelor cheie negative pentru a nu risipi bugetul.",
            ads_google_title: "02. GOOGLE ADS (INTENT)",
            ads_intro: "Nu aducem doar \"click-uri\". Aducem clienți plătitori. Campanii setate pe obiective de conversie (Lead, Sale), urmărite prin tracking server-side.",
            ads_meta_desc: "Ideal pentru a genera cerere (Demand Generation). Nu așteptăm clienții să caute, mergem noi peste ei cu oferta ta.",
            ads_meta_point_1: "Segmentare audiențe (Lookalike, Retargeting)",
            ads_meta_point_2: "Testare A/B constantă pe creative-uri",
            ads_meta_point_3: "Copywriting persuasiv (unghiuri de marketing generate cu AI)",
            ads_meta_title: "01. META ADS (FB & INSTAGRAM)",
            ads_process_title: "CUM LUCRĂM <span class='text-brand'>ÎMPREUNĂ?</span>",
            ads_stack_title: "STACK TEHNOLOGIC:",
            ads_step_1_desc: "Săptămâna 1. Primim acces la conturi, analizăm istoricul și setăm obiectivele KPI.",
            ads_step_1_title: "AUDIT & ONBOARDING",
            ads_step_2_desc: "Săptămâna 2. Creăm structura campaniilor, scriem textele și pregătim tracking-ul.",
            ads_step_2_title: "STRATEGIE & SETUP",
            ads_step_3_desc: "Momentul adevărului. Campaniile sunt active și începem să colectăm date reale.",
            ads_step_3_title: "LANSARE (GO LIVE)",
            ads_step_4_desc: "Lunar. Oprim ce pierde bani, scalăm ce aduce profit. Raportare la fiecare 30 de zile.",
            ads_step_4_title: "OPTIMIZARE & SCALE",
            ads_title: "PERFORMANCE <span class='text-outline'>MARKETING</span>",
            ads_tracking_desc: "Fără date, doar ghicim. Implementăm Google Tag Manager și CAPI (Conversion API) pentru a ști exact cât te costă un client, nu doar un click.",
            ads_tracking_title: "03. TRACKING & RAPORTARE",
            case_challenge_title: "PROVOCAREA",
            case_services_title: "SERVICII LIVRATE",
            case_studies_desc: "Rezultate reale, nu teorie. Vezi cum transformăm bugetele în creștere măsurabilă: lead-uri, vânzări și conversii.",
            case_studies_title: "STUDII DE CAZ",
            case_timeline_title: "TIMELINE",
            case_timeline_value: "Pilot + optimizare: 2–4 săptămâni",
            contact_desc: "Scrie-ne pe email sau WhatsApp pentru o evaluare inițială. Dacă ne potrivim, revenim în 24h cu un plan clar.",
            contact_email_label: "EMAIL",
            contact_phone_label: "PHONE / WHATSAPP",
            contact_step_2: "Te contactăm (Email/Telefon) pentru a stabili o scurtă discuție de cunoaștere (Discovery Call).",
            contact_step_3: "Dacă ne potrivim, primești o ofertă și un plan de acțiune personalizat.",
            contact_title: "LET'S TALK <span class=\"text-highlight\">NUMBERS.</span>",
            cta_btn: "Programează o discuție",
            cta_subtitle: "Spune-mi unde vrei să ajungi și îți trimit un plan clar în 24h.",
            cta_title: "Hai să-ți construim creșterea.",
            faq_1_a: "Depinde de industrie și obiectiv. Ca regulă, ai nevoie de suficient buget încât algoritmii să iasă din \"learning\" și să putem optimiza. Dacă bugetul e foarte mic, lucrăm mai întâi la ofertă, landing și tracking, apoi scalăm.",
            faq_1_q: "CARE ESTE BUGETUL MINIM RECOMANDAT?",
            faq_2_a: "Primele semnale apar în 48–72h de la lansare, dar optimizarea reală se vede de obicei în 2–4 săptămâni, după ce strângem date relevante și eliminăm risipa.",
            faq_2_q: "ÎN CÂT TIMP APAR REZULTATELE?",
            faq_3_a: "Lucrăm pe abonament lunar, fără blocaje pe 12 luni. Rămâi pentru că vezi progres, nu pentru că \"trebuie\".",
            faq_3_q: "EXISTĂ PERIOADĂ CONTRACTUALĂ?",
            faq_4_a: "Ne ocupăm noi: direcție creativă, layout-uri, UGC guidance sau producție (dacă e nevoie). Putem porni și din materiale existente + îmbunătățiri rapide, apoi construim biblioteca de creative.",
            faq_4_q: "CE SE ÎNTÂMPLĂ DACĂ NU AM POZE/VIDEO?",
            faq_title: "ÎNTREBĂRI FRECVENTE",
            footer_book: "Programează o discuție - click aici",
            footer_casestudies: "Studii de caz",
            footer_expertise: "Expertiză",
            footer_privacy: "Confidențialitate",
            footer_rights: "&copy;2026 GREEN PHEONIX CONCEPT SRL. TOATE DREPTURILE REZERVATE.",
            footer_studio: "Studio",
            hero_btn_1: "ÎNCEPE PROIECTUL",
            hero_btn_2: "VEZI STUDII DE CAZ ->",
            hero_desc: "Nu vânăm trenduri. Construim sisteme digitale care convertesc: ads + landing + tracking + optimizare. Un mix controlat de date, creativitate și execuție rapidă — ca să ai creștere predictibilă, nu \"noroc\".",
            hero_h1_1: "PRECIZIE",
            hero_h1_2: "PERFORMANȚĂ",
            hero_h1_3: "MARKETING.",
            hero_location: "LOC: BRAȘOV",
            hero_poster_a_cta: "CLICK TO START",
            hero_poster_b_cta: "CLICK FOR DETAILS",
            hero_poster_c_cta: "CLICK TO SCALE",
            hero_stat_1: "ROAS CURENT",
            hero_stat_2: "CAMPANII ACTIVE",
            hero_system_online: "SISTEM ONLINE",
            hero_ticker: "/// STRATEGIE /// AUDIT /// IMPLEMENTARE /// SCALARE /// TRACKING /// CRO /// CREATIVE /// AUTOMATIZARE ///",
            hero_ver: "AGENȚIE_VER_2.5",
            nav_about: "Despre",
            nav_contact: "Contact",
            nav_home: "Acasă",
            nav_portfolio: "Portofoliu",
            nav_services: "Servicii",
            notfound_cta: "RESTART SYSTEM ->",
            notfound_desc: "Pagina pe care o cauți a fost ștearsă, mutată sau nu a existat niciodată. Coordonate invalide.",
            notfound_title: "SYSTEM_FAILURE",
            portfolio_read: "CITEȘTE",
            portfolio_sidebar_desc: "Rezultate reale, nu teorie. Vezi cum am transformat investițiile în profit pentru partenerii noștri.",
            portfolio_sidebar_title: "CASE <br><span class='text-outline'>STUDIES</span>",
            portfolio_stat_1_label: "AD SPEND GESTIONAT",
            portfolio_stat_2_label: "PROIECTE LIVRATE",
            portfolio_stat_3_label: "INDUSTRII ACOPERITE",
            portfolio_title: "SELECTED <span class='text-outline'>WORKS</span>",
            res_challenge_title: "PROVOCAREA",
            res_client: "CLIENT: BPD TRANSPORT - TRANSPORT ROMÂNIA - ITALIA",
            res_deliverables_title: "LIVRABILE",
            res_impact_title: "IMPACT: MAI MULTE CERERI, MAI PUȚIN TIMP PIERDUT",
            res_next_label: "URMĂTORUL PROIECT",
            res_stack_title: "TECH STACK",
            res_stat_1_label: "Confirmare rapidă – prin WhatsApp / telefon",
            res_stat_2_label: "Rute clare – opriri & program stabil",
            res_stat_3_label: "Suport real – înainte și în timpul cursei",
            res_title: "BPD TRANSPORT: DRUMURI BINE ORGANIZATE, FĂRĂ STRES.",
            service_1_big: "STRATEGIE",
            service_1_desc: "Nu începem cu \"ce credem\". Începem cu ce spun datele. Analizăm funnel-ul, tracking-ul și oferta, apoi construim un plan clar: ce testăm, de ce și în ce ordine.",
            service_1_link: "CERE UN AUDIT ->",
            service_1_title: "AUDIT & STRATEGIE",
            service_2_big: "DESIGN",
            service_2_desc: "Viteză + conversie. Landing pages și site-uri gândite ca instrumente de vânzare: structură clară, copy convingător, UX fără zgomot și optimizare pentru mobil.",
            service_2_link: "VEZI PROCESUL WEB ->",
            service_2_title: "WEBSITE-URI CARE VÂND",
            service_3_big: "CREȘTERE",
            service_3_desc: "Motorul de scalare. Campanii Meta, Google și TikTok, cu tracking corect și testare constantă pe unghiuri + creative. Optimizăm zilnic pentru profit, nu pentru vanity metrics.",
            service_3_link: "VEZI STRATEGIA ADS ->",
            service_3_title: "PERFORMANCE ADS",
            services_title: "/// CAPABILITĂȚI DE BAZĂ",
            social_proof_sentence: "NOI CONSTRUIM SISTEME PENTRU <span class=\"brand-slot\"><span class=\"brand-text\">BRANDURI</span></span>",
            social_proof_top: "Din România, pentru branduri care vor creștere reală.",
            web_cta: "DISCUTĂ DESPRE SITE-UL TĂU",
            web_faq_a1: "Tu. Folosim conturile tale de hosting și CMS, iar accesul rămâne la tine după livrare.",
            web_faq_a2: "Da. Scriem textele în funcție de publicul țintă și obiectivele de conversie, apoi le validăm cu tine.",
            web_faq_q2: "Realizați și copywritingul?",
            web_faq_title: "ÎNTREBĂRI FRECVENTE",
            web_intro: "Un site nu este un tablou. Este un instrument de vânzare. Construim pagini rapide, optimizate pentru mobil și gândite să convertească vizitatorii în lead-uri.",
            web_landing_desc: "O singură pagină, un singur obiectiv: să transforme vizitatorul în lead. Eliminăm meniurile complexe și distragerile. Structură psihologică: Hero -> Problemă -> Soluție -> Dovadă -> CTA.",
            web_landing_title: "01. LANDING PAGE",
            web_process_section_title: "CUM LUCRĂM <span class='text-brand'>ÎMPREUNĂ?</span>",
            web_process_step_1: "<strong>Wireframe & Copy:</strong> Scriem textele înainte de design.",
            web_process_step_3: "<strong>Development:</strong> Scriem codul curat și rapid.",
            web_process_title: "PROCESUL DE DEZVOLTARE",
            web_project_type_1: "Landing Page (Conversie)",
            web_project_type_2: "Corporate Site (5–8 pagini)",
            web_project_type_3: "E-commerce (Shopify/Woo)",
            web_project_types_title: "TIPURI DE PROIECTE:",
            web_site_desc: "Pentru afaceri care au nevoie de validare și autoritate în piață. Include pagini esențiale (Despre, Servicii, Portofoliu) și optimizare SEO On-Page de bază.",
            web_site_title: "02. SITE DE PREZENTARE",
            web_stack_title: "STACK:",
            web_step_1_desc: "Săptămâna 1. Primim acces la conturi, analizăm istoricul și setăm obiectivele KPI.",
            web_step_1_title: "AUDIT & ONBOARDING",
            web_step_2_desc: "Săptămâna 2. Definim arhitectura site-ului, scriem copy-ul și pregătim designul.",
            web_step_2_title: "STRATEGIE & SETUP",
            web_step_3_desc: "Dezvoltare, optimizare viteză, testare formulare și redirecționări corecte.",
            web_step_3_title: "BUILD & QA",
            web_step_4_desc: "Lansare controlată, monitorizare heatmaps/analytics și iterații în primele 30 de zile.",
            web_step_4_title: "GO LIVE & ITERAȚIE",
            web_title: "WEB <span class='text-outline'>ENGINEERING</span>",
        },
        en: {
            // ... (Păstrează traducerile tale din engleză aici)
        },
        it: {
            // ... (Păstrează traducerile tale din italiană aici)
        }
    };

    const loadMarketingPixels = () => {
        if (window.__pixelsLoaded) return;
        window.__pixelsLoaded = true;

        // GA4
        const gaScript = document.createElement('script');
        gaScript.async = true;
        gaScript.src = `https://www.googletagmanager.com/gtag/js?id=${TRACKING_CONFIG.ga4_id}`;
        document.head.appendChild(gaScript);

        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', TRACKING_CONFIG.ga4_id);

        // TikTok Pixel
        !function (w, d, t) {
            w.TiktokAnalyticsObject = t;
            var ttq = w[t] = w[t] || [];
            ttq.methods = ["page", "track", "identify", "instances", "debug", "on", "off", "once", "ready", "alias", "group", "enableCookie", "disableCookie", "holdConsent", "revokeConsent", "grantConsent"];
            ttq.setAndDefer = function (t, e) { t[e] = function () { t.push([e].concat(Array.prototype.slice.call(arguments, 0))); }; };
            for (var i = 0; i < ttq.methods.length; i++) ttq.setAndDefer(ttq, ttq.methods[i]);
            ttq.instance = function (t) {
                var e = ttq._i[t] || [];
                for (var n = 0; n < ttq.methods.length; n++) ttq.setAndDefer(e, ttq.methods[n]);
                return e;
            };
            ttq.load = function (e, n) {
                var r = "https://analytics.tiktok.com/i18n/pixel/events.js", o = n && n.partner;
                ttq._i = ttq._i || {};
                ttq._i[e] = [];
                ttq._i[e]._u = r;
                ttq._t = ttq._t || {};
                ttq._t[e] = +new Date;
                ttq._o = ttq._o || {};
                ttq._o[e] = n || {};
                n = d.createElement("script");
                n.type = "text/javascript";
                n.async = true;
                n.src = r + "?sdkid=" + e + "&lib=" + t;
                e = d.getElementsByTagName("script")[0];
                e.parentNode.insertBefore(n, e);
            };
            ttq.load(TRACKING_CONFIG.tiktok_pixel_id);
            ttq.page();
        }(window, document, 'ttq');

        // Meta Pixel
        !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
        fbq('init', TRACKING_CONFIG.meta_pixel_id);
        fbq('track', 'PageView');
    };

    const setupCookieBanner = () => {
        const consent = localStorage.getItem('cookieConsent');

        if (consent === 'granted') {
            loadMarketingPixels();
            return;
        }

        if (consent === null) {
            const overlay = document.createElement('div');
            overlay.className = 'cookie-overlay';
            overlay.id = 'cookieOverlay';
            overlay.innerHTML = `
                <div class="cookie-banner">
                    <h3>COOKIE CONSENT</h3>
                    <p>Salut! Folosim cookie-uri pentru a optimiza performanța campaniilor și pentru a-ți oferi o experiență personalizată.</p>
                    <div class="cookie-banner__actions">
                        <button class="cookie-btn-accept" onclick="window.setConsent('granted')">Acceptă tot</button>
                        <button class="cookie-btn-refuse" onclick="window.setConsent('denied')">Refuză</button>
                        <a href="politica.html" class="cookie-btn-link">Mai multe detalii</a>
                    </div>
                </div>
            `;
            document.body.appendChild(overlay);
            document.body.classList.add('cookie-modal-open');
        }

        window.setConsent = (status) => {
            localStorage.setItem('cookieConsent', status);
            if (status === 'granted') loadMarketingPixels();

            const overlay = document.getElementById('cookieOverlay');
            if (overlay) overlay.remove();
            document.body.classList.remove('cookie-modal-open');
        };
    };

    const setupLangSwitcher = () => {
        window.changeLanguage = (lang) => {
            document.documentElement.setAttribute('lang', lang);
            document.querySelectorAll('[data-lang]').forEach((el) => {
                const key = el.getAttribute('data-lang');
                const value = translations[lang] ? (translations[lang][key] || translations['ro'][key]) : translations['ro'][key];
                if (value) el.innerHTML = value;
            });
            document.querySelectorAll('.lang-btn').forEach((btn) => {
                btn.classList.toggle('active', btn.getAttribute('onclick').includes(lang));
            });
            localStorage.setItem('preferredLang', lang);
        };
        const savedLang = localStorage.getItem('preferredLang') || 'ro';
        window.changeLanguage(savedLang);
    };

    const setupMenu = () => {
        const hamburger = document.querySelector('.hamburger');
        const mobileMenu = document.getElementById('mobileMenu');
        if (!hamburger || !mobileMenu) return;

        hamburger.addEventListener('click', () => {
            mobileMenu.classList.toggle('active');
            hamburger.classList.toggle('active');
        });
    };

    // --- CURSORUL PERSONALIZAT ---
    const setupCursor = () => {
        if (!window.matchMedia('(pointer: fine)').matches) return;

        const cursorDot = document.createElement('div');
        const cursorOutline = document.createElement('div');
        cursorDot.className = 'cursor-dot';
        cursorOutline.className = 'cursor-outline';
        document.body.appendChild(cursorDot);
        document.body.appendChild(cursorOutline);

        window.addEventListener('mousemove', (e) => {
            const posX = e.clientX;
            const posY = e.clientY;

            cursorDot.style.left = `${posX}px`;
            cursorDot.style.top = `${posY}px`;

            cursorOutline.animate(
                { left: `${posX}px`, top: `${posY}px` },
                { duration: 500, fill: 'forwards' }
            );
        });

        const hoverables = document.querySelectorAll('a, button, .pill-btn, .editorial-card, .poster-visual');
        hoverables.forEach((el) => {
            el.addEventListener('mouseenter', () => document.body.classList.add('hovering'));
            el.addEventListener('mouseleave', () => document.body.classList.remove('hovering'));
        });
    };

    // --- ANIMAȚIILE DE APARIȚIE (REVEAL) ---
    const setupReveal = () => {
        const elements = document.querySelectorAll('.reveal');
        if (!elements.length) return;

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) entry.target.classList.add('active');
                });
            },
            { threshold: 0.1 }
        );

        elements.forEach((el) => observer.observe(el));
    };

    document.addEventListener('DOMContentLoaded', () => {
        setupMenu();
        setupLangSwitcher();
        setupCookieBanner();
        setupCursor();
        setupReveal();
    });
})();
