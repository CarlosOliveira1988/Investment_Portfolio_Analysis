
###############################################################################################
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt     #Importação da biblioteca Matplotlib

#from extrato import numberOperationsYear
from extrato import * 



from urllib.request import urlopen

###############################################################################################
#Definitions
SOURCE_FILE_DIRECTORY = r"C:\Users\Fred\source\repos\Investment_Portfolio_Analysis"
FILE_NAME = "\Extrato_Fred.xlsx"

file = SOURCE_FILE_DIRECTORY+FILE_NAME


###############################################################################################
#Tests
#https://statusinvest.com.br/acoes/itsa4

#link = "https://statusinvest.com.br/acoes/itsa4"
#f = urlopen(link)
#myfile = f.read()
#print(myfile)

#date1 = "2019-01-01"
#date2 = "2020-12-31"
#customTableDate (file, "all", "FII", "NA", "NA", "all", "Compra", date1, date2)



##############################################################
#Teste para plotar a função numberOperationsYear
date, buy, sell = numberOperationsYear(file)

x = np.arange(len(date))
width = 0.35

fig, ax = plt.subplots()

rects1 = ax.bar(x - width/2, buy, width, label='Compra')
rects2 = ax.bar(x + width/2, sell, width, label='Venda')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Número')
ax.set_title('Quantidade de operações por ano')
ax.set_xticks(x)
ax.set_xticklabels(date)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.show()
#############################################################