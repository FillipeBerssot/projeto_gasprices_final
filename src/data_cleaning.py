import os
import pandas as pd


PARQUET_PATH = 'data/dados_limpos.parquet'

def load_and_clean_data(file_path: str) -> pd.DataFrame:
    if os.path.exists(PARQUET_PATH):
        return pd.read_parquet(PARQUET_PATH)
    
    df = pd.read_excel(file_path, skiprows=16)
    df = df.rename(columns={
        'MÊS': 'Data',
        'PRODUTO': 'Produto',
        'REGIÃO': 'Regiao',
        'ESTADO': 'Estado',
        'PREÇO MÉDIO REVENDA': 'Preco_Medio_Revenda',
        'MARGEM MÉDIA REVENDA': 'Margem_Media_Revenda'
    })

    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')

    df = df.replace('-', pd.NA)

    def _is_price_like(col:str) -> bool:
        u = col.upper()
        return ('PREÇO' in u) or ('PRECO' in u) or ('MARGEM' in u)
    
    for col in df.columns:
        if _is_price_like(col) and col != 'Produto' and col != 'Estado' and col != 'Regiao':
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df['Preco_Medio_Revenda'] = pd.to_numeric(df['Preco_Medio_Revenda'], errors='coerce')
    df['Margem_Media_Revenda'] = pd.to_numeric(df['Margem_Media_Revenda'], errors='coerce')

    df_final = df.dropna(subset=['Preco_Medio_Revenda']).copy()

    cols_keep = ["Data", "Produto", "Regiao", "Estado", "Preco_Medio_Revenda", "Margem_Media_Revenda"]
    df_save = df_final[cols_keep]

    df_save.to_parquet(PARQUET_PATH, index=False)

    return df_save