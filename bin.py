import pandas as pd
import openpyxl



df_xlsx = pd.read_excel('dados_date_buy.xlsx')

print(df_xlsx)

df_xlsx.to_csv('date_buy.csv', encoding='UTF-8', index=False)