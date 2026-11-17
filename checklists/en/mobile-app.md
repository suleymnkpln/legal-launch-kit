# Checklist: mobile app (App Store + Google Play)

Last verified: 2026-11-17. Source: [app-stores.md](../../skills/legal-launch-audit/references/app-stores.md).

## Every app
- [ ] **Privacy policy URL** in the store listing **and** inside the app.
- [ ] **Apple App Privacy label** and **Google Play Data safety form**, matching real behaviour including SDKs.
- [ ] **iOS privacy manifest** (`PrivacyInfo.xcprivacy`) for the app and SDKs.
- [ ] **Permissions:** only those used. iOS purpose strings that explain the real purpose. Android sensitive-permission declarations.
- [ ] **Apple age rating questionnaire** (4+/9+/13+/16+/18+).

## Conditional
- [ ] **Accounts:** in-app account deletion (Apple 5.1.1(v)) **and** a web deletion link for Google Play.
- [ ] **Ads:** a Google-certified CMP (UMP) for the EEA/UK/CH. On iOS, App Tracking Transparency before tracking.
- [ ] **IAP / subscriptions:** price, period, renewal and cancel info before purchase; restore purchases; Terms + Privacy links on the paywall.
- [ ] **Monetised and available in the EU:** declare **trader status** (address, phone and email become public in the EU).
- [ ] **User-generated content:** report, block, filter, contact info.
- [ ] **Kids:** Apple Kids / Google Families rules; COPPA.
- [ ] **Firebase or other foreign backend:** disclose it and put transfer safeguards in place (GDPR / KVKK Art. 9).
- [ ] **AI chat/image features:** disclose AI.

## Avoid 🗑️
- Unused permissions (location, contacts, microphone) added "just in case".
- Forcing sign-up for features that do not need an account.
- A privacy policy listing SDKs you don't use, or missing ones you do.
