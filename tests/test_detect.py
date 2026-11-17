"""Tests for the detector. Run: python3 -m unittest discover -s tests"""

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "legal-launch-audit" / "scripts" / "detect.py"
FIXTURE = ROOT / "tests" / "fixtures" / "sample-app"

spec = importlib.util.spec_from_file_location("detect", SCRIPT)
detect = importlib.util.module_from_spec(spec)
spec.loader.exec_module(detect)


class DetectFixtureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = detect.scan(FIXTURE, max_hits=5)
        cls.flags = {f["id"] for f in cls.result["derived_flags"]}

    def test_platforms(self):
        self.assertIn("web", self.result["platforms"])
        self.assertIn("flutter", self.result["platforms"])
        self.assertIn("android", self.result["platforms"])

    def test_expected_flags(self):
        expected = {
            "trackers_without_consent_manager",
            "admob_without_ump",
            "auth_without_deletion",
            "foreign_processors",
            "pii_overcollection",
            "odr_link",
            "sales_without_precontract",
            "marketing_messages",
            "consent_antipatterns",
            "cleartext",
            "android_sensitive_permissions",
            "social_tr_under15",
            "cra_security_contact",
            "android_dev_verification",
        }
        missing = expected - self.flags
        self.assertFalse(missing, f"missing flags: {missing}")

    def test_no_false_flags(self):
        # The fixture links a privacy page, so this flag must not fire.
        self.assertNotIn("no_privacy_notice", self.flags)
        # No AI SDK in the fixture.
        self.assertNotIn("ai_features", self.flags)

    def test_evidence_has_file_and_line(self):
        for sig in self.result["signals"].values():
            for ev in sig["evidence"]:
                self.assertTrue((FIXTURE / ev["file"]).is_file(), ev)
                self.assertGreaterEqual(ev["line"], 1)

    def test_contacts_permission_is_not_a_contact_page(self):
        mentions = self.result["legal_pages"]["imprint_contact"]["mentions"]
        self.assertFalse(any("AndroidManifest" in m["file"] for m in mentions))

    def test_project_summary_and_sectors(self):
        sources = {item["source"] for item in self.result["project_summary"]}
        self.assertIn("README.md", sources)
        self.assertIn("health_fitness", self.result["sector_hints"])

    def test_turkish_pattern_helper(self):
        import re
        pat = re.compile(detect.tr("çerez"), re.I)
        for word in ("çerez", "Çerez", "cerez", "CEREZ"):
            self.assertTrue(pat.search(word), word)

    def test_cli_json(self):
        out = subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURE), "--format", "json"],
            check=True, capture_output=True, text=True,
        ).stdout
        data = json.loads(out)
        self.assertIn("derived_flags", data)


RN_IOS = ROOT / "tests" / "fixtures" / "rn-ios-app"
CLEAN = ROOT / "tests" / "fixtures" / "clean-site"


class DetectRnIosTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = detect.scan(RN_IOS, max_hits=5)
        cls.flags = {f["id"] for f in cls.result["derived_flags"]}

    def test_platforms(self):
        self.assertIn("ios", self.result["platforms"])
        self.assertIn("react-native", self.result["platforms"])

    def test_ios_flags(self):
        for flag in ("no_privacy_manifest", "ios_tracking_without_att", "admob_without_ump",
                     "ai_features", "subscription_terms", "cleartext", "no_privacy_notice"):
            self.assertIn(flag, self.flags)

    def test_deletion_found(self):
        self.assertIn("account_deletion", self.result["signals"])
        self.assertNotIn("auth_without_deletion", self.flags)

    def test_iap_only_has_no_refund_page_flag(self):
        # Store billing handles refunds; do not ask for a web shop returns page.
        self.assertNotIn("sales_without_withdrawal", self.flags)
        self.assertNotIn("sales_without_precontract", self.flags)

    def test_summary_from_package_and_plist(self):
        values = " ".join(i["value"] for i in self.result["project_summary"])
        self.assertIn("AI chat companion", values)
        self.assertIn("ChatPal", values)


class DetectCleanSiteTest(unittest.TestCase):
    def test_no_flags_for_clean_brochure_site(self):
        result = detect.scan(CLEAN, max_hits=5)
        self.assertEqual(result["derived_flags"], [], result["derived_flags"])

    def test_fail_on_exit_codes(self):
        clean = subprocess.run([sys.executable, str(SCRIPT), str(CLEAN), "--fail-on", "P0"],
                               capture_output=True, text=True)
        self.assertEqual(clean.returncode, 0)
        dirty = subprocess.run([sys.executable, str(SCRIPT), str(FIXTURE), "--fail-on", "P0"],
                               capture_output=True, text=True)
        self.assertEqual(dirty.returncode, 1)
        self.assertIn("auth_without_deletion", dirty.stderr)


if __name__ == "__main__":
    unittest.main()
