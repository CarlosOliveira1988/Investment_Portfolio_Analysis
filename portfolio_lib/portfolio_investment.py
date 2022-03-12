"""This file has a set of methods related to Portfolio/Extrato."""

import os
import re
import sys

import pandas as pd
import requests
import yfinance as yf
from bs4 import BeautifulSoup

try:
    from indexer_lib.fixed_income import FixedIncomeCalculation

    from portfolio_lib.portfolio_history import OperationsHistory as OpInfo

except ModuleNotFoundError:

    # Change the directory
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

    # Run the import statements
    from indexer_lib.fixed_income import FixedIncomeCalculation

    from portfolio_lib.portfolio_history import OperationsHistory as OpInfo


class PortfolioInvestment:
    """This is a class to manage all portfolio operations."""

    def __init__(self):
        """Create the PortfolioInvestment object."""
        self.fixedIncomeCalc = FixedIncomeCalculation()
        self.fileOperations = None
        self.openedOperations = None
        self.operations = None
        self.operationsYear = None
        self.currentVariableIncome = None
        self.currentFixedIncome = None
        self.currentTreasuries = None
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

        # Dataframe with opened operations
        history = OpInfo(self.operations.copy())
        self.openedOperations = history.getOpenedOperationsDataframe()

        # 3 lists of number of operations by year. Suitable to be plot.
        self.operationsYear = self.numberOperationsYear()

        # Dataframe of the current portfolio related to 'Renda Variavel'
        self.currentVariableIncome = self.__currentPortfolio()

        # Dataframe of the current portfolio related to 'Renda Fixa'
        self.currentFixedIncome = self.__currentRendaFixa()

        # Dataframe of the current portfolio related to 'Tesouro Direto'
        self.currentTreasuries = self.__currentTesouroDireto()

    def getExtrato(self):
        """Return the raw dataframe related to the excel porfolio file."""
        extrato = pd.read_excel(self.fileOperations)

        # Excel file has title and data lines
        if len(extrato):
            return extrato

        # Excel file has ONLY the title line
        else:
            col_list = self.getExpectedColumnsTitleList()
            return pd.DataFrame(columns=col_list)

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
        dataframe = self.operations.copy()
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

    def __getMarketValueSum(self, wallet, market):
        df = wallet[wallet["Mercado"] == market]
        return df["Preço mercado"].sum()

    def __setTickerPercentage(self, wallet, market):
        marketValue = self.__getMarketValueSum(wallet, market)
        marketDF = wallet[wallet["Mercado"].isin([market])]
        for index, row in marketDF.iterrows():
            marketPrice = row["Preço mercado"]
            percentage = marketPrice / marketValue
            wallet.at[index, "Porcentagem carteira"] = percentage

    def __getDefaultDataframe(self):
        col_list = [
            "Ticker",
            "Mercado",
            "Indexador",
            "Rentabilidade-média Contratada",
            "Data Inicial",
            "Data Final",
            "Quantidade",
            "Preço médio",
            "Preço médio+taxas",
            "Preço pago",
            "Proventos",
            "Custos",
            "Taxas",
            "IR",
            "Dividendos",
            "JCP",
            "Cotação",
            "Preço mercado",
            "Preço mercado-pago",
            "Rentabilidade mercado-pago",
            "Resultado liquido",
            "Rentabilidade liquida",
            "Porcentagem carteira",
        ]
        defaultDF = pd.DataFrame(columns=col_list)
        return defaultDF

    def __createWalletDefaultColumns(self, market_list):
        # Dataframe with opened operations
        df = self.openedOperations.copy()

        # 'Extrato' dataframe has title and data lines
        if len(df):

            def __getQuantidade(df):
                return df["Quantidade Compra"] - df["Quantidade Venda"]

            def __getPrecoMedio(df):
                priceBuy = df["Preço-médio Compra"]
                qtdBuy = df["Quantidade Compra"]
                total_price = qtdBuy * priceBuy
                total_qtd = qtdBuy
                return total_price / total_qtd

            def __getPrecoMedioTaxas(wallet, df):
                qtd_for_fees = df["Quantidade Compra"] + df["Quantidade Venda"]
                mean_fee = wallet["Taxas"] / qtd_for_fees
                return mean_fee + wallet["Preço médio"]

            def __getPrecoPago(wallet):
                return wallet["Quantidade"] * wallet["Preço médio"]

            # Wallet default dataframe with all empty columns
            wallet = self.__getDefaultDataframe()

            # Prepare the useful dataframe
            df = df[df["Mercado"].isin(market_list)]
            df.drop_duplicates(subset="Ticker", keep="first", inplace=True)

            # Copy the useful data to the 'wallet'
            wallet["Ticker"] = df["Ticker"]
            wallet["Mercado"] = df["Mercado"]
            wallet["Indexador"] = df["Indexador"]
            wallet["Rentabilidade-média Contratada"] = df["Taxa Contratada"]
            wallet["Data Inicial"] = df["Data Inicial"]
            wallet["Data Final"] = df["Data Final"]
            wallet["Proventos"] = df["Dividendos"] + df["JCP"]
            wallet["Custos"] = df["Taxas"] + df["IR"]
            wallet["Taxas"] = df["Taxas"]
            wallet["IR"] = df["IR"]
            wallet["Dividendos"] = df["Dividendos"]
            wallet["JCP"] = df["JCP"]
            wallet["Quantidade"] = __getQuantidade(df)
            wallet["Preço médio"] = __getPrecoMedio(df)
            wallet["Preço médio+taxas"] = __getPrecoMedioTaxas(wallet, df)
            wallet["Preço pago"] = __getPrecoPago(wallet)

            # Sort the data by market and ticker
            wallet = wallet.sort_values(by=["Mercado", "Ticker"])

            return wallet

        # 'Extrato' dataframe has ONLY the title line
        else:
            return self.__getDefaultDataframe()

    def __calculateWalletDefaultColumns(self, wallet, market_list):
        # Calculate the target values
        wallet["Preço mercado"] = wallet["Quantidade"] * wallet["Cotação"]
        deltaPrice = wallet["Preço mercado"] - wallet["Preço pago"]
        wallet["Preço mercado-pago"] = deltaPrice
        buyPrice = wallet["Preço pago"]
        wallet["Rentabilidade mercado-pago"] = deltaPrice / buyPrice
        netResult = deltaPrice + wallet["Proventos"] - wallet["Custos"]
        wallet["Resultado liquido"] = netResult
        wallet["Rentabilidade liquida"] = netResult / buyPrice

        # Calculate the ticker percentage per market
        for mkt in market_list:
            self.__setTickerPercentage(wallet, mkt)

    def currentPortfolio(self):
        """Analyze the operations to get the current wallet.

        Return a dataframe containing the current wallet of stocks, FIIs,
        ETFs and BDRs.
        """
        return self.currentVariableIncome.copy()

    def __currentPortfolio(self):
        # Prepare the default wallet dataframe
        market_list = ["Ações", "ETF", "FII", "BDR"]
        wallet = self.__createWalletDefaultColumns(market_list)

        # Create a list of ticker to be used in YFinance API
        listTicker = wallet["Ticker"].tolist()
        listTicker = [(Ticker + ".SA") for Ticker in listTicker]

        # Get the current values of all tickers in the wallet
        if listTicker:
            curPricesTickers = self.currentMarketPriceByTickerList(listTicker)
            for index, row in wallet.iterrows():
                ticker = row["Ticker"] + ".SA"
                wallet.at[index, "Cotação"] = float(curPricesTickers[ticker])

        # Calculate values related to the wallet default columns
        self.__calculateWalletDefaultColumns(wallet, market_list)

        return wallet

    def currentPortfolioGoogleDrive(self):
        """Save the excel file to be used in Google Drive."""
        # Get the current portfolio
        dataframe = self.currentPortfolio()

        # Define the columns to be displayed in the exported spreadsheet
        # This will also define the columns order, that is useful to the
        # next steps
        expected_col_list = [
            "Ticker",
            "Mercado",
            "Quantidade",
            "Preço médio",
            "Preço pago",
            "Proventos",
            "Custos",
            "Cotação",
            "Preço mercado",
            "Preço mercado-pago",
            "Rentabilidade mercado-pago",
            "Resultado liquido",
            "Rentabilidade liquida",
        ]
        dataframe = dataframe[expected_col_list]

        # Define the columns in the exported spreadsheet
        ticker_col = "A"
        market_col = "B"
        quantity_col = "C"
        mean_price_col = "D"
        buy_price_col = "E"
        earning_col = "F"
        costs_col = "G"
        quotation_col = "H"
        market_price_col = "I"
        rent_gain_price_col = "J"
        gain_price_col = "K"
        net_result_col = "L"
        net_result_perc_col = "M"
        empty_col = "N"
        chart_col = "O"
        sum_if_col = "P"

        # Add some formulas to be used in GoogleSheets
        i = 2
        for index, row in dataframe.iterrows():
            # This function takes a long time to run.
            # Not suitable to uncomment while testing.
            dfticker = dataframe["Ticker"]
            dataframe["Cotação"] = '=googlefinance("' + dfticker + '")'

            market_price_str = "=" + quantity_col + str(i)
            market_price_str += "*" + quotation_col + str(i)
            dataframe.at[index, "Preço mercado"] = market_price_str

            gain_price_str = "=" + market_price_col + str(i)
            gain_price_str += "-" + buy_price_col + str(i)
            dataframe.at[index, "Preço mercado-pago"] = gain_price_str

            rent_gain_str = "=" + rent_gain_price_col + str(i)
            rent_gain_str += "/" + buy_price_col + str(i)
            dataframe.at[index, "Rentabilidade mercado-pago"] = rent_gain_str

            net_result_str = "=" + earning_col + str(i)
            net_result_str += "+" + rent_gain_price_col + str(i)
            net_result_str += "-" + costs_col + str(i)
            dataframe.at[index, "Resultado liquido"] = net_result_str

            net_perc_str = "=" + net_result_col + str(i)
            net_perc_str += "/" + buy_price_col + str(i)
            dataframe.at[index, "Rentabilidade liquida"] = net_perc_str
            # Increment the index to calculate the cells in Excel file.
            i += 1

        # Create a Pandas Excel writer using XlsxWriter as the engine
        file_name = "carteiraGoogleDrive.xlsx"
        writer = pd.ExcelWriter(file_name, engine="xlsxwriter")

        # Convert the dataframe to an XlsxWriter Excel object.
        dataframe.to_excel(writer, sheet_name="Sheet1", index=False)

        # Get the xlsxwriter workbook and worksheet objects.
        workbook = writer.book
        worksheet = writer.sheets["Sheet1"]

        # Add some cell formats.
        formatFloat = workbook.add_format(
            {"num_format": "#,##0.00", "align": "center"},
        )
        formatText = workbook.add_format(
            {"align": "center"},
        )
        formatPerc = workbook.add_format(
            {"num_format": "0.00%", "align": "center"},
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
        df_len = str(len(dataframe) + 1)
        worksheet.conditional_format(
            rent_gain_price_col + "2:" + net_result_perc_col + df_len,
            {
                "type": "cell",
                "criteria": ">=",
                "value": 0,
                "format": formatGreen,
            },
        )

        # Conditional formatting.If values are lesser than zero
        worksheet.conditional_format(
            rent_gain_price_col + "2:" + net_result_perc_col + df_len,
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

        # Set the column width and format
        def formatAsText(col_list, width=15):
            for col in col_list:
                worksheet.set_column(col + ":" + col, width, formatText)

        def formatAsFloat(col_list, width=15):
            for col in col_list:
                worksheet.set_column(col + ":" + col, width, formatFloat)

        def formatAsPercentage(col_list, width=15):
            for col in col_list:
                worksheet.set_column(col + ":" + col, width, formatPerc)

        formatAsText(
            [
                ticker_col,
                market_col,
            ]
        )
        formatAsFloat(
            [
                quantity_col,
                mean_price_col,
                buy_price_col,
                earning_col,
                costs_col,
                quotation_col,
                market_price_col,
            ]
        )
        formatAsFloat(
            [
                rent_gain_price_col,
                net_result_col,
            ],
            width=25,
        )
        formatAsPercentage(
            [
                gain_price_col,
                net_result_perc_col,
            ],
            width=25,
        )

        # Create supplementary table to support graphic of percentage
        # List of category
        formatAsText([chart_col])
        worksheet.write(chart_col + "1", "Ativo", bold)
        worksheet.write(chart_col + "2", "Ações")
        worksheet.write(chart_col + "3", "BDR")
        worksheet.write(chart_col + "4", "ETF")
        worksheet.write(chart_col + "5", "FII")

        # Create list of the values
        formatAsFloat([sum_if_col], width=20)
        start_sumif = "=SUMIF(" + market_col + "2:" + market_col + '100, "'
        end_sumif = '", ' + market_price_col + "2:" + market_price_col + "100)"
        worksheet.write(sum_if_col + "1", "Valor R$", bold)
        worksheet.write(sum_if_col + "2", start_sumif + "Ações" + end_sumif)
        worksheet.write(sum_if_col + "3", start_sumif + "BDR" + end_sumif)
        worksheet.write(sum_if_col + "4", start_sumif + "ETF" + end_sumif)
        worksheet.write(sum_if_col + "5", start_sumif + "FII" + end_sumif)

        # Create conditional format for borders
        chart_table_range = chart_col + "1:" + sum_if_col + "5"
        worksheet.conditional_format(
            chart_table_range, {"type": "no_errors", "format": formatBorder}
        )

        # Creates a Pie chart
        chart1 = workbook.add_chart({"type": "pie"})

        # Configure the series and add user defined segment colors
        categ_range = "=Sheet1!$" + chart_col + "$2:$" + chart_col + "$5"
        val_range = "=Sheet1!$" + sum_if_col + "$2:$" + sum_if_col + "$5"
        chart1.add_series(
            {
                "data_labels": {"percentage": True},
                "categories": categ_range,
                "values": val_range,
            }
        )

        # Add a title
        chart1.set_title({"name": "Composição da carteira"})

        # Insert the chart into the worksheet (with an offset)
        chart_cell = chart_col + "8"
        worksheet.insert_chart(
            chart_cell,
            chart1,
            {"x_offset": 25, "y_offset": 10},
        )

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
        return self.currentTreasuries.copy()

    def __currentTesouroDireto(self):
        # Prepare the default wallet dataframe
        market_list = ["Tesouro Direto"]
        wallet = self.__createWalletDefaultColumns(market_list)

        # Insert the current market values
        for index, row in wallet.iterrows():
            ticker = row["Ticker"]
            wallet.at[index, "Cotação"] = self.currentMarketTesouro(ticker)

        # Calculate values related to the wallet default columns
        self.__calculateWalletDefaultColumns(wallet, market_list)

        return wallet

    def currentValRendaFixa(
        self,
        initial_date,
        final_date,
        indexer,
        rate,
        buyPrice,
    ):
        """Return the current price of the related 'Renda Fixa' ticker."""
        if indexer == "PREFIXADO":
            return self.fixedIncomeCalc.getValueByPrefixedRate(
                initial_date,
                final_date,
                rate,
                buyPrice,
            )
        elif indexer == "IPCA":
            return self.fixedIncomeCalc.getValueByPrefixedRatePlusIPCA(
                initial_date,
                final_date,
                rate,
                buyPrice,
            )
        elif indexer == "CDI":
            return self.fixedIncomeCalc.getValueByProportionalCDI(
                initial_date,
                final_date,
                rate,
                buyPrice,
            )
        else:
            return float(buyPrice)

    def currentRendaFixa(self):
        """Create a dataframe with all open operations of Renda Fixa."""
        return self.currentFixedIncome.copy()

    def __currentRendaFixa(self):
        # Prepare the default wallet dataframe
        market_list = ["Renda Fixa"]
        wallet = self.__createWalletDefaultColumns(market_list)

        # Insert the current market values
        for index, row in wallet.iterrows():
            initial_date = row["Data Inicial"]
            final_date = row["Data Final"]
            indexer = row["Indexador"]
            rate = row["Rentabilidade-média Contratada"]
            buy_price = row["Preço médio"]
            wallet.at[index, "Cotação"] = self.currentValRendaFixa(
                initial_date,
                final_date,
                indexer,
                rate,
                buy_price,
            )

        # Calculate values related to the wallet default columns
        self.__calculateWalletDefaultColumns(wallet, market_list)

        return wallet


if __name__ == "__main__":

    import os

    # Main directory
    SOURCE_FILE_DIRECTORY = os.path.join(os.path.curdir, "portfolio_lib")
    FILE_NAME = "PORTFOLIO_TEMPLATE.xlsx"
    FILE = os.path.join(SOURCE_FILE_DIRECTORY, FILE_NAME)

    # Example:
    portfolio = PortfolioInvestment()
    portfolio.setFile(FILE)
    if portfolio.isValidFile():
        portfolio.run()
        carteiraGD = portfolio.currentPortfolioGoogleDrive()
        carteiraRV = portfolio.currentPortfolio()
        carteiraRF = portfolio.currentRendaFixa()
        tesouro = portfolio.currentTesouroDireto()
        print("\nCarteira Renda Variável:", carteiraRV)
        print("\nCarteira Renda Fixa:", carteiraRF)
        print("\nCarteira Tesouro Direto:", tesouro)
    else:
        print("\nThe selected Portfolio file is not in the expected format.")
        print("\nPlease, check the following expected column names:")
        for title in portfolio.getExpectedColumnsTitleList():
            print(" - ", title)
