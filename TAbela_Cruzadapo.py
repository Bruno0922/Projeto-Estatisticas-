import pandas as pd
import numpy as np

COL_ESCOLARIDADE = 'EdLevel'
COL_LINGUAGENS = 'LanguageHaveWorkedWith'
COL_NOVA_LINGUAGEM = 'Linguagem'

def carregar_e_processar_dados(nome_arquivo_excel, nome_aba, ano):
    """
    Carrega o DataFrame, gera a tabulação cruzada bruta e calcula as porcentagens.
    """
    print(f"--- Processando dados Stack Overflow {ano} (Aba: {nome_aba}) ---")
    
    # Carregar o DataFrame
    try:
        df = pd.read_excel(nome_arquivo_excel, sheet_name=nome_aba)
    except Exception as e:
        print(f"❌ ERRO ao carregar arquivo/aba: {e}")
        return None, None # Retorna None para ambas as tabelas
    
    # 1. Limpeza de dados
    df_limpo = df.dropna(subset=[COL_ESCOLARIDADE, COL_LINGUAGENS])
    
    # 2. Desagregação das linguagens
    df_linguagens_separadas = (
        df_limpo[COL_LINGUAGENS].astype(str).str.split(';', expand=True).stack().reset_index(level=1, drop=True)
    )
    df_linguagens_separadas.name = COL_NOVA_LINGUAGEM
    df_long = df_limpo[[COL_ESCOLARIDADE]].join(df_linguagens_separadas)
    
    # 3. Gerar a Tabulação Cruzada (Contagem Bruta)
    tabela_bruta = pd.crosstab(
        index=df_long[COL_ESCOLARIDADE],
        columns=df_long[COL_NOVA_LINGUAGEM],
        margins=True,
        margins_name='Total'
    )
    
    # 4. Calcular a Tabulação Cruzada em Porcentagem
    # Normalize 'index' = 0 calcula a porcentagem por COLUNA
    # Normalize 'index' = 1 calcula a porcentagem por LINHA (Escolaridade) <-- ESTE É O FOCO!
    tabela_percentual = pd.crosstab(
        index=df_long[COL_ESCOLARIDADE],
        columns=df_long[COL_NOVA_LINGUAGEM],
        normalize='index' # Normaliza por linha (o total de programadores naquele nível)
    )
    # Formatação para porcentagem (opcional, mas facilita a leitura no Excel)
    tabela_percentual = (tabela_percentual * 100).round(2).astype(str) + '%'
    
    # 5. Salvar os entregáveis
    nome_excel_bruta = f'analise_cruzada_bruta_{ano}.xlsx'
    tabela_bruta.to_excel(nome_excel_bruta)
    print(f"✅ Contagem Bruta salva: {nome_excel_bruta}")
    
    nome_excel_perc = f'analise_cruzada_percentual_{ano}.xlsx'
    tabela_percentual.to_excel(nome_excel_perc)
    print(f"✅ Porcentagem por Escolaridade salva: {nome_excel_perc}")
    
    return tabela_bruta, tabela_percentual

# --- Execução para os anos 2024 e 2022 ---

# DEFINIÇÕES DE ARQUIVOS (VERIFIQUE NOVAMENTE OS NOMES)
nome_arquivo_excel = "analise_pesquisa_2024_2022.xlsx" # Nome do seu arquivo Excel principal
aba_2024 = "survey_results_2024" 
aba_2022 = "survey_results_2022" 

# Execute as funções
tabela_bruta_2024, tabela_perc_2024 = carregar_e_processar_dados(nome_arquivo_excel, aba_2024, 2024)
tabela_bruta_2022, tabela_perc_2022 = carregar_e_processar_dados(nome_arquivo_excel, aba_2022, 2022)

print("\nProcessamento de contagens brutas e porcentagens concluído.")