
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
import requests
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requiscao.json()
dados = roteiro['Estoque']
@st.dialog(f"Atenção") 
def alerta(item):
    st.warning(f'O item: {item} não conta no cadastro, Deseja continuar:')
    botao_sim = st.button('Sim')
    if botao_sim:
      descricao = st.text_input(label='',placeholder='Insira uma descrição')
      deposito_ref = db.reference('Depósito')
      caminho = f'Rec/{item}'
      
      Estoque_ref = db.reference('Estoque')
      caminho_estoque = f'{item}'
    
    # Adicionando dados
      deposito_ref.child(caminho).set({
          'quantidade': quantidade  # Exemplo de dado adicional
      })
      Estoque_ref.child(caminho_estoque).set({
          'Descrição': descricao,
          'foto':None# Exemplo de dado adicional
      })
      st.success('Deu certo')
lista_produtos = []
for item in dados:
                if item in lista_produtos:
                      pass
                else:
                      lista_produtos.append(item)
tab1,tab2 = st.tabs(['Alimentação Manual','Alimentação de itens da nota'])
with tab1:
  item = st.text_input(label='',placeholder='Insira um item')
  if item not in lista_produtos:
    alerta(item)
  quantidade = st.number_input(placeholder=f'Insira a quantidade do item',value=None,label='')
  if item and quantidade:
    botao_adicionar = st.button(f'Adicionar Item: {item}')
    if botao_adicionar:
      deposito_ref = db.reference('Depósito')
      caminho = f'Rec/{item}'
    
    # Adicionando dados
      deposito_ref.child(caminho).set({
          'quantidade': quantidade  # Exemplo de dado adicional
      })
      st.success(f'Item {item} adicionado com sucesso')
  
