import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Função para carregar os dados
def load_data():
    # Verificar se "data" já foi inicializado no session_state, caso contrário, inicializar com dados de exemplo
    if "data" not in st.session_state:
        # Aqui você pode carregar dados de exemplo ou dados reais de um arquivo/URL
        st.session_state["data"] = {
            'Created': ['2024-01-05', '2024-02-15', '2024-03-20', '2023-04-10', '2023-05-25'],
            'Closed': ['2024-02-10', '2024-03-18', '2024-04-25', '2023-05-15', '2023-06-30'],
            'Work': ['ESC', 'ESC', 'ESC', 'ESC', 'ESC'],
            'Assigned': ['Analista A', 'Analista B', 'Analista A', 'Analista C', 'Analista B']
        }

    # Transformar os dados em um DataFrame
    data = st.session_state["data"]
    df = pd.DataFrame(data)
    
    # Converter colunas de datas
    df['Created'] = pd.to_datetime(df['Created'])
    df['Closed'] = pd.to_datetime(df['Closed'])
    
    # Ajustar a coluna 'Assigned' para manter apenas o texto antes do '<'
    df['Assigned'] = df['Assigned'].str.split('<').str[0].str.strip()
    
    return df

# Carregar os dados
df = load_data()

# Configurar o Streamlit
st.title('Análise de ESCs')

# Adicionar filtro na barra lateral para selecionar o tipo de "Work"
work_types = df['Work'].unique()
work_types = np.insert(work_types, 0, "Todos")  # Adiciona "Todos" como primeira opção
selected_work_type = st.sidebar.selectbox('Selecione o Tipo:', work_types, index=int(np.where(work_types == "ESC")[0][0]))

# Adicionar filtro na barra lateral para selecionar o analista "Assigned"
analysts = df['Assigned'].unique()
analysts = np.insert(analysts, 0, "Todos")  # Adiciona "Todos" como primeira opção
selected_analyst = st.sidebar.selectbox('Selecione o Analista:', analysts, index=0)

# Filtrar os dados pelo tipo de "Work" e analista selecionados
if selected_work_type == "Todos":
    df_filtered = df
else:
    df_filtered = df[df['Work'] == selected_work_type]

if selected_analyst != "Todos":
    df_filtered = df_filtered[df_filtered['Assigned'] == selected_analyst]

df_2023 = df_filtered[df_filtered['Created'].dt.year == 2023]
df_2024 = df_filtered[df_filtered['Created'].dt.year == 2024]

# Contar o número de criações por mês para cada ano
df_2023['month'] = df_2023['Created'].dt.month
df_2024['month'] = df_2024['Created'].dt.month
creations_2023 = df_2023['month'].value_counts().sort_index()
creations_2024 = df_2024['month'].value_counts().sort_index()

# Garantir que todos os meses estejam representados
all_months = range(1, 13)
creations_2023 = creations_2023.reindex(all_months, fill_value=0)
creations_2024 = creations_2024.reindex(all_months, fill_value=0)

# Criar o gráfico de barras para comparação entre 2023 e 2024
fig1, ax1 = plt.subplots()
width = 0.35  # Largura das barras

# Posições das barras no eixo x
x = np.arange(len(all_months))

# Barras para 2023 e 2024
bars1 = ax1.bar(x - width/2, creations_2023, width, label='2023')
bars2 = ax1.bar(x + width/2, creations_2024, width, label='2024')

# Adicionar rótulos de dados
for bar in bars1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom', ha='center')

for bar in bars2:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom', ha='center')

# Configurar o gráfico
ax1.set_xlabel('Mês')
ax1.set_ylabel('Quantidades')
ax1.set_title(f'"{selected_work_type}" por "{selected_analyst}" abertas por Mês em 2023 e 2024')
ax1.set_xticks(x)
ax1.set_xticklabels(['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])
ax1.legend()

# Exibir o primeiro gráfico no Streamlit
st.pyplot(fig1)

# Função para adicionar o total geral por analista e uma linha de total geral
def add_total_columns_and_row(df_table):
    # Adicionar coluna "Total Geral" por analista (soma por linha)
    df_table['Total analista'] = df_table.sum(axis=1)
    
    # Calcular o total de cada coluna (mês) e também o total geral
    total_row = df_table.sum(axis=0)
    total_row.name = 'Total mês'
    
    # Adicionar a linha de total ao DataFrame usando pd.concat()
    df_table_with_total = pd.concat([df_table, pd.DataFrame([total_row])])
    
    return df_table_with_total

# Criar tabela de analistas por mês para 2023 e 2024
analyst_table_2023 = df_2023.groupby(['Assigned', df_2023['Created'].dt.month]).size().unstack(fill_value=0)
analyst_table_2023 = add_total_columns_and_row(analyst_table_2023)  # Adicionar total geral por analista e por mês

analyst_table_2024 = df_2024.groupby(['Assigned', df_2024['Created'].dt.month]).size().unstack(fill_value=0)
analyst_table_2024 = add_total_columns_and_row(analyst_table_2024)  # Adicionar total geral por analista e por mês

# Exibir as tabelas
st.write("Tabela de Analistas por Mês em 2023")
st.table(analyst_table_2023)

st.write("Tabela de Analistas por Mês em 2024")
st.table(analyst_table_2024)

# Filtrar dados para o ano de 2024
if selected_work_type == "Todos":
    df_2024_total = df[(df['Created'].dt.year == 2024)]
else:
    df_2024_total = df[(df['Work'] == selected_work_type) & (df['Created'].dt.year == 2024)]

if selected_analyst != "Todos":
    df_2024_total = df_2024_total[df_2024_total['Assigned'] == selected_analyst]

# Contar todas as criações abertas por mês
df_2024_total['created_month'] = df_2024_total['Created'].dt.month
abertas_por_mes = df_2024_total['created_month'].value_counts().sort_index()

# Filtrar dados fechados do tipo "ESC" em 2024
if selected_work_type == "Todos":
    df_esc_2024_closed = df[(df['Closed'].dt.year == 2024)]
else:
    df_esc_2024_closed = df[(df['Work'] == selected_work_type) & (df['Closed'].dt.year == 2024)]

if selected_analyst != "Todos":
    df_esc_2024_closed = df_esc_2024_closed[df_esc_2024_closed['Assigned'] == selected_analyst]

# Contar fechadas por mês
df_esc_2024_closed['closed_month'] = df_esc_2024_closed['Closed'].dt.month
fechadas_por_mes = df_esc_2024_closed['closed_month'].value_counts().sort_index()

# Garantir que todos os meses estejam representados
abertas_por_mes = abertas_por_mes.reindex(all_months, fill_value=0)
fechadas_por_mes = fechadas_por_mes.reindex(all_months, fill_value=0)

# Criar gráfico de barras para todas abertas e fechadas do tipo "ESC" por mês em 2024
fig2, ax2 = plt.subplots()

# Barras para abertas e fechadas
bars3 = ax2.bar(x - width/2, abertas_por_mes, width, label='Abertas')
bars4 = ax2.bar(x + width/2, fechadas_por_mes, width, label='Fechadas')

# Adicionar rótulos de dados
for bar in bars3:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom', ha='center')

for bar in bars4:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom', ha='center')

# Configurar o gráfico
ax2.set_xlabel('Mês')
ax2.set_ylabel('Quantidades')
ax2.set_title(f'ESCs por "{selected_analyst}" abertas e fechadas em 2024')
ax2.set_xticks(x)
ax2.set_xticklabels(['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])
ax2.legend()

# Exibir o segundo gráfico no Streamlit
st.pyplot(fig2)

# Criar tabela de analistas por mês para ESCs abertas e fechadas em 2024
analyst_table_open_2024 = df_2024_total.groupby(['Assigned', df_2024_total['Created'].dt.month]).size().unstack(fill_value=0)
analyst_table_open_2024 = add_total_columns_and_row(analyst_table_open_2024)  # Adicionar total geral por analista e por mês

analyst_table_closed_2024 = df_esc_2024_closed.groupby(['Assigned', df_esc_2024_closed['Closed'].dt.month]).size().unstack(fill_value=0)
analyst_table_closed_2024 = add_total_columns_and_row(analyst_table_closed_2024)  # Adicionar total geral por analista e por mês

# Exibir as tabelas
st.write("Tabela de Analistas para ESCs Abertas por Mês em 2024")
st.table(analyst_table_open_2024)

st.write("Tabela de Analistas para ESCs Fechadas por Mês em 2024")
st.table(analyst_table_closed_2024)