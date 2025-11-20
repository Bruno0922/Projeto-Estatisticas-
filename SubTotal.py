import pandas as pd
from functools import reduce 

# --- 1. CONFIGURAÇÕES DE ENTRADA ---
ID_ARQUIVO_24_22 = 'analise_pesquisa_2024_2022.xlsx'
ID_ARQUIVO_20_18 = 'analise_pesquisa_2018_2020.xlsm' 
ID_ARQUIVO_SAIDA_FINAL = 'soma_total_escolaridade_original.xlsx'

# Mapeamento de abas e colunas
CONFIG_CARGA = {
    '2024': {'arquivo': ID_ARQUIVO_24_22, 'sheet': 'survey_results_2024', 'coluna': 'EdLevel'},
    '2022': {'arquivo': ID_ARQUIVO_24_22, 'sheet': 'survey_results_2022', 'coluna': 'EdLevel'},
    '2020': {'arquivo': ID_ARQUIVO_20_18, 'sheet': 'survey_results_public_2020', 'coluna': 'EdLevel'},
    '2018': {'arquivo': ID_ARQUIVO_20_18, 'sheet': 'survey_results_public_2018', 'coluna': 'FormalEducation'}, # Coluna diferente em 2018
}

lista_contagens = []
anos_sucesso = []

# --- 2. FUNÇÃO DE PROCESSAMENTO E CONTAGEM POR ANO (SEM HARMONIZAÇÃO) ---

def processar_e_contar_escolaridade_original(ano, config):
    """
    Carrega os dados e calcula as contagens brutas usando os nomes originais das categorias.
    """
    print(f"--- Processando Contagens Originais de {ano} ---")
    
    try:
        # Carregamento de dados
        df = pd.read_excel(config['arquivo'], sheet_name=config['sheet'], usecols=[config['coluna']])
        
        col_original = config['coluna']

        # 1. Calcula a contagem de ocorrências por categoria ORIGINAL
        # Remove nulos antes de contar
        contagem = df[col_original].value_counts()
        contagem = contagem.rename(f'Contagem {ano}')
        
        # Converte para DataFrame para facilitar o merge
        df_contagem = contagem.to_frame()
        
        print(f"✅ Sucesso. {contagem.sum()} respostas processadas para {ano}.")
        return df_contagem, ano

    except FileNotFoundError:
        print(f" ❌ ERRO de Arquivo: O arquivo '{config['arquivo']}' (necessário para {ano}) não foi encontrado. Ignorando este ano.")
        return None, None
    except KeyError as e:
        print(f" ❌ ERRO de Coluna: A coluna {e} não foi encontrada na planilha de {ano}. Ignorando este ano.")
        return None, None
    except Exception as e:
        print(f" ❌ ERRO geral ao processar {ano}: {e}. Ignorando este ano.")
        return None, None


# --- 3. EXECUÇÃO E CONSOLIDAÇÃO ---

for ano, config in CONFIG_CARGA.items():
    df_resultado, ano_sucesso = processar_e_contar_escolaridade_original(ano, config)
    if df_resultado is not None:
        lista_contagens.append(df_resultado)
        anos_sucesso.append(ano_sucesso)

if len(lista_contagens) >= 1:
    
    # 3.1. União dos DataFrames (Merge Outer para incluir todas as categorias)
    df_consolidado = reduce(
        lambda left, right: pd.merge(left, right, left_index=True, right_index=True, how='outer'), 
        lista_contagens
    )
    
    # Preencher valores ausentes com 0
    df_consolidado = df_consolidado.fillna(0).astype(int)

    # 3.2. Soma dos Valores (Horizontalmente)
    contagem_cols = [f'Contagem {ano}' for ano in anos_sucesso]
    df_consolidado['Soma Total'] = df_consolidado[contagem_cols].sum(axis=1)

    # 3.3. Adicionar Linha de Total Geral (na última linha)
    # Soma vertical das colunas de contagem e da Soma Total
    total_geral = df_consolidado.sum()
    total_geral.name = 'TOTAL GERAL DE RESPONDENTES' # Nome da nova linha
    
    df_consolidado.loc[total_geral.name] = total_geral

    # 3.4. Formatação Final
    # Reordenar as colunas
    colunas_ordenadas = contagem_cols + ['Soma Total']
    df_consolidado = df_consolidado[colunas_ordenadas]

    # 4. Salvar o arquivo de saída
    try:
        df_consolidado.to_excel(ID_ARQUIVO_SAIDA_FINAL, sheet_name='Contagens_Originais')
        print(f"\n✨ SUCESSO TOTAL! Tabela de Escolaridade (contagens originais) salva em: {ID_ARQUIVO_SAIDA_FINAL}")

    except Exception as e:
        print(f"\n ❌ Erro ao salvar o arquivo final: {e}")
        
    print("\n--- TABELA DE ESCOLARIDADE (CONTAGENS ORIGINAIS) ---")
    # Mostra a tabela completa
    print(df_consolidado.to_string())
    
else:
    print("\n 🛑 ERRO CRÍTICO: Não foi possível processar contagens de nenhum ano. Verifique os logs de erro.")