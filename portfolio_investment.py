import pandas as pd             #Import the Pandas library to manage dataframes.
import yfinance as yf           #Imports the Yahoo Finance library to work with current values of assets.


SOURCE_FILE_DIRECTORY = r"C:\Users\Fred\Documents\GitHub\Investment_Portfolio_Analysis"
FILE_NAME = "\Extrato_Fred.xlsx"

file = SOURCE_FILE_DIRECTORY+FILE_NAME


class PorfolioInvestment:

    """
    This is a class to manage the all operations of the portfolio.

    """

    def __init__ (self, fileOperations):
        self.operations = pd.read_excel(file)                   #Dataframe with all the operations from the Excel file.
        self.operationsYear = self.numberOperationsYear()       #3 lists Number of operations by year. Suitable to be plot.
        self.current = self.currentPortfolio()                  #Dataframe of the current portfolio. Suitable to be plot.
        
        
 
    def overallTaxAndIncomes (self):
        """
        Returns the sum of the fees, income tax, dividend and jcp of all operations.

        The input for the method is the file that holds the operations.        
        """
        fee = self.operations['Taxas'].sum()
        incomeTax = self.operations['IR'].sum()
        dividend = self.operations['Dividendos'].sum()
        jcp = self.operations['JCP'].sum()

        return fee, incomeTax, dividend, jcp

    def numberOperationsYear (self):
        """
        Returns 3 lists containing the number of operations. The lists are linked between themselves according to the year.
        """

        dataframe = self.operations

        firstYear = dataframe["Data"].min()     #Calculates the year of the first operation
        lastYear = dataframe["Data"].max()      #Calculates the yar of the last operation
        
        #Creates the empy lists
        listYear = []
        listBuy = []
        listSell = []
        janFirst = '-01-01'     #Auxiliary variable to create the first date of the year
        decLast = '-12-31'      #Auxiliary variable to create the last date of the year
        
        #Collects the number of operations per year
        for i in range(firstYear.year, lastYear.year+1):
            start = str(i) + janFirst
            end = str(i) + decLast
            #Get filtered table according to the year
            filtered = dataframe[ (dataframe["Data"] >= start) & (dataframe["Data"] <= end) ]
            filteredBuy = filtered[ (filtered["Operação"] == "Compra") ]
            filteredSell = filtered[ (filtered["Operação"] == "Venda")]
            #Add the values in the lists
            listYear.append(i)
            listBuy.append(len(filteredBuy.index))
            listSell.append(len(filteredSell.index))
        
        return listYear, listBuy, listSell   


    def operationsByTicker (self,ticker):
        """
        Returns a filtered dataframe according to the ticker.

        The input for the method is the file that holds the operations. The filter is done based on this file.
        """
        dataframe = self.operations[self.operations["Ticker"] == ticker]
        return dataframe

    def unitsTicker (self, ticker):
        """
        Returns how many stocks of the given ticker.
        """
        dataframe = self.operationsByTicker(ticker)             #Filter the table by ticker
        buy = dataframe[dataframe["Operação"]=="Compra"]        #Filter the table by buy operation
        buy = int(buy["Quantidade"].sum())                      #Calculates the number of units bought
        sell = dataframe[dataframe["Operação"]=="Venda"]        #Filter the table by sell operation
        sell = int(sell["Quantidade"].sum())                    #Calculates the number of units sold
    
        return buy, sell, buy-sell

   
    def tesouroSelic (self):
        """
        Return all operations in Tesouro SELIC
        """
        dataframe = self.operations[self.operations["Mercado"]=="Tesouro Direto"]
        dataframe = dataframe[dataframe["Indexador"]=="SELIC"]
        #filtered = table[table["Mercado"]=="Tesouro Direto"]
        return dataframe


    def customTable (self, ticker, market, dueDate, profitability, index, operation):
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


    def customTableDate (self, ticker, market, dueDate, profitability, index, operation, startDate, endDate):
        """
        Reads the Excel file with all the operations.

        Returns a filtered dataframe according with the desired parameters and a certain time range.
        """

        dataframe = self.customTable(ticker, market, dueDate, profitability, index, operation)
        dataframe = dataframe[dataframe["Data"] >= startDate]
        dataframe = dataframe[dataframe["Data"] <= endDate]
        return dataframe


    def earningsByTicker (self, ticker):
        """
        Returns the total earnings of a given ticker.
        """
        dataframe = self.operationsByTicker(ticker)
        dataframe = dataframe[dataframe["Operação"] == "Provento"]
        #Returns the sum of dividens and JCP.
        return (float(dataframe["Dividendos"].sum() + dataframe["JCP"].sum()))


    def avgPriceTicker (self, ticker):
        """
        Return the average price of a given ticker
        """
        dataframe = self.operationsByTicker(ticker)
        #Fills with 0 the data that is not fullfilled in the dataframe. 
        #It is important because non filled cells will return NaN, which will cause calculation issues.
        dataframe = dataframe.fillna(0)

        avgPrice = 0
        avgPriceOld = 0
        qtStock = 0
        qtStockOld = 0
        costs = 0
        for index,row in dataframe.iterrows():
            #If the current operation is a buy event, then updates the average price
            if row['Operação'] == "Compra":
                #Get the number of stocks of the operation
                qtStock = row["Quantidade"]                 
                #Sum the costs
                costs = row["Taxas"] + row["IR"]            
                #Calculates the average price of the operation
                avgPrice = (row["Quantidade"] * row["Preço Unitário"] + costs) / qtStock
                #Calculates the average price considering also the previous operations
                avgPrice = ((avgPriceOld * qtStockOld) + avgPrice * qtStock) / (qtStockOld + qtStock)
                avgPriceOld = avgPrice
                qtStockOld += row["Quantidade"]

            #If the current operation is a sell event, then updates the number of stocks
            elif row["Operação"] == "Venda":
                qtStock -= row["Quantidade"]
                qtStockOld -= row["Quantidade"]

        numberStocks = qtStockOld
        return avgPrice, numberStocks

    
    def currentMarketPriceByTicker (self, ticker):
        """
        Returns the last price of the stock.

        I had issues when downloading data for Fundos imobiliários. It was necessary to work with period of 30d.
        I believe that is mandatory period or start/end date. With start/end I also had issues for reading the values.
        The solution was to consider "30d" as the period. I compared the results from function in Google and they were correct.
        """
        dataframe = yf.download(ticker, period = "30d")
        data = dataframe['Adj Close'].tail(1)
        return float(data)


    def currentMarketPriceByTickerList (self, list):
        """
        Returns a dataframe with the last price of the stocks in the list.

        """
        dataframe = yf.download(list, period = "1d")
        data = dataframe['Adj Close'].tail(1)
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
        return data.info['sector'] 


    def currentPortfolio(self):
        """
        Analyzes the operations to get the current wallet. 

        Return a dataframe containing the current wallet stocks/FIIs.
        """
        dataframe = self.operations
        dataframe = dataframe[ (dataframe["Mercado"]== "Ações") | (dataframe["Mercado"]== "ETF") | (dataframe["Mercado"]== "FII")]
        
        dataframe.drop_duplicates(subset ="Ticker", keep = 'first', inplace = True)
        
        #Creates the wallet
        wallet = pd.DataFrame()
        #Copies the ticker and market information
        wallet["Ticker"] = dataframe["Ticker"]
        wallet["Mercado"] = dataframe["Mercado"]
        #Sort the data by market and ticker
        wallet = wallet.sort_values(by=["Mercado", "Ticker"])
        wallet["Setor"] = ""                #Creates a blank column
        wallet["Quantidade"] = ""           #Creates a blank column
        wallet["Preço médio"] = ""          #Creates a blank column
        wallet["Cotação"] = ""              #Creates a blank column
        wallet["Preço pago"] = ""           #Creates a blank column
        wallet["Preço mercado"] = ""        #Creates a blank column
        wallet["Proventos"] = ""            #Creates a blank column
        wallet["Resultado liquido"] = ""    #Creates a blank column
        wallet["Porcentagem"] = ""          #Creates a blank column

        #Calculate of the quantity of all non duplicate tickers
        for index, row in wallet.iterrows():

            avgPrice, numberStocks = self.avgPriceTicker (row["Ticker"])

            #Check the quantity. If zero, there drops it from the dataframe.             
            if numberStocks == 0:
                wallet = wallet.drop([index])
            #If non zero, keeps the ticker and updates the quantity and the average price.    
            else:
                #wallet.at[index, "Setor"] = sectorOfTicker(row["Ticker"])
                wallet.at[index, "Quantidade"] = int(numberStocks)
                wallet.at[index, "Preço médio"] = avgPrice
                #Modifies the name of the ticker so Yahoo Finance can understand. Yahoo Finance adds the ".SA" to the ticker name.
                #newTicker = row["Ticker"]+".SA"
                #wallet.at[index, "Cotação"] = currentMarketPriceByTicker(newTicker )
                #Calculates the earnings by ticket
                wallet.at[index, "Proventos"] = self.earningsByTicker(row["Ticker"])
    

        #Creates a list of ticker to be used for finding current prices of the ticker
        listTicker = wallet["Ticker"].tolist()
        for i in range(len(listTicker)):
            listTicker[i] = listTicker[i] + ".SA"
        #Gets the current values of all tickers in the wallet
        currentPricesTickers = self.currentMarketPriceByTickerList(listTicker)
        
        for index, row in wallet.iterrows():
            ticker = row["Ticker"] + ".SA"
            wallet.at[index, "Cotação"] = float(currentPricesTickers[ticker])        
        


        #Calculates the price according with the average price
        wallet["Preço pago"] = wallet["Quantidade"] * wallet["Preço médio"]
        #Calculates the price according with the current market value
        wallet["Preço mercado"] = wallet["Quantidade"] * wallet["Cotação"]
        #Calculates the liquid result of the ticker
        wallet["Resultado liquido"] =  wallet["Preço mercado"] + wallet["Proventos"] - wallet["Preço pago"]

        #Filter the stocks
        walletStock = wallet[wallet["Mercado"]== "Ações"]
        #Calculates the market value of stocks
        marketValueStock = walletStock["Preço mercado"].sum()
        #Filter the ETFs
        walletETF = wallet[wallet["Mercado"]== "ETF"]
        #Calculates the market value of ETFs
        marketValueETF = walletETF["Preço mercado"].sum()
        #Filter the FIIs
        walletFII = wallet[wallet["Mercado"]== "FII"]
        #Calculates the market value of FIIs
        marketValueFII = walletFII["Preço mercado"].sum()
        
        #Calculates the percentage of stocks and FIIs in the wallet
        for index, row in wallet.iterrows():
            if row["Mercado"] == "Ações":
                wallet.at[index, "Porcentagem"] = 100 * row["Preço mercado"] / marketValueStock
            elif row["Mercado"] == "ETF":
                wallet.at[index, "Porcentagem"] = 100 * row["Preço mercado"] / marketValueETF
            elif row["Mercado"] == "FII":
                wallet.at[index, "Porcentagem"] = 100 * row["Preço mercado"] / marketValueFII
        
        return wallet


   

    def currentPortfolioGoogleDrive(self):
        dataframe = self.current
        
        
        for index, row in dataframe.iterrows():
            dataframe["Cotação"] = "=googlefinance(\"" + dataframe["Ticker"] + "\")"

        return dataframe




portfolio = PorfolioInvestment(file)
carteiraGD = portfolio.currentPortfolioGoogleDrive()
carteiraGD.to_excel("carteiraGD.xlsx") 
print(carteiraGD)




#Examples:
#print(portfolio.operations)
#print(portfolio.overallTaxAndIncomes())
#print(portfolio.customTableDate("ITSA4", "Ações", "NA", "NA", "all", "all", "20/04/2021", "19/05/2021"))
#print(portfolio.numberOperationsYear())
#print(portfolio.earningsByTicker("ITSA4"))
#print(portfolio.avgPriceTicker("ITSA4"))
#print(portfolio.currentMarketPriceByTicker("CPTS11.SA"))
#print(portfolio.currentMarketPriceByTickerList(["ITSA4.SA", ".....SA", ".....SA", "....SA", ".....SA"]))
#print(portfolio.currentMarketPriceByTickerWebScrappingStatusInvest("CPTS11","FII"))
#print(portfolio.sectorOfTicker("PETR4"))
#carteira = portfolio.currentPortfolio()
#print(portfolio.operationsYear)
