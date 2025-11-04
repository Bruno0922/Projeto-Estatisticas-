import pandas as pd
import numpy as np 

COL_ESCOLARIDADE = 'EdLevel'
COL_LINGUAGENS = 'LanguageHaveWorkedWith'
COL_NOVA_LINGUAGEM = 'Linguagem'

def carregar_e_processar_dados(nome_arquivo_excel, nome_aba, ano):
    """
    Carrega o DataFrame do arquivo Excel, limpa valores NA, desagrega a coluna de linguagens
    e aplica pd.crosstab.
    """
    print(f"--- Processando dados da pesquisa Stack Overflow {ano} (Aba: {nome_aba}) ---")
    
    
    try:
        df = pd.read_excel(nome_arquivo_excel, sheet_name=nome_aba)
    except FileNotFoundError:
        print(f"ERRO: O arquivo EXCEL '{nome_arquivo_excel}' não foi encontrado.")
        return None
    except ValueError:
        print(f" ERRO: A aba '{nome_aba}' não foi encontrada no arquivo Excel.")
        return None

   
    df_limpo = df.dropna(subset=[COL_ESCOLARIDADE, COL_LINGUAGENS])
    print(f"Total de linhas após a remoção de NA: {len(df_limpo)}")
    
    df_linguagens_separadas = (
        df_limpo[COL_LINGUAGENS].astype(str).str.split(';', expand=True).stack().reset_index(level=1, drop=True)
    )
    df_linguagens_separadas.name = COL_NOVA_LINGUAGEM
    
    df_long = df_limpo[[COL_ESCOLARIDADE]].join(df_linguagens_separadas)
    
    tabela_cruzada = pd.crosstab(
        index=df_long[COL_ESCOLARIDADE],
        columns=df_long[COL_NOVA_LINGUAGEM],
        margins=True,
        margins_name='Total'
    )
    
    nome_excel_saida = f'analise_cruzada_{ano}.xlsx'
    tabela_cruzada.to_excel(nome_excel_saida)
    print(f"✅ Tabulação Cruzada gerada e salva em: {nome_excel_saida}")
    return tabela_cruzada


nome_arquivo_excel = "analise_pesquisa_2024_2022.xlsx" 

aba_2024 = "survey_results_2024" 
aba_2022 = "survey_results_2022" 





tabela_cruzada_2024 = carregar_e_processar_dados(nome_arquivo_excel, aba_2024, 2024)
tabela_cruzada_2022 = carregar_e_processar_dados(nome_arquivo_excel, aba_2022, 2022)

print("\nProcessamento concluído.")