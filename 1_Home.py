import streamlit as st
import pandas as pd
import webbrowser

# Verifica se os dados já estão carregados no estado da sessão
if "data" not in st.session_state:
    # Lê o arquivo CSV
    data_raw = pd.read_csv('https://github.com/alexadrez/inventory-tracker-1/blob/main/Total.csv', sep=';')
    
    # Remove as linhas onde a coluna "ID" tem valores ausentes
    data_cleaned = data_raw.dropna(subset=["ID"])
    
    # Armazena os dados limpos no estado da sessão
    st.session_state["data"] = data_cleaned

st.write("# TESTANDO")
st.sidebar.markdown("Teste")

btn = st.button("Acesse os dados")
if btn:
    webbrowser.open_new_tab("https://app.powerbi.com/links/NHkCdP6ifr?ctid=80da1fca-0e59-41fa-8e47-f4faa3e1324d&pbi_source=linkShare")

st.markdown(
    """
    Testando escrever texto.
    Separando em linhas.

    Teste **negrito**.
"""
)
