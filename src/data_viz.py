import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# Divider vertical de altura fixa
def vr(height=360, thickness=1, top=24):
    st.markdown(
        f"""
        <div style="display:flex; justify-content:center;">
          <div class="vr-line" style="height:{height}px; border-left-width:{thickness}px; margin-top:{top}px;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Grafico de comparação temporal (PREÇO X ESTADO)
def plot_comparacao_temporal(df_comparacao, produto):
    fig = px.line(
        df_comparacao,
        x='Data',
        y='Preco_Medio_Revenda',
        color='Estado',
        title=f'Evolução do Preço Médio de {produto} por Estado',
        labels={'Preco_Medio_Revenda': 'Preço Médio (R$/L)', 'Data': 'Mês/Ano'},
        line_shape='linear'
    )

    fig.update_layout(
        plot_bgcolor = '#f0f2f6',
        margin=dict(t=50, l=0, r=0, b=0),
        hovermode= 'x unified'
    )

    return fig

# Grafico de faixa anual (Maximo e Minimo):
def plot_faixa_anual(df_faixa, produto, ano):
    df_plot = df_faixa.sort_values(by='Amplitude', ascending=False)

    fig = px.bar(
        df_plot,
        x='Estado',
        y='max',
        title=f'Volatilidade de Preços (Máx/Mín) de {produto} em {ano}',
        labels={'max': 'Preço Máximo (R$/L)', 'Estado': 'Estado'},
        color='Amplitude',
        color_continuous_scale=px.colors.sequential.Agsunset,
        text_auto='.2f'
    )

    fig.add_trace(go.Scatter(
        x=df_plot['Estado'],
        y=df_plot['min'],
        mode='markers+text',
        name='Preço Mínimo',
        marker=dict(color='black', size=10, symbol='line-ew-open'),
        text=df_plot['min'].apply(lambda x: f'R$ {x:.2f}'),
        textposition='bottom center'
    ))

    fig.update_layout(
        hovermode='x',
        showlegend=False,
        plot_bgcolor='#f0f2f6',
        xaxis={'categoryorder': 'array', 'categoryarray': df_plot['Estado']}
    )

    return fig