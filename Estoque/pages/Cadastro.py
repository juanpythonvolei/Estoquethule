import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
import requests
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
codigo = st.text_input(label='',placeholder='Insira o Código do produto')
descricao = st.text_input(label='',placeholder='Insira uma descirção do produto')
foto = st.text_input(label='',placeholder='Insira a foto do Produto')
col1,col2,col3 = st.columns(3)


@st.dialog(f"Deseja realmente excluir o produtos") 
def exclusao():
    try:
        requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
        roteiro = requiscao.json()
        dados = roteiro['Estoque']
        lista_nomes = [item for item in dados]
        produto_excluir = st.selectbox(label='',options=lista_nomes,index=None,placeholder='Selecione um produto')       
        if produto_excluir:
                    veiculo_ref = db.reference(f'Estoque/{produto_excluir}')
                    veiculo_ref.delete()
                    st.success(f'Produto {produto_excluir} excluido')
        else:
                st.info(f'Você realmente deseja excluir o produto {produto_excluir}')
    except:
        st.info('Por enquanto, não foram registrados produtos')


excluir = st.button('Excluir Produtos')
if excluir:
        exclusao()
ref = db.reference('Estoque')
if codigo and descricao and foto:
    with col1:
        cadastro = st.button('Cadastar Produtos')
        if cadastro:
            dict_produto = {'Foto':foto,'Descrição':descricao}
            try:
                        caminho_cadastro = f'{codigo}'
                        ref.child(caminho_cadastro).set({
                        'foto':foto,
                        'Descrição':descricao
                    })
            except:
                        st.error('Não há saida de dados disponível')

else:
        st.error('Ainda há campos a serem preenchidos')
with st.popover('Alterar informações de Produtos'):
    requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
    roteiro = requiscao.json()
    dados = roteiro['Estoque']
    lista_produto_alteracao = []
    lista_alteracao_campo = []
    for item in dados:
        lista_produto_alteracao.append(item)
        for elemento in dados[f'{item}']:
            lista_alteracao_campo.append(elemento)
    alteracao_item = st.selectbox(placeholder='Selecione a alteração',label='',options=lista_produto_alteracao)
    
    if alteracao_item
           alteracao_campo = st.selectbox(placeholder='Selecione a alteração',label='',options=lista_alteracao_campo)

    
