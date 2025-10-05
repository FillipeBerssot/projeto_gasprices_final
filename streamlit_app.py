import streamlit as st

from src.data_cleaning import load_and_clean_data
from src.data_analysis import (
    calcular_faixa_anual,
    preparar_comparacao_temporal,
    preco_mais_barato_atual,
    preco_mais_barato_anual,
    preco_mais_caro_atual,
    preco_mais_caro_anual,
    FILE_NAME
)
from src.data_viz import plot_comparacao_temporal, plot_faixa_anual, vr


# Configuração da pagina:
st.set_page_config(layout="wide", page_title="⛽ Análise de Preços de Combustíveis ANP")

# Estilos globais para o divisor vertical
st.markdown("""
<style>
:root{
  --vr-color: rgba(250,250,250,0.28);
}
/* linha vertical */
.vr-line{
  border-left: 2px solid var(--vr-color);
  margin-left:auto; margin-right:auto;          /* centraliza dentro da coluna do meio */
}
/* tira um pouco do padding da coluna do meio pra parecer realmente central */
div[data-testid="column"]:nth-of-type(2) {      /* é a coluna do meio nesse bloco de 3 colunas */
  padding-left: .1rem !important;
  padding-right: .1rem !important;
}
</style>
""", unsafe_allow_html=True)

# Carregamento de dados com cache
@st.cache_data
def get_data():
    return load_and_clean_data(FILE_NAME)

df = get_data()

# Barra lateral (controle do usuario):
st.sidebar.title('⛽ Filtros de Análise')

# Seletor de produto:
produtos_disponiveis = df['Produto'].unique()

produto_padrao = 'GASOLINA COMUM' if 'GASOLINA COMUM' in produtos_disponiveis else produtos_disponiveis[0]

produto_selecionado = st.sidebar.selectbox(
    '1. Produto Selecionado:',
    produtos_disponiveis,
    index=produtos_disponiveis.tolist().index(produto_padrao)
)

# Seletor de Regiões:
regioes = df['Regiao'].unique()
regioes_selecionadas = st.sidebar.multiselect(
    '2. Regiões de Análise:',
    regioes,
    default=regioes.tolist()
)

# Seletor de Estados:
if regioes_selecionadas:
    df_regioes_filtrado = df[df['Regiao'].isin(regioes_selecionadas)]

    estados_na_regiao = sorted(df_regioes_filtrado['Estado'].unique())

    estados_selecionados = st.sidebar.multiselect(
        '3. Estados para Comparação Temporal:',
        estados_na_regiao,
        default=estados_na_regiao[:5]
    )
else:
    estados_selecionados = []
    st.sidebar.warning('Selecione pelo menos uma Região.')

# Seletor de Ano:
anos_diponiveis = sorted(
    df['Data'].dt.year.dropna().astype(int).unique().tolist(), 
    reverse=True
)

if not anos_diponiveis:
    st.sidebar.error('Não há anos disponíveis no dataset.')
    ano_selecionado = None
else:
    ano_padrao = 2020 if 2020 in anos_diponiveis else anos_diponiveis[0]
    idx_padrao = anos_diponiveis.index(ano_padrao)

    ano_selecionado = st.sidebar.selectbox(
        '4. Ano de Análise (Máximo/Mínimo):',
        anos_diponiveis,
        index=idx_padrao,
    )

# Informações do Autor
st.sidebar.markdown('---')
st.sidebar.markdown('**✨ Desenvolvido por Fillipe Berssot**')

st.sidebar.markdown('**Links:**')

st.sidebar.markdown(
    """
    <div style="display: flex; flex-direction: column; gap: 5px;">
        <a href="https://www.linkedin.com/in/fillipe-berssot/" target="_blank" style="text-decoration: none; color: inherit;">
            <span style="font-size: 1.2em;">💼</span> LinkedIn
        </a>
        <a href="https://github.com/FillipeBerssot" target="_blank" style="text-decoration: none; color: inherit;">
            <span style="font-size: 1.2em;">💻</span> GitHub
        </a>
        <a href="mailto:fillipeberssot95@hotmail.com" style="text-decoration: none; color: inherit;">
            <span style="font-size: 1.2em;">📧</span> E-mail
        </a>
    </div>
    """, 
    unsafe_allow_html=True
)

# Exibição da pagina principal:
st.title(f'📈 Preços de {produto_selecionado}: Análise Comparativa')
st.markdown('Dashboard interativo para entender a diferença de preços, a volatilidade e as tendências de mercado (2013-2025)')

col1, mid, col2 = st.columns([1, 0.07, 1], vertical_alignment='top')

# Comparação Direta
# Preco minimo atual
with col1:
    st.header("🏆 Menor Preço em 2025")

    df_comparacao_filtrado = preparar_comparacao_temporal(produto_selecionado, estados_selecionados)

    estado_mais_barato, preco_mais_barato = preco_mais_barato_atual(df_comparacao_filtrado)

    if estado_mais_barato != 'N/A':
        st.metric(
            label=f'Estado Mais Barato (2025)',
            value=f'R$ {preco_mais_barato:.3f}',
            delta=estado_mais_barato,
            delta_color='normal'
        )
    else:
        st.info('Selecione estados para a comparação de menor preço.')

    st.markdown('---')

    # Preco maximo atual
    st.subheader(f'❌ Maior Preço em 2025')

    df_comparacao_filtrado = preparar_comparacao_temporal(produto_selecionado, estados_selecionados)

    estado_mais_caro, preco_mais_caro = preco_mais_caro_atual(df_comparacao_filtrado)

    if estado_mais_caro != 'N/A':
        st.metric(
            label=f'Estado Mais Caro (2025)',
            value=f'R$ {preco_mais_caro:.3f}',
            delta=estado_mais_caro,
            delta_color='inverse'
        )
# Divider vertical:
with mid:
    vr(height=440, thickness=1, top=28)

# Menor preço de acordo com estado e ano selecionado:
with col2:
    st.header(f'🏆 Menor Preço em {ano_selecionado}')

    estado_min_anual, preco_min_anual = preco_mais_barato_anual(
        produto_selecionado,
        ano_selecionado,
        estados_selecionados,
        )
    if estado_min_anual != 'N/A':
        st.metric(
            label=f'Estado Mais Barato em {ano_selecionado}',
            value=f'R$ {preco_min_anual:.3f}',
            delta=estado_min_anual,
            delta_color='normal'
        )
    else:
        st.info(f'Dados indisponíveis para {ano_selecionado}.')

    st.markdown('---')

    # Maior preço de acordo com estado e ano selecionado:
    st.subheader(f'❌ Maior Preço em {ano_selecionado}')

    estado_max_anual, preco_max_anual = preco_mais_caro_anual(
        produto_selecionado,
        ano_selecionado,
        estados_selecionados,
    )
    if estado_max_anual != 'N/A':
        st.metric(
            label=f'Estado Mais Caro em {ano_selecionado}',
            value=f'R$ {preco_max_anual:.3f}',
            delta=estado_max_anual,
            delta_color='inverse'
        )
    else:
        st.info(f'Dados indisponíveis para {ano_selecionado}.')

st.markdown('---')

# Gráfico de faixa anual (Max/Min):
st.header(f'Volatilidade de Preços (Máx/Mín) em {ano_selecionado}')

df_faixa = calcular_faixa_anual(produto_selecionado, ano_selecionado)

st.plotly_chart(
    plot_faixa_anual(df_faixa, produto_selecionado, ano_selecionado),
    use_container_width=True
)

# Gráfico de comparação temporal:
st.markdown('---')
if estados_selecionados:
    st.header(f'Evolução Temporal: Comparação entre Estados')

    st.plotly_chart(
        plot_comparacao_temporal(df_comparacao_filtrado, produto_selecionado),
        use_container_width=True
    )
else:
    st.warning('Selecione pelo menos um estado no filtro lateral para visualizar a comparação temporal.')