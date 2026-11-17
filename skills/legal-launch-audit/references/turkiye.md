# Türkiye reference

Last verified: 2026-11-17. Sources are official texts where possible (mevzuat.gov.tr, kvkk.gov.tr, ticaret.gov.tr, Resmî Gazete). Amounts of administrative fines are updated every year by revaluation; do not quote fine amounts in reports, link the source instead.

## §1 Personal data: KVKK (Law No. 6698)

Source: <https://www.mevzuat.gov.tr/mevzuatmetin/1.5.6698.pdf>, <https://www.kvkk.gov.tr>

**Applies when:** any personal data of identifiable people is processed. That includes contact forms, accounts, order data, analytics identifiers, IP addresses in logs and mobile advertising IDs.

**Privacy notice (aydınlatma metni, Art. 10)** must state at least:
- identity of the data controller (and representative, if any),
- purposes of processing,
- to whom and for what purpose data may be transferred,
- method of collection and legal basis,
- the data subject's rights under Art. 11.

The notice must be given **at the time of collection** (link next to the form or on the first screen of the app), in clear language, and must match the real processing. The Communiqué on the Procedures and Principles of the Disclosure Obligation adds format rules.

**Data subject requests (Art. 11 and 13):** the controller must answer within 30 days, free of charge as a rule. The notice should explain how to apply (e.g. email, KEP, written application).

**Security (Art. 12):** technical and administrative measures. Minimum signals in code: HTTPS, hashed passwords, no secrets in the client, access control, log retention policy.

**Data minimisation (Art. 4):** processing must be "linked, limited and proportionate". Typical audit findings: TCKN collected for newsletters, birth date collected without need, location permission requested by apps that do not use it.

**Special-category data (Art. 6):** health, biometrics, religion, etc. This raises the bar (explicit consent or narrow legal grounds plus extra security measures). Flag it as P0 if found.

## §2 Explicit consent (açık rıza) vs. notice

Consent is **one** of the legal bases (Art. 5/1). Others include performance of a contract, a legal obligation and legitimate interest (Art. 5/2).

Audit rules:
- The notice (aydınlatma) is always required. Consent is required only when no other legal basis applies.
- Asking for consent for processing that already has another basis is misleading. The Board treats it as abuse of the consent mechanism. Typical example: a mandatory "açık rıza" checkbox to submit a contact form.
- Consent must be specific, informed, freely given and separate. It cannot be bundled with the notice or the terms, cannot be pre-ticked, and cannot be a condition of the main service.
- Typical cases that **do** need consent: commercial electronic messages (also İYS, §9), non-essential cookies/SDKs (§3), most special-category data, and some foreign transfers when no other Art. 9 mechanism exists (§4).

## §3 Cookies and SDK trackers

Source: KVKK *Çerez Uygulamaları Hakkında Rehber* (Cookie Guidelines; first published 2022, updated 2025): <https://kvkk.gov.tr/Icerik/7353/Cerez-Uygulamalari-Hakkinda-Rehber>

- Strictly necessary cookies (session, security, load balancing, remembering the consent choice) need no consent but must be explained.
- Analytics, advertising, personalisation and session-replay cookies/pixels need **explicit consent before they are set**.
- "Accept all" and "Reject all" should be equally prominent. Continuing to browse is not consent. No pre-ticked boxes. Making access to the whole site depend on consent (a cookie wall) is problematic.
- Practical code check: analytics/ad tags (gtag, fbq, TikTok pixel, Yandex Metrica, Hotjar/Clarity) must not load unconditionally in `<head>`. They must be gated by the consent manager.
- Mobile apps: SDK identifiers work like cookies. Apply the same logic to Firebase Analytics, ad SDKs, etc. (consent first where required).

## §4 Transfers abroad (KVKK Art. 9, as amended by Law No. 7499, in force 1 June 2024)

Sources: KVKK announcements on standard contracts (<https://www.kvkk.gov.tr/Icerik/7938/Standart-Sozlesmeler-ve-Baglayici-Sirket-Kurallarina-Iliskin-Dokumanlar-Hakkinda-Kamuoyu-Duyurusu>), Regulation on the Procedures and Principles for Transfer of Personal Data Abroad (2024).

Layered regime:
1. **adequacy decision** for the country/sector (check the current list on kvkk.gov.tr),
2. otherwise **appropriate safeguards**: Board-approved **standard contract** (four templates), binding corporate rules, or an undertaking approved by the Board,
3. otherwise narrow **incidental (non-recurring) exceptions**, which include explicit consent for an incidental transfer.

Key rules:
- A signed standard contract must be **notified to the KVKK within 5 business days** of the last signature (KEP or the Standard Contract Notification Module). Failing to notify is an administrative offence.
- The transitional period that allowed transfers based on explicit consent alone ended on 1 September 2024.
- **Audit trigger:** any foreign cloud/SaaS that receives personal data. Typical examples: Firebase / Google Cloud, AWS, Azure, Vercel, Netlify, Supabase, Cloudflare, Google Analytics, Meta Pixel, Mailchimp, SendGrid, Sentry, OpenAI and other AI APIs, Stripe and RevenueCat. The privacy notice must mention the transfer, and the safeguard must exist. The code alone cannot prove a contract exists, so report it as ❓ "verify contract + notification".

## §5 VERBİS (Data Controllers' Registry)

Source: <https://verbis.kvkk.gov.tr>; Board decisions 2018/87, 2023/1154 (balance-sheet threshold raised to TRY 100 million), 2025/1572 (published in the Official Gazette on 1 Oct 2025) and 2025/2393 (25 Dec 2025).

- **Exempt (general rule):** controllers with fewer than 50 employees per year **and** an annual balance-sheet total below TRY 100 million, whose main activity is **not** processing special-category data.
- **Main activity is special-category data** (e.g. clinics, psychologists, dietitians): exempt only if fewer than 10 employees and an annual balance-sheet total below TRY 10 million (since 1 Oct 2025).
- Controllers **not keeping balance-sheet-basis books**: only the employee criterion is applied (decision 2025/2393).
- Controllers **resident abroad** that process data of people in Türkiye are not covered by the size exemption.
- Some professions (lawyers, notaries, accountants, etc.) have specific exemptions.

Audit output: this cannot be decided from code. Ask the user or mark ❓ with the criteria above.

## §6 E-commerce: Law No. 6563, ETBİS, imprint

Sources: <https://www.mevzuat.gov.tr/mevzuatmetin/1.5.6563.pdf>; Regulation on Service Providers and Intermediary Service Providers in Electronic Commerce; ETBİS: <https://ticaret.gov.tr/ic-ticaret/elektronik-ticaret/elektronik-ticaret-bilgi-sistemi-etbis>

**Imprint / identity (künye):** a service provider selling online must make easily accessible, before the contract, at least:
- name / trade name,
- MERSİS number (or tax ID if not registered),
- address, email and phone,
- KEP address where applicable,
- for regulated professions: professional chamber and rules.

Usually this lives on an "İletişim / Künye" page and in the footer.

**ETBİS:** service providers and intermediary service providers that enable contracts or orders for goods/services **through their own** electronic commerce environment (site or app) must register on ETBİS via e-Devlet **before starting**. They must keep the record updated and make the annual notifications.
- Selling **only** through a Turkish marketplace (aracı hizmet sağlayıcı): generally no own ETBİS record is needed. Selling through a foreign marketplace while resident in Türkiye: registration is needed.
- Brochure sites with no ordering: not needed. Showing an ETBİS badge there is clutter.

**Order process (6563 Art. 4–5):** before the order, show the technical steps to place the order, how to correct input errors, contract storage, and the languages. After the order, send a confirmation without delay.

## §7 Distance sales (Law No. 6502 + Distance Contracts Regulation)

Sources: <https://www.mevzuat.gov.tr/mevzuatmetin/1.5.6502.pdf>; Mesafeli Sözleşmeler Yönetmeliği (2014, amended; amendment published in the Official Gazette of 24 May 2025 No. 32909, in force since **1 January 2026**).

**Applies when:** B2C sales of goods/services concluded at a distance (site, app, phone). Not B2B.

**Pre-contract information form (ön bilgilendirme formu)** must be confirmed by the consumer before the order. Main contents:
- essential characteristics of the goods/service,
- seller identity and contact details,
- total price including taxes and delivery costs,
- payment, delivery and performance terms,
- withdrawal right: conditions, period (14 days), procedure, and the address to send the notice to, or the statement that there is no withdrawal right and why,
- complaint channels (consumer arbitration committee / consumer court),
- **since 2026: information on mandatory mediation before going to court within the monetary limits**,
- for digital content: functionality and interoperability.

**Distance sales contract (mesafeli satış sözleşmesi):** must be confirmed and then delivered to the consumer on a durable medium (e.g. email/PDF).

**Withdrawal right (cayma hakkı):** 14 days without giving reasons.
- For goods, the period starts at delivery.
- If the consumer is not properly informed, the period extends (up to one year).
- Since 1 Jan 2026 the cost of returning goods after withdrawal cannot be charged to the consumer.
- The draft exception for phones/tablets/computers was withdrawn, so those keep the withdrawal right.
- Exceptions (Regulation Art. 15) include goods made to the consumer's specifications, perishable goods, unsealed hygiene products, and digital content or services **performed instantly** in electronic form. The exception must be stated in the pre-contract form, and the consumer's acknowledgement must be obtained where required.

**Subscriptions:** fixed-term or indefinite subscriptions are also governed by the Subscription Contracts Regulation (abonelik sözleşmeleri). Cancellation must be possible through the same channel used to subscribe.

**Mobile in-app purchases via Apple/Google billing:** whether the developer or the store is the seller, and how these obligations split between them, depends on the store's agency/reseller model. Mark ❓ and recommend legal review rather than guessing.

## §8 Advertising, pricing, reviews, AI (Commercial Advertising and Unfair Commercial Practices Regulation)

Source: amendment published in the Official Gazette of **1 July 2026 (No. 33297)**, in force **1 August 2026**; Ministry of Trade *Tüketici Değerlendirmeleri Hakkında Kılavuz*.

- **Consumer reviews:**
  - only buyers of the product/service may review it, and reviews from channels that cannot verify a purchase cannot be published,
  - reviews must be published regardless of being positive or negative, kept for at least one year and ordered by objective criteria (date, rating, seller),
  - fake reviews and paid endorsements are banned,
  - the seller's pre-publication response window is now 48 hours.
- **Discount reference price:**
  - goods: the lowest price applied in the **10 days** before the discount,
  - perishable goods and services: the price immediately before the discount,
  - set per sales channel.
- **Influencer content:** paid, gifted or discounted collaborations must carry "Reklam" or "Tanıtım" plus the brand. The label must be visible at first glance without scrolling, and audio-only content must say it at the start.
- **AI:** ads must clearly disclose AI use or AI-generated characters that could noticeably influence consumers. Ads may not use an AI-made digital copy of a real person that falsely suggests they used or recommended the product.
- **Environmental claims:** must be specific and substantiated by authorised or accredited bodies, with the methodology available.
- **Price transparency ("no hidden fees"):** the price shown must include taxes. Mandatory extra costs must be shown before the order. Drip pricing is an unfair practice.
- **Unproven claims:** "number 1", "the best", "clinically proven", etc. need evidence.

## §9 Commercial electronic messages: İYS

Sources: 6563 Art. 6–8; Regulation on Commercial Communication and Commercial Electronic Messages; <https://iys.org.tr>

- Sending commercial SMS, email or calls to consumers requires **prior consent**. A sender must **register on İYS** and keep the consent and rejection records there.
- Recipients who are merchants/tradespeople (tacir/esnaf) do not need prior consent, but their addresses must still be registered on İYS, and rejections must be honoured.
- Every message must offer an easy, free opt-out. Opt-outs must be processed within 3 business days.
- Purely informational messages about an existing transaction (order confirmation, shipping, password reset) do not need consent, provided they contain no promotion.
- Marketing consent must not be made a condition of the product or service. It must be a separate, unticked checkbox.
- **Audit triggers in code:** SMS providers (Netgsm, İleti Merkezi, Twilio…), newsletter/email-marketing SDKs (Mailchimp, Brevo, Klaviyo, SendGrid marketing), and "kampanyalardan haberdar olmak istiyorum" checkboxes.

## §10 User-generated content (Law No. 5651)

Source: <https://www.mevzuat.gov.tr/mevzuatmetin/1.5.5651.pdf>

- Platforms hosting user content act as hosting providers (yer sağlayıcı). They need:
  - a working process to receive and act on content notices and court/authority decisions,
  - traffic data retention as required by the law and its regulation.
- Large social network providers (above the user thresholds) have additional obligations: a local representative and reporting. This rarely applies to new projects.
- **Any** service where users create, view or share content for social interaction is a *sosyal ağ sağlayıcı* for the under-15 rules in §11. **That definition has no user threshold.**
- Audit output: check that a report/complaint mechanism and contact exist. Mark retention as ❓ unless the logs config is visible.

## §11 Children and social networks: under-15 ban and age verification (Law No. 7578)

Sources:
- Law No. 7578 amending Law 5651 Additional Art. 4 (Official Gazette 1 May 2026, No. 33240),
- *Sosyal Ağ Sağlayıcı Tarafından Çocuklara Özgü Ayrıştırılmış Hizmet Sunulmasına ve Yaş Doğrulamaya İlişkin Yönetmelik*, issued by the Cyber Security Presidency (Official Gazette 10 Oct 2026, No. 33396).

**Applies to:** domestic and foreign social network providers accessible from Türkiye. A social network provider means anyone enabling users to create, view or share text, image, audio or location content for social interaction. **There is no user-count threshold.** A small app with profiles, posts, comments or chat between users may fall in scope. Mark ❓ when unsure, never ➖ without a reason.

**Obligations (in force 1 November 2026):**
- **Under 15:** no service, and account applications must be refused.
- **Age verification:** a token generated via **e-Devlet** that only says over/under 15 and over/under 18. The platform must validate that the token comes from the Presidency.
- **Existing accounts** must be verified at least once by **31 March 2027**. Accounts found to be under 15 are closed after notice.
- **Ages 15–17 must get a separated ("ayrıştırılmış") service:**
  - private account by default (no public option),
  - messages only from followed accounts, without read receipts,
  - no live streaming, no infinite auto-scroll or other addictive features,
  - restricted contact sync and friend suggestions,
  - **no profiling or personalised ads**,
  - technical measures against screenshots of children's content.
- **Parental controls in Turkish:** account settings, approval of paid transactions, spending and time limits, location sharing. The child is notified when controls are enabled.
- **Complaints:** a free, accessible, Turkish-language appeal channel. Appeals are not decided solely by automated systems.
- **Online game platforms:** Law 7578 also contains provisions on game platforms. Their secondary rules were not covered in the source checked. Mark ❓ for games with chat, user content or in-game purchases, and check the current regulation.

**Audit signals:** user profiles, follow/friend features, posts/comments/chat, live streaming, location sharing, a feed. If found and the market includes Türkiye, this is P0 until the scope question is answered.

## §12 Accessibility in Türkiye

As of the last verification no general private-sector web/app accessibility mandate was identified that is comparable to the EU Accessibility Act. Public-sector rules exist. Report accessibility as **O (recommended, WCAG 2.1 AA)** for Turkish-only private projects, and as **C** if the project also targets EU consumers (see eu.md §4).

## Out of scope: refer to a professional

- tax registration and invoicing (e-Arşiv/e-Fatura),
- company formation and sole-proprietorship status,
- trademark search,
- sector licences (health, finance, gambling, alcohol, pharmacy, tourism agencies),
- payment-institution licensing,
- employment law.
