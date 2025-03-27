from sqlalchemy import create_engine, text
import pandas as pd
from src.app import df_final  # Certifique-se de que o df_final está acessível

# Configuração do banco de dados
host = 'dpg-cvfdnt0fnakc739nfaqg-a.oregon-postgres.render.com'
port = '5432'
dbname = 'airflow_steam'
user = 'airflow_steam_user'
password = 'PJX5rcoxDV1DfLPtt3mEEJrFu8s9o2bb'

# String de conexão
conn_str = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}'

def load_data():
    """ Função que cria a tabela e carrega os dados no banco de dados """
    
    engine = create_engine(conn_str)
    table_name = 'raw_data'

    create_table_sql = f"""
    CREATE TABLE {table_name} (
        item TEXT,
        date DATE,
        offers INT,
        price FLOAT
    );
    """

    with engine.begin() as connection:
        connection.execute(text("DROP TABLE IF EXISTS raw_data CASCADE;"))
        print(f"Tabela {table_name} deletada com sucesso!")

        connection.execute(text(create_table_sql))
        print(f"Tabela {table_name} criada com sucesso!")

    # Inserindo dados no banco
    df_final.to_sql(table_name, engine, if_exists='replace', index=False)

    # Criando uma VIEW
    with engine.begin() as connection:
        connection.execute(text("CREATE OR REPLACE VIEW raw_data_new AS (SELECT * FROM raw_data);"))
        print("View criada com sucesso!")

    print("Dataframe abaixo")
    print(df_final)
    print("Dados carregados com sucesso!")
