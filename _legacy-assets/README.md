# _legacy-assets/

Reusable assets salvaged from the legacy Django prototype (`greenpheonix/`) before deleting it.
These are reference materials for the upcoming Astro 5 + Tailwind 4 migration.

## Contents

### `i18n/translations.js`
Client-side i18n dictionary (RO + EN) used by the legacy Django build.
Covers navbar, hero, services, testimonials, portfolio, FAQ, CTA, footer.
**Use:** seed for Astro `src/i18n/` JSON files. Add IT keys to complete the trilingual set.

### `email-templates/`
- `welcome_client.html` — onboarding email (account activation, password reset CTA, kickoff steps)
- `contract_client.html` — contract delivery email

Branded HTML emails with inline CSS (Outlook-safe). Ready to reuse with any transactional provider
(Resend, Postmark, Brevo). Replace Django `{{ var }}` placeholders with the target template syntax.

### `includes/`
Django template partials that map directly to Astro components:
- `base.html` — page shell (head, fonts, GA4/Pixel slots, navbar/footer/cookie banner includes)
- `navbar.html` — desktop + mobile nav with i18n `data-i18n` attributes and language switcher
- `footer.html`
- `cookie_banner.html` — **the single canonical cookie banner** (the static site has 3 conflicting versions)
- `schema_markup.html` — LocalBusiness JSON-LD (NAP, taxID, founder, services)

### `data/case-studies-fixtures.json`
Django fixture with 2 real case studies (BPD Transport, CBS Express) — metrics, copy, structure.
**Note:** BPD will be removed from the public site, but the data shape is useful as a CMS schema reference.
CBS Express is a keeper.

### `payments-reference/`
- `stripe_service.py` — Stripe Checkout / subscription helper
- `bt_pay.py` — Banca Transilvania payment gateway integration
- `django_models.py` — `Abonament`, `Plata`, `LivrabilClient`, `RaportClient`, `PromoTrial`, `ContractSemnat`

Reference only — informs the data model for the Astro + (Stripe/BT) integration.

### `django-models-reference/`
- `core_models.py` — Testimonial model (with `client_foto`, `rezultat_cheie`, `client_industrie`)
- `case_studies_models.py` — StudiuDeCaz model (slug, industrie, canal, metrici, featured)
- `blog_models.py` — blog post schema

Use these to design the content schema (Astro Content Collections / headless CMS).

---

**This folder is reference material. Do not import from it at runtime in the new build.**
