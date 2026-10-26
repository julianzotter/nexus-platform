import json
import re
import sys
import unittest
from pathlib import Path

GALLERY = Path(__file__).resolve().parents[1] / "prototypes" / "design-gallery"
sys.path.insert(0, str(GALLERY))
from build_manifest import ROOT, build, tracked_files  # noqa: E402


class DesignGalleryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = build()
        cls.designs = {d["id"]: d for d in cls.manifest["designs"]}

    def test_ids_unique(self):
        self.assertEqual(len(self.designs), len(self.manifest["designs"]))

    def test_every_tracked_html_outside_gallery_is_listed(self):
        html = {f for f in tracked_files(ROOT) if f.endswith(".html") and not f.startswith("prototypes/design-gallery/")}
        listed = {d["path"] for d in self.manifest["designs"] if d["kind"] == "html"}
        self.assertEqual(html, listed)

    def test_previews_and_scripts_resolve(self):
        for d in self.manifest["designs"]:
            for key in ("preview", "script"):
                if key in d:
                    self.assertTrue((GALLERY / d[key]).resolve().is_file(), d[key])

    def test_catalog_concepts_included(self):
        catalog = json.loads((ROOT / "docs/concepts/2026-10-13/catalog.json").read_text(encoding="utf-8"))
        for c in catalog["concepts"]:
            self.assertEqual(self.designs[c["id"]]["status"], c["status"])

    def test_curated_architectures_stay_unverified_and_consistent(self):
        arch = [d for d in self.manifest["designs"] if d["kind"] == "architecture"]
        self.assertTrue(arch)
        for d in arch:
            self.assertIn("unverified", d["status"])
            self.assertTrue(d.get("provenance"))
            ids = {n["id"] for n in d["diagram"]["nodes"]}
            for src, dst, _ in d["diagram"]["edges"]:
                self.assertIn(src, ids)
                self.assertIn(dst, ids)

    def test_committed_manifest_matches_build(self):
        text = (GALLERY / "designs.manifest.js").read_text(encoding="utf-8")
        stored = json.loads(text.removeprefix("window.NEXUS_DESIGNS = ").rstrip().rstrip(";"))
        # commit is excluded: it changes as soon as the manifest itself is committed
        self.assertEqual(stored["designs"], self.manifest["designs"], "run prototypes/design-gallery/build_manifest.py")

    def test_previews_are_sandboxed_without_same_origin(self):
        html = (GALLERY / "index.html").read_text(encoding="utf-8")
        frames = re.findall(r"<iframe[^>]*>", html)
        self.assertTrue(frames)
        for frame in frames:
            self.assertIn("sandbox=", frame)
            self.assertNotIn("allow-same-origin", frame)


if __name__ == "__main__":
    unittest.main()
