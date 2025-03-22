import pandas as pd
import requests

my_inventsory = ['https://steamcommunity.com/market/pricehistory/?country=PT&currency=7&appid=730&market_hash_name=Glock-18%20%7C%20Gamma%20Doppler%20(Factory%20New)',
                'https://steamcommunity.com/market/pricehistory/?country=PT&currency=7&appid=730&market_hash_name=USP-S%20%7C%20Whiteout%20(Minimal%20Wear)']



inventory = {

    'Glock - Gamma Dopple (FN)': 'https://steamcommunity.com/market/pricehistory/?country=PT&currency=7&appid=730&market_hash_name=Glock-18%20%7C%20Gamma%20Doppler%20(Factory%20New)',
    'Usp - Whiteout (MW)': 'https://steamcommunity.com/market/pricehistory/?country=PT&currency=7&appid=730&market_hash_name=USP-S%20%7C%20Whiteout%20(Minimal%20Wear)',
    'M4A4 - Dragon King (MW)': 'https://steamcommunity.com/market/listings/730/M4A4%20%7C%20%E9%BE%8D%E7%8E%8B%20(Dragon%20King)%20(Minimal%20Wear)',
    'P250 - See Ya Later (MW)': 'https://steamcommunity.com/market/listings/730/P250%20%7C%20See%20Ya%20Later%20(Minimal%20Wear)',
    'M4A1-S - PrintStream (FT)': 'https://steamcommunity.com/market/listings/730/M4A1-S%20%7C%20Printstream%20(Field-Tested)',
    'MP9 - Monte Fuji (FT)': 'https://steamcommunity.com/market/listings/730/MP9%20%7C%20Mount%20Fuji%20(Factory%20New)',
    'Desert Eagle - Ocean Drive (MW)': 'https://steamcommunity.com/market/listings/730/Desert%20Eagle%20%7C%20Ocean%20Drive%20(Minimal%20Wear)',
    'Agente Sir Bloody': 'https://steamcommunity.com/market/listings/730/Sir%20Bloody%20Silent%20Darryl%20%7C%20The%20Professionals',
    'AK-47 - Bloodsport (FT)': 'https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Bloodsport%20(Field-Tested)',
    'Hunstman - Crimson Web (FT)': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Huntsman%20Knife%20%7C%20Crimson%20Web%20(Field-Tested)',
    'Talon - Night Stripe (BS)': 'https://steamcommunity.com/market/listings/730/%E2%98%85%20Talon%20Knife%20%7C%20Night%20Stripe%20(Battle-Scarred)',
    'Galil - Cerberus (MW)': 'https://steamcommunity.com/market/listings/730/Galil%20AR%20%7C%20Cerberus%20(Minimal%20Wear)'}

cookie = {'steamLoginSecure': '76561198361827516%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MDAwMl8yNTgzRTJFNl9EM0E1OCIsICJzdWIiOiAiNzY1NjExOTgzNjE4Mjc1MTYiLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3NDI3MzU1OTQsICJuYmYiOiAxNzM0MDA5MDE3LCAiaWF0IjogMTc0MjY0OTAxNywgImp0aSI6ICIwMDBFXzI2MDYzQTREXzg3Njk2IiwgIm9hdCI6IDE3MzQxODMwMzgsICJydF9leHAiOiAxNzUyNzM5MTYwLCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiMTc3LjM1LjEzOS4yNDAiLCAiaXBfY29uZmlybWVyIjogIjE3Ny4zNS4xMzkuMjQwIiB9.-iopYCcoeTd33K5qW-mELxMTSssQOMxHJZ0VnKJ61xqM1vH9CtbB56vK3KGW4NeBhtRQBf-YinJK9xhqLHJZBQ'}

API = requests.get('https://steamcommunity.com/market/pricehistory/?country=PT&currency=7&appid=730&market_hash_name=Glock-18%20%7C%20Gamma%20Doppler%20(Factory%20New)', cookies=cookie)

API.text

df = pd.DataFrame(API.json())

df[['date', 'price', 'offers']] = pd.DataFrame(df.prices.tolist(), index=df.index)
remover = ['prices', 'success', 'price_suffix', 'price_prefix']
df.drop(remover, inplace=True, axis=1)


df["date_clean"] = df["date"].str.replace(r"\d+: \+\d+", "", regex=True).str.strip()
df["date"] = pd.to_datetime(df["date_clean"], format="%b %d %Y", errors="coerce")

df["offers"] = df["offers"].str.strip()  # Remove espaços extras
df["offers"] = df["offers"].str.replace(r"\D", "", regex=True)  # Remove qualquer caractere não numérico
df["offers"] = pd.to_numeric(df["offers"], errors="coerce").astype("Int64")
df["offers"] = df["offers"].fillna(0).astype(int)

df['item'] = 'Glock - Gamma Dopple (FN)'

df_novo = df[["item", "date", "offers", "price"]]

print(df_novo)
#print(df.describe())


