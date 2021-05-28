# Investment_Portfolio_Analysis
This repository is useful to perform some financial analysis in Investment Portfolio.


------------------------------------------------------------------------------------------------------------------------------------

BASIC INSTALLATION:

1)  Install the Anaconda for Python 3.8:
    - https://www.anaconda.com/products/individual

2)  Open the Chrome Web Browser.

3)  Run the "Jupyter Notebook" application from "Windows -> Start Menu". Please, note that:
    - a "Jupyter Notebook" tab will be opened in Chrome Web Browser;
    - an "Anaconda Prompt Window" will be opened in your desktop; please, do not close it while working in the project.

4)  Adjust the "SOURCE_FILE_DIRECTORY" variable according to your desktop local folder.

5)  Try to run the script from "Jupyter Notebook" (Investment_Portfolio_Analysis.ipynb) in Chrome Web Browser.
5a) If some "XXXX module not found" error appears, try to install the "module" using the "pip" command in "Anaconda Prompt Window".
    Example:
    - "pandas module not found" -> pip install pandas
	- "datetime module not found" -> pip install datetime


------------------------------------------------------------------------------------------------------------------------------------

HOW IT WORKS:

1)  The following Excel files are available in a local directory ("SOURCE_FILE_DIRECTORY"), with monthly official data, from Jan/2000 to Apr/2021:
    - SELIC mensal.xlsx
    - CDI mensal.xlsx
    - IPCA mensal.xlsx
    - Poupança antiga mensal.xlsx
    - Poupança nova mensal.xlsx
    - FGTS mensal.xlsx

2)  When running the following example, it will be printed the "Total Profit" and the "Total Interest Rate" related to the specified period, when investing R$1000,00 in IPCA indexer.
    - Example: calcPrintTotalProfitValuesFromDate("IPCA", 1000, "2020-03-01", "2021-04-01")

3)  The data will be calculated taking in account the Excel spreadsheets data.


------------------------------------------------------------------------------------------------------------------------------------

DEFAULT EXPECTED RESULT:

When running the script with the default values, the following result will be printed:

	IPCA:
	Data Inicial: 2020-03-01
	Data Final: 2021-04-01
	Aporte Inicial: R$ 1000.00
	Taxa de Juros Total: 6.50%
	Juros Total: R$ 65.03
	Valor Final Total: R$ 1065.03

	SELIC:
	Data Inicial: 2020-03-01
	Data Final: 2021-04-01
	Aporte Inicial: R$ 1000.00
	Taxa de Juros Total: 2.77%
	Juros Total: R$ 27.75
	Valor Final Total: R$ 1027.75

	CDI:
	Data Inicial: 2020-03-01
	Data Final: 2021-04-01
	Aporte Inicial: R$ 1000.00
	Taxa de Juros Total: 2.78%
	Juros Total: R$ 27.82
	Valor Final Total: R$ 1027.82

	FGTS:
	Data Inicial: 2020-03-01
	Data Final: 2021-04-01
	Aporte Inicial: R$ 1000.00
	Taxa de Juros Total: 3.51%
	Juros Total: R$ 35.08
	Valor Final Total: R$ 1035.08

	Poupanca regra antiga:
	Data Inicial: 2020-03-01
	Data Final: 2021-04-01
	Aporte Inicial: R$ 1000.00
	Taxa de Juros Total: 7.23%
	Juros Total: R$ 72.32
	Valor Final Total: R$ 1072.32

	Poupanca regra nova:
	Data Inicial: 2020-03-01
	Data Final: 2021-04-01
	Aporte Inicial: R$ 1000.00
	Taxa de Juros Total: 2.00%
	Juros Total: R$ 19.98
	Valor Final Total: R$ 1019.98

	
------------------------------------------------------------------------------------------------------------------------------------
