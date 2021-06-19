
import pandas as pd
import numpy as np
from datetime import datetime


import matplotlib.pyplot as plt     #Importação da biblioteca Matplotlib


SOURCE_FILE_DIRECTORY = r"C:\Users\Fred\source\repos\Investment_Portfolio_Analysis"
FILE_NAME = "\Extrato_Fred.xlsx"

file = SOURCE_FILE_DIRECTORY+FILE_NAME


def readOperations (file):
    """
    Reads the Excel file with all the operations.
    
    Returns the a data frame containing the full table.
    """
    fullTable = pd.read_excel(file)
    return fullTable


def overallTaxAndIncomes (file):
    """
    Reads the Excel file with all the operations.

    Returns the sum of the fees, income tax, dividend and jcp of all operations.
    """
    table = readOperations(file)
    fee = table['Taxas'].sum()
    incomeTax = table['IR'].sum()
    dividend = table['Dividendos'].sum()
    jcp = table['JCP'].sum()

    return fee, incomeTax, dividend, jcp


def filteredTable (file,ticker):
    """
    Reads the Excel file with all the operations.

    Returns a filtered table according to the ticker.
    """
    table = readOperations(file)
    filter = table[table["Ticker"]==ticker]
    return filter
    

def unitsTicker(file,ticker):
    """
    Returns how many stocks of the given ticker.
    """
    table = filteredTable(file,TICKER)              #Filter the table by ticker
    buy = table[table["Operação"]=="Compra"]        #Filter the table by buy operation
    buy = int(buy["Quantidade"].sum())              #Calculates the number of units bought
    sell = table[table["Operação"]=="Venda"]        #Filter the table by sell operation
    sell = int(sell["Quantidade"].sum())            #Calculates the number of units sold
    
    return buy, sell, buy-sell


def tesouroSelic (file):
    """
    Reads the Excel file with all the operations

    Return all operations in Tesouro SELIC
    """
    table = readOperations(file)
    table = table[table["Mercado"]=="Tesouro Direto"]
    table = table[table["Indexador"]=="SELIC"]
    #filtered = table[table["Mercado"]=="Tesouro Direto"]
    return table



def customTable (file, ticker, market, dueDate, profitability, index, operation):
    """
    Reads the Excel file with all the operations.

    Returns a filtered dataframe according with the desired parameters.
    """
    table = readOperations(file)
    if ticker != "all":
        table = table[table["Ticker"] == ticker]
    if market != "all":
        table = table[table["Mercado"] == market]
    if dueDate != "NA":
        table = table[table["Vencimento"] == dueDate]
    if profitability != "NA":
        table = table[table["Rentabilidade Contratada"] == dueDate]
    if index != "all":
        table = table[table["Indexador"] == index]
    if operation != "all":
        table = table[table["Operação"] == operation]
    return table
    


def customTableDate (file, ticker, market, dueDate, profitability, index, operation, startDate, endDate):
    """
    Reads the Excel file with all the operations.

    Returns a filtered dataframe according with the desired parameters and a certain time range.
    """

    table = customTable(file, ticker, market, dueDate, profitability, index, operation)
    table = table[table["Data"] >= startDate]
    table = table[table["Data"] <= endDate]
    return table




def numberOperationsYear (file):
    """
    Reads the Excel file with all the operations.

    Returns 3 lists containing the number of operations. The lists are linked between themselves according to the year.
    """

    table = readOperations(file)

    firstYear = table["Data"].min()     #Calculate the year of the first operation
    lastYear = table["Data"].max()      #Calculate the yar of the last operation
    
    #Create the empy lists
    listYear = []
    listBuy = []
    listSell = []
    janFirst = '-01-01'     #Auxiliary variable to create the first date of the year
    decLast = '-12-31'      #Auxiliary variable to create the last date of the year
    
    #Collect the number of operations per year
    for i in range(firstYear.year, lastYear.year+1):
        start = str(i) + janFirst
        end = str(i) + decLast
        #Get filtered table according to the year
        filtered = table[ (table["Data"] >= start) & (table["Data"] <= end) ]
        filteredBuy = filtered[ (filtered["Operação"] == "Compra") ]
        filteredSell = filtered[ (filtered["Operação"] == "Venda")]
        #Add the values in the lists
        listYear.append(i)
        listBuy.append(len(filteredBuy.index))
        listSell.append(len(filteredSell.index))
    
    return listYear, listBuy, listSell   
    



#width = 0.3
#ax = plt.figure()
#plt.bar(a , b, label='Buy', width=width)
#lt.bar(a , c , label='Sell', width=width)
#plt.legend(title='Legenda')
#lt.grid()
#plt.show()

#customTable (file, "all", "FII", "NA", "NA", "all", "Compra")
#print(overallTaxAndIncomes(file))
#a,b,c=units(file,TICKER)
#filteredTable(file,TICKER)



