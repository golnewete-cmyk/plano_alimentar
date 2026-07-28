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

# Estrutura de cada refeição: lista de (seção, grupo_alimentar).
# Refeições principais (Almoço/Jantar) seguem o padrão clínico tradicional
# em 3 blocos - ENTRADA (saladas/vegetais), PRATO (carboidrato + proteína +
# gordura de preparo) e BEBIDA (suco) - tal como estruturado na prática
# clínica de referência fornecida. Lanches e café da manhã permanecem como
# lista única ("principal"), sem subseções, por serem refeições mais simples.
# Repetir o mesmo grupo duas vezes (ex.: "vegetal" na entrada) faz o
# algoritmo selecionar dois alimentos distintos daquele grupo automaticamente.
ESTRUTURA_REFEICAO = {
    "Café da manhã": [
        ("principal", "carboidrato"),
        ("principal", "proteina"),
        ("principal", "fruta"),
        ("principal", "gordura"),
    ],
    "Lanche da manhã": [
        ("principal", "fruta"),
        ("principal", "proteina"),
    ],
    "Lanche da tarde": [
        ("principal", "fruta"),
        ("principal", "proteina"),
        ("principal", "carboidrato"),
    ],
    "Almoço": [
        ("entrada", "vegetal"),
        ("entrada", "vegetal"),
        ("prato", "carboidrato"),
        ("prato", "proteina"),
        ("prato", "gordura"),
        ("bebida", "bebida"),
    ],
    "Jantar": [
        ("entrada", "vegetal"),
        ("entrada", "vegetal"),
        ("prato", "carboidrato"),
        ("prato", "proteina"),
        ("prato", "gordura"),
        ("bebida", "bebida"),
    ],
    "Ceia": [
        ("principal", "proteina"),
        ("principal", "fruta"),
    ],
}

# Ordem e rótulos de exibição das seções dentro de uma refeição
ORDEM_SECOES = ["principal", "entrada", "prato", "bebida"]
ROTULO_SECAO = {
    "principal": None,   # sem subtítulo — lista direta dos alimentos
    "entrada": "ENTRADA",
    "prato": "PRATO",
    "bebida": "BEBIDA",
}

# Grupos que recebem porção fixa de referência (não entram no sistema
# linear de macronutrientes nem na calibração fina de porções) — seu papel
# nutricional é fibra, micronutrientes ou hidratação/acompanhamento, não
# macronutriente principal.
GRUPOS_PORCAO_FIXA = ("vegetal", "bebida")

# Horário sugerido de cada refeição, por número de refeições do dia
HORARIOS_REFEICOES = {
    3: {"Café da manhã": "07:30", "Almoço": "12:30", "Jantar": "20:00"},
    4: {"Café da manhã": "07:30", "Almoço": "12:30", "Lanche da tarde": "16:30", "Jantar": "20:00"},
    5: {"Café da manhã": "07:00", "Lanche da manhã": "10:00", "Almoço": "12:30",
        "Lanche da tarde": "16:30", "Jantar": "20:00"},
    6: {"Café da manhã": "07:00", "Lanche da manhã": "10:00", "Almoço": "12:30",
        "Lanche da tarde": "16:30", "Jantar": "20:00", "Ceia": "22:00"},
}

# ---------------------------------------------------------------------------
# RECOMENDAÇÕES CLÍNICAS PADRÃO
# ---------------------------------------------------------------------------
# Ingestão hídrica: 30-35 mL/kg/dia é a faixa consolidada para adultos
# saudáveis (European Food Safety Authority / Institute of Medicine), usada
# aqui para sugerir uma faixa de referência de litros/dia.
AGUA_ML_KG_MIN = 30
AGUA_ML_KG_MAX = 35

RECOMENDACOES_GERAIS = [
    "Mastigar bem os alimentos e comer devagar, com atenção plena à refeição.",
    "Evitar líquidos durante as refeições; se possível, aguardar cerca de 30 minutos antes ou depois de comer.",
    "Registrar as refeições realizadas e eventuais desconfortos gastrointestinais em um diário alimentar.",
    "Priorizar o preparo dos alimentos grelhado, cozido, assado ou refogado, evitando frituras no dia a dia.",
    "Respeitar os horários sugeridos das refeições, ajustando-os à rotina pessoal sempre que necessário.",
]

RECOMENDACOES_POR_OBJETIVO = {
    "emagrecimento": "Evitar repetir pratos e servir as porções já no tamanho definido no plano, evitando 'comer na panela'.",
    "manutencao": "Manter a regularidade dos horários das refeições para preservar o equilíbrio energético alcançado.",
    "hipertrofia": "Não pular refeições, especialmente as fontes proteicas, para sustentar a síntese proteica muscular ao longo do dia.",
}

RECOMENDACOES_POR_RESTRICAO = {
    "sem_lactose": "Verificar sempre o rótulo dos alimentos industrializados quanto à presença de leite ou derivados ocultos.",
    "sem_gluten": "Verificar sempre o rótulo dos alimentos industrializados quanto à presença de trigo, cevada, centeio ou aveia contaminada cruzadamente.",
    "vegano": "Considerar acompanhamento da suplementação de vitamina B12, que não está presente em fontes vegetais.",
    "vegetariano": "Combinar leguminosas (feijão, lentilha, grão-de-bico) com cereais ao longo do dia para melhorar a qualidade proteica.",
    "sem_ovo": "Verificar sempre o rótulo de produtos de panificação e massas quanto à presença de ovo.",
    "sem_frutos_do_mar": "Verificar sempre o rótulo de temperos e caldos industrializados quanto à presença de extrato de frutos do mar.",
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

# Campos de identificação profissional exibidos no cabeçalho do PDF.
# Ficam vazios por padrão: cada nutricionista preenche os próprios dados
# no formulário antes de gerar o PDF (nenhuma marca ou identidade de
# terceiros é utilizada pelo sistema).
NUTRICIONISTA_PADRAO = {
    "nome": "",
    "especialidade": "Nutrição Clínica",
    "crn": "",
    "telefone": "",
    "email": "",
    "local_atendimento": "",
}