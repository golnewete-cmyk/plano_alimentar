"""
engine/food_selector.py

Algoritmo determinístico de seleção de alimentos e cálculo de porções.

Regras de decisão implementadas:
1) Cada refeição possui uma "estrutura" (config.ESTRUTURA_REFEICAO) que
   define quais grupos alimentares devem compor aquela refeição.
2) A energia alocada à refeição é distribuída entre os grupos presentes
   segundo pesos nutricionalmente coerentes (GROUP_ALLOCATION), garantindo
   que carboidrato/proteína dominem as refeições principais e frutas/
   vegetais complementem com fibras e micronutrientes.
3) A seleção do alimento específico dentro de cada grupo é determinística:
   respeita restrições alimentares, prioriza alimentos da lista de
   preferências do paciente e evita repetir o mesmo alimento mais de uma
   vez no mesmo dia (varredura circular sobre a lista filtrada).
4) A porção (em gramas) é calculada para que o alimento entregue a energia
   alocada a ele, arredondada em múltiplos de 5 g para viabilidade prática.
5) Para cada alimento escolhido, o sistema gera até 2 substituições
   nutricionalmente equivalentes (mesmo grupo, valor calórico por 100 g
   dentro de +-25%), recalculando a porção equivalente em gramas.
"""

import config
from database.foods_data import filtrar_alimentos

# Nutriente "alvo" que cada papel de grupo deve preencher diretamente.
# Em vez de repartir apenas calorias entre os grupos (o que distorce a
# meta de proteína quando o alimento escolhido tem baixa densidade
# proteica, ex.: feijão), a porção de cada alimento é calculada para
# entregar o nutriente que ele representa na refeição. Vegetais e frutas
# usam porção fixa de referência (medida caseira padrão), pois seu papel
# nutricional principal é fibra e micronutrientes, não macro principal.
NUTRIENTE_ALVO_POR_GRUPO = {
    "carboidrato": "carboidrato_100g",
    "proteina": "proteina_100g",
    "gordura": "gordura_100g",
}


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
                        evitados: list, usados: set, contadores: dict) -> dict:
    """Seleciona o próximo alimento disponível de um grupo, evitando repetição
    no mesmo dia. Usa varredura circular determinística por grupo."""
    candidatos = filtrar_alimentos(grupo, restricoes)
    candidatos = _ordenar_por_preferencia(candidatos, preferidos, evitados, grupo)

    if not candidatos:
        # Sem alimentos compatíveis: relaxa apenas a exclusão de "evitados"
        candidatos = filtrar_alimentos(grupo, restricoes)
        if not candidatos:
            return None

    nao_usados = [a for a in candidatos if a["nome"] not in usados]
    pool = nao_usados if nao_usados else candidatos

    # Sempre toma o primeiro da lista (já ordenada por preferência e, para
    # papéis macro, por maior densidade do nutriente-alvo). Como os
    # alimentos já usados no dia são removidos do pool, a variedade entre
    # as refeições é garantida naturalmente, sem sacrificar a aderência
    # nutricional ao escolher alimentos de baixa densidade por rotação cega.
    escolhido = pool[0]
    usados.add(escolhido["nome"])
    contadores[grupo] = contadores.get(grupo, 0) + 1
    return escolhido


def _calcular_porcao_g(alimento: dict, kcal_alvo: float) -> float:
    if alimento["kcal_100g"] <= 0:
        return alimento["porcao_base_g"]
    gramas = (kcal_alvo / alimento["kcal_100g"]) * 100
    gramas = max(10, min(gramas, 400))
    return round(gramas / 5) * 5


def _calcular_porcao_por_nutriente(alimento: dict, nutriente_campo: str, alvo_g: float) -> float:
    """Calcula a porção (g) necessária para que o alimento entregue
    `alvo_g` gramas do nutriente indicado (proteína, carboidrato ou
    gordura), respeitando limites práticos de porção (10 g a 400 g)."""
    densidade = alimento.get(nutriente_campo, 0)
    if densidade <= 0:
        return alimento["porcao_base_g"]
    gramas = (alvo_g / densidade) * 100
    gramas = max(10, min(gramas, 400))
    return round(gramas / 5) * 5


def _macros_da_porcao(alimento: dict, gramas: float) -> dict:
    fator = gramas / 100
    return {
        "kcal": round(alimento["kcal_100g"] * fator, 1),
        "proteina": round(alimento["proteina_100g"] * fator, 1),
        "carboidrato": round(alimento["carboidrato_100g"] * fator, 1),
        "gordura": round(alimento["gordura_100g"] * fator, 1),
    }


def gerar_substituicoes(alimento: dict, restricoes: list, gramas_original: float, limite: int = 2) -> list:
    """Gera substituições nutricionalmente equivalentes (mesmo grupo alimentar,
    kcal/100g dentro de +-25%) recalculando a porção equivalente em gramas."""
    candidatos = filtrar_alimentos(alimento["grupo"], restricoes)
    kcal_original_total = alimento["kcal_100g"] * (gramas_original / 100)

    equivalentes = []
    for c in candidatos:
        if c["nome"] == alimento["nome"]:
            continue
        razao = c["kcal_100g"] / alimento["kcal_100g"] if alimento["kcal_100g"] else 1
        if 0.75 <= razao <= 1.25:
            gramas_eq = _calcular_porcao_g(c, kcal_original_total)
            equivalentes.append({
                "nome": c["nome"],
                "gramas": gramas_eq,
                "medida_caseira_referencia": c["medida_caseira"],
                "porcao_base_g": c["porcao_base_g"],
            })
        if len(equivalentes) >= limite:
            break
    return equivalentes


def _resolver_porcoes_macro(alimentos_macro: list, alvo_vetor: dict) -> dict:
    """Resolve um sistema linear para determinar, em conjunto, a porção (g)
    de cada alimento de papel macro (carboidrato/proteína/gordura) presente
    na refeição, de modo que a soma dos três (considerando que cada alimento
    contribui um pouco de cada macronutriente) atinja as metas de proteína,
    carboidrato e gordura da refeição simultaneamente. Isso evita o erro de
    calcular cada alimento isoladamente e somar excedentes cruzados (ex.:
    o feijão contribui tanto para proteína quanto para carboidrato).

    Retorna um dicionário {nome_do_grupo: gramas}.
    """
    import numpy as np

    papeis = [grupo for grupo, _alimento in alimentos_macro]
    n = len(papeis)
    if n == 0:
        return {}

    # Matriz A: A[i][j] = gramas do macronutriente do papel i entregues por
    # 1 grama do alimento do papel j. Vetor b: meta (g) do macronutriente do papel i.
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
        # Sistema singular (ex.: alimento sem nenhum dos nutrientes-alvo):
        # recorre a uma estimativa isolada por nutriente como fallback seguro.
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


def montar_refeicao(nome_refeicao: str, kcal_alvo_refeicao: float,
                     proteina_alvo_refeicao: float, carboidrato_alvo_refeicao: float,
                     gordura_alvo_refeicao: float, restricoes: list,
                     preferidos: list, evitados: list, usados: set, contadores: dict) -> dict:
    """Monta uma refeição completa: seleciona alimentos de cada grupo exigido
    pela estrutura da refeição. Vegetais e frutas recebem porção fixa de
    referência (papel de fibra/micronutrientes); os alimentos de papel
    macro (carboidrato/proteína/gordura) têm suas porções calculadas em
    conjunto, via sistema linear, para atingir as metas de macronutrientes
    da refeição de forma coerente."""
    grupos = config.ESTRUTURA_REFEICAO.get(nome_refeicao, ["carboidrato", "proteina"])

    metas_nutriente = {
        "proteina": proteina_alvo_refeicao,
        "carboidrato": carboidrato_alvo_refeicao,
        "gordura": gordura_alvo_refeicao,
    }

    selecionados = []  # (grupo, alimento)
    for grupo in grupos:
        alimento = _escolher_alimento(grupo, restricoes, preferidos, evitados, usados, contadores)
        if alimento is not None:
            selecionados.append((grupo, alimento))

    alimentos_macro = [(g, a) for g, a in selecionados if g in NUTRIENTE_ALVO_POR_GRUPO]
    alimentos_fixos = [(g, a) for g, a in selecionados if g not in NUTRIENTE_ALVO_POR_GRUPO]

    gramas_macro = _resolver_porcoes_macro(alimentos_macro, metas_nutriente)

    itens = []
    total_kcal = total_proteina = total_carboidrato = total_gordura = 0.0

    for grupo, alimento in selecionados:
        if grupo in gramas_macro:
            gramas = gramas_macro[grupo]
        else:
            gramas = alimento["porcao_base_g"]

        macros = _macros_da_porcao(alimento, gramas)
        substituicoes = gerar_substituicoes(alimento, restricoes, gramas)

        itens.append({
            "grupo": grupo,
            "nome": alimento["nome"],
            "gramas": gramas,
            "medida_caseira": alimento["medida_caseira"],
            "porcao_base_g": alimento["porcao_base_g"],
            "kcal": macros["kcal"],
            "proteina": macros["proteina"],
            "carboidrato": macros["carboidrato"],
            "gordura": macros["gordura"],
            "substituicoes": substituicoes,
        })

        total_kcal += macros["kcal"]
        total_proteina += macros["proteina"]
        total_carboidrato += macros["carboidrato"]
        total_gordura += macros["gordura"]

    return {
        "nome": nome_refeicao,
        "itens": itens,
        "totais": {
            "kcal": round(total_kcal, 1),
            "proteina": round(total_proteina, 1),
            "carboidrato": round(total_carboidrato, 1),
            "gordura": round(total_gordura, 1),
        },
    }