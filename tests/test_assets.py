import hashlib
import struct
import unittest
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "workbook" / "nz-border-movements.twbx"
EXTERNAL_HYPER = ROOT / "data" / "nz_border_movements_2019_2025.hyper"
DASHBOARD_NAME = "New Zealand Border Movement Recovery Monitor"
KPI_SHEETS = {
    "2025 Movements (M)",
    "KPI Change vs 2024",
    "KPI Recovery vs 2019",
    "KPI Air Share 2025",
}
ANALYTICAL_SHEETS = {
    "Monthly Arrivals vs Departures",
    "Annual Net Traveller Movements",
    "Monthly Arrivals by Age Group",
    "Yearly Arrivals by Citizenship",
    "Arrivals by Travel Mode",
    "Arrivals by Last Overseas Port Country",
    "Monthly Arrivals Trend",
    "Share of Arrivals by Sex",
}


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
        cls.dashboard = cls.root.find(f"./dashboards/dashboard[@name='{DASHBOARD_NAME}']")
        if cls.dashboard is None:
            raise AssertionError(f"Missing target dashboard: {DASHBOARD_NAME}")

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
            *ANALYTICAL_SHEETS,
            *KPI_SHEETS,
        }
        self.assertTrue(expected.issubset(worksheet_names))

        size = self.dashboard.find("size")
        self.assertEqual((size.attrib["maxwidth"], size.attrib["maxheight"]), ("1280", "760"))
        desktop_sheet_names = {
            zone.attrib["name"]
            for zone in self.dashboard.findall("./zones//zone[@name]")
        }
        self.assertTrue(KPI_SHEETS.issubset(desktop_sheet_names))
        self.assertNotIn("Arrivals by Travel Mode", desktop_sheet_names)

    def test_complete_month_filter_is_on_analytical_worksheets(self):
        for name in ANALYTICAL_SHEETS:
            worksheet = self.root.find(f"./worksheets/worksheet[@name='{name}']")
            self.assertIsNotNone(worksheet, name)
            serialized = ET.tostring(worksheet, encoding="unicode")
            self.assertIn("Calculation_1179556407406592", serialized, name)
            self.assertIn('member="true"', serialized, name)

        for name in KPI_SHEETS:
            worksheet = self.root.find(f"./worksheets/worksheet[@name='{name}']")
            serialized = ET.tostring(worksheet, encoding="unicode")
            self.assertIn("MONTH([date]) &lt;= 11", serialized, name)

    def test_metric_names_and_definitions_are_safe(self):
        self.assertIn("Net Traveller Movements", self.twb_text)
        self.assertNotIn("Net Arrivals", self.twb_text)
        self.assertIn("Last Overseas Port Country", self.twb_text)
        self.assertIn("RECOVERY VS 2019", self.twb_text)
        self.assertIn("2025 TOTAL (M)", self.twb_text)
        self.assertIn("VS JAN-NOV 2024", self.twb_text)
        self.assertIn("Arrivals minus departures", self.twb_text)
        self.assertIn("NZ BORDER MOVEMENTS DASHBOARD", self.twb_text)
        self.assertIn("DATETRUNC(&apos;month&apos;", self.twb_text)
        self.assertIn("MONTH([date]) &lt;= 11", self.twb_text)

    def test_kpi_cards_are_filterable_worksheets(self):
        desktop_names = {
            zone.attrib.get("name") for zone in self.dashboard.findall("./zones//zone[@name]")
        }
        self.assertTrue(KPI_SHEETS.issubset(desktop_names))

        required_action_filters = {
            "Action (Direction Code)",
            "Action (Citizenship status)",
            "Action (Last Overseas Port Country)",
        }
        for name in KPI_SHEETS:
            worksheet = self.root.find(f"./worksheets/worksheet[@name='{name}']")
            filter_columns = {node.attrib.get("column", "") for node in worksheet.findall(".//filter")}
            for caption in required_action_filters:
                self.assertTrue(any(caption in column for column in filter_columns), f"{name}: {caption}")
            self.assertIsNotNone(worksheet.find(".//encodings/text"), name)

        actions = self.root.findall("./actions/action")
        actions_by_caption = {action.attrib.get("caption"): action for action in actions}
        expected_sources = {
            "Update KPIs from chart selection": "Monthly Arrivals vs Departures",
            "Filter by Overseas Country": "Arrivals by Last Overseas Port Country",
        }
        for caption, source_name in expected_sources.items():
            action = actions_by_caption[caption]
            self.assertEqual(action.find("activation").attrib.get("auto-clear"), "true")
            self.assertEqual(action.find("source").attrib.get("worksheet"), source_name)
            self.assertEqual(
                action.find("command/param[@name='target']").attrib.get("value"),
                DASHBOARD_NAME,
            )

        citizenship_action = actions_by_caption["Update KPIs by citizenship"]
        self.assertEqual(citizenship_action.find("activation").attrib.get("auto-clear"), "true")
        self.assertEqual(citizenship_action.find("source").attrib.get("dashboard"), DASHBOARD_NAME)
        self.assertEqual(
            citizenship_action.find("command/param[@name='target']").attrib.get("value"),
            DASHBOARD_NAME,
        )

    def test_citizenship_series_have_labels_and_legends(self):
        self.assertIn("Annual Arrivals by Citizenship", self.twb_text)
        self.assertIn("NZ citizens", self.twb_text)
        self.assertIn("Non-NZ citizens", self.twb_text)

        serialized = ET.tostring(self.dashboard, encoding="unicode")
        self.assertNotIn("none:citizenship:nk", serialized)

    def test_dashboard_zones_do_not_use_box_borders(self):
        bordered_zones = [
            zone
            for zone in self.dashboard.findall(".//zone")
            if zone.find("./zone-style/format[@attr='border-width']") is not None
            and zone.find("./zone-style/format[@attr='border-width']").attrib.get("value") != "0"
        ]
        self.assertEqual(bordered_zones, [])

    def test_dashboard_uses_reference_inspired_visual_hierarchy(self):
        serialized = ET.tostring(self.dashboard, encoding="unicode")
        self.assertIn("#E8EDF3", serialized)
        self.assertIn("#062c6f", serialized)
        self.assertIn("REPORT SCOPE", serialized)
        self.assertIn("2025 Movements (M)", serialized)
        self.assertIn("KPI Air Share 2025", serialized)
        self.assertIn("LAST PORT", serialized)
        self.assertIn("Not nationality", serialized)
        self.assertIn("COMPLETE DATA THROUGH NOV 2025", serialized)
        self.assertNotIn("OVERVIEW", serialized)
        self.assertNotIn("DEMOGRAPHICS", serialized)

        size = self.dashboard.find("./size")
        self.assertEqual(size.attrib["maxwidth"], "1280")
        self.assertEqual(size.attrib["maxheight"], "760")

        desktop = self.dashboard.find("./zones")
        white_surfaces = [
            zone
            for zone in desktop.findall(".//zone")
            if zone.find("./zone-style/format[@attr='background-color'][@value='#ffffff']")
            is not None
        ]
        self.assertGreaterEqual(len(white_surfaces), 7)

    def test_authored_phone_layout_exists(self):
        phone = self.dashboard.find("./devicelayouts/devicelayout[@name='Phone']")
        self.assertIsNotNone(phone)
        self.assertNotIn("auto-generated", phone.attrib)
        self.assertGreaterEqual(len(phone.findall(".//zone[@name]")), 5)
        size = phone.find("./size")
        self.assertEqual(size.attrib.get("maxheight"), "2600")
        self.assertEqual(size.attrib.get("sizing-mode"), "vscroll")
        phone_serialized = ET.tostring(phone, encoding="unicode")
        self.assertNotIn('type-v2="color"', phone_serialized)
        self.assertIn("Monthly Arrivals vs Departures", phone_serialized)
        self.assertIn("Departures", phone_serialized)

    def test_dashboard_screenshots_exist(self):
        expected_dimensions = {
            "dashboard-desktop.png": (1280, 760),
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
