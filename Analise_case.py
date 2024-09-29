import pandas as pd
import matplotlib.pyplot as plt

file_lojas_path = 'tabela_estrutura_lojas.xlsx'
file_vendas_path = 'tabela_vendas.xlsx'

df_lojas = pd.read_excel(file_lojas_path)
df_vendas = pd.read_excel(file_vendas_path)
df_lojas_preview = df_lojas.head()
df_vendas_preview = df_vendas.head()
df_lojas_preview, df_vendas_preview



faturamento_por_mes = df_vendas.groupby('MES')['FATURAMENTO_BRUTO'].sum()
faturamento_janeiro = faturamento_por_mes.get('JANEIRO', 0)
faturamento_fevereiro = faturamento_por_mes.get('FEVEREIRO', 0)
df_vendas_lojas = df_vendas.merge(df_lojas, on='CODIGO_LOJA', how='left')
faturamento_por_rede_mes = df_vendas_lojas.groupby(['MES', 'NOME_SUPERMERCADO'])['FATURAMENTO_BRUTO'].sum().unstack()
faturamento_janeiro_por_rede = faturamento_por_rede_mes.loc['JANEIRO']
faturamento_fevereiro_por_rede = faturamento_por_rede_mes.loc['FEVEREIRO']
crescimento_faturamento = ((faturamento_fevereiro - faturamento_janeiro) / faturamento_janeiro) * 100
crescimento_faturamento_por_rede = ((faturamento_fevereiro_por_rede - faturamento_janeiro_por_rede) / faturamento_janeiro_por_rede) * 100
crescimento_faturamento, crescimento_faturamento_por_rede


colors = ['green' if value > 0 else 'red' for value in crescimento_faturamento_por_rede]
fig, ax = plt.subplots()
bars = crescimento_faturamento_por_rede.plot(kind='bar', ax=ax, color=colors)

ax.set_title('Variação Percentual no Faturamento - Fevereiro vs Janeiro')
ax.set_ylabel('Variação Percentual (%)')
ax.set_xlabel('Supermercado')
ax.axhline(0, color='black', linewidth=1)

handles = [
    plt.Line2D([0], [0], color='green', lw=4, label=f'Supermercado B: {crescimento_faturamento_por_rede["SUPERMERCADO B"]:.2f}%'),
    plt.Line2D([0], [0], color='red', lw=4, label=f'Supermercado A: {crescimento_faturamento_por_rede["SUPERMERCADO A"]:.2f}%')
]
ax.legend(handles=handles, loc='upper right')

plt.xticks(rotation=0)
plt.tight_layout()
plt.show()



faturamento_categoria_rede_mes = df_vendas_lojas.groupby(['MES', 'NOME_SUPERMERCADO', 'NOME_CATEGORIA'])['FATURAMENTO_BRUTO'].sum().unstack(level=0)
faturamento_categoria_variacao = ((faturamento_categoria_rede_mes['FEVEREIRO'] - faturamento_categoria_rede_mes['JANEIRO']) / faturamento_categoria_rede_mes['JANEIRO']) * 100

categoria_puxa_cima_a = faturamento_categoria_variacao.loc['SUPERMERCADO A'].idxmax()
categoria_puxa_baixo_a = faturamento_categoria_variacao.loc['SUPERMERCADO A'].idxmin()

categoria_puxa_cima_b = faturamento_categoria_variacao.loc['SUPERMERCADO B'].idxmax()
categoria_puxa_baixo_b = faturamento_categoria_variacao.loc['SUPERMERCADO B'].idxmin()

valor_cima_a = faturamento_categoria_variacao.loc['SUPERMERCADO A', categoria_puxa_cima_a]
valor_baixo_a = faturamento_categoria_variacao.loc['SUPERMERCADO A', categoria_puxa_baixo_a]

valor_cima_b = faturamento_categoria_variacao.loc['SUPERMERCADO B', categoria_puxa_cima_b]
valor_baixo_b = faturamento_categoria_variacao.loc['SUPERMERCADO B', categoria_puxa_baixo_b]

resultados = {
    "Supermercado A": {
        "Puxa para cima (categoria)": categoria_puxa_cima_a,
        "Variação para cima (%)": valor_cima_a,
        "Puxa para baixo (categoria)": categoria_puxa_baixo_a,
        "Variação para baixo (%)": valor_baixo_a
    },
    "Supermercado B": {
        "Puxa para cima (categoria)": categoria_puxa_cima_b,
        "Variação para cima (%)": valor_cima_b,
        "Puxa para baixo (categoria)": categoria_puxa_baixo_b,
        "Variação para baixo (%)": valor_baixo_b
    }
}

resultados


fig, axs = plt.subplots(1, 2, figsize=(12, 6))

categorias_a = ['BEBIDAS (Cima)', 'LIMPEZA (Baixo)']
variacao_a = [valor_cima_a, valor_baixo_a]
colors_a = ['green', 'red']

bars_a = axs[0].bar(categorias_a, variacao_a, color=colors_a)
axs[0].set_title('Supermercado A - Variação por Categoria')
axs[0].set_ylabel('Variação Percentual (%)')
axs[0].axhline(0, color='black', linewidth=1)
for bar, valor in zip(bars_a, variacao_a):
    axs[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{valor:.2f}%', 
                ha='center', va='bottom' if valor > 0 else 'top')

categorias_b = ['BEBIDAS (Cima)', 'CESTA BASICA (Baixo)']
variacao_b = [valor_cima_b, valor_baixo_b]
colors_b = ['green', 'red']
bars_b = axs[1].bar(categorias_b, variacao_b, color=colors_b)
axs[1].set_title('Supermercado B - Variação por Categoria')
axs[1].axhline(0, color='black', linewidth=1)
for bar, valor in zip(bars_b, variacao_b):
    axs[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{valor:.2f}%', 
                ha='center', va='bottom' if valor > 0 else 'top')

plt.tight_layout()
plt.show()


file_perfil_clientes_path = 'tabela_perfil_clientes.xlsx'
df_perfil_clientes = pd.read_excel(file_perfil_clientes_path)
df_perfil_clientes.head()


df_vendas_com_perfil = df_vendas.merge(df_perfil_clientes, on='CODIGO_CLIENTE', how='left')
faturamento_por_perfil_a = df_vendas_com_perfil.groupby('PERFIL_SUPERMERCADO_A')['FATURAMENTO_BRUTO'].sum()
faturamento_por_perfil_b = df_vendas_com_perfil.groupby('PERFIL_SUPERMERCADO_B')['FATURAMENTO_BRUTO'].sum()
faturamento_por_perfil_a_sorted = faturamento_por_perfil_a.sort_values(ascending=False)
faturamento_por_perfil_b_sorted = faturamento_por_perfil_b.sort_values(ascending=False)
faturamento_por_perfil_a_sorted, faturamento_por_perfil_b_sorted


fig, axs = plt.subplots(1, 2, figsize=(14, 6))
bars_a = faturamento_por_perfil_a_sorted.plot(kind='bar', ax=axs[0], color='skyblue')
axs[0].set_title('Supermercado A - Faturamento por Perfil')
axs[0].set_ylabel('Faturamento Bruto (R$)')
axs[0].set_xlabel('Perfil')
axs[0].tick_params(axis='x', rotation=45)
for bar in bars_a.patches:
    axs[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'R${bar.get_height():,.2f}', 
                ha='center', va='bottom')

bars_b = faturamento_por_perfil_b_sorted.plot(kind='bar', ax=axs[1], color='lightgreen')
axs[1].set_title('Supermercado B - Faturamento por Perfil')
axs[1].set_ylabel('Faturamento Bruto (R$)')
axs[1].set_xlabel('Perfil')
axs[1].tick_params(axis='x', rotation=45)
for bar in bars_b.patches:
    axs[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'R${bar.get_height():,.2f}', 
                ha='center', va='bottom')
plt.tight_layout()
plt.show()



fluxo_consumidores_a = df_vendas_lojas[df_vendas_lojas['NOME_SUPERMERCADO'] == 'SUPERMERCADO A'].groupby('MES')['CODIGO_CUPOM_FISCAL'].nunique()
fluxo_consumidores_b = df_vendas_lojas[df_vendas_lojas['NOME_SUPERMERCADO'] == 'SUPERMERCADO B'].groupby('MES')['CODIGO_CUPOM_FISCAL'].nunique()
ticket_medio_a = df_vendas_lojas[df_vendas_lojas['NOME_SUPERMERCADO'] == 'SUPERMERCADO A'].groupby('MES')['FATURAMENTO_BRUTO'].sum() / fluxo_consumidores_a
ticket_medio_b = df_vendas_lojas[df_vendas_lojas['NOME_SUPERMERCADO'] == 'SUPERMERCADO B'].groupby('MES')['FATURAMENTO_BRUTO'].sum() / fluxo_consumidores_b

{
    'Fluxo de Consumidores - Supermercado A': fluxo_consumidores_a,
    'Ticket Médio - Supermercado A': ticket_medio_a,
    'Fluxo de Consumidores - Supermercado B': fluxo_consumidores_b,
    'Ticket Médio - Supermercado B': ticket_medio_b
}


fig, axs = plt.subplots(2, 2, figsize=(14, 12))
axs[0, 0].bar(['Janeiro', 'Fevereiro'], fluxo_consumidores_a, color='lightgreen')
axs[0, 0].set_title('Supermercado A - Fluxo de Consumidores')
axs[0, 0].set_ylabel('Número de Cupons Fiscais')
for i, valor in enumerate(fluxo_consumidores_a):
    axs[0, 0].text(i, valor, f'{valor}', ha='center', va='bottom')

axs[0, 1].bar(['Janeiro', 'Fevereiro'], ticket_medio_a, color='lightgreen')
axs[0, 1].set_title('Supermercado A - Ticket Médio')
axs[0, 1].set_ylabel('Ticket Médio (R$)')
for i, valor in enumerate(ticket_medio_a):
    axs[0, 1].text(i, valor, f'R${valor:.2f}', ha='center', va='bottom')

axs[1, 0].bar(['Janeiro', 'Fevereiro'], fluxo_consumidores_b, color='skyblue')
axs[1, 0].set_title('Supermercado B - Fluxo de Consumidores')
axs[1, 0].set_ylabel('Número de Cupons Fiscais')
for i, valor in enumerate(fluxo_consumidores_b):
    axs[1, 0].text(i, valor, f'{valor}', ha='center', va='bottom')

axs[1, 1].bar(['Janeiro', 'Fevereiro'], ticket_medio_b, color='skyblue')
axs[1, 1].set_title('Supermercado B - Ticket Médio')
axs[1, 1].set_ylabel('Ticket Médio (R$)')
for i, valor in enumerate(ticket_medio_b):
    axs[1, 1].text(i, valor, f'R${valor:.2f}', ha='center', va='bottom')

plt.tight_layout()
plt.show()