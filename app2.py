import requests
import pandas as pd

# Cookie para autenticação
cookie = {'steamLoginSecure': '76561198361827516%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MDAwMl8yNTgzRTJFNl9EM0E1OCIsICJzdWIiOiAiNzY1NjExOTgzNjE4Mjc1MTYiLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3NDI3MzU1OTQsICJuYmYiOiAxNzM0MDA5MDE3LCAiaWF0IjogMTc0MjY0OTAxNywgImp0aSI6ICIwMDBFXzI2MDYzQTREXzg3Njk2IiwgIm9hdCI6IDE3MzQxODMwMzgsICJydF9leHAiOiAxNzUyNzM5MTYwLCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiMTc3LjM1LjEzOS4yNDAiLCAiaXBfY29uZmlybWVyIjogIjE3Ny4zNS4xMzkuMjQwIiB9.-iopYCcoeTd33K5qW-mELxMTSssQOMxHJZ0VnKJ61xqM1vH9CtbB56vK3KGW4NeBhtRQBf-YinJK9xhqLHJZBQ'}  

# Dicionário com os itens e suas URLs
inventory = {

    'Glock - Gamma Dopple (FN)': 'https://steamcommunity.com/market/pricehistory/?country=PT&currency=7&appid=730&market_hash_name=Glock-18%20%7C%20Gamma%20Doppler%20(Factory%20New)',
    'Usp - Whiteout (MW)': 'https://steamcommunity.com/market/pricehistory/?country=PT&currency=7&appid=730&market_hash_name=USP-S%20%7C%20Whiteout%20(Minimal%20Wear)',
    'M4A4 - Dragon King (MW)': 'https://steamcommunity.com/market/pricehistory/?country=PT&currency=7&appid=730&market_hash_name=M4A4%20%7C%20%E9%BE%8D%E7%8E%8B%20(Dragon%20King)%20(Minimal%20Wear)',
    'P250 - See Ya Later (MW)': 'https://steamcommunity.com/market/pricehistory/?country=PT&currency=7&appid=730&market_hash_name=P250%20%7C%20See%20Ya%20Later%20(Minimal%20Wear)',
    'M4A1-S - PrintStream (FT)': 'https://steamcommunity.com/market/pricehistory/?country=PT&currency=7&appid=730&market_hash_name=M4A1-S%20%7C%20Printstream%20(Field-Tested)',
    'MP9 - Monte Fuji (FT)': 'https://steamcommunity.com/market/pricehistory/?country=PT&currency=7&appid=730&market_hash_name=MP9%20%7C%20Mount%20Fuji%20(Factory%20New)',
    'Desert Eagle - Ocean Drive (MW)': 'https://steamcommunity.com/market/pricehistory/?country=PT&currency=7&appid=730&market_hash_name=Desert%20Eagle%20%7C%20Ocean%20Drive%20(Minimal%20Wear)',
    'Agente Sir Bloody': 'https://steamcommunity.com/market/pricehistory/?country=PT&currency=7&appid=730&market_hash_name=Sir%20Bloody%20Silent%20Darryl%20%7C%20The%20Professionals',
    'AK-47 - Bloodsport (FT)': 'https://steamcommunity.com/market/pricehistory/?country=PT&currency=7&appid=730&market_hash_name=AK-47%20%7C%20Bloodsport%20(Field-Tested)',
    'Hunstman - Crimson Web (FT)': 'https://steamcommunity.com/market/pricehistory/?country=PT&currency=7&appid=730&market_hash_name=%E2%98%85%20Huntsman%20Knife%20%7C%20Crimson%20Web%20(Field-Tested)',
    'Talon - Night Stripe (BS)': 'https://steamcommunity.com/market/pricehistory/?country=PT&currency=7&appid=730&market_hash_name=%E2%98%85%20Talon%20Knife%20%7C%20Night%20Stripe%20(Battle-Scarred)',
    'Galil - Cerberus (MW)': 'https://steamcommunity.com/market/pricehistory/?country=PT&currency=7&appid=730&market_hash_name=Galil%20AR%20%7C%20Cerberus%20(Minimal%20Wear)'}


# DataFrame final
df_final = pd.DataFrame()

# Loop sobre os itens do inventário
for item_name, url in inventory.items():
    try:
        # Requisição para a API com cookie
        response = requests.get(url, cookies=cookie)
        data = response.json()

        # Criando DataFrame com os dados retornados
        df = pd.DataFrame(data['prices'], columns=['date', 'price', 'offers'])

        # Limpeza e ajustes
        df["date_clean"] = df["date"].str.replace(r"\d+: \+\d+", "", regex=True).str.strip()
        df["date"] = pd.to_datetime(df["date_clean"], format="%b %d %Y", errors="coerce")
        df["offers"] = df["offers"].str.replace(r"\D", "", regex=True).astype("Int64").fillna(0).astype(int)

        # Adicionando nome do item ao DataFrame
        df["item"] = item_name

        # Selecionando colunas finais
        df = df[["item", "date", "offers", "price"]]

        # Concatenando ao DataFrame final
        df_final = pd.concat([df_final, df], ignore_index=True)

        print(f"✔ Sucesso: {item_name}")

    except Exception as e:
        print(f"❌ Erro ao processar {item_name}: {e}")

# Exibir resultado final
print(df_final)

df_final.to_csv('inventory_data.csv')
