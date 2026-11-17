# Sample audit report

> Fictional project: the test fixture in [`tests/fixtures/sample-app`](../tests/fixtures/sample-app). This shows the output format of the `legal-launch-audit` skill. The skill writes in the user's language; this sample is in English.

---

# Legal launch audit: sample-app

Date: 2026-11-17 · Scope: web (Next.js), Flutter (Android) · Markets: TR, EU
Mode: read-only (no files changed)

## 1. What the product does

*FitStore* is an online shop (web) selling fitness supplements to consumers in Türkiye and the EU. It has a companion Flutter app with accounts where users track workouts and **follow friends**. Revenue comes from product sales (Stripe) and in-app ads (AdMob). The personal data it needs: account email, orders and addresses, workout data and social connections. Sectors: **restricted goods (supplements)**, **health/fitness** (workout data), **social** (follow feature). *Inferred from README and code; please confirm.*

## 1b. Project profile

| Question | Answer | Evidence |
|---|---|---|
| Sells to consumers? | Yes, Stripe checkout on web | `package.json:8` |
| Accounts? | Yes, Firebase Auth sign-up in the app | `lib/main.dart:4` |
| Ads / analytics | Google Analytics (web), AdMob (app) | `web/index.html:6`, `pubspec.yaml:6` |
| Data stored abroad | Firebase (Google Cloud), Stripe | `package.json:7-8` |
| Commercial messages | Newsletter opt-in on the contact form | `web/index.html:18` |
| Children / sensitive data | No signals | — |
| Assumptions | B2C; sole trader in Türkiye; under 50 employees | user to confirm |

Project types: **C** (e-commerce) + **F** (mobile app with accounts and ads).

## 2. Findings

| # | Status | Priority | Item | Evidence | Why it matters | Fix | Source |
|---|---|---|---|---|---|---|---|
| 1 | ❌ | P0 | In-app account deletion | Sign-up at `lib/main.dart:4`; no `delete` path found in `lib/` | Apple 5.1.1(v); Google Play User Data policy | Settings → Delete account calling `currentUser.delete()` + backend cleanup | [Apple](https://developer.apple.com/help/app-review/guideline-reference/5-1-1-account-deletion), [Google](https://support.google.com/googleplay/android-developer/answer/13327111) |
| 2 | ❌ | P0 | Consent before analytics | GA loads unconditionally in `<head>`: `web/index.html:6-11`; no consent manager | KVKK Cookie Guidelines; ePrivacy Art. 5(3) | Add a CMP; load gtag only after consent (or use Consent Mode with default *denied*) | turkiye.md §3, eu.md §2 |
| 3 | ⚠️ | P1 | Pre-ticked marketing checkbox | `web/index.html:18` (`checked`) | Consent must be an active choice; İYS rules | Remove `checked`; keep the box separate and optional | turkiye.md §9 |
| 4 | ❌ | P1 | Certified CMP for AdMob | `pubspec.yaml:6`; no UMP calls | Google EU User Consent Policy (EEA/UK/CH) | Integrate the Google UMP SDK and request consent before loading ads | [AdMob](https://support.google.com/admob/answer/13554116) |
| 5 | ❓ | P1 | Transfers abroad (Firebase, Stripe) | `package.json:7-8` | KVKK Art. 9: standard contract + notification in 5 business days | Confirm contracts and notifications; list the recipients and countries in the notice | turkiye.md §4 |
| 6 | ❌ | P1 | Pre-contract form + distance-sales contract | No page or route found matching `on-bilgilendirme`/`mesafeli` | Distance Contracts Regulation | Add both to the checkout (confirm before ordering, send by email) | turkiye.md §7 |
| 7 | ❌ | P1 | Withdrawal / returns policy and EU withdrawal button | No `iade`/`cayma`/`refund` page | 14-day right; EU CRD Art. 11a since 19 June 2026 | Publish the policy; add a two-step withdrawal function for EU buyers | eu.md §3 |
| 8 | ⚠️ | P1 | Cleartext traffic allowed | `android/app/src/main/AndroidManifest.xml:5` | Security obligation (KVKK Art. 12 / GDPR Art. 32) | Remove `usesCleartextTraffic="true"` | — |
| 9 | ⚠️ | P2 | National ID field on the contact form | `web/index.html:17` | Data minimisation (KVKK Art. 4) | Remove the TCKN field | turkiye.md §1 |
| 10 | ⚠️ | P2 | Sensitive permissions | `READ_CONTACTS`, `ACCESS_FINE_LOCATION` in the manifest; no usage found in `lib/` | Store policy + minimisation | Remove unused permissions | app-stores.md §3 |
| 11 | ⚠️ | P2 | Privacy page incomplete | `/gizlilik-politikasi` linked at `web/index.html:22`; no KVKK notice items, no SDK list | KVKK Art. 10 | Rewrite using `templates/tr/kvkk-aydinlatma-metni.md` | turkiye.md §1 |
| 12 | ❌ | P2 | Imprint / contact | None found | 6563 + service-provider regulation | Add an "İletişim / Künye" page with MERSİS, address, KEP | turkiye.md §6 |
| 13 | ❓ | P0 | TR under-15 rules for the follow feature | `lib/main.dart` `followUser` | Users follow each other, so the app may count as a *sosyal ağ sağlayıcı*. Since 1 Nov 2026: no under-15 users, e-Devlet age token, protected mode for 15–17 | Decide whether the social feature stays; if yes, plan age verification + parental controls, or remove the feature for TR | turkiye.md §11 |
| 14 | ❓ | P2 | Supplement advertising and health claims | `README.md:3` | Supplements are under the advertising regulation (TR 2026 amendment adds supplements to food-claim rules); "boosts fat burning"-type claims need evidence | Review product texts for health claims | turkiye.md §8, sectors.md |

## 3. Not needed / remove

- 🗑️ EU ODR link at `web/index.html:23`: the platform closed on 20 July 2025.
- ➖ CCPA rights page: no US market selected.
- ➖ EU Accessibility Act: exempt if a microenterprise (<10 staff, ≤ €2M). Confirm, otherwise it becomes C.

## 4. Needs a human decision

1. Is a KVKK standard contract signed with Google (Firebase) and Stripe, and was it notified within 5 business days?
2. Is the ETBİS registration done before sales start?
3. Will the newsletter actually be sent? If yes, is İYS registration done?
4. Employee count and balance sheet total, for VERBİS?

## 5. Prioritised action plan

| Priority | Action | Owner |
|---|---|---|
| P0 | Add account deletion (in-app + web page for Google Play) | dev |
| P0 | Add a CMP; gate GA behind consent | dev |
| P1 | Integrate UMP before AdMob loads | dev |
| P1 | Pre-contract form, distance-sales contract, withdrawal policy, EU withdrawal button | dev + legal |
| P1 | Unticked, separate marketing checkbox; İYS registration | dev + business |
| P1 | Transfer safeguards for Firebase/Stripe | legal |
| P1 | Disable cleartext traffic | dev |
| P2 | Remove TCKN field, unused permissions, ODR link; add imprint; rewrite privacy notice | dev + legal |

## 6. Limits

Not legal advice. Laws checked as of 2026-11-17. Out of scope: tax and e-invoice obligations, company status, sector licences.
