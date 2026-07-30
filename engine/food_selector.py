"""
engine/food_selector.py

Algoritmo determinístico de seleção de alimentos, cálculo de porções e
formatação da descrição de cada item no padrão clínico de referência
(quantidade em medida caseira + gramas/ml entre parênteses, com opções
alternativas equivalentes unidas por "ou").

Regras de decisão implementadas:
1) Cada refeição possui uma "estrutura" (config.ESTRUTURA_REFEICAO) que
   define, por seção (entrada/prato/bebida/principal), quais grupos
   alimentares devem compor aquela refeição.
2) Cada alimento de papel macro (carboidrato/proteína/gordura) tem sua
   porção calculada de forma INDEPENDENTE, a partir da meta do nutriente
   que ele representa na refeição, e sempre dentro de uma faixa realista
   em torno da porção de referência do próprio alimento (entre 40% e 200%
   dela, 150% para gorduras). Isso evita o problema de um sistema
   "resolvido em conjunto" zerar um alimento (ex.: quase nada de arroz)
   para compensar outro (ex.: excesso de feijão) só para bater a meta
   exata — o que gera combinações irreais. Pequenos desvios do total do
   dia são corrigidos depois pela calibração fina do plano.
3) Vegetais e bebidas (config.GRUPOS_PORCAO_FIXA) recebem porção fixa de
   referência — seu papel nutricional é fibra/micronutrientes/hidratação,
   não macronutriente principal.
4) A seleção do alimento específico dentro de cada grupo é determinística:
   respeita restrições alimentares (inclusive termos genéricos como
   "peixe", "carne", "laticínios", "leguminosas", "glúten" — não apenas o
   nome exato do alimento), prioriza alimentos da lista de preferências do
   paciente e, para grupos de papel macro, prioriza maior densidade do
   nutriente-alvo; evita repetir o mesmo alimento no mesmo dia.
5) Para cada alimento escolhido, o sistema gera até 2 opções alternativas
   nutricionalmente equivalentes (mesmo grupo, mesmo contexto de refeição,
   kcal/100g dentro de +-25%), compostas na mesma linha unidas por "ou".
"""

import config
from database.foods_data import filtrar_alimentos

NUTRIENTE_ALVO_POR_GRUPO = {
    "carboidrato": "carboidrato_100g",
    "proteina": "proteina_100g",
    "gordura": "gordura_100g",
}

# Faixa de porção aceitável, como múltiplo da porção de referência de cada
# alimento (porcao_base_g). Gorduras usam teto mais baixo pois são densas
# em energia e porções grandes não são clinicamente usuais.
FAIXA_MULTIPLICADOR = {
    "carboidrato": (0.4, 2.0),
    "proteina": (0.4, 2.0),
    "gordura": (0.4, 1.5),
}

# Termos genéricos comumente usados por pacientes/nutricionistas para
# descrever categorias inteiras de alimentos a evitar, mapeados para os
# alimentos específicos do banco que pertencem a cada categoria. Isso
# garante que escrever apenas "peixe" já exclua tilápia e atum, sem
# precisar digitar o nome exato de cada preparação.
SINONIMOS_EVITAR = {
    "peixe": ["tilápia", "atum"],
    "peixes": ["tilápia", "atum"],
    "frutos do mar": ["tilápia", "atum"],
    "carne": ["patinho"],
    "carne vermelha": ["patinho"],
    "carne bovina": ["patinho"],
    "boi": ["patinho"],
    "frango": ["frango"],
    "aves": ["frango"],
    "galinha": ["frango"],
    "ovo": ["ovo"],
    "ovos": ["ovo"],
    "leite": ["leite", "iogurte", "queijo", "whey"],
    "laticinio": ["iogurte", "queijo", "whey"],
    "laticinios": ["iogurte", "queijo", "whey"],
    "laticínios": ["iogurte", "queijo", "whey"],
    "leguminosa": ["feijão", "lentilha", "grão-de-bico"],
    "leguminosas": ["feijão", "lentilha", "grão-de-bico"],
    "feijao": ["feijão"],
    "gluten": ["pão", "macarrão"],
    "glúten": ["pão", "macarrão"],
}


# ---------------------------------------------------------------------------
# FORMATAÇÃO DE QUANTIDADE E MEDIDA CASEIRA
# ---------------------------------------------------------------------------

def _formatar_quantidade(valor: float) -> str:
    """Arredonda para o múltiplo de 0,5 mais próximo (mínimo 0,5) e formata
    no padrão brasileiro (vírgula decimal), sem casas decimais desnecessárias."""
    valor = max(0.5, round(valor * 2) / 2)
    if valor == int(valor):
        return str(int(valor))
    return str(valor).replace(".", ",")


def formatar_alimento(alimento: dict, gramas: float) -> str:
    """Formata um alimento e sua porção no padrão 'quantidade medida_caseira
    de nome (gramas/ml)', ex.: '2 fatias de pão de forma (50 g)'."""
    unidade_peso = alimento.get("unidade_peso_g") or alimento["porcao_base_g"]
    quantidade = gramas / unidade_peso if unidade_peso else 1
    texto_qtd = _formatar_quantidade(quantidade)
    valor_num = float(texto_qtd.replace(",", "."))
    unidade_nome = alimento["unidade_nome"] if valor_num <= 1 else alimento["unidade_nome_plural"]
    unidade_medida = alimento.get("unidade_medida", "g")
    return f"{texto_qtd} {unidade_nome} de {alimento['nome']} ({gramas:.0f} {unidade_medida})"


# ---------------------------------------------------------------------------
# SELEÇÃO DE ALIMENTOS
# ---------------------------------------------------------------------------

def _termo_bate(evitado_termo: str, nome_alimento: str) -> bool:
    """Verifica se um termo informado pelo paciente/nutricionista (ex.:
    'peixe', 'carne', 'laticínios') deve excluir um alimento do banco,
    seja por correspondência direta no nome, seja por pertencer à
    categoria genérica mapeada em SINONIMOS_EVITAR."""
    if evitado_termo in nome_alimento:
        return True
    substitutos = SINONIMOS_EVITAR.get(evitado_termo)
    if substitutos and any(sub in nome_alimento for sub in substitutos):
        return True
    return False


def _ordenar_por_preferencia(alimentos: list, preferidos: list, evitados: list, grupo: str = None) -> list:
    """Ordena colocando alimentos preferidos primeiro e removendo indesejados
    (inclusive por termo genérico, ver _termo_bate). Para grupos com papel
    macro (proteína/carboidrato/gordura), usa como critério de desempate a
    maior densidade do nutriente-alvo por 100 g, priorizando fontes mais
    eficientes para atingir a meta com uma porção realista."""
    preferidos_lower = [p.strip().lower() for p in preferidos if p.strip()]
    evitados_lower = [e.strip().lower() for e in evitados if e.strip()]

    filtrados = [
        a for a in alimentos
        if not any(_termo_bate(ev, a["nome"].lower()) for ev in evitados_lower)
    ]

    campo_densidade = NUTRIENTE_ALVO_POR_GRUPO.get(grupo)

    def chave(alimento):
        nome = alimento["nome"].lower()
        eh_preferido = any(pref in nome for pref in preferidos_lower)
        densidade = -alimento.get(campo_densidade, 0) if campo_densidade else 0
        return (0 if eh_preferido else 1, densidade, alimento["nome"])

    return sorted(filtrados, key=chave)


def _escolher_alimento(grupo: str, restricoes: list, preferidos: list,
                       evitados: list, usados: set, contexto: str = None) -> dict:
    """Seleciona o próximo alimento disponível de um grupo, evitando repetição
    no mesmo dia e priorizando preferência/densidade do nutriente-alvo.
    O contexto ("refeicao_principal" ou "lanche") restringe a escolha a
    alimentos tradicionalmente adequados àquele tipo de refeição."""
    candidatos = filtrar_alimentos(grupo, restricoes, contexto)
    candidatos = _ordenar_por_preferencia(candidatos, preferidos, evitados, grupo)

    if not candidatos:
        # Relaxa primeiro o contexto, depois os "evitados", antes de desistir
        candidatos = filtrar_alimentos(grupo, restricoes)
        candidatos = _ordenar_por_preferencia(candidatos, preferidos, evitados, grupo)
        if not candidatos:
            return None

    nao_usados = [a for a in candidatos if a["nome"] not in usados]
    pool = nao_usados if nao_usados else candidatos

    escolhido = pool[0]
    usados.add(escolhido["nome"])
    return escolhido


def _macros_da_porcao(alimento: dict, gramas: float) -> dict:
    fator = gramas / 100
    return {
        "kcal": round(alimento["kcal_100g"] * fator, 1),
        "proteina": round(alimento["proteina_100g"] * fator, 1),
        "carboidrato": round(alimento["carboidrato_100g"] * fator, 1),
        "gordura": round(alimento["gordura_100g"] * fator, 1),
    }


def _faixa_porcao(alimento: dict, grupo: str) -> tuple:
    base = alimento["porcao_base_g"]
    mult_min, mult_max = FAIXA_MULTIPLICADOR.get(grupo, (0.4, 2.0))
    return base * mult_min, base * mult_max


def _calcular_porcao_por_nutriente(alimento: dict, grupo: str, alvo_g: float) -> float:
    """Calcula a porção (g) de um alimento a partir da meta do nutriente que
    ele representa na refeição (proteína/carboidrato/gordura), sempre
    dentro de uma faixa realista em torno da porção de referência do
    próprio alimento — evita tanto porções irrisórias quanto exageradas."""
    campo = NUTRIENTE_ALVO_POR_GRUPO.get(grupo)
    minimo, maximo = _faixa_porcao(alimento, grupo)

    if not campo:
        return alimento["porcao_base_g"]

    densidade = alimento.get(campo, 0)
    if densidade <= 0:
        gramas = alimento["porcao_base_g"]
    else:
        gramas = (alvo_g / densidade) * 100

    gramas = max(minimo, min(gramas, maximo))
    return round(gramas / 5) * 5


def _calcular_porcao_por_kcal(alimento: dict, kcal_alvo: float, grupo: str = None) -> float:
    if alimento["kcal_100g"] <= 0:
        return alimento["porcao_base_g"]
    gramas = (kcal_alvo / alimento["kcal_100g"]) * 100
    minimo, maximo = _faixa_porcao(alimento, grupo) if grupo else (10, 400)
    gramas = max(minimo, min(gramas, maximo))
    return round(gramas / 5) * 5


def gerar_alternativas(alimento: dict, restricoes: list, gramas_original: float,
                       contexto: str = None, evitados: list = None, limite: int = 2) -> list:
    """Gera até `limite` alternativas nutricionalmente equivalentes (mesmo
    grupo alimentar e contexto de refeição, kcal/100g dentro de +-25%,
    respeitando também os alimentos a evitar), recalculando a porção
    equivalente. Retorna lista de (alimento_dict, gramas)."""
    candidatos = filtrar_alimentos(alimento["grupo"], restricoes, contexto)
    evitados_lower = [e.strip().lower() for e in (evitados or []) if e.strip()]
    candidatos = [
        c for c in candidatos
        if not any(_termo_bate(ev, c["nome"].lower()) for ev in evitados_lower)
    ]
    kcal_original_total = alimento["kcal_100g"] * (gramas_original / 100)

    alternativas = []
    for c in candidatos:
        if c["nome"] == alimento["nome"]:
            continue
        razao = c["kcal_100g"] / alimento["kcal_100g"] if alimento["kcal_100g"] else 1
        if 0.75 <= razao <= 1.25:
            gramas_eq = _calcular_porcao_por_kcal(c, kcal_original_total, alimento["grupo"])
            alternativas.append((c, gramas_eq))
        if len(alternativas) >= limite:
            break
    return alternativas


# ---------------------------------------------------------------------------
# MONTAGEM DA REFEIÇÃO
# ---------------------------------------------------------------------------

def montar_refeicao(nome_refeicao: str, proteina_alvo_refeicao: float,
                     carboidrato_alvo_refeicao: float, gordura_alvo_refeicao: float,
                     restricoes: list, preferidos: list, evitados: list, usados: set) -> dict:
    """Monta uma refeição completa organizada em seções (entrada/prato/
    bebida/principal, conforme config.ESTRUTURA_REFEICAO). Cada item traz
    a descrição já formatada em medida caseira + gramas, com alternativas
    equivalentes unidas por 'ou'."""
    estrutura = config.ESTRUTURA_REFEICAO.get(nome_refeicao, [("principal", "carboidrato"), ("principal", "proteina")])
    contexto = "refeicao_principal" if nome_refeicao in ("Almoço", "Jantar") else "lanche"

    metas_nutriente = {
        "proteina": proteina_alvo_refeicao,
        "carboidrato": carboidrato_alvo_refeicao,
        "gordura": gordura_alvo_refeicao,
    }

    secoes = {}
    total_kcal = total_proteina = total_carboidrato = total_gordura = 0.0

    for secao, grupo in estrutura:
        alimento = _escolher_alimento(grupo, restricoes, preferidos, evitados, usados, contexto)
        if alimento is None:
            continue

        if grupo in NUTRIENTE_ALVO_POR_GRUPO:
            gramas = _calcular_porcao_por_nutriente(alimento, grupo, metas_nutriente[grupo])
        else:
            gramas = alimento["porcao_base_g"]

        macros = _macros_da_porcao(alimento, gramas)
        alternativas = gerar_alternativas(alimento, restricoes, gramas, contexto, evitados)

        partes_texto = [formatar_alimento(alimento, gramas)]
        for alt_alimento, alt_gramas in alternativas:
            partes_texto.append(formatar_alimento(alt_alimento, alt_gramas))
        descricao = " ou ".join(partes_texto)

        item = {
            "grupo": grupo,
            "nome": alimento["nome"],
            "gramas": gramas,
            "descricao": descricao,
            "kcal": macros["kcal"],
            "proteina": macros["proteina"],
            "carboidrato": macros["carboidrato"],
            "gordura": macros["gordura"],
        }

        secoes.setdefault(secao, []).append(item)

        total_kcal += macros["kcal"]
        total_proteina += macros["proteina"]
        total_carboidrato += macros["carboidrato"]
        total_gordura += macros["gordura"]

    secoes_ordenadas = [
        {"secao": s, "titulo": config.ROTULO_SECAO.get(s), "itens": secoes[s]}
        for s in config.ORDEM_SECOES if s in secoes
    ]

    return {
        "nome": nome_refeicao,
        "secoes": secoes_ordenadas,
        "totais": {
            "kcal": round(total_kcal, 1),
            "proteina": round(total_proteina, 1),
            "carboidrato": round(total_carboidrato, 1),
            "gordura": round(total_gordura, 1),
        },
    }