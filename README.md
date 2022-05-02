# [Tax-Revenue-Dashboard](https://dataviz.worldbank.org/views/TaxRevenueDashboard/TaxRevenueDashboard?:showAppBanner=false&&:display_count=n&&:showVizHome=n&&:origin=viz_share_link&&:embed=y&&:isGuestRedirectFromVizportal=y)
The Tax Revenue Dashboard is a tool for benchmarking tax policy performance. The dashboard aims to provide policymakers and researchers with necessary data and information to conduct a high-level analysis of a country's tax system. By using the dashboard, users can:
1. Benchmark a country’s tax performance against other countries
2. Analyze tax collection trends and tax structure
3. Compare a country’s performance with the average and best performer (tax capacity/tax gap)
4. Evaluate the performance of a country’s tax collection using the tax buoyancy of the major taxes
5. See trends in rates of major taxes
6. Compare the tax performance of regions and income groups

The dashboard will be expanded to include other relevant data such as C-efficiency, the corporate Marginal Effective Tax Rate (METR), and the corporate Average Effective Tax Rate (AETR), and tax incentives.

## Data sources and methodology
1. This dashboard uses the [GRD dataset from UNUWider](https://www.wider.unu.edu/project/grd-%E2%80%93-government-revenue-dataset) updated with data available from public websites of several countries’ Ministries of Finance.
2. Tax rates are sourced from [KPMG’s online dataset](https://home.kpmg/xx/en/home/services/tax/tax-tools-and-resources/tax-rates-online.html).
3. The potential (tax capacity) of a country is calculated by using the [Stochastic Frontier Analysis module from Stata](https://www.stata.com/manuals13/rfrontier.pdf) controlling for per capita GDP and the openness.

## Using the dashboard
Please download the [Tax Revenue Dashboard presentation](https://github.com/Revenue-Academy/Tax-Revenue-Dashboard/blob/main/Tax%20Revenue%20Dashboard%20-%20Final.pptx) to learn more about how you can use the dashboard and understand the interaction among various charts and dashboards. The code and data used in Tax Revenue Dashboard can be accessed at [World Bank Revenue Academy GitHub](https://github.com/Revenue-Academy/Tax-Revenue-Dashboard) page.

## Dashboard link
Click [here](https://dataviz.worldbank.org/views/TaxRevenueDashboard/TaxRevenueDashboard?:showAppBanner=false&:display_count=n&:showVizHome=n&:origin=viz_share_link&:embed=y&:isGuestRedirectFromVizportal=y) to access Tax Revenue Dashboard

## Files in this repository
- [Tax Revenue Dashboard - Final.pptx](https://github.com/Revenue-Academy/Tax-Revenue-Dashboard/blob/main/Tax%20Revenue%20Dashboard%20-%20Final.pptx): This file is includes training material on how to use the dashboard.
- [country_code_updated.xls](https://github.com/Revenue-Academy/Tax-Revenue-Dashboard/blob/main/country_code_updated.xls): This file contains country metadata like Income Group, Region, etc.
- [rev_tax_data2.rar](https://github.com/Revenue-Academy/Tax-Revenue-Dashboard/blob/main/rev_tax_data2.rar): This archive file contains a CSV file containing all the data used by Tableau dashboard.
- [tax_revenue_4_mar_2022.rar](https://github.com/Revenue-Academy/Tax-Revenue-Dashboard/blob/main/tax_revenue_4_mar_2022.rar): This archive file contains a Excel file containing the extracted and calculated data into a raw format.
- [rev_tax_v6_mobilelayouts.twb](https://github.com/Revenue-Academy/Tax-Revenue-Dashboard/blob/main/rev_tax_v6_mobilelayouts.twb): This file contains the whole Tableau workbook containing all the sheets and dashboard along with some additional calculations done within Tableau.
- [data.py](https://github.com/Revenue-Academy/Tax-Revenue-Dashboard/blob/main/data.py) and [clsTaxRevenueDashboard.py](https://github.com/Revenue-Academy/Tax-Revenue-Dashboard/blob/main/clsTaxRevenueDashboard.py): These two Python files are used to convert the data from Excel file inside "tax_revenue_4_mar_2022.rar" file (original format) to data in CSV format inside "rev_tax_data2.rar" file. These files also include some data transformation, and validation code to ensure data integrity. Currently we are using clsTaxRevenueDashboard.py file to convert the data from raw to final format. These Python source files also include some comments and other documentation on the use of various functions.
