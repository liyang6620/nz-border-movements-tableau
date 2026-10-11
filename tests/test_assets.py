import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AssetTests(unittest.TestCase):
    def test_packaged_workbook_is_valid(self):
        workbook = ROOT / "workbook" / "nz-border-movements.twbx"
        self.assertTrue(zipfile.is_zipfile(workbook))

        with zipfile.ZipFile(workbook) as archive:
            names = archive.namelist()
            self.assertTrue(any(name.lower().endswith(".twb") for name in names))
            self.assertTrue(any(name.lower().endswith(".hyper") for name in names))

    def test_dashboard_preview_exists(self):
        previews = list((ROOT / "screenshots").glob("*.png"))
        self.assertEqual(len(previews), 1)
        self.assertGreater(previews[0].stat().st_size, 100_000)


if __name__ == "__main__":
    unittest.main()
