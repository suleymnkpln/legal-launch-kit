# Changelog

## 0.3.0 — 2026-11-18
- `--fail-on P0|P1|P2|P3` for CI: exit code 1 when blockers are found; GitHub Actions example in README.
- Turkish templates: distance sales contract, terms of use, account deletion page.
- New test fixtures: React Native + iOS app, clean brochure site (no-false-positive check). 17 tests.
- In-app purchases alone no longer trigger the web-shop returns-page flag (stores handle refunds).

## 0.2.0 — 2026-11-17
- Product understanding step: the detector extracts the project summary (README, store listing, package/pubspec, app name, page title) and sector hints; the skill confirms the purpose before judging.
- New `references/sectors.md` (health, finance, kids, social, dating, marketplace, gambling, AI, IoT, restricted goods…).
- New 2026 rules: Türkiye under-15 social network ban + e-Devlet age verification (Law 7578, regulation in force 1 Nov 2026), EU Cyber Resilience Act reporting (since 11 Sept 2026), UK Online Safety Act note, Android developer verification.
- Findings must explain why the rule applies to *this* project, with a concrete fix.
- README: compatibility table for Claude Code, Codex, Copilot, Gemini CLI, Cursor and others; `npx skills add`.

## 0.1.0 — 2026-11-17
- First release: requirement matrix (7 project types), references for Türkiye, EU, US and app stores (verified 2026-11-17).
- `detect.py` scanner with file:line evidence and review flags (web, Flutter, Android, iOS, React Native).
- `legal-launch-audit` agent skill.
- Checklists (EN/TR), skeleton templates, sample report, CI tests.
