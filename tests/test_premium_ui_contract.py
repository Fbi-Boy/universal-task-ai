from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "backend" / "web"


class PremiumUiContractTests(unittest.TestCase):
    def setUp(self):
        self.html = (WEB / "index.html").read_text(encoding="utf-8")
        self.css = (WEB / "ui.css").read_text(encoding="utf-8")
        self.js = (WEB / "ui.js").read_text(encoding="utf-8")

    def test_every_javascript_id_selector_exists_in_markup(self):
        selectors = set(re.findall(r'document\.querySelector\("#([a-zA-Z0-9_-]+)"\)', self.js))
        markup_ids = set(re.findall(r'\bid="([a-zA-Z0-9_-]+)"', self.html))
        self.assertTrue(selectors)
        self.assertEqual(selectors - markup_ids, set())

    def test_navigation_anchors_resolve_to_existing_sections(self):
        targets = set(re.findall(r'\bid="([a-zA-Z0-9_-]+)"', self.html))
        hrefs = re.findall(r'<a\b[^>]*\bhref="#([^"]+)"', self.html)
        self.assertGreaterEqual(len(hrefs), 5)
        self.assertEqual(set(hrefs) - targets, set())

    def test_api_key_is_not_persisted_in_local_storage_or_url(self):
        self.assertIn('sessionStorage.setItem("uta_api_key"', self.js)
        self.assertNotIn("localStorage", self.js)
        self.assertNotRegex(self.js, r'\b(?:location\.href|window\.location)\s*=.*apiKey')

    def test_responsive_and_reduced_motion_styles_exist(self):
        self.assertIn("@media (max-width: 1200px)", self.css)
        self.assertIn("@media (max-width: 850px)", self.css)
        self.assertIn("@media (max-width: 600px)", self.css)
        self.assertIn("prefers-reduced-motion: reduce", self.css)

    def test_accessible_navigation_and_task_controls_exist(self):
        self.assertIn('aria-label="Primary navigation"', self.html)
        self.assertIn('aria-labelledby="composer-title"', self.html)
        self.assertIn('id="focus-task"', self.html)
        self.assertIn('workspaceSearch.onkeydown', self.js)


if __name__ == "__main__":
    unittest.main()
