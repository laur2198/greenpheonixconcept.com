# Plan Complet Modificări Site — Green Pheonix Concept
## Document pentru Claude Code — Toate modificările din conversație

---

## CUM FOLOSEȘTI ACEST DOCUMENT

1. Deschizi terminalul în folderul proiectului: `cd greenpheonix && claude`
2. Îi spui lui Claude Code: *"Citește fișierul GreenPheonix_Plan_Complet_Modificari.md și implementează modificările în ordinea exactă din document. Confirmă-mi după fiecare fază înainte să treci la următoarea."*
3. Lucrezi fază cu fază — nu sări peste nicio fază
4. Testezi local după fiecare fază înainte să continui

---

## REGULI GENERALE PENTRU CLAUDE CODE

- **Nu rescrie** nimic existent care funcționează — doar extinde
- **Păstrează stilul vizual** — dark theme, accente auriu/verde, font bold, grid overlay, estetică tech/terminal
- **Nu introduce** React, Vue sau orice framework JS nou — site-ul folosește JS vanilla
- **Toate variabilele sensibile** (Stripe keys, secret key, DB) în fișierul `.env` — niciodată hardcodate
- **Comentează în română** orice funcție sau clasă nouă
- **Testează fiecare URL nou** înainte de a trece la faza următoare
- **Nu șterge** migrații existente

---

## FAZA 1 — FUNDAȚIE & SETUP
### Prioritate: Obligatoriu primul

**1.1 — Fișier .env și variabile de environment**

Creează fișierul `.env` în rădăcina folderului `greenpheonix/` cu următoarele variabile goale de completat manual:

```
SECRET_KEY=
DEBUG=True
DATABASE_URL=
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_ID_STARTER=price_...
STRIPE_PRICE_ID_BUSINESS=price_...
STRIPE_PRICE_ID_PRO=price_...
EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
ALLOWED_HOSTS=localhost,127.0.0.1
```

Adaugă `.env` în `.gitignore` dacă nu e deja acolo.

Instalează `python-decouple` și actualizează `requirements.txt`.

Actualizează `config/settings/base.py` să citească toate variabilele din `.env` via decouple.

**1.2 — Dependențe noi**

Adaugă în `requirements.txt` și instalează:
- `stripe>=7.0.0`
- `Pillow>=10.0.0`
- `python-decouple>=3.8`

**1.3 — Media files**

În `config/settings/base.py` adaugă:
```
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

În `config/urls.py` adaugă servirea media în development.

**1.4 — Auth settings**

În `config/settings/base.py` adaugă:
```
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/portal/'
LOGOUT_REDIRECT_URL = '/'
```

---

## FAZA 2 — MODELE NOI (toate migrațiile)
### Prioritate: Înainte de orice template sau view

**2.1 — Model Pachet** în `apps/servicii/models.py`

Câmpuri obligatorii:
- `nume` — CharField max 50
- `tier` — CharField cu choices: starter / business / pro
- `pret_lunar` — DecimalField EUR
- `pret_setup` — DecimalField EUR, default 0
- `descriere` — TextField scurt (1-2 propoziții)
- `features` — JSONField listă de string-uri (bullet points)
- `recomandat` — BooleanField (cardul evidențiat)
- `activ` — BooleanField
- `ordine` — PositiveIntegerField pentru sortare manuală
- Meta ordering: `['ordine']`

**2.2 — Model StudiuDeCaz** — verifică `apps/studii_de_caz/models.py` și adaugă câmpurile lipsă:
- `titlu`, `slug` (unic, auto-generat)
- `client` — CharField
- `nisa` — CharField
- `problema` — TextField
- `solutie` — TextField
- `rezultate` — TextField
- `perioada` — CharField (ex: "Ian 2026 – prezent")
- `imagine_cover` — ImageField upload_to='studii_de_caz/'
- `logo_client` — ImageField opțional
- `featured` — BooleanField (apare pe homepage)
- `activ` — BooleanField
- `creat_la` — auto_now_add
- Meta ordering: `['-creat_la']`

**2.3 — Modele Stripe** în `apps/plati/models.py` — adaugă:

Model `Abonament`:
- `user` — ForeignKey la User Django
- `pachet` — ForeignKey la Pachet
- `stripe_subscription_id` — CharField
- `stripe_customer_id` — CharField
- `status` — choices: activ / anulat / suspendat / trial
- `data_start` — DateTimeField
- `data_urmatoarei_plati` — DateTimeField null/blank
- `creat_la` — auto_now_add

Model `Plata`:
- `abonament` — ForeignKey la Abonament
- `stripe_payment_intent_id` — CharField
- `suma` — DecimalField
- `valuta` — CharField default 'eur'
- `status` — choices: reusit / esuat / pending
- `data_plata` — DateTimeField
- `factura_url` — URLField blank (link Stripe invoice)

Model `RaportClient`:
- `abonament` — ForeignKey la Abonament
- `titlu` — CharField (ex: "Raport Mai 2026")
- `luna` — DateField
- `fisier` — FileField upload_to='rapoarte/'
- `creat_la` — auto_now_add

Model `LivrabilClient`:
- `abonament` — ForeignKey la Abonament
- `titlu` — CharField
- `categorie` — choices: reclame / rapoarte / documente / altele
- `fisier` — FileField upload_to='livrabile/'
- `descriere` — TextField blank
- `creat_la` — auto_now_add

**2.4 — Rulează migrațiile**
```
python manage.py makemigrations servicii
python manage.py makemigrations studii_de_caz
python manage.py makemigrations plati
python manage.py migrate
```

---

## FAZA 3 — ADMIN PANEL EXTINS
### Prioritate: Înainte de views — vrei să poți adăuga date din admin

**3.1 — Admin Pachete** în `apps/servicii/admin.py`:
- Înregistrează modelul `Pachet`
- List display: nume, tier, pret_lunar, recomandat, activ, ordine
- List filter: tier, recomandat, activ
- List editable: ordine, activ, recomandat
- Search: nume

**3.2 — Admin Studii de Caz** în `apps/studii_de_caz/admin.py`:
- List display: titlu, client, nisa, featured, activ, creat_la
- List filter: featured, activ, nisa
- Search: titlu, client
- Prepopulate slug din titlu
- Fieldsets organizate: Info generale / Conținut / Media / Setări

**3.3 — Admin Abonamente** în `apps/plati/admin.py`:
- List display: user, pachet, status, data_start, data_urmatoarei_plati
- List filter: status, pachet
- Search: user__email, stripe_customer_id
- Inline `Plata` în pagina de Abonament (readonly)
- Inline `RaportClient` în pagina de Abonament
- Inline `LivrabilClient` în pagina de Abonament

---

## FAZA 4 — PAGINA PACHETE & PREȚURI
### Prima pagină vizibilă nouă

**4.1 — View** în `apps/servicii/views.py`:
- Funcție `pachete` care returnează toate pachetele active ordonate

**4.2 — URL** în `apps/servicii/urls.py`:
- `path('pachete/', views.pachete, name='pachete')`

**4.3 — Template** `templates/servicii/pachete.html`:

Layout: 3 carduri side-by-side pe desktop, stack pe mobil

Fiecare card conține:
- Badge "Cel mai ales" dacă `pachet.recomandat == True`
- Numele pachetului (mare, bold)
- Prețul lunar (foarte mare, auriu)
- Info setup — dacă `pret_setup > 0` afișează "+ Xâ‚¬ setup o singură dată", altfel "Setup inclus gratuit"
- Descrierea scurtă
- Lista features cu icon checkmark în față la fiecare
- Buton CTA: "Vreau acest pachet" → deschide WhatsApp cu mesaj pre-completat:
  `https://wa.me/40793650902?text=Salut%2C+vreau+detalii+despre+pachetul+[NUME_PACHET]`

Stilul cardului recomandat: border auriu, ușor mai mare, badge vizibil

**4.4 — Navbar** în `templates/includes/navbar.html`:
- Adaugă link "Pachete & Prețuri" → `{% url 'pachete' %}`

---

## FAZA 5 — STUDII DE CAZ ACTUALIZATE

**5.1 — Views** în `apps/studii_de_caz/views.py`:
- View `lista` — toate studiile active
- View `detail` — studiu individual după slug
- View `featured` — primele 2-3 cu `featured=True` pentru homepage

**5.2 — URLs** în `apps/studii_de_caz/urls.py`:
- `path('', views.lista, name='studii_lista')`
- `path('<slug:slug>/', views.detail, name='studiu_detail')`

**5.3 — Template lista** `templates/studii_de_caz/lista.html`:
- Grid 2 coloane pe desktop, 1 pe mobil
- Fiecare card: imagine cover, titlu, client, nișă, perioadă, buton "Vezi studiul complet"

**5.4 — Template detail** `templates/studii_de_caz/detail.html`:
- Hero cu imagine cover full-width
- Secțiuni separate: Problema / Soluția / Rezultatele
- Logo client dacă există
- Buton "Lucrăm împreună?" → pagina pachete

**5.5 — Homepage** `templates/core/home.html`:
- Adaugă secțiune "Studii de caz" cu primele 2 studii featured
- Link "Vezi toate" → lista studii

---

## FAZA 6 — PAGINA DESPRE — SECȚIUNEA EXPERIENȚĂ

**Fișier:** `templates/core/despre.html`

Adaugă secțiune nouă după bio-ul existent cu titlul "Experiență cu branduri reale".

Conține 2 carduri side-by-side:

Card 1:
- Tag: FMCG / Retail
- Titlu: Reinert & Martinel — The Family Butchers Romania
- Descriere: Social media management, strategie de conținut și colaborare pe packaging pentru piața românească. Experiență directă în industria alimentară și retail FMCG.

Card 2:
- Tag: Transport / Logistică
- Titlu: VIP-Transporte
- Descriere: Campanii Meta Ads pentru diaspora română din Germania și Austria. Creatives, audiențe, optimizare continuă și strategie de comunicare pe WhatsApp.

---

## FAZA 7 — INTEGRARE STRIPE

**7.1 — Serviciu Stripe** — creează fișier nou `apps/plati/stripe_service.py`:

Funcții necesare:
- `creeaza_customer(email, nume)` — creează customer în Stripe
- `creeaza_abonament(customer_id, price_id)` — creează subscription
- `anuleaza_abonament(subscription_id)` — anulează la sfârșitul perioadei
- `obtine_facturi(customer_id)` — returnează lista facturi
- `creeaza_portal_session(customer_id)` — Stripe Customer Portal

**7.2 — Views Stripe** în `apps/plati/views.py`:

View `checkout(request, pachet_slug)`:
- Require login
- Obține pachetul după slug
- Mapează la Stripe Price ID din settings
- Creează Stripe Checkout Session cu `mode='subscription'`
- Redirect la Stripe hosted checkout
- La succes redirect la `/portal/`

View `webhook(request)`:
- Acceptă doar POST
- Validează semnătura Stripe cu `STRIPE_WEBHOOK_SECRET`
- Procesează evenimentele:
  - `invoice.paid` → actualizează Plata și Abonament status=activ
  - `invoice.payment_failed` → status=suspendat
  - `customer.subscription.deleted` → status=anulat
  - `customer.subscription.updated` → actualizează data_urmatoarei_plati
- Returnează HTTP 200 întotdeauna (chiar și la erori — altfel Stripe retrimite)

View `anuleaza_abonament(request)`:
- Require login
- POST only
- Apelează `stripe_service.anuleaza_abonament()`
- Actualizează modelul local
- Redirect la portal cu mesaj confirmare

**7.3 — URLs** în `apps/plati/urls.py`:
- `path('checkout/<slug:pachet_slug>/', views.checkout, name='checkout')`
- `path('webhook/', views.webhook, name='stripe_webhook')`
- `path('anuleaza/', views.anuleaza_abonament, name='anuleaza_abonament')`
- `path('portal/', views.portal_client, name='portal_client')`

**7.4 — URL principal** în `config/urls.py`:
- `path('plati/', include('apps.plati.urls'))`
- `path('', include('django.contrib.auth.urls'))`

**7.5 — Buton checkout pe pagina pachete**:
- Dacă user autentificat → link la `/plati/checkout/<pachet_slug>/`
- Dacă user neautentificat → link la WhatsApp (comportament actual)

---

## FAZA 8 — PORTAL CLIENT

**View `portal_client`** în `apps/plati/views.py`:
- `@login_required`
- Obține abonamentul activ al userului curent
- Obține rapoartele și livrabilele asociate
- Obține istoricul plăților

**Template** `templates/plati/portal_client.html`:

Secțiunea 1 — Abonamentul meu:
- Numele pachetului activ + lista features
- Status cu culoare (verde=activ, roșu=anulat, galben=suspendat)
- Data următoarei plăți
- Buton "Schimbă pachetul" → pagina pachete
- Buton "Anulează abonamentul" → modal confirmare → POST la `/plati/anuleaza/`

Secțiunea 2 — Istoricul plăților:
- Tabel: Data / Suma / Status / Factură
- Link descărcare factură din `factura_url` dacă există

Secțiunea 3 — Rapoarte lunare:
- Cards cu: titlu, luna, buton Download
- Mesaj "Nu există rapoarte încă" dacă lista e goală

Secțiunea 4 — Livrabile & Fișiere:
- Filtru pe categorii: Toate / Reclame / Rapoarte / Documente / Altele
- Cards cu: titlu, categorie, descriere, buton Download
- Mesaj "Nu există fișiere încă" dacă lista e goală

---

## FAZA 9 — AUTENTIFICARE CLIENT

**Templates de creat** (stil consistent cu site-ul — dark theme):
- `templates/registration/login.html` — formular email + parolă, link "Am uitat parola"
- `templates/registration/password_reset_form.html`
- `templates/registration/password_reset_done.html`
- `templates/registration/password_reset_confirm.html`
- `templates/registration/password_reset_complete.html`

**Navbar actualizare** în `templates/includes/navbar.html`:
- Dacă `user.is_authenticated`:
  - Afișează "Bună, [user.first_name]" sau emailul
  - Link "Portalul meu" → `/plati/portal/`
  - Link "Deconectare" → logout
- Dacă neautentificat:
  - Link "Contul meu" → `/login/`
- Dacă `user.is_staff`:
  - Link "Admin" → `/admin/`

**Creare automată cont client** — în webhook Stripe la evenimentul `customer.subscription.created`:
- Verifică dacă există User cu emailul din Stripe
- Dacă nu există → creează User cu email și parolă random
- Trimite email cu link de setare parolă via Django `send_mail`
- Creează modelul `Abonament` asociat

---

## FAZA 10 — HOMEPAGE ACTUALIZAT

**Fișier:** `templates/core/home.html`

Adaugă/actualizează secțiunile:

Secțiunea Pachete (nou):
- Titlu: "Pachete clare. Prețuri corecte."
- Afișează cele 3 pachete în format compact (fără toate features)
- Buton "Vezi toate pachetele" → `/servicii/pachete/`

Secțiunea Studii de caz (nou):
- Titlu: "Rezultate reale"
- Primele 2 studii cu `featured=True`
- Buton "Vezi toate" → `/studii-de-caz/`

Secțiunea CTA final (actualizează):
- Titlu: "Gata să aduci mai mulți clienți?"
- Două butoane: "Vezi pachete" și "Scrie-ne pe WhatsApp"

---

## FAZA 11 — STRIPE PAYMENT LINKS (opțional, fără cod)

Aceasta nu necesită cod — se face manual în Stripe Dashboard:

1. Dashboard Stripe → Products → Add product pentru fiecare pachet
2. Setează recurring price în EUR lunar
3. Payment Links → Create → selectezi produsul
4. Copiezi link-ul generat

Salvează cele 3 linkuri generate:
- Starter: `https://buy.stripe.com/...`
- Business: `https://buy.stripe.com/...`
- Pro: `https://buy.stripe.com/...`

Aceste linkuri se pot pune direct pe pagina de pachete ca alternativă la checkout-ul Django, sau se trimit clienților pe WhatsApp fără nicio integrare tehnică.

---

## ORDINEA EXACTĂ DE IMPLEMENTARE

```
FAZA 1  → Setup .env și dependențe         (15 min)
FAZA 2  → Toate modelele + migrații        (30 min)
FAZA 3  → Admin extins                     (20 min)
         ↓ TESTEAZĂ: intră în /admin și adaugă date
FAZA 4  → Pagina Pachete                   (45 min)
         ↓ TESTEAZĂ: /servicii/pachete/ funcționează
FAZA 5  → Studii de caz                    (30 min)
         ↓ TESTEAZĂ: adaugă 2 studii din admin, verifică listare și detail
FAZA 6  → Pagina Despre                    (15 min)
         ↓ TESTEAZĂ: secțiunea experiență apare corect
FAZA 7  → Integrare Stripe                 (60 min)
         ↓ TESTEAZĂ: plată cu card 4242 4242 4242 4242
FAZA 8  → Portal client                    (45 min)
         ↓ TESTEAZĂ: autentificare + vedere portal
FAZA 9  → Autentificare client             (30 min)
         ↓ TESTEAZĂ: login/logout/reset parolă
FAZA 10 → Homepage actualizat              (20 min)
         ↓ TESTEAZĂ: toate secțiunile noi apar corect
FAZA 11 → Stripe Payment Links             (manual în dashboard)
```

**Total estimat: 5-6 ore de implementare cu Claude Code**

---

## DATE DE ADĂUGAT DIN ADMIN DUPĂ IMPLEMENTARE

### Pachete (adaugă în ordine):

**Pachet 1 — Starter**
- Tier: starter | Preț: 300€/lună | Setup: 200€ | Recomandat: Nu | Ordine: 1
- Features: ["8 postări social media/lună", "Raport lunar de performanță", "Suport WhatsApp în timpul săptămânii", "Monitorizare pagină Facebook/Instagram"]

**Pachet 2 — Business**
- Tier: business | Preț: 600€/lună | Setup: 0€ | Recomandat: Da | Ordine: 2
- Features: ["16 postări social media/lună", "Campanii Meta Ads (100€ buget inclus)", "Site de prezentare inclus gratuit", "Raport detaliat + call lunar de strategie", "Suport prioritar WhatsApp"]

**Pachet 3 — Pro**
- Tier: pro | Preț: 1.200€/lună | Setup: 0€ | Recomandat: Nu | Ordine: 3
- Features: ["20 postări + Stories zilnice", "Meta Ads + Google Ads (200€ buget inclus)", "Site premium cu funcționalități avansate", "Raport detaliat + call bilunar", "Suport prioritar 7 zile/săptămână", "Strategie trimestrială de marketing"]

### Studii de caz (adaugă după faza 5):

**Studiu 1 — VIP-Transporte**
- Slug: vip-transporte | Featured: Da | Activ: Da
- Nișă: Transport persoane și colete — Diaspora România–Germania/Austria
- Perioada: Ianuarie 2026 – prezent
- Problema: Zero prezență digitală, zero rezervări online, dependență exclusivă de recomandări word-of-mouth. Clientul nu era vizibil deloc pentru diaspora română din Germania și Austria.
- Soluția: Campanii Meta Ads cu obiectiv Messages/WhatsApp, creatives video și imagine statică cu hook emoțional, audiențe targetate diaspora română din DE/AT, copywriting în română adaptat pentru comunitatea din diaspora.
- Rezultatele: Campanii active cu reach constant în diaspora română, rezervări prin WhatsApp în creștere, primele rezultate vizibile în primele 2 săptămâni de la lansare.

**Studiu 2 — Lemet Stone SRL**
- Slug: lemet-stone | Featured: Da | Activ: Da
- Nișă: Fabricație și comercializare piatră naturală — B2B/B2C
- Perioada: Februarie 2026 – prezent
- Problema: Calculul prețurilor pentru blaturi de piatră (granit, marmură) se făcea manual în Excel pentru fiecare client în parte — proces lent, predispus la erori, și imposibil de utilizat direct de clienți pe site.
- Soluția: Calculator de prețuri WordPress/HTML plugin cu logică replicată exact din Excel-ul clientului, markup 30% integrat automat, calcul per MP și per ML în funcție de tipul de tăietură, interfață simplă pentru client final fără cunoștințe tehnice.
- Rezultatele: Automatizare completă a procesului de calculare prețuri, clienții pot obține un preț estimativ direct pe site fără să contacteze firma, economie de timp semnificativă pentru echipa Lemet Stone.

---

## CHECKLIST FINAL ÎNAINTE DE LIVE

- [ ] Toate fazele implementate și testate local
- [ ] Plată test cu cardul Stripe `4242 4242 4242 4242` funcționează
- [ ] Webhook Stripe procesat corect (verificat în Stripe Dashboard → Events)
- [ ] Portal client afișează corect datele
- [ ] Login/logout/reset parolă funcționează
- [ ] Toate paginile noi sunt accesibile din navbar
- [ ] `.env` nu e în GitHub (verifică `.gitignore`)
- [ ] Stripe keys schimbate din `pk_test_` în `pk_live_` pentru producție
- [ ] MEDIA_ROOT configurat corect pentru upload fișiere
- [ ] Site testat pe mobil (responsive)


---

## FAZA 12 — PACHET PROMO 7 ZILE

### Concept
Pachet de testare cu durată fixă de 7 zile la prețul de 50€ — reprezintă exclusiv comisionul agenției pentru setup și management inițial. Bugetul de reclame (Meta Ads / Google Ads) este separat și aparține clientului — nu este inclus în cei 50€ și nu trece prin Green Pheonix Concept.

---

### 12.1 — Model PromoTrial în `apps/plati/models.py`

Adaugă model nou:

```
PromoTrial:
- user (ForeignKey la User Django, null=True blank=True)
- nume_client (CharField — pentru clienți fără cont)
- email_client (EmailField)
- telefon_client (CharField)
- nisa_client (CharField — ex: Transport, FMCG, Turism)
- pachet_dorit_dupa_trial (ForeignKey la Pachet, null=True blank=True)
- stripe_payment_intent_id (CharField)
- suma (DecimalField, default=50.00)
- valuta (default: eur)
- status (choices: platit / activ / finalizat / anulat / convertit)
- data_start (DateTimeField, null=True)
- data_expirare (DateTimeField, null=True — calculat automat: data_start + 7 zile)
- convertit_la_pachet (BooleanField, default=False)
- nota_interna (TextField, blank=True — vizibil doar în admin)
- creat_la (auto_now_add)
```

Metodă pe model:
- `este_activ()` — returnează True dacă status=activ și data_expirare > now()
- `zile_ramase()` — returnează numărul de zile până la expirare

---

### 12.2 — Stripe — plată unică pentru trial

Spre deosebire de pachetele lunare care folosesc Subscriptions, Pachetul Promo folosește **Payment Intent** (plată unică de 50€, nu recurentă).

View `checkout_trial(request)` în `apps/plati/views.py`:
- Creează Stripe Checkout Session cu `mode='payment'` (nu subscription)
- Suma: 5000 (50€ în cenți)
- Descriere: "Pachet Promo 7 Zile — Green Pheonix Concept"
- La succes: creează PromoTrial cu status=platit, trimite email confirmare, redirect la `/portal/trial/`
- Metadata Stripe: email client, nișă, pachet dorit după trial

Webhook actualizat — adaugă handler pentru:
- `payment_intent.succeeded` → actualizează PromoTrial status=activ, setează data_start și data_expirare

---

### 12.3 — Pagină Trial în portal

Template `templates/plati/portal_trial.html`:

Afișează:
- Status trial (activ / expirat)
- Zile rămase (număr mare, vizibil)
- Ce primește în cele 7 zile (lista livrabile)
- Secțiune "Bugetul de reclame" — text explicativ clar:
  *"Bugetul investit în reclame (Meta Ads, Google Ads) este separat de comisionul agenției și aparține în totalitate contului tău de publicitate. Green Pheonix Concept nu accesează și nu administrează acești bani."*
- Buton "Continuă cu pachet lunar" → pagina pachete
- Dacă trial expirat: banner prominent cu CTA "Alege pachetul tău"

---

### 12.4 — Admin Trial

În `apps/plati/admin.py` adaugă:
- List display: email_client, nisa_client, status, data_start, data_expirare, zile_ramase, convertit_la_pachet
- List filter: status, convertit_la_pachet, nisa_client
- Search: email_client, nume_client
- Acțiune: "Marchează ca convertit la pachet lunar"
- Câmp `nota_interna` editabil — pentru notițe despre client

---

### 12.5 — Pagina de vânzare trial

URL: `/promo/` sau `/test-gratuit/`

Template `templates/plati/promo_trial.html`:

Secțiunea Hero:
- Titlu: "Testează-ne 7 zile. Riști doar 50€."
- Subtitlu: "Setup complet, primele reclame live, primele rezultate — sau îți explicăm exact ce trebuie schimbat."

Secțiunea Ce primești în 7 zile:
- ✅ Audit complet al prezenței digitale actuale
- ✅ Setup campanie Meta Ads (structură + audiențe + creatives)
- ✅ 3 variante de copy testate
- ✅ Raport zilei 7 cu rezultate și recomandări
- ✅ Recomandare pachet lunar personalizată

Secțiunea Transparență buget reclame:
- Titlu: "Cum funcționează bugetul de reclame?"
- Text: "Cei 50€ reprezintă exclusiv onorariul Green Pheonix Concept pentru setup și management. Bugetul de reclame este al tău, merge direct în contul tău Meta/Google, și îl controlezi tu în totalitate. Recomandat: minimum 200-300 lei/săptămână pentru rezultate vizibile."

Formular înainte de plată (colectează date înainte de Stripe):
- Nume și prenume
- Email
- Telefon (WhatsApp)
- Nișa business-ului
- Platforma dorită: Meta Ads / Google Ads / Ambele
- Ce vrei să obții în 7 zile (textarea scurt)

Buton CTA: "Începe acum — 50€" → Stripe checkout plată unică

---

### 12.6 — Email automat după plată trial

Trimis automat via Django `send_mail` când webhook confirmă plata:

Subiect: "Bun venit la Green Pheonix Concept — Trialul tău de 7 zile a început!"

Conținut:
- Confirmare plată 50€
- Ce urmează în primele 24 ore (îl contactezi tu pe WhatsApp)
- Reamintire că bugetul de reclame e separat și al lui
- Link portal: `/portal/trial/`
- Numărul tău de WhatsApp pentru contact direct

---

### 12.7 — Navbar și linkuri

În `templates/includes/navbar.html`:
- Adaugă buton/link "Testează 7 zile — 50€" cu accent vizual (culoare diferită, poate auriu)
- Poziționat prominent — după "Pachete & Prețuri"

Pe pagina Pachete `templates/servicii/pachete.html`:
- Adaugă banner deasupra celor 3 carduri:
  *"Nu ești sigur? Testează-ne 7 zile pentru 50€ înainte să te abonezi."*
  Buton: "Vezi oferta de test" → `/promo/`

---

### 12.8 — Flux complet trial → conversie

```
Client găsește pagina /promo/
        ↓
Completează formularul (nume, email, nișă, obiectiv)
        ↓
Redirect Stripe — plată unică 50€
        ↓
Webhook confirmă plata → creare PromoTrial status=activ
        ↓
Email automat de confirmare trimis clientului
        ↓
TU primești notificare → contactezi clientul pe WhatsApp în max 24 ore
        ↓
Lucrezi 7 zile: audit + setup reclame + optimizare
        ↓
Ziua 7: trimiți raport + recomandare pachet lunar personalizată
        ↓
Client decide:
    DA → alege pachet lunar → checkout normal → PromoTrial.convertit=True
    NU → trial se închide → follow-up după 30 zile
```

---

### DATE DE ADĂUGAT — Pachet Promo în admin

După implementare adaugă și în modelul `Pachet` un pachet special:
- Nume: Promo Trial 7 Zile
- Tier: starter (sau creează choice nou: trial)
- Preț: 50€ one-time (nu recurent)
- Setup: 0€
- Recomandat: Nu
- Activ: Da
- Features: ["Audit prezență digitală", "Setup campanie Meta Ads", "3 variante copy testate", "Audiențe personalizate", "Raport complet ziua 7", "Recomandare pachet personalizată"]
- Notă importantă vizibilă: "Bugetul de reclame este separat și aparține clientului"

