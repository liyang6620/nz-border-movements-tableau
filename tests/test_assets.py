import hashlib
import struct
import unittest
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "workbook" / "nz-border-movements.twbx"
EXTERNAL_HYPER = ROOT / "data" / "nz_border_movements_2019_2025.hyper"


class WorkbookAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not zipfile.is_zipfile(WORKBOOK):
            raise AssertionError(f"Invalid packaged workbook: {WORKBOOK}")
        cls.archive = zipfile.ZipFile(WORKBOOK)
        twb_names = [name for name in cls.archive.namelist() if name.lower().endswith(".twb")]
        hyper_names = [name for name in cls.archive.namelist() if name.lower().endswith(".hyper")]
        if len(twb_names) != 1 or len(hyper_names) != 1:
            raise AssertionError("TWBX must contain exactly one TWB and one Hyper extract")
        cls.twb_name = twb_names[0]
        cls.hyper_name = hyper_names[0]
        cls.twb_bytes = cls.archive.read(cls.twb_name)
        cls.twb_text = cls.twb_bytes.decode("utf-8")
        cls.root = ET.fromstring(cls.twb_bytes)

    @classmethod
    def tearDownClass(cls):
        cls.archive.close()

    def test_packaged_extract_matches_validation_extract(self):
        packaged_hash = hashlib.sha256(self.archive.read(self.hyper_name)).hexdigest()
        external_hash = hashlib.sha256(EXTERNAL_HYPER.read_bytes()).hexdigest()
        self.assertEqual(packaged_hash, external_hash)

    def test_required_worksheets_and_dashboard_exist(self):
        worksheet_names = {node.attrib["name"] for node in self.root.findall("./worksheets/worksheet")}
        expected = {
            "Monthly Arrivals vs Departures",
            "Annual Net Traveller Movements",
            "Monthly Arrivals by Age Group",
            "Yearly Arrivals by Citizenship",
            "Arrivals by Travel Mode",
            "Arrivals by Last Overseas Port Country",
        }
        self.assertTrue(expected.issubset(worksheet_names))

        dashboard = self.root.find("./dashboards/dashboard")
        self.assertIsNotNone(dashboard)
        self.assertEqual(dashboard.attrib["name"], "New Zealand Border Movement Recovery Monitor")
        size = dashboard.find("size")
        self.assertEqual((size.attrib["maxwidth"], size.attrib["maxheight"]), ("1200", "900"))
        desktop_sheet_names = {
            zone.attrib["name"]
            for zone in dashboard.findall("./zones//zone[@name]")
        }
        self.assertNotIn("Arrivals by Travel Mode", desktop_sheet_names)

    def test_complete_month_filter_is_on_every_worksheet(self):
        worksheets = self.root.findall("./worksheets/worksheet")
        self.assertGreaterEqual(len(worksheets), 8)
        for worksheet in worksheets:
            serialized = ET.tostring(worksheet, encoding="unicode")
            self.assertIn("Calculation_1179556407406592", serialized, worksheet.attrib["name"])
            self.assertIn('member="true"', serialized, worksheet.attrib["name"])

    def test_metric_names_and_definitions_are_safe(self):
        self.assertIn("Net Traveller Movements", self.twb_text)
        self.assertNotIn("Net Arrivals", self.twb_text)
        self.assertIn("Last Overseas Port Country", self.twb_text)
        self.assertIn("OF 2019 JAN-NOV", self.twb_text)
        self.assertIn("2025 / 2019 ARRIVALS", self.twb_text)
        self.assertIn("New Zealand Border Movement Monitor", self.twb_text)
        self.assertNotIn(">          VS 2019  </run>", self.twb_text)
        self.assertIn("DATETRUNC(&apos;month&apos;", self.twb_text)

    def test_citizenship_series_have_labels_and_legends(self):
        self.assertIn("Annual Arrivals by Citizenship", self.twb_text)
        self.assertIn("NZ citizens", self.twb_text)
        self.assertIn("Non-NZ citizens", self.twb_text)

        dashboard = self.root.find("./dashboards/dashboard")
        citizenship_legends = [
            zone
            for zone in dashboard.findall(".//zone")
            if zone.attrib.get("type-v2") == "color"
            and "citizenship" in zone.attrib.get("param", "")
        ]
        self.assertGreaterEqual(len(citizenship_legends), 2)

    def test_authored_phone_layout_exists(self):
        phone = self.root.find("./dashboards/dashboard/devicelayouts/devicelayout")
        self.assertIsNotNone(phone)
        self.assertEqual(phone.attrib.get("name"), "Phone")
        self.assertNotIn("auto-generated", phone.attrib)
        self.assertGreaterEqual(len(phone.findall(".//zone[@name]")), 5)

    def test_dashboard_screenshots_exist(self):
        expected_dimensions = {
            "dashboard-desktop.png": (1200, 900),
            "dashboard-mobile.png": (375, 2600),
        }
        for filename, dimensions in expected_dimensions.items():
            screenshot = ROOT / "screenshots" / filename
            self.assertTrue(screenshot.exists(), filename)
            self.assertGreater(screenshot.stat().st_size, 50_000, filename)
            with screenshot.open("rb") as image:
                self.assertEqual(image.read(8), b"\x89PNG\r\n\x1a\n", filename)
                image.read(8)  # IHDR length and chunk type
                actual_dimensions = struct.unpack(">II", image.read(8))
            self.assertEqual(actual_dimensions, dimensions, filename)


if __name__ == "__main__":
    unittest.main()
