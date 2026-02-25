import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregue seu CSV (ajuste o caminho)
df = pd.read_csv("Dados_Tratados/tabela7240_tratada_long.csv", sep=';')

# Filtra apenas população geral (Total / Total)
df_geral = df[(df['Quesito_Indigena'] == 'Total') & (df['Localizacao_Domicilio'] == 'Total')]

# 1. População Total por Região e Ano (apenas 'Categoria' == 'Total' e 'Sexo' == 'Total')
df_total = df_geral[(df_geral['Categoria'] == 'Total') & (df_geral['Sexo'] == 'Total')]

plt.figure(figsize=(10, 6))
sns.barplot(data=df_total, x='Regiao_UF', y='Quantidade', hue='Ano', palette='viridis')
plt.title('População Total (15+ anos) por Grande Região - 2010 vs 2022')
plt.ylabel('Quantidade (em milhões)')
plt.xlabel('Região / UF')
plt.xticks(rotation=45)
plt.legend(title='Ano')
plt.tight_layout()
plt.show()  # ou plt.savefig('pop_total_regioes.png')

# 2. Taxa de alfabetização por região e ano
df_pivot = df_geral.pivot_table(
    index=['Regiao_UF', 'Ano'],
    columns=['Categoria'],
    values='Quantidade',
    aggfunc='sum'
).reset_index()

df_pivot['% Alfabetizadas'] = df_pivot['Alfabetizadas'] / df_pivot['Total'] * 100
df_pivot['% Nao Alfabetizadas'] = 100 - df_pivot['% Alfabetizadas']

plt.figure(figsize=(12, 6))
sns.barplot(data=df_pivot, x='Regiao_UF', y='% Alfabetizadas', hue='Ano', palette='Blues')
plt.title('Taxa de Alfabetização (%) - População 15+ anos')
plt.ylabel('% Alfabetizadas')
plt.ylim(70, 100)
plt.xticks(rotation=45)
plt.legend(title='Ano')
plt.tight_layout()
plt.show()

# 3. Não alfabetizados em 2022 por sexo
df_nao_2022 = df_geral[(df_geral['Ano'] == 2022) & (df_geral['Categoria'] == 'NaoAlfabetizadas') & (df_geral['Sexo'] != 'Total')]

plt.figure(figsize=(10, 6))
sns.barplot(data=df_nao_2022, x='Regiao_UF', y='Quantidade', hue='Sexo', palette='Reds')
plt.title('População Não Alfabetizada (2022) por Região e Sexo')
plt.ylabel('Quantidade')
plt.xticks(rotation=45)
plt.legend(title='Sexo')
plt.tight_layout()
plt.show()