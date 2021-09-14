import re
import sys
from datetime import date, datetime, timedelta

import pandas as pd
import requests
import xlsxwriter
import yfinance as yf
from bs4 import BeautifulSoup
from numpy import AxisError
from pandas.core.indexes.datetimes import date_range


class PorfolioInvestment:

    """
    This is a class to manage the all operations of the portfolio.

    """

    def __init__(self, fileOperations):
        self.fileOperations = fileOperations
        self.operations = pd.read_excel(
            fileOperations
        )  # Dataframe with all the operations from the Excel file.
        self.operationsYear = (
            self.numberOperationsYear()
        )  # 3 lists Number of operations by year. Suitable to be plot.
        self.current = (
            self.currentPortfolio()
        )  # Dataframe of the current portfolio. Suitable to be plot.

    def getExtrato(self):
        self.operations = pd.read_excel(self.fileOperations)
        return self.operations

    def overallTaxAndIncomes(self):
        """
        Returns the sum of the fees, income tax, dividend and jcp of all operations.

        The input for the method is the file that holds the operations.
        """
        fee = self.operations["Taxas"].sum()
        incomeTax = self.operations["IR"].sum()
        dividend = self.operations["Dividendos"].sum()
        jcp = self.operations["JCP"].sum()

        return fee, incomeTax, dividend, jcp

    def numberOperationsYear(self):
        """
        Returns 3 lists containing the number of operations. The lists are linked between themselves according to the year.
        """

        dataframe = self.operations

        firstYear = dataframe[
            "Data"
        ].min()  # Calculates the year of the first operation
        lastYear = dataframe["Data"].max()  # Calculates the yar of the last operation

        # Creates the empy lists
        listYear = []
        listBuy = []
        listSell = []
        janFirst = "-01-01"  # Auxiliary variable to create the first date of the year
        decLast = "-12-31"  # Auxiliary variable to create the last date of the year

        # Collects the number of operations per year
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
        """
        Returns a filtered dataframe according to the ticker.

        The input for the method is the file that holds the operations. The filter is done based on this file.
        """
        dataframe = self.operations[self.operations["Ticker"] == ticker]
        return dataframe

    def unitsTicker(self, ticker):
        """
        Returns how many stocks of the given ticker.
        """
        dataframe = self.operationsByTicker(ticker)  # Filter the table by ticker
        buy = dataframe[
            dataframe["Operação"] == "Compra"
        ]  # Filter the table by buy operation
        buy = int(buy["Quantidade"].sum())  # Calculates the number of units bought
        sell = dataframe[
            dataframe["Operação"] == "Venda"
        ]  # Filter the table by sell operation
        sell = int(sell["Quantidade"].sum())  # Calculates the number of units sold

        return buy, sell, buy - sell

    def tesouroSelic(self):
        """
        Return all operations in Tesouro SELIC
        """
        dataframe = self.operations[self.operations["Mercado"] == "Tesouro Direto"]
        dataframe = dataframe[dataframe["Indexador"] == "SELIC"]
        # filtered = table[table["Mercado"]=="Tesouro Direto"]
        return dataframe

    def customTable(self, ticker, market, dueDate, profitability, index, operation):
        """
        Reads the Excel file with all the operations.

        Returns a filtered dataframe according with the desired parameters.
        """
        dataframe = self.operations
        if ticker != "all":
            dataframe = dataframe[dataframe["Ticker"] == ticker]
        if market != "all":
            dataframe = dataframe[dataframe["Mercado"] == market]
        if dueDate != "NA":
            dataframe = dataframe[dataframe["Vencimento"] == dueDate]
        if profitability != "NA":
            dataframe = dataframe[dataframe["Rentabilidade Contratada"] == dueDate]
        if index != "all":
            dataframe = dataframe[dataframe["Indexador"] == index]
        if operation != "all":
            dataframe = dataframe[dataframe["Operação"] == operation]
        return dataframe

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
        """
        Reads the Excel file with all the operations.

        Returns a filtered dataframe according with the desired parameters and a certain time range.
        """

        dataframe = self.customTable(
            ticker, market, dueDate, profitability, index, operation
        )
        dataframe = dataframe[dataframe["Data"] >= startDate]
        dataframe = dataframe[dataframe["Data"] <= endDate]
        return dataframe

    def earningsByTicker(self, ticker):
        """
        Returns the total earnings of a given ticker.
        """
        dataframe = self.operationsByTicker(ticker)
        dataframe = dataframe[dataframe["Operação"] == "Provento"]
        # Returns the sum of dividens and JCP.
        return float(dataframe["Dividendos"].sum() + dataframe["JCP"].sum())

    def avgPriceTicker(self, ticker):
        """
        Return the average price of a given ticker
        """
        dataframe = self.operationsByTicker(ticker)
        # Fills with 0 the data that is not fullfilled in the dataframe.
        # It is important because non filled cells will return NaN, which will cause calculation issues.
        dataframe = dataframe.fillna(0)

        avgPrice = 0
        avgPriceOld = 0
        qtStock = 0.0
        qtStockOld = 0.0
        costs = 0
        for index, row in dataframe.iterrows():
            # If the current operation is a buy event, then updates the average price
            if row["Operação"] == "Compra":
                # Get the number of stocks of the operation
                qtStock = row["Quantidade"]
                # Sum the costs
                costs = row["Taxas"] + row["IR"]
                # Calculates the average price of the operation
                avgPrice = (row["Quantidade"] * row["Preço Unitário"] + costs) / qtStock
                # Calculates the average price considering also the previous operations
                avgPrice = ((avgPriceOld * qtStockOld) + avgPrice * qtStock) / (
                    qtStockOld + qtStock
                )
                avgPriceOld = avgPrice
                qtStockOld += row["Quantidade"]

            # If the current operation is a sell event, then updates the number of stocks
            elif row["Operação"] == "Venda":
                qtStock -= row["Quantidade"]
                qtStockOld -= row["Quantidade"]

        # numberStocks = qtStockOld
        return avgPrice, qtStockOld

    def currentMarketPriceByTicker(self, ticker):
        """
        Returns the last price of the stock.

        I had issues when downloading data for Fundos imobiliários. It was necessary to work with period of 30d.
        I believe that is mandatory period or start/end date. With start/end I also had issues for reading the values.
        The solution was to consider "30d" as the period. I compared the results from function in Google and they were correct.
        """
        dataframe = yf.download(ticker, period="30d")
        data = dataframe["Adj Close"].tail(1)
        return float(data)

    def currentMarketPriceByTickerList(self, list):
        """
        Returns a dataframe with the last price of the stocks in the list.

        """
        dataframe = yf.download(list, period="1d")
        data = dataframe["Adj Close"].tail(1)
        return data

    # def currentMarketPriceByTickerWebScrappingStatusInvest(self, ticker, market):
    #     """
    #     Returns the last price of the stock from website Status Invest.

    #     Requests have taken about 1s to get processed.
    #     """
    #     #Prepares the correct URL
    #     if market == "Ações":
    #         url = "https://statusinvest.com.br/acoes/"
    #     elif market == "FII":
    #         url = "https://statusinvest.com.br/fundos-imobiliarios/"
    #     elif market == "ETF":
    #         url = "https://statusinvest.com.br/etfs/"

    #     #Adds the ticket to the URL for search
    #     url += ticker
    #     #Get information from URL
    #     page = requests.get(url)
    #     soup = BeautifulSoup(page.content, 'html.parser')
    #     #Get the current value from ticker
    #     value = soup.find(class_='value').get_text()
    #     #Replace the comma to point in order to transform the string in a number.
    #     value = value.replace(',','.')

    #     return float(value)

    def sectorOfTicker(self, ticker):
        """
        Returns the sector of a given ticker

        The function uses the yfinance library to get the information.
        """

        ticker = ticker + ".SA"
        data = yf.Ticker(ticker)
        return data.info["sector"]

    def currentPortfolio(self):
        """
        Analyzes the operations to get the current wallet.
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
        # Copies the ticker and market information
        wallet["Ticker"] = dataframe["Ticker"]
        wallet["Mercado"] = dataframe["Mercado"]
        # Sort the data by market and ticker
        wallet = wallet.sort_values(by=["Mercado", "Ticker"])
        wallet["Setor"] = ""  # Creates a blank column
        wallet["Quantidade"] = ""  # Creates a blank column
        wallet["Preço médio"] = ""  # Creates a blank column
        wallet["Cotação"] = ""  # Creates a blank column
        wallet["Preço pago"] = ""  # Creates a blank column
        wallet["Preço mercado"] = ""  # Creates a blank column
        wallet["Proventos"] = ""  # Creates a blank column
        wallet["Resultado liquido"] = ""  # Creates a blank column
        wallet["Porcentagem carteira"] = ""  # Creates a blank column

        # Calculate of the quantity of all non duplicate tickers
        for index, row in wallet.iterrows():

            avgPrice, numberStocks = self.avgPriceTicker(row["Ticker"])

            # Check the quantity. If zero, there drops it from the dataframe.
            if numberStocks == 0:
                wallet = wallet.drop([index])
            # If non zero, keeps the ticker and updates the quantity and the average price.
            else:
                # wallet.at[index, "Setor"] = sectorOfTicker(row["Ticker"])
                wallet.at[index, "Quantidade"] = int(numberStocks)
                wallet.at[index, "Preço médio"] = avgPrice
                # Modifies the name of the ticker so Yahoo Finance can understand. Yahoo Finance adds the ".SA" to the ticker name.
                # newTicker = row["Ticker"]+".SA"
                # wallet.at[index, "Cotação"] = currentMarketPriceByTicker(newTicker )
                # Calculates the earnings by ticket
                wallet.at[index, "Proventos"] = self.earningsByTicker(row["Ticker"])

        # Creates a list of ticker to be used for finding current prices of the ticker
        listTicker = wallet["Ticker"].tolist()
        for i in range(len(listTicker)):
            listTicker[i] = listTicker[i] + ".SA"
        # Gets the current values of all tickers in the wallet
        currentPricesTickers = self.currentMarketPriceByTickerList(listTicker)

        for index, row in wallet.iterrows():
            ticker = row["Ticker"] + ".SA"
            wallet.at[index, "Cotação"] = float(currentPricesTickers[ticker])

        # Calculates the price according with the average price
        wallet["Preço pago"] = wallet["Quantidade"] * wallet["Preço médio"]
        # Calculates the price according with the current market value
        wallet["Preço mercado"] = wallet["Quantidade"] * wallet["Cotação"]
        # Calculates the liquid result of the ticker
        wallet["Resultado liquido"] = (
            wallet["Preço mercado"] + wallet["Proventos"] - wallet["Preço pago"]
        )

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
        # Get the current portfolio
        dataframe = self.current
        # Removes the column from original dataframe
        dataframe = dataframe.drop(["Porcentagem carteira"], axis=1)

        i = 2
        for index, row in dataframe.iterrows():

            # dataframe.at[index, "Setor"] = self.sectorOfTicker(row["Ticker"])      #This function takes a long time to run. Not suitable to uncomment while testing.
            dataframe["Cotação"] = '=googlefinance("' + dataframe["Ticker"] + '")'
            dataframe.at[index, "Preço mercado"] = "=E" + str(i) + "*G" + str(i)
            dataframe.at[index, "Resultado liquido"] = (
                "=I" + str(i) + "+J" + str(i) + "-H" + str(i)
            )

            i += 1  # Increments the index to calculate the cells in Excel file.

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter("carteiraGoogleDrive.xlsx", engine="xlsxwriter")

        # Convert the dataframe to an XlsxWriter Excel object.
        dataframe.to_excel(writer, sheet_name="Sheet1")

        # Get the xlsxwriter workbook and worksheet objects.
        workbook = writer.book
        worksheet = writer.sheets["Sheet1"]

        # Add some cell formats.
        format1 = workbook.add_format({"num_format": "#,##0.00", "align": "center"})
        format2 = workbook.add_format({"align": "center"})
        formatBorder = workbook.add_format(
            {"bottom": 1, "top": 1, "left": 1, "right": 1}
        )

        bold = workbook.add_format({"bold": True, "align": "center"})

        # Green fill with dark green text.
        formatGreen = workbook.add_format(
            {"bg_color": "#C6EFCE", "font_color": "#006100"}
        )

        # Light red fill with dark red text.
        formatRed = workbook.add_format(
            {"bg_color": "#FFC7CE", "font_color": "#9C0006"}
        )

        # Conditional formatting. If values are greater equal than zero
        worksheet.conditional_format(
            "K2:K100",
            {"type": "cell", "criteria": ">=", "value": 0, "format": formatGreen},
        )
        # Conditional formatting.If values are lesser than zero
        worksheet.conditional_format(
            "K2:K100",
            {"type": "cell", "criteria": "<", "value": 0, "format": formatRed},
        )

        # Note: It isn't possible to format any cells that already have a format such
        # as the index or headers or any cells that contain dates or datetimes.

        # Set the column width and format.
        worksheet.set_column("B:B", 14, format1)
        worksheet.set_column("C:C", 14, format1)
        # worksheet.set_column('D:D', 20, format1)
        worksheet.set_column("E:E", 14, format2)
        worksheet.set_column("F:F", 14, format1)
        worksheet.set_column("G:G", 14, format1)
        worksheet.set_column("H:H", 14, format1)
        worksheet.set_column("I:I", 16, format1)
        worksheet.set_column("J:J", 14, format1)
        worksheet.set_column("K:K", 20, format1)

        # Creates supplementary table to support graphic of percentage
        # List of category
        worksheet.write("M1", "Ativo", bold)
        worksheet.set_column("M:M", 14, format2)
        worksheet.write("M2", "Ações")
        worksheet.write("M3", "BDR")
        worksheet.write("M4", "ETF")
        worksheet.write("M5", "FII")
        # Creates list of the values
        worksheet.set_column("N:N", 18, format1)
        worksheet.write("N1", "Valor R$", bold)  # List values
        worksheet.write("N2", '=SUMIF(C2:C100, "Ações", I2:I100)')
        worksheet.write("N3", '=SUMIF(C2:C100, "BDR", I2:I100)')
        worksheet.write("N4", '=SUMIF(C2:C100, "ETF", I2:I100)')
        worksheet.write("N5", '=SUMIF(C2:C100, "FII", I2:I100)')
        # Creates conditional format for borders
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

    def currentMarketPriceTesouroWebScrappingStatusInvest(self, ticker):
        """
        Returns the last price of the stock from website Status Invest.

        LFT = Letras Financeira do Tesouro = Tesouro Selic
        LTN = Letras do Tesouro Nacional = Tesouro Prefixado (sem cupons)
        NTN-F = Notas do Tesouro Nacional Tipo F = Tesouro Prefixado (com cupons semestrais)
        NTN-B Principal = Notas do Tesouro Nacional Tipo B Principal = Tesouro IPCA (sem cupons)
        NTN-B = Notas do Tesouro Nacional Tipo B = Tesouro IPCA (com cupons semestrais)
        """

        rgx_selic = re.compile(
            r"(SELIC) (\d\d\d\d)|(LFT) (\d\d\d\d\d\d)",
        )
        rgx_pre = re.compile(
            r"(Prefixado) (\d\d\d\d)|(LTN) (\d\d\d\d\d\d)",
        )
        rgx_pre_juros = re.compile(
            r"(Prefixado com Juros Semestrais) (\d\d\d\d)|(NTN-F) (\d\d\d\d\d\d)",
        )
        rgx_ipca = re.compile(
            r"(IPCA\+) (\d\d\d\d)|(NTN-B Principal) (\d\d\d\d\d\d)",
        )
        rgx_ipca_juros = re.compile(
            r"(IPCA\+ com Juros Semestrais) (\d\d\d\d)|(NTN-B) (\d\d\d\d\d\d)",
        )

        pattern_dict = {
            "SELIC": [
                rgx_selic,
                "https://statusinvest.com.br/tesouro/tesouro-selic-",
            ],
            "Prefixado": [
                rgx_pre,
                "https://statusinvest.com.br/tesouro/tesouro-prefixado-",
            ],
            "Prefixado com Juros Semestrais": [
                rgx_pre_juros,
                "https://statusinvest.com.br/tesouro/tesouro-prefixado-com-juros-semestrais-",
            ],
            "IPCA+": [
                rgx_ipca,
                "https://statusinvest.com.br/tesouro/tesouro-ipca-",
            ],
            "IPCA+ com Juros Semestrais": [
                rgx_ipca_juros,
                "https://statusinvest.com.br/tesouro/tesouro-ipca-com-juros-semestrais-",
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

        if url != False:
            # Get information from URL
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            # Get the current value from ticker
            value = soup.find(class_="value").get_text()

            # Replace the point to empty in order to transform the string in a number.
            value = value.replace(".", "")
            # Replace comma to point because Python uses point as decimal spacer.
            value = value.replace(",", ".")

        return float(value)

    def currentTesouroDireto(self):
        """
        Creates a dataframe with all open operations of Tesouro Direto.
        """
        dataframe = self.operations
        dataframe = dataframe[dataframe["Mercado"] == "Tesouro Direto"]
        dataframe = dataframe[dataframe["Operação"] != "Cobrança"]

        dataframe.drop_duplicates(subset="Ticker", keep="first", inplace=True)

        # Creates the wallet
        wallet = pd.DataFrame()
        # Copies the ticker and market information
        wallet["Ticker"] = dataframe["Ticker"]
        wallet["Mercado"] = dataframe["Mercado"]
        wallet["Indexador"] = dataframe["Indexador"]

        # Sort the data by market and ticker
        # wallet = wallet.sort_values(by=["Mercado", "Ticker"])
        wallet["Quantidade"] = ""  # Creates a blank column
        wallet["Cotação"] = ""  # Creates a blank column
        # wallet["Preço pago"] = ""           #Creates a blank column
        wallet["Preço mercado"] = ""  # Creates a blank column
        # wallet["Resultado liquido"] = ""    #Creates a blank column
        wallet["Porcentagem carteira"] = ""  # Creates a blank column

        # Sort the data by ticker
        wallet = wallet.sort_values(by=["Ticker"])

        # Calculate of the quantity of all non duplicate tickers
        for index, row in wallet.iterrows():

            avgPrice, numberStocks = self.avgPriceTicker(row["Ticker"])

            # Check the quantity. If zero, there drops it from the dataframe.
            if round(numberStocks, 2) == 0:
                wallet = wallet.drop([index])
            # If non zero, keeps the ticker and updates the quantity and the average price.
            else:
                wallet.at[index, "Quantidade"] = float(numberStocks)
                wallet.at[
                    index, "Cotação"
                ] = self.currentMarketPriceTesouroWebScrappingStatusInvest(
                    row["Ticker"]
                )

        # Calculates the price according with the current market value
        wallet["Preço mercado"] = wallet["Quantidade"] * wallet["Cotação"]

        totalTesouroDireto = wallet["Preço mercado"].sum()

        # Calculates the percentage of stocks and FIIs in the wallet
        for index, row in wallet.iterrows():
            wallet.at[index, "Porcentagem carteira"] = (
                row["Preço mercado"] / totalTesouroDireto
            )

        return wallet


if __name__ == "__main__":

    SOURCE_FILE_DIRECTORY = sys.path[0]
    FILE_NAME = r"\PORTFOLIO_TEMPLATE.xlsx"

    file = SOURCE_FILE_DIRECTORY + FILE_NAME

    # Example:
    portfolio = PorfolioInvestment(file)
    carteiraGD = portfolio.currentPortfolioGoogleDrive()
    carteira = portfolio.currentPortfolio()
    tesouro = portfolio.currentTesouroDireto()
