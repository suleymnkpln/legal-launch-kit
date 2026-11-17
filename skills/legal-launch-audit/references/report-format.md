# Report format

Write the report in the user's language. Turkish headings are given in brackets for Turkish users.

## Status icons

| Icon | Meaning |
|---|---|
| ✅ | Present and matches real behaviour |
| ❌ | Required but missing |
| ⚠️ | Present but incomplete, outdated or contradicting the code (e.g. the policy omits an SDK found in code) |
| ➖ | Not applicable. Always give the reason (e.g. "no sales → no distance contract needed") |
| ❓ | Cannot be decided from the code. Needs a fact from the user or a professional |
| 🗑️ | Present but unnecessary or harmful clutter: remove it |

## Priority

| Level | Meaning | Examples |
|---|---|---|
| **P0** blocker | Likely store rejection, illegal processing, or a high-fine risk | no account deletion in an app with sign-up; trackers fire before consent; special-category data without a basis; no privacy policy |
| **P1** high | Clear legal gap with real exposure | foreign transfer not disclosed; marketing SMS without İYS; missing pre-contract form in a shop; missing EU withdrawal button |
| **P2** medium | Incomplete content, mismatches, clutter that misleads | policy lists the wrong SDKs; forced consent checkbox; outdated ODR link |
| **P3** low | Good practice | accessibility statement for an exempt microenterprise; cookie table formatting |

## Required structure

```markdown
# Legal launch audit: <project name>  [Yasal yayın denetimi]

Date: YYYY-MM-DD · Scope: <web | android | ios | flutter …> · Markets: <TR, EU, US …>
Mode: read-only (no files changed)

## 1. What the product does  [Ürün özeti]
One paragraph: purpose, users (B2C/B2B, age), revenue model, personal data needed, legally relevant features, sector(s). Mark anything inferred as "assumed" and ask the user to confirm.

## 1b. Project profile  [Proje profili]
| Question | Answer | Evidence |
|---|---|---|
| Sells to consumers? | yes/no/unknown | file:line or "user said" |
| Accounts? | … | … |
| Ads / analytics / pixels | … | … |
| Data stored abroad | … | … |
| Commercial messages (SMS/email) | … | … |
| Children / special-category data | … | … |
| Assumptions made | … | |

## 2. Findings  [Bulgular]
| # | Status | Priority | Item | Evidence (file:line) | Why it applies to *this* project | Fix | Source |
|---|---|---|---|---|---|---|---|
| 1 | ❌ | P0 | In-app account deletion | lib/auth/sign_up.dart:42 (sign-up exists), no delete path found | Users create accounts on the sign-up screen, so both stores require that they can delete them in the app; without it the next update is rejected | Add Settings → Delete account (call `currentUser.delete()` + delete Firestore user docs) and a web deletion page for Google Play | link |

Group the rows: Privacy · Consumer/commerce · Technical · Store · Content/AI.

## 3. Not needed / remove  [Gereksiz veya kaldırılmalı]
Items marked ➖ or 🗑️ with one-line reasons.

## 4. Needs a human decision  [İnsan kararı gerekenler]
Items marked ❓ with the exact question to answer (e.g. "Is a KVKK standard contract signed with Google for Firebase and notified within 5 business days?").

## 5. Prioritised action plan  [Öncelikli eylem planı]
P0 → P3, each a single concrete action with an owner hint (dev / legal / business).

## 6. Limits  [Sınırlar]
Not legal advice. Laws verified as of <reference date>. Items outside scope (tax, company registration, licences) listed.
```

## Rules for evidence

- Cite `path:line` for every code-based claim. Use the detector output, then open the file to confirm before citing.
- For "missing" claims, say what was searched (e.g. "no route or file matching privacy|gizlilik|kvkk under src/, public/").
- Never claim a contract, registration (ETBİS, VERBİS, İYS) or store setting exists or is missing based on code alone. Those are ❓ unless the user confirms.
- Link the official source for each legal claim (from the reference files). Do not invent article numbers.
