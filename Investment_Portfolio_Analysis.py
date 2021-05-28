#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from datetime import datetime

SOURCE_FILE_DIRECTORY = r"D:\Dudu\Finanças\Investimentos\Mercado Financeiro\Investment_Portfolio_Analysis"

SOURCE_FILE_INITIAL_DATE = "2000-01-01"

indexer_dict = {
    "IPCA": SOURCE_FILE_DIRECTORY + "\IPCA mensal.xlsx",
    "SELIC": SOURCE_FILE_DIRECTORY + "\SELIC mensal.xlsx",
    "CDI":  SOURCE_FILE_DIRECTORY + "\CDI mensal.xlsx",
    "FGTS": SOURCE_FILE_DIRECTORY + "\FGTS mensal.xlsx",
    "Poupanca regra antiga": SOURCE_FILE_DIRECTORY + "\Poupança antiga mensal.xlsx",
    "Poupanca regra nova": SOURCE_FILE_DIRECTORY + "\Poupança nova mensal.xlsx"
}

def __calcTotalProfitValueFromMonthlyInterestRateList(initial_value, monthly_interest_rate_list):
    total_profit_value = initial_value
    for monthly_interest_rate in monthly_interest_rate_list:
        adjusted_monthly_interest_rate = (1 + monthly_interest_rate/100)
        total_profit_value = adjusted_monthly_interest_rate * total_profit_value
    return total_profit_value
       
def __calcTotalInterestRate(initial_value, final_value):
    total_interest_rate = (final_value-initial_value) / initial_value
    total_interest_rate *= 100
    return total_interest_rate
    
def calcTotalProfitValues(initial_value, monthly_interest_rate_list):
    """
    Receives an 'Initial Value' and a 'Monthly Interest Rate List'.
    
    Returns a tuple with the 'Total Profit Value' and the 'Total Interest Rate (%)'.
    """
    total_profit_value = __calcTotalProfitValueFromMonthlyInterestRateList(initial_value, monthly_interest_rate_list)
    total_interest_rate = __calcTotalInterestRate(initial_value, total_profit_value)
    return total_profit_value, total_interest_rate

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

initial_date = "2020-03-01"
final_date = "2021-04-01"

calcPrintTotalProfitValuesFromDate("IPCA", 1000, initial_date, final_date)
calcPrintTotalProfitValuesFromDate("SELIC", 1000, initial_date, final_date)
calcPrintTotalProfitValuesFromDate("CDI", 1000, initial_date, final_date)
calcPrintTotalProfitValuesFromDate("FGTS", 1000, initial_date, final_date)
calcPrintTotalProfitValuesFromDate("Poupanca regra antiga", 1000, initial_date, final_date)
calcPrintTotalProfitValuesFromDate("Poupanca regra nova", 1000, initial_date, final_date)
