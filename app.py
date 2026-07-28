"""
app.py
Aplicação Streamlit única e exclusiva: formulário de dados do paciente
(incluindo recordatório alimentar habitual e observações clínicas
complementares) seguido do botão "Gerar Plano Alimentar", que aciona o
motor determinístico de geração do plano e permite exportar o resultado
em PDF no padrão visual de um documento clínico profissional.
"""

import streamlit as st

import config
from assets.styles import get_css
from engine.meal_plan_generator import gerar_plano_alimentar
from engine.pdf_generator import gerar_pdf
from utils.validators import validar_paciente

st.set_page_config(page_title=config.APP_TITLE, page_icon=config.APP_ICON, layout="wide")
st.markdown(get_css(), unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="app-header">
        <h1>{config.APP_ICON} {config.APP_TITLE}</h1>
        <p>Geração automática de planos alimentares baseada em evidências</p>
    </div>
    """,
    unsafe_allow_html=True,
)

RESTRICOES_LABELS = {
    "vegetariano": "Vegetariano",
    "vegano": "Vegano",
    "sem_lactose": "Sem lactose",
    "sem_gluten": "Sem glúten",
    "sem_ovo": "Sem ovo",
    "sem_frutos_do_mar": "Sem frutos do mar",
}

# ---------------------------------------------------------------------------
# DADOS DA NUTRICIONISTA (cabeçalho do PDF) — preenchidos uma vez, ficam
# disponíveis para qualquer paciente gerado nesta sessão.
# ---------------------------------------------------------------------------
with st.sidebar:
    st.subheader("🩺 Dados profissionais")
    st.caption("Usados apenas no cabeçalho do PDF exportado.")
    nutri_nome = st.text_input("Nome da nutricionista", value="")
    nutri_especialidade = st.text_input("Especialidade", value=config.NUTRICIONISTA_PADRAO["especialidade"])
    nutri_crn = st.text_input("CRN", value="")
    nutri_telefone = st.text_input("Telefone / WhatsApp", value="")
    nutri_email = st.text_input("E-mail", value="")
    nutri_local = st.text_input("Local de atendimento", value="")

nutricionista = {
    "nome": nutri_nome,
    "especialidade": nutri_especialidade,
    "crn": nutri_crn,
    "telefone": nutri_telefone,
    "email": nutri_email,
    "local_atendimento": nutri_local,
}

with st.form("form_paciente"):
    st.subheader("Dados do paciente")

    nome_paciente = st.text_input("Nome do paciente (exibido no PDF)", placeholder="ex.: Maria da Silva")

    col1, col2, col3 = st.columns(3)
    with col1:
        sexo_label = st.radio("Sexo biológico", ["Feminino", "Masculino"], horizontal=True)
        sexo = "feminino" if sexo_label == "Feminino" else "masculino"
        idade = st.number_input("Idade (anos)", min_value=10, max_value=100, value=30, step=1)
    with col2:
        peso = st.number_input("Peso (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.5)
        altura = st.number_input("Altura (cm)", min_value=100.0, max_value=250.0, value=170.0, step=1.0)
    with col3:
        objetivo_label = st.selectbox(
            "Objetivo do plano",
            ["Emagrecimento", "Manutenção do peso", "Hipertrofia / Ganho de massa"],
        )
        objetivo_map = {
            "Emagrecimento": "emagrecimento",
            "Manutenção do peso": "manutencao",
            "Hipertrofia / Ganho de massa": "hipertrofia",
        }
        objetivo = objetivo_map[objetivo_label]

    col4, col5 = st.columns(2)
    with col4:
        nivel_label = st.selectbox(
            "Nível de atividade física",
            [v["label"] for v in config.FATORES_ATIVIDADE.values()],
        )
        nivel_map = {v["label"]: k for k, v in config.FATORES_ATIVIDADE.items()}
        nivel_atividade = nivel_map[nivel_label]
    with col5:
        numero_refeicoes = st.selectbox("Número de refeições por dia", [3, 4, 5, 6], index=1)

    st.markdown("---")
    st.subheader("Restrições e preferências alimentares")

    col6, col7 = st.columns(2)
    with col6:
        restricoes_labels_sel = st.multiselect(
            "Restrições alimentares", list(RESTRICOES_LABELS.values())
        )
        restricoes = [k for k, v in RESTRICOES_LABELS.items() if v in restricoes_labels_sel]
    with col7:
        alimentos_evitados_raw = st.text_input(
            "Alimentos a evitar (separados por vírgula)", placeholder="ex.: fígado, berinjela"
        )

    alimentos_preferidos_raw = st.text_input(
        "Alimentos preferidos, se houver (separados por vírgula)",
        placeholder="ex.: frango, batata-doce, banana",
    )

    st.markdown("---")
    st.subheader("Recordatório alimentar habitual")
    st.caption(
        "Registre aqui o que o paciente já costuma comer nos últimos dias. "
        "Essa informação fica documentada no PDF como base do levantamento "
        "clínico que fundamentou a construção deste novo plano."
    )

    col8, col9 = st.columns(2)
    with col8:
        habito_cafe = st.text_area(
            "Café da manhã habitual", height=80,
            placeholder="ex.: pão com manteiga, café com leite integral",
        )
        habito_almoco = st.text_area(
            "Almoço habitual", height=80,
            placeholder="ex.: arroz, feijão, bife acebolado, salada de alface e tomate",
        )
    with col9:
        habito_lanche = st.text_area(
            "Lanches habituais", height=80,
            placeholder="ex.: bolacha recheada, salgados, refrigerante",
        )
        habito_jantar = st.text_area(
            "Jantar habitual", height=80,
            placeholder="ex.: sanduíche, macarrão instantâneo",
        )

    st.markdown("---")
    st.subheader("Observações clínicas complementares")
    observacoes_clinicas = st.text_area(
        "Comorbidades, medicações em uso, exames laboratoriais relevantes, "
        "rotina de sono, nível de estresse, prática de atividade física, etc.",
        height=100,
        placeholder="ex.: hipotireoidismo controlado, uso de levotiroxina, sono irregular (5h/noite)...",
    )

    submitted = st.form_submit_button("🌿 GERAR PLANO ALIMENTAR")

if submitted:
    paciente = {
        "sexo": sexo,
        "idade": int(idade),
        "peso": float(peso),
        "altura": float(altura),
        "objetivo": objetivo,
        "nivel_atividade": nivel_atividade,
        "numero_refeicoes": int(numero_refeicoes),
        "restricoes": restricoes,
        "alimentos_preferidos": [a for a in alimentos_preferidos_raw.split(",") if a.strip()],
        "alimentos_evitados": [a for a in alimentos_evitados_raw.split(",") if a.strip()],
    }

    erros = validar_paciente(paciente)

    if erros:
        for e in erros:
            st.error(e)
    else:
        plano = gerar_plano_alimentar(paciente)
        st.session_state["plano"] = plano
        st.session_state["nome_paciente"] = nome_paciente
        st.session_state["habitos_alimentares"] = {
            "Café da manhã habitual": habito_cafe,
            "Almoço habitual": habito_almoco,
            "Lanches habituais": habito_lanche,
            "Jantar habitual": habito_jantar,
        }
        st.session_state["observacoes_clinicas"] = observacoes_clinicas

if "plano" in st.session_state:
    plano = st.session_state["plano"]
    n = plano["necessidades"]

    st.markdown("---")
    st.subheader("Resumo nutricional calculado")

    st.markdown(
        f"""
        <div class="metric-row">
            <div class="metric-box"><div class="metric-value">{n.geb:.0f}</div><div class="metric-label">GEB (kcal)</div></div>
            <div class="metric-box"><div class="metric-value">{n.get:.0f}</div><div class="metric-label">GET (kcal)</div></div>
            <div class="metric-box"><div class="metric-value">{n.vet:.0f}</div><div class="metric-label">VET do plano (kcal)</div></div>
            <div class="metric-box"><div class="metric-value">{plano['imc']}</div><div class="metric-label">IMC ({plano['classificacao_imc']})</div></div>
        </div>
        <br>
        <div class="metric-row">
            <div class="metric-box"><div class="metric-value">{n.proteina_g:.0f} g</div><div class="metric-label">Proteína / dia</div></div>
            <div class="metric-box"><div class="metric-value">{n.carboidrato_g:.0f} g</div><div class="metric-label">Carboidrato / dia</div></div>
            <div class="metric-box"><div class="metric-value">{n.gordura_g:.0f} g</div><div class="metric-label">Gordura / dia</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    validacao = plano["validacao"]
    badge_class = "badge-success" if validacao["aprovado"] else "badge-warning"
    badge_text = "PLANO VALIDADO" if validacao["aprovado"] else "PLANO FORA DA TOLERÂNCIA"
    st.markdown(f'<br><span class="badge {badge_class}">{badge_text}</span>', unsafe_allow_html=True)
    for msg in validacao["mensagens"]:
        st.caption(f"⚠ {msg}")

    # ---- Botão de exportação em PDF --------------------------------------
    pdf_bytes = gerar_pdf(
        plano=plano,
        nutricionista=nutricionista,
        paciente_nome=st.session_state.get("nome_paciente", ""),
        habitos_alimentares=st.session_state.get("habitos_alimentares"),
        observacoes_clinicas=st.session_state.get("observacoes_clinicas"),
    )
    st.download_button(
        "📄 Baixar plano alimentar em PDF",
        data=pdf_bytes,
        file_name="plano_alimentar.pdf",
        mime="application/pdf",
    )

    st.markdown("---")
    st.subheader("Plano alimentar do dia")

    for refeicao in plano["refeicoes"]:
        secoes_html = ""
        for secao in refeicao["secoes"]:
            titulo_html = f'<div class="secao-titulo">{secao["titulo"]}</div>' if secao["titulo"] else ""
            itens_html = "".join(
                f'<div class="food-item"><div class="food-name">{item["descricao"]}</div>'
                f'<div class="food-detail">{item["kcal"]:.0f} kcal · P {item["proteina"]:.1f} g '
                f'· C {item["carboidrato"]:.1f} g · G {item["gordura"]:.1f} g</div></div>'
                for item in secao["itens"]
            )
            secoes_html += titulo_html + itens_html

        st.markdown(
            f"""
            <div class="card">
                <div class="card-meal-title">{refeicao['horario']} · {refeicao['nome']}</div>
                <div class="food-detail">Meta: {refeicao['kcal_alvo']:.0f} kcal · Total real: {refeicao['totais']['kcal']:.0f} kcal</div>
                {secoes_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.subheader("Recomendações")
    rec = plano["recomendacoes"]
    st.markdown(
        f"""
        <div class="card">
            <div class="card-meal-title">Ingestão de água entre as refeições</div>
            <div class="food-detail">Entre {rec['agua_min_l']:.1f} e {rec['agua_max_l']:.1f} litros por dia</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    for tip in rec["outras"]:
        st.markdown(f"- {tip}")

    st.markdown("---")
    st.caption(
        "Metodologia: Gasto energético basal por Mifflin-St Jeor (1990); fator de "
        "atividade FAO/OMS/UNU (2001); ajuste calórico e proteína por objetivo segundo "
        "ISSN Position Stand (Aragon et al., 2017); lipídios conforme DRI/IOM (2005); "
        "ingestão hídrica de referência de 30-35 mL/kg/dia."
    )