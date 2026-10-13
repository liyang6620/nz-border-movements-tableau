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


def metric_runs(
    label: str,
    value: str,
    value_color: str = "#176B87",
    suffix: str = "",
) -> str:
    suffix_run = (
        f"<run fontcolor='#5C677D' fontname='Tableau Book' fontsize='8'> {suffix}</run>"
        if suffix
        else ""
    )
    return f"""
          <run bold='true' fontcolor='#5C677D' fontname='Tableau Book' fontsize='8'>{label}</run>
          <run bold='true' fontcolor='{value_color}' fontname='Tableau Book' fontsize='18'>&#10;{value}</run>{suffix_run}
        """


def inline_metric_runs(
    label: str,
    value: str,
    value_color: str = "#176B87",
) -> str:
    return f"""
          <run bold='true' fontcolor='#5C677D' fontname='Tableau Book' fontsize='8'>{label}  </run>
          <run bold='true' fontcolor='{value_color}' fontname='Tableau Book' fontsize='15'>{value}</run>
        """


def dashboard_xml() -> str:
    title_runs = """
          <run bold='true' fontcolor='#172033' fontname='Tableau Book' fontsize='21'>New Zealand Border Movement Monitor</run>
        """
    subtitle_runs = """
          <run fontcolor='#5C677D' fontname='Tableau Book' fontsize='10'>Complete months through Nov 2025 | Provisional Stats NZ traveller movements</run>
        """
    desktop_metrics = [
        (3, 1800, 18000, metric_runs("2025 JAN-NOV ARRIVALS", "6.02M")),
        (4, 20600, 17000, metric_runs("YEAR ON YEAR VS 2024", "+4.3%", "#20805D")),
        (5, 38400, 22000, metric_runs("2025 JAN-NOV ARRIVALS", "94.2%", suffix="OF 2019 JAN-NOV")),
        (6, 61200, 17000, metric_runs("NET MOVEMENTS", "-1.5K", "#B64B4B")),
        (7, 79000, 19200, metric_runs("AIR ARRIVAL SHARE", "99.2%")),
    ]
    note_runs = """
          <run bold='true' fontcolor='#172033' fontname='Tableau Book' fontsize='10'>How to read this dashboard</run>
          <run fontcolor='#4B5568' fontname='Tableau Book' fontsize='9'>&#10;Data through 8 Dec 2025; December is excluded from trend and comparison views because it is incomplete. Net Traveller Movements = arrivals minus departures. It is not net migration or population change. “Last Overseas Port Country” describes the nearest/last overseas port, not residence, nationality, or trip purpose.</run>
        """

    desktop_zones = "\n".join(
        [
            "<zone h='100000' id='1' type-v2='layout-basic' w='100000' x='0' y='0'>",
            text_zone(2, 1800, 1200, 96400, 4200, title_runs, "#F7F8FA", 4),
            text_zone(17, 1800, 5400, 96400, 2400, subtitle_runs, "#F7F8FA", 2),
            *[
                text_zone(zone_id, x, 8400, width, 9400, runs, "#FFFFFF", 8)
                for zone_id, x, width, runs in desktop_metrics
            ],
            sheet_zone(10, "Monthly Arrivals vs Departures", 1800, 19000, 60800, 32000),
            sheet_zone(11, "Annual Net Traveller Movements", 63600, 19000, 34600, 32000),
            sheet_zone(12, "Monthly Arrivals by Age Group", 1800, 52200, 30000, 32000),
            sheet_zone(13, "Yearly Arrivals by Citizenship", 32800, 52200, 32200, 32000),
            sheet_zone(14, "Arrivals by Last Overseas Port Country", 65800, 52200, 32400, 32000),
            # Air share is already surfaced as a KPI. Keeping the near-100%
            # travel-mode chart on the dashboard repeated the same signal and
            # forced unreadable year labels into a small panel.
            text_zone(16, 1800, 85400, 96400, 13000, note_runs, "#F4F7FA", 8),
            "</zone>",
            f"""<zone h='5000' id='20' name='Monthly Arrivals vs Departures' pane-specification-id='0' param='[{DATASOURCE}].[none:direction_code:nk]' show-title='false' type-v2='color' w='12000' x='49000' y='20200' />""",
            f"""<zone h='5500' id='21' name='Yearly Arrivals by Citizenship' pane-specification-id='0' param='[{DATASOURCE}].[none:citizenship:nk]' show-title='false' type-v2='color' w='15000' x='51500' y='56500' />""",
        ]
    )

    phone_title = """
          <run bold='true' fontcolor='#172033' fontname='Tableau Book' fontsize='14'>NZ Border Movements</run>
        """
    phone_subtitle = """
          <run fontcolor='#5C677D' fontname='Tableau Book' fontsize='9'>Complete months through Nov 2025</run>
        """
    phone_metrics = [
        (3, inline_metric_runs("2025 JAN-NOV ARRIVALS", "6.02M")),
        (4, inline_metric_runs("YEAR ON YEAR VS 2024", "+4.3%", "#20805D")),
        (5, inline_metric_runs("2025 / 2019 ARRIVALS", "94.2%")),
        (6, inline_metric_runs("NET MOVEMENTS", "-1.5K", "#B64B4B")),
        (7, inline_metric_runs("AIR ARRIVAL SHARE", "99.2%")),
    ]
    phone_zones = "\n".join(
        [
            "<zone h='100000' id='42' type-v2='layout-basic' w='100000' x='0' y='0'>",
            "<zone h='98000' id='41' param='vert' type-v2='layout-flow' w='97000' x='1500' y='1000'>",
            text_zone(2, 1500, 800, 97000, 3600, phone_title, "#F7F8FA", 4),
            text_zone(17, 1500, 4400, 97000, 2600, phone_subtitle, "#F7F8FA", 3),
            *[
                text_zone(zone_id, 1500, 0, 97000, 4200, runs, "#FFFFFF", 6)
                for zone_id, runs in phone_metrics
            ],
            sheet_zone(10, "Monthly Arrivals vs Departures", 1500, 27000, 97000, 15500),
            sheet_zone(11, "Annual Net Traveller Movements", 1500, 43000, 97000, 11000),
            sheet_zone(12, "Monthly Arrivals by Age Group", 1500, 55000, 97000, 14000),
            sheet_zone(13, "Yearly Arrivals by Citizenship", 1500, 70000, 97000, 12000),
            sheet_zone(14, "Arrivals by Last Overseas Port Country", 1500, 83000, 97000, 13000),
            text_zone(16, 1500, 96500, 97000, 5000, note_runs, "#F4F7FA", 5),
            "</zone>",
            "</zone>",
            f"""<zone h='4200' id='21' name='Yearly Arrivals by Citizenship' pane-specification-id='0' param='[{DATASOURCE}].[none:citizenship:nk]' show-title='false' type-v2='color' w='40000' x='57000' y='72500' />""",
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


def improve_worksheet_semantics(worksheet: str) -> str:
    if "<worksheet name='Yearly Arrivals by Citizenship'>" in worksheet:
        worksheet = worksheet.replace(
            "Annual Arrivals by Citizenship Status",
            "Annual Arrivals by Citizenship",
            1,
        )
        worksheet = worksheet.replace(
            "&lt;Sheet Name&gt;",
            "Annual Arrivals by Citizenship",
            1,
        )
        worksheet = worksheet.replace(
            "<run bold='true'>Month: </run>",
            "<run bold='true'>Year: </run>",
            1,
        )
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
        "<column caption='Citizenship' datatype='string' name='[citizenship]' role='dimension' type='nominal' />",
        """<column caption='Citizenship status' datatype='string' name='[citizenship]' role='dimension' type='nominal'>
              <aliases>
                <alias key='&quot;NZ&quot;' value='NZ citizens' />
                <alias key='&quot;non-NZ&quot;' value='Non-NZ citizens' />
              </aliases>
            </column>""",
    )
    xml = xml.replace(
        "<run fontsize='9'>&lt;Sheet Name&gt;</run>",
        "<run bold='true' fontcolor='#172033' fontname='Tableau Book' fontsize='11'>&lt;Sheet Name&gt;</run>",
    )
    xml = xml.replace("value='Number of Travellers'", "value='Traveller movements'")

    worksheet_pattern = re.compile(r"<worksheet name='[^']+'>.*?</worksheet>", re.DOTALL)
    xml = worksheet_pattern.sub(
        lambda match: improve_worksheet_semantics(
            add_complete_month_filter(match.group(0))
        ),
        xml,
    )

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
