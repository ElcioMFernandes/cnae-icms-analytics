import streamlit as st
import requests as rq
import pandas as pd
import numpy as np
import plotly.express as px

url = 'http://127.0.0.1:8000/api/v1/arrecadacao'

st.set_page_config(layout='wide', initial_sidebar_state='collapsed', page_title='📊 CNAE-ICMS Analytics')

st.title('CNAE-ICMS Analytics')

# Definir o mapeamento de cores para cada comércio
color_map = {
    'Comércio': '#1f77b4',  # Azul
    'Indústria': '#ff7f0e',  # Laranja
    'Serviço': '#2ca02c',    # Verde
    'Agropecuária e Pesca': '#d62728',  # Vermelho
    'Meio Ambiente': '#9467bd'  # Roxo
}


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
aba1, aba2, aba3 = st.tabs(['Visão Geral', 'Visão Detalhada', 'Dataframe'])

# Primeira aba: Arrecadações por comércio e mensais
with aba1:
    # Sidebar com formulário
    with st.sidebar.form(key='filter_form'):
        start_date = st.date_input('Data de início', value=pd.to_datetime('2020-01-01'))
        end_date = st.date_input('Data de término', value=pd.to_datetime('2020-12-31'))
        comercios = list(pd.read_json(url)['comercio'].unique())
        selected_comercios = st.multiselect('Selecione os Comércios', sorted(comercios), default=comercios)
        submit_button = st.form_submit_button(label='Aplicar Filtros')

    response = rq.get(url)
    dados = pd.DataFrame(response.json())
    dados['valor'] = pd.to_numeric(dados['valor'], errors='coerce')
    dados = dados.dropna(subset=['valor'])
    dados['data'] = pd.to_datetime(dados['data'], format='%Y-%m-%d')

    # Aplicar filtro de data e comércios
    dados = dados[(dados['data'] >= pd.to_datetime(start_date)) & (dados['data'] <= pd.to_datetime(end_date))]
    if selected_comercios:
        dados = dados[dados['comercio'].isin(selected_comercios)]

    if 'comercio' in dados.columns:
        dados['comercio'] = dados['comercio'].fillna('Desconhecido')
        receita_comercio = dados.groupby('comercio')['valor'].sum().sort_values(ascending=False).reset_index()
        receita_comercio['valor_formatado'] = receita_comercio['valor'].apply(lambda x: formata_numero(x, prefixo='R$'))
    else:
        st.error("A coluna 'comercio' não foi encontrada nos dados.")

    receita_mensal = dados.set_index('data').groupby(pd.Grouper(freq='ME'))['valor'].sum().reset_index()
    receita_mensal['Ano'] = receita_mensal['data'].dt.year
    receita_mensal['Mês'] = receita_mensal['data'].dt.month_name()
    receita_mensal = receita_mensal.sort_values('data')

    # Métricas lado a lado
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Arrecadado", formata_numero(dados['valor'].sum(), prefixo='R$'))
    with col2:
        media_arrecadacao = dados['valor'].mean()
        st.metric("Média de Arrecadação por Comércio", formata_numero(media_arrecadacao, prefixo='R$'))
    with col3:
        maior_arrecadacao_mes = receita_mensal['valor'].max()
        st.metric("Maior Arrecadação Mensal", formata_numero(maior_arrecadacao_mes, prefixo='R$'))
    with col4:
        st.metric("Quantidade de Arrecadações", dados['valor'].count())


    # Adicionar um único st.markdown para separar as métricas dos gráficos
    st.markdown('---')

    # Gráficos lado a lado
    col1, col2 = st.columns(2)
    with col1:
        fig_rec_comercio = px.bar(receita_comercio,
                                  x='comercio',
                                  y='valor',
                                  color='comercio',
                                  title='Arrecadação por Comércio',
                                  color_discrete_map=color_map,
                                  labels={'comercio': 'Comércio', 'valor': 'Valor Arrecadado'},
                                  text='valor_formatado')
        fig_rec_comercio.update_traces(textangle=0)
        st.plotly_chart(fig_rec_comercio, use_container_width=True)

    with col2:
        receita_historico_comercio = dados.groupby([pd.Grouper(key='data', freq='M'), 'comercio'])['valor'].sum().reset_index()
        fig_rec_historico = px.line(receita_historico_comercio,
                                    x='data',
                                    y='valor',
                                    color='comercio',
                                    title='Histórico de Arrecadação por Comércio',
                                    color_discrete_map=color_map,
                                    labels={'data': 'Data', 'valor': 'Valor Arrecadado', 'comercio': 'Comércio'},
                                    markers=True)

        st.plotly_chart(fig_rec_historico, use_container_width=True)

# Função para buscar a descrição de um código CNAE
def busca_descricao(endpoint, codigo):
    url = f"{endpoint}?codigo={codigo}"
    response = rq.get(url)
    if response.status_code == 200:
        return response.json()[0]['descricao']
    else:
        return codigo  # Caso falhe, retorna o código como fallback

# Segunda aba: Visualização Detalhada
with aba2:
    col1, col2 = st.columns([1, 2])  # Aumentar a proporção da segunda coluna para o gráfico

    # Na primeira coluna, os filtros
    with col1:
        with st.expander("Filtros Específicos", expanded=True):  # Filtros colapsados por padrão
            # Carregar descrições para a Seção
            secao_options = sorted(dados['secao'].unique())
            secao_descriptions = {secao: busca_descricao("http://127.0.0.1:8000/api/v1/secao/", secao).capitalize() for secao in secao_options}
            selected_secao = st.selectbox('Selecione a Seção', ['Todas'] + [secao_descriptions[secao] for secao in secao_options])

            # Carregar descrições para a Divisão com base na Seção selecionada
            if selected_secao != 'Todas':
                selected_secao_codigo = list(secao_descriptions.keys())[list(secao_descriptions.values()).index(selected_secao)]
                divisao_options = sorted(dados[dados['secao'] == selected_secao_codigo]['divisao'].unique())
                divisao_descriptions = {divisao: busca_descricao("http://127.0.0.1:8000/api/v1/divisao/", divisao).capitalize() for divisao in divisao_options}
                selected_divisao = st.selectbox('Selecione a Divisão', ['Todas'] + [divisao_descriptions[divisao] for divisao in divisao_options])
            else:
                selected_divisao = st.selectbox('Selecione a Divisão', ['Todas'], disabled=True)

            # Carregar descrições para o Grupo com base na Divisão selecionada
            if selected_divisao != 'Todas':
                selected_divisao_codigo = list(divisao_descriptions.keys())[list(divisao_descriptions.values()).index(selected_divisao)]
                grupo_options = sorted(dados[dados['divisao'] == selected_divisao_codigo]['grupo'].unique())
                grupo_descriptions = {grupo: busca_descricao("http://127.0.0.1:8000/api/v1/grupo/", grupo).capitalize() for grupo in grupo_options}
                selected_grupo = st.selectbox('Selecione o Grupo', ['Todas'] + [grupo_descriptions[grupo] for grupo in grupo_options])
            else:
                selected_grupo = st.selectbox('Selecione o Grupo', ['Todas'], disabled=True)

            # Carregar descrições para a Classe com base no Grupo selecionado
            if selected_grupo != 'Todas':
                selected_grupo_codigo = list(grupo_descriptions.keys())[list(grupo_descriptions.values()).index(selected_grupo)]
                classe_options = sorted(dados[dados['grupo'] == selected_grupo_codigo]['classe'].unique())
                classe_descriptions = {classe: busca_descricao("http://127.0.0.1:8000/api/v1/classe/", classe).capitalize() for classe in classe_options}
                selected_classe = st.selectbox('Selecione a Classe', ['Todas'] + [classe_descriptions[classe] for classe in classe_options])
            else:
                selected_classe = st.selectbox('Selecione a Classe', ['Todas'], disabled=True)

            # Carregar descrições para a Subclasse com base na Classe selecionada
            if selected_classe != 'Todas':
                selected_classe_codigo = list(classe_descriptions.keys())[list(classe_descriptions.values()).index(selected_classe)]
                subclasse_options = sorted(dados[dados['classe'] == selected_classe_codigo]['subclasse'].unique())
                subclasse_descriptions = {subclasse: busca_descricao("http://127.0.0.1:8000/api/v1/subclasse/", subclasse).capitalize() for subclasse in subclasse_options}
                selected_subclasse = st.selectbox('Selecione a Subclasse', ['Todas'] + [subclasse_descriptions[subclasse] for subclasse in subclasse_options])
            else:
                selected_subclasse = st.selectbox('Selecione a Subclasse', ['Todas'], disabled=True)

    # Definir o filtro ativo com base na seleção do usuário
    filtro_ativo = "Nenhum filtro aplicado, exibindo todos os dados"
    if selected_subclasse != 'Todas':
        filtro_ativo = f"Filtrado por Subclasse: {selected_subclasse}"
    elif selected_classe != 'Todas':
        filtro_ativo = f"Filtrado por Classe: {selected_classe}"
    elif selected_grupo != 'Todas':
        filtro_ativo = f"Filtrado por Grupo: {selected_grupo}"
    elif selected_divisao != 'Todas':
        filtro_ativo = f"Filtrado por Divisão: {selected_divisao}"
    elif selected_secao != 'Todas':
        filtro_ativo = f"Filtrado por Seção: {selected_secao}"

    # Na segunda coluna, os gráficos ocupam mais espaço
    with col2:
        # Aplicar filtros específicos ao dataframe
        filtered_data = dados.copy()
        if selected_secao != 'Todas':
            filtered_data = filtered_data[filtered_data['secao'] == list(secao_descriptions.keys())[list(secao_descriptions.values()).index(selected_secao)]]
        if selected_divisao != 'Todas':
            filtered_data = filtered_data[filtered_data['divisao'] == list(divisao_descriptions.keys())[list(divisao_descriptions.values()).index(selected_divisao)]]
        if selected_grupo != 'Todas':
            filtered_data = filtered_data[filtered_data['grupo'] == list(grupo_descriptions.keys())[list(grupo_descriptions.values()).index(selected_grupo)]]
        if selected_classe != 'Todas':
            filtered_data = filtered_data[filtered_data['classe'] == list(classe_descriptions.keys())[list(classe_descriptions.values()).index(selected_classe)]]
        if selected_subclasse != 'Todas':
            filtered_data = filtered_data[filtered_data['subclasse'] == list(subclasse_descriptions.keys())[list(subclasse_descriptions.values()).index(selected_subclasse)]]

        # Métricas lado a lado
        col3, col4 = st.columns(2)
        with col3:
            st.metric("Total Arrecadado", formata_numero(filtered_data['valor'].sum(), prefixo='R$'))
        with col4:
            st.metric("Quantidade de Arrecadações", filtered_data['valor'].count())

        st.markdown('---')
        
        # Exibir o filtro ativo abaixo dos filtros
        st.write(f"**{filtro_ativo}**")

        # Gráfico na largura total da coluna 2
        receita_detalhada = filtered_data.groupby('data')['valor'].sum().reset_index()
        receita_detalhada['valor_formatado'] = receita_detalhada['valor'].apply(lambda x: formata_numero(x, prefixo='R$'))

        fig_rec_detalhada = px.bar(receita_detalhada,
                                   x='data',
                                   y='valor',
                                   labels={'data': 'Data', 'valor': 'Valor arrecadado'},
                                   text='valor_formatado')  # Exibindo o valor formatado no gráfico

        fig_rec_detalhada.update_traces(textangle=0)  # Manter o texto alinhado horizontalmente
        st.plotly_chart(fig_rec_detalhada, use_container_width=True)

# Terceira aba: Dataframe
with aba3:
    st.dataframe(dados)
