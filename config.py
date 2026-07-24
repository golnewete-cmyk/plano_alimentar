"""
config.py
Configurações globais do sistema: paleta visual, constantes científicas
e parâmetros usados pelo motor de geração de planos alimentares.

FUNDAMENTO CIENTÍFICO (resumo das decisões metodológicas adotadas):

1) EQUAÇÃO DE GASTO ENERGÉTICO BASAL (GEB): Mifflin-St Jeor (1990).
   Escolhida em detrimento de Harris-Benedict (1919, revisada 1984) porque
   estudos de validação (ex.: Frankenfield et al., 2005, J Am Diet Assoc)
   demonstram que Mifflin-St Jeor apresenta maior acurácia preditiva em
   adultos eutróficos, sobrepeso e obesos, sendo a equação recomendada pela
   Academy of Nutrition and Dietetics para uso em população saudável sem
   necessidade de calorimetria indireta.

2) FATOR ATIVIDADE (PAL - Physical Activity Level): valores consolidados
   segundo FAO/OMS/UNU (2001) e amplamente utilizados na prática clínica
   (sedentário 1.2 até muito ativo 1.9).

3) AJUSTE CALÓRICO POR OBJETIVO: déficit de 15-25% (emagrecimento) e
   superávit de 10-15% (ganho de massa) são as faixas recomendadas por
   diretrizes de sociedades de nutrição esportiva (ISSN Position Stand,
   Aragon et al., 2017) para minimizar perda de massa magra e favorecer
   adesão/sustentabilidade em comparação a déficits agressivos (>25%).

4) DISTRIBUIÇÃO DE MACRONUTRIENTES:
   - Proteína: prescrita em g/kg de peso corporal (não em % do VET), pois
     esta é a abordagem recomendada pela literatura de nutrição esportiva
     (ISSN, 2017), com faixas de 1.2-1.6 g/kg (manutenção) até
     1.6-2.2 g/kg (emagrecimento/hipertrofia), garantindo preservação de
     massa magra.
   - Lipídios: 20-35% do VET (DRI/IOM, 2005), com piso mínimo de 0.8 g/kg
     para garantir síntese hormonal adequada.
   - Carboidratos: valor residual do VET após proteína e lipídios serem
     alocados, garantido acima do piso mínimo de segurança de 100 g/dia
     para função de SNC.

5) NÚMERO DE REFEIÇÕES: não há evidência de superioridade metabólica de
   um número fixo de refeições sobre outro para o mesmo total calórico
   diário (revisões sistemáticas sobre frequência alimentar), portanto o
   número de refeições é definido por preferência/rotina do paciente
   (3 a 6 refeições/dia), distribuindo o VET proporcionalmente.
"""

APP_TITLE = "Plano Alimentar Inteligente"
APP_ICON = "🌿"

# ---------------------------------------------------------------------------
# PALETA VISUAL - dark mode premium (verde profundo, verde oliva, dourado fosco)
# ---------------------------------------------------------------------------
COLORS = {
    "bg_primary": "#0E1512",
    "bg_secondary": "#161F1B",
    "bg_card": "#1B2620",
    "border": "#2B3830",
    "green_deep": "#0F3D2E",
    "green_olive": "#5B6B3B",
    "gold": "#C9A45C",
    "gold_soft": "#D8C39A",
    "text_primary": "#EDEDE7",
    "text_secondary": "#A9B3AB",
    "success": "#6FAE8C",
    "danger": "#C96B5C",
}

# ---------------------------------------------------------------------------
# CONSTANTES CIENTÍFICAS
# ---------------------------------------------------------------------------

# Fatores de atividade física (PAL) - FAO/OMS/UNU 2001
FATORES_ATIVIDADE = {
    "sedentario": {"label": "Sedentário (pouco ou nenhum exercício)", "pal": 1.20},
    "leve": {"label": "Leve (exercício leve 1-3x/semana)", "pal": 1.375},
    "moderado": {"label": "Moderado (exercício moderado 3-5x/semana)", "pal": 1.55},
    "alto": {"label": "Alto (exercício intenso 6-7x/semana)", "pal": 1.725},
    "muito_alto": {"label": "Muito alto (atleta / treino 2x ao dia)", "pal": 1.90},
}

# Ajuste calórico por objetivo (percentual sobre o GET/TDEE)
AJUSTE_OBJETIVO = {
    "emagrecimento": -0.20,   # déficit de 20%
    "manutencao": 0.0,
    "hipertrofia": 0.125,     # superávit de 12.5%
}

# Proteína em g/kg de peso corporal, por objetivo (ISSN Position Stand, 2017)
PROTEINA_G_KG = {
    "emagrecimento": 2.0,
    "manutencao": 1.4,
    "hipertrofia": 2.0,
}

# Percentual de lipídios sobre o VET (DRI/IOM 2005) e piso mínimo em g/kg
PERCENTUAL_LIPIDIOS = 0.27
LIPIDIOS_MIN_G_KG = 0.8

# Piso de segurança de carboidratos (g/dia) para função de sistema nervoso central
CARBOIDRATO_MINIMO_G = 100

# Limites de segurança de calorias diárias (evitar planos extremos)
KCAL_MINIMO_MULHER = 1200
KCAL_MINIMO_HOMEM = 1500
KCAL_MAXIMO = 4500

# Valor energético dos macronutrientes (kcal/g) - Atwater
KCAL_POR_G = {"proteina": 4, "carboidrato": 4, "gordura": 9}

# ---------------------------------------------------------------------------
# TEMPLATES DE DISTRIBUIÇÃO CALÓRICA POR NÚMERO DE REFEIÇÕES
# (percentual do VET alocado a cada refeição do dia)
# ---------------------------------------------------------------------------
TEMPLATES_REFEICOES = {
    3: [
        {"nome": "Café da manhã", "pct": 0.30},
        {"nome": "Almoço", "pct": 0.40},
        {"nome": "Jantar", "pct": 0.30},
    ],
    4: [
        {"nome": "Café da manhã", "pct": 0.25},
        {"nome": "Almoço", "pct": 0.35},
        {"nome": "Lanche da tarde", "pct": 0.15},
        {"nome": "Jantar", "pct": 0.25},
    ],
    5: [
        {"nome": "Café da manhã", "pct": 0.20},
        {"nome": "Lanche da manhã", "pct": 0.10},
        {"nome": "Almoço", "pct": 0.30},
        {"nome": "Lanche da tarde", "pct": 0.15},
        {"nome": "Jantar", "pct": 0.25},
    ],
    6: [
        {"nome": "Café da manhã", "pct": 0.18},
        {"nome": "Lanche da manhã", "pct": 0.09},
        {"nome": "Almoço", "pct": 0.27},
        {"nome": "Lanche da tarde", "pct": 0.13},
        {"nome": "Jantar", "pct": 0.23},
        {"nome": "Ceia", "pct": 0.10},
    ],
}

# Estrutura de grupos de alimentos usada em cada refeição (define quais
# categorias devem compor cada tipo de refeição para garantir equilíbrio
# nutricional e variedade)
ESTRUTURA_REFEICAO = {
    "Café da manhã": ["carboidrato", "proteina", "fruta", "gordura"],
    "Lanche da manhã": ["fruta", "proteina"],
    "Lanche da tarde": ["fruta", "proteina", "carboidrato"],
    "Almoço": ["carboidrato", "proteina", "vegetal", "gordura"],
    "Jantar": ["carboidrato", "proteina", "vegetal", "gordura"],
    "Ceia": ["proteina", "fruta"],
}

# Restrições alimentares suportadas
RESTRICOES_DISPONIVEIS = [
    "vegetariano",
    "vegano",
    "sem_lactose",
    "sem_gluten",
    "sem_ovo",
    "sem_frutos_do_mar",
]