# AUDIT-REPORT.md — Green Pheonix Concept

**Branch:** `refactor/astro-migration-prep`
**Date:** 2026-05-26
**Scope:** Pre-migration audit of the static site (HTML/CSS/JS) prior to migration to Astro 5 + Tailwind 4 (trilingual RO/IT/EN + blog + AEO/GEO schema).
**Note:** No HTML/CSS/JS source files have been modified in this pass. The only repo mutations are: (a) salvage of reusable assets from the legacy `greenpheonix/` Django folder into `_legacy-assets/`, and (b) deletion of the now-redundant `greenpheonix/` folder.

---

## Executive summary

The static site is structurally healthy (semantic HTML, complete `alt` coverage, consent-gated tracking) but carries significant CSS debt that will become friction during the Astro/Tailwind migration if not addressed: 3 coexisting cookie-banner stylesheets, ~62 `!important` declarations (several of which contradict the reveal-animation logic), and ~15% selector duplication concentrated in the cookie banner and reveal blocks. BPD Transport material (a former client) is woven into 5 pages and must be excised. The legacy Django prototype at `greenpheonix/` was a parallel duplicate of the site with extra production-grade scaffolding (i18n dictionary, branded email templates, Stripe/BT integration, Django models for testimonials/case studies/blog) — the reusable parts have been salvaged to `_legacy-assets/` and the folder has been deleted. The brand name is correctly spelled `Pheonix` (non-standard, intentional) everywhere — no `Phoenix` typos found.

---

## File inventory (root only — post-cleanup)

### HTML
| File | Lines |
|---|---|
| `index.html` | 420 |
| `landing-transportatori.html` | 301 |
| `servicii-ads.html` | 242 |
| `servicii-web.html` | 225 |
| `proiect-detaliu.html` | 221 |
| `contact.html` | 220 |
| `portofoliu.html` | 190 |
| `studiu-caz-bpd.html` | 189 |
| `politica.html` | 170 |
| `despre.html` | 154 |
| `404.html` | 99 |
| **Total** | **2431** |

### CSS
| File | Lines |
|---|---|
| `style.css` | **1698** |

### JS
| File | Lines |
|---|---|
| `main.js` | 343 |

### Images & video (root)
| File | Size |
|---|---|
| `gpc-site.zip` | 14 MB (legacy backup — candidate for deletion) |
| `hero_gpc.svg` | 2.9 MB (SVG is oversized — likely embeds raster) |
| `video marketing bpd.mp4` | 2.4 MB (BPD — to remove) |
| `video website bpd.mp4` | 2.3 MB (BPD — to remove) |
| `founder.png` | 2.3 MB (needs WebP/AVIF + resize) |
| `mockup_laptop_bpd.mp4` | 1.9 MB (BPD — to remove) |
| `europa.png` | 1.9 MB (needs compression) |
| `mockup_web_mobil.svg` | 988 KB |
| `logo_gpc.svg` | 568 KB (oversized SVG) |
| `solutionarea_oline.png` | 52 KB |
| `solutionarea_alternativa.png` | 52 KB |
| `og-transport.jpg` / `og-web.jpg` / `og-image.jpg` / `og-ads.jpg` | 38–44 KB each |
| `founder-og.jpg` | 36 KB |
| `logo_bpdtrans.png` | 20 KB (BPD — to remove) |
| `favicon.svg` / `favicon-32.png` / `favicon-16.png` | <1 KB each |

### Config / docs / other
- `.editorconfig`
- `.vscode/settings.json` (42 bytes)
- `.claude/settings.local.json`
- `robots.txt`, `sitemap.xml`
- `README.md` (2 lines — placeholder)
- `GreenPheonix_Plan_Complet_Modificari.md` (19 KB) and `GreenPheonix_Plan_Complet_Modificari (1).md` (25 KB) — **two near-duplicate planning docs**
- `_legacy-assets/` — new, contains salvaged material (see below)
- No `package.json`, no `.github/`, no CI

---

## Legacy `greenpheonix/` folder — what was there

The folder was a **complete Django 4+ prototype** (~5,655 lines of templates + Python apps) that duplicated the public site and added production scaffolding never wired into the live build:

- **Django apps:** `core`, `servicii`, `studii_de_caz`, `blog`, `contact`, `plati` (payments)
- **Templates:** 38 HTML files mirroring the static site + email templates + payment portal + login/registration
- **Static duplicates:** 17 images + 3 videos identical to root-level assets (megabytes of duplication)
- **i18n:** `static/js/translations.js` — full RO/EN dictionary (~60 keys covering navbar, hero, services, testimonials, portfolio, CTA, footer)
- **Branded transactional emails:** `welcome_client.html`, `contract_client.html` (inline-CSS, Outlook-safe)
- **Cookie banner:** a single clean Django partial (`includes/cookie_banner.html`) — the canonical version that the static `style.css` triplicated
- **Schema markup:** `includes/schema_markup.html` — `LocalBusiness` JSON-LD (NAP, taxID `RO45667331`, founder, areaServed, serviceType, sameAs)
- **Real case-study fixtures:** BPD Transport + CBS Express with metrics
- **Payments:** Stripe service helper, BT Pay integration, full subscription model (`Abonament`, `Plata`, `RaportClient`, `LivrabilClient`, `PromoTrial`, `ContractSemnat`)
- **Models worth keeping as schema reference:** Testimonial, StudiuDeCaz, BlogPost

### What was salvaged → `_legacy-assets/`
```
_legacy-assets/
├── README.md                              (index + usage notes)
├── i18n/translations.js                   (RO+EN seed for Astro i18n; add IT)
├── email-templates/
│   ├── welcome_client.html                (branded HTML email)
│   └── contract_client.html
├── includes/
│   ├── base.html                          (Django page shell)
│   ├── navbar.html                        (with i18n data-* attrs + lang switcher)
│   ├── footer.html
│   ├── cookie_banner.html                 (canonical single-banner markup)
│   └── schema_markup.html                 (LocalBusiness JSON-LD)
├── data/case-studies-fixtures.json        (BPD + CBS, real metrics)
├── payments-reference/
│   ├── stripe_service.py
│   ├── bt_pay.py
│   └── django_models.py
└── django-models-reference/
    ├── core_models.py                     (Testimonial)
    ├── case_studies_models.py             (StudiuDeCaz)
    └── blog_models.py
```

### What was deleted
The entire `greenpheonix/` Django app (apps/, config/, migrations, manage.py, requirements.txt, duplicated static media, and template files that mirror the static site). All deletions are reversible via git history on this branch.

---

## Critical problems (must-fix BEFORE Astro migration)

1. **Cookie banner triplication in `style.css`** — three independent style blocks coexist:
   - lines **901–940**: white minimal banner (`.cookie-banner__btn`)
   - lines **1331–1406**: premium dark variant with brand-green border (incl. mobile dup at 1393)
   - lines **1449–1520**: brutalist dark variant (`.cookie-btn-accept` / `.cookie-btn-refuse`)
   
   ~150 lines of redundant CSS, all live. Decide on ONE design (the canonical Django partial in `_legacy-assets/includes/cookie_banner.html` uses the `.cookie-btn-accept/refuse` classnames, suggesting version #3 was the intended final). Remove the other two in the migration.

2. **`.reveal` animation `!important` chaos** — `.reveal` is defined twice (lines 81 and 1594) with conflicting rules. The block at lines 81–89 uses 3 `!important` flags that override the animation rules defined later, breaking the intersection-observer reveal behavior in subtle ways. Re-author from scratch in Tailwind (`@starting-style` / `data-state` pattern).

3. **BPD Transport content removal (28 references across 5 files):**
   - `studiu-caz-bpd.html` — 12 mentions (entire page → delete)
   - `proiect-detaliu.html` — 8 mentions
   - `index.html` — 4 mentions
   - `portofoliu.html` — 3 mentions
   - `landing-transportatori.html` — 1 mention
   
   Also delete: `logo_bpdtrans.png`, `video marketing bpd.mp4`, `video website bpd.mp4`, `mockup_laptop_bpd.mp4`, `og-transport.jpg`, and the BPD entry in `_legacy-assets/data/case-studies-fixtures.json` (keep the CBS Express entry).

4. **Two near-duplicate planning docs at the root** — `GreenPheonix_Plan_Complet_Modificari.md` (19 KB) and `GreenPheonix_Plan_Complet_Modificari (1).md` (25 KB). Diff them, keep the canonical one (or move to `docs/`), delete the other.

5. **`gpc-site.zip` (14 MB) committed to repo root** — a full backup of the live site. Move out of the repo or delete; large binaries in git inflate clone size permanently.

---

## Moderate problems (address DURING migration)

6. **CSS custom properties** — 15 declared in `:root` (style.css:1–30), 2 unused: `--text-inverse` (line 23), `--brand-light` (line 5). Move tokens to Tailwind theme config; drop unused.

7. **62 `!important` declarations** — heavy usage in mobile breakpoints (lines 1014–1043) and reveal blocks. Acceptable in `prefers-reduced-motion` (lines 1250–1260). Rebuild in Tailwind utility-first to eliminate.

8. **16 duplicated selectors (~4.5% of 357 total)** — mostly clustered in cookie-banner block. Resolves itself when cookie banner is consolidated.

9. **`politica.html` is missing all SEO metadata** — no `<meta name="description">`, no `og:*`, no `twitter:*`. Every other page has 7–9 OG/Twitter tags.

10. **No `<article>` element used anywhere** — appropriate to introduce on `studiu-caz-*`, blog detail, `proiect-detaliu` pages during migration.

11. **i18n is RO/EN only** — `_legacy-assets/i18n/translations.js` covers RO + EN. The target is trilingual RO/IT/EN; the IT keys need to be authored (use the existing keys as the contract).

12. **Schema markup contradiction** — `_legacy-assets/includes/schema_markup.html` lists address as `Gura Calitei, VN` (Vrancea), but the brief describes the agency as Brașov-based. Reconcile NAP across schema, footer, and contact page before migration; AEO/GEO will fail if NAP isn't consistent.

13. **`hero_gpc.svg` (2.9 MB) and `logo_gpc.svg` (568 KB)** — abnormally large for SVGs; likely embed raster data or unoptimized paths. Run SVGO or re-export.

14. **`founder.png` (2.3 MB) and `europa.png` (1.9 MB)** — convert to WebP/AVIF with `<picture>` fallback and serve responsively.

15. **`README.md` is 2 lines** — write a real README during migration with stack, dev setup, deploy notes.

---

## Minor problems (nice-to-have)

16. **`main.js` has empty `en` and `it` translation stubs (lines 162–167)** — TODOs that will be replaced when the Astro i18n routing is built.

17. **Custom-cursor implementation (`main.js` lines 289–317)** — uses requestAnimationFrame on every `mousemove`. Consider gating behind `pointer: fine` media query in the Astro version, or removing entirely (debatable UX value).

18. **No `.github/` directory, no CI** — add a minimal workflow during migration (typecheck, build, Lighthouse on PRs).

19. **No `package.json`** — expected; will be added with Astro 5.

20. **Pheonix vs Phoenix:** verified — **100% `Pheonix`** across all root HTML (50+ instances). No corrections needed. (Be aware: the misspelling is intentional, but external tools/SEO will sometimes auto-correct; lock it in `<title>` and `og:site_name`.)

21. **Accessibility baseline is good:** 0 images without `alt`, 0 icon-only buttons without `aria-label`, 3 contact-form inputs all properly labelled with `for`/`id`. Maintain this standard in the Astro port.

---

## External dependencies present

- **Google Fonts** (loaded on 7 pages): Oswald (400, 700), Space Grotesk (300, 600), Space Mono — `https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&family=Space+Grotesk:wght@300;600&family=Space+Mono`
- **GA4:** `G-BP0J2SJTP1` (gated behind cookie consent, `main.js:177–183`)
- **Meta Pixel:** `1250834263629342` (gated, `main.js:218–220`)
- **TikTok Pixel:** `D64F6T3C77U69UNGKT30` (gated, `main.js:186–215`)
- **Microsoft Clarity:** **NOT installed** — add during migration if desired
- No jQuery, no GSAP, no AOS — animations are hand-rolled with IntersectionObserver

Tracking consent flow is correct (localStorage-persisted, pixels only load after `grant`). Port this logic 1:1 into the Astro version.

---

## Recommended next steps

1. **Merge the two planning markdown docs** into one canonical `docs/PLAN.md`, delete the duplicate, and remove `gpc-site.zip`. Quick win, frees ~14 MB.
2. **Decide on ONE cookie banner design** (recommend version #3 / `.cookie-btn-accept`, matching the Django partial). This decision unlocks ~150 lines of CSS cleanup.
3. **Reconcile NAP** (Brașov vs Gura Calitei / VN) across schema, footer, contact page — must be settled before AEO/GEO schema is locked in.
4. **Strip all BPD content** as a single dedicated commit on this branch: delete `studiu-caz-bpd.html`, the 4 BPD media files, and edit out the 28 textual references. Keep the case-study layout — it'll host CBS Express + future studies.
5. **Author IT translations** against the keys in `_legacy-assets/i18n/translations.js` while the dictionary is fresh.
6. **Initialize Astro 5 + Tailwind 4** in a new top-level structure (e.g. `src/`, `public/`), porting `_legacy-assets/includes/cookie_banner.html`, `schema_markup.html`, navbar/footer as Astro components first to validate the design system.
7. **Compress hero/founder/europa images** (WebP/AVIF + SVGO) — measurable LCP improvement before any code is shipped.

---

## Sign-off

- `refactor/astro-migration-prep` branch: created and checked out.
- `_legacy-assets/`: populated (i18n, emails, includes, fixtures, payments + models references). Index in `_legacy-assets/README.md`.
- `greenpheonix/`: removed via `git rm -rf` (recoverable from history if needed).
- No HTML/CSS/JS source files modified in this audit pass.
