#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from datetime import datetime

import matplotlib.pyplot as plt     #Importação da biblioteca Matplotlib

SOURCE_FILE_DIRECTORY = r"C:\Users\Fred\Documents\GitHub\Investment_Portfolio_Analysis"

SOURCE_FILE_INITIAL_DATE = "2000-01-01"

indexer_dict = {
    "IPCA": SOURCE_FILE_DIRECTORY + "\IPCA mensal.xlsx",
    "SELIC": SOURCE_FILE_DIRECTORY + "\SELIC mensal.xlsx",
    "CDI":  SOURCE_FILE_DIRECTORY + "\CDI mensal.xlsx",
    "FGTS": SOURCE_FILE_DIRECTORY + "\FGTS mensal.xlsx",
    "Poupanca regra antiga": SOURCE_FILE_DIRECTORY + "\Poupança antiga mensal.xlsx",
    "Poupanca regra nova": SOURCE_FILE_DIRECTORY + "\Poupança nova mensal.xlsx"
}



#Calcula o retorno total de uma lista de taxas mensais
def __calcTotalProfitValueFromMonthlyInterestRateList(initial_value, monthly_interest_rate_list):
    total_profit_value = initial_value
    for monthly_interest_rate in monthly_interest_rate_list:
        adjusted_monthly_interest_rate = (1 + monthly_interest_rate/100)
        total_profit_value = adjusted_monthly_interest_rate * total_profit_value
    return total_profit_value

#Calcula a diferença de taxa       
def __calcTotalInterestRate(initial_value, final_value):
    total_interest_rate = (final_value-initial_value) / initial_value
    total_interest_rate *= 100
    return total_interest_rate

#    
def calcTotalProfitValues(initial_value, monthly_interest_rate_list):
    """
    Receives an 'Initial Value' and a 'Monthly Interest Rate List'.
    
    Returns a tuple with the 'Total Profit Value' and the 'Total Interest Rate (%)'.
    """
    total_profit_value = __calcTotalProfitValueFromMonthlyInterestRateList(initial_value, monthly_interest_rate_list)
    total_interest_rate = __calcTotalInterestRate(initial_value, total_profit_value)
    return total_profit_value, total_interest_rate


#Cria lista de taxas
def convertExcelToMonthlyInterestRateList(excel_excel_file_name):
    """
    Receives an 'Excel File Name' and returns a 'Monthly Interest Rate List', with values starting from January/2000.
    
    The Excel format is the same used for IPCA, SELIC and other similar Excel files.
    """
    excel_table = pd.read_excel(excel_excel_file_name)
    excel_table = excel_table.drop(["Unnamed: 13", "Fonte"], axis=1)
    excel_table = excel_table.sort_values(by=["Ano"])
    excel_table = excel_table.drop(["Ano"], axis=1)
    excel_table = excel_table.stack(dropna=True)
    monthly_interest_rate_list = list(excel_table)
    return monthly_interest_rate_list


#Printa valores
def printTotalProfitValues(initial_value, total_profit_value, total_interest_rate, indexer_name, initial_date, final_date):
    """
    Print the 'Initial Value', 'Total Profit Value' and 'Total Interest Rate (%)' values per 'Indexer Name'.
    """
    print(indexer_name + ":")
    print("Data Inicial: " + initial_date)
    print("Data Final: " + final_date)
    print("Aporte Inicial: R$ {:.2f}".format(initial_value))
    print("Taxa de Juros Total: {:.2f}%".format(total_interest_rate))
    print("Juros Total: R$ {:.2f}".format(initial_value * total_interest_rate/100))
    print("Valor Final Total: R$ {:.2f}".format(total_profit_value))
    print('')



#Converte valores da tabela para lista
def convertMonthlyInterestRateListToTable(monthly_interest_rate_list):
    """
    Receives a 'Monthly Interest Rate List' and returns a 'Monthly Interest Rate Table' with the columns:
     - 'Data Base'
     - 'Taxa Mensal'
     
    The 'Data Base' column starts in the first Monday of the 2000 year.
    """
    monthly_date_list = list(pd.date_range(start=SOURCE_FILE_INITIAL_DATE, periods=len(monthly_interest_rate_list), freq="BMS"))
    monthly_interest_rate_dict = {"Data Base": monthly_date_list, "Taxa Mensal": monthly_interest_rate_list}
    monthly_interest_rate_table = pd.DataFrame(monthly_interest_rate_dict, columns = ["Data Base", "Taxa Mensal"])
    return monthly_interest_rate_table

def cutMonthlyInterestRateTable(monthly_interest_rate_table, initial_date, final_date):
    monthly_df = monthly_interest_rate_table
    monthly_df_filtered = monthly_df.loc[(monthly_df["Data Base"] >= initial_date) & (monthly_df["Data Base"] <= final_date)]
    return monthly_df_filtered

def convertMonthlyInterestRateTableToList(monthly_interest_rate_table):
    monthly_interest_rate_table_short = monthly_interest_rate_table.drop(["Data Base"], axis=1)
    monthly_interest_rate_table_short = monthly_interest_rate_table_short.stack(dropna=True)
    return list(monthly_interest_rate_table_short)

def calcTotalProfitValuesFromDate(indexer_name, initial_value, initial_date, final_date):
    monthly_interest_rate_list = convertExcelToMonthlyInterestRateList(indexer_dict[indexer_name])
    monthly_interest_rate_table = convertMonthlyInterestRateListToTable(monthly_interest_rate_list)
    monthly_interest_rate_short_table = cutMonthlyInterestRateTable(monthly_interest_rate_table, initial_date, final_date)
    monthly_interest_rate_short_list = convertMonthlyInterestRateTableToList(monthly_interest_rate_short_table)
    total_profit_value, total_interest_rate = calcTotalProfitValues(initial_value, monthly_interest_rate_short_list)
    return total_profit_value, total_interest_rate
    
def calcPrintTotalProfitValuesFromDate(indexer_name, initial_value, initial_date, final_date):
    profit_value, interest_rate = calcTotalProfitValuesFromDate(indexer_name, initial_value, initial_date, final_date)
    printTotalProfitValues(initial_value, profit_value, interest_rate, indexer_name, initial_date, final_date)  


#######################################################
 
#função nova
def teste(initial_value, monthly_interest_rate_list):
    value=monthly_interest_rate_list
  
    value['Correcao']=""
    total_profit_value=initial_value
    for i in range(len(monthly_interest_rate_list)):
        adjusted_monthly_interest_rate = (1 + monthly_interest_rate_list.iloc[i,1]/100)
        total_profit_value = adjusted_monthly_interest_rate * total_profit_value
        value.iloc[i,2]=total_profit_value
    return value

#Valor de base para cálculo
valor = 4954.35
d1 = "2017-04-07"
d2 = "2019-05-17"

indexer_name = "IPCA"
monthly_interest_rate_list = convertExcelToMonthlyInterestRateList(indexer_dict[indexer_name])
monthly_interest_rate_table = convertMonthlyInterestRateListToTable(monthly_interest_rate_list)
monthly_interest_rate_table = cutMonthlyInterestRateTable(monthly_interest_rate_table, d1, d2)
aux=teste(valor,monthly_interest_rate_table)
plt.plot(aux['Data Base'],aux['Correcao'], label='IPCA')

indexer_name = "CDI"
monthly_interest_rate_list = convertExcelToMonthlyInterestRateList(indexer_dict[indexer_name])
monthly_interest_rate_table = convertMonthlyInterestRateListToTable(monthly_interest_rate_list)
monthly_interest_rate_table = cutMonthlyInterestRateTable(monthly_interest_rate_table, d1, d2)
aux=teste(valor,monthly_interest_rate_table)
plt.plot(aux['Data Base'],aux['Correcao'], label='CDI') 


indexer_name = "SELIC"
monthly_interest_rate_list = convertExcelToMonthlyInterestRateList(indexer_dict[indexer_name])
monthly_interest_rate_table = convertMonthlyInterestRateListToTable(monthly_interest_rate_list)
monthly_interest_rate_table = cutMonthlyInterestRateTable(monthly_interest_rate_table, d1, d2)
aux=teste(valor,monthly_interest_rate_table)
plt.plot(aux['Data Base'],aux['Correcao'], label='SELIC')

indexer_name = "FGTS"
monthly_interest_rate_list = convertExcelToMonthlyInterestRateList(indexer_dict[indexer_name])
monthly_interest_rate_table = convertMonthlyInterestRateListToTable(monthly_interest_rate_list)
monthly_interest_rate_table = cutMonthlyInterestRateTable(monthly_interest_rate_table, d1, d2)
aux=teste(valor,monthly_interest_rate_table)
plt.plot(aux['Data Base'],aux['Correcao'], label='FGTS')

plt.legend(title='Legenda')
plt.ylabel('R$1 ao longo do tempo')
plt.xlabel('Tempo')
plt.grid()
plt.show()

print(type(monthly_interest_rate_table))






#monthly_interest_rate_short_table = cutMonthlyInterestRateTable(monthly_interest_rate_table, initial_date, final_date)
#lista=convertExcelToMonthlyInterestRateList(indexer_dict[indexer_name])
#print(monthly_interest_rate_short_table)
#test=teste(1000,monthly_interest_rate_short_table)
#print(test.iloc[:,1])

#plt.plot( test.iloc[:,0], test.iloc[:,1], 'ro' )
#plt.ylabel('Valor da operação')
#plt.xlabel('Data')
#plt.show()




#calcPrintTotalProfitValuesFromDate("IPCA", 1000, initial_date, final_date)
#calcPrintTotalProfitValuesFromDate("SELIC", 1000, initial_date, final_date)
#calcPrintTotalProfitValuesFromDate("CDI", 1000, initial_date, final_date)
#calcPrintTotalProfitValuesFromDate("FGTS", 1000, initial_date, final_date)
#calcPrintTotalProfitValuesFromDate("Poupanca regra antiga", 1000, initial_date, final_date)
#calcPrintTotalProfitValuesFromDate("Poupanca regra nova", 1000, initial_date, final_date)





#calcTotalProfitValues(1000,monthly_interest_rate_short_table)

#print (monthly_interest_rate_short_table)




##Plota valor da operação
#plt.plot( monthly_interest_rate_short_table.iloc[:,1], monthly_interest_rate_short_table.iloc[:,2], 'ro' )
#plt.plot( monthly_interest_rate_short_table["Data Base"], monthly_interest_rate_short_table["Taxa Mensal"], 'ro' )
#plt.ylabel('Valor da operação')
#plt.xlabel('Data')
#plt.show()