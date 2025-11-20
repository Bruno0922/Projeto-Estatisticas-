import pandas as pd
import os 



ID_ARQUIVO_EXCEL = 'analise_pesquisa_2018_2020.xlsm'

SHEET_2020 = 'survey_results_public_2020' 
SHEET_2018 = 'survey_results_public_2018' 

COL_2020 = 'EdLevel'
COL_2018 = 'FormalEducation'

ID_ARQUIVO_SAIDA = 'edlevel_comparacao_2018_2020_final.xlsx'

df_2020 = None
df_2018 = None

print("--- Tentando carregar dados do Excel (2020 e 2018) ---")
print(f"Arquivo: {ID_ARQUIVO_EXCEL}")


try:
    df_2020 = pd.read_excel(
        ID_ARQUIVO_EXCEL,
        sheet_name=SHEET_2020,
        usecols=[COL_2020]
    )
    df_2020.columns = ['Escolaridade'] 
    print(f"Sucesso ao carregar dados de 2020 (Planilha: {SHEET_2020}, Coluna: {COL_2020})")

except Exception as e:
    print(f" ❌ Erro Crítico ao carregar dados de 2020: {e}")
    



try:
    df_2018 = pd.read_excel(
        ID_ARQUIVO_EXCEL,
        sheet_name=SHEET_2018,
        usecols=[COL_2018]
    )
    df_2018.columns = ['Escolaridade']
    print(f"Sucesso ao carregar dados de 2018 (Planilha: {SHEET_2018}, Coluna: {COL_2018})")
    
except Exception as e:
    print(f" ❌ Erro Crítico ao carregar dados de 2018: {e}")



if df_2020 is not None and df_2018 is not None:
    
   
    contagem_2020 = df_2020['Escolaridade'].value_counts().rename('Contagem 2020')
    contagem_2018 = df_2018['Escolaridade'].value_counts().rename('Contagem 2018')

   
    tabela_edlevel = pd.merge(
        contagem_2020, 
        contagem_2018, 
        left_index=True, 
        right_index=True, 
        how='outer'
    ).fillna(0) 
    
   
    total_2020 = tabela_edlevel['Contagem 2020'].sum()
    total_2018 = tabela_edlevel['Contagem 2018'].sum()

    tabela_edlevel['% 2020'] = (tabela_edlevel['Contagem 2020'] / total_2020) * 100
    tabela_edlevel['% 2018'] = (tabela_edlevel['Contagem 2018'] / total_2018) * 100

   
    tabela_final = tabela_edlevel[['Contagem 2020', '% 2020', 'Contagem 2018', '% 2018']].copy()
    
    
    tabela_final.loc['Total Geral'] = [total_2020, 100.00, total_2018, 100.00]

    
    tabela_final['Contagem 2020'] = tabela_final['Contagem 2020'].astype(int)
    tabela_final['Contagem 2018'] = tabela_final['Contagem 2018'].astype(int)
    tabela_final['% 2020'] = tabela_final['% 2020'].map('{:,.2f}%'.format)
    tabela_final['% 2018'] = tabela_final['% 2018'].map('{:,.2f}%'.format)

    tabela_final = tabela_final[['Contagem 2020', '% 2020', 'Contagem 2018', '% 2018']]

    
    try:
        tabela_final.to_excel(ID_ARQUIVO_SAIDA, sheet_name='Comparacao Escolaridade')
        print(f"\n ✅ Sucesso! A tabela final foi salva no arquivo: {ID_ARQUIVO_SAIDA}")

    except Exception as e:
        print(f"\n ❌ Erro ao salvar o arquivo de saída: {e}")
        
    
    print("\n Tabela de Nível de Escolaridade (Escolaridade) Comparativa Final:")
    print(tabela_final)