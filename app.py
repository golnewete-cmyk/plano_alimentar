"""
app.py
Aplicação Streamlit única e exclusiva: formulário de dados do paciente
seguido do botão "Gerar Plano Alimentar", que aciona o motor determinístico
de geração automática do plano.
"""

import streamlit as st

import config
from assets.styles import get_css
from engine.meal_plan_generator import gerar_plano_alimentar
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

with st.form("form_paciente"):
    st.subheader("Dados do paciente")

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

    st.markdown("---")
    st.subheader("Plano alimentar do dia")

    for refeicao in plano["refeicoes"]:
        itens_html = ""
        for item in refeicao["itens"]:
            subs = item["substituicoes"]
            subs_html = ""
            if subs:
                partes = [f"{s['nome']} ({s['gramas']:.0f} g)" for s in subs]
                subs_html = f'<div class="food-sub">Substituições equivalentes: {" | ".join(partes)}</div>'

            itens_html += f"""
            <div class="food-item">
                <div class="food-name">{item['nome']} — {item['gramas']:.0f} g <span class="food-detail">({item['medida_caseira']})</span></div>
                <div class="food-detail">{item['kcal']:.0f} kcal · P {item['proteina']:.1f} g · C {item['carboidrato']:.1f} g · G {item['gordura']:.1f} g</div>
                {subs_html}
            </div>
            """

        st.markdown(
            f"""
            <div class="card">
                <div class="card-meal-title">{refeicao['nome']}</div>
                <div class="food-detail">Meta: {refeicao['kcal_alvo']:.0f} kcal · Total real: {refeicao['totais']['kcal']:.0f} kcal</div>
                {itens_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.caption(
        "Metodologia: Gasto energético basal por Mifflin-St Jeor (1990); fator de "
        "atividade FAO/OMS/UNU (2001); ajuste calórico e proteína por objetivo segundo "
        "ISSN Position Stand (Aragon et al., 2017); lipídios conforme DRI/IOM (2005)."
    )