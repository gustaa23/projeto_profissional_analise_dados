import pandas as pd
from pathlib import Path

# Configuração
PASTA_BASE = Path(__file__).parent.resolve()
ARQUIVO = PASTA_BASE / "Dados" / "tabela7240.xlsx"
PASTA_SAIDA = PASTA_BASE / "Dados_Tratados"
ARQUIVO_SAIDA = PASTA_SAIDA / "tabela7240_tratada_long.csv"

PASTA_SAIDA.mkdir(exist_ok=True)

print("Iniciando tratamento da tabela 7240...")
print(f"Arquivo: {ARQUIVO}")

try:
    # Leitura raw para diagnóstico e controle
    df_raw = pd.read_excel(
        ARQUIVO,
        engine="openpyxl",
        sheet_name=0,          # mude se a aba não for a primeira
        header=None,
        dtype=str
    )

    print(f"Linhas brutas lidas: {len(df_raw)}")

    # Remove linhas totalmente vazias
    df_raw = df_raw.dropna(how='all').reset_index(drop=True)

    # Pula as ~9 linhas de cabeçalho (dados começam na linha índice 8 → iloc[8:])
    CABECALHO_LINHAS = 9
    df = df_raw.iloc[CABECALHO_LINHAS:].reset_index(drop=True)

    # Remove colunas totalmente vazias (se houver)
    df = df.loc[:, df.notna().any()]

    print(f"Colunas após limpeza: {len(df.columns)}")
    print("Primeiras 5 linhas dos dados (depois do cabeçalho):")
    print(df.head(5).to_string(index=False))

    # Define nomes realistas para as 21 colunas (baseado na estrutura IBGE)
    # Ajuste se necessário após ver o print acima
    colunas = [
        'Regiao_UF',
        'Quesito_Indigena',
        'Localizacao_Domicilio',
        # 2010
        '2010_Total_Total',
        '2010_Total_Homens',
        '2010_Total_Mulheres',
        '2010_Alfabetizadas_Total',
        '2010_Alfabetizadas_Homens',
        '2010_Alfabetizadas_Mulheres',
        '2010_NaoAlfabetizadas_Total',
        '2010_NaoAlfabetizadas_Homens',
        '2010_NaoAlfabetizadas_Mulheres',
        # 2022
        '2022_Total_Total',
        '2022_Total_Homens',
        '2022_Total_Mulheres',
        '2022_Alfabetizadas_Total',
        '2022_Alfabetizadas_Homens',
        '2022_Alfabetizadas_Mulheres',
        '2022_NaoAlfabetizadas_Total',
        '2022_NaoAlfabetizadas_Homens',
        '2022_NaoAlfabetizadas_Mulheres'
    ]

    if len(df.columns) == len(colunas):
        df.columns = colunas
    else:
        df.columns = [f"col_{i}" for i in range(len(df.columns))]
        print(f"Aviso: número de colunas ({len(df.columns)}) não bate com {len(colunas)} nomes sugeridos")

    # Converte valores numéricos (remove pontos de milhar, etc.)
    for col in df.columns[3:]:  # a partir das colunas numéricas
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(r'\.', '', regex=True).str.replace(r'[^\d-]', '', regex=True),
            errors='coerce'
        )

    # Filtra linhas úteis (regiões, Brasil, estados indígenas, etc.)
    df = df[df['Regiao_UF'].str.contains(
        r"(Norte|Nordeste|Sudeste|Sul|Centro-Oeste|Brasil|Em terras|Fora de terras|Cor ou raça indígena)",
        case=False, na=False
    )].reset_index(drop=True)

    # Transforma para formato longo (melt) - recomendado para análise posterior
    df_long = pd.melt(
        df,
        id_vars=['Regiao_UF', 'Quesito_Indigena', 'Localizacao_Domicilio'],
        value_vars=df.columns[3:],
        var_name='Ano_Categoria_Sexo',
        value_name='Quantidade'
    )

    # Separa Ano, Categoria e Sexo (opcional, mas útil)
    df_long[['Ano', 'Categoria', 'Sexo']] = df_long['Ano_Categoria_Sexo'].str.split('_', expand=True, n=2)
    df_long = df_long.drop(columns=['Ano_Categoria_Sexo'])

    # Salva
    df_long.to_csv(ARQUIVO_SAIDA, index=False, encoding='utf-8-sig', sep=';')

    print("\nTratamento concluído com sucesso!")
    print(f"Salvo em: {ARQUIVO_SAIDA}")
    print(f"Shape final (long format): {df_long.shape}")
    print("\nPrimeiras 10 linhas do resultado:")
    print(df_long.head(10))

except Exception as e:
    print("Erro durante o processamento:")
    print(e)