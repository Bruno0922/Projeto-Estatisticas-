import pandas as pd
import numpy as np
import os

# --- 1. CONFIGURAÇÕES DE ENTRADA ---
# Usando os nomes dos arquivos que você carregou
ID_ARQUIVO_24_22 = 'analise_pesquisa_2024_2022.xlsx'
ID_ARQUIVO_20_18 = 'analise_pesquisa_2018_2020.xlsm' 
TOP_N = 10 # Limite para o Top 10

# Mapeamento de abas e colunas para cada ano
CONFIG_CARGA = {
    '2024': {'arquivo': ID_ARQUIVO_24_22, 'sheet': 'survey_results_2024', 'col_esc': 'EdLevel', 'col_lang': 'LanguageHaveWorkedWith'},
    '2022': {'arquivo': ID_ARQUIVO_24_22, 'sheet': 'survey_results_2022', 'col_esc': 'EdLevel', 'col_lang': 'LanguageHaveWorkedWith'},
    # Usamos os nomes originais dos arquivos para garantir o acesso aos dados carregados
    '2020': {'arquivo': ID_ARQUIVO_20_18, 'sheet': 'survey_results_public_2020', 'col_esc': 'EdLevel', 'col_lang': 'LanguageWorkedWith'},
    '2018': {'arquivo': ID_ARQUIVO_20_18, 'sheet': 'survey_results_public_2018', 'col_esc': 'FormalEducation', 'col_lang': 'LanguageWorkedWith'},
}


# --- 2. FUNÇÃO DE PROCESSAMENTO, FILTRO E SALVAMENTO ---

def processar_e_salvar_top_n_porcentagem(ano, config):
    """
    Gera a Tabela Cruzada de PORCENTAGEM, filtra pelo Top N de linguagens 
    e salva em um arquivo específico do ano.
    """
    print(f"\n--- Processando e Salvando PORCENTAGEM TOP {TOP_N} de {ano} ---")
    
    NOME_ARQUIVO_SAIDA = f'porcentagem_top_{ano}.xlsx'

    try:
        # Carregamento de dados
        df = pd.read_excel(config['arquivo'], sheet_name=config['sheet'])

        col_esc = config['col_esc']
        col_lang = config['col_lang']

        # 1. Limpeza e Desagregação (Splitting)
        df_limpo = df.dropna(subset=[col_esc, col_lang])
        
        df_linguagens_separadas = (
            df_limpo[col_lang].astype(str).str.split(';', expand=True).stack().reset_index(level=1, drop=True)
        )
        df_linguagens_separadas.name = 'Linguagem'
        
        df_long = df_limpo[[col_esc]].join(df_linguagens_separadas)

        # 2. Geração da Tabela Cruzada de CONTAGENS BRUTAS (Para identificar o Top N)
        tabela_bruta = pd.crosstab(
            index=df_long[col_esc],
            columns=df_long['Linguagem']
        )
        
        # 3. Identificar o Top N (pela contagem mais alta)
        top_n_linguagens = tabela_bruta.sum().sort_values(ascending=False).head(TOP_N).index.tolist()
        
        print(f"  Top {TOP_N} Linguagens em {ano}: {', '.join(top_n_linguagens)}")

        # 4. Geração da Tabela de PORCENTAGEM POR NÍVEL DE ESCOLARIDADE
        # Usamos normalize='index' para obter a proporção DENTRO de cada nível de escolaridade (linha)
        tabela_perc_completa = pd.crosstab(
            index=df_long[col_esc],
            columns=df_long['Linguagem'],
            normalize='index' 
        )
        
        # Filtra a tabela de Porcentagem usando o Top N identificado
        tabela_final_perc = tabela_perc_completa[top_n_linguagens]
        
        # 5. Formatação e Salvamento
        tabela_final_perc = (tabela_final_perc * 100).round(2)
        
        # Formata para string com '%'
        for col in tabela_final_perc.columns:
            tabela_final_perc[col] = tabela_final_perc[col].map('{:,.2f}%'.format)
            
        
        # Salva o arquivo individual
        tabela_final_perc.to_excel(NOME_ARQUIVO_SAIDA, sheet_name=f'Porcentagem_Top_{TOP_N}')
        
        print(f"✅ SUCESSO! O arquivo '{NOME_ARQUIVO_SAIDA}' foi criado com as porcentagens do Top {TOP_N} de {ano}.")
        
        # Retorna a tabela para visualização
        return tabela_final_perc.head(5)

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
    tabela_amostra = processar_e_salvar_top_n_porcentagem(ano, config)
    if tabela_amostra is not None:
        print(f"\n--- Amostra de 'porcentagem_top_{ano}.xlsx' ---")
        print(tabela_amostra)