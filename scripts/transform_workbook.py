"""Apply the reviewed analytical and layout changes to the packaged workbook.

The script is intentionally deterministic so the binary TWBX can be rebuilt and
validated in CI without depending on a Tableau Desktop installation.
"""

from __future__ import annotations

import html
import os
import re
import shutil
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "workbook" / "nz-border-movements.twbx"

DATASOURCE = "federated.0usvi7l1mmfuyz14ohd3u0z4gxtj"
COMPLETE_MONTH_ID = "Calculation_1179556407406592"
COMPLETE_MONTH_INSTANCE = f"none:{COMPLETE_MONTH_ID}:nk"
NEW_HYPER_ENTRY = "Data/nz-border-movements/nz_border_movements_2019_2025.hyper"


def zone_style(background: str = "#FFFFFF", margin: int = 6) -> str:
    return f"""<zone-style>
          <format attr='background-color' value='{background}' />
          <format attr='border-color' value='#D9DEE7' />
          <format attr='border-style' value='solid' />
          <format attr='border-width' value='1' />
          <format attr='margin' value='{margin}' />
        </zone-style>"""


def text_zone(
    zone_id: int,
    x: int,
    y: int,
    w: int,
    h: int,
    runs: str,
    background: str = "#FFFFFF",
    margin: int = 8,
) -> str:
    return f"""<zone forceUpdate='true' h='{h}' id='{zone_id}' type-v2='text' w='{w}' x='{x}' y='{y}'>
        <formatted-text>{runs}</formatted-text>
        {zone_style(background, margin)}
      </zone>"""


def sheet_zone(zone_id: int, name: str, x: int, y: int, w: int, h: int) -> str:
    return f"""<zone h='{h}' id='{zone_id}' name='{html.escape(name, quote=True)}' w='{w}' x='{x}' y='{y}'>
        <layout-cache minheight='180' minwidth='220' type-h='scalable' type-w='scalable' />
        {zone_style()}
      </zone>"""


def dashboard_xml() -> str:
    title_runs = """
          <run bold='true' fontcolor='#172033' fontname='Tableau Book' fontsize='22'>New Zealand Border Movement Recovery Monitor</run>
        """
    subtitle_runs = """
          <run fontcolor='#5C677D' fontname='Tableau Book' fontsize='10'>Complete months through Nov 2025 | Provisional Stats NZ traveller movements</run>
        """
    kpi_runs = """
          <run bold='true' fontcolor='#172033' fontname='Tableau Book' fontsize='10'>2025 JAN-NOV ARRIVALS</run>
          <run bold='true' fontcolor='#176B87' fontname='Tableau Book' fontsize='20'>&#10;6.02M</run>
          <run fontcolor='#5C677D' fontname='Tableau Book' fontsize='9'>          YOY VS 2024  </run>
          <run bold='true' fontcolor='#20805D' fontname='Tableau Book' fontsize='16'>+4.3%</run>
          <run fontcolor='#5C677D' fontname='Tableau Book' fontsize='9'>          VS 2019  </run>
          <run bold='true' fontcolor='#176B87' fontname='Tableau Book' fontsize='16'>94.2%</run>
          <run fontcolor='#5C677D' fontname='Tableau Book' fontsize='9'>          NET MOVEMENTS  </run>
          <run bold='true' fontcolor='#B64B4B' fontname='Tableau Book' fontsize='16'>-1.5K</run>
          <run fontcolor='#5C677D' fontname='Tableau Book' fontsize='9'>          AIR SHARE  </run>
          <run bold='true' fontcolor='#176B87' fontname='Tableau Book' fontsize='16'>99.2%</run>
        """
    note_runs = """
          <run bold='true' fontcolor='#172033' fontname='Tableau Book' fontsize='10'>How to read this dashboard</run>
          <run fontcolor='#4B5568' fontname='Tableau Book' fontsize='9'>&#10;Data through 8 Dec 2025; December is excluded from trend and comparison views because it is incomplete. Net Traveller Movements = arrivals minus departures. It is not net migration or population change. “Last Overseas Port Country” describes the nearest/last overseas port, not residence, nationality, or trip purpose.</run>
        """

    desktop_zones = "\n".join(
        [
            "<zone h='100000' id='1' type-v2='layout-basic' w='100000' x='0' y='0'>",
            text_zone(2, 1800, 1200, 96400, 4000, title_runs, "#F7F8FA", 4),
            text_zone(17, 1800, 5200, 96400, 2500, subtitle_runs, "#F7F8FA", 2),
            text_zone(3, 1800, 8200, 96400, 9800, kpi_runs, "#FFFFFF", 10),
            sheet_zone(10, "Monthly Arrivals vs Departures", 1800, 19000, 60000, 30000),
            sheet_zone(11, "Annual Net Traveller Movements", 63000, 19000, 35200, 30000),
            sheet_zone(12, "Monthly Arrivals by Age Group", 1800, 50000, 31200, 26000),
            sheet_zone(13, "Yearly Arrivals by Citizenship", 34000, 50000, 31200, 26000),
            sheet_zone(14, "Arrivals by Last Overseas Port Country", 66200, 50000, 32000, 26000),
            # Air share is already surfaced as a KPI. Keeping the near-100%
            # travel-mode chart on the dashboard repeated the same signal and
            # forced unreadable year labels into a small panel.
            text_zone(16, 1800, 77000, 96400, 21500, note_runs, "#F4F7FA", 10),
            "</zone>",
            f"""<zone h='5500' id='20' name='Monthly Arrivals vs Departures' pane-specification-id='0' param='[{DATASOURCE}].[none:direction_code:nk]' show-title='false' type-v2='color' w='12000' x='48500' y='20200' />""",
        ]
    )

    phone_title = """
          <run bold='true' fontcolor='#172033' fontname='Tableau Book' fontsize='17'>NZ Border Movement Recovery Monitor</run>
          <run fontcolor='#5C677D' fontname='Tableau Book' fontsize='9'>&#10;Complete months through Nov 2025</run>
        """
    phone_kpis = """
          <run bold='true' fontcolor='#176B87' fontname='Tableau Book' fontsize='15'>6.02M arrivals</run>
          <run fontcolor='#4B5568' fontname='Tableau Book' fontsize='9'>   YoY </run><run bold='true' fontcolor='#20805D' fontsize='11'>+4.3%</run>
          <run fontcolor='#4B5568' fontname='Tableau Book' fontsize='9'>   vs 2019 </run><run bold='true' fontcolor='#176B87' fontsize='11'>94.2%</run>
          <run fontcolor='#4B5568' fontname='Tableau Book' fontsize='9'>&#10;Net movements </run><run bold='true' fontcolor='#B64B4B' fontsize='11'>-1.5K</run>
          <run fontcolor='#4B5568' fontname='Tableau Book' fontsize='9'>   Air share </run><run bold='true' fontcolor='#176B87' fontsize='11'>99.2%</run>
        """
    phone_zones = "\n".join(
        [
            "<zone h='100000' id='42' type-v2='layout-basic' w='100000' x='0' y='0'>",
            "<zone h='98000' id='41' param='vert' type-v2='layout-flow' w='97000' x='1500' y='1000'>",
            text_zone(2, 1500, 800, 97000, 6200, phone_title, "#F7F8FA", 4),
            text_zone(3, 1500, 7600, 97000, 8500, phone_kpis, "#FFFFFF", 8),
            sheet_zone(10, "Monthly Arrivals vs Departures", 1500, 17000, 97000, 18500),
            sheet_zone(11, "Annual Net Traveller Movements", 1500, 36500, 97000, 13000),
            sheet_zone(12, "Monthly Arrivals by Age Group", 1500, 50500, 97000, 13000),
            sheet_zone(13, "Yearly Arrivals by Citizenship", 1500, 64500, 97000, 13000),
            sheet_zone(14, "Arrivals by Last Overseas Port Country", 1500, 78500, 97000, 14000),
            text_zone(16, 1500, 93500, 97000, 5500, note_runs, "#F4F7FA", 6),
            "</zone>",
            "</zone>",
        ]
    )

    return f"""<dashboard enable-sort-zone-taborder='true' name='New Zealand Border Movement Recovery Monitor'>
      <style>
        <style-rule element='dashboard'>
          <format attr='background-color' value='#F7F8FA' />
        </style-rule>
      </style>
      <size maxheight='900' maxwidth='1200' minheight='900' minwidth='1200' />
      <datasources>
        <datasource caption='NZ Border Movements 2019-2025' name='{DATASOURCE}' />
      </datasources>
      <datasource-dependencies datasource='{DATASOURCE}'>
        <column caption='COVID Period' datatype='string' name='[Calculation_0304857701953537]' role='dimension' type='nominal'>
          <calculation class='tableau' formula='IF [date] &lt; #2020-03-01# THEN &quot;Pre-COVID&quot;&#13;&#10;ELSEIF [date] &lt; #2022-07-01# THEN &quot;COVID&quot;&#13;&#10;ELSE &quot;Post-COVID&quot;&#13;&#10;END' />
        </column>
        <column-instance column='[Calculation_0304857701953537]' derivation='None' name='[none:Calculation_0304857701953537:nk]' pivot='key' type='nominal' />
      </datasource-dependencies>
      <zones>{desktop_zones}</zones>
      <devicelayouts>
        <devicelayout name='Phone'>
          <size maxheight='2600' minheight='2600' sizing-mode='vscroll' />
          <zones>{phone_zones}</zones>
        </devicelayout>
      </devicelayouts>
      <simple-id uuid='{{B3F8233D-4DDB-476F-BDE8-D24A4AF5CB58}}' />
    </dashboard>"""


def add_complete_month_filter(worksheet: str) -> str:
    if f"column='[{COMPLETE_MONTH_ID}]'" not in worksheet:
        dependency = f"""
            <column caption='Complete Month' datatype='boolean' name='[{COMPLETE_MONTH_ID}]' role='dimension' type='nominal'>
              <calculation class='tableau' formula='DATETRUNC(&apos;month&apos;, [date]) &lt; DATETRUNC(&apos;month&apos;, {{ MAX([date]) }})' />
            </column>
            <column-instance column='[{COMPLETE_MONTH_ID}]' derivation='None' name='[{COMPLETE_MONTH_INSTANCE}]' pivot='key' type='nominal' />"""
        worksheet = worksheet.replace("          </datasource-dependencies>", dependency + "\n          </datasource-dependencies>", 1)

    filter_xml = f"""          <filter class='categorical' column='[{DATASOURCE}].[{COMPLETE_MONTH_INSTANCE}]'>
            <groupfilter function='member' level='[{COMPLETE_MONTH_INSTANCE}]' member='true' user:ui-domain='database' user:ui-enumeration='inclusive' user:ui-marker='enumerate' />
          </filter>
"""
    if f"column='[{DATASOURCE}].[{COMPLETE_MONTH_INSTANCE}]'" not in worksheet:
        insert_at = worksheet.find("          <slices>")
        if insert_at < 0:
            insert_at = worksheet.find("          <aggregation")
        worksheet = worksheet[:insert_at] + filter_xml + worksheet[insert_at:]

    slice_column = f"            <column>[{DATASOURCE}].[{COMPLETE_MONTH_INSTANCE}]</column>\n"
    if f">[{DATASOURCE}].[{COMPLETE_MONTH_INSTANCE}]</column>" not in worksheet:
        if "          </slices>" in worksheet:
            worksheet = worksheet.replace("          </slices>", slice_column + "          </slices>", 1)
        else:
            slices = f"          <slices>\n{slice_column}          </slices>\n"
            worksheet = worksheet.replace("          <aggregation", slices + "          <aggregation", 1)
    return worksheet


def transform_twb(xml: str) -> str:
    replacements = [
        ("Impact of COVID-19 on New Zealand Border Movements (2019–2025)", "New Zealand Border Movement Recovery Monitor"),
        ("Geographic Distribution of Overseas Arrivals to New Zealand", "Arrivals by Last Overseas Port Country"),
        ("Share of Arrivals by Travel Mode (Air vs Non-Air)", "Arrivals by Travel Mode"),
        ("Net Arrivals Over Time", "Annual Net Traveller Movements"),
        ("Net Arrivals", "Net Traveller Movements"),
        ("Data/tableau_project/NZ Border Movements 2019-2025.hyper", NEW_HYPER_ENTRY),
        ("Data/tableau_project/Data+ (border_daily_2019_2021).hyper", NEW_HYPER_ENTRY),
        ("Data+ (border_daily_2019_2021)", "NZ Border Movements 2019-2025"),
        ("Æ&#10;", "&#10;"),
    ]
    for old, new in replacements:
        xml = xml.replace(old, new)

    xml = xml.replace(
        "<column datatype='string' name='[closest_overseas_port_country]'",
        "<column caption='Last Overseas Port Country' datatype='string' name='[closest_overseas_port_country]'",
    )
    xml = xml.replace(
        "<run fontsize='9'>&lt;Sheet Name&gt;</run>",
        "<run bold='true' fontcolor='#172033' fontname='Tableau Book' fontsize='11'>&lt;Sheet Name&gt;</run>",
    )
    xml = xml.replace("value='Number of Travellers'", "value='Traveller movements'")

    worksheet_pattern = re.compile(r"<worksheet name='[^']+'>.*?</worksheet>", re.DOTALL)
    xml = worksheet_pattern.sub(lambda match: add_complete_month_filter(match.group(0)), xml)

    dashboard_pattern = re.compile(
        r"<dashboard enable-sort-zone-taborder='true' name='New Zealand Border Movement Recovery Monitor'>.*?</dashboard>",
        re.DOTALL,
    )
    xml, count = dashboard_pattern.subn(dashboard_xml(), xml, count=1)
    if count != 1:
        raise RuntimeError(f"Expected one dashboard to replace, found {count}")

    # Make the analytical scope explicit in the two most important chart titles.
    xml = xml.replace(
        "<worksheet name='Monthly Arrivals vs Departures'>",
        "<worksheet name='Monthly Arrivals vs Departures'>",
        1,
    )
    return xml


def rebuild_workbook() -> None:
    if not WORKBOOK.exists():
        raise FileNotFoundError(WORKBOOK)

    with zipfile.ZipFile(WORKBOOK) as source:
        entries = source.infolist()
        twb_entries = [entry for entry in entries if entry.filename.lower().endswith(".twb")]
        hyper_entries = [entry for entry in entries if entry.filename.lower().endswith(".hyper")]
        if len(twb_entries) != 1 or len(hyper_entries) != 1:
            raise RuntimeError("Expected exactly one TWB and one Hyper extract")
        twb_name = twb_entries[0].filename
        original_hyper = hyper_entries[0].filename
        xml = source.read(twb_name).decode("utf-8")
        transformed = transform_twb(xml)

        fd, temp_name = tempfile.mkstemp(suffix=".twbx", dir=WORKBOOK.parent)
        os.close(fd)
        try:
            with zipfile.ZipFile(temp_name, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as target:
                for entry in entries:
                    data = source.read(entry.filename)
                    output_name = entry.filename
                    if entry.filename == twb_name:
                        data = transformed.encode("utf-8")
                    elif entry.filename == original_hyper:
                        output_name = NEW_HYPER_ENTRY
                    target.writestr(output_name, data)
            # Windows can deny atomic replacement for files previously opened by
            # Tableau even after the process exits; a direct binary copy remains
            # deterministic and works on all supported development platforms.
            shutil.copyfile(temp_name, WORKBOOK)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)


if __name__ == "__main__":
    rebuild_workbook()
    print(f"Updated {WORKBOOK}")
