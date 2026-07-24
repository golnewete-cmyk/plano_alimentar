"""
utils/validators.py

Validação dos dados do paciente antes de acionar o motor de geração do
plano alimentar. Garante integridade e plausibilidade fisiológica dos
valores informados pela nutricionista.
"""


def validar_paciente(paciente: dict) -> list:
    """Retorna uma lista de mensagens de erro. Lista vazia significa que os
    dados são válidos e o plano pode ser gerado."""
    erros = []

    peso = paciente.get("peso", 0)
    altura = paciente.get("altura", 0)
    idade = paciente.get("idade", 0)

    if not (30 <= peso <= 300):
        erros.append("Peso deve estar entre 30 kg e 300 kg.")

    if not (100 <= altura <= 250):
        erros.append("Altura deve estar entre 100 cm e 250 cm.")

    if not (10 <= idade <= 100):
        erros.append("Idade deve estar entre 10 e 100 anos.")

    if paciente.get("sexo") not in ("masculino", "feminino"):
        erros.append("Sexo biológico deve ser informado.")

    if paciente.get("nivel_atividade") not in (
        "sedentario", "leve", "moderado", "alto", "muito_alto"
    ):
        erros.append("Nível de atividade física inválido.")

    if paciente.get("objetivo") not in ("emagrecimento", "manutencao", "hipertrofia"):
        erros.append("Objetivo do plano inválido.")

    if paciente.get("numero_refeicoes") not in (3, 4, 5, 6):
        erros.append("Número de refeições deve estar entre 3 e 6.")

    restricoes = paciente.get("restricoes", [])
    if "vegano" in restricoes and "vegetariano" in restricoes:
        # vegano já implica vegetariano; não é erro, apenas normaliza
        pass

    return erros