import pandas as pd




df = pd.read_excel('dados_date_buy.xlsx')


print(df)


df.to_csv('date_buy.csv', encoding='UTF-8', index=False)