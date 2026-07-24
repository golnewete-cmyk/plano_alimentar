"""
engine/calculations.py

Implementa os cálculos científicos do sistema:
- Gasto Energético Basal (GEB) via Mifflin-St Jeor
- Gasto Energético Total (GET/TDEE)
- Ajuste calórico por objetivo
- Distribuição de macronutrientes (proteína, lipídio, carboidrato)

Todas as fórmulas e faixas de referência estão documentadas em config.py.
"""

from dataclasses import dataclass

import config


@dataclass
class NecessidadesNutricionais:
    geb: float
    get: float
    vet: float  # valor energético total (VET) já ajustado pelo objetivo
    proteina_g: float
    gordura_g: float
    carboidrato_g: float
    proteina_kcal: float
    gordura_kcal: float
    carboidrato_kcal: float


def calcular_geb(sexo: str, peso_kg: float, altura_cm: float, idade: int) -> float:
    """
    Gasto Energético Basal pela equação de Mifflin-St Jeor (1990).

    Homens:   GEB = 10*peso + 6.25*altura - 5*idade + 5
    Mulheres: GEB = 10*peso + 6.25*altura - 5*idade - 161
    """
    base = 10 * peso_kg + 6.25 * altura_cm - 5 * idade
    if sexo == "masculino":
        return base + 5
    return base - 161


def calcular_get(geb: float, nivel_atividade: str) -> float:
    """Gasto Energético Total = GEB x Fator de Atividade (PAL)."""
    pal = config.FATORES_ATIVIDADE[nivel_atividade]["pal"]
    return geb * pal


def aplicar_ajuste_objetivo(get: float, objetivo: str) -> float:
    """Aplica o percentual de déficit/superávit calórico conforme o objetivo."""
    ajuste = config.AJUSTE_OBJETIVO[objetivo]
    return get * (1 + ajuste)


def aplicar_limites_seguranca(vet: float, sexo: str) -> float:
    """Garante que o VET final não fique abaixo de limites mínimos de segurança
    nem acima de um teto máximo plausível para um plano alimentar padrão."""
    minimo = config.KCAL_MINIMO_HOMEM if sexo == "masculino" else config.KCAL_MINIMO_MULHER
    vet = max(vet, minimo)
    vet = min(vet, config.KCAL_MAXIMO)
    return vet


def calcular_macronutrientes(vet: float, peso_kg: float, objetivo: str) -> dict:
    """
    Distribui o VET em proteína, gordura e carboidrato.

    1) Proteína definida em g/kg (ISSN Position Stand, 2017).
    2) Gordura definida como percentual do VET (DRI/IOM 2005), respeitando
       piso mínimo de 0.8 g/kg.
    3) Carboidrato = valor residual do VET, respeitando piso mínimo de
       segurança (config.CARBOIDRATO_MINIMO_G).
    """
    proteina_g_kg = config.PROTEINA_G_KG[objetivo]
    proteina_g = proteina_g_kg * peso_kg
    proteina_kcal = proteina_g * config.KCAL_POR_G["proteina"]

    gordura_kcal = vet * config.PERCENTUAL_LIPIDIOS
    gordura_g = gordura_kcal / config.KCAL_POR_G["gordura"]
    gordura_minima_g = config.LIPIDIOS_MIN_G_KG * peso_kg
    if gordura_g < gordura_minima_g:
        gordura_g = gordura_minima_g
        gordura_kcal = gordura_g * config.KCAL_POR_G["gordura"]

    carboidrato_kcal = vet - proteina_kcal - gordura_kcal
    carboidrato_g = carboidrato_kcal / config.KCAL_POR_G["carboidrato"]

    if carboidrato_g < config.CARBOIDRATO_MINIMO_G:
        carboidrato_g = config.CARBOIDRATO_MINIMO_G
        carboidrato_kcal = carboidrato_g * config.KCAL_POR_G["carboidrato"]
        # Recalcula o VET total para manter consistência interna do plano
        vet = proteina_kcal + gordura_kcal + carboidrato_kcal

    return {
        "vet": vet,
        "proteina_g": round(proteina_g, 1),
        "gordura_g": round(gordura_g, 1),
        "carboidrato_g": round(carboidrato_g, 1),
        "proteina_kcal": round(proteina_kcal, 0),
        "gordura_kcal": round(gordura_kcal, 0),
        "carboidrato_kcal": round(carboidrato_kcal, 0),
    }


def calcular_necessidades(paciente: dict) -> NecessidadesNutricionais:
    """Orquestra todo o cálculo científico a partir dos dados do paciente."""
    geb = calcular_geb(paciente["sexo"], paciente["peso"], paciente["altura"], paciente["idade"])
    get = calcular_get(geb, paciente["nivel_atividade"])
    vet = aplicar_ajuste_objetivo(get, paciente["objetivo"])
    vet = aplicar_limites_seguranca(vet, paciente["sexo"])
    macros = calcular_macronutrientes(vet, paciente["peso"], paciente["objetivo"])

    return NecessidadesNutricionais(
        geb=round(geb, 0),
        get=round(get, 0),
        vet=round(macros["vet"], 0),
        proteina_g=macros["proteina_g"],
        gordura_g=macros["gordura_g"],
        carboidrato_g=macros["carboidrato_g"],
        proteina_kcal=macros["proteina_kcal"],
        gordura_kcal=macros["gordura_kcal"],
        carboidrato_kcal=macros["carboidrato_kcal"],
    )


def calcular_imc(peso_kg: float, altura_cm: float) -> float:
    altura_m = altura_cm / 100
    return round(peso_kg / (altura_m ** 2), 1)


def classificar_imc(imc: float) -> str:
    if imc < 18.5:
        return "Abaixo do peso"
    if imc < 25:
        return "Peso adequado"
    if imc < 30:
        return "Sobrepeso"
    if imc < 35:
        return "Obesidade grau I"
    if imc < 40:
        return "Obesidade grau II"
    return "Obesidade grau III"