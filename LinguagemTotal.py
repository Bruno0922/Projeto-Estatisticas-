import pandas as pd
import numpy as np
import os

# --- 1. CONFIGURAÇÕES DE ENTRADA ---
ID_ARQUIVO_24_22 = 'analise_pesquisa_2024_2022.xlsx'
ID_ARQUIVO_20_18 = 'analise_pesquisa_2018_2020.xlsm' # Se este arquivo não for encontrado, 2020/2018 serão ignorados.
TOP_N = 10 # Limite para o Top 10

# Mapeamento de abas e colunas para cada ano
CONFIG_CARGA = {
    '2024': {'arquivo': ID_ARQUIVO_24_22, 'sheet': 'survey_results_2024', 'col_esc': 'EdLevel', 'col_lang': 'LanguageHaveWorkedWith'},
    '2022': {'arquivo': ID_ARQUIVO_24_22, 'sheet': 'survey_results_2022', 'col_esc': 'EdLevel', 'col_lang': 'LanguageHaveWorkedWith'},
    '2020': {'arquivo': ID_ARQUIVO_20_18, 'sheet': 'survey_results_public_2020', 'col_esc': 'EdLevel', 'col_lang': 'LanguageWorkedWith'},
    '2018': {'arquivo': ID_ARQUIVO_20_18, 'sheet': 'survey_results_public_2018', 'col_esc': 'FormalEducation', 'col_lang': 'LanguageWorkedWith'},
}


# --- 2. FUNÇÃO DE PROCESSAMENTO, FILTRO E SALVAMENTO ---

def processar_e_salvar_top_n_contagens(ano, config):
    """
    Gera a Tabela Cruzada de CONTAGENS BRUTAS, filtra pelo Top N de linguagens 
    e salva em um arquivo específico do ano.
    """
    print(f"\n--- Processando e Salvando CONTAGENS TOP {TOP_N} de {ano} ---")
    
    NOME_ARQUIVO_SAIDA = f'contagens_top_{ano}.xlsx'

    try:
        # Carregamento de dados (tentando ler como Excel)
        df = pd.read_excel(config['arquivo'], sheet_name=config['sheet'])

        col_esc = config['col_esc']
        col_lang = config['col_lang']

        # 1. Limpeza e Desagregação (Splitting)
        df_limpo = df.dropna(subset=[col_esc, col_lang])
        
        # Cria uma coluna 'Linguagem' com uma linha para cada linguagem usada
        df_linguagens_separadas = (
            df_limpo[col_lang].astype(str).str.split(';', expand=True).stack().reset_index(level=1, drop=True)
        )
        df_linguagens_separadas.name = 'Linguagem'
        
        # Junta a coluna de escolaridade com a lista longa de linguagens
        df_long = df_limpo[[col_esc]].join(df_linguagens_separadas)

        # 2. Geração da Tabela Cruzada de CONTAGENS BRUTAS
        # SEM o parâmetro normalize='index'
        tabela_contagens = pd.crosstab(
            index=df_long[col_esc],
            columns=df_long['Linguagem']
        )
        
        # 3. Identificar o Top N
        # Encontra as colunas com a maior soma (mais usadas no ano)
        top_n_linguagens = tabela_contagens.sum().sort_values(ascending=False).head(TOP_N).index.tolist()
        
        print(f"  Top {TOP_N} Linguagens em {ano}: {', '.join(top_n_linguagens)}")

        # 4. Filtro da Tabela de Contagens
        tabela_final_contagens = tabela_contagens[top_n_linguagens]
        
        # 5. Formatação e Salvamento
        # Garante que todos os valores sejam inteiros (Contagem)
        tabela_final_contagens = tabela_final_contagens.fillna(0).astype(int)
        
        # Salva o arquivo individual
        tabela_final_contagens.to_excel(NOME_ARQUIVO_SAIDA, sheet_name=f'Contagens_Top_{TOP_N}')
        
        print(f"✅ SUCESSO! O arquivo '{NOME_ARQUIVO_SAIDA}' foi criado com as contagens brutas do Top {TOP_N} de {ano}.")
        
        # Retorna a tabela para visualização
        return tabela_final_contagens.head(5)

    except FileNotFoundError:
        print(f" ❌ ERRO de Arquivo: O arquivo '{config['arquivo']}' (necessário para {ano}) não foi encontrado. Ignorando este ano.")
        return None
    except KeyError as e:
        print(f" ❌ ERRO de Coluna: A coluna {e} não foi encontrada na planilha de {ano}. Ignorando este ano.")
        return None
    except Exception as e:
        print(f" ❌ ERRO geral ao processar {ano}: {e}. Ignorando este ano.")
        return None


# --- 3. EXECUÇÃO PRINCIPAL ---

for ano, config in CONFIG_CARGA.items():
    tabela_amostra = processar_e_salvar_top_n_contagens(ano, config)
    if tabela_amostra is not None:
        print(f"\n--- Amostra de 'contagens_top_{ano}.xlsx' ---")
        print(tabela_amostra)