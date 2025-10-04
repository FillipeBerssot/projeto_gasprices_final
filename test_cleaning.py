# Testar a Limpeza do Dataset

from data_cleaning import load_and_clean_data


FILE_NAME = 'data_gas_mensal_2013-2025.xlsx'

print('iniciando a limpeza do arquivo...')
df_limpo = load_and_clean_data(FILE_NAME)
print('Limpeza concluida com sucesso.\n')

print('--- 1. Primeiras 5 linhas (df.head()) ---')
print('Isto verifica se o cabeçalho foi lido corretamente na linha 17.')
print(df_limpo.head())
print('\n' + '='*50 + '\n')

print('--- 2. Tipos de Dados e Ausentes (df.info()) ---' )
print('Isto verifica se as colunas "Data" e "Preco_Medio_Revenda" foram convertidos corretamente.')
df_limpo.info()

print('\n' + '='*50 + '\n')
print('--- 3. Estatisticas Basicas (df.describe()) ---')
print('Isto só funciona se os preços forem numeros. Verifique se "Preco_Medio_Revenda" tem Média, Mínimo e Máximo.')
print(df_limpo['Preco_Medio_Revenda'].describe().to_string())