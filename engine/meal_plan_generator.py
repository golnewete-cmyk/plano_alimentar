"""
engine/meal_plan_generator.py

Orquestra a geração completa do plano alimentar:
1) Calcula as necessidades nutricionais do paciente (calculations.py)
2) Distribui o VET entre as refeições do dia conforme o número de
   refeições escolhido (config.TEMPLATES_REFEICOES)
3) Monta cada refeição selecionando alimentos compatíveis (food_selector.py)
4) Valida o plano final comparando totais reais x necessidades calculadas
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

    restricoes = paciente.get("restricoes", [])
    preferidos = paciente.get("alimentos_preferidos", [])
    evitados = paciente.get("alimentos_evitados", [])

    usados = set()
    contadores = {}

    refeicoes = []
    for bloco in template:
        pct = bloco["pct"]
        kcal_alvo = necessidades.vet * pct
        refeicao = montar_refeicao(
            nome_refeicao=bloco["nome"],
            kcal_alvo_refeicao=kcal_alvo,
            proteina_alvo_refeicao=necessidades.proteina_g * pct,
            carboidrato_alvo_refeicao=necessidades.carboidrato_g * pct,
            gordura_alvo_refeicao=necessidades.gordura_g * pct,
            restricoes=restricoes,
            preferidos=preferidos,
            evitados=evitados,
            usados=usados,
            contadores=contadores,
        )
        refeicao["kcal_alvo"] = round(kcal_alvo, 1)
        refeicoes.append(refeicao)

    totais_dia = _somar_totais(refeicoes)

    # ---- Calibração fina -------------------------------------------------
    # A montagem de cada refeição é resolvida de forma independente; pequenos
    # desvios acumulados entre refeições podem levar o total diário a ficar
    # fora da tolerância. Aplica-se aqui um fator de escala proporcional
    # apenas sobre os alimentos de papel macro (carboidrato/proteína/
    # gordura) — vegetais e frutas mantêm a porção de referência fixa, pois
    # seu papel é fibra/micronutrientes — para aproximar o total real do VET
    # calculado cientificamente.
    if necessidades.vet > 0:
        fator_escala = necessidades.vet / totais_dia["kcal"] if totais_dia["kcal"] else 1.0
        if abs(fator_escala - 1.0) > 0.02:
            for refeicao in refeicoes:
                for item in refeicao["itens"]:
                    if item["grupo"] not in ("vegetal", "fruta"):
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

    imc = calcular_imc(paciente["peso"], paciente["altura"])

    return {
        "paciente": paciente,
        "necessidades": necessidades,
        "imc": imc,
        "classificacao_imc": classificar_imc(imc),
        "refeicoes": refeicoes,
        "totais_dia": totais_dia,
        "validacao": validacao,
    }


def _somar_totais(refeicoes: list) -> dict:
    return {
        "kcal": round(sum(r["totais"]["kcal"] for r in refeicoes), 1),
        "proteina": round(sum(r["totais"]["proteina"] for r in refeicoes), 1),
        "carboidrato": round(sum(r["totais"]["carboidrato"] for r in refeicoes), 1),
        "gordura": round(sum(r["totais"]["gordura"] for r in refeicoes), 1),
    }


def _recalcular_totais_refeicao(refeicao: dict) -> None:
    refeicao["totais"] = {
        "kcal": round(sum(i["kcal"] for i in refeicao["itens"]), 1),
        "proteina": round(sum(i["proteina"] for i in refeicao["itens"]), 1),
        "carboidrato": round(sum(i["carboidrato"] for i in refeicao["itens"]), 1),
        "gordura": round(sum(i["gordura"] for i in refeicao["itens"]), 1),
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