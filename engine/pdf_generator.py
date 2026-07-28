"""
engine/pdf_generator.py

Geração do PDF do plano alimentar, seguindo o padrão visual e o nível de
detalhamento de documentos clínicos profissionais de referência:
- Cabeçalho com identificação da nutricionista/clínica (dados preenchidos
  pela própria profissional no formulário — nenhuma marca de terceiros é
  reproduzida) e informações de contato.
- Bloco "INFORMAÇÕES DO CLIENTE".
- Bloco "REFEIÇÕES", organizado por horário, com subseções ENTRADA/PRATO/
  BEBIDA quando aplicável, alimentos com quantidade em medida caseira e
  gramas/ml, e opções equivalentes unidas por "ou".
- Bloco "RECOMENDAÇÕES" (ingestão de água + orientações gerais).

Usa reportlab (platypus) para montar o documento em memória e retorna os
bytes do PDF, prontos para download via Streamlit.
"""

import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
)

# ---------------------------------------------------------------------------
# PALETA DE IMPRESSÃO (documento claro/profissional — distinta do dark mode
# do aplicativo, adequada para impressão e leitura pelo paciente)
# ---------------------------------------------------------------------------
VERDE_PRINCIPAL = colors.HexColor("#1B6E52")
VERDE_ESCURO = colors.HexColor("#0F3D2E")
VERDE_CLARO_BG = colors.HexColor("#EAF5F0")
CINZA_TEXTO = colors.HexColor("#4B5563")
CINZA_CLARO = colors.HexColor("#9CA3AF")
PRETO_TEXTO = colors.HexColor("#1F2937")
BORDA = colors.HexColor("#D9E4DE")

OBJETIVO_LABEL = {
    "emagrecimento": "Emagrecimento",
    "manutencao": "Manutenção do peso",
    "hipertrofia": "Hipertrofia / Ganho de massa",
}


def _estilos():
    base = getSampleStyleSheet()
    estilos = {
        "titulo_app": ParagraphStyle(
            "titulo_app", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=17, textColor=VERDE_ESCURO, leading=20,
        ),
        "contato": ParagraphStyle(
            "contato", parent=base["Normal"], fontName="Helvetica",
            fontSize=8.5, textColor=CINZA_TEXTO, leading=12, alignment=2,
        ),
        "secao_titulo": ParagraphStyle(
            "secao_titulo", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=11.5, textColor=VERDE_PRINCIPAL, leading=16,
            spaceBefore=14, spaceAfter=6, letterSpacing=0.5,
        ),
        "subsecao_titulo": ParagraphStyle(
            "subsecao_titulo", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=9.5, textColor=PRETO_TEXTO, leading=13, spaceBefore=6, spaceAfter=2,
        ),
        "refeicao_titulo": ParagraphStyle(
            "refeicao_titulo", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=10.5, textColor=PRETO_TEXTO, leading=14, spaceBefore=10, spaceAfter=3,
        ),
        "item": ParagraphStyle(
            "item", parent=base["Normal"], fontName="Helvetica",
            fontSize=9.3, textColor=PRETO_TEXTO, leading=13.5, leftIndent=10,
        ),
        "corpo": ParagraphStyle(
            "corpo", parent=base["Normal"], fontName="Helvetica",
            fontSize=9.3, textColor=PRETO_TEXTO, leading=13.5,
        ),
        "corpo_cinza": ParagraphStyle(
            "corpo_cinza", parent=base["Normal"], fontName="Helvetica",
            fontSize=8.7, textColor=CINZA_TEXTO, leading=12.5,
        ),
        "rodape": ParagraphStyle(
            "rodape", parent=base["Normal"], fontName="Helvetica-Oblique",
            fontSize=7.7, textColor=CINZA_CLARO, leading=11,
        ),
    }
    return estilos


def _barra_secao(texto: str, estilo) -> Table:
    """Barra colorida de título de seção, no mesmo espírito visual do
    documento de referência (faixa verde clara com texto verde em caixa alta)."""
    t = Table([[Paragraph(texto.upper(), estilo)]], colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), VERDE_CLARO_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def gerar_pdf(plano: dict, nutricionista: dict, paciente_nome: str,
              habitos_alimentares: dict = None, observacoes_clinicas: str = None) -> bytes:
    """Constrói o PDF completo do plano alimentar e retorna seus bytes."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=16 * mm, bottomMargin=14 * mm, leftMargin=20 * mm, rightMargin=20 * mm,
    )
    est = _estilos()
    story = []

    paciente = plano["paciente"]
    necessidades = plano["necessidades"]

    # ---- Cabeçalho -------------------------------------------------------
    contato_linhas = []
    if nutricionista.get("nome"):
        contato_linhas.append(f"<b>{nutricionista['nome']}</b>")
    if nutricionista.get("especialidade"):
        contato_linhas.append(nutricionista["especialidade"])
    if nutricionista.get("crn"):
        contato_linhas.append(f"CRN {nutricionista['crn']}")
    if nutricionista.get("telefone"):
        contato_linhas.append(nutricionista["telefone"])
    if nutricionista.get("email"):
        contato_linhas.append(nutricionista["email"])
    if nutricionista.get("local_atendimento"):
        contato_linhas.append(nutricionista["local_atendimento"])
    contato_html = "<br/>".join(contato_linhas) if contato_linhas else "—"

    cabecalho = Table(
        [[Paragraph("🌿 Plano Alimentar", est["titulo_app"]),
          Paragraph(contato_html, est["contato"])]],
        colWidths=[95 * mm, 75 * mm],
    )
    cabecalho.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(cabecalho)
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=0.7, color=BORDA))
    story.append(Spacer(1, 10))

    # ---- Informações do cliente -------------------------------------------
    story.append(_barra_secao("Informações do cliente", est["secao_titulo"]))
    story.append(Spacer(1, 6))

    sexo_label = "Feminino" if paciente["sexo"] == "feminino" else "Masculino"
    linhas_cliente = [
        f"<b>Nome:</b> {paciente_nome or '—'}",
        f"<b>Sexo:</b> {sexo_label} &nbsp;&nbsp; <b>Idade:</b> {paciente['idade']} anos",
        f"<b>Peso:</b> {paciente['peso']:.1f} kg &nbsp;&nbsp; <b>Altura:</b> {paciente['altura']:.0f} cm "
        f"&nbsp;&nbsp; <b>IMC:</b> {plano['imc']} ({plano['classificacao_imc']})",
        f"<b>Objetivo:</b> {OBJETIVO_LABEL.get(paciente['objetivo'], paciente['objetivo'])}",
        f"<b>Necessidade energética estimada:</b> {necessidades.vet:.0f} kcal/dia "
        f"&nbsp;&nbsp; <b>Proteína:</b> {necessidades.proteina_g:.0f} g "
        f"&nbsp;&nbsp; <b>Carboidrato:</b> {necessidades.carboidrato_g:.0f} g "
        f"&nbsp;&nbsp; <b>Gordura:</b> {necessidades.gordura_g:.0f} g",
    ]
    if paciente.get("restricoes"):
        linhas_cliente.append(f"<b>Restrições alimentares:</b> {', '.join(paciente['restricoes'])}")

    for linha in linhas_cliente:
        story.append(Paragraph(linha, est["corpo"]))
    story.append(Spacer(1, 4))

    # ---- Recordatório alimentar (hábitos atuais do paciente) --------------
    if habitos_alimentares and any(v.strip() for v in habitos_alimentares.values() if v):
        story.append(_barra_secao("Recordatório alimentar habitual", est["secao_titulo"]))
        story.append(Spacer(1, 6))
        story.append(Paragraph(
            "Levantamento do que o paciente costumava consumir antes do início deste plano, "
            "utilizado como base para a construção das novas orientações.",
            est["corpo_cinza"],
        ))
        story.append(Spacer(1, 4))
        for rotulo, texto in habitos_alimentares.items():
            if texto and texto.strip():
                story.append(Paragraph(f"<b>{rotulo}:</b> {texto.strip()}", est["corpo"]))
        story.append(Spacer(1, 4))

    if observacoes_clinicas and observacoes_clinicas.strip():
        story.append(_barra_secao("Observações clínicas complementares", est["secao_titulo"]))
        story.append(Spacer(1, 6))
        story.append(Paragraph(observacoes_clinicas.strip(), est["corpo"]))
        story.append(Spacer(1, 4))

    # ---- Refeições ---------------------------------------------------------
    story.append(_barra_secao("Refeições", est["secao_titulo"]))
    story.append(Spacer(1, 4))

    for refeicao in plano["refeicoes"]:
        cabecalho_refeicao = f"{refeicao['horario']} &nbsp;&nbsp; {refeicao['nome'].upper()}"
        story.append(Paragraph(cabecalho_refeicao, est["refeicao_titulo"]))

        for secao in refeicao["secoes"]:
            if secao["titulo"]:
                story.append(Paragraph(secao["titulo"], est["subsecao_titulo"]))
            for item in secao["itens"]:
                story.append(Paragraph(f"•&nbsp; {item['descricao']}", est["item"]))

    story.append(Spacer(1, 6))

    # ---- Recomendações -------------------------------------------------
    recomendacoes = plano["recomendacoes"]
    story.append(_barra_secao("Recomendações", est["secao_titulo"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Ingestão de água entre as refeições", est["subsecao_titulo"]))
    story.append(Paragraph(
        f"Entre {recomendacoes['agua_min_l']:.1f} e {recomendacoes['agua_max_l']:.1f} litros por dia.",
        est["corpo"],
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Outras recomendações", est["subsecao_titulo"]))
    for tip in recomendacoes["outras"]:
        story.append(Paragraph(f"•&nbsp; {tip}", est["item"]))

    # ---- Rodapé -----------------------------------------------------------
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDA))
    story.append(Spacer(1, 4))
    validacao = plano["validacao"]
    nota_validacao = (
        "Plano dentro da tolerância científica de cálculo."
        if validacao["aprovado"] else
        "Atenção: revisar manualmente — plano fora da tolerância de cálculo "
        f"(desvio calórico de {validacao['kcal_diff_pct']:.1f}%)."
    )
    story.append(Paragraph(
        f"{nota_validacao} Este plano foi gerado por um algoritmo de apoio à decisão clínica, "
        "com base em equações e diretrizes nutricionais reconhecidas, e deve ser revisado e "
        "validado pela nutricionista responsável antes da entrega ao paciente.",
        est["rodape"],
    ))

    doc.build(story)
    return buffer.getvalue()