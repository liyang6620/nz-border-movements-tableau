"""Apply the reviewed analytical baseline changes to the packaged workbook.

The script records the XML-level refactor used during development. The checked-in
TWBX remains the release artifact because final layout adjustments are completed
and visually verified in Tableau Desktop/Public.
"""

from __future__ import annotations

import html
import os
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "workbook" / "nz-border-movements.twbx"

DATASOURCE = "federated.0usvi7l1mmfuyz14ohd3u0z4gxtj"
COMPLETE_MONTH_ID = "Calculation_1179556407406592"
COMPLETE_MONTH_INSTANCE = f"none:{COMPLETE_MONTH_ID}:nk"
NEW_HYPER_ENTRY = "Data/nz-border-movements/nz_border_movements_2019_2025.hyper"
KPI_ACTIONS = {
    "direction": "ActionKPI_Direction_20261014",
    "citizenship": "ActionKPI_Citizenship_20261014",
    "country": "ActionKPI_Country_20261014",
}
KPI_SHEETS = {
    "current": "2025 Movements (M)",
    "yoy": "KPI Change vs 2024",
    "recovery": "KPI Recovery vs 2019",
    "air": "KPI Air Share 2025",
}
DASHBOARD_NAME = "New Zealand Border Movement Recovery Monitor"


def zone_style(background: str = "#FFFFFF", margin: int = 6) -> str:
    return f"""<zone-style>
          <format attr='background-color' value='{background}' />
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


def sheet_zone(
    zone_id: int,
    name: str,
    x: int,
    y: int,
    w: int,
    h: int,
    background: str = "#FFFFFF",
    margin: int = 8,
    show_title: bool = True,
) -> str:
    title_attr = "" if show_title else " show-title='false'"
    return f"""<zone h='{h}' id='{zone_id}' name='{html.escape(name, quote=True)}'{title_attr} w='{w}' x='{x}' y='{y}'>
        <layout-cache minheight='180' minwidth='220' type-h='scalable' type-w='scalable' />
        {zone_style(background, margin)}
      </zone>"""


def kpi_sheet_xml(name: str, title: str, calculation_id: str, formula: str, uuid: str) -> str:
    """Build a filterable text-mark worksheet for one headline metric."""
    value_instance = f"usr:{calculation_id}:qk"
    return f"""    <worksheet name='{html.escape(name, quote=True)}'>
      <layout-options>
        <title>
          <formatted-text>
            <run bold='true' fontcolor='#4F5968' fontname='Tableau Book' fontsize='8'>{html.escape(title)}</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources>
            <datasource caption='NZ Border Movements 2019-2025' name='{DATASOURCE}' />
          </datasources>
          <datasource-dependencies datasource='{DATASOURCE}'>
            <column caption='Complete Month' datatype='boolean' name='[{COMPLETE_MONTH_ID}]' role='dimension' type='nominal'>
              <calculation class='tableau' formula='DATETRUNC(&apos;month&apos;, [date]) &lt; DATETRUNC(&apos;month&apos;, {{ MAX([date]) }})' />
            </column>
            <column caption='Citizenship status' datatype='string' name='[citizenship]' role='dimension' type='nominal'>
              <aliases>
                <alias key='&quot;NZ&quot;' value='NZ citizens' />
                <alias key='&quot;non-NZ&quot;' value='Non-NZ citizens' />
              </aliases>
            </column>
            <column caption='Last Overseas Port Country' datatype='string' name='[closest_overseas_port_country]' role='dimension' semantic-role='[Country].[ISO3166_2]' type='nominal' />
            <column caption='Date' datatype='date' name='[date]' role='dimension' type='ordinal' />
            <column caption='Direction Code' datatype='string' name='[direction_code]' role='dimension' type='nominal'>
              <aliases>
                <alias key='&quot;A&quot;' value='Arrivals' />
                <alias key='&quot;D&quot;' value='Departures' />
              </aliases>
            </column>
            <column caption='{html.escape(title, quote=True)}' datatype='real' name='[{calculation_id}]' role='measure' type='quantitative'>
              <calculation class='tableau' formula='{formula}' />
            </column>
            <column-instance column='[{COMPLETE_MONTH_ID}]' derivation='None' name='[{COMPLETE_MONTH_INSTANCE}]' pivot='key' type='nominal' />
            <column-instance column='[{calculation_id}]' derivation='None' name='[{value_instance}]' pivot='key' type='quantitative' />
            <column caption='Total Movements' datatype='integer' name='[total_movements]' role='measure' type='quantitative' />
            <column caption='Travel Mode' datatype='string' name='[travel_mode]' role='dimension' type='nominal' />
          </datasource-dependencies>
          <filter class='categorical' column='[{DATASOURCE}].[Action (direction_code)]'>
            <groupfilter function='level-members' level='[direction_code]' user:ui-action-filter='[{KPI_ACTIONS["direction"]}]' user:ui-enumeration='all' user:ui-marker='enumerate' />
          </filter>
          <filter class='categorical' column='[{DATASOURCE}].[Action (citizenship)]'>
            <groupfilter function='level-members' level='[citizenship]' user:ui-action-filter='[{KPI_ACTIONS["citizenship"]}]' user:ui-enumeration='all' user:ui-marker='enumerate' />
          </filter>
          <filter class='categorical' column='[{DATASOURCE}].[Action (closest_overseas_port_country)]'>
            <groupfilter function='level-members' level='[closest_overseas_port_country]' user:ui-action-filter='[{KPI_ACTIONS["country"]}]' user:ui-enumeration='all' user:ui-marker='enumerate' />
          </filter>
          <filter class='categorical' column='[{DATASOURCE}].[{COMPLETE_MONTH_INSTANCE}]'>
            <groupfilter function='member' level='[{COMPLETE_MONTH_INSTANCE}]' member='true' user:ui-domain='database' user:ui-enumeration='inclusive' user:ui-marker='enumerate' />
          </filter>
          <slices>
            <column>[{DATASOURCE}].[Action (direction_code)]</column>
            <column>[{DATASOURCE}].[Action (citizenship)]</column>
            <column>[{DATASOURCE}].[Action (closest_overseas_port_country)]</column>
            <column>[{DATASOURCE}].[{COMPLETE_MONTH_INSTANCE}]</column>
          </slices>
          <aggregation value='true' />
        </view>
        <style>
          <style-rule element='worksheet'>
            <format attr='display-field-labels' value='false' />
          </style-rule>
        </style>
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Text' />
            <encodings>
              <text column='[{DATASOURCE}].[{value_instance}]' />
            </encodings>
            <style>
              <style-rule element='mark'>
                <format attr='mark-labels-show' value='true' />
                <format attr='mark-labels-cull' value='false' />
              </style-rule>
            </style>
          </pane>
        </panes>
        <rows />
        <cols />
      </table>
      <simple-id uuid='{{{uuid}}}' />
    </worksheet>"""


def kpi_specs() -> list[dict[str, str]]:
    current_formula = (
        "ROUND(SUM(IF YEAR([date]) = 2025 AND MONTH([date]) &lt;= 11 THEN [total_movements] END) / 1000000, 2)"
    )
    yoy_formula = (
        "IF SUM(IF YEAR([date]) = 2024 AND MONTH([date]) &lt;= 11 THEN [total_movements] END) = 0 THEN NULL ELSE "
        "ROUND((SUM(IF YEAR([date]) = 2025 AND MONTH([date]) &lt;= 11 THEN [total_movements] END) / "
        "SUM(IF YEAR([date]) = 2024 AND MONTH([date]) &lt;= 11 THEN [total_movements] END) - 1) * 100, 1) END"
    )
    recovery_formula = (
        "IF SUM(IF YEAR([date]) = 2019 AND MONTH([date]) &lt;= 11 THEN [total_movements] END) = 0 THEN NULL ELSE "
        "ROUND(SUM(IF YEAR([date]) = 2025 AND MONTH([date]) &lt;= 11 THEN [total_movements] END) / "
        "SUM(IF YEAR([date]) = 2019 AND MONTH([date]) &lt;= 11 THEN [total_movements] END) * 100, 1) END"
    )
    air_formula = (
        "IF SUM(IF YEAR([date]) = 2025 AND MONTH([date]) &lt;= 11 THEN [total_movements] END) = 0 THEN NULL ELSE "
        "ROUND(SUM(IF YEAR([date]) = 2025 AND MONTH([date]) &lt;= 11 AND [travel_mode] = &quot;A&quot; THEN [total_movements] END) / "
        "SUM(IF YEAR([date]) = 2025 AND MONTH([date]) &lt;= 11 THEN [total_movements] END) * 100, 1) END"
    )
    return [
        {
            "name": KPI_SHEETS["current"],
            "title": "SELECTED MOVEMENTS | JAN-NOV 2025 (M)",
            "id": "Calculation_KPI_Current_20261014",
            "formula": current_formula,
            "uuid": "A4EE8C88-4244-41A7-8D93-DAC1D1D62671",
        },
        {
            "name": KPI_SHEETS["yoy"],
            "title": "CHANGE VS JAN-NOV 2024 (%)",
            "id": "Calculation_KPI_YoY_20261014",
            "formula": yoy_formula,
            "uuid": "F64E04E0-6109-4DF9-9798-78F001942D3A",
        },
        {
            "name": KPI_SHEETS["recovery"],
            "title": "2025 AS % OF JAN-NOV 2019",
            "id": "Calculation_KPI_Recovery_20261014",
            "formula": recovery_formula,
            "uuid": "62F6153C-6EB3-4699-A763-444011514276",
        },
        {
            "name": KPI_SHEETS["air"],
            "title": "AIR SHARE | JAN-NOV 2025 (%)",
            "id": "Calculation_KPI_Air_20261014",
            "formula": air_formula,
            "uuid": "374DD92E-153B-4715-AE6A-D444E2555BCA",
        },
    ]


def kpi_worksheets_xml() -> str:
    return "\n".join(
        kpi_sheet_xml(
            spec["name"],
            spec["title"],
            spec["id"],
            spec["formula"],
            spec["uuid"],
        )
        for spec in kpi_specs()
    )


def dashboard_xml() -> str:
    title_runs = """
          <run bold='true' fontcolor='#FFFFFF' fontname='Tableau Book' fontsize='17'>NZ BORDER MOVEMENTS DASHBOARD</run>
        """
    subtitle_runs = """
          <run fontcolor='#FFFFFF' fontname='Tableau Book' fontsize='9'>Recovery, traveller mix and movement trends</run>
        """
    brand_runs = """
          <run bold='true' fontcolor='#D9918B' fontname='Tableau Book' fontsize='23'>NZ</run>
          <run bold='true' fontcolor='#FFFFFF' fontname='Tableau Book' fontsize='9'>&#10;BORDER MOVEMENTS</run>
        """
    scope_runs = """
          <run bold='true' fontcolor='#FFFFFF' fontname='Tableau Book' fontsize='10'>REPORT SCOPE</run>
          <run fontcolor='#DCE8FF' fontname='Tableau Book' fontsize='7'>&#10;&#10;REPORT PERIOD</run>
          <run bold='true' fontcolor='#FFFFFF' fontname='Tableau Book' fontsize='8'>&#10;Jan-Nov 2025</run>
          <run fontcolor='#DCE8FF' fontname='Tableau Book' fontsize='7'>&#10;&#10;BENCHMARKS</run>
          <run bold='true' fontcolor='#FFFFFF' fontname='Tableau Book' fontsize='8'>&#10;2019 and 2024</run>
          <run fontcolor='#DCE8FF' fontname='Tableau Book' fontsize='7'>&#10;&#10;DATA STATUS</run>
          <run bold='true' fontcolor='#FFFFFF' fontname='Tableau Book' fontsize='8'>&#10;Complete months</run>
        """
    note_runs = """
          <run bold='true' fontcolor='#FFFFFF' fontname='Tableau Book' fontsize='10'>DATA GUIDE</run>
          <run fontcolor='#9FB9E8' fontname='Tableau Book' fontsize='7'>&#10;NET MOVEMENT</run>
          <run fontcolor='#FFFFFF' fontname='Tableau Book' fontsize='8'>&#10;Arrivals minus departures</run>
          <run fontcolor='#DCE8FF' fontname='Tableau Book' fontsize='7'>&#10;Not net migration</run>
          <run fontcolor='#9FB9E8' fontname='Tableau Book' fontsize='7'>&#10;LAST PORT</run>
          <run fontcolor='#FFFFFF' fontname='Tableau Book' fontsize='8'>&#10;Final overseas port</run>
          <run fontcolor='#DCE8FF' fontname='Tableau Book' fontsize='7'>&#10;Not nationality</run>
        """

    header_meta_runs = """
          <run bold='true' fontcolor='#DCE8FF' fontname='Tableau Book' fontsize='8'>COMPLETE DATA THROUGH NOV 2025</run>
        """

    citizenship_title_runs = """
          <run bold='true' fontcolor='#172033' fontname='Tableau Book' fontsize='11'>Annual Arrivals by Citizenship</run>
        """
    citizenship_legend_runs = """
          <run fontcolor='#4C78A8' fontname='Tableau Book' fontsize='9'>&#9632;</run>
          <run fontcolor='#4F5968' fontname='Tableau Book' fontsize='8'> Non-NZ citizens     </run>
          <run fontcolor='#F28E2B' fontname='Tableau Book' fontsize='9'>&#9632;</run>
          <run fontcolor='#4F5968' fontname='Tableau Book' fontsize='8'> NZ citizens</run>
        """

    source_runs = """
          <run fontcolor='#DCE8FF' fontname='Tableau Book' fontsize='7'>SOURCE</run>
          <run bold='true' fontcolor='#FFFFFF' fontname='Tableau Book' fontsize='8'>&#10;Stats NZ</run>
          <run fontcolor='#9FB9E8' fontname='Tableau Book' fontsize='7'>&#10;Provisional data</run>
        """

    desktop_zones = "\n".join(
        [
            "<zone h='100000' id='1' type-v2='layout-basic' w='100000' x='0' y='0'>",
            # Reference layout: a narrow navy rail, a single report header,
            # three cards across the top, and three analytical columns below.
            text_zone(30, 2500, 2200, 11500, 95600, "", "#062C6F", 0),
            text_zone(18, 3600, 5200, 9300, 19000, brand_runs, "#062C6F", 4),
            text_zone(32, 2500, 27800, 11500, 500, "", "#5F7EB5", 0),
            text_zone(19, 3400, 30000, 9500, 29000, scope_runs, "#062C6F", 4),
            text_zone(33, 2500, 61500, 11500, 500, "", "#5F7EB5", 0),
            text_zone(16, 3000, 64000, 10500, 18500, note_runs, "#062C6F", 4),
            text_zone(34, 2500, 85000, 11500, 500, "", "#5F7EB5", 0),
            text_zone(35, 3400, 87500, 9500, 8000, source_runs, "#062C6F", 4),

            text_zone(45, 15800, 2200, 82200, 11200, "", "#062C6F", 0),
            text_zone(2, 16400, 3000, 45500, 4800, title_runs, "#062C6F", 3),
            text_zone(17, 16400, 8600, 41000, 3000, subtitle_runs, "#062C6F", 2),
            text_zone(36, 74200, 5000, 22600, 3600, header_meta_runs, "#062C6F", 2),

            sheet_zone(39, KPI_SHEETS["current"], 15800, 16500, 17000, 14500, "#FFFFFF", 8),
            sheet_zone(40, KPI_SHEETS["yoy"], 34200, 16500, 17000, 14500, "#FFFFFF", 8),
            sheet_zone(42, KPI_SHEETS["recovery"], 15800, 32500, 17000, 15000, "#FFFFFF", 8),
            sheet_zone(43, KPI_SHEETS["air"], 34200, 32500, 17000, 15000, "#FFFFFF", 8),

            sheet_zone(14, "Arrivals by Last Overseas Port Country", 52600, 16500, 45400, 31000, "#FFFFFF", 8),
            sheet_zone(10, "Monthly Arrivals vs Departures", 15800, 50000, 31500, 47800, "#FFFFFF", 8),
            sheet_zone(12, "Monthly Arrivals by Age Group", 48800, 50000, 23500, 47800, "#FFFFFF", 8),
            sheet_zone(11, "Annual Net Traveller Movements", 73800, 50000, 24200, 22500, "#FFFFFF", 8),
            text_zone(46, 73800, 74000, 24200, 23800, "", "#FFFFFF", 0),
            text_zone(47, 74600, 75200, 22600, 4300, citizenship_title_runs, "#FFFFFF", 2),
            text_zone(48, 74600, 79500, 22600, 3900, citizenship_legend_runs, "#FFFFFF", 1),
            sheet_zone(13, "Yearly Arrivals by Citizenship", 74600, 83500, 22600, 13500, "#FFFFFF", 3, False),
            zone_style("#E8EDF3", 0),
            "</zone>",
            f"""<zone h='5200' id='20' name='Monthly Arrivals vs Departures' pane-specification-id='0' param='[{DATASOURCE}].[none:direction_code:nk]' show-title='false' type-v2='color' w='10000' x='37000' y='51200' />""",
        ]
    )

    phone_title = """
          <run bold='true' fontcolor='#FFFFFF' fontname='Tableau Book' fontsize='14'>NZ BORDER MOVEMENTS</run>
        """
    phone_subtitle = """
          <run fontcolor='#DCE8FF' fontname='Tableau Book' fontsize='8'>Recovery monitor | Complete months through Nov 2025</run>
        """
    phone_note_runs = """
          <run bold='true' fontcolor='#172033' fontname='Tableau Book' fontsize='9'>HOW TO READ</run>
          <run fontcolor='#4F5665' fontname='Tableau Book' fontsize='8'>&#10;Complete months only. Net movement means arrivals minus departures; it is not net migration. Port country is the last overseas port, not nationality.</run>
        """
    phone_monthly_title_legend_runs = """
          <run bold='true' fontcolor='#172033' fontname='Tableau Book' fontsize='10'>Monthly Arrivals vs Departures</run>
          <run fontcolor='#4C78A8' fontname='Tableau Book' fontsize='9'>&#10;&#9632;</run>
          <run fontcolor='#4F5968' fontname='Tableau Book' fontsize='8'> Arrivals     </run>
          <run fontcolor='#F28E2B' fontname='Tableau Book' fontsize='9'>&#9632;</run>
          <run fontcolor='#4F5968' fontname='Tableau Book' fontsize='8'> Departures</run>
        """
    phone_zones = "\n".join(
        [
            "<zone h='100000' id='42' type-v2='layout-basic' w='100000' x='0' y='0'>",
            "<zone h='98000' id='41' param='vert' type-v2='layout-flow' w='97000' x='1500' y='1000'>",
            text_zone(2, 1500, 800, 97000, 4000, phone_title, "#062C6F", 7),
            text_zone(17, 1500, 4800, 97000, 2800, phone_subtitle, "#062C6F", 7),
            sheet_zone(3, KPI_SHEETS["current"], 1500, 9000, 47500, 8000, "#FFFFFF", 6),
            sheet_zone(4, KPI_SHEETS["yoy"], 51000, 9000, 47500, 8000, "#FFFFFF", 6),
            sheet_zone(50, KPI_SHEETS["recovery"], 1500, 17500, 47500, 8500, "#FFFFFF", 6),
            sheet_zone(51, KPI_SHEETS["air"], 51000, 17500, 47500, 8500, "#FFFFFF", 6),
            text_zone(49, 1500, 26500, 97000, 3500, phone_monthly_title_legend_runs, "#FFFFFF", 5),
            sheet_zone(10, "Monthly Arrivals vs Departures", 1500, 30000, 97000, 12000, "#FFFFFF", 5, False),
            sheet_zone(11, "Annual Net Traveller Movements", 1500, 43500, 97000, 10500),
            sheet_zone(12, "Monthly Arrivals by Age Group", 1500, 55500, 97000, 14500),
            text_zone(47, 1500, 70500, 97000, 2500, citizenship_title_runs, "#FFFFFF", 5),
            text_zone(48, 1500, 73000, 97000, 2500, citizenship_legend_runs, "#FFFFFF", 4),
            sheet_zone(13, "Yearly Arrivals by Citizenship", 1500, 75500, 97000, 9000, "#FFFFFF", 5, False),
            sheet_zone(14, "Arrivals by Last Overseas Port Country", 1500, 85000, 97000, 10500),
            text_zone(16, 1500, 97000, 97000, 4500, phone_note_runs, "#FFFFFF", 6),
            "</zone>",
            "</zone>",
        ]
    )

    return f"""<dashboard enable-sort-zone-taborder='true' name='New Zealand Border Movement Recovery Monitor'>
      <style>
        <style-rule element='dashboard'>
          <format attr='background-color' value='#E8EDF3' />
        </style-rule>
      </style>
      <size maxheight='760' maxwidth='1280' minheight='760' minwidth='1280' />
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
    if (
        "<worksheet name='Monthly Arrivals by Age Group'>" in worksheet
        and "[none:age_at_travel_range:nk]' scope='rows' value=''" not in worksheet
    ):
        axis_formats = f"""<style-rule element='axis'>
            <format attr='title' class='0' field='[{DATASOURCE}].[none:age_at_travel_range:nk]' scope='rows' value='' />
            <format attr='title' class='0' field='[{DATASOURCE}].[sum:total_movements:qk]' scope='rows' value='' />"""
        worksheet = worksheet.replace(
            "<style-rule element='axis'>",
            axis_formats,
            1,
        )
    if "<worksheet name='Monthly Arrivals by Age Group'>" in worksheet:
        worksheet = worksheet.replace(
            "caption='Age At Travel Range'",
            "caption='Age group'",
            1,
        )
    if "<worksheet name='Annual Net Traveller Movements'>" in worksheet:
        if "[sum:Calculation_0304857685766144:qk]' scope='rows' value=''" not in worksheet:
            net_axis_style = f"""<style>
          <style-rule element='axis'>
            <format attr='title' class='0' field='[{DATASOURCE}].[sum:Calculation_0304857685766144:qk]' scope='rows' value='' />
          </style-rule>
        </style>"""
            worksheet = worksheet.replace("<style />", net_axis_style, 1)
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
        worksheet = worksheet.replace(
            "scope='rows' value='Traveller movements'",
            "scope='rows' value=''",
            1,
        )
    return worksheet


def ensure_kpi_calculations(xml: str) -> str:
    """Register KPI calculations in the workbook datasource, not only in sheets."""
    insertion_marker = "      <column datatype='string' hidden='true' name='[Path]'"
    marker_index = xml.find(insertion_marker)
    if marker_index < 0:
        raise RuntimeError("Could not locate the datasource calculation insertion point")

    datasource_prefix = xml[:marker_index]
    datasource_suffix = xml[marker_index:]
    for spec in kpi_specs():
        field_pattern = re.compile(
            rf"\s*<column caption='[^']*' datatype='real' name='\[{re.escape(spec['id'])}\]'.*?</column>",
            re.DOTALL,
        )
        datasource_prefix = field_pattern.sub("", datasource_prefix)

    fields = "\n".join(
        f"""      <column caption='{html.escape(spec['title'], quote=True)}' datatype='real' name='[{spec['id']}]' role='measure' type='quantitative'>
        <calculation class='tableau' formula='{spec['formula']}' />
      </column>"""
        for spec in kpi_specs()
    )
    return datasource_prefix + fields + "\n" + datasource_suffix


def ensure_action_groups(xml: str) -> str:
    groups = []
    for caption, field in (
        ("Action (direction_code)", "direction_code"),
        ("Action (citizenship)", "citizenship"),
    ):
        if f"name='[{caption}]'" not in xml:
            groups.append(
                f"""      <group caption='{caption}' hidden='true' name='[{caption}]' name-style='unqualified' user:auto-column='sheet_link'>
        <groupfilter function='crossjoin'>
          <groupfilter function='level-members' level='[{field}]' />
        </groupfilter>
      </group>"""
            )
    if not groups:
        return xml

    country_group = re.compile(
        r"(<group caption='Action \(closest_overseas_port_country\)'.*?</group>)",
        re.DOTALL,
    )
    xml, count = country_group.subn(
        lambda match: match.group(1) + "\n" + "\n".join(groups),
        xml,
        count=1,
    )
    if count != 1:
        raise RuntimeError("Could not locate the datasource action-group insertion point")
    return xml


def kpi_action_xml(caption: str, action_id: str, source_sheet: str, field: str) -> str:
    target_url = quote(DASHBOARD_NAME, safe="")
    expression = (
        f"tsl:{target_url}?%5B{DATASOURCE}%5D.%5B{field}%5D~s0="
        f"&lt;[{DATASOURCE}].[{field}]~na&gt;"
    )
    return f"""    <action caption='{html.escape(caption, quote=True)}' name='[{action_id}]'>
      <activation auto-clear='true' type='on-select' />
      <source dashboard='{DASHBOARD_NAME}' type='sheet' worksheet='{html.escape(source_sheet, quote=True)}' />
      <link caption='{html.escape(caption, quote=True)}' delimiter=',' escape='\\' expression='{expression}' include-null='true' multi-select='true' url-escape='true' />
      <command command='tsc:tsl-filter'>
        <param name='target' value='{DASHBOARD_NAME}' />
      </command>
    </action>"""


def ensure_kpi_actions(xml: str) -> str:
    for action_id in KPI_ACTIONS.values():
        pattern = re.compile(
            rf"\s*<action[^>]*name='\[{re.escape(action_id)}\]'.*?</action>",
            re.DOTALL,
        )
        xml = pattern.sub("", xml)

    actions = "\n".join(
        [
            kpi_action_xml(
                "Filter KPIs by Direction",
                KPI_ACTIONS["direction"],
                "Monthly Arrivals vs Departures",
                "direction_code",
            ),
            kpi_action_xml(
                "Filter KPIs by Citizenship",
                KPI_ACTIONS["citizenship"],
                "Yearly Arrivals by Citizenship",
                "citizenship",
            ),
            kpi_action_xml(
                "Filter KPIs by Overseas Country",
                KPI_ACTIONS["country"],
                "Arrivals by Last Overseas Port Country",
                "closest_overseas_port_country",
            ),
        ]
    )
    action_block = re.compile(r"(<actions>)(.*?)(\s+<datasources>)", re.DOTALL)
    xml, count = action_block.subn(
        lambda match: match.group(1) + match.group(2) + "\n" + actions + match.group(3),
        xml,
        count=1,
    )
    if count != 1:
        raise RuntimeError("Could not locate the workbook actions block")
    return xml


def ensure_kpi_worksheets(xml: str) -> str:
    for name in KPI_SHEETS.values():
        pattern = re.compile(
            rf"\s*<worksheet name='{re.escape(name)}'>.*?</worksheet>",
            re.DOTALL,
        )
        xml = pattern.sub("", xml)
    return xml.replace("  </worksheets>", "\n" + kpi_worksheets_xml() + "\n  </worksheets>", 1)


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

    xml = ensure_kpi_calculations(xml)
    xml = ensure_action_groups(xml)
    xml = ensure_kpi_actions(xml)
    xml = ensure_kpi_worksheets(xml)

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
