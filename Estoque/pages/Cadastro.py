import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
import requests
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
codigo = st.text_input(label='',placeholder='Insira o Código do produto')
descricao = st.text_input(label='',placeholder='Insira uma descirção do produto')
col1,col2,col3 = st.columns(3)


@st.dialog(f"Deseja realmente excluir o produtos") 
def exclusao():
    requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
    roteiro = requiscao.json()
    dados = roteiro['Produtos']
    lista_nomes = []
    for item in dados:
            item_estoque = dados[f'{item}']
            for elemento in item_estoque:
                espec = item_estoque[f'{elemento}']
                st.write(espec)
   # produto_excluir = st.selectbox(label='Selecione o produto',options=lista_nomes,index=None)
    if produto_excluir:
        lista_verificada = []
        for item in dados:

            veiculo_ref = db.reference(f'Produtos/{produto_excluir}')
            veiculo_ref.delete()
            st.success(f'Produto {produto_excluir} excluido')
    else:
        st.info(f'Você realmente deseja excluir o produto {produto_excluir}')


with col1:
    localizacao = st.text_input(label='',placeholder='Insira a localização')
    
with col2:  
    quantidade = st.number_input(label='',placeholder='Insira a quantidade')
with col3:
    foto = st.text_input(label='',placeholder='Insira a foto do Produto')
    col=localizacao[3:6]
    Prat=localizacao[0:2]
    alt = localizacao[7:]
    if len(col) != 3 or len(alt)!= 2 or len(Prat)!=2:
        st.error(f'A posição {localizacao} está incorreta. Insira-a novamente')
        localizacao = ''
    excluir = st.button('Excluir Produtos')
    if excluir:
        exclusao()
ref = db.reference('Produtos')
if codigo and descricao and quantidade and foto and localizacao:
    with col1:
        cadastro = st.button('Cadastar Produtos')
        if cadastro:
            dict_produto = {'Código':codigo,'Quantidade':quantidade,'Foto':foto,'Descrição':descricao}
            try:
                ref.child(codigo).push().set(dict_produto)
                st.success(f'Protudo de código: {codigo} cadastrado com sucesso')
            except:
                st.error('Não há saida de dados disponível')
