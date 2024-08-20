import streamlit as st
import requests as rq
import pandas as pd
import numpy as np
import plotly.express as px

url = 'http://127.0.0.1:8000/api/v1/arrecadacao'

st.set_page_config(layout='wide', initial_sidebar_state='collapsed', page_title='📊 CNAE-ICMS Analytics')

st.title('CNAE-ICMS Analytics')

# Função para formatar os números
def formata_numero(valor, prefixo=''):
    if valor >= 1_000_000_000:  # Bilhões
        return f"{prefixo} {valor/1_000_000_000:.2f} bilhões"
    elif valor >= 1_000_000:  # Milhões
        return f"{prefixo} {valor/1_000_000:.2f} milhões"
    elif valor >= 1_000:  # Milhares
        return f"{prefixo} {valor/1_000:.2f} mil"
    else:  # Menor que mil
        return f"{prefixo} {valor:.2f}"

# Criação das abas
aba1, aba2, aba3 = st.tabs(['Arrecadações por comércio e mensais', 'Visualização Detalhada', 'Dataframe'])

# Primeira aba: Arrecadações por comércio e mensais
with aba1:
    # Sidebar com formulário
    with st.sidebar.form(key='filter_form'):
        # Sidebar para selecionar o intervalo de datas
        start_date = st.date_input('Data de início', value=pd.to_datetime('2020-01-01'))
        end_date = st.date_input('Data de término', value=pd.to_datetime('2020-12-31'))

        # Sidebar para selecionar múltiplos comércios
        comercios = list(pd.read_json(url)['comercio'].unique())
        selected_comercios = st.multiselect('Selecione os Comércios', sorted(comercios), default=comercios)

        # Botão de submissão do formulário
        submit_button = st.form_submit_button(label='Aplicar Filtros')

    response = rq.get(url)
    dados = pd.DataFrame(response.json())
    dados['valor'] = pd.to_numeric(dados['valor'], errors='coerce')
    dados = dados.dropna(subset=['valor'])
    dados['data'] = pd.to_datetime(dados['data'], format='%Y-%m-%d')

    # Aplicar filtro de data
    dados = dados[(dados['data'] >= pd.to_datetime(start_date)) & (dados['data'] <= pd.to_datetime(end_date))]

    # Aplicar filtro de comércios, se houver seleções
    if selected_comercios:
        dados = dados[dados['comercio'].isin(selected_comercios)]

    # Verifique se a coluna 'comercio' existe e trate valores ausentes
    if 'comercio' in dados.columns:
        dados['comercio'] = dados['comercio'].fillna('Desconhecido')  # Preencha valores ausentes com 'Desconhecido'
        
        # Agrupe por comércio e calcule a soma dos valores
        receita_comercio = dados.groupby('comercio')['valor'].sum().sort_values(ascending=False).reset_index()
        receita_comercio['valor_formatado'] = receita_comercio['valor'].apply(lambda x: formata_numero(x, prefixo='R$'))
    else:
        st.error("A coluna 'comercio' não foi encontrada nos dados.")

    receita_mensal = dados.set_index('data').groupby(pd.Grouper(freq='ME'))['valor'].sum().reset_index()

    receita_mensal['Ano'] = receita_mensal['data'].dt.year
    receita_mensal['Mês'] = receita_mensal['data'].dt.month_name()

    receita_mensal = receita_mensal.sort_values('data')

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Arrecadado", formata_numero(dados['valor'].sum(), prefixo='R$'))
        fig_rec_comercio = px.bar(receita_comercio,
                                x='comercio',
                                y='valor',
                                color='comercio',
                                title='Arrecadação por Comércio',
                                labels={'comercio': 'Comércio', 'valor': 'Valor Arrecadado'},
                                text='valor_formatado')
        fig_rec_comercio.update_traces(textangle=0)
        st.plotly_chart(fig_rec_comercio, use_container_width=True)

    with col2:
        st.metric("Quantidade de Arrecadações", formata_numero(dados['valor'].count()))
        fig_rec_mensal = px.line(receita_mensal,
                                x='data',
                                y='valor',
                                markers=True,
                                range_y=(0, receita_mensal['valor'].max() + 1),
                                color='Ano',
                                line_dash='Ano',
                                labels={'data': 'Mês', 'valor': 'Valor Arrecadado'},
                                title='Arrecadação Mensal')
        st.plotly_chart(fig_rec_mensal, use_container_width=True)

# Segunda aba: Visualização Detalhada
with aba2:
    with st.expander("Filtros Específicos", expanded=False):  # Alterado para vir oculto por padrão
        # Filtrar opções com base na seleção anterior
        secao_options = sorted(dados['secao'].unique())  # Ordenação alfabética
        selected_secao = st.selectbox('Selecione a Seção', ['Todas'] + secao_options)
        
        divisao_options = sorted(dados[dados['secao'] == selected_secao]['divisao'].unique()) if selected_secao != 'Todas' else sorted(dados['divisao'].unique())
        selected_divisao = st.selectbox('Selecione a Divisão', ['Todas'] + divisao_options)
        
        grupo_options = sorted(dados[dados['divisao'] == selected_divisao]['grupo'].unique()) if selected_divisao != 'Todas' else sorted(dados['grupo'].unique())
        selected_grupo = st.selectbox('Selecione o Grupo', ['Todas'] + grupo_options)
        
        classe_options = sorted(dados[dados['grupo'] == selected_grupo]['classe'].unique()) if selected_grupo != 'Todas' else sorted(dados['classe'].unique())
        selected_classe = st.selectbox('Selecione a Classe', ['Todas'] + classe_options)
        
        subclasse_options = sorted(dados[dados['classe'] == selected_classe]['subclasse'].unique()) if selected_classe != 'Todas' else sorted(dados['subclasse'].unique())
        selected_subclasse = st.selectbox('Selecione a Subclasse', ['Todas'] + subclasse_options)

    # Aplicar filtros específicos
    filtered_data = dados.copy()
    if selected_secao != 'Todas':
        filtered_data = filtered_data[filtered_data['secao'] == selected_secao]
    if selected_divisao != 'Todas':
        filtered_data = filtered_data[filtered_data['divisao'] == selected_divisao]
    if selected_grupo != 'Todas':
        filtered_data = filtered_data[filtered_data['grupo'] == selected_grupo]
    if selected_classe != 'Todas':
        filtered_data = filtered_data[filtered_data['classe'] == selected_classe]
    if selected_subclasse != 'Todas':
        filtered_data = filtered_data[filtered_data['subclasse'] == selected_subclasse]

    # Adicionar as métricas Total Arrecadado e Quantidade de Arrecadações
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Arrecadado", formata_numero(filtered_data['valor'].sum(), prefixo='R$'))
    with col2:
        st.metric("Quantidade de Arrecadações", formata_numero(filtered_data['valor'].count()))

    # Calcular arrecadação mensal com base nos filtros
    receita_detalhada = filtered_data.groupby('data')['valor'].sum().reset_index()
    receita_detalhada['valor_formatado'] = receita_detalhada['valor'].apply(lambda x: formata_numero(x, prefixo='R$'))

    # Exibir gráfico de arrecadação detalhada
    fig_rec_detalhada = px.bar(receita_detalhada,
                               x='data',
                               y='valor',
                               title='Arrecadação Detalhada por Filtros',
                               labels={'data': 'Data', 'valor': 'Valor Arrecadado'},
                               text='valor_formatado')  # Exibindo o valor formatado no gráfico

    fig_rec_detalhada.update_traces(textangle=0)  # Manter o texto alinhado horizontalmente
    st.plotly_chart(fig_rec_detalhada, use_container_width=True)


# Terceira aba: Dataframe
with aba3:
    st.dataframe(dados)
