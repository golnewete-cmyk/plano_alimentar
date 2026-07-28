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
2) Alimentos de papel macro (carboidrato/proteína/gordura) têm a porção
   conjunta de todos os itens da refeição resolvida por um sistema linear,
   de modo a atingir simultaneamente as metas de proteína, carboidrato e
   gordura da refeição (evitando dupla contagem de macronutrientes entre
   alimentos, ex.: feijão contribuindo tanto proteína quanto carboidrato).
3) Vegetais e bebidas (config.GRUPOS_PORCAO_FIXA) recebem porção fixa de
   referência — seu papel nutricional é fibra/micronutrientes/hidratação,
   não macronutriente principal.
4) A seleção do alimento específico dentro de cada grupo é determinística:
   respeita restrições alimentares, prioriza alimentos da lista de
   preferências do paciente e, para grupos de papel macro, prioriza maior
   densidade do nutriente-alvo; evita repetir o mesmo alimento no mesmo dia.
5) Para cada alimento escolhido, o sistema gera até 2 opções alternativas
   nutricionalmente equivalentes (mesmo grupo, kcal/100g dentro de +-25%),
   compostas na mesma linha unidas por "ou", como na prática clínica de
   referência (ex.: "2 fatias de pão de forma (50 g) ou 1 unidade de pão
   francês (50 g)").
"""

import numpy as np

import config
from database.foods_data import filtrar_alimentos

NUTRIENTE_ALVO_POR_GRUPO = {
    "carboidrato": "carboidrato_100g",
    "proteina": "proteina_100g",
    "gordura": "gordura_100g",
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

def _ordenar_por_preferencia(alimentos: list, preferidos: list, evitados: list, grupo: str = None) -> list:
    """Ordena colocando alimentos preferidos primeiro e removendo indesejados.
    Para grupos com papel macro (proteína/carboidrato/gordura), usa como
    critério de desempate a maior densidade do nutriente-alvo por 100 g —
    isso evita que um alimento de baixa densidade proteica (ex.: leguminosas,
    ~5-9 g de proteína/100 g) seja escalado a porções irreais (300-400 g)
    só para tentar atingir a meta de proteína de uma refeição."""
    preferidos_lower = [p.strip().lower() for p in preferidos if p.strip()]
    evitados_lower = [e.strip().lower() for e in evitados if e.strip()]

    filtrados = [
        a for a in alimentos
        if not any(ev in a["nome"].lower() for ev in evitados_lower)
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


def _calcular_porcao_por_kcal(alimento: dict, kcal_alvo: float) -> float:
    if alimento["kcal_100g"] <= 0:
        return alimento["porcao_base_g"]
    gramas = (kcal_alvo / alimento["kcal_100g"]) * 100
    gramas = max(10, min(gramas, 400))
    return round(gramas / 5) * 5


def gerar_alternativas(alimento: dict, restricoes: list, gramas_original: float,
                       contexto: str = None, limite: int = 2) -> list:
    """Gera até `limite` alternativas nutricionalmente equivalentes (mesmo
    grupo alimentar e contexto de refeição, kcal/100g dentro de +-25%),
    recalculando a porção equivalente. Retorna lista de (alimento_dict, gramas)."""
    candidatos = filtrar_alimentos(alimento["grupo"], restricoes, contexto)
    kcal_original_total = alimento["kcal_100g"] * (gramas_original / 100)

    alternativas = []
    for c in candidatos:
        if c["nome"] == alimento["nome"]:
            continue
        razao = c["kcal_100g"] / alimento["kcal_100g"] if alimento["kcal_100g"] else 1
        if 0.75 <= razao <= 1.25:
            gramas_eq = _calcular_porcao_por_kcal(c, kcal_original_total)
            alternativas.append((c, gramas_eq))
        if len(alternativas) >= limite:
            break
    return alternativas


# ---------------------------------------------------------------------------
# SISTEMA LINEAR DE PORÇÕES (macronutrientes)
# ---------------------------------------------------------------------------

def _resolver_porcoes_macro(alimentos_macro: list, alvo_vetor: dict) -> dict:
    """Resolve, em conjunto, a porção (g) de cada alimento de papel macro
    presente na refeição, de modo que a soma atinja as metas de proteína,
    carboidrato e gordura simultaneamente. Retorna {grupo: gramas}."""
    papeis = [grupo for grupo, _alimento in alimentos_macro]
    n = len(papeis)
    if n == 0:
        return {}

    A = np.zeros((n, n))
    b = np.zeros(n)
    for i, papel_i in enumerate(papeis):
        campo = NUTRIENTE_ALVO_POR_GRUPO[papel_i]
        b[i] = alvo_vetor[papel_i]
        for j, (_papel_j, alimento_j) in enumerate(alimentos_macro):
            A[i][j] = alimento_j.get(campo, 0) / 100.0

    try:
        x = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        x = np.array([
            (alvo_vetor[papeis[j]] / max(alimentos_macro[j][1].get(NUTRIENTE_ALVO_POR_GRUPO[papeis[j]], 0), 0.01)) * 100
            if alimentos_macro[j][1].get(NUTRIENTE_ALVO_POR_GRUPO[papeis[j]], 0) > 0
            else alimentos_macro[j][1]["porcao_base_g"]
            for j in range(n)
        ])

    gramas_por_papel = {}
    for j, papel_j in enumerate(papeis):
        gramas = max(10.0, min(float(x[j]), 400.0))
        gramas_por_papel[papel_j] = round(gramas / 5) * 5
    return gramas_por_papel


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

    selecionados = []  # (secao, grupo, alimento)
    for secao, grupo in estrutura:
        alimento = _escolher_alimento(grupo, restricoes, preferidos, evitados, usados, contexto)
        if alimento is not None:
            selecionados.append((secao, grupo, alimento))

    alimentos_macro = [(g, a) for _s, g, a in selecionados if g in NUTRIENTE_ALVO_POR_GRUPO]
    gramas_macro = _resolver_porcoes_macro(alimentos_macro, metas_nutriente)

    secoes = {}
    total_kcal = total_proteina = total_carboidrato = total_gordura = 0.0

    for secao, grupo, alimento in selecionados:
        gramas = gramas_macro.get(grupo, alimento["porcao_base_g"])
        macros = _macros_da_porcao(alimento, gramas)
        alternativas = gerar_alternativas(alimento, restricoes, gramas, contexto)

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