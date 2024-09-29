import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Carregar os dados
file_lojas_path = 'tabela_estrutura_lojas.xlsx'
file_vendas_path = 'tabela_vendas.xlsx'
file_perfil_clientes_path = 'tabela_perfil_clientes.xlsx'

df_lojas = pd.read_excel(file_lojas_path)
df_vendas = pd.read_excel(file_vendas_path)
df_perfil_clientes = pd.read_excel(file_perfil_clientes_path)

# Merge dos dados
df_vendas_lojas = df_vendas.merge(df_lojas, on='CODIGO_LOJA', how='left')
df_vendas_com_perfil = df_vendas.merge(df_perfil_clientes, on='CODIGO_CLIENTE', how='left')

# Cálculos de faturamento geral
faturamento_por_mes = df_vendas.groupby('MES')['FATURAMENTO_BRUTO'].sum().reset_index()
faturamento_por_rede_mes = df_vendas_lojas.groupby(['MES', 'NOME_SUPERMERCADO'])['FATURAMENTO_BRUTO'].sum().reset_index()

# Cálculo de faturamento por perfil
faturamento_por_perfil_a = df_vendas_com_perfil.groupby('PERFIL_SUPERMERCADO_A')['FATURAMENTO_BRUTO'].sum().reset_index()
faturamento_por_perfil_b = df_vendas_com_perfil.groupby('PERFIL_SUPERMERCADO_B')['FATURAMENTO_BRUTO'].sum().reset_index()

# Cálculo de variação de faturamento por categoria
faturamento_categoria_rede_mes = df_vendas_lojas.groupby(['MES', 'NOME_SUPERMERCADO', 'NOME_CATEGORIA'])['FATURAMENTO_BRUTO'].sum().unstack(level=0)
faturamento_categoria_variacao = ((faturamento_categoria_rede_mes['FEVEREIRO'] - faturamento_categoria_rede_mes['JANEIRO']) / faturamento_categoria_rede_mes['JANEIRO']) * 100

# Preparar dados para gráficos de variação por categoria
faturamento_categoria_variacao_a = faturamento_categoria_variacao.loc['SUPERMERCADO A'].reset_index()
faturamento_categoria_variacao_a.columns = ['NOME_CATEGORIA', 'VARIACAO_PERC']

faturamento_categoria_variacao_b = faturamento_categoria_variacao.loc['SUPERMERCADO B'].reset_index()
faturamento_categoria_variacao_b.columns = ['NOME_CATEGORIA', 'VARIACAO_PERC']

# Inicializando o aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo com cores da marca Pão de Açúcar
app.layout = html.Div(style={'backgroundColor': '#FFFFFF'}, children=[
    html.H1("Dashboard de Análise de Vendas - Pão de Açúcar", style={'text-align': 'center', 'color': '#6CAF60'}),

    dcc.Tabs(style={'font-size': '18px', 'background-color': '#6CAF60'}, children=[
        dcc.Tab(label='Resumo de Faturamento', children=[
            html.Div([
                html.H2("Crescimento de Faturamento Mensal", style={'color': '#6CAF60'}),
                dcc.Graph(
                    figure=px.bar(faturamento_por_mes, x='MES', y='FATURAMENTO_BRUTO',
                                  title="Faturamento por Mês", color_discrete_sequence=['#6CAF60'])
                    .update_layout(
                        annotations=[dict(text="Este gráfico mostra o crescimento do faturamento entre os meses de janeiro e fevereiro.", 
                                          xref='paper', yref='paper', showarrow=False, x=0.5, y=1.15,
                                          font=dict(size=12, color="black"))]
                    )
                ),
            ]),
            html.Div([
                html.H2("Faturamento por Rede", style={'color': '#6CAF60'}),
                dcc.Graph(
                    figure=px.bar(faturamento_por_rede_mes, x='MES', y='FATURAMENTO_BRUTO', color='NOME_SUPERMERCADO',
                                  barmode='group', title="Faturamento por Rede e Mês", color_discrete_map={
                                      'SUPERMERCADO A': '#6CAF60', 'SUPERMERCADO B': '#FFD700'})
                    .update_layout(
                        annotations=[dict(text="Compara o faturamento entre os Supermercados A e B nos meses de janeiro e fevereiro.", 
                                          xref='paper', yref='paper', showarrow=False, x=0.5, y=1.15,
                                          font=dict(size=12, color="black"))]
                    )
                ),
            ]),
        ]),

        dcc.Tab(label='Perfis de Clientes', children=[
            html.Div([
                html.H2("Faturamento por Perfil de Cliente - Supermercado A", style={'color': '#6CAF60'}),
                dcc.Graph(
                    figure=px.bar(faturamento_por_perfil_a, x='PERFIL_SUPERMERCADO_A', y='FATURAMENTO_BRUTO', 
                                  title="Supermercado A - Faturamento por Perfil de Cliente", color_discrete_sequence=['#6CAF60'])
                    .update_layout(
                        annotations=[dict(text="Este gráfico destaca os perfis de clientes que mais contribuem para o faturamento do Supermercado A.", 
                                          xref='paper', yref='paper', showarrow=False, x=0.5, y=1.15,
                                          font=dict(size=12, color="black"))]
                    )
                ),
            ]),
            html.Div([
                html.H2("Faturamento por Perfil de Cliente - Supermercado B", style={'color': '#FFD700'}),
                dcc.Graph(
                    figure=px.bar(faturamento_por_perfil_b, x='PERFIL_SUPERMERCADO_B', y='FATURAMENTO_BRUTO', 
                                  title="Supermercado B - Faturamento por Perfil de Cliente", color_discrete_sequence=['#FFD700'])
                    .update_layout(
                        annotations=[dict(text="Este gráfico destaca os perfis de clientes que mais contribuem para o faturamento do Supermercado B.", 
                                          xref='paper', yref='paper', showarrow=False, x=0.5, y=1.15,
                                          font=dict(size=12, color="black"))]
                    )
                ),
            ]),
        ]),

        dcc.Tab(label='Análise por Categoria', children=[
            html.Div([
                html.H2("Variação Percentual por Categoria - Supermercado A", style={'color': '#6CAF60'}),
                dcc.Graph(
                    figure=px.bar(faturamento_categoria_variacao_a, x='NOME_CATEGORIA', y='VARIACAO_PERC',
                                  title="Supermercado A - Variação Percentual por Categoria", color_discrete_sequence=['#6CAF60'])
                    .update_layout(
                        annotations=[dict(text="Este gráfico mostra a variação percentual do faturamento de cada categoria no Supermercado A.", 
                                          xref='paper', yref='paper', showarrow=False, x=0.5, y=1.15,
                                          font=dict(size=12, color="black"))]
                    )
                ),
            ]),
            html.Div([
                html.H2("Variação Percentual por Categoria - Supermercado B", style={'color': '#FFD700'}),
                dcc.Graph(
                    figure=px.bar(faturamento_categoria_variacao_b, x='NOME_CATEGORIA', y='VARIACAO_PERC',
                                  title="Supermercado B - Variação Percentual por Categoria", color_discrete_sequence=['#FFD700'])
                    .update_layout(
                        annotations=[dict(text="Este gráfico mostra a variação percentual do faturamento de cada categoria no Supermercado B.", 
                                          xref='paper', yref='paper', showarrow=False, x=0.5, y=1.15,
                                          font=dict(size=12, color="black"))]
                    )
                ),
            ]),
        ]),

        dcc.Tab(label='Fluxo e Ticket Médio', children=[
            html.Div([
                html.H2("Fluxo de Consumidores por Mês - Supermercado A", style={'color': '#6CAF60'}),
                dcc.Graph(
                    figure=px.bar(x=['Janeiro', 'Fevereiro'], y=[45141, 42095], 
                                  labels={'x': 'Mês', 'y': 'Número de Cupons Fiscais'}, 
                                  title="Fluxo de Consumidores - Supermercado A", color_discrete_sequence=['#6CAF60'])
                    .update_layout(
                        annotations=[dict(text="Este gráfico compara o fluxo de consumidores no Supermercado A entre janeiro e fevereiro.", 
                                          xref='paper', yref='paper', showarrow=False, x=0.5, y=1.15,
                                          font=dict(size=12, color="black"))]
                    )
                ),
            ]),
            html.Div([
                html.H2("Ticket Médio por Mês - Supermercado A", style={'color': '#6CAF60'}),
                dcc.Graph(
                    figure=px.bar(x=['Janeiro', 'Fevereiro'], y=[56.35, 59.79], 
                                  labels={'x': 'Mês', 'y': 'Ticket Médio (R$)'}, 
                                  title="Ticket Médio - Supermercado A", color_discrete_sequence=['#6CAF60'])
                    .update_layout(
                        annotations=[dict(text="Este gráfico compara o ticket médio no Supermercado A entre janeiro e fevereiro.", 
                                          xref='paper', yref='paper', showarrow=False, x=0.5, y=1.15,
                                          font=dict(size=12, color="black"))]
                    )
                ),
            ]),
            html.Div([
                html.H2("Fluxo de Consumidores por Mês - Supermercado B", style={'color': '#FFD700'}),
                dcc.Graph(
                    figure=px.bar(x=['Janeiro', 'Fevereiro'], y=[21287, 21021], 
                                  labels={'x': 'Mês', 'y': 'Número de Cupons Fiscais'}, 
                                  title="Fluxo de Consumidores - Supermercado B", color_discrete_sequence=['#FFD700'])
                    .update_layout(
                        annotations=[dict(text="Este gráfico compara o fluxo de consumidores no Supermercado B entre janeiro e fevereiro.", 
                                          xref='paper', yref='paper', showarrow=False, x=0.5, y=1.15,
                                          font=dict(size=12, color="black"))]
                    )
                ),
            ]),
            html.Div([
                html.H2("Ticket Médio por Mês - Supermercado B", style={'color': '#FFD700'}),
                dcc.Graph(
                    figure=px.bar(x=['Janeiro', 'Fevereiro'], y=[88.13, 121.00], 
                                  labels={'x': 'Mês', 'y': 'Ticket Médio (R$)'}, 
                                  title="Ticket Médio - Supermercado B", color_discrete_sequence=['#FFD700'])
                    .update_layout(
                        annotations=[dict(text="Este gráfico compara o ticket médio no Supermercado B entre janeiro e fevereiro.", 
                                          xref='paper', yref='paper', showarrow=False, x=0.5, y=1.15,
                                          font=dict(size=12, color="black"))]
                    )
                ),
            ]),
        ]),
    ])
])

# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
