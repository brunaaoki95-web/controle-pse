import streamlit as st
import pandas as pd

# --------------------------------------------------
# CONFIGURAÇÃO
# --------------------------------------------------
st.set_page_config(
    page_title="Controle de PSE",
    page_icon="📊",
    layout="centered"
)

# --------------------------------------------------
# CARREGAR ATLETAS (COM TRATAMENTO DE ERRO)
# --------------------------------------------------
@st.cache_data
def carregar_atletas():
    df = pd.read_excel("atletas.xlsx")

    # Padronizar nomes das colunas
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    return df

df_atletas = carregar_atletas()

# DEBUG VISUAL (pode remover depois)
st.write("Colunas encontradas:", df_atletas.columns.tolist())

# --------------------------------------------------
# VERIFICAÇÃO DE SEGURANÇA
# --------------------------------------------------
colunas_necessarias = {"id", "nome", "categoria", "posição"}

if not colunas_necessarias.issubset(df_atletas.columns):
    st.error("❌ Erro na planilha atletas.xlsx")
    st.error(f"Colunas esperadas: {colunas_necessarias}")
    st.stop()

# --------------------------------------------------
# MAPA DE ATLETAS
# --------------------------------------------------
mapa_atletas = (
    df_atletas
    .set_index("id")
    .to_dict(orient="index")
)

# --------------------------------------------------
# PEGAR PARÂMETROS DA URL
# --------------------------------------------------
params = st.query_params
id_atleta = params.get("id")

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

# NOME DO ATLETA
nome_atleta = dados_atleta["nome"] if dados_atleta else ""

st.text_input(
    "Nome do atleta",
    value=nome_atleta,
    disabled=True
)

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

if st.button("Salvar"):
    st.success("Treino registrado com sucesso!")
