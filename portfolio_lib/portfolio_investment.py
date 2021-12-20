"""This file has a set of methods related to Portfolio/Extrato."""

import re
import sys

import pandas as pd
import requests
import yfinance as yf
from bs4 import BeautifulSoup


class PortfolioInvestment:
    """This is a class to manage all portfolio operations."""

    def __init__(self):
        """Create the PortfolioInvestment object."""
        self.fileOperations = None
        self.operations = None
        self.operationsYear = None
        self.current = None
        self.expected_title_list = [
            "Mercado",
            "Ticker",
            "Operação",
            "Data",
            "Rentabilidade Contratada",
            "Indexador",
            "Vencimento",
            "Quantidade",
            "Preço Unitário",
            "Preço Total",
            "Taxas",
            "IR",
            "Dividendos",
            "JCP",
            "Custo Total",
            "Notas",
        ]

    def getExpectedColumnsTitleList(self):
        """Return a list of expected column titles."""
        return self.expected_title_list

    def setFile(self, fileOperations):
        """Set the excel file related to the porfolio."""
        self.fileOperations = fileOperations

    def isValidFile(self):
        """Return if the excel portfolio file is valid or not."""
        valid_flag = True
        dataframe = pd.read_excel(self.fileOperations)
        # If some expected column is not present in the excel file
        # or the title line is empty in the excel file,
        # then the file is not valid
        if list(dataframe):
            for expected_title in self.expected_title_list:
                if expected_title not in dataframe:
                    valid_flag = False
                    break
        else:
            valid_flag = False
        return valid_flag

    def run(self):
        """Run the main routines related to the excel porfolio file."""
        # Dataframe with all the operations from the Excel file.
        self.operations = self.getExtrato()

        # 3 lists of number of operations by year. Suitable to be plot.
        self.operationsYear = self.numberOperationsYear()

        # Dataframe of the current portfolio. Suitable to be plot.
        self.current = self.currentPortfolio()

    def getExtrato(self):
        """Return the raw dataframe related to the excel porfolio file."""
        extrato = pd.read_excel(self.fileOperations)
        return extrato

    def overallTaxAndIncomes(self):
        """Return the sum of the fees, income tax, dividend and jcp."""
        fee = self.operations["Taxas"].sum()
        incomeTax = self.operations["IR"].sum()
        dividend = self.operations["Dividendos"].sum()
        jcp = self.operations["JCP"].sum()
        return fee, incomeTax, dividend, jcp

    def numberOperationsYear(self):
        """Return 3 lists containing the number of operations.

        The lists are linked between themselves according to the year.
        """
        dataframe = self.operations
        firstYear = dataframe["Data"].min()
        lastYear = dataframe["Data"].max()

        # Creates the empty lists
        listYear = []
        listBuy = []
        listSell = []
        janFirst = "-01-01"  # Auxiliary variable for the first day of the year
        decLast = "-12-31"  # Auxiliary variable for he last day of the year

        # Collects the number of operations per year
        if len(dataframe):
            for i in range(firstYear.year, lastYear.year + 1):
                start = str(i) + janFirst
                end = str(i) + decLast
                # Get filtered table according to the year
                filtered = dataframe[
                    (dataframe["Data"] >= start) & (dataframe["Data"] <= end)
                ]
                filteredBuy = filtered[(filtered["Operação"] == "Compra")]
                filteredSell = filtered[(filtered["Operação"] == "Venda")]
                # Add the values in the lists
                listYear.append(i)
                listBuy.append(len(filteredBuy.index))
                listSell.append(len(filteredSell.index))

        return listYear, listBuy, listSell

    def operationsByTicker(self, ticker):
        """Return a filtered dataframe according to the ticker.

        The input for the method is the file that holds the operations.
        The filter is done based on this file.
        """
        dataframe = self.operations[self.operations["Ticker"] == ticker]
        return dataframe

    def unitsTicker(self, ticker):
        """Return how many stocks of the given ticker."""
        # Filter the table by ticker
        dataframe = self.operationsByTicker(ticker)

        # Filter the table by buy operation
        buy = dataframe[dataframe["Operação"] == "Compra"]

        # Calculate the number of units bought
        buy = int(buy["Quantidade"].sum())

        # Filter the table by sell operation
        sell = dataframe[dataframe["Operação"] == "Venda"]

        # Calculate the number of units sold
        sell = int(sell["Quantidade"].sum())

        return buy, sell, buy - sell

    def tesouroSelic(self):
        """Return all operations related to Tesouro SELIC."""
        dataframe = self.operations[
            self.operations["Mercado"] == "Tesouro Direto",
        ]
        dataframe = dataframe[
            dataframe["Indexador"] == "SELIC",
        ]
        return dataframe

    def customTable(
        self,
        ticker,
        market,
        dueDate,
        profitability,
        index,
        operation,
    ):
        """Read the Excel file with all the operations.

        Return a filtered dataframe according with the desired parameters.
        """
        df = self.operations
        if ticker != "all":
            df = df[df["Ticker"] == ticker]
        if market != "all":
            df = df[df["Mercado"] == market]
        if dueDate != "NA":
            df = df[df["Vencimento"] == dueDate]
        if profitability != "NA":
            df = df[df["Rentabilidade Contratada"] == dueDate]
        if index != "all":
            df = df[df["Indexador"] == index]
        if operation != "all":
            df = df[df["Operação"] == operation]
        return df

    def customTableDate(
        self,
        ticker,
        market,
        dueDate,
        profitability,
        index,
        operation,
        startDate,
        endDate,
    ):
        """Read the Excel file with all the operations.

        Return a filtered dataframe according with the desired parameters
        and a certain time range.
        """
        dataframe = self.customTable(
            ticker, market, dueDate, profitability, index, operation
        )
        dataframe = dataframe[dataframe["Data"] >= startDate]
        dataframe = dataframe[dataframe["Data"] <= endDate]
        return dataframe

    def earningsByTicker(self, ticker):
        """Return the total earnings of a given ticker."""
        dataframe = self.operationsByTicker(ticker)
        dataframe = dataframe[dataframe["Operação"] == "Provento"]
        return float(dataframe["Dividendos"].sum() + dataframe["JCP"].sum())

    def avgPriceTicker(self, ticker):
        """Return the average price of a given ticker."""
        dataframe = self.operationsByTicker(ticker)

        # Fill with 0 the data that is not fullfilled in the dataframe.
        # It is important because non filled cells will return NaN,
        # which will cause calculation issues.
        dataframe = dataframe.fillna(0)

        avgPrice = 0
        avgPriceOld = 0
        qtStock = 0.0
        qtStockOld = 0.0
        costs = 0
        for index, row in dataframe.iterrows():
            # If the current operation is a buy event,
            # then update the average price
            if row["Operação"] == "Compra":
                # Get some useful data
                qtStock = row["Quantidade"]
                unitPrice = row["Preço Unitário"]
                costs = row["Taxas"] + row["IR"]

                # Calculate the average price of the operation
                avgPrice = (qtStock * unitPrice + costs) / qtStock

                # Calculate the average price considering also
                # the previous operations
                oldStockPrice = avgPriceOld * qtStockOld
                curStockPrice = avgPrice * qtStock
                qtStockTotal = qtStockOld + qtStock
                avgPrice = (oldStockPrice + curStockPrice) / qtStockTotal
                avgPriceOld = avgPrice
                qtStockOld += qtStock

            # If the current operation is a sell event,
            # then updates the number of stocks
            elif row["Operação"] == "Venda":
                qtStock -= row["Quantidade"]
                qtStockOld -= row["Quantidade"]

        # numberStocks = qtStockOld
        return avgPrice, qtStockOld

    def currentMarketPriceByTicker(self, ticker):
        """Return the last price of the stock."""
        # I had issues when downloading data for Fundos imobiliários.
        # It was necessary to work with period of 30d.
        # I believe that is mandatory period or start/end date.
        # With start/end I also had issues for reading the values.
        # The solution was to consider "30d" as the period.
        # I compared the results from function in Google and they were correct.
        dataframe = yf.download(ticker, period="30d")
        data = dataframe["Adj Close"].tail(1)
        return float(data)

    def currentMarketPriceByTickerList(self, list):
        """Return a dataframe with the last price of the stocks in the list."""
        dataframe = yf.download(list, period="1d")
        data = dataframe["Adj Close"].tail(1)

        # The 'tail' method returns a 'pandas.series'
        # when exists only 1 ticker in the variable 'list'.
        #
        # In order to solve the '1 ticker' case and return always
        # a 'pandas.dataframe' with the ticker name, we need to convert
        # the 'pandas.series' to a 'pandas.dataframe' and adjust its
        # column name.
        try:
            data = data.to_frame()
            if len(data) == 1:
                data = data.rename(columns={"Adj Close": list[0]})
        except AttributeError:
            data = data
        return data

    def sectorOfTicker(self, ticker):
        """Return the sector of a given ticker.

        The function uses the yfinance library to get the information.
        """
        ticker = ticker + ".SA"
        data = yf.Ticker(ticker)
        return data.info["sector"]

    def currentPortfolio(self):
        """Analyze the operations to get the current wallet.

        Return a dataframe containing the current wallet stocks/FIIs.
        """
        dataframe = self.operations
        dataframe = dataframe[
            (dataframe["Mercado"] == "Ações")
            | (dataframe["Mercado"] == "ETF")
            | (dataframe["Mercado"] == "FII")
            | (dataframe["Mercado"] == "BDR")
        ]
        dataframe.drop_duplicates(subset="Ticker", keep="first", inplace=True)

        # Creates the wallet
        wallet = pd.DataFrame()

        # Copy the ticker and market information
        wallet["Ticker"] = dataframe["Ticker"]
        wallet["Mercado"] = dataframe["Mercado"]

        # Sort the data by market and ticker
        wallet = wallet.sort_values(by=["Mercado", "Ticker"])

        # Create blank columns
        wallet["Quantidade"] = ""
        wallet["Preço médio"] = ""
        wallet["Cotação"] = ""
        wallet["Preço pago"] = ""
        wallet["Preço mercado"] = ""
        wallet["Proventos"] = ""
        wallet["Resultado liquido"] = ""
        wallet["Porcentagem carteira"] = ""

        # Calculate of the quantity of all non duplicate tickers
        for index, row in wallet.iterrows():

            rticker = row["Ticker"]
            avgPrice, numberStocks = self.avgPriceTicker(rticker)

            # Check the quantity.
            # If zero, then drops it from the dataframe.
            if numberStocks == 0:
                wallet = wallet.drop([index])
            # If non zero, keeps the ticker and updates the
            # quantity and the average price.
            else:
                wallet.at[index, "Quantidade"] = int(numberStocks)
                wallet.at[index, "Preço médio"] = avgPrice
                wallet.at[index, "Proventos"] = self.earningsByTicker(rticker)

        # Create a list of ticker to be used for finding
        # current prices of the ticker
        listTicker = wallet["Ticker"].tolist()
        for i in range(len(listTicker)):
            listTicker[i] = listTicker[i] + ".SA"

        # Get the current values of all tickers in the wallet
        if listTicker:
            curPricesTickers = self.currentMarketPriceByTickerList(listTicker)
            for index, row in wallet.iterrows():
                ticker = row["Ticker"] + ".SA"
                wallet.at[index, "Cotação"] = float(curPricesTickers[ticker])

        # Calculate the price according with the average price
        wallet["Preço pago"] = wallet["Quantidade"] * wallet["Preço médio"]
        # Calculate the price according with the current market value
        wallet["Preço mercado"] = wallet["Quantidade"] * wallet["Cotação"]
        # Calculate the liquid result of the ticker
        deltaPrice = wallet["Preço mercado"] - wallet["Preço pago"]
        wallet["Resultado liquido"] = deltaPrice + wallet["Proventos"]

        # Filter the stocks
        walletStock = wallet[wallet["Mercado"] == "Ações"]
        # Calculates the market value of stocks
        marketValueStock = walletStock["Preço mercado"].sum()
        # Filter the ETFs
        walletETF = wallet[wallet["Mercado"] == "ETF"]
        # Calculates the market value of ETFs
        marketValueETF = walletETF["Preço mercado"].sum()
        # Filter the FIIs
        walletFII = wallet[wallet["Mercado"] == "FII"]
        # Calculates the market value of FIIs
        marketValueFII = walletFII["Preço mercado"].sum()
        # Filter the BDRs
        walletBDR = wallet[wallet["Mercado"] == "BDR"]
        # Calculates the market value of FIIs
        marketValueBDR = walletBDR["Preço mercado"].sum()

        # Calculates the percentage of stocks and FIIs in the wallet
        for index, row in wallet.iterrows():
            if row["Mercado"] == "Ações":
                wallet.at[index, "Porcentagem carteira"] = (
                    row["Preço mercado"] / marketValueStock
                )
            elif row["Mercado"] == "ETF":
                wallet.at[index, "Porcentagem carteira"] = (
                    row["Preço mercado"] / marketValueETF
                )
            elif row["Mercado"] == "FII":
                wallet.at[index, "Porcentagem carteira"] = (
                    row["Preço mercado"] / marketValueFII
                )
            elif row["Mercado"] == "BDR":
                wallet.at[index, "Porcentagem carteira"] = (
                    row["Preço mercado"] / marketValueBDR
                )

        return wallet

    def currentPortfolioGoogleDrive(self):
        """Save the excel file to be used in Google Drive."""
        # Get the current portfolio
        dataframe = self.current
        # Removes the column from original dataframe
        dataframe = dataframe.drop(["Porcentagem carteira"], axis=1)

        i = 2
        for index, row in dataframe.iterrows():
            # This function takes a long time to run.
            # Not suitable to uncomment while testing.
            dfticker = dataframe["Ticker"]
            dataframe["Cotação"] = '=googlefinance("' + dfticker + '")'
            market_price_str = "=E" + str(i) + "*G" + str(i)
            dataframe.at[index, "Preço mercado"] = market_price_str
            net_result_str = "=I" + str(i) + "+J" + str(i) + "-H" + str(i)
            dataframe.at[index, "Resultado liquido"] = net_result_str
            # Increment the index to calculate the cells in Excel file.
            i += 1

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(
            "carteiraGoogleDrive.xlsx",
            engine="xlsxwriter",
        )

        # Convert the dataframe to an XlsxWriter Excel object.
        dataframe.to_excel(writer, sheet_name="Sheet1")

        # Get the xlsxwriter workbook and worksheet objects.
        workbook = writer.book
        worksheet = writer.sheets["Sheet1"]

        # Add some cell formats.
        format1 = workbook.add_format(
            {"num_format": "#,##0.00", "align": "center"},
        )
        format2 = workbook.add_format(
            {"align": "center"},
        )
        formatBorder = workbook.add_format(
            {"bottom": 1, "top": 1, "left": 1, "right": 1},
        )

        bold = workbook.add_format(
            {"bold": True, "align": "center"},
        )

        # Green fill with dark green text.
        formatGreen = workbook.add_format(
            {"bg_color": "#C6EFCE", "font_color": "#006100"},
        )

        # Light red fill with dark red text.
        formatRed = workbook.add_format(
            {"bg_color": "#FFC7CE", "font_color": "#9C0006"},
        )

        # Conditional formatting. If values are greater equal than zero
        worksheet.conditional_format(
            "K2:K100",
            {
                "type": "cell",
                "criteria": ">=",
                "value": 0,
                "format": formatGreen,
            },
        )

        # Conditional formatting.If values are lesser than zero
        worksheet.conditional_format(
            "K2:K100",
            {
                "type": "cell",
                "criteria": "<",
                "value": 0,
                "format": formatRed,
            },
        )

        # Note: It isn't possible to format any cells that
        # already have a format such as the index or headers
        # or any cells that contain dates or datetimes.

        # Set the column width and format.
        worksheet.set_column("B:B", 14, format1)
        worksheet.set_column("C:C", 14, format1)
        worksheet.set_column("E:E", 14, format2)
        worksheet.set_column("F:F", 14, format1)
        worksheet.set_column("G:G", 14, format1)
        worksheet.set_column("H:H", 14, format1)
        worksheet.set_column("I:I", 16, format1)
        worksheet.set_column("J:J", 14, format1)
        worksheet.set_column("K:K", 20, format1)

        # Create supplementary table to support graphic of percentage
        # List of category
        worksheet.write("M1", "Ativo", bold)
        worksheet.set_column("M:M", 14, format2)
        worksheet.write("M2", "Ações")
        worksheet.write("M3", "BDR")
        worksheet.write("M4", "ETF")
        worksheet.write("M5", "FII")

        # Create list of the values
        worksheet.set_column("N:N", 18, format1)
        worksheet.write("N1", "Valor R$", bold)
        worksheet.write("N2", '=SUMIF(C2:C100, "Ações", I2:I100)')
        worksheet.write("N3", '=SUMIF(C2:C100, "BDR", I2:I100)')
        worksheet.write("N4", '=SUMIF(C2:C100, "ETF", I2:I100)')
        worksheet.write("N5", '=SUMIF(C2:C100, "FII", I2:I100)')

        # Create conditional format for borders
        worksheet.conditional_format(
            "M1:N5", {"type": "no_errors", "format": formatBorder}
        )

        # Creates a Pie chart
        chart1 = workbook.add_chart({"type": "pie"})

        # Configure the series and add user defined segment colors.
        chart1.add_series(
            {
                "data_labels": {"percentage": True},
                "categories": "=Sheet1!$M$2:$M$5",
                "values": "=Sheet1!$N$2:$N$5",
            }
        )

        # Add a title
        chart1.set_title({"name": "Composição da carteira"})

        # Insert the chart into the worksheet (with an offset)
        worksheet.insert_chart("M8", chart1, {"x_offset": 25, "y_offset": 10})

        # Close the Pandas Excel writer and output the Excel file
        writer.save()

        return dataframe

    def currentMarketTesouro(self, ticker):
        """Return the last price of the stock from website Status Invest.

        LFT = Letras Financeira do Tesouro
            -> Tesouro Selic
        LTN = Letras do Tesouro Nacional
            -> Tesouro Prefixado sem cupons
        NTN-F = Notas do Tesouro Nacional Tipo F
            -> Tesouro Prefixado com cupons semestrais
        NTN-B Principal = Notas do Tesouro Nacional Tipo B Principal
            -> Tesouro IPCA sem cupons
        NTN-B = Notas do Tesouro Nacional Tipo B
            -> Tesouro IPCA com cupons semestrais
        """
        dig4 = r"(\d\d\d\d)"
        dig6 = r"(\d\d\d\d\d\d)"
        rgx_selic = re.compile(
            r"(SELIC) " + dig4 + "|(LFT) " + dig6,
        )
        rgx_pre = re.compile(
            r"(Prefixado) " + dig4 + "|(LTN) " + dig6,
        )
        rgx_pre_juros = re.compile(
            r"(Prefixado com Juros Semestrais) " + dig4 + "|(NTN-F) " + dig6,
        )
        rgx_ipca = re.compile(
            r"(IPCA\+) " + dig4 + "|(NTN-B Principal) " + dig6,
        )
        rgx_ipca_juros = re.compile(
            r"(IPCA\+ com Juros Semestrais) " + dig4 + "|(NTN-B) " + dig6,
        )

        init_link = r"https://statusinvest.com.br/tesouro/"
        pattern_dict = {
            "SELIC": [
                rgx_selic,
                init_link + "tesouro-selic-",
            ],
            "Prefixado": [
                rgx_pre,
                init_link + "tesouro-prefixado-",
            ],
            "Prefixado com Juros Semestrais": [
                rgx_pre_juros,
                init_link + "tesouro-prefixado-com-juros-semestrais-",
            ],
            "IPCA+": [
                rgx_ipca,
                init_link + "tesouro-ipca-",
            ],
            "IPCA+ com Juros Semestrais": [
                rgx_ipca_juros,
                init_link + "tesouro-ipca-com-juros-semestrais-",
            ],
        }

        def getYearPattern(rgx, text):
            matching = rgx.search(text)
            if matching:
                if matching.group(2):
                    return matching.group(2)
                elif matching.group(4):
                    slc = matching.group(4)[4:]
                    return "20" + slc
                else:
                    return None
            else:
                return None

        def getURL(text):
            url = False
            for value_list in pattern_dict.values():
                rgx = value_list[0]
                link = value_list[1]
                year = getYearPattern(rgx, text)
                if year:
                    url = link + year
                    break
            return url

        value = 0
        url = getURL(ticker)

        if url:
            # Get information from URL
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")

            # Get the current value from ticker
            value = soup.find(class_="value").get_text()

            # Replace the point to empty in order to transform
            # the string in a number.
            value = value.replace(".", "")

            # Replace comma to point because Python uses point
            # as decimal spacer.
            value = value.replace(",", ".")

        return float(value)

    def currentTesouroDireto(self):
        """Create a dataframe with all open operations of Tesouro Direto."""
        dataframe = self.operations.copy()
        dataframe = dataframe[dataframe["Mercado"] == "Tesouro Direto"]
        dataframe = dataframe[dataframe["Operação"] != "Cobrança"]
        dataframe.drop_duplicates(subset="Ticker", keep="first", inplace=True)

        # Create the wallet
        wallet = pd.DataFrame()

        # Copy the ticker and market information
        wallet["Ticker"] = dataframe["Ticker"]
        wallet["Mercado"] = dataframe["Mercado"]
        wallet["Indexador"] = dataframe["Indexador"]

        # Create blank columns
        wallet["Quantidade"] = ""
        wallet["Preço médio"] = ""
        wallet["Preço pago"] = ""
        wallet["Cotação"] = ""
        wallet["Preço mercado"] = ""
        wallet["Proventos"] = ""
        wallet["Porcentagem carteira"] = ""

        # Sort the data by ticker
        wallet = wallet.sort_values(by=["Ticker"])

        # Calculate of the quantity of all non duplicate tickers
        for index, row in wallet.iterrows():

            ticker = row["Ticker"]
            avgPrice, numberStocks = self.avgPriceTicker(ticker)

            # Check the quantity.
            # If zero, then drops it from the dataframe.
            if round(numberStocks, 2) == 0:
                wallet = wallet.drop([index])
            # If non zero, keeps the ticker and updates
            # the quantity and the average price.
            else:
                wallet.at[index, "Quantidade"] = float(numberStocks)
                wallet.at[index, "Preço médio"] = float(avgPrice)
                wallet.at[index, "Cotação"] = self.currentMarketTesouro(ticker)
                wallet.at[index, "Proventos"] = self.earningsByTicker(ticker)

        # Calculate the prices
        wallet["Preço mercado"] = wallet["Quantidade"] * wallet["Cotação"]
        wallet["Preço pago"] = wallet["Quantidade"] * wallet["Preço médio"]

        # Calculate the net result
        deltaPrice = wallet["Preço mercado"] - wallet["Preço pago"]
        wallet["Resultado liquido"] = deltaPrice + wallet["Proventos"]

        totalTesouroDireto = wallet["Preço mercado"].sum()

        # Calculates the percentage of stocks and FIIs in the wallet
        for index, row in wallet.iterrows():
            wallet.at[index, "Porcentagem carteira"] = (
                row["Preço mercado"] / totalTesouroDireto
            )

        return wallet


if __name__ == "__main__":

    SOURCE_FILE_DIRECTORY = sys.path[0]
    FILE_NAME = r"\PORTFOLIO_TEMPLATE2.xlsx"

    file = SOURCE_FILE_DIRECTORY + FILE_NAME

    # Example:
    portfolio = PortfolioInvestment()
    portfolio.setFile(file)
    if portfolio.isValidFile():
        portfolio.run()
        carteiraGD = portfolio.currentPortfolioGoogleDrive()
        carteira = portfolio.currentPortfolio()
        tesouro = portfolio.currentTesouroDireto()
    else:
        print("\nThe selected Portfolio file is not in the expected format.")
        print("\nPlease, check the following expected column names:")
        for title in portfolio.getExpectedColumnsTitleList():
            print(" - ", title)
