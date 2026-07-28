"""
engine/meal_plan_generator.py

Orquestra a geração completa do plano alimentar:
1) Calcula as necessidades nutricionais do paciente (calculations.py)
2) Distribui o VET e os macronutrientes entre as refeições do dia
3) Monta cada refeição em seções (entrada/prato/bebida/principal),
   selecionando alimentos compatíveis e formatando a descrição no padrão
   clínico de referência (food_selector.py)
4) Aplica calibração fina proporcional para aproximar o total real do VET
5) Gera as recomendações clínicas (hidratação + orientações gerais)
6) Valida o plano final comparando totais reais x necessidades calculadas
"""

import config
from engine.calculations import calcular_necessidades, calcular_imc, classificar_imc
from engine.food_selector import montar_refeicao

TOLERANCIA_KCAL = 0.08          # +-8% de tolerância no total calórico diário
TOLERANCIA_PROTEINA = 0.15      # +-15% de tolerância na proteína diária


def gerar_plano_alimentar(paciente: dict) -> dict:
    necessidades = calcular_necessidades(paciente)

    num_refeicoes = paciente["numero_refeicoes"]
    template = config.TEMPLATES_REFEICOES[num_refeicoes]
    horarios = config.HORARIOS_REFEICOES[num_refeicoes]

    restricoes = paciente.get("restricoes", [])
    preferidos = paciente.get("alimentos_preferidos", [])
    evitados = paciente.get("alimentos_evitados", [])

    usados = set()

    refeicoes = []
    for bloco in template:
        pct = bloco["pct"]
        nome = bloco["nome"]
        refeicao = montar_refeicao(
            nome_refeicao=nome,
            proteina_alvo_refeicao=necessidades.proteina_g * pct,
            carboidrato_alvo_refeicao=necessidades.carboidrato_g * pct,
            gordura_alvo_refeicao=necessidades.gordura_g * pct,
            restricoes=restricoes,
            preferidos=preferidos,
            evitados=evitados,
            usados=usados,
        )
        refeicao["horario"] = horarios.get(nome, "")
        refeicao["kcal_alvo"] = round(necessidades.vet * pct, 1)
        refeicoes.append(refeicao)

    # Ordena as refeições pelo horário sugerido
    refeicoes.sort(key=lambda r: r["horario"])

    totais_dia = _somar_totais(refeicoes)

    # ---- Calibração fina -------------------------------------------------
    # A montagem de cada refeição é resolvida de forma independente; pequenos
    # desvios acumulados entre refeições podem levar o total diário a ficar
    # fora da tolerância. Aplica-se aqui um fator de escala proporcional
    # apenas sobre os itens de papel macro (carboidrato/proteína/gordura) —
    # vegetais e bebidas mantêm a porção fixa de referência — para aproximar
    # o total real do VET calculado cientificamente.
    if necessidades.vet > 0 and totais_dia["kcal"] > 0:
        fator_escala = necessidades.vet / totais_dia["kcal"]
        if abs(fator_escala - 1.0) > 0.02:
            for refeicao in refeicoes:
                for secao in refeicao["secoes"]:
                    for item in secao["itens"]:
                        if item["grupo"] not in config.GRUPOS_PORCAO_FIXA:
                            gramas_antigas = item["gramas"]
                            nova_gramas = max(10, min(gramas_antigas * fator_escala, 400))
                            nova_gramas = round(nova_gramas / 5) * 5
                            razao = (nova_gramas / gramas_antigas) if gramas_antigas else 1.0
                            item["gramas"] = nova_gramas
                            item["kcal"] = round(item["kcal"] * razao, 1)
                            item["proteina"] = round(item["proteina"] * razao, 1)
                            item["carboidrato"] = round(item["carboidrato"] * razao, 1)
                            item["gordura"] = round(item["gordura"] * razao, 1)
                _recalcular_totais_refeicao(refeicao)
            totais_dia = _somar_totais(refeicoes)

    validacao = _validar_plano(totais_dia, necessidades)
    recomendacoes = _gerar_recomendacoes(paciente)
    imc = calcular_imc(paciente["peso"], paciente["altura"])

    return {
        "paciente": paciente,
        "necessidades": necessidades,
        "imc": imc,
        "classificacao_imc": classificar_imc(imc),
        "refeicoes": refeicoes,
        "totais_dia": totais_dia,
        "validacao": validacao,
        "recomendacoes": recomendacoes,
    }


def _somar_totais(refeicoes: list) -> dict:
    return {
        "kcal": round(sum(r["totais"]["kcal"] for r in refeicoes), 1),
        "proteina": round(sum(r["totais"]["proteina"] for r in refeicoes), 1),
        "carboidrato": round(sum(r["totais"]["carboidrato"] for r in refeicoes), 1),
        "gordura": round(sum(r["totais"]["gordura"] for r in refeicoes), 1),
    }


def _recalcular_totais_refeicao(refeicao: dict) -> None:
    itens = [item for secao in refeicao["secoes"] for item in secao["itens"]]
    refeicao["totais"] = {
        "kcal": round(sum(i["kcal"] for i in itens), 1),
        "proteina": round(sum(i["proteina"] for i in itens), 1),
        "carboidrato": round(sum(i["carboidrato"] for i in itens), 1),
        "gordura": round(sum(i["gordura"] for i in itens), 1),
    }


def _validar_plano(totais_dia: dict, necessidades) -> dict:
    """Verifica se o plano gerado está dentro das tolerâncias aceitáveis
    em relação ao VET e à meta de proteína calculados cientificamente."""
    kcal_diff_pct = abs(totais_dia["kcal"] - necessidades.vet) / necessidades.vet
    proteina_diff_pct = (
        abs(totais_dia["proteina"] - necessidades.proteina_g) / necessidades.proteina_g
        if necessidades.proteina_g else 0
    )

    kcal_ok = kcal_diff_pct <= TOLERANCIA_KCAL
    proteina_ok = proteina_diff_pct <= TOLERANCIA_PROTEINA

    mensagens = []
    if not kcal_ok:
        mensagens.append(
            f"Valor calórico total do plano ({totais_dia['kcal']:.0f} kcal) "
            f"fora da tolerância de {TOLERANCIA_KCAL*100:.0f}% em relação à "
            f"meta ({necessidades.vet:.0f} kcal)."
        )
    if not proteina_ok:
        mensagens.append(
            f"Proteína total do plano ({totais_dia['proteina']:.0f} g) fora "
            f"da tolerância de {TOLERANCIA_PROTEINA*100:.0f}% em relação à "
            f"meta ({necessidades.proteina_g:.0f} g)."
        )

    return {
        "aprovado": kcal_ok and proteina_ok,
        "kcal_diff_pct": round(kcal_diff_pct * 100, 1),
        "proteina_diff_pct": round(proteina_diff_pct * 100, 1),
        "mensagens": mensagens,
    }


def _gerar_recomendacoes(paciente: dict) -> dict:
    """Gera a seção de recomendações clínicas: faixa de ingestão hídrica
    (30-35 mL/kg/dia) e orientações gerais, complementadas conforme o
    objetivo e as restrições alimentares do paciente."""
    peso = paciente["peso"]
    agua_min_l = round(peso * config.AGUA_ML_KG_MIN / 1000, 1)
    agua_max_l = round(peso * config.AGUA_ML_KG_MAX / 1000, 1)

    tips = list(config.RECOMENDACOES_GERAIS)

    tip_objetivo = config.RECOMENDACOES_POR_OBJETIVO.get(paciente.get("objetivo"))
    if tip_objetivo:
        tips.append(tip_objetivo)

    for restricao in paciente.get("restricoes", []):
        tip = config.RECOMENDACOES_POR_RESTRICAO.get(restricao)
        if tip:
            tips.append(tip)

    return {
        "agua_min_l": agua_min_l,
        "agua_max_l": agua_max_l,
        "outras": tips,
    }