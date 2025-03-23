from sqlalchemy import create_engine, text
import pandas as pd
from app import df_final

# Substitua pelos seus dados de conexão
host = 'dpg-cvfdnt0fnakc739nfaqg-a.oregon-postgres.render.com'
port = '5432'  # O padrão do PostgreSQL
dbname = 'airflow_steam'
user = 'airflow_steam_user'
password = 'PJX5rcoxDV1DfLPtt3mEEJrFu8s9o2bb'

# String de conexão do PostgreSQL
conn_str = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}'

# Criação da conexão
engine = create_engine(conn_str)

# Definindo o nome da tabela
table_name = 'raw_data'  # Escolha o nome da tabela no banco

# Criando o comando SQL CREATE OR REPLACE TABLE
create_table_sql = f"""


CREATE TABLE {table_name} (
    item TEXT,
    date DATE,
    offers INT,
    price FLOAT
);
"""

# Executando o comando no banco de dados
with engine.connect() as connection:
    connection.execute(text("DROP TABLE IF EXISTS raw_data CASCADE;"))
    connection.commit()
    print(f"Tabela {table_name} deletada com sucesso!")


    connection.execute(text(create_table_sql))
    print(f"Tabela {table_name} criada ou substituída com sucesso!")


df_final.to_sql(table_name, engine, if_exists='replace', index=False)


with engine.connect() as connection:
    connection.execute(text("CREATE OR REPLACE VIEW raw_data_new as (SELECT * FROM raw_data);"))
    connection.commit()
    print(f"View criada com sucesso!")


print("DF$#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print(df_final)