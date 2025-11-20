import pandas as pd
from io import StringIO

# --- 1. CONFIGURAÇÕES DE ENTRADA E ARQUIVOS (Dados injetados) ---
ID_ARQUIVO_SAIDA_FINAL = 'Soma_Total_Linguagens_vs_Niveis_Originais_2018_2024.xlsx' 

# Conteúdo dos arquivos CSV (Dados extraídos dos seus uploads)
# NOTE: Os dados de 2022 e 2024 foram usados no script anterior para simulação,
# mas como você me forneceu os arquivos de contagem de cada ano, vamos usá-los.
CSV_CONTENT = {
    '2024': """
EdLevel,JavaScript,HTML/CSS,SQL,Python,TypeScript,Bash/Shell (all shells),Java,C#,C++,C
"Associate degree (A.A., A.S., etc.)",1212,1082,1022,732,754,530,487,644,296,267
"Bachelor’s degree (B.A., B.S., B.Eng., etc.)",15664,12940,12884,11437,10093,7839,7260,6772,4828,4213
"Master’s degree (M.A., M.S., M.Eng., MBA, etc.)",8252,6660,7613,8002,5296,5330,4581,3706,3329,2745
Primary/elementary school,722,702,352,667,374,352,327,310,359,297
"Professional degree (JD, MD, Ph.D, Ed.D, etc.)",1166,997,1140,1864,579,1085,667,488,891,714
"Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)",3797,3609,2562,3227,2180,1895,1926,1624,1775,1638
Some college/university study without earning a degree,5074,4429,3959,3586,2991,2760,2132,2087,1726,1731
Something else,564,537,427,405,325,270,287,277,215,209
""",
    '2022': """
EdLevel,JavaScript,HTML/CSS,SQL,Python,TypeScript,Java,Bash/Shell,C#,C++,PHP
"Associate degree (A.A., A.S., etc.)",1614,1399,1273,867,806,703,615,803,383,681
"Bachelor’s degree (B.A., B.S., B.Eng., etc.)",20311,16586,15571,13232,11338,10203,8133,8659,5954,6058
"Master’s degree (M.A., M.S., M.Eng., MBA, etc.)",8766,7084,7647,7773,5014,5170,4816,3916,3408,2599
"Other doctoral degree (Ph.D., Ed.D., etc.)",838,721,787,1495,326,456,846,315,681,229
Primary/elementary school,1201,1146,527,1069,524,566,471,526,552,380
"Professional degree (JD, MD, etc.)",705,590,605,408,351,334,248,296,176,308
"Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)",5478,5108,3322,4478,2604,2872,2239,2258,2483,1825
Some college/university study without earning a degree,6590,5631,4793,4219,3379,2901,2922,2652,2054,2330
Something else,835,784,547,546,370,384,335,415,292,371
""",
    '2020': """
EdLevel,JavaScript,HTML/CSS,SQL,Python,Java,Bash/Shell/PowerShell,C#,PHP,TypeScript,C++
"Associate degree (A.A., A.S., etc.)",1327,1257,1064,615,619,596,741,638,501,305
"Bachelor’s degree (B.A., B.S., B.Eng., etc.)",17308,15822,14024,10318,10009,7889,7863,6178,6773,5267
I never completed any formal education,278,259,183,144,151,104,125,154,106,103
"Master’s degree (M.A., M.S., M.Eng., MBA, etc.)",7525,6661,6592,5705,4846,4417,3521,2485,2979,2921
"Other doctoral degree (Ph.D., Ed.D., etc.)",650,609,629,1049,492,692,275,206,175,550
Primary/elementary school,568,603,302,484,345,254,279,243,162,317
"Professional degree (JD, MD, etc.)",526,484,463,254,319,244,258,270,194,132
"Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)",3027,3160,2203,2271,2014,1375,1517,1415,960,1444
Some college/university study without earning a degree,4986,4751,3897,2898,2574,2476,2265,2135,1859,1646
""",
    '2018': """
FormalEducation,JavaScript,HTML,CSS,SQL,Java,Bash/Shell,Python,C#,PHP,C++
Associate degree,1833,1834,1772,1529,962,904,798,1020,998,486
"Bachelor’s degree (BA, BS, B.Eng., etc.)",25755,24751,23617,20894,16424,13475,12751,12668,10545,7995
I never completed any formal education,313,331,310,213,169,156,150,140,197,121
"Master’s degree (MA, MS, M.Eng., MBA, etc.)",11342,10818,10131,9763,8174,7379,7198,5646,4331,4648
"Other doctoral degree (Ph.D, Ed.D., etc.)",872,890,806,870,666,1013,1213,411,278,734
Primary/elementary school,787,875,821,467,553,445,603,405,443,383
"Professional degree (JD, MD, etc.)",757,730,699,653,499,378,330,392,398,238
"Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)",4773,5159,4875,3672,3413,2715,3111,2298,2703,2398
Some college/university study without earning a degree,7209,7135,6896,5801,3997,4225,3703,3473,3577,2439
"""
}

# --- 2. MAPAS DE HARMONIZAÇÃO ---

# 2.1 Mapeamento de Linguagens para unificar nomes diferentes
MAPA_LINGUAGENS = {
    'Bash/Shell/PowerShell': 'Bash/Shell',
    'Bash/Shell (all shells)': 'Bash/Shell', 
    'HTML': 'HTML/CSS', 
    'CSS': 'HTML/CSS',   
    'C': 'C/C++', # 2024 tem C separado
    'C++': 'C/C++',
}

# 2.2 Mapeamento para harmonizar NOMES de níveis de escolaridade que variam levemente
MAPA_HARMONIZACAO_NOMES_ESCOLARIDADE = {
    "Bachelor’s degree (B.A., B.S., B.Eng., etc.)": "Bachelor's degree",
    "Bachelor’s degree (BA, BS, B.Eng., etc.)": "Bachelor's degree",
    
    "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)": "Master's degree",
    "Master’s degree (MA, MS, M.Eng., MBA, etc.)": "Master's degree",
    
    "Associate degree (A.A., A.S., etc.)": "Associate degree",
    "Associate degree": "Associate degree",
    
    "Professional degree (JD, MD, Ph.D, Ed.D, etc.)": "Professional degree",
    "Professional degree (JD, MD, etc.)": "Professional degree",

    "Other doctoral degree (Ph.D., Ed.D., etc.)": "Other doctoral degree",
    "Other doctoral degree (Ph.D, Ed.D., etc.)": "Other doctoral degree",
    
    # Manter o resto como estão, garantindo consistência
    "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)": "Secondary school",
    "Primary/elementary school": "Primary/elementary school",
    "Some college/university study without earning a degree": "Some college/university study without earning a degree",
    "I never completed any formal education": "I never completed any formal education",
    "Something else": "Something else",
}


lista_df = []
anos_processados = []

# --- 3. FUNÇÃO DE CARREGAMENTO E PRÉ-PROCESSAMENTO (1:1) ---

def carregar_e_preparar_dados_originais(ano, content):
    print(f"--- Processando dados de {ano} (Níveis Originais 1:1) ---")
    
    try:
        # 1. Lê a string de conteúdo CSV
        df = pd.read_csv(
            StringIO(content), 
            index_col=0, # Define a primeira coluna (EdLevel/FormalEducation) como índice
            encoding='utf-8', 
        )
        
        # 2. Renomear o índice para 'Escolaridade' (apenas para clareza interna)
        df.index.name = 'Escolaridade'
        
        # 3. Harmonizar as colunas de linguagens
        df.columns = df.columns.to_series().replace(MAPA_LINGUAGENS)
        
        # 🌟 CRÍTICO: Somar colunas duplicadas após a harmonização (ex: HTML/CSS)
        df = df.T.groupby(level=0).sum().T 
        
        # 4. Aplicar o mapeamento de harmonização de NOMES de escolaridade no índice
        df.index = df.index.to_series().replace(MAPA_HARMONIZACAO_NOMES_ESCOLARIDADE)
        df.index.name = 'Escolaridade'
        
        # 5. Agrupar e somar linhas que caíram na mesma categoria harmonizada (índice)
        df_agrupado = df.groupby(level=0).sum()
        
        anos_processados.append(ano)
        print(f"✅ SUCESSO. {ano} processado (Níveis Originais).")
        return df_agrupado

    except Exception as e:
        print(f" ❌ ERRO GERAL ao ler/processar {ano}: {e}. Ignorando o ano.")
        return None

# --- 4. EXECUÇÃO DO CARREGAMENTO ---

for ano, content in CSV_CONTENT.items():
    df_ano = carregar_e_preparar_dados_originais(ano, content)
    if df_ano is not None:
        lista_df.append(df_ano)

# --- 5. CONSOLIDAÇÃO FINAL (SOMA) ---

if lista_df:
    
    print(f"\n--- INICIANDO CONSOLIDAÇÃO E SOMA FINAL ({', '.join(anos_processados)}) ---")
    
    # 5.1 CONCATENAÇÃO E SOMA FINAL: Concatena todos os DataFrames e soma os valores agrupados pelo índice (Escolaridade)
    df_consolidado = pd.concat(lista_df, sort=False).groupby(level=0).sum()
    
    # 5.2 Definir a ordem de exibição lógica
    ordem_niveis = [
        "Primary/elementary school",
        "Secondary school",
        "Associate degree",
        "Some college/university study without earning a degree",
        "Bachelor's degree",
        "Professional degree",
        "Master's degree",
        "Other doctoral degree",
        "I never completed any formal education",
        "Something else"
    ]
    
    # Reordenar as linhas (índice), preenchendo com 0 se a categoria não existir
    df_consolidado = df_consolidado.reindex(ordem_niveis, fill_value=0)
    
    # 5.3 Calcular a Coluna de Soma Total por Nível (Linhas)
    df_consolidado['Soma Total por Nível'] = df_consolidado.sum(axis=1)
    
    # 5.4 Calcular a Linha de Soma Total (Colunas)
    total_geral_linguagens = df_consolidado.sum(axis=0)
    total_geral_linguagens.name = 'TOTAL GERAL (2018-2024)' 
    df_consolidado.loc[total_geral_linguagens.name] = total_geral_linguagens
    
    # Limpeza e conversão final para inteiro
    tabela_final = df_consolidado.fillna(0).astype(int)

    # 6. Salvar o arquivo de saída
    try:
        tabela_final.to_excel(ID_ARQUIVO_SAIDA_FINAL, sheet_name='Soma_Niveis_Originais_2018_2024')
        
        print(f"\n✨ SUCESSO FINAL! Tabela cruzada SOMADA de {', '.join(anos_processados)} salva em: **{ID_ARQUIVO_SAIDA_FINAL}**")

    except Exception as e:
        print(f"\n ❌ Erro ao salvar o arquivo final: {e}")
        
    print("\n--- TABELA CRUZADA CONSOLIDADA E SOMADA (2018-2024) - NÍVEIS ORIGINAIS ---")
    print(tabela_final)
    
else:
    print("\n 🛑 ERRO CRÍTICO: Não foi possível processar dados de nenhum ano. A consolidação não pode ser realizada.")