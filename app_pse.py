import streamlit as st
import pandas as pd
import os
from datetime import date
import matplotlib.pyplot as plt

st.set_page_config(page_title="Controle de PSE", layout="centered")

ARQUIVO_DADOS = "controle_pse.xlsx"

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        return pd.read_excel(ARQUIVO_DADOS)
    else:
        return pd.DataFrame(columns=[
            "Data",
            "Atleta",
            "Modalidade",
            "Duração (min)",
            "PSE",
            "Carga"
        ])

def salvar_dados(df):
    df.to_excel(ARQUIVO_DADOS, index=False)

st.title("📊 Controle de PSE - Treinamento")

df = carregar_dados()

st.subheader("➕ Registrar treino")

with st.form("form_pse"):
    data = st.date_input("Data", date.today())
    atleta = st.text_input("Nome do atleta")
    modalidade = st.selectbox("Modalidade", ["Quadra", "Areia", "Academia"])
    duracao = st.number_input("Duração do treino (min)", min_value=0, step=5)
    pse = st.slider("PSE (0 = descanso | 10 = máximo)", 0, 10)

    submitted = st.form_submit_button("Salvar")

    if submitted:
        if atleta == "" or duracao == 0:
            st.warning("Preencha corretamente todos os campos.")
        else:
            carga = duracao * pse

            novo_registro = pd.DataFrame([{
                "Data": data,
                "Atleta": atleta,
                "Modalidade": modalidade,
                "Duração (min)": duracao,
                "PSE": pse,
                "Carga": carga
            }])

            df = pd.concat([df, novo_registro], ignore_index=True)
            salvar_dados(df)

            st.success(f"Treino registrado! Carga = {carga}")

st.divider()
st.subheader("📋 Histórico de Treinos")

if df.empty:
    st.info("Nenhum treino registrado ainda.")
else:
    atleta_filtro = st.selectbox(
        "Filtrar por atleta",
        ["Todos"] + sorted(df["Atleta"].unique().tolist())
    )

    if atleta_filtro != "Todos":
        df_filtrado = df[df["Atleta"] == atleta_filtro]
    else:
        df_filtrado = df

    st.dataframe(df_filtrado, use_container_width=True)

    st.subheader("📈 Evolução da carga")

    df_filtrado["Data"] = pd.to_datetime(df_filtrado["Data"])
    carga_diaria = df_filtrado.groupby("Data")["Carga"].sum()

    fig, ax = plt.subplots()
    carga_diaria.plot(ax=ax, marker="o")
    ax.set_ylabel("Carga de treino")
    ax.set_xlabel("Data")
    ax.grid(True)

    st.pyplot(fig)