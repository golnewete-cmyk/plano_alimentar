"""
database/foods_data.py

Banco de alimentos estruturado por grupo alimentar.

Cada alimento contém:
- nome
- grupo: carboidrato | proteina | gordura | vegetal | fruta | bebida
- kcal_100g, proteina_100g, carboidrato_100g, gordura_100g (composição por
  100 g/100 ml, valores de referência da Tabela Brasileira de Composição
  de Alimentos - TACO/UNICAMP e USDA FoodData Central)
- porcao_base_g: porção usual de referência, em gramas ou mililitros
- unidade_medida: "g" ou "ml" (usado apenas na exibição da porção)
- unidade_nome / unidade_nome_plural: nome da medida caseira de UMA
  unidade (ex.: "fatia" / "fatias", "colher de sopa" / "colheres de sopa"),
  usada para expressar a porção calculada de forma prática, no padrão
  "1,5 fatia (75 g)" em vez de apenas gramas.
- unidade_peso_g: peso (g ou ml) correspondente a 1 unidade da medida
  caseira acima. A quantidade de unidades exibida = porção_calculada /
  unidade_peso_g.
- restricoes_incompativeis: lista de restrições que EXCLUEM este alimento
- tags: marcadores adicionais (ex.: "vegano", "integral")

O banco foi projetado para ser facilmente expansível: basta adicionar
novos dicionários às listas abaixo, sempre preenchendo os campos de unidade.
"""

FOODS = [
    # ---------------------------- CARBOIDRATOS ----------------------------
    {"nome": "arroz branco cozido", "grupo": "carboidrato", "kcal_100g": 128,
     "proteina_100g": 2.5, "carboidrato_100g": 28.1, "gordura_100g": 0.2,
     "porcao_base_g": 100, "unidade_medida": "g",
     "unidade_nome": "colher de servir", "unidade_nome_plural": "colheres de servir", "unidade_peso_g": 50,
     "restricoes_incompativeis": [], "tags": ["vegano"]},
    {"nome": "arroz integral cozido", "grupo": "carboidrato", "kcal_100g": 124,
     "proteina_100g": 2.6, "carboidrato_100g": 25.8, "gordura_100g": 1.0,
     "porcao_base_g": 100, "unidade_medida": "g",
     "unidade_nome": "colher de servir", "unidade_nome_plural": "colheres de servir", "unidade_peso_g": 50,
     "restricoes_incompativeis": [], "tags": ["vegano", "integral"]},
    {"nome": "batata-doce cozida", "grupo": "carboidrato", "kcal_100g": 77,
     "proteina_100g": 0.6, "carboidrato_100g": 18.4, "gordura_100g": 0.1,
     "porcao_base_g": 150, "unidade_medida": "g",
     "unidade_nome": "unidade média", "unidade_nome_plural": "unidades médias", "unidade_peso_g": 150,
     "restricoes_incompativeis": [], "tags": ["vegano"]},
    {"nome": "batata inglesa cozida", "grupo": "carboidrato", "kcal_100g": 52,
     "proteina_100g": 1.2, "carboidrato_100g": 11.9, "gordura_100g": 0.1,
     "porcao_base_g": 150, "unidade_medida": "g",
     "unidade_nome": "unidade média", "unidade_nome_plural": "unidades médias", "unidade_peso_g": 150,
     "restricoes_incompativeis": [], "tags": ["vegano"]},
    {"nome": "mandioca cozida", "grupo": "carboidrato", "kcal_100g": 125,
     "proteina_100g": 0.6, "carboidrato_100g": 30.1, "gordura_100g": 0.3,
     "porcao_base_g": 100, "unidade_medida": "g",
     "unidade_nome": "pedaço médio", "unidade_nome_plural": "pedaços médios", "unidade_peso_g": 50,
     "restricoes_incompativeis": [], "tags": ["vegano"]},
    {"nome": "pão integral", "grupo": "carboidrato", "kcal_100g": 253,
     "proteina_100g": 9.4, "carboidrato_100g": 49.9, "gordura_100g": 3.3,
     "porcao_base_g": 50, "unidade_medida": "g",
     "unidade_nome": "fatia", "unidade_nome_plural": "fatias", "unidade_peso_g": 25,
     "restricoes_incompativeis": ["sem_gluten"], "tags": ["integral"]},
    {"nome": "pão francês", "grupo": "carboidrato", "kcal_100g": 300,
     "proteina_100g": 8.0, "carboidrato_100g": 58.6, "gordura_100g": 3.1,
     "porcao_base_g": 50, "unidade_medida": "g",
     "unidade_nome": "unidade", "unidade_nome_plural": "unidades", "unidade_peso_g": 50,
     "restricoes_incompativeis": ["sem_gluten"], "tags": []},
    {"nome": "aveia em flocos", "grupo": "carboidrato", "kcal_100g": 394,
     "proteina_100g": 13.9, "carboidrato_100g": 67.0, "gordura_100g": 8.5,
     "porcao_base_g": 30, "unidade_medida": "g",
     "unidade_nome": "colher de sopa", "unidade_nome_plural": "colheres de sopa", "unidade_peso_g": 10,
     "restricoes_incompativeis": [], "tags": ["vegano", "integral"]},
    {"nome": "tapioca (goma hidratada)", "grupo": "carboidrato", "kcal_100g": 240,
     "proteina_100g": 0.2, "carboidrato_100g": 59.0, "gordura_100g": 0.0,
     "porcao_base_g": 60, "unidade_medida": "g",
     "unidade_nome": "unidade média", "unidade_nome_plural": "unidades médias", "unidade_peso_g": 60,
     "restricoes_incompativeis": [], "tags": ["vegano"]},
    {"nome": "macarrão integral cozido", "grupo": "carboidrato", "kcal_100g": 124,
     "proteina_100g": 5.3, "carboidrato_100g": 25.0, "gordura_100g": 0.9,
     "porcao_base_g": 100, "unidade_medida": "g",
     "unidade_nome": "escumadeira", "unidade_nome_plural": "escumadeiras", "unidade_peso_g": 100,
     "restricoes_incompativeis": ["sem_gluten"], "tags": ["integral"]},
    {"nome": "quinoa cozida", "grupo": "carboidrato", "kcal_100g": 120,
     "proteina_100g": 4.4, "carboidrato_100g": 21.3, "gordura_100g": 1.9,
     "porcao_base_g": 100, "unidade_medida": "g",
     "unidade_nome": "colher de sopa", "unidade_nome_plural": "colheres de sopa", "unidade_peso_g": 25,
     "restricoes_incompativeis": [], "tags": ["vegano"]},
    {"nome": "cuscuz de milho cozido", "grupo": "carboidrato", "kcal_100g": 112,
     "proteina_100g": 2.1, "carboidrato_100g": 25.3, "gordura_100g": 0.3,
     "porcao_base_g": 100, "unidade_medida": "g",
     "unidade_nome": "fatia média", "unidade_nome_plural": "fatias médias", "unidade_peso_g": 100,
     "restricoes_incompativeis": [], "tags": ["vegano"]},

    # ------------------------------ PROTEÍNAS ------------------------------
    {"nome": "peito de frango grelhado", "grupo": "proteina", "kcal_100g": 159,
     "proteina_100g": 32.0, "carboidrato_100g": 0.0, "gordura_100g": 2.5,
     "porcao_base_g": 120, "unidade_medida": "g",
     "unidade_nome": "filé médio", "unidade_nome_plural": "filés médios", "unidade_peso_g": 100,
     "restricoes_incompativeis": ["vegetariano", "vegano"], "tags": []},
    {"nome": "patinho moído grelhado", "grupo": "proteina", "kcal_100g": 172,
     "proteina_100g": 28.0, "carboidrato_100g": 0.0, "gordura_100g": 6.0,
     "porcao_base_g": 120, "unidade_medida": "g",
     "unidade_nome": "colher de sopa cheia", "unidade_nome_plural": "colheres de sopa cheias", "unidade_peso_g": 30,
     "restricoes_incompativeis": ["vegetariano", "vegano"], "tags": []},
    {"nome": "tilápia grelhada", "grupo": "proteina", "kcal_100g": 128,
     "proteina_100g": 26.0, "carboidrato_100g": 0.0, "gordura_100g": 2.7,
     "porcao_base_g": 120, "unidade_medida": "g",
     "unidade_nome": "filé médio", "unidade_nome_plural": "filés médios", "unidade_peso_g": 100,
     "restricoes_incompativeis": ["vegetariano", "vegano", "sem_frutos_do_mar"], "tags": []},
    {"nome": "ovo cozido", "grupo": "proteina", "kcal_100g": 155,
     "proteina_100g": 13.0, "carboidrato_100g": 1.1, "gordura_100g": 10.6,
     "porcao_base_g": 100, "unidade_medida": "g",
     "unidade_nome": "unidade", "unidade_nome_plural": "unidades", "unidade_peso_g": 50,
     "restricoes_incompativeis": ["vegano", "sem_ovo"], "tags": ["vegetariano"]},
    {"nome": "tofu grelhado", "grupo": "proteina", "kcal_100g": 145,
     "proteina_100g": 15.8, "carboidrato_100g": 2.3, "gordura_100g": 8.7,
     "porcao_base_g": 120, "unidade_medida": "g",
     "unidade_nome": "fatia", "unidade_nome_plural": "fatias", "unidade_peso_g": 30,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "grão-de-bico cozido", "grupo": "proteina", "kcal_100g": 164,
     "proteina_100g": 8.9, "carboidrato_100g": 27.4, "gordura_100g": 2.6,
     "porcao_base_g": 120, "unidade_medida": "g",
     "unidade_nome": "colher de sopa", "unidade_nome_plural": "colheres de sopa", "unidade_peso_g": 30,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "lentilha cozida", "grupo": "proteina", "kcal_100g": 116,
     "proteina_100g": 9.0, "carboidrato_100g": 20.1, "gordura_100g": 0.4,
     "porcao_base_g": 120, "unidade_medida": "g",
     "unidade_nome": "colher de sopa", "unidade_nome_plural": "colheres de sopa", "unidade_peso_g": 30,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "feijão-preto cozido", "grupo": "proteina", "kcal_100g": 77,
     "proteina_100g": 4.5, "carboidrato_100g": 14.0, "gordura_100g": 0.5,
     "porcao_base_g": 120, "unidade_medida": "g",
     "unidade_nome": "concha média", "unidade_nome_plural": "conchas médias", "unidade_peso_g": 60,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "whey protein (isolado)", "grupo": "proteina", "kcal_100g": 380,
     "proteina_100g": 80.0, "carboidrato_100g": 5.0, "gordura_100g": 3.0,
     "porcao_base_g": 30, "unidade_medida": "g",
     "unidade_nome": "scoop", "unidade_nome_plural": "scoops", "unidade_peso_g": 30,
     "restricoes_incompativeis": ["vegano", "sem_lactose"], "tags": ["vegetariano"]},
    {"nome": "iogurte natural desnatado", "grupo": "proteina", "kcal_100g": 41,
     "proteina_100g": 4.0, "carboidrato_100g": 5.9, "gordura_100g": 0.2,
     "porcao_base_g": 170, "unidade_medida": "g",
     "unidade_nome": "pote", "unidade_nome_plural": "potes", "unidade_peso_g": 170,
     "restricoes_incompativeis": ["vegano", "sem_lactose"], "tags": ["vegetariano"]},
    {"nome": "queijo cottage", "grupo": "proteina", "kcal_100g": 98,
     "proteina_100g": 11.1, "carboidrato_100g": 3.4, "gordura_100g": 4.3,
     "porcao_base_g": 100, "unidade_medida": "g",
     "unidade_nome": "colher de sopa", "unidade_nome_plural": "colheres de sopa", "unidade_peso_g": 25,
     "restricoes_incompativeis": ["vegano", "sem_lactose"], "tags": ["vegetariano"]},
    {"nome": "atum em lata (água)", "grupo": "proteina", "kcal_100g": 116,
     "proteina_100g": 25.5, "carboidrato_100g": 0.0, "gordura_100g": 1.0,
     "porcao_base_g": 100, "unidade_medida": "g",
     "unidade_nome": "lata pequena", "unidade_nome_plural": "latas pequenas", "unidade_peso_g": 100,
     "restricoes_incompativeis": ["vegetariano", "vegano", "sem_frutos_do_mar"], "tags": []},

    # ------------------------------ GORDURAS -------------------------------
    {"nome": "azeite de oliva extravirgem", "grupo": "gordura", "kcal_100g": 884,
     "proteina_100g": 0.0, "carboidrato_100g": 0.0, "gordura_100g": 100.0,
     "porcao_base_g": 8, "unidade_medida": "ml",
     "unidade_nome": "colher de sopa", "unidade_nome_plural": "colheres de sopa", "unidade_peso_g": 8,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "abacate", "grupo": "gordura", "kcal_100g": 96,
     "proteina_100g": 1.2, "carboidrato_100g": 6.0, "gordura_100g": 8.4,
     "porcao_base_g": 80, "unidade_medida": "g",
     "unidade_nome": "colher de sopa", "unidade_nome_plural": "colheres de sopa", "unidade_peso_g": 27,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "castanha-do-pará", "grupo": "gordura", "kcal_100g": 656,
     "proteina_100g": 14.3, "carboidrato_100g": 12.3, "gordura_100g": 66.4,
     "porcao_base_g": 15, "unidade_medida": "g",
     "unidade_nome": "unidade", "unidade_nome_plural": "unidades", "unidade_peso_g": 7.5,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "amêndoas", "grupo": "gordura", "kcal_100g": 579,
     "proteina_100g": 21.2, "carboidrato_100g": 21.6, "gordura_100g": 49.9,
     "porcao_base_g": 15, "unidade_medida": "g",
     "unidade_nome": "unidade", "unidade_nome_plural": "unidades", "unidade_peso_g": 1.5,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "pasta de amendoim integral", "grupo": "gordura", "kcal_100g": 588,
     "proteina_100g": 25.1, "carboidrato_100g": 20.0, "gordura_100g": 50.0,
     "porcao_base_g": 15, "unidade_medida": "g",
     "unidade_nome": "colher de sopa", "unidade_nome_plural": "colheres de sopa", "unidade_peso_g": 15,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "semente de chia", "grupo": "gordura", "kcal_100g": 486,
     "proteina_100g": 16.5, "carboidrato_100g": 42.1, "gordura_100g": 30.7,
     "porcao_base_g": 12, "unidade_medida": "g",
     "unidade_nome": "colher de sopa", "unidade_nome_plural": "colheres de sopa", "unidade_peso_g": 12,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},

    # ------------------------------ VEGETAIS -------------------------------
    {"nome": "brócolis cozido", "grupo": "vegetal", "kcal_100g": 25,
     "proteina_100g": 2.1, "carboidrato_100g": 4.0, "gordura_100g": 0.3,
     "porcao_base_g": 100, "unidade_medida": "g",
     "unidade_nome": "colher de sopa", "unidade_nome_plural": "colheres de sopa", "unidade_peso_g": 25,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "cenoura crua ralada", "grupo": "vegetal", "kcal_100g": 41,
     "proteina_100g": 0.9, "carboidrato_100g": 9.6, "gordura_100g": 0.2,
     "porcao_base_g": 80, "unidade_medida": "g",
     "unidade_nome": "colher de sopa", "unidade_nome_plural": "colheres de sopa", "unidade_peso_g": 27,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "alface", "grupo": "vegetal", "kcal_100g": 15,
     "proteina_100g": 1.4, "carboidrato_100g": 2.4, "gordura_100g": 0.2,
     "porcao_base_g": 60, "unidade_medida": "g",
     "unidade_nome": "folha", "unidade_nome_plural": "folhas", "unidade_peso_g": 15,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "tomate", "grupo": "vegetal", "kcal_100g": 18,
     "proteina_100g": 0.9, "carboidrato_100g": 3.9, "gordura_100g": 0.2,
     "porcao_base_g": 90, "unidade_medida": "g",
     "unidade_nome": "unidade média", "unidade_nome_plural": "unidades médias", "unidade_peso_g": 90,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "abobrinha refogada", "grupo": "vegetal", "kcal_100g": 21,
     "proteina_100g": 1.3, "carboidrato_100g": 4.0, "gordura_100g": 0.3,
     "porcao_base_g": 100, "unidade_medida": "g",
     "unidade_nome": "colher de sopa", "unidade_nome_plural": "colheres de sopa", "unidade_peso_g": 25,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "couve refogada", "grupo": "vegetal", "kcal_100g": 33,
     "proteina_100g": 2.9, "carboidrato_100g": 4.3, "gordura_100g": 0.7,
     "porcao_base_g": 80, "unidade_medida": "g",
     "unidade_nome": "colher de sopa", "unidade_nome_plural": "colheres de sopa", "unidade_peso_g": 27,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "pepino em fatias", "grupo": "vegetal", "kcal_100g": 12,
     "proteina_100g": 0.7, "carboidrato_100g": 2.0, "gordura_100g": 0.1,
     "porcao_base_g": 90, "unidade_medida": "g",
     "unidade_nome": "fatia", "unidade_nome_plural": "fatias", "unidade_peso_g": 15,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "beterraba cozida", "grupo": "vegetal", "kcal_100g": 32,
     "proteina_100g": 1.3, "carboidrato_100g": 7.0, "gordura_100g": 0.1,
     "porcao_base_g": 80, "unidade_medida": "g",
     "unidade_nome": "fatia", "unidade_nome_plural": "fatias", "unidade_peso_g": 27,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},

    # ------------------------------- FRUTAS --------------------------------
    {"nome": "banana", "grupo": "fruta", "kcal_100g": 89,
     "proteina_100g": 1.1, "carboidrato_100g": 22.8, "gordura_100g": 0.3,
     "porcao_base_g": 100, "unidade_medida": "g",
     "unidade_nome": "unidade média", "unidade_nome_plural": "unidades médias", "unidade_peso_g": 100,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "maçã", "grupo": "fruta", "kcal_100g": 52,
     "proteina_100g": 0.3, "carboidrato_100g": 13.8, "gordura_100g": 0.2,
     "porcao_base_g": 130, "unidade_medida": "g",
     "unidade_nome": "unidade média", "unidade_nome_plural": "unidades médias", "unidade_peso_g": 130,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "mamão papaya", "grupo": "fruta", "kcal_100g": 43,
     "proteina_100g": 0.5, "carboidrato_100g": 10.8, "gordura_100g": 0.3,
     "porcao_base_g": 150, "unidade_medida": "g",
     "unidade_nome": "fatia média", "unidade_nome_plural": "fatias médias", "unidade_peso_g": 150,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "morango", "grupo": "fruta", "kcal_100g": 32,
     "proteina_100g": 0.7, "carboidrato_100g": 7.7, "gordura_100g": 0.3,
     "porcao_base_g": 120, "unidade_medida": "g",
     "unidade_nome": "unidade média", "unidade_nome_plural": "unidades médias", "unidade_peso_g": 15,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "laranja", "grupo": "fruta", "kcal_100g": 47,
     "proteina_100g": 0.9, "carboidrato_100g": 11.8, "gordura_100g": 0.1,
     "porcao_base_g": 150, "unidade_medida": "g",
     "unidade_nome": "unidade média", "unidade_nome_plural": "unidades médias", "unidade_peso_g": 150,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "abacaxi em fatias", "grupo": "fruta", "kcal_100g": 50,
     "proteina_100g": 0.5, "carboidrato_100g": 13.1, "gordura_100g": 0.1,
     "porcao_base_g": 130, "unidade_medida": "g",
     "unidade_nome": "fatia", "unidade_nome_plural": "fatias", "unidade_peso_g": 65,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "uva", "grupo": "fruta", "kcal_100g": 69,
     "proteina_100g": 0.7, "carboidrato_100g": 18.1, "gordura_100g": 0.2,
     "porcao_base_g": 100, "unidade_medida": "g",
     "unidade_nome": "cacho pequeno", "unidade_nome_plural": "cachos pequenos", "unidade_peso_g": 100,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "kiwi", "grupo": "fruta", "kcal_100g": 61,
     "proteina_100g": 1.1, "carboidrato_100g": 14.7, "gordura_100g": 0.5,
     "porcao_base_g": 140, "unidade_medida": "g",
     "unidade_nome": "unidade", "unidade_nome_plural": "unidades", "unidade_peso_g": 70,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "melancia em fatia", "grupo": "fruta", "kcal_100g": 30,
     "proteina_100g": 0.6, "carboidrato_100g": 7.6, "gordura_100g": 0.2,
     "porcao_base_g": 200, "unidade_medida": "g",
     "unidade_nome": "fatia grande", "unidade_nome_plural": "fatias grandes", "unidade_peso_g": 200,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "pera", "grupo": "fruta", "kcal_100g": 57,
     "proteina_100g": 0.4, "carboidrato_100g": 15.2, "gordura_100g": 0.1,
     "porcao_base_g": 130, "unidade_medida": "g",
     "unidade_nome": "unidade média", "unidade_nome_plural": "unidades médias", "unidade_peso_g": 130,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},

    # ------------------------------- BEBIDAS -------------------------------
    # Acompanham Almoço/Jantar em porção fixa de referência (papel de
    # hidratação/acompanhamento, não de macronutriente principal).
    {"nome": "suco de uva integral", "grupo": "bebida", "kcal_100g": 60,
     "proteina_100g": 0.1, "carboidrato_100g": 15.0, "gordura_100g": 0.0,
     "porcao_base_g": 200, "unidade_medida": "ml",
     "unidade_nome": "copo", "unidade_nome_plural": "copos", "unidade_peso_g": 200,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "suco de laranja natural", "grupo": "bebida", "kcal_100g": 37,
     "proteina_100g": 0.5, "carboidrato_100g": 8.9, "gordura_100g": 0.1,
     "porcao_base_g": 200, "unidade_medida": "ml",
     "unidade_nome": "copo", "unidade_nome_plural": "copos", "unidade_peso_g": 200,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "água de coco", "grupo": "bebida", "kcal_100g": 22,
     "proteina_100g": 0.1, "carboidrato_100g": 5.3, "gordura_100g": 0.1,
     "porcao_base_g": 200, "unidade_medida": "ml",
     "unidade_nome": "copo", "unidade_nome_plural": "copos", "unidade_peso_g": 200,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
    {"nome": "suco de abacaxi natural", "grupo": "bebida", "kcal_100g": 46,
     "proteina_100g": 0.3, "carboidrato_100g": 11.3, "gordura_100g": 0.1,
     "porcao_base_g": 200, "unidade_medida": "ml",
     "unidade_nome": "copo", "unidade_nome_plural": "copos", "unidade_peso_g": 200,
     "restricoes_incompativeis": [], "tags": ["vegano", "vegetariano"]},
]

# ---------------------------------------------------------------------------
# CONTEXTO DE USO: em quais tipos de refeição cada alimento é
# tradicionalmente adequado. Evita, por exemplo, que aveia em flocos ou
# castanhas (tipicamente de café da manhã/lanche) sejam escaladas a
# porções grandes para compor o prato principal do almoço/jantar, que
# arroz/batata sejam usados como "lanche", que leguminosas (feijão,
# lentilha, grão-de-bico) apareçam em lanches, ou que laticínios/whey
# (tipicamente de café da manhã/lanche) apareçam como prato principal do
# almoço/jantar.
_CARBOIDRATOS_SO_LANCHE = {"pão integral", "pão francês", "aveia em flocos", "tapioca (goma hidratada)"}
_CARBOIDRATOS_AMBOS = {"batata-doce cozida", "quinoa cozida", "cuscuz de milho cozido"}
_GORDURAS_SO_LANCHE = {"castanha-do-pará", "amêndoas", "pasta de amendoim integral", "semente de chia"}
_GORDURAS_AMBOS = {"azeite de oliva extravirgem", "abacate"}
_PROTEINAS_SO_REFEICAO_PRINCIPAL = {"grão-de-bico cozido", "lentilha cozida", "feijão-preto cozido"}
_PROTEINAS_SO_LANCHE = {"iogurte natural desnatado", "queijo cottage", "whey protein (isolado)"}

for _alimento in FOODS:
    if _alimento["grupo"] == "proteina":
        if _alimento["nome"] in _PROTEINAS_SO_REFEICAO_PRINCIPAL:
            _alimento["contextos"] = ["refeicao_principal"]
        elif _alimento["nome"] in _PROTEINAS_SO_LANCHE:
            _alimento["contextos"] = ["lanche"]
        else:
            _alimento["contextos"] = ["refeicao_principal", "lanche"]
    elif _alimento["grupo"] in ("vegetal", "fruta", "bebida"):
        _alimento["contextos"] = ["refeicao_principal", "lanche"]
    elif _alimento["nome"] in _CARBOIDRATOS_SO_LANCHE:
        _alimento["contextos"] = ["lanche"]
    elif _alimento["nome"] in _CARBOIDRATOS_AMBOS or _alimento["nome"] in _GORDURAS_AMBOS:
        _alimento["contextos"] = ["refeicao_principal", "lanche"]
    elif _alimento["nome"] in _GORDURAS_SO_LANCHE:
        _alimento["contextos"] = ["lanche"]
    else:
        # demais carboidratos (arroz, batata inglesa, mandioca, macarrão) e
        # a gordura não listada acima -> refeição principal
        _alimento["contextos"] = ["refeicao_principal"]


def filtrar_alimentos(grupo: str, restricoes: list, contexto: str = None) -> list:
    """
    Retorna todos os alimentos de um determinado grupo que sejam
    compatíveis com a lista de restrições do paciente e, se informado,
    com o contexto da refeição ("refeicao_principal" ou "lanche").
    """
    resultado = []
    for alimento in FOODS:
        if alimento["grupo"] != grupo:
            continue
        incompativel = any(r in alimento["restricoes_incompativeis"] for r in restricoes)
        if incompativel:
            continue
        if contexto and contexto not in alimento.get("contextos", []):
            continue
        resultado.append(alimento)
    return resultado