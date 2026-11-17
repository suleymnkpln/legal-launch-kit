# App Store (Apple) and Google Play reference

Last verified: 2026-11-17. Store policies change several times a year. Always link the live guideline in reports.

- Apple App Review Guidelines: <https://developer.apple.com/app-store/review/guidelines/>
- Google Play Developer Policy Center: <https://play.google/developer-content-policy/>

## §1 Privacy disclosures

**Both stores**
- A **privacy policy URL** is mandatory in the store listing, and must also be reachable **inside the app**. Apple 5.1.1(i): the policy must identify the data collected, how it is collected and used, the third parties it is shared with, retention/deletion and how to request deletion.
- The store data labels must reflect **all** collection, **including by third-party SDKs**:
  - Apple: App Privacy "nutrition label",
  - Google: **Data safety** form, which is required even when you collect nothing.

  Mismatches between labels, policy and real SDKs are a common rejection and enforcement cause.

**Apple only**
- **Privacy manifest** (`PrivacyInfo.xcprivacy`): required for the app and for listed commonly used third-party SDKs. It declares the data collected and the "required reason" APIs used (e.g. UserDefaults, file timestamps, system boot time, disk space).
  - Code check: the file exists in the iOS target, and SDK versions are recent enough to ship their own manifests.

**Google Play only**
- **User Data policy, Prominent disclosure:** when an app collects personal or sensitive data in a way users would not expect, an in-app disclosure must come **before** the consent/runtime permission request.

Sources: <https://developer.apple.com/documentation/bundleresources/privacy-manifest-files>, <https://support.google.com/googleplay/android-developer/answer/10787469>, <https://support.google.com/googleplay/android-developer/answer/10144311>

## §2 Account deletion

- **Apple 5.1.1(v):** apps that support account creation **must let users initiate account deletion inside the app**. A link to a website is acceptable only if it leads directly to the deletion page. Highly regulated industries may add verification steps. Source: <https://developer.apple.com/help/app-review/guideline-reference/5-1-1-account-deletion>
- **Google Play User Data policy:** apps that allow account creation must:
  - offer deletion **in the app**, and
  - provide a **web link** (in the Data safety form) where users can request account and associated data deletion **without reinstalling** the app.

  The page must name the app or developer, and deleting the account must also delete the associated data (except what must be retained by law, which must be disclosed). Source: <https://support.google.com/googleplay/android-developer/answer/13327111>
- Apple 5.1.1(v) also says apps may not require sign-in for features that do not need an account.
- Code signals: `deleteUser`, `currentUser.delete()`, `/account/delete`, "Delete account", "Hesabı sil". If auth SDKs exist but no deletion path is found → P0 for mobile.

## §3 Permissions and tracking

- **iOS:** every protected resource needs a purpose string in `Info.plist` (`NSCameraUsageDescription`, `NSLocationWhenInUseUsageDescription`, `NSPhotoLibraryUsageDescription`, `NSMicrophoneUsageDescription`, `NSContactsUsageDescription`…). The text must explain the real purpose.
- **iOS tracking:** linking data with other companies' data for targeted ads or measurement, or sharing with data brokers, requires **App Tracking Transparency** (`NSUserTrackingUsageDescription` + `ATTrackingManager.requestTrackingAuthorization`) before accessing IDFA or tracking.
- **Android:** request only the permissions the app uses (check `AndroidManifest.xml`). Sensitive permissions are restricted and may need a declaration form in Play Console:
  - location in background,
  - SMS / call log,
  - `QUERY_ALL_PACKAGES`,
  - `MANAGE_EXTERNAL_STORAGE`,
  - accessibility services,
  - exact alarms.
- **Audit rule:** permission declared but never used in code → "too much" finding (data minimisation + store risk).

## §4 Monetisation: trader status, ads consent, subscriptions

- **EU trader status (DSA Art. 30–31):**
  - **Apple:** every developer must declare trader or non-trader status in App Store Connect. Traders' address, phone and email are shown on EU product pages, and apps without a declared status were removed from EU storefronts in Feb 2025. Source: <https://developer.apple.com/help/app-store-connect/manage-compliance-information/manage-european-union-digital-services-act-compliance-information>
  - **Google Play:** has a similar trader declaration in Play Console. Google has announced that traders' contact details (including phone and address for personal accounts) will be shown on store listings from 1 March 2027.
  - Monetisation (paid app, IAP, **or ads**) is a strong indicator of trader status. Being an individual does not automatically make you a non-trader. Solo developers should consider a business address/phone before declaring.
- **Ads in the EEA, UK and Switzerland:** Google requires a **Google-certified CMP integrated with IAB TCF** to serve personalised ads (EEA/UK since 16 Jan 2024, Switzerland since 31 July 2024). The Google **User Messaging Platform (UMP) SDK** qualifies. Without it, only non-personalised or limited ads may serve. Source: <https://support.google.com/admob/answer/13554116>
  - Code check: AdMob SDK present → UMP (`ConsentInformation`, `UserMessagingPlatform`, `ConsentForm`) present and requested **before** loading ads.
- **Subscriptions:**
  - Apple 3.1.2: clear terms, price, period, and what the user gets, before purchase.
  - Google Play subscriptions policy: clear offer terms and an easy cancel path (link to store subscription management).
  - Restore purchases button (Apple).
  - Link to the Terms of Use/EULA and privacy policy on the paywall.

## §5 Age rating, kids, user-generated content

- **Apple age ratings:** the system now uses **4+, 9+, 13+, 16+ and 18+**. Developers had to answer the updated questionnaire (in-app controls, capabilities, medical/wellness, violent themes) by 31 January 2026, or app updates are blocked. Source: <https://developer.apple.com/news/?id=ks775ehf>
- **Kids:**
  - Apple Kids Category: no third-party analytics/ads except in limited cases, plus a parental gate.
  - Google Play Families policy: certified ad SDKs only, no precise location.
- **UGC apps (Apple 1.2, Google Play UGC policy):** the app must have all of:
  - a method to filter objectionable content,
  - a mechanism to report offensive content,
  - the ability to block abusive users,
  - published contact information.

  Apple updated guidelines in 2025–2026 to stress age-appropriate experiences for creator/UGC content.

## §6 Android developer verification (all distribution channels)

Source: <https://support.google.com/android-developer-console/answer/16561738>

- Apps installed on **certified Android devices** must be registered by a **verified developer**, whichever store they come from: Google Play, other stores or sideloaded APKs.
- In force since **30 September 2026** in Brazil, Indonesia, Singapore and Thailand. **Global rollout planned from 2027.**
- Play developers verify in Play Console. Developers distributing **only outside Play** use the Android Developer Console.
- Audit: if the app is distributed as an APK or via third-party stores, mark ❓ "developer identity verified and app registered?".

## §7 Not store law, but often asked

- **Login services (Apple 4.8):** if the app uses a third-party or social login for the primary account, it must also offer an equivalent login option that meets Apple's privacy criteria (limits data to name/email, allows hiding the email, no ad tracking without consent). Sign in with Apple qualifies. Exceptions exist, so check the live guideline.
- **Export compliance:** encryption declaration in App Store Connect (`ITSAppUsesNonExemptEncryption`).
