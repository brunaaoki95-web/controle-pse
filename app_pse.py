import streamlit as st
import pandas as pd

# --------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# --------------------------------------------------
st.set_page_config(
    page_title="Controle de PSE",
    page_icon="📊",
    layout="centered"
)

# --------------------------------------------------
# CARREGAR PLANILHA DE ATLETAS
# --------------------------------------------------
@st.cache_data
def carregar_atletas():
    return pd.read_excel("atletas.xlsx")

df_atletas = carregar_atletas()

# --------------------------------------------------
# MAPA DE ATLETAS (id -> dados)
# --------------------------------------------------
mapa_atletas = (
    df_atletas
    .set_index("id")
    .to_dict(orient="index")
)

# --------------------------------------------------
# PEGAR PARÂMETROS DA URL (?perfil=atleta&id=1)
# --------------------------------------------------
params = st.query_params
id_atleta = params.get("id", None)

dados_atleta = None
if id_atleta:
    try:
        id_atleta = int(id_atleta)
        dados_atleta = mapa_atletas.get(id_atleta)
    except:
        dados_atleta = None

# --------------------------------------------------
# INTERFACE
# --------------------------------------------------
st.title("➕ Registrar treino")

# DATA
data = st.date_input("Data")

# NOME DO ATLETA (AUTOMÁTICO PELO LINK)
nome_atleta = dados_atleta["nome"] if dados_atleta else ""

st.text_input(
    "Nome do atleta",
    value=nome_atleta,
    disabled=True
)

# MOSTRAR CATEGORIA E POSIÇÃO
if dados_atleta:
    st.caption(
        f"Categoria: {dados_atleta['categoria']} | "
        f"Posição: {dados_atleta['posição']}"
    )
else:
    st.warning("Atleta não identificado. Verifique o link.")

# MODALIDADE
modalidade = st.selectbox(
    "Modalidade",
    ["Quadra", "Academia", "Físico"]
)

# DURAÇÃO
duracao = st.number_input(
    "Duração do treino (min)",
    min_value=0,
    step=10
)

# PSE
pse = st.slider(
    "PSE (0 = descanso | 10 = máximo)",
    0, 10, 0
)

# SALVAR (por enquanto só confirmação visual)
if st.button("Salvar"):
    st.success("Treino registrado com sucesso!")
