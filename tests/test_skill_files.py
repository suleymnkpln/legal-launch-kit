"""Validates SKILL.md frontmatter and that referenced files exist.

Agent tools refuse to load a skill whose frontmatter does not parse, so this
runs in CI on every push. No third-party YAML library is needed: the
frontmatter is kept to simple `key: value` lines on purpose.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with '---' on the first line")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("frontmatter is not closed with '---'")
    data = {}
    for raw in text[4:end].splitlines():
        if not raw.strip():
            continue
        if raw.startswith((" ", "\t")):
            raise ValueError(f"nested/indented YAML not allowed here: {raw!r}")
        key, sep, value = raw.partition(":")
        if not sep:
            raise ValueError(f"not a key: value line: {raw!r}")
        value = value.strip()
        if value.startswith(("'", '"')) and not value.endswith(value[0]):
            raise ValueError(f"unclosed quote in {key}")
        if not value.startswith(("'", '"')) and ": " in value:
            raise ValueError(f"unquoted ': ' inside value of {key} breaks YAML; quote the value")
        data[key.strip()] = value.strip("'\"")
    return data


class SkillFilesTest(unittest.TestCase):
    def test_each_skill(self):
        skill_dirs = [d for d in SKILLS.iterdir() if d.is_dir()]
        self.assertTrue(skill_dirs, "no skills found")
        for d in skill_dirs:
            with self.subTest(skill=d.name):
                text = (d / "SKILL.md").read_text(encoding="utf-8")
                fm = parse_frontmatter(text)
                self.assertEqual(fm.get("name"), d.name)
                self.assertRegex(fm["name"], NAME_RE)
                self.assertLessEqual(len(fm["name"]), 64)
                desc = fm.get("description", "")
                self.assertTrue(desc, "description missing")
                self.assertLessEqual(len(desc), 1024)
                self.assertNotRegex(desc, r"[<>]")
                # Every relative link in SKILL.md must point to a real file.
                for link in re.findall(r"\]\(((?:references|scripts)/[^)#]+)\)", text):
                    self.assertTrue((d / link).is_file(), f"broken link: {link}")

    def test_reference_dates(self):
        for ref in (SKILLS / "legal-launch-audit" / "references").glob("*.md"):
            if ref.name == "report-format.md":
                continue
            with self.subTest(ref=ref.name):
                self.assertRegex(ref.read_text(encoding="utf-8"), r"Last verified: \d{4}-\d{2}-\d{2}")


if __name__ == "__main__":
    unittest.main()
