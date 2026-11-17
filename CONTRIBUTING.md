# Contributing

Thanks for helping keep launch-time legal requirements clear and current.

## Ground rules

1. **Every legal claim needs a source.** Prefer official sources: legislation portals, regulator guidance, official gazettes, store policy pages. Secondary sources (law firm notes) are fine for context, but link the primary text where it exists.
2. **No legal advice wording.** Describe what a rule requires and when it applies. Do not tell readers what to do in their specific case.
3. **Write the trigger.** Every requirement must say *when* it applies. "Always" is rarely true.
4. **Update the date.** If you change a reference file, update its `Last verified:` line.
5. **Short quotes only.** Paraphrase legal texts and guidance in your own words and link them. Do not paste long passages.

## Types of contributions

| You want to… | Do this |
|---|---|
| Report an outdated rule | Open a **Law update** issue with the source link and effective date |
| Fix a rule | Edit the reference file + matrix row, update `Last verified:` |
| Add a country/market | Add `skills/legal-launch-audit/references/<country>.md` (copy the structure of `turkiye.md`), add rows or a "Markets" code to `matrix.md`, and link it in `SKILL.md` step 3 |
| Improve detection | Add a pattern to `SIGNALS` in `scripts/detect.py`, add a case to `tests/fixtures/`, and a test in `tests/test_detect.py` |
| Add a checklist/template | Put it in `checklists/<lang>/` or `templates/<lang>/` and link it from the README |

## Development

```bash
python3 -m unittest discover -s tests -v
python3 skills/legal-launch-audit/scripts/detect.py tests/fixtures/sample-app
```

The detector must stay **dependency-free** and **read-only**.

## SKILL.md rules (checked in CI)

- The frontmatter is plain `key: value` lines. Only `name` and `description` are used.
- `name` equals the folder name: lowercase, digits, hyphens, max 64 characters.
- `description` is at most 1024 characters, with no `<` or `>`. Do not put an unquoted `: ` inside it, because that breaks YAML parsing in some tools.
- Relative links in SKILL.md must point to existing files.
