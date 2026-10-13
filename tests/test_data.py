import unittest
from pathlib import Path

from tableauhyperapi import Connection, HyperProcess, TableName, Telemetry


ROOT = Path(__file__).resolve().parents[1]
HYPER = ROOT / "data" / "nz_border_movements_2019_2025.hyper"
TABLE = TableName("Extract", "Extract")


class HyperDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.process = HyperProcess(Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU)
        cls.connection = Connection(cls.process.endpoint, str(HYPER))

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()
        cls.process.close()

    def scalar(self, sql):
        return self.connection.execute_scalar_query(sql)

    def test_schema(self):
        definition = self.connection.catalog.get_table_definition(TABLE)
        fields = {str(column.name).strip('"') for column in definition.columns}
        expected = {
            "year", "month", "day", "date", "citizenship", "direction_code",
            "customs_port_code", "travel_mode", "closest_overseas_port_code",
            "closest_overseas_port_name", "closest_overseas_port_country",
            "sex_code", "age_at_travel_range", "total_movements",
        }
        self.assertEqual(fields, expected)

    def test_reviewed_baseline(self):
        row = self.connection.execute_list_query(
            f'SELECT MIN("date"), MAX("date"), COUNT(*), SUM("total_movements") FROM {TABLE}'
        )[0]
        self.assertEqual(str(row[0]), "2019-01-01")
        self.assertEqual(str(row[1]), "2025-12-08")
        self.assertEqual(row[2], 2_222_255)
        self.assertEqual(row[3], 60_866_193)

    def test_direction_domain_and_non_negative_movements(self):
        directions = {
            row[0]
            for row in self.connection.execute_list_query(
                f'SELECT DISTINCT "direction_code" FROM {TABLE}'
            )
        }
        self.assertEqual(directions, {"A", "D"})
        self.assertEqual(
            self.scalar(f'SELECT COUNT(*) FROM {TABLE} WHERE "total_movements" < 0'),
            0,
        )

    def test_latest_month_is_incomplete(self):
        max_date = str(self.scalar(f'SELECT MAX("date") FROM {TABLE}'))
        latest_month_days = self.scalar(
            f'''SELECT COUNT(DISTINCT "date") FROM {TABLE}
                WHERE DATE_TRUNC('month', "date") =
                      DATE_TRUNC('month', (SELECT MAX("date") FROM {TABLE}))'''
        )
        self.assertEqual(max_date, "2025-12-08")
        self.assertEqual(latest_month_days, 8)
        self.assertLess(latest_month_days, 28)

    def test_headline_metrics(self):
        query = f'''SELECT
            SUM(CASE WHEN "direction_code" = 'A' THEN "total_movements" ELSE 0 END),
            SUM(CASE WHEN "direction_code" = 'D' THEN "total_movements" ELSE 0 END),
            SUM(CASE WHEN "direction_code" = 'A' AND "travel_mode" = 'A' THEN "total_movements" ELSE 0 END)
          FROM {TABLE}
          WHERE "date" BETWEEN DATE '2025-01-01' AND DATE '2025-11-30' '''
        arrivals, departures, air_arrivals = self.connection.execute_list_query(query)[0]
        self.assertEqual(arrivals, 6_016_113)
        self.assertEqual(departures, 6_017_595)
        self.assertEqual(arrivals - departures, -1_482)
        self.assertAlmostEqual(air_arrivals / arrivals, 0.9923, places=4)


if __name__ == "__main__":
    unittest.main()
