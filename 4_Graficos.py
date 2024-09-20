import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Função para carregar os dados
def load_data():
    # Verificar se "data" já foi inicializado no session_state, caso contrário, inicializar com dados de exemplo
    if "data" not in st.session_state:
        # Lê o arquivo CSV
        data_raw = pd.read_csv('C:\\Users\\aleguimaraes\\repos\\aulas_dsfame_streamlit\\data\\Total.csv', sep=';')
        
        # Remove as linhas onde a coluna "ID" tem valores ausentes
        data_cleaned = data_raw.dropna(subset=["ID"])
        
        # Limpar os nomes das colunas (remover espaços extras)
        data_cleaned.columns = data_cleaned.columns.str.strip()

        # Armazena os dados limpos no estado da sessão
        st.session_state["data"] = data_cleaned

    # Transformar os dados em um DataFrame
    data = st.session_state["data"]
    df = pd.DataFrame(data)
    
    # Verificar se as colunas 'Created' e 'Closed' existem
    if 'Created' not in df.columns or 'Closed' not in df.columns:
        st.error("As colunas 'Created' ou 'Closed' não foram encontradas no arquivo CSV.")
        st.write("Colunas disponíveis no arquivo:", df.columns.tolist())  # Exibe as colunas disponíveis para depuração
        return pd.DataFrame()  # Retorna um DataFrame vazio para evitar erros subsequentes

    # Converter colunas de datas
    df['Created'] = pd.to_datetime(df['Created'], errors='coerce')  # Converte para datetime, ignorando erros
    df['Closed'] = pd.to_datetime(df['Closed'], errors='coerce')  # Converte para datetime, ignorando erros
    
    # Ajustar a coluna 'Assigned' para manter apenas o texto antes do '<'
    df['Assigned'] = df['Assigned'].str.split('<').str[0].str.strip()
    
    return df

# Carregar os dados
df = load_data()

# Verificar se o DataFrame está vazio (caso tenha ocorrido um erro de carregamento)
if df.empty:
    st.stop()  # Interrompe a execução do código se o DataFrame estiver vazio

# Configurar a barra lateral para selecionar o ano e o tipo de trabalho
st.sidebar.title("Filtros")

# Filtrar os anos disponíveis com base na coluna 'Created'
years = df['Created'].dt.year.dropna().unique()
selected_year = st.sidebar.selectbox('Selecione o Ano de Abertura:', sorted(years), index=len(years)-1)

# Filtrar os tipos de trabalho disponíveis (coluna 'Work')
work_types = df['Work'].unique()
work_types = ['Todos'] + list(work_types)  # Adiciona "Todos" como primeira opção
selected_work_type = st.sidebar.selectbox('Selecione o Tipo de Trabalho:', work_types)

# Filtrar os dados com base no ano e tipo de trabalho selecionados
df_filtered = df[df['Created'].dt.year == selected_year]

if selected_work_type != 'Todos':
    df_filtered = df_filtered[df_filtered['Work'] == selected_work_type]

# Verificar se há dados após os filtros
if df_filtered.empty:
    st.warning(f'Nenhum dado encontrado para o ano {selected_year} e tipo "{selected_work_type}".')
else:
    # Contar a quantidade de atribuições por analista
    analyst_counts = df_filtered['Assigned'].value_counts()

    # Verificar se há dados suficientes para gerar o gráfico
    if analyst_counts.empty:
        st.warning(f'Nenhuma atribuição de analista encontrada para o ano {selected_year} e tipo "{selected_work_type}".')
    else:
        # Criar o gráfico de pizza
        fig, ax = plt.subplots()
        ax.pie(analyst_counts, labels=analyst_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Assegura que o gráfico de pizza seja desenhado como um círculo.

        # Configurar o título do gráfico
        st.title(f'Distribuição de ESCs por Analista - {selected_year} ({selected_work_type})')

        # Exibir o gráfico de pizza
        st.pyplot(fig)