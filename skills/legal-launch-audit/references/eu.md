# European Union / EEA reference (most points also apply to the UK)

Last verified: 2026-11-17. EU directives are implemented by national law; details (fines, wording, exact deadlines) can differ per member state. When the user names a country (e.g. Poland, Germany), say that national implementation must be checked.

## §1 GDPR (Regulation (EU) 2016/679)

Source: <https://eur-lex.europa.eu/eli/reg/2016/679/oj>

**Territorial scope (Art. 3):** applies to controllers established in the EU, and to non-EU controllers that **offer goods/services to people in the EU** or **monitor their behaviour** (e.g. tracking/analytics aimed at EU users). Signals of targeting include EU languages and currencies, EU shipping, and EU app-store storefronts combined with EU marketing.

**Checks:**
- **Privacy notice (Art. 13/14):** it must cover:
  - controller identity and contact, plus the DPO if one is appointed,
  - purposes and legal basis for each purpose,
  - legitimate interests where relied on,
  - recipients,
  - third-country transfers and the safeguard used,
  - retention periods,
  - rights (including complaint to a supervisory authority),
  - whether data provision is required,
  - automated decision-making.
- **Legal basis (Art. 6):** consent is only one option. Do not ask for consent for contract performance.
- **Consent (Art. 7):** freely given, specific, informed, unambiguous; withdrawable as easily as given; no pre-ticked boxes.
- **Rights (Art. 15–22):** a working request channel; answer within one month as a rule.
- **Records of processing (Art. 30):** the exemption for organisations under 250 employees does not apply if processing is not occasional, is risky, or involves special-category data. In practice most online businesses should keep records.
- **DPIA (Art. 35):** needed for high-risk processing, e.g. large-scale profiling or special-category data, systematic monitoring and new technologies. Flag ❓ when signals appear (health data, biometrics, location tracking, AI scoring).
- **Processors (Art. 28):** a data processing agreement (DPA) with each vendor (hosting, analytics, email, AI APIs).
- **International transfers (Chapter V):** an adequacy decision (e.g. the EU-US Data Privacy Framework for certified US companies), otherwise standard contractual clauses plus a transfer impact assessment.
- **EU representative (Art. 27):** required for non-EU controllers within Art. 3(2) scope, unless occasional and low-risk processing.
- **Security (Art. 32), breach notification (Art. 33/34):** notify the supervisory authority within 72 hours where required.

## §2 ePrivacy: cookies and device storage

Source: Directive 2002/58/EC Art. 5(3) (national laws implement it): <https://eur-lex.europa.eu/eli/dir/2002/58/oj>

- Storing or reading information on the user's device (cookies, localStorage, SDK identifiers, fingerprinting) requires **prior consent**, unless strictly necessary for the service requested.
- Regulators expect a "reject" option on the first layer that is as easy as "accept", no pre-ticked purposes, no "consent by scrolling", and no loading of trackers before consent.
- Ad tech in the EEA/UK/CH: Google requires a Google-certified CMP integrated with IAB TCF for personalised ads (see app-stores.md §4).
- Code check: in the HTML/bundle, find tracking tags and SDK initialisation and confirm they are gated by a consent state.

## §3 Consumer law

Sources: Consumer Rights Directive 2011/83/EU as amended by Directive (EU) 2023/2673 (<https://eur-lex.europa.eu/eli/dir/2023/2673/oj>); Price Indication Directive 98/6/EC as amended by the Omnibus Directive (EU) 2019/2161; e-Commerce Directive 2000/31/EC Art. 5–6, 10–11; Regulation (EU) 2024/3228 (ODR repeal).

- **Trader identity (e-Commerce Directive Art. 5):**
  - name,
  - geographic address,
  - email,
  - trade register number,
  - VAT number,
  - supervisory authority / professional rules where relevant.

  In Germany and Austria this is the well-known "Impressum".
- **Pre-contract information (CRD Art. 6)** and confirmation on a durable medium. Show the total price including taxes and all mandatory fees.
- **Order button:** must be labelled clearly, e.g. "order with obligation to pay".
- **Right of withdrawal: 14 days (CRD Art. 9–16).** The model withdrawal form must be provided.
  - Digital content not on a tangible medium: the withdrawal right is lost only if performance began with the consumer's **prior express consent and acknowledgement**. This must be captured in the checkout.
- **Withdrawal function ("withdrawal button", new CRD Art. 11a):** applies **since 19 June 2026** to distance contracts concluded through an online interface (website or app) where a withdrawal right exists. Requirements:
  - a clearly labelled function (e.g. "withdraw from contract here"), available throughout the withdrawal period,
  - a two-step flow: the consumer enters or confirms the details, then a confirmation button,
  - an acknowledgement of receipt sent on a durable medium without undue delay.

  Some member states transposed late, but the obligation applies. Audit trigger: EU B2C online sales.
- **Price reductions (Omnibus):** an announced reduction must show the **lowest price in the prior 30 days** (member states may vary for perishables or new products).
- **Reviews (Omnibus):** if you publish consumer reviews, state whether and how you ensure they come from real buyers. Fake reviews are banned.
- **Personalised pricing:** must be disclosed when the price is personalised by automated decision-making.
- **ODR platform:** closed on **20 July 2025**, and the duty to link to it was repealed. **Remove old ODR links** (status X in the matrix). Information about ADR bodies may still be required by national law and sector.

## §4 European Accessibility Act (Directive (EU) 2019/882)

Source: <https://eur-lex.europa.eu/eli/dir/2019/882/oj>

- Applies since **28 June 2025** to covered services provided to consumers. Covered services include **e-commerce services** (websites and mobile apps used to sell to consumers), consumer banking, e-books, electronic communications, and passenger-transport digital services.
- **Microenterprise exemption for services:** fewer than 10 employees **and** annual turnover or balance sheet ≤ €2 million. It does not cover products.
- Practical standard: EN 301 549 / WCAG 2.1 AA. You must also give information on how the service meets the requirements (an accessibility statement).
- Transitional rules: service contracts agreed before 28 June 2025 may continue until 28 June 2030.
- Audit checks in code:
  - `alt` attributes on images,
  - labels on form fields,
  - `lang` attribute,
  - colour contrast (flag for manual check),
  - keyboard focus,
  - accessible names on icon buttons,
  - Flutter `Semantics` and Android/iOS content descriptions.

## §5 Digital Services Act (Regulation (EU) 2022/2065)

Source: <https://eur-lex.europa.eu/eli/reg/2022/2065/oj>

- **All intermediary services** (including hosting of user content): a single point of contact (Art. 11/12) and terms that explain content moderation (Art. 14).
- **Hosting services:** notice-and-action mechanism (Art. 16) and a statement of reasons when removing content (Art. 17).
- **Online platforms:**
  - internal complaint system,
  - no dark patterns (Art. 25),
  - ad transparency (Art. 26),
  - recommender-system transparency (Art. 27),
  - minors' protection (Art. 28).

  Micro and small enterprises are exempt from most platform-level duties (Art. 19).
- **Marketplaces:** trader traceability (Art. 30) and compliance by design (Art. 31).
- **App developers:** stores must collect and display trader details under Art. 30–31 (see app-stores.md §4).

## §6 AI Act (Regulation (EU) 2024/1689)

Source: <https://eur-lex.europa.eu/eli/reg/2024/1689/oj>

- **Transparency obligations (Art. 50) apply since 2 August 2026.** The Digital Omnibus on AI (adopted mid-2026) postponed the high-risk system duties but **did not** postpone Art. 50, except for a short delay of the machine-readable marking duty (Art. 50(2)) for generative systems already on the market.
  - Systems that interact with people (chatbots, voice assistants): users must be told they are interacting with AI unless it is obvious.
  - Generative AI output (text, image, audio, video): providers must mark it as AI-generated in a machine-readable way.
  - Deployers publishing deepfakes, or AI text on matters of public interest: these must be disclosed.
  - Emotion recognition / biometric categorisation: inform the people exposed.
- **AI literacy (Art. 4)** has applied since 2 Feb 2025 to providers and deployers.
- **Prohibited practices (Art. 5)** have applied since 2 Feb 2025, e.g. manipulative techniques, social scoring and some biometric uses. Flag P0 if there are signals.
- Audit trigger: AI SDKs/APIs in code (openai, gemini/genai, mistral, LLM chat UIs), AI image generation features, AI avatars.

## §7 Cyber Resilience Act (Regulation (EU) 2024/2847)

Source: <https://eur-lex.europa.eu/eli/reg/2024/2847/oj>

- **Scope:** products with digital elements made available in the EU, **including standalone software such as mobile and desktop apps**, even when free in some cases, plus the remote data processing needed for them. Pure SaaS without a distributed product is generally outside scope. Open-source projects that are not monetised have special treatment.
- **Since 11 September 2026 (Art. 14):** manufacturers must report **actively exploited vulnerabilities** and **severe incidents** affecting their products via ENISA's Single Reporting Platform:
  - an early warning within 24 hours,
  - then a notification within 72 hours,
  - then a final report.

  This also applies to products already on the market.
- **From 11 December 2027:** full essential cybersecurity requirements, vulnerability handling, security updates for the support period, SBOM, conformity assessment and CE marking.
- **Audit checks:**
  - a published way to report vulnerabilities (e.g. `security.txt`, `SECURITY.md` or a security contact on the site/app page),
  - a named person/process for 24-hour reporting,
  - a dependency inventory.

  Mark ❓ for the process. Code can only show whether a security contact exists.

## §8 UK note

The UK GDPR and PECR mirror most EU privacy and cookie rules. The **Online Safety Act** applies to user-to-user and search services with links to the UK. It requires illegal-content and children's risk assessments, and highly effective age assurance where pornography or other primary priority content is possible. Flag ❓ for UGC services with UK users.

## §9 Member-state notes

- **Poland:**
  - the data protection authority is the UODO,
  - national consumer law follows the CRD,
  - business activity registration and tax status (CEIDG, VAT) are **out of scope**; refer to an accountant or lawyer.
- **Germany/Austria:**
  - the Impressum is strictly enforced via competitor warning letters,
  - the TDDDG (Germany) implements the cookie rules.
- **France:** the CNIL publishes detailed cookie and consent guidance; a "reject all" option on the first layer is expected.
