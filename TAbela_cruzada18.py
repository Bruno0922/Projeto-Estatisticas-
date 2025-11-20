import pandas as pd
import numpy as np
import os 


NOME_ARQUIVO_EXCEL = 'analise_pesquisa_2018_2020.xlsm'
COL_LINGUAGENS = 'LanguageWorkedWith' 
COL_NOVA_LINGUAGEM = 'Linguagem'

ABA_2020 = 'survey_results_public_2020'
ABA_2018 = 'survey_results_public_2018' 

def get_column_names(ano):
    """Retorna os nomes das colunas de Escolaridade e Linguagens para um dado ano."""
    if ano == 2018:
        return 'FormalEducation', 'LanguageWorkedWith'
    elif ano == 2020:
       
        return 'EdLevel', 'LanguageWorkedWith' 
    else:
        raise ValueError(f"Mapeamento de colunas não definido para o ano {ano}")


def carregar_e_processar_dados_brutos(nome_arquivo_excel, nome_aba, ano):
    """
    Carrega, processa e salva APENAS a contagem bruta (Tabulação Cruzada).
    """
    COL_ESCOLARIDADE, COL_LINGUAGENS_TRATADA = get_column_names(ano)

    print(f"--- Processando dados Stack Overflow {ano} (Aba: {nome_aba}) ---")
    print(f"  Colunas usadas: Escolaridade='{COL_ESCOLARIDADE}', Linguagem='{COL_LINGUAGENS_TRATADA}'")
    
    
    try:
        df = pd.read_excel(nome_arquivo_excel, sheet_name=nome_aba)
    except Exception as e:
        print(f" ❌ ERRO ao carregar arquivo/aba: {e}")
        return None

    df_limpo = df.dropna(subset=[COL_ESCOLARIDADE, COL_LINGUAGENS_TRATADA])
    print(f"Total de linhas processadas para {ano}: {len(df_limpo)}")
    
    df_linguagens_separadas = (
        df_limpo[COL_LINGUAGENS_TRATADA].astype(str).str.split(';', expand=True).stack().reset_index(level=1, drop=True)
    )
    df_linguagens_separadas.name = COL_NOVA_LINGUAGEM
    
    df_long = df_limpo[[COL_ESCOLARIDADE]].join(df_linguagens_separadas)
    
    tabela_bruta = pd.crosstab(
        index=df_long[COL_ESCOLARIDADE],
        columns=df_long[COL_NOVA_LINGUAGEM],
        margins=True,          
        margins_name='Total'   
    )
    
    nome_excel_saida = f'analise_cruzada_bruta_{ano}.xlsx'
    tabela_bruta.to_excel(nome_excel_saida)
    print(f"✅ SUCESSO! Contagem Bruta salva em: {nome_excel_saida}")
    
    return tabela_bruta


tabela_bruta_2020 = carregar_e_processar_dados_brutos(NOME_ARQUIVO_EXCEL, ABA_2020, 2020)
tabela_bruta_2018 = carregar_e_processar_dados_brutos(NOME_ARQUIVO_EXCEL, ABA_2018, 2018)

print("\nProcessamento de Contagem Bruta (Tabulação Cruzada) concluído. Verifique os dois arquivos Excel.")