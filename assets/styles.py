"""
assets/styles.py
CSS customizado injetado no Streamlit para criar a identidade visual
premium dark mode (verde profundo / verde oliva / dourado fosco),
inspirada conceitualmente em estéticas minimalistas de nutrição
clínica de alto padrão. Nenhuma marca ou identidade gráfica específica
é reproduzida — apenas o conceito estético (dark, elegante, verde+dourado).
"""

import config


def get_css() -> str:
    c = config.COLORS
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Jost:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'Jost', sans-serif;
}}

.stApp {{
    background: linear-gradient(180deg, {c['bg_primary']} 0%, {c['bg_secondary']} 100%);
    color: {c['text_primary']};
}}

section[data-testid="stSidebar"] {{
    background: {c['bg_secondary']};
    border-right: 1px solid {c['border']};
}}

h1, h2, h3 {{
    font-family: 'Cormorant Garamond', serif;
    color: {c['gold_soft']};
    letter-spacing: 0.5px;
}}

.app-header {{
    text-align: center;
    padding: 1.2rem 0 0.4rem 0;
    border-bottom: 1px solid {c['border']};
    margin-bottom: 1.6rem;
}}
.app-header h1 {{
    font-size: 2.6rem;
    margin-bottom: 0.1rem;
    color: {c['gold']};
}}
.app-header p {{
    color: {c['text_secondary']};
    font-size: 0.95rem;
    letter-spacing: 2px;
    text-transform: uppercase;
}}

.stButton > button {{
    background: linear-gradient(135deg, {c['green_deep']} 0%, {c['green_olive']} 100%);
    color: {c['text_primary']};
    border: 1px solid {c['gold']};
    border-radius: 6px;
    padding: 0.7rem 1.4rem;
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-size: 0.85rem;
    width: 100%;
    transition: all 0.25s ease;
}}
.stButton > button:hover {{
    background: {c['gold']};
    color: {c['bg_primary']};
    border-color: {c['gold']};
}}

.card {{
    background: {c['bg_card']};
    border: 1px solid {c['border']};
    border-radius: 10px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1.1rem;
}}

.card-meal-title {{
    color: {c['gold']};
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.5rem;
    margin-bottom: 0.2rem;
    border-bottom: 1px solid {c['border']};
    padding-bottom: 0.4rem;
}}

.food-item {{
    padding: 0.55rem 0;
    border-bottom: 1px dashed {c['border']};
}}
.food-item:last-child {{
    border-bottom: none;
}}
.food-name {{
    color: {c['text_primary']};
    font-weight: 500;
    font-size: 1.02rem;
}}
.food-detail {{
    color: {c['text_secondary']};
    font-size: 0.85rem;
}}
.food-sub {{
    color: {c['green_olive']};
    font-size: 0.78rem;
    margin-top: 0.15rem;
}}

.badge {{
    display: inline-block;
    padding: 0.25rem 0.7rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}}
.badge-success {{
    background: rgba(111, 174, 140, 0.15);
    color: {c['success']};
    border: 1px solid {c['success']};
}}
.badge-warning {{
    background: rgba(201, 107, 92, 0.15);
    color: {c['danger']};
    border: 1px solid {c['danger']};
}}

.metric-row {{
    display: flex;
    gap: 0.8rem;
    flex-wrap: wrap;
}}
.metric-box {{
    flex: 1;
    min-width: 130px;
    background: {c['bg_card']};
    border: 1px solid {c['border']};
    border-radius: 10px;
    padding: 0.9rem 1rem;
    text-align: center;
}}
.metric-value {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.9rem;
    color: {c['gold']};
    font-weight: 600;
}}
.metric-label {{
    color: {c['text_secondary']};
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

hr {{
    border-color: {c['border']};
}}

::-webkit-scrollbar {{
    width: 8px;
}}
::-webkit-scrollbar-thumb {{
    background: {c['green_olive']};
    border-radius: 4px;
}}
</style>
"""