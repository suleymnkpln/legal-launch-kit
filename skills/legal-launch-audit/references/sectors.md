# Sector triggers: what the product *does* changes what it needs

Last verified: 2026-11-17. Use this after you understand the product's purpose (SKILL.md step 2). Each sector adds obligations **on top of** the matrix. Many sectors need a licence or a professional. Say so clearly instead of guessing.

| Purpose / feature | Extra things to check | Refer to a professional? |
|---|---|---|
| **Health, fitness, wellness, period/pregnancy tracking, mental health, diet** | Special-category data (KVKK Art. 6, GDPR Art. 9): explicit consent or a narrow legal basis, stronger security, DPIA (EU), no ad-tech sharing of health signals. Apple HealthKit and Google Health Connect data may not be used for ads. US: Washington My Health My Data Act and similar state health-data laws; FTC Health Breach Notification Rule. If the app diagnoses or treats: medical-device rules (EU MDR, TR TİTCK). | Yes, if medical claims or diagnosis |
| **Finance: payments, wallets, lending, investing, crypto, insurance** | Payment/e-money licensing (TR Law 6493, EU PSD2/EMD), crypto-asset rules (TR SPK/CMB licensing, EU MiCA), KYC/AML (MASAK, AMLD), consumer credit disclosure. Apple 5.1.1(ix) regulated industries; Google Play financial services declaration. | Yes, always |
| **Children / education (under 13–18)** | COPPA (US), GDPR Art. 8 age of digital consent (13–16 by country), KVKK guardian consent, Apple Kids / Google Families, no behavioural ads, TR under-15 social network rules (turkiye.md §11) if social features, UK Age Appropriate Design Code. | Recommended |
| **Social, community, chat, dating, UGC** | TR under-15 ban + e-Devlet age verification + parental controls (turkiye.md §11); report/block/moderation (Apple 1.2, Google UGC policy, DSA Art. 16, Law 5651); UK Online Safety Act. Dating: sexual-orientation data is special-category; 18+ age gating; safety features. | Recommended |
| **Marketplace / multi-vendor / classifieds** | Intermediary service provider rules (TR 6563 *aracı hizmet sağlayıcı* regulation), seller identity collection (DSA Art. 30), ranking transparency (EU P2B Regulation), consumer info that the seller is a trader or private person. | Recommended |
| **Delivery, ride-hailing, booking, travel** | Precise location data (minimise, explain), sector licences (TR: travel agencies need a TÜRSAB licence, transport permits), cancellation/refund rules for services with a fixed date (withdrawal exceptions). | Yes, for licences |
| **Location tracking / family locator / fleet** | Continuous location is high-risk: clear purpose, consent where required, background-location declaration (Google Play), retention limits, no secret tracking of other people. | Recommended |
| **Gambling, betting, loot boxes, sweepstakes, lotteries** | Real-money gambling is prohibited or state-licensed in TR (Spor Toto / Milli Piyango system) and licensed per country elsewhere. Apple and Google restrict it. Loot boxes must disclose odds (Apple 3.1.1). Promotional draws in TR need permission (Milli Piyango İdaresi). | Yes, always |
| **AI companion, AI chat, AI image/voice generation** | AI disclosure (EU AI Act Art. 50); deepfake labelling; minors' safety; content moderation; training on user data needs a basis and notice; TR advertising AI disclosure. App store rules on AI-generated content and age ratings. | Recommended |
| **IoT / connected devices / Bluetooth hardware** | EU Cyber Resilience Act (product requirements; reporting since 11 Sept 2026); EU Data Act (data access for connected-product users, applicable since 12 Sept 2025); radio equipment cybersecurity rules. | Yes |
| **Alcohol, tobacco, pharmacy, supplements, weapons** | Online sale bans/restrictions (TR prohibits online sale of alcohol and tobacco to consumers; pharmacy sales are limited), advertising restrictions, age gates. | Yes, always |
| **Employment / HR / recruiting** | Candidate data notice, automated hiring decisions (EU AI Act high-risk; NYC Local Law 144), retention of CVs. | Recommended |
| **Real estate, legal, medical professionals' sites** | Professional advertising rules (e.g. TR bar and medical association advertising bans), chamber info in the imprint. | Yes |

## How to use it in the report

1. In the profile, state the product's purpose in one sentence and the sector(s) it falls into.
2. For each matching row, add findings with the specific feature that triggers them, e.g. "your step-counter syncs with HealthKit (`ios/Runner/Health.swift:12`) → health data is special-category".
3. If the sector needs a licence, put it under "Needs a human decision" with the authority name. Do not claim that the licence is or is not needed without facts.
