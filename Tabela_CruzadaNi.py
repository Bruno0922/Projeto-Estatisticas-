import pandas as pd
import os 


ID_ARQUIVO_EXCEL = 'analise_pesquisa_2024_2022.xlsx'

SHEET_2024 = 'survey_results_2024'  
SHEET_2022 = 'survey_results_2022' 

ID_ARQUIVO_SAIDA = 'edlevel_comparacao_final.xlsx'

df_2024 = None
df_2022 = None

print("--- Tentando carregar dados do Excel ---")

# Carregar os dados de 2024
try:
    df_2024 = pd.read_excel(
        ID_ARQUIVO_EXCEL,
        sheet_name=SHEET_2024,
        usecols=['EdLevel']
    )
    print(f"Sucesso ao carregar dados de 2024 (Planilha: {SHEET_2024})")

except FileNotFoundError:
    print(f" Erro Crítico: Arquivo Excel '{ID_ARQUIVO_EXCEL}' não encontrado.")
    print(f"O script está sendo executado em: {os.getcwd()}")
    
except ValueError:
    print(f" Erro Crítico: Planilha '{SHEET_2024}' não encontrada no arquivo Excel.")
    



# Carregar os dados de 2022
try:
    df_2022 = pd.read_excel(
        ID_ARQUIVO_EXCEL,
        sheet_name=SHEET_2022,
        usecols=['EdLevel']
    )
    print(f"Sucesso ao carregar dados de 2022 (Planilha: {SHEET_2022})")
except Exception:
    try:
        SHEET_2022_ALT = 'survey_results_2022.csv' 
        df_2022 = pd.read_excel(
            ID_ARQUIVO_EXCEL,
            sheet_name=SHEET_2022_ALT,
            usecols=['EdLevel']
        )
        print(f"Sucesso ao carregar dados de 2022 com nome alternativo: '{SHEET_2022_ALT}'")
    except Exception as e:
        print(f" Erro ao carregar dados de 2022. Planilha '{SHEET_2022}' e '{SHEET_2022_ALT}' falharam: {e}")



if df_2024 is not None and df_2022 is not None:
    
  
    contagem_2024 = df_2024['EdLevel'].value_counts().rename('Contagem 2024')
    contagem_2022 = df_2022['EdLevel'].value_counts().rename('Contagem 2022')

   
    tabela_edlevel = pd.merge(
        contagem_2024, 
        contagem_2022, 
        left_index=True, 
        right_index=True, 
        how='outer'
    ).fillna(0)

    
    total_2024 = tabela_edlevel['Contagem 2024'].sum()
    total_2022 = tabela_edlevel['Contagem 2022'].sum()

    tabela_edlevel['% 2024'] = (tabela_edlevel['Contagem 2024'] / total_2024) * 100
    tabela_edlevel['% 2022'] = (tabela_edlevel['Contagem 2022'] / total_2022) * 100

    
    tabela_final = tabela_edlevel[['Contagem 2024', '% 2024', 'Contagem 2022', '% 2022']].copy()
    tabela_final.loc['Total Geral'] = [total_2024, 100.00, total_2022, 100.00]

    
    tabela_final = tabela_final.apply(pd.to_numeric, errors='ignore', axis=1)
    tabela_final['Contagem 2024'] = tabela_final['Contagem 2024'].astype(int)
    tabela_final['Contagem 2022'] = tabela_final['Contagem 2022'].astype(int)
    tabela_final['% 2024'] = tabela_final['% 2024'].map('{:,.2f}%'.format)
    tabela_final['% 2022'] = tabela_final['% 2022'].map('{:,.2f}%'.format)

    tabela_final = tabela_final[['Contagem 2024', '% 2024', 'Contagem 2022', '% 2022']]

    try:
        tabela_final.to_excel(ID_ARQUIVO_SAIDA, sheet_name='Comparacao EdLevel')
        print(f"\n Sucesso! A tabela final foi salva no arquivo: {ID_ARQUIVO_SAIDA}")

    except Exception as e:
        print(f"\n Erro ao salvar o arquivo de saída: {e}")
        
    
    print("\n Tabela de Nível de Escolaridade (EdLevel) no formato original do questionário.")
    print(tabela_final)


