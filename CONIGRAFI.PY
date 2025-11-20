import json
import warnings

# Ignora avisos (apenas por boas práticas, embora não vá ler arquivos)
warnings.filterwarnings("ignore")

# ==============================================================================
# 🎯 DADOS MANUAIS AQUI (EDITAR APENAS ESTA SEÇÃO)
# ==============================================================================

# 1. Níveis de Escolaridade (Rótulos do gráfico)
NIVEIS_ESCOLARIDADE = [
    "Ensino Fundamental",
    "Ensino Médio",
    "Bacharelado",
    "Pós-Graduação"
]

# 2. Linguagens de Foco (Botões no dashboard)
LINGUAGENS_FOCO = ['JavaScript', 'HTML/CSS', 'Python', 'SQL', 'Java']

# 3. Dados Anuais (Contagens Absolutas)
# Estrutura: {Ano: {Escolaridade: {Linguagem: Contagem}}}
DADOS_ANUAIS_CONTAGEM = {
    "2020": {
        "Ensino Fundamental": {
            "JavaScript": 1500,
            "HTML/CSS": 1000,
            "Python": 500,
            "SQL": 300,
            "Java": 200
        },
        "Ensino Médio": {
            "JavaScript": 8000,
            "HTML/CSS": 6500,
            "Python": 4000,
            "SQL": 3000,
            "Java": 1500
        },
        "Bacharelado": {
            "JavaScript": 25000,
            "HTML/CSS": 20000,
            "Python": 18000,
            "SQL": 15000,
            "Java": 10000
        },
        "Pós-Graduação": {
            "JavaScript": 10000,
            "HTML/CSS": 8000,
            "Python": 12000,
            "SQL": 9000,
            "Java": 7000
        }
    },
    "2024": {
        # AQUI VOCÊ PODE INSERIR OS DADOS DO ANO 2024
        "Ensino Fundamental": {
            "JavaScript": 2000,
            "HTML/CSS": 1500,
            "Python": 800,
            "SQL": 500,
            "Java": 300
        },
        "Ensino Médio": {
            "JavaScript": 10000,
            "HTML/CSS": 8500,
            "Python": 6000,
            "SQL": 4000,
            "Java": 2500
        },
        "Bacharelado": {
            "JavaScript": 35000,
            "HTML/CSS": 30000,
            "Python": 28000,
            "SQL": 22000,
            "Java": 18000
        },
        "Pós-Graduação": {
            "JavaScript": 15000,
            "HTML/CSS": 12000,
            "Python": 18000,
            "SQL": 14000,
            "Java": 11000
        }
    }
}

# 4. Dados de Ranking Total (Opcional, se não for usar, mantenha como None)
# Como o dashboard só usa os dados anuais, manteremos o ranking como nulo.
DADOS_RANKING_TOTAL = None 

# ==============================================================================
# ⚙️ Geração do JSON (Não Edite Abaixo)
# ==============================================================================
print("--- Iniciando geração manual de dados JSON ---")

estrutura_final = {
    'labels': NIVEIS_ESCOLARIDADE, 
    'yearly_count_data': DADOS_ANUAIS_CONTAGEM,
    'total_ranking_data': DADOS_RANKING_TOTAL, 
    'linguagens_foco': LINGUAGENS_FOCO
}

try:
    # Abertura com encoding='utf-8' e ensure_ascii=False para garantir
    # que o JSON seja perfeitamente válido, mesmo com caracteres em português.
    with open('data_dashboard.json', 'w', encoding='utf-8') as f:
        json.dump(estrutura_final, f, indent=4, ensure_ascii=False) 
    print("\n----------------------------------------------------")
    print("✅ Arquivo 'data_dashboard.json' MANUAL gerado com sucesso!")
    print("----------------------------------------------------")
except Exception as e:
    print(f"ERRO CRÍTICO ao escrever o JSON: {e}")