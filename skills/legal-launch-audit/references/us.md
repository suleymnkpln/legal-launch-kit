# United States reference

Last verified: 2026-11-17. There is no comprehensive federal privacy law. As of late 2026 about 20 states have comprehensive consumer privacy laws in force and a few more are enacted with 2027–2028 start dates. Check a current tracker before stating a count.

## §1 State privacy laws (CCPA/CPRA as the reference model)

Sources: <https://oag.ca.gov/privacy/ccpa>, <https://cppa.ca.gov/regulations/>

**CCPA applies to for-profit businesses doing business in California that meet any one of:**
- annual gross revenue above the threshold (USD 25 million, adjusted for inflation; check the current figure),
- buying, selling or sharing the personal information of 100,000 or more California consumers or households,
- deriving 50% or more of annual revenue from selling or sharing personal information.

Most small indie apps and sites are **below** these thresholds. Report as **➖ not applicable (threshold)** unless the user confirms otherwise. Do not inflate obligations.

**If applicable:**
- a privacy policy with the CCPA-specific disclosures, updated every 12 months,
- "Do Not Sell or Share My Personal Information" (and "Limit the Use of My Sensitive Personal Information" where relevant) links, or a combined opt-out,
- honour **Global Privacy Control (GPC)** browser signals as an opt-out,
- a notice at collection,
- since 1 Jan 2026, updated CCPA regulations: risk assessments for high-risk processing; ADMT (automated decision-making technology) duties for significant decisions from 1 Jan 2027; cybersecurity audits phased in from 2028.

**CalOPPA (California Online Privacy Protection Act)** is broader: any commercial website or online service collecting personally identifiable information from California residents must post a privacy policy, regardless of size. That is why a privacy policy is effectively **R** for any US-facing project.

**Other states** (Virginia, Colorado, Connecticut, Texas, Oregon and others): similar rights, opt-outs for targeted advertising and sale, consent for sensitive data, often universal opt-out signal recognition. Thresholds are usually based on the number of residents' records (often 100,000) rather than revenue, but Texas and Nebraska apply to almost every business that is not a small business as defined by the SBA. Treat these as **C** with the threshold question.

## §2 Children: COPPA

Source: amended COPPA Rule (90 FR 16918), effective 23 June 2025, **compliance date 22 April 2026**: <https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule>

- **Applies to:** services directed to children under 13, mixed-audience services, and general-audience services with actual knowledge that they collect personal information from under-13s.
- **Required:**
  - verifiable parental consent before collecting,
  - a direct notice to parents,
  - an online notice,
  - data retention limits and a written retention policy,
  - a written information security program.

  Under the amendments, disclosure to third parties for targeted ads needs separate consent.
- **Mixed-audience services** may age-screen and apply COPPA only to under-13 users.
- **Audit signals:**
  - "kids", "children" or "for ages 4+" in metadata,
  - Google Play Families or Apple Kids category,
  - `tagForChildDirectedTreatment`, AdMob max ad content rating,
  - cartoonish UI combined with ad SDKs.
- **State app-store age-verification laws** (e.g. Utah, Texas, Louisiana) and kids' online-safety laws are evolving and partly in litigation. Flag ❓ for apps likely used by minors.

## §3 Subscriptions and auto-renewal

Sources: ROSCA (<https://www.ftc.gov/legal-library/browse/statutes/restore-online-shoppers-confidence-act>), FTC Act §5, state automatic-renewal laws (e.g. California ARL, amended 2025).

- The FTC's 2024 "Click-to-Cancel" rule was **vacated** by the Eighth Circuit on 8 July 2025 (on procedural grounds). The FTC restarted rulemaking in 2026, and **ROSCA still applies**:
  - clear disclosure of all material terms before taking billing information,
  - express informed consent before charging,
  - a simple mechanism to stop recurring charges.
- State laws (California especially) require online cancellation, renewal reminders for some plans, and consent to renewal terms.
- Audit check:
  - the paywall shows the price, period, renewal terms and how to cancel, near the buy button,
  - the cancellation path is no harder than signing up,
  - free-trial conversion terms are clear.

## §4 Other federal touch-points

- **FTC Act §5 (deception/unfairness):** privacy policies must match practice. This is the most common FTC privacy theory, and it is why "policy vs. SDK" mismatches are high priority.
- **FTC endorsement guides and fake-review rule:** fake reviews, undisclosed incentivised reviews and review suppression are prohibited.
- **CAN-SPAM:** commercial emails need an accurate sender, a non-deceptive subject, a physical postal address, and a working unsubscribe honoured within 10 business days.
- **TCPA:** marketing SMS/calls need prior express written consent.
- **ADA (websites):** there is no single federal web standard for private businesses, but web-accessibility lawsuits are frequent. WCAG 2.1 AA is the de facto benchmark. Report it as **O** (recommended), raising it to a risk note for US-facing e-commerce.
