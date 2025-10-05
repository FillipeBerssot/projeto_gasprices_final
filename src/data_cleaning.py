import pandas as pd


def load_and_clean_data(file_path):
    df = pd.read_excel(file_path, skiprows=16)

    df = df.rename(columns={
        'MÊS': 'Data',
        'PRODUTO': 'Produto',
        'REGIÃO': 'Regiao',
        'ESTADO': 'Estado',
        'PREÇO MÉDIO REVENDA': 'Preco_Medio_Revenda',
        'MARGEM MÉDIA REVENDA': 'Margem_Media_Revenda'
    })

    df['Data'] = pd.to_datetime(df['Data'])

    df['Preco_Medio_Revenda'] = pd.to_numeric(df['Preco_Medio_Revenda'], errors='coerce')
    df['Margem_Media_Revenda'] = pd.to_numeric(df['Margem_Media_Revenda'], errors='coerce')

    df_final = df.dropna(subset=['Preco_Medio_Revenda'])

    return df_final