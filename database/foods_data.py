"""
database/foods_data.py

Banco de alimentos estruturado por grupo alimentar.

Cada alimento contém:
- nome
- grupo: carboidrato | proteina | gordura | vegetal | fruta
- kcal_100g, proteina_100g, carboidrato_100g, gordura_100g (composição por
  100 g, valores de referência da Tabela Brasileira de Composição de
  Alimentos - TACO/UNICAMP e USDA FoodData Central)
- porcao_base_g: porção usual de referência (medida caseira)
- medida_caseira: descrição da porção usual em linguagem popular
- restricoes_incompativeis: lista de restrições que EXCLUEM este alimento
  (ex.: um alimento com glúten possui "sem_gluten" nesta lista, pois é
  incompatível com quem restringe glúten)
- tags: marcadores adicionais (ex.: "vegano", "integral")

O banco foi projetado para ser facilmente expansível: basta adicionar
novos dicionários às listas abaixo.
"""

FOODS = [
    # ---------------------------- CARBOIDRATOS ----------------------------
    {"nome": "Arroz branco cozido", "grupo": "carboidrato", "kcal_100g": 128,
     "proteina_100g": 2.5, "carboidrato_100g": 28.1, "gordura_100g": 0.2,
     "porcao_base_g": 100, "medida_caseira": "4 colheres de sopa",
     "restricoes_incompativeis": [], "tags": ["vegano"]},
    {"nome": "Arroz integral cozido", "grupo": "carboidrato", "kcal_100g": 124,
     "proteina_100g": 2.6, "carboidrato_100g": 25.8, "gordura_100g": 1.0,
     "porcao_base_g": 100, "medida_caseira": "4 colheres de sopa",
     "restricoes_incompativeis": [], "tags": ["vegano", "integral"]},
    {"nome": "Batata-doce cozida", "grupo": "carboidrato", "kcal_100g": 77,
     "proteina_100g": 0.6, "carboidrato_100g": 18.4, "gordura_100g": 0.1,
     "porcao_base_g": 150, "medida_caseira": "1 unidade média",
     "restricoes_incompativeis": [], "tags": ["vegano"]},
    {"nome": "Batata inglesa cozida", "grupo": "carboidrato", "kcal_100g": 52,
     "proteina_100g": 1.2, "carboidrato_100g": 11.9, "gordura_100g": 0.1,
     "porcao_base_g": 150, "medida_caseira": "1 unidade média",
     "restricoes_incompativeis": [], "tags": ["vegano"]},
    {"nome": "Mandioca cozida", "grupo": "carboidrato", "kcal_100g": 125,
     "proteina_100g": 0.6, "carboidrato_100g": 30.1, "gordura_100g": 0.3,
     "porcao_base_g": 100, "medida_caseira": "2 pedaços médios",
     "restricoes_incompativeis": [], "tags": ["vegano"]},
    {"nome": "Pão integral", "grupo": "carboidrato", "kcal_100g": 253,
     "proteina_100g": 9.4, "carboidrato_100g": 49.9, "gordura_100g": 3.3,
     "porcao_base_g": 50, "medida_caseira": "2 fatias",
     "restricoes_incompativeis": ["sem_gluten"], "tags": ["integral"]},
    {"nome": "Pão francês", "grupo": "carboidrato", "kcal_100g": 300,
     "proteina_100g": 8.0, "carboidrato_100g": 58.6, "gordura_100g": 3.1,
     "porcao_base_g": 50, "medida_caseira": "1 unidade",
     "restricoes_incompativeis": ["sem_gluten"], "tags": []},
    {"nome": "Aveia em flocos", "grupo": "carboidrato", "kcal_100g": 394,
     "proteina_100g": 13.9, "carboidrato_100g": 67.0, "gordura_100g": 8.5,
     "porcao_base_g": 30, "medida_caseira": "3 colheres de sopa",
     "restricoes_incompativeis": [], "tags": ["vegano", "integral"]},
    {"nome": "Tapioca (goma hidratada)", "grupo": "carboidrato", "kcal_100g": 240,
     "proteina_100g": 0.2, "carboidrato_100g": 59.0, "gordura_100g": 0.0,
     "porcao_base_g": 60, "medida_caseira": "1 unidade média",
     "restricoes_incompativeis": [], "tags": ["vegano"]},
    {"nome": "Macarrão integral cozido", "grupo": "carboidrato", "kcal_100g": 124,
     "proteina_100g": 5.3, "carboidrato_100g": 25.0, "gordura_100g": 0.9,
     "porcao_base_g": 100, "medida_caseira": "1 escumadeira",
     "restricoes_incompativeis": ["sem_gluten"], "tags": ["integral"]},
    {"nome": "Quinoa cozida", "grupo": "carboidrato", "kcal_100g": 120,
     "proteina_100g": 4.4, "carboidrato_100g": 21.3, "gordura_100g": 1.9,
     "porcao_base_g": 100, "medida_caseira": "4 colheres de sopa",
     "restricoes_incompativeis": [], "tags": ["vegano"]},
    {"nome": "Cuscuz de milho cozido", "grupo": "carboidrato", "kcal_100g": 112,
     "proteina_100g": 2.1, "carboidrato_100g": 25.3, "gordura_100g": 0.3,
     "porcao_base_g": 100, "medida_caseira": "1 fatia média",
     "restricoes_incompativeis": [], "tags": ["vegano"]},

    # ------------------------------ PROTEÍNAS ------------------------------
    {"nome": "Peito de frango grelhado", "grupo": "proteina", "kcal_100g": 159,
     "proteina_100g": 32.0, "carboidrato_100g": 0.0, "gordura_100g": 2.5,
     "porcao_base_g": 120, "medida_caseira": "1 filé médio",
     "restricoes_incompativeis": ["vegetariano", "vegano"], "tags": []},
    {"nome": "Patinho moído grelhado", "grupo": "proteina", "kcal_100g": 172,
     "proteina_100g": 28.0, "carboidrato_100g": 0.0, "gordura_100g": 6.0,
     "porcao_base_g": 120, "medida_caseira": "4 colheres de sopa",
     "restricoes_incompativeis": ["vegetariano", "vegano"], "tags": []},
    {"nome": "Tilápia grelhada", "grupo": "proteina", "kcal_100g": 128,
     "proteina_100g": 26.0, "carboidrato_100g": 0.0, "gordura_100g": 2.7,
     "porcao_base_g": 120, "medida_caseira": "1 filé médio",
     "restricoes_incompativeis": ["vegetariano", "vegano", "sem_frutos_do_mar"], "tags": []},
    {"nome": "Ovo cozido", "grupo": "proteina", "kcal_100g": 155,
     "proteina_100g": 13.0, "carboidrato_100g": 1.1, "gordura_100g": 10.6,
     "porcao_base_g": 100, "medida_caseira": "2 unidades",
     "restricoes_incompativeis": ["vegano", "sem_ovo"], "tags": ["vegetariano"]},
    {"nome": "Tofu grelhado", "grupo": "proteina", "kcal_100g": 145,
     "proteina_100g": 15.8, "carboidrato_100g": 2.3, "gordura_100g": 8.7,
     "porcao_base_g": 120, "medida_caseira": "4 fatias",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Grão-de-bico cozido", "grupo": "proteina", "kcal_100g": 164,
     "proteina_100g": 8.9, "carboidrato_100g": 27.4, "gordura_100g": 2.6,
     "porcao_base_g": 120, "medida_caseira": "4 colheres de sopa",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Lentilha cozida", "grupo": "proteina", "kcal_100g": 116,
     "proteina_100g": 9.0, "carboidrato_100g": 20.1, "gordura_100g": 0.4,
     "porcao_base_g": 120, "medida_caseira": "4 colheres de sopa",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Feijão-preto cozido", "grupo": "proteina", "kcal_100g": 77,
     "proteina_100g": 4.5, "carboidrato_100g": 14.0, "gordura_100g": 0.5,
     "porcao_base_g": 120, "medida_caseira": "1 concha média",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Whey protein (isolado)", "grupo": "proteina", "kcal_100g": 380,
     "proteina_100g": 80.0, "carboidrato_100g": 5.0, "gordura_100g": 3.0,
     "porcao_base_g": 30, "medida_caseira": "1 scoop",
     "restricoes_incompativeis": ["vegano", "sem_lactose"], "tags": ["vegetariano"]},
    {"nome": "Iogurte natural desnatado", "grupo": "proteina", "kcal_100g": 41,
     "proteina_100g": 4.0, "carboidrato_100g": 5.9, "gordura_100g": 0.2,
     "porcao_base_g": 170, "medida_caseira": "1 pote",
     "restricoes_incompativeis": ["vegano", "sem_lactose"], "tags": ["vegetariano"]},
    {"nome": "Queijo cottage", "grupo": "proteina", "kcal_100g": 98,
     "proteina_100g": 11.1, "carboidrato_100g": 3.4, "gordura_100g": 4.3,
     "porcao_base_g": 100, "medida_caseira": "4 colheres de sopa",
     "restricoes_incompativeis": ["vegano", "sem_lactose"], "tags": ["vegetariano"]},
    {"nome": "Atum em lata (água)", "grupo": "proteina", "kcal_100g": 116,
     "proteina_100g": 25.5, "carboidrato_100g": 0.0, "gordura_100g": 1.0,
     "porcao_base_g": 100, "medida_caseira": "1 lata pequena",
     "restricoes_incompativeis": ["vegetariano", "vegano", "sem_frutos_do_mar"], "tags": []},

    # ------------------------------ GORDURAS -------------------------------
    {"nome": "Azeite de oliva extravirgem", "grupo": "gordura", "kcal_100g": 884,
     "proteina_100g": 0.0, "carboidrato_100g": 0.0, "gordura_100g": 100.0,
     "porcao_base_g": 8, "medida_caseira": "1 colher de sopa",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Abacate", "grupo": "gordura", "kcal_100g": 96,
     "proteina_100g": 1.2, "carboidrato_100g": 6.0, "gordura_100g": 8.4,
     "porcao_base_g": 80, "medida_caseira": "3 colheres de sopa",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Castanha-do-pará", "grupo": "gordura", "kcal_100g": 656,
     "proteina_100g": 14.3, "carboidrato_100g": 12.3, "gordura_100g": 66.4,
     "porcao_base_g": 15, "medida_caseira": "2 unidades",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Amêndoas", "grupo": "gordura", "kcal_100g": 579,
     "proteina_100g": 21.2, "carboidrato_100g": 21.6, "gordura_100g": 49.9,
     "porcao_base_g": 15, "medida_caseira": "10 unidades",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Pasta de amendoim integral", "grupo": "gordura", "kcal_100g": 588,
     "proteina_100g": 25.1, "carboidrato_100g": 20.0, "gordura_100g": 50.0,
     "porcao_base_g": 15, "medida_caseira": "1 colher de sopa",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Semente de chia", "grupo": "gordura", "kcal_100g": 486,
     "proteina_100g": 16.5, "carboidrato_100g": 42.1, "gordura_100g": 30.7,
     "porcao_base_g": 12, "medida_caseira": "1 colher de sopa",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},

    # ------------------------------ VEGETAIS -------------------------------
    {"nome": "Brócolis cozido", "grupo": "vegetal", "kcal_100g": 25,
     "proteina_100g": 2.1, "carboidrato_100g": 4.0, "gordura_100g": 0.3,
     "porcao_base_g": 100, "medida_caseira": "4 colheres de sopa",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Cenoura crua ralada", "grupo": "vegetal", "kcal_100g": 41,
     "proteina_100g": 0.9, "carboidrato_100g": 9.6, "gordura_100g": 0.2,
     "porcao_base_g": 80, "medida_caseira": "3 colheres de sopa",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Alface", "grupo": "vegetal", "kcal_100g": 15,
     "proteina_100g": 1.4, "carboidrato_100g": 2.4, "gordura_100g": 0.2,
     "porcao_base_g": 60, "medida_caseira": "4 folhas",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Tomate", "grupo": "vegetal", "kcal_100g": 18,
     "proteina_100g": 0.9, "carboidrato_100g": 3.9, "gordura_100g": 0.2,
     "porcao_base_g": 90, "medida_caseira": "1 unidade média",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Abobrinha refogada", "grupo": "vegetal", "kcal_100g": 21,
     "proteina_100g": 1.3, "carboidrato_100g": 4.0, "gordura_100g": 0.3,
     "porcao_base_g": 100, "medida_caseira": "4 colheres de sopa",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Couve refogada", "grupo": "vegetal", "kcal_100g": 33,
     "proteina_100g": 2.9, "carboidrato_100g": 4.3, "gordura_100g": 0.7,
     "porcao_base_g": 80, "medida_caseira": "3 colheres de sopa",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Pepino", "grupo": "vegetal", "kcal_100g": 12,
     "proteina_100g": 0.7, "carboidrato_100g": 2.0, "gordura_100g": 0.1,
     "porcao_base_g": 90, "medida_caseira": "6 fatias",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariona"]},
    {"nome": "Beterraba cozida", "grupo": "vegetal", "kcal_100g": 32,
     "proteina_100g": 1.3, "carboidrato_100g": 7.0, "gordura_100g": 0.1,
     "porcao_base_g": 80, "medida_caseira": "3 fatias",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},

    # ------------------------------- FRUTAS --------------------------------
    {"nome": "Banana", "grupo": "fruta", "kcal_100g": 89,
     "proteina_100g": 1.1, "carboidrato_100g": 22.8, "gordura_100g": 0.3,
     "porcao_base_g": 100, "medida_caseira": "1 unidade média",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Maçã", "grupo": "fruta", "kcal_100g": 52,
     "proteina_100g": 0.3, "carboidrato_100g": 13.8, "gordura_100g": 0.2,
     "porcao_base_g": 130, "medida_caseira": "1 unidade média",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Mamão papaya", "grupo": "fruta", "kcal_100g": 43,
     "proteina_100g": 0.5, "carboidrato_100g": 10.8, "gordura_100g": 0.3,
     "porcao_base_g": 150, "medida_caseira": "1 fatia média",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Morango", "grupo": "fruta", "kcal_100g": 32,
     "proteina_100g": 0.7, "carboidrato_100g": 7.7, "gordura_100g": 0.3,
     "porcao_base_g": 120, "medida_caseira": "8 unidades médias",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Laranja", "grupo": "fruta", "kcal_100g": 47,
     "proteina_100g": 0.9, "carboidrato_100g": 11.8, "gordura_100g": 0.1,
     "porcao_base_g": 150, "medida_caseira": "1 unidade média",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Abacaxi", "grupo": "fruta", "kcal_100g": 50,
     "proteina_100g": 0.5, "carboidrato_100g": 13.1, "gordura_100g": 0.1,
     "porcao_base_g": 130, "medida_caseira": "2 fatias",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Uva", "grupo": "fruta", "kcal_100g": 69,
     "proteina_100g": 0.7, "carboidrato_100g": 18.1, "gordura_100g": 0.2,
     "porcao_base_g": 100, "medida_caseira": "1 cacho pequeno",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Kiwi", "grupo": "fruta", "kcal_100g": 61,
     "proteina_100g": 1.1, "carboidrato_100g": 14.7, "gordura_100g": 0.5,
     "porcao_base_g": 140, "medida_caseira": "2 unidades",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Melancia", "grupo": "fruta", "kcal_100g": 30,
     "proteina_100g": 0.6, "carboidrato_100g": 7.6, "gordura_100g": 0.2,
     "porcao_base_g": 200, "medida_caseira": "1 fatia grande",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "Pera", "grupo": "fruta", "kcal_100g": 57,
     "proteina_100g": 0.4, "carboidrato_100g": 15.2, "gordura_100g": 0.1,
     "porcao_base_g": 130, "medida_caseira": "1 unidade média",
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
]


def filtrar_alimentos(grupo: str, restricoes: list) -> list:
    """
    Retorna todos os alimentos de um determinado grupo que sejam
    compatíveis com a lista de restrições do paciente.
    """
    resultado = []
    for alimento in FOODS:
        if alimento["grupo"] != grupo:
            continue
        incompativel = any(r in alimento["restricoes_incompativeis"] for r in restricoes)
        if incompativel:
            continue
        resultado.append(alimento)
    return resultado