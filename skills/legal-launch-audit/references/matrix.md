# Requirement matrix: project type × legal item

Last verified: 2026-11-17. Laws change; every row links to the detailed reference file where the source is cited.

## How to read this

**Project types**

| Code | Project type |
|---|---|
| **A** | Brochure / corporate site: no accounts, no sales (a contact form at most) |
| **B** | Lead-generation site: forms, newsletter, quote requests, booking requests |
| **C** | E-commerce: own web shop or app selling goods/services to consumers |
| **D** | SaaS / subscription web product (paid plans, auto-renewal) |
| **E** | Mobile app: no account, no purchases, no ads |
| **F** | Mobile app with any of: accounts, in-app purchases, subscriptions, ads |
| **G** | Platform with user-generated content or third-party sellers (marketplace, community, reviews) |

A real project often combines types (e.g. **C + F**). Apply the union of the rows.

**Status codes**

| Code | Meaning |
|---|---|
| **R** | Required for this type in the selected market |
| **C** | Conditional: required only if the trigger in the "Trigger" column is true |
| **O** | Optional / recommended good practice; not a legal obligation by itself |
| **–** | Not needed for this type. Adding it is clutter, not compliance |
| **X** | Avoid: outdated, misleading or itself a compliance risk |

Markets: **TR** = Türkiye, **EU** = EU/EEA (most rows also fit UK), **US** = United States, **Store** = Apple App Store / Google Play policy.

## 1. Privacy and data protection

| # | Item | A | B | C | D | E | F | G | Markets | Trigger / note | Details |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1.1 | Privacy notice (TR: *KVKK aydınlatma metni*; EU: GDPR Art. 13/14 notice; US: privacy policy) | R* | R | R | R | C | R | R | TR EU US Store | *A: required as soon as any personal data is processed (contact form, analytics, server logs with IP). E: required by both stores if the app or any SDK collects data; Google Play requires a privacy policy link for every app. | turkiye.md §1, eu.md §1, us.md §1, app-stores.md §1 |
| 1.2 | Explicit consent text (TR: *açık rıza metni*) | – | C | C | C | C | C | C | TR EU | Only for processing whose legal basis is consent: marketing messages, non-essential cookies/SDKs, special-category data, some foreign transfers. Never bundle it with the privacy notice or make it a condition of the service. | turkiye.md §2 |
| 1.3 | Data-subject request channel (access, deletion, correction) | R | R | R | R | C | R | R | TR EU US | Wherever personal data is processed. Must be a real, working channel (email/form), named in the notice. | turkiye.md §1, eu.md §1 |
| 1.4 | Cookie / SDK consent banner or prompt | C | C | C | C | C | C | C | TR EU UK | Only if non-essential cookies, pixels or SDKs (analytics, ads, session replay) run. Reject must be as easy as accept; nothing non-essential may fire before consent. | turkiye.md §3, eu.md §2 |
| 1.5 | Cookie policy | C | C | C | C | – | C | C | TR EU | Same trigger as 1.4. May be a section of the privacy notice. | turkiye.md §3 |
| 1.6 | Cross-border transfer safeguards (TR: KVKK Art. 9 standard contract + notification within 5 business days) | C | C | C | C | C | C | C | TR EU | Data stored or processed abroad (Firebase, AWS, Vercel, Google Analytics, Supabase, OpenAI…). Very common, very often missed. | turkiye.md §4, eu.md §1 |
| 1.7 | VERBİS registration | C | C | C | C | C | C | C | TR | Thresholds apply (employees, balance sheet, special-category data, controller abroad). Most small Turkish businesses are exempt. | turkiye.md §5 |
| 1.8 | EU representative (GDPR Art. 27) | C | C | C | C | C | C | C | EU | Controller outside the EU that targets or monitors people in the EU. | eu.md §1 |
| 1.9 | US state rights page / "Do Not Sell or Share" link, honour GPC | C | C | C | C | C | C | C | US | Only above state thresholds (e.g. CCPA revenue / volume thresholds) or when selling/sharing data for targeted ads. | us.md §1 |
| 1.10 | Children's data rules (COPPA, age gating) | C | C | C | C | C | C | C | US Store EU | Child-directed or mixed-audience service, or actual knowledge of under-13 users. | us.md §2, app-stores.md §5 |

## 2. Consumer and commerce

| # | Item | A | B | C | D | E | F | G | Markets | Trigger / note | Details |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.1 | Business identity / imprint (name, address, registry no., email, phone) | R* | R | R | R | – | C | R | TR EU | *Any commercial site. TR: 6563 + service-provider regulation (MERSİS, KEP…). EU: e-Commerce Directive Art. 5. F: shown via store listing when trader (see 4.6). | turkiye.md §6, eu.md §3 |
| 2.2 | Terms of use / terms of service | O | O | R | R | O | R | R | All | Needed wherever there is an account, a contract, paid service or user content. Not a statutory "page" for a pure brochure site. | — |
| 2.3 | Pre-contract information form (TR: *ön bilgilendirme formu*) | – | – | R | C | – | C | C | TR EU | B2C distance sales. D/F: when you sell directly (not via App Store/Play billing). G: each seller's obligation, platform must enable it. | turkiye.md §7, eu.md §3 |
| 2.4 | Distance sales contract (TR: *mesafeli satış sözleşmesi*) | – | – | R | C | – | C | C | TR | Same trigger as 2.3. | turkiye.md §7 |
| 2.5 | Withdrawal / returns policy (TR: *cayma hakkı*, 14 days) | – | – | R | C | – | C | C | TR EU | B2C distance sales. Know the exceptions (instantly delivered digital content, personalised goods…). | turkiye.md §7, eu.md §3 |
| 2.6 | EU online "withdrawal function" (button) | – | – | C | C | – | C | C | EU | B2C contracts concluded online with a statutory withdrawal right, applicable since 19 June 2026. | eu.md §3 |
| 2.7 | Subscription terms + easy cancellation | – | – | C | C | – | C | – | TR EU US Store | Auto-renewing plans. Show price, period, renewal and cancellation path before payment. | us.md §3, app-stores.md §4 |
| 2.8 | Total price shown incl. taxes and fees ("no hidden fees") | – | – | R | R | – | C | C | TR EU US | Any priced offer. | turkiye.md §8, eu.md §3 |
| 2.9 | Discount reference price rules | – | – | C | C | – | C | C | TR EU | Any "was / now" or "% off" claim. TR goods: lowest price of the previous 10 days (since 1 Aug 2026); EU: lowest price of the previous 30 days. | turkiye.md §8, eu.md §3 |
| 2.10 | Review / rating rules ("no fake reviews") | – | – | C | C | – | C | C | TR EU | You show customer reviews. TR (since 1 Aug 2026): only verified buyers, publish positive and negative alike for at least a year, objective ordering. | turkiye.md §8 |
| 2.11 | Substantiated claims ("no unproven claims"), influencer ad labels, green claims | O | C | C | C | C | C | C | TR EU US | Marketing claims, influencer posts, environmental claims. | turkiye.md §8 |
| 2.12 | ETBİS registration | – | – | C | C | – | C | C | TR | Selling online through **your own** site/app (or as a marketplace). Not needed if you sell only through a Turkish marketplace. | turkiye.md §6 |
| 2.13 | İYS registration + marketing consent | – | C | C | C | – | C | C | TR | You send commercial SMS / email / calls to consumers. | turkiye.md §9 |
| 2.14 | Link to the EU ODR platform | X | X | X | X | X | X | X | EU | Platform closed on 20 July 2025; obligation repealed. Remove old links. | eu.md §3 |

## 3. Technical and security

| # | Item | A | B | C | D | E | F | G | Markets | Trigger / note | Details |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3.1 | HTTPS everywhere + HTTP→HTTPS redirect | R | R | R | R | – | R | R | All | Security obligation under KVKK Art. 12 / GDPR Art. 32; also SEO. | turkiye.md §1 |
| 3.2 | Card data via a PCI-compliant provider (no raw card storage) | – | – | R | R | – | C | C | All | You take card payments. | — |
| 3.3 | Accessibility (WCAG 2.1 AA) + accessibility statement | O | O | C | C | O | C | C | EU | EU: consumer e-commerce and some other services since 28 June 2025; services by microenterprises (<10 staff, ≤ €2M turnover/balance) exempt. Elsewhere recommended. | eu.md §4 |
| 3.4 | Licensed images, fonts, music, icons | R | R | R | R | R | R | R | All | Any third-party asset. Keep license proof. | — |
| 3.5 | Third-party plugins / SDK inventory | O | R | R | R | R | R | R | All | Every SDK must be reflected in the privacy notice, consent and store labels. | — |
| 3.6 | Data minimisation (no unnecessary fields) | R | R | R | R | R | R | R | All | E.g. no national ID number (TCKN) or birth date for a newsletter. | turkiye.md §1 |
| 3.7 | Vulnerability / incident reporting process + public security contact (EU Cyber Resilience Act) | – | – | C | – | C | C | C | EU | Software products (mobile/desktop apps, distributed software) on the EU market: reporting of actively exploited vulnerabilities since 11 Sept 2026; full requirements from 11 Dec 2027. | eu.md §7 |

## 4. App store specific

| # | Item | A | B | C | D | E | F | G | Markets | Trigger / note | Details |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4.1 | In-app account deletion (+ web deletion link on Google Play) | – | – | C | C | – | C | C | Store | App lets users create an account. | app-stores.md §2 |
| 4.2 | Apple privacy "nutrition label" / Google Play Data safety form | – | – | C | C | R | R | C | Store | Every app on the stores; must match real SDK behaviour. | app-stores.md §1 |
| 4.3 | iOS privacy manifest (PrivacyInfo.xcprivacy) for app + SDKs | – | – | C | C | C | C | C | Store | iOS apps using required-reason APIs or listed SDKs. | app-stores.md §1 |
| 4.4 | Permission purpose strings + in-app disclosure before runtime prompt | – | – | C | C | C | C | C | Store | Camera, location, contacts, microphone, photos, tracking… | app-stores.md §3 |
| 4.5 | App Tracking Transparency prompt (iOS) | – | – | C | C | C | C | C | Store | Tracking across apps/sites (ad IDs, data brokers). | app-stores.md §3 |
| 4.6 | EU trader status (DSA) in App Store Connect / Play Console | – | – | C | C | C | C | C | Store EU | Monetised apps (paid, IAP, ads) are usually "traders"; address/phone/email become public. | app-stores.md §4 |
| 4.7 | Certified CMP (TCF) for ads in EEA/UK/Switzerland | – | – | C | C | – | C | C | Store EU | AdMob/AdSense/Ad Manager personalised ads to those regions (Google UMP SDK qualifies). | app-stores.md §4 |
| 4.8 | Age rating questionnaire (Apple 4+/9+/13+/16+/18+) | – | – | C | C | R | R | R | Store | Every iOS app. | app-stores.md §5 |
| 4.9 | Android developer verification + app registration | – | – | C | C | C | C | C | Store | Android apps on certified devices, from any store or sideloaded. In force in BR/ID/SG/TH since 30 Sept 2026; global from 2027. | app-stores.md §6 |

## 5. Platform / content / AI

| # | Item | A | B | C | D | E | F | G | Markets | Trigger / note | Details |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5.1 | Notice-and-takedown / report-content flow | – | – | – | C | – | C | R | TR EU Store | User-generated content. TR: Law 5651 hosting-provider rules; EU: DSA notice-and-action; Apple 1.2 requires report + block for UGC apps. | turkiye.md §10, eu.md §5, app-stores.md §5 |
| 5.2 | AI interaction / AI-generated content disclosure | C | C | C | C | C | C | C | EU TR | Chatbots, AI-generated images/text/voice shown to people (EU AI Act Art. 50 since 2 Aug 2026); AI in ads (TR since 1 Aug 2026). | eu.md §6, turkiye.md §8 |
| 5.3 | TR under-15 ban, e-Devlet age verification, protected mode for 15–17, parental controls | – | – | – | C | – | C | R | TR | Users can create, view or share content for social interaction (profiles, posts, comments, chat, live, location). No user threshold. In force 1 Nov 2026; existing accounts must be verified by 31 Mar 2027. | turkiye.md §11 |
| 5.4 | UK Online Safety Act duties | – | – | – | C | – | C | C | UK | User-to-user content with UK users. | eu.md §8 |
| 5.5 | Sector-specific rules (health, finance, kids, dating, gambling, location, IoT…) | C | C | C | C | C | C | C | All | Depends on what the product **does**. | sectors.md |

## 6. What is "too much"? (common clutter that adds risk, not compliance)

- A mandatory "I give explicit consent (açık rıza)" checkbox on a contact form whose data you only use to answer the message. That processing does not rely on consent. Forcing consent is a KVKK error.
- One combined "I accept the privacy notice and terms and consent to marketing" checkbox. The privacy notice is *read*, not accepted. Marketing consent must be separate and optional.
- Pre-ticked consent boxes, or "by continuing to browse you accept cookies".
- A cookie banner on a site that sets no non-essential cookies. It is not illegal, just noise. Prefer removing the trackers over adding a banner.
- Distance-sales contract, pre-contract form, ETBİS badge or return policy on a site that sells nothing.
- EU ODR platform link (repealed in 2025).
- Copy-pasted privacy policies listing tools you do not use, or missing the ones you do. Inaccuracy is itself a violation.
- Collecting TCKN, full birth date, gender or exact location "just in case".
- "VERBİS registered" or "GDPR certified" badges that are not true. There is no general "GDPR certificate".
