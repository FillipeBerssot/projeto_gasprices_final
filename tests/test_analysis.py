from src.data_analysis import calcular_faixa_anual, preparar_comparacao_temporal, preco_mais_barato_atual, FILE_NAME
from src.data_cleaning import load_and_clean_data


PRODUTO_TESTE = 'GASOLINA COMUM'
ANO_TESTE = 2026
ESTADOS_TESTE = ['BAHIA', 'PERNAMBUCO', 'SAO PAULO']

df_completo = load_and_clean_data(FILE_NAME)

if ANO_TESTE not in df_completo['Data'].dt.year.unique():
    ANO_TESTE = df_completo['Data'].dt.year.max()
    print(f'Ajustando ano do teste para o mais recente disponivel: {ANO_TESTE}\n')

# Teste faixa anual:
print(' --- 1. TESTE FAIXA ANUAL (Max/Min/Amplitude) ---')
df_faixa_teste = calcular_faixa_anual(PRODUTO_TESTE, ANO_TESTE)
print(f'Análise de {PRODUTO_TESTE} em {ANO_TESTE}:')
print(df_faixa_teste.sort_values(by='Amplitude', ascending=False).head().to_string())
print('\n' + '='*50 + '\n')

# Teste de comparação temporal e preco mais barato:
print(' --- 2. TESTE DE COMPARAÇÃO DIRETA (Menor preço Atual) ---')

df_comparacao_teste = preparar_comparacao_temporal(PRODUTO_TESTE, ESTADOS_TESTE)

estado, preco = preco_mais_barato_atual(df_comparacao_teste)

print(f"Estados comparados: {', '.join(ESTADOS_TESTE)}")
print(f'Estado mais barato na ultima data: {estado} (R$ {preco:.3f})')

print('\n' + '='*50 + '\n')
print('Teste do Modulo 2 conluido. Se os preços e a amplitude aparecerem, está tudo certo.')