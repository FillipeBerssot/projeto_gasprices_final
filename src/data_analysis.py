from src.data_cleaning import load_and_clean_data


FILE_NAME = 'data/data_gas_mensal_2013-2025.xlsx'

# Calculo de faixa anula (maximo e minimo):
def calcular_faixa_anual(produto, ano):
    df = load_and_clean_data(FILE_NAME)

    df_filtrado = df[
        (df['Produto'] == produto) &
        (df['Data'].dt.year == ano)
    ]

    faixa_anual = df_filtrado.groupby('Estado')['Preco_Medio_Revenda'].agg(['min', 'max']).reset_index()
    faixa_anual['Amplitude'] = faixa_anual['max'] - faixa_anual['min']

    return faixa_anual

# Preparação para comparação temporal entre estados:
def preparar_comparacao_temporal(produto, estados_selecionados):
    df = load_and_clean_data(FILE_NAME)

    df_comparacao = df[
        (df['Produto'] == produto) &
        (df['Estado'].isin(estados_selecionados))
    ]

    return df_comparacao

# Comparação direta:
def preco_mais_barato_atual(df_comparacao):
    if df_comparacao.empty:
        return 'N/A', 0.0
    
    data_recente = df_comparacao['Data'].max()
    
    df_recente = df_comparacao[df_comparacao['Data'] == data_recente]

    estado_min = df_recente.loc[df_recente['Preco_Medio_Revenda'].idxmin()]

    return estado_min['Estado'], estado_min['Preco_Medio_Revenda']

def preco_mais_caro_atual(df_comparacao):
    if df_comparacao.empty:
        return 'N/A', 0.0
    
    data_recente = df_comparacao['Data'].max()

    df_recente = df_comparacao[df_comparacao['Data'] == data_recente]

    estado_max = df_recente.loc[df_recente['Preco_Medio_Revenda'].idxmax()]

    return estado_max['Estado'], estado_max['Preco_Medio_Revenda']
    

def preco_mais_barato_anual(produto, ano, estados_selecionados):
    df = load_and_clean_data(FILE_NAME)

    df_filtrado = df[
        (df['Produto'] == produto) &
        (df['Data'].dt.year == ano) &
        (df['Estado'].isin(estados_selecionados))
    ]

    if df_filtrado.empty:
        return 'N/A', 0.0
    
    estado_min = df_filtrado.loc[df_filtrado['Preco_Medio_Revenda'].idxmin()]

    return estado_min['Estado'], estado_min['Preco_Medio_Revenda']

def preco_mais_caro_anual(produto, ano, estados_selecionados):
    df = load_and_clean_data(FILE_NAME)

    df_filtrado = df[
        (df['Produto'] == produto) &
        (df['Data'].dt.year == ano) &
        (df['Estado'].isin(estados_selecionados)) 
    ]

    if df_filtrado.empty:
        return 'N/A', 0.0
    
    estado_max = df_filtrado.loc[df_filtrado['Preco_Medio_Revenda'].idxmax()]

    return estado_max['Estado'], estado_max['Preco_Medio_Revenda']
